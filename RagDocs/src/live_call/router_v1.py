from re import A
from urllib import response
from fastapi import (
    APIRouter,
    Depends,
    WebSocket,
    WebSocketDisconnect,
    HTTPException,
    status,
)
from aio_pika import connect, ExchangeType, exceptions
from fastapi.security import OAuth2PasswordBearer
import asyncio
import json
from datetime import datetime, time
import pytz


from src.db.models import Conversations, Summaries
from src.db.subroutes.conversations import read_conversation
from src.db.subroutes.profile_info import create_profile_from_linkedin_url
from src.db.subroutes.conversations import create_conversation
from src.db.schemas import Conversation, ConversationsResponse, ProfileInfo
from src.db.subroutes.summaries import create_summary, update_summary
from src.enums import CallTypes, Dialers, ProfileTypes
from src.integrations.email_provider.gmail.router import send_email
from src.integrations.hubspot.objects import edit_object, get_object_by_id
from src.live_call.llm_agent import LLMAgent
from src.db.utils import authenticate_user, handle_error
from src.config import config
from src.live_call.schemas import SetupParams
from src.logger import Logger
from src.live_call.utils import (
    close_websocket,
    connect_recall_bot,
    finish_task,
    generate_random_string,
    is_zoom_meeting_service_running,
    live_call_summary_generation,
    update_hubspot_and_send_email,
    validate_websocket_connection,
)

