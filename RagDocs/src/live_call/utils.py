from asyncio import CancelledError
import asyncio
import json
from uuid import uuid4
from fastapi import HTTPException, WebSocketException, WebSocket, status
import openai
import requests
from os.path import join

from recallAI import RecallAI

from src.config import config
from src.db.models import Transcripts
from src.db.schemas import Conversation
from src.db.utils import authenticate_user
from src.enums import CallTypes
from src.logger import Logger
from src.utils.prompt_formatter import PromptTemplate
from src.utils.prompts import get_prompt
from src.integrations.email_provider.smtp.router import send_email, EmailRequest
from src.integrations.hubspot.objects import create_engagement, edit_object
from vocode.streaming.telephony import conversation

logger = Logger("live_call")

def generate_random_string():
    return str(uuid4())


async def validate_websocket_connection(websocket: WebSocket):
    auth_token = websocket.query_params.get("Authorization")
    if not auth_token:
        logger.error("No Auth token in Websocket")
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION, reason="No Auth token in Websocket"
        )

    # Validate the auth token
    auth_response = authenticate_user(auth_token)
    if auth_response.get("status") != 200:
        logger.error("Invalid Auth token in Websocket")
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="Invalid Auth token in Websocket",
        )

    # Extract meeting_link from the query parameter
    meeting_link = websocket.query_params.get("meeting_link")
    if not meeting_link:
        logger.error("No meeting_link in Websocket")
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION, reason="No meeting_link in Websocket"
        )

    # Extract meeting_link from the query parameter
    conversation_id = websocket.query_params.get("conversation_id")
    if not conversation_id:
        logger.error("No conversation_id in Websocket")
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="No conversation_id in Websocket",
        )

    return auth_response

def is_zoom_meeting_service_running():
    try:
        response = requests.get(config["ZOOM_MEETING_BOT_API_BASE_URL"])
        return response.status_code == 200
    except Exception as e:
        print(f"Error checking zoom meeting boot service service status: {str(e)}")
        return False

async def connect_recall_bot(meeting_link: str, conversationId: str, agent_name: str):
    recall = RecallAI()
    recall.connect_bot(
        {"meeting_url": meeting_link},
        config["RECALL_TRANSCRIPTION_URL"] + conversationId,
    )
    error= None
    
    while True:
        response = recall.get_bot()
        if len(response.get("meeting_participants", [])) > 0:
            participant_names = [
                i["name"] for i in response["meeting_participants"]
            ]
            if agent_name in participant_names:
                break
            else:
                error = {
                    "event": "error",
                    "msg": f"agent_name ({agent_name}) not present in the meeting.",
                }
                recall.leave_meeting()
                break
        else:
            await asyncio.sleep(0.1)
            
    # TODO: Remove this commented block when we fully switch-over to recall.
    # zoom_bot_response = await start_zoom_recording_bot(
    #     meeting_link, conversation.conversationId
    # )

    # if zoom_bot_response.get("status") != 200:
    #     await websocket.send_text(
    #         "Zoom recording bot failed to join the meeting!"
    #     )
    #     logger.error(
    #         "log message from bot worker: ", zoom_bot_response["message"]
    #     )
    #     logger.error(f"Zoom recording bot failed to join the meeting!")
    #     raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    
    return recall, error


async def start_zoom_recording_bot(meeting_link: str, conversationId: str):
    try:
        payload = json.dumps(
            {
                "meetingUrl": meeting_link,
                "botName": "jivi",
                "conversationId": conversationId,
            }
        )

        headers = {"Content-Type": "application/json"}

        resp = requests.post(
            f"{config['ZOOM_BOT_BACKEND']}/join-zoom",
            headers=headers,
            data=payload,
        )

        if resp.status_code == 200:
            return {"status": 200, "message": "Zoom recording bot started successfully"}
        else:
            return {
                "status": 400,
                "message": "Error starting zoom recording bot",
            }
    except Exception as e:
        return {
            "status": 400,
            "message": f"Error starting zoom recording bot {e}",
        }

async def update_hubspot_and_send_email(conversation: Conversation, auth_token: str):
    conversation_summary = live_call_summary_generation(conversationId=Conversation.conversationId)
    await edit_object("contacts", conversation.profileInfo.hubspotInfo.hs_object_id, { # type: ignore
        "properties": {
            "notes": conversation.profileInfo.hubspotInfo.notes + "\n" + conversation_summary['callSummary'], # type: ignore
            "email": conversation.profileInfo.hubspotInfo.email + "\n _____________________" + # type: ignore
                    "subject: minutes of meeting" + "\n" +
                    conversation.profileInfo.hubspotInfo.notes + '\n Action Item: \n' + conversation.profileInfo.hubspotInfo.task # type: ignore
        }
    }, auth_token=auth_token);

    # Create an EmailRequest object
    email_request = EmailRequest(
        to=conversation.profileInfo.hubspotInfo.email, # type: ignore
        subject="minutes of meeting",
        message=conversation.profileInfo.hubspotInfo.notes + '\n Action Item: \n' + conversation.profileInfo.hubspotInfo.task # type: ignore
    )

    await send_email(
        email_request=email_request,
        auth_token=auth_token
    )
    
async def finish_task(task):
    logger.debug(f"Canceling {task}")
    if task:
        task.cancel()
        try:
            return await task  # Wait for the task to complete
        except CancelledError:
            return  # Ignore the cancellation error


async def close_websocket(websocket: WebSocket):
    await websocket.close()
    logger.debug("WebSocket connection closed.")


