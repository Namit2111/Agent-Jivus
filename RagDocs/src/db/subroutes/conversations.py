from math import ceil
from typing import Annotated
from datetime import datetime
from fastapi import Depends, HTTPException, Query, status, APIRouter
from fastapi.security import OAuth2PasswordBearer

from src.db.schemas import (
    Conversation,
    ConversationsListResponse,
    ConversationsResponse,
    Persona,
    PageParams,
    ProfileInfo,
)
from src.db.utils import (
    authenticate_user,
    handle_error,
    valid_conversation_id,
    valid_agent_id,
)
from src.enums import CallTypes, UserRoles
from src.db.models import Conversations, LiveInsights, Summaries, Transcripts

router = APIRouter(prefix="/conversations", tags=["conversations"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_base_conversation(conversation_id: str = Depends(valid_conversation_id)):
    return Conversations.objects(conversationId=conversation_id).first()


def get_conversation(conversation_id: str = Depends(valid_conversation_id)):
    return Conversations.objects(conversationId=conversation_id).first().full()


@router.get("/user")
async def list_conversations(
    call_type: CallTypes,
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1)] = 20,
    agent_id: str | None = Depends(valid_agent_id),
    auth_token: str = Depends(oauth2_scheme),
) -> ConversationsListResponse:  # type: ignore
    try:
        auth_response = authenticate_user(auth_token)
        if auth_response.get("status") != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=auth_response.get("message", "Invalid user auth token"),
            )
        current_user_role: str = auth_response["user_info"].get("role")
        current_user_id = auth_response["user_info"].get("id")

        if agent_id:
            if current_user_role == UserRoles.MANAGER.value:
                current_user_subordinates = auth_response["user_info"].get(
                    "subordinates"
                )
                current_user_subordinates = [
                    str(subordinate["id"]) for subordinate in current_user_subordinates
                ]
                if agent_id not in current_user_subordinates:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Requested user is not your subordinate",
                    )
                conversations_query = Conversations.objects(
                    userId=agent_id, callType=call_type
                )
                total = conversations_query.count()
                conversations = (
                    conversations_query.skip(size * (page - 1))
                    .order_by("-updatedAt")
                    .limit(size)
                    .full()
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="You are not a Manager",
                )
        else:
            conversations_query = Conversations.objects(
                userId=current_user_id, callType=call_type
            )
            total = conversations_query.count()
            conversations = (
                conversations_query.order_by("-updatedAt")
                .skip(size * (page - 1))
                .limit(size)
                .full()
            )

        conversations = [
            ConversationsResponse(**conversation.to_mongo(use_db_field=False))
            for conversation in conversations
        ]
        pageParam = PageParams(
            totalItems=total, totalPages=ceil(total / size), page=page, size=size
        )

        return ConversationsListResponse(
            conversations=conversations, pageParam=pageParam
        )
    except Exception as e:
        handle_error(e)


@router.get("/{conversation_id}", response_model=ConversationsResponse)
def read_conversation(conversation_id: str = Depends(valid_conversation_id)) -> Conversation:  # type: ignore
    try:
        conversation = get_conversation(conversation_id)
        return Conversation(**conversation.to_mongo(use_db_field=False))
    except Exception as e:
        handle_error(e)


@router.post("/", response_model=ConversationsResponse)
def create_conversation(conversation_in: Conversation) -> Conversation:  # type: ignore
    try:
        conversation = Conversations(
            conversationId=conversation_in.conversationId,
            userId=conversation_in.userId,
            dialer=conversation_in.dialer,
            callType=conversation_in.callType,
            callScenario=conversation_in.callScenario,
            callRecordingUrl=conversation_in.callRecordingUrl,
            callDuration=conversation_in.callDuration,
            callDateTime=conversation_in.callDateTime,
            persona=(
                (
                    conversation_in.persona.id
                    if type(conversation_in.persona) == Persona
                    else conversation_in.persona
                )
                if conversation_in.persona
                else None
            ),
            metadata=conversation_in.metadata,
            profileInfo=(
                (
                    conversation_in.profileInfo.id
                    if type(conversation_in.profileInfo) == ProfileInfo
                    else conversation_in.profileInfo
                )
                if conversation_in.profileInfo
                else None
            ),
        )
        conversation = conversation.save()
        LiveInsights(conversationId=conversation_in.conversationId).save()
        Transcripts(conversationId=conversation_in.conversationId).save()
        Summaries(conversationId=conversation_in.conversationId).save()
        conversation = conversation.full()
        return Conversation(**conversation.to_mongo(use_db_field=False))
    except Exception as e:
        handle_error(e)


@router.put("/{conversation_id}", response_model=ConversationsResponse)
def update_conversation(
    new_conversation: Conversation,
    conversation_id: str = Depends(valid_conversation_id),
):
    try:
        conversation = get_base_conversation(conversation_id)
        conversation_update_status = conversation.modify(
            updatedAt=datetime.now(),
            conversationId=new_conversation.conversationId,
            user=new_conversation.userId,
            persona=new_conversation.persona,
            callScenario=new_conversation.callScenario,
            dialer=new_conversation.dialer,
            callType=new_conversation.callType,
            callRecordingUrl=new_conversation.callRecordingUrl,
            callDuration=new_conversation.callDuration,
            callDateTime=new_conversation.callDateTime,
        )
        conversation.reload()

        if conversation_update_status:
            return Conversation(**conversation.to_mongo(use_db_field=False))
        else:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail="Unable to Update Transcript",
            )
    except Exception as e:
        handle_error(e)


@router.delete("/{conversation_id}")
def delete_conversation(conversation_id: str = Depends(valid_conversation_id)):
    try:
        conversation = get_base_conversation(conversation_id)
        conversation.delete()
        return {"message": "success"}
    except Exception as e:
        handle_error(e)