logger = Logger("live_call")
router = APIRouter(prefix="/v1/live-call", tags=["live-call"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/setup", response_model=ConversationsResponse)
async def setup_live_call(
    setupParams: SetupParams, auth_token: str = Depends(oauth2_scheme)
):
    try:
        auth_response = authenticate_user(auth_token)
        if auth_response.get("status") != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=auth_response.get("message", "Invalid user auth token"),
            )
        user_id = auth_response.get("user_info").get("id")  # type:ignore
        hubspotInfo = await get_object_by_id("contacts", setupParams.hsContactID, 'email,email_chain,notes', auth_token=auth_token)
        profileInfo = create_profile_from_linkedin_url(
            setupParams.linkedinUrl, ProfileTypes.USER, hubspotInfo=hubspotInfo["properties"]
        )
        new_conversation = Conversation(
            conversationId=generate_random_string(),
            userId=user_id,
            callType=CallTypes.LIVE_CALL,
            callScenario="discovery_call",
            dialer=Dialers.ZOOM,
            profileInfo=profileInfo,
            metadata={
                "desiredOutcome": setupParams.desiredOutcome
            },
        )
        conversation = create_conversation(new_conversation)

        return conversation
    except Exception as e:
        handle_error(e)


@router.websocket("/zoom")
async def zoom_live_call_stream(
    websocket: WebSocket,
    auth_response: dict = Depends(validate_websocket_connection),
):
    await websocket.accept()
    logger.debug("WebSocket connection accepted")

    # Send connection acknowledgment
    await websocket.send_text("Connection open")

    agent_name = auth_response["user_info"].get("name")
    conversation_id = websocket.query_params["conversation_id"]
    meeting_link = websocket.query_params["meeting_link"]
    llm_agent_started = False
    llm_agent = None
    bot_left_meeting = False
    bot = None
    try:
        while True:
            message_str = await asyncio.wait_for(websocket.receive_text(), timeout=2700)
            message = json.loads(message_str)
            event = message.get("event")
            logger.debug(
                f"Received message: {message} | event: {event} | conversation_id: {conversation_id}"
            )
            if event == "start" and not llm_agent_started:
                llm_agent_started = True
                logger.debug(f"zoom meeting link: {meeting_link}")

                conversation = read_conversation(conversation_id)
                
                # Check if current time is within the allowed range
                if is_zoom_meeting_service_running():
                    logger.debug("Zoom meeting bot is available.")
                else:
                    logger.debug("Zoom meeting bot not available switching to recall bot.")
                    bot, error = await connect_recall_bot(
                        meeting_link=meeting_link,
                        conversationId=conversation_id,
                        agent_name=agent_name
                    )
                    
                    if error is not None and 'event' in error and error['event'] == "error":                   
                        logger.error(error['msg'])
                        await websocket.send_json(
                            {
                                "event": "error",
                                "msg": error['msg'],
                            }
                        )
                        bot.leave_meeting()
                        bot_left_meeting = True
                        raise Exception(error['msg'])
               
                await websocket.send_json(
                    {
                        "event": "status_change",
                        "msg": "Meeting started",
                    }
                )
                logger.info("Meeting started")

                live_nudge_task = asyncio.create_task(
                    insight_consume_and_send_messages(
                        str(conversation.conversationId),
                        config["RABBITMQ_URL"],
                        f"insight_queue_{conversation.conversationId}",
                        websocket,
                    )
                )
                logger.debug(f"live_nudge_task started: {live_nudge_task}")

                llm_agent = LLMAgent(
                    api_key=config["OPENAI_API_KEY"],
                    conversation=conversation,
                    model=config["LLMAGENT_MODEL_NAME"],
                    alt_insight_pipeline=config["LLMAGENT_ALT_INSIGHT_PIPELINE"],
                    stream_output=config["LLMAGENT_STREAM_OUTPUT"],
                    ignore_agent_transcriptions=config[
                        "LLMAGENT_IGNORE_AGENT_TRANSCRIPTIONS"
                    ],
                    previous_insight_handling=config[
                        "LLMAGENT_PREVIOUS_INSIGHT_HANDLING"
                    ],
                )
                transcript_consumer_task, _ = await start_transcript_consumer(
                    queue_name=f"transcript_queue_{conversation.conversationId}",
                    conversation=conversation,
                    agent_name=agent_name,
                    llm_agent=llm_agent,
                )

            elif event == "stop" and llm_agent_started:
                await finish_task(transcript_consumer_task)
                await finish_task(live_nudge_task)
                await websocket.send_json(
                    {
                        "event": "status_change",
                        "msg": "Stopped",
                    }
                )
                break  # Break the loop to end the WebSocket connection
            else:
                logger.error(
                    f"Unhandled event or state: {event}, llm_agent_started: {llm_agent_started}"
                )

            await asyncio.sleep(0.1)
            
        
        # send_meeting_notes()
        # update_hubspot(conversation_id, auth_response)
            

    except WebSocketDisconnect:
        await finish_task(transcript_consumer_task)
        await finish_task(live_nudge_task)
        logger.error("WebSocket connection closed by client.")

    except asyncio.TimeoutError:
        logger.error("Timeout waiting for client message.")
        await finish_task(live_nudge_task)

    # except Exception as e:
    #     logger.error(f"Unexpected error: {e}")

    finally:
        await update_hubspot_and_send_email(conversation=conversation, auth_token=auth_response['auth_token'])
        logger.info("Cleaned up everything after Call")
        if not bot_left_meeting:
            bot.leave_meeting() # ignore: type
        del llm_agent
        await close_websocket(websocket)

# async def send_meeting_notes():
    
    
# async def update_hubspot(conversation_id, auth_response):
    
    
        

async def transcript_rabbitmq_consumer(
    rabbitmq_url,
    queue_name: str,
    conversation: Conversation,
    agent_name: str,
    llm_agent: LLMAgent,
):
    queue = None
    channel = None
    connection = None
    # Create a cancellation event for the consumer
    cancellation_event = asyncio.Event()
    try:
        connection = await connect(rabbitmq_url)
        async with connection:
            channel = await connection.channel()
            # Declare an exchange
            exchange = await channel.declare_exchange(
                "live_call_agent", ExchangeType.DIRECT, durable=False, auto_delete=True
            )

            # Declare and bind the queue
            queue = await channel.declare_queue(queue_name, auto_delete=True)
            await queue.bind(
                exchange, routing_key=f"transcript_{conversation.conversationId}"
            )

            logger.info(
                f"transcript rabbitmq_consumer started for queue {queue_name} | key = transcript_{conversation.conversationId}"
            )

            # Initialize a single instance of LLMAgent.
            lock = asyncio.Lock()

            await llm_agent.start_conversation(agent_name=agent_name)

            logger.info(f"transcript rabbitmq_consumer llm setup completed")

            async def on_message(message):
                async with message.process():
                    logger.debug(
                        f"Triggered on_message for message: {message.body.decode('utf-8')}"
                    )
                    async with lock:

                        # Decode message body from bytes to string
                        message_body_str = message.body.decode("utf-8")

                        # Deserialize string to a Python dictionary
                        message_data = json.loads(message_body_str)

                        if not message_data.get("transcript"):
                            message_data["transcript"] = " ".join(
                                [word["text"] for word in message_data["words"]]
                            )

                        logger.debug(f"Inside Lock for Message: {message_data}")
                        logger.start_latency_timer()

                        await llm_agent.add_new_transcript(
                            message_data,
                            use_simplification=True,  # TODO: remove 'use_simplification'
                        )

                        logger.log_latency("Insight for new Transcript")
                        logger.debug(f"LLMAgent finished for message: {message_data}")

                        return None

            # Start consuming messages
            async with queue.iterator() as q:
                async for message in q:
                    if cancellation_event.is_set():
                        return None

                    await on_message(message)

    except asyncio.CancelledError:
        # The task was cancelled, set the cancellation event
        cancellation_event.set()
        logger.debug("Transcript Consumer has been cancelled.")
        # Clean up resources
    except Exception as e:
        logger.error(e)
    finally:
        # Clean up resources that need to be cleaned up
        # regardless of whether there was an exception or not
        if queue:
            await queue.unbind(exchange, f"transcript_{conversation.conversationId}")
        if channel:
            await channel.close()
        if connection:
            await connection.close()
        await llm_agent.cancel_insight_task()
        logger.debug(f"Cleaned up resources for queue {queue_name}")


async def start_transcript_consumer(
    queue_name: str, conversation: Conversation, agent_name: str, llm_agent: LLMAgent
):
    task_name = f"transcript-consumer-{conversation.conversationId}"
    all_task_names = [t.get_name() for t in asyncio.all_tasks()]
    if task_name in all_task_names:
        logger.error("queue name in consumer task ... so exiting ...")
        raise HTTPException(
            status_code=400, detail="Consumer already running for this queue."
        )

    task = asyncio.create_task(
        transcript_rabbitmq_consumer(
            config["RABBITMQ_URL"], queue_name, conversation, agent_name, llm_agent
        ),
        name=task_name,
    )
    return task, {
        "message": f"Consumer started for queue: {queue_name}, conversation_id: {conversation.conversationId}"
    }


async def insight_consume_and_send_messages(
    conversation_id: str, rabbitmq_url, queue_name: str, websocket: WebSocket
):
    try:
        connection = await connect(rabbitmq_url)
        async with connection:
            channel = await connection.channel()

            # Declare an exchange
            exchange = await channel.declare_exchange(
                "live_call_agent", ExchangeType.DIRECT, durable=False, auto_delete=True
            )
            logger.debug(
                f"insight_consume_and_send_messages started for queue {queue_name}"
            )

            # Declare the queue
            queue = await channel.declare_queue(queue_name, auto_delete=True)

            # Bind the queue to the exchange with the routing key
            await asyncio.ensure_future(
                queue.bind(exchange, routing_key=f"insight_{conversation_id}")
            )
            logger.debug(f"insight_queue is bound to {conversation_id}")

            # Create a cancellation event for the consumer
            cancellation_event = asyncio.Event()

            async def on_message(message):
                async with message.process():
                    # Decode message body from bytes to string
                    message_body_str = message.body.decode("utf-8")

                    # Deserialize string to a Python dictionary
                    message_data = json.loads(message_body_str)

                    logger.debug(f"message data: {message_data}")

                    live_nudge_response = {
                        "event": "live_nudge",
                        "data": message_data,
                    }

                    logger.debug(f"conversation_id: {conversation_id}")

                    # Send the message data over the WebSocket
                    await websocket.send_json(live_nudge_response)

            # Start consuming messages
            async with queue.iterator() as q:
                async for message in q:
                    if cancellation_event.is_set():
                        return None
                    await on_message(message)

    except asyncio.CancelledError:
        # The task was cancelled
        cancellation_event.set()
        logger.debug("Insight Consumer has been cancelled.")
    except exceptions.ChannelClosed as e:
        logger.error(
            f"ChannelClosed: Cleaning up resources for queue {queue_name} | reason: {e.reason}"
        )
    except Exception as e:
        logger.error(e)
    finally:
        # Clean up resources
        if queue:
            await queue.unbind(exchange, f"insight_{conversation_id}")
        if channel:
            await channel.close()
        if connection:
            await connection.close()
        logger.debug(f"Cleaned up resources for queue {queue_name}")