def live_call_summary_llm(prompt):
    with open(
        join(config["PARAMETER_SCHEMAS_PATH"], "live_call_summary_schema.json"), "r"
    ) as schema_file:
        call_summary_schema = json.load(schema_file)
    messages = [
        {"role": "system", "content": "you are a virtual assistant"},
        {"role": "user", "content": prompt},
    ]
    completion = openai.chat.completions.create(
        model=config["LIVE_CALL_SUMMARY_MODEL_NAME"],
        messages=messages,
        functions=[{"name": "generate_response", "parameters": call_summary_schema}],
        function_call={"name": "generate_response"},
        temperature=config["LIVE_CALL_SUMMARY_TEMPERATURE"],
        top_p=config["LIVE_CALL_SUMMARY_TOP_P"],
        frequency_penalty=config["LIVE_CALL_SUMMARY_FREQUENCY_PENALTY"],
        presence_penalty=config["LIVE_CALL_SUMMARY_PRESENCE_PENALTY"],
        max_tokens=config["LIVE_CALL_SUMMARY_MAX_TOKENS"],
    )

    raw_data_str = completion.choices[0].message.function_call.arguments  # type: ignore # TODO: function_call is deprecated.
    llm_response = json.loads(raw_data_str)

    return llm_response


def live_call_summary_generation(conversationId: str):
    def format_transcripts(transcripts):
        if not transcripts:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "No transcripts Found.")
        combined_transcript = [transcripts[0]]
        for t in transcripts[1:]:
            if t["speaker"] == combined_transcript[-1]["speaker"]:
                transcript_copy = dict(combined_transcript[-1])
                transcript_copy["transcript"] += " " + t["transcript"]
                combined_transcript[-1] = transcript_copy
            else:
                combined_transcript.append(t)
        formatted_transcript = [
            f'{t["speaker"]}: {t["transcript"]}' for t in combined_transcript
        ]
        return " \n\n".join(formatted_transcript)

    transcripts = Transcripts.objects(conversationId=conversationId).first().turns
    live_call_summary_prompt = PromptTemplate(
        get_prompt(
            promptType="summary",
            callType=CallTypes.LIVE_CALL,
            defaultPromptFile="live_call_summary_prompt.txt",
        )
    )
    live_call_summary_prompt = live_call_summary_prompt.fill_slots(
        {
            "call_transcript": format_transcripts(transcripts),
        }
    )

    call_summary = live_call_summary_llm(live_call_summary_prompt)
    return call_summary





def ai_agent_summary_generation(conversation):
    def format_transcripts(transcripts):
        if not transcripts:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "No transcripts Found.")
        combined_transcript = [transcripts[0]]
        for t in transcripts[1:]:
            if t["role"] == combined_transcript[-1]["role"]:
                transcript_copy = dict(combined_transcript[-1])
                transcript_copy["message"] += " " + t["message"]
                combined_transcript[-1] = transcript_copy
            else:
                combined_transcript.append(t)
        formatted_transcript = [
            f'{t["role"]}: {t["message"]}' for t in combined_transcript
        ]
        return " \n\n".join(formatted_transcript)
    live_call_summary_prompt = PromptTemplate(
        get_prompt(
            promptType="summary",
            callType=CallTypes.LIVE_CALL,
            defaultPromptFile="live_call_summary_prompt.txt",
        )
    )
    formatted_transcripts = format_transcripts(conversation.get('transcripts'))
    live_call_summary_prompt = live_call_summary_prompt.fill_slots(
        {
            "call_transcript": formatted_transcripts,
        }
    )

    call_summary = live_call_summary_llm(live_call_summary_prompt)
    return call_summary

async def update_hubspot_and_send_email_ai_agent(conversation, auth_token: str):
    conversation_summary = ai_agent_summary_generation(conversation=conversation)

    hubspotInfo = conversation.get('hubspotInfo')
    hs_object_id = hubspotInfo.get('hs_object_id')
    email = hubspotInfo.get('email')
    email_chain = hubspotInfo.get('email_chain') or ""
    
    note_data = {
        "engagement": {
            "active": True,
            "type": "NOTE"
        },
        "associations": {
            "contactIds": [hs_object_id],
            "companyIds": [],
            "dealIds": [],
            "ownerIds": []
        },
        "metadata": {
            "body": conversation_summary['callSummary']
        }
    }
    
    await create_engagement(data=note_data, auth_token=auth_token);
    
    # await edit_object("contacts", hs_object_id, { # type: ignore
    #     "properties": {
    #         "email_chain": email_chain + "\n _____________________" + # type: ignore
    #                 "subject: minutes of meeting" + "\n" +
    #                 conversation_summary['callSummary'] # type: ignore
    #     }
    # }, auth_token=auth_token);

    # Create an EmailRequest object
    email_request = EmailRequest(
        to=email, # type: ignore
        subject="minutes of meeting",
        message=conversation_summary['callSummary'] # type: ignore
    )

    await send_email(
        email_request=email_request,
        auth_token=auth_token
    )
    
    # Sample object for logging email with engagement api
    # email_data = {
    #     "engagement": {
    #         "active": True,
    #         "type": "EMAIL",
    #         "timestamp": 1640995200000 
    #     },
    #     "associations": {
    #         "contactIds": [60351639171],
    #         "companyIds": [],
    #         "dealIds": [],
    #         "ownerIds": []
    #     },
    #     "metadata": {
    #         "from": "sender@gmail.ai",
    #         "to": ["receiver@gmail.com"],
    #         "subject": "Follow-up on our recent conversation",
    #         "text": "Hello, here's a summary of our conversation and next steps."
    #     }
    # }
