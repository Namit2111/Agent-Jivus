import json
from os.path import join
from fastapi import HTTPException, status
import openai

from src.config import config
from src.db.subroutes.conversations import get_base_conversation
from src.db.models import Personas, Transcripts
from src.enums import CallTypes
from src.utils.prompt_formatter import PromptTemplate
from src.utils.prompts import get_prompt

openai.api_key = config["OPENAI_API_KEY"]


def training_call_summary_llm(prompt):
    with open(
        join(config["PARAMETER_SCHEMAS_PATH"], "training_call_summary_schema.json"), "r"
    ) as schema_file:
        call_summary_schema = json.load(schema_file)
    messages = [
        {"role": "system", "content": "you are a virtual assistant"},
        {"role": "user", "content": prompt},
    ]
    completion = openai.chat.completions.create(
        model=config["TRAINING_CALL_SUMMARY_MODEL_NAME"],
        messages=messages,
        functions=[{"name": "generate_response", "parameters": call_summary_schema}],
        function_call={"name": "generate_response"},
        temperature=config["TRAINING_CALL_SUMMARY_TEMPERATURE"],
        top_p=config["TRAINING_CALL_SUMMARY_TOP_P"],
        frequency_penalty=config["TRAINING_CALL_SUMMARY_FREQUENCY_PENALTY"],
        presence_penalty=config["TRAINING_CALL_SUMMARY_PRESENCE_PENALTY"],
        max_tokens=config["TRAINING_CALL_SUMMARY_MAX_TOKENS"],
    )

    raw_data_str = completion.choices[0].message.function_call.arguments  # type: ignore # TODO: function_call is deprecated.
    llm_response = json.loads(raw_data_str)

    return llm_response


def training_call_summary_generation(conversation_id: str):
    def format_transcripts(transcripts, user_name, prospect_name):
        if not transcripts:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "No transcripts Found.")
        formatted_transcript = []
        for t in transcripts:
            if t["speaker"] == "user":
                formatted_transcript.append(f"{user_name} : {t['transcript']}")
            elif t["speaker"] == "assistant":
                formatted_transcript.append(f"{prospect_name} : {t['transcript']}")
        return " \n\n".join(formatted_transcript)

    conversation = get_base_conversation(conversation_id=conversation_id)
    user_name = "Agent"
    persona = get_persona(persona_id=conversation.persona.id)
    training_call_summary_prompt = PromptTemplate(
        get_prompt(
            promptType="summary",
            callType=CallTypes.TRAINING_CALL,
            persona=persona,
            defaultPromptFile="training_call_summary_prompt.txt",
        )
    )
    training_call_summary_prompt = training_call_summary_prompt.fill_slots(
        {
            "call_transcript": format_transcripts(
                Transcripts.objects(conversationId=conversation_id).first().turns,
                user_name,
                (
                    Personas.objects(id=conversation.persona.id).first().personaName
                    if conversation.callType == CallTypes.TRAINING_CALL
                    else conversation.profileInfo.linkedinInfo.data["full_name"]
                ),
            ),
        }
    )

    call_summary = training_call_summary_llm(training_call_summary_prompt)
    return call_summary
