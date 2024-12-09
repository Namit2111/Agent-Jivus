# TODO: More Refactoring
# 1. Remove usage of mongo models and package them to db folder and call via functions.

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import AnyUrl
from src.db.subroutes.conversations import create_conversation
from src.db.schemas import Conversation, LinkedInInfo, Persona, User
from src.db.subroutes.personas import get_persona
from src.db.subroutes.profile_info import patch_profile_linkedin
from src.pre_call.schemas import ConversationCreateReq
from src.enums import CallTypes
from src.db.models import ModelInfos
from src.pre_call.agent import (
    CustomRouter,
)
from src.logger import Logger
from src.pre_call.utils import (
    get_auth_response,
    linkedin_summary_generation,
    training_call_prompt_generation,
)
from src.pre_call.thunks import (
    AZURE_SYNTHESIZER_THUNK,
    DEEPGRAM_TRANSCRIBER_THUNK,
    CHATGPT_AGENT_THUNK,
)

logger = Logger("pre_call")


router = APIRouter(prefix="/v1/pre-call", tags=["pre-call"])

router.include_router(
    CustomRouter(
        transcriber_thunk=DEEPGRAM_TRANSCRIBER_THUNK,
        agent_thunk=CHATGPT_AGENT_THUNK,  # type: ignore
        synthesizer_thunk=AZURE_SYNTHESIZER_THUNK,
        logger=logger,
    ).get_router()
)


@router.post("/setup")
async def setup_conversation(
    conversation: ConversationCreateReq,
    auth_response: dict = Depends(get_auth_response),
):
    try:
        userId = auth_response.get("user_info").get("id")  # type:ignore
        persona = get_persona(conversation.personaId)
        if str(persona.userId) != userId:
            logger.error("Persona does not belong to the user")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Persona does not belong to the user",
            )

        training_call_prompt = training_call_prompt_generation(
            conversation.personaId, User(**auth_response["user_info"])
        )
        logger.debug(f"training_call_prompt: {training_call_prompt}")

        new_conversation = Conversation(
            conversationId=conversation.conversationId,
            userId=userId,
            callType=CallTypes.TRAINING_CALL,
            callScenario=persona.callScenario,
            persona=Persona(**persona.to_mongo(use_db_field=False)),
        )

        logger.debug(f"new_conversation: {new_conversation.model_dump()}")

        conversation_obj = create_conversation(new_conversation)

        modelInfo = ModelInfos(
            conversationId=conversation_obj.conversationId,
            systemPrompt=training_call_prompt,
        )
        modelInfo.save()
        return {"conversationId": str(conversation_obj.conversationId)}

    except Exception as e:
        # Handle other exceptions and return an appropriate error code
        logger.error(f"An error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {e}",
        )


@router.post("/fetch_linkedin")
def fetch_linkedin_info(linkedinUrl: str, profile_id: str):
    try:
        response, summary,buyingStyleInfo = linkedin_summary_generation(linkedinUrl)
        linkedIN_data = LinkedInInfo(url=linkedinUrl, data=response, summary=summary,buyingStyle=buyingStyleInfo)
        patch_profile_linkedin(linkedIN_data=linkedIN_data, profile_id=profile_id)
        return {"response": response, "summary": summary}
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
