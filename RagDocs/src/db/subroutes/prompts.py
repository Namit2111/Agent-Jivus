from datetime import datetime
from src.enums import UserRoles
from src.logger import Logger
from src.db.schemas import PromptCreationInput, PromptResponse, PromptUpdateInput
from src.db.utils import handle_error, valid_prompt_id
from src.db.models import Prompts
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.utils.auth import get_auth_response
from src.utils.prompts import resolve_prompt_name

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix="/prompts", tags=["prompts"])
logger = Logger("prompts")


def ensure_admin_user(auth_response=Depends(get_auth_response)):
    current_user_role = auth_response["user_info"]["role"]
    if (
        current_user_role == UserRoles.ADMIN.value
        or current_user_role == UserRoles.SUPER_ADMIN.value
    ):
        return auth_response
    else:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="You are not an ADMIN."
        )


def get_prompt(id: str = Depends(valid_prompt_id)) -> Prompts:
    prompt = Prompts.objects(id=id).first()
    assert prompt
    return prompt


# TODO: List Prompts
@router.get("/list", response_model=list[PromptResponse])
async def list_prompts(auth_response: str = Depends(ensure_admin_user)):
    try:
        prompts = Prompts.objects().order_by("-updatedAt")
        prompts = [
            PromptResponse(**prompt.to_mongo(use_db_field=False)) for prompt in prompts
        ]
        return prompts
    except Exception as e:
        handle_error(e)


@router.get("/{id}", response_model=PromptResponse)
def read_prompt(
    id: str = Depends(valid_prompt_id), auth_response: str = Depends(ensure_admin_user)
):
    try:
        prompt = get_prompt(id)
        return PromptResponse(**prompt.to_mongo(use_db_field=False))
    except Exception as e:
        handle_error(e)


@router.post("/", response_model=PromptResponse)
def create_prompt(
    prompt: PromptCreationInput,
    auth_response: str = Depends(ensure_admin_user),
):
    try:
        promptName = resolve_prompt_name(
            promptType=prompt.promptType,
            callType=prompt.callType.value,
            callScenario=prompt.callScenario,  # type: ignore
            difficultyLevel=prompt.difficultyLevel,  # type: ignore
        )
        promptDoc = Prompts(
            name=promptName,
            body=prompt.body,
            modelSettings=prompt.modelSettings,
        )
        promptDoc = promptDoc.save()
        return PromptResponse(**promptDoc.to_mongo(use_db_field=False))
    except Exception as e:
        handle_error(e)


@router.put("/{id}", response_model=PromptResponse)
def update_prompt(
    id: str,
    new_prompt: PromptUpdateInput,
    auth_response: str = Depends(ensure_admin_user),
):
    try:
        prompt = get_prompt(id)
        prompt_update_status = prompt.modify(
            body=new_prompt.body,
            modelSettings=new_prompt.modelSettings,
            updatedAt=datetime.now(),
        )
        prompt.reload()
        if prompt_update_status:
            return PromptResponse(**prompt.to_mongo(use_db_field=False))
        else:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail="Unable to Update Prompt",
            )
    except Exception as e:
        handle_error(e)


@router.delete("/{id}")
def delete_prompt(
    id: str = Depends(valid_prompt_id), auth_response: str = Depends(ensure_admin_user)
):
    try:
        prompt = get_prompt(id)
        prompt.delete()
        return {"message": "success"}
    except Exception as e:
        handle_error(e)
