from bson import ObjectId
from bson.errors import InvalidId
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.config import config
from src.db.models import Conversations, Personas, ProfileInfos, Prompts
from uuid import UUID
import requests
from src.db.schemas import User
from src.logger import Logger

logger = Logger("db_utils")


def valid_profile_id(profile_id: str):
    try:
        ObjectId(profile_id)
        profile = ProfileInfos.objects(profileId=profile_id).first()
        assert profile
        return profile_id
    except Exception as e:
        handle_error(e)


def valid_persona_id(persona_id: str):
    try:
        ObjectId(persona_id)
        persona = Personas.objects(id=persona_id).first()
        assert persona
        return persona_id
    except Exception as e:
        handle_error(e)


def valid_prompt_id(id: str):
    try:
        ObjectId(id)
        prompt = Prompts.objects(id=id).first()
        assert prompt
        return id
    except Exception as e:
        handle_error(e)


def valid_conversation_id(conversation_id: str):
    try:
        UUID(conversation_id, version=4)
        conversation = Conversations.objects(conversationId=conversation_id).first()
        assert conversation
        return conversation_id
    except Exception as e:
        handle_error(e)


def valid_agent_id(agent_id: str | None = None):
    try:
        if agent_id:
            ObjectId(agent_id)
        return agent_id
    except Exception as e:
        handle_error(e)


def authenticate_user(token: str) -> dict:  # type: ignore
    try:
        resp = requests.get(
            f"{config['NODE_BACKEND']}/user/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        if resp.status_code == 200:
            x_org_id = resp.headers.get("x-org-id")
            return {
                "status": 200,
                "message": "Authentication successful",
                "user_info": resp.json(),
                "x_org_id": x_org_id,
                "auth_token": token,  # TODO: Potentially Bad but this return value is only used internally.
            }
        else:
            return {
                "status": 400,
                "message": "Authentication failed",
            }
    except Exception as e:
        handle_error(e)


# TODO: Make this better
def handle_error(e: Exception):
    logger.error(e, stack_info=True, exc_info=True)
    try:
        raise e
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
