from datetime import datetime
from src.db.schemas import LinkedInInfo, Persona, PersonasResponse
from src.utils.auth import get_auth_response
from src.db.utils import handle_error, valid_persona_id
from src.db.models import Personas
from fastapi import APIRouter, Depends, HTTPException, status

from src.enums import UserRoles

router = APIRouter(prefix="/personas", tags=["personas"])


def get_persona(persona_id: str = Depends(valid_persona_id)) -> Personas:
    return Personas.objects(id=persona_id).first()


@router.get("/user", response_model=list[PersonasResponse])
def read_personas_of_user(auth_response: dict = Depends(get_auth_response)):
    try:
        userId = auth_response["user_info"]["id"]
        personas = Personas.objects(userId=userId)
        return [
            PersonasResponse(**persona.to_mongo(use_db_field=False))
            for persona in personas
        ]
    except Exception as e:
        handle_error(e)


@router.get("/info/{persona_id}", response_model=LinkedInInfo)
def read_persona_info(persona_id: str = Depends(valid_persona_id)):
    from src.pre_call.utils import get_persona_profile_info

    try:
        persona = get_persona(persona_id)
        linkedin_api_resp, linkedin_summary,buyingStyleInfo = get_persona_profile_info(persona)
        return LinkedInInfo(
            data=linkedin_api_resp, summary=linkedin_summary, url=persona.linkedInUrl,buyingStyle=buyingStyleInfo
        )
    except Exception as e:
        handle_error(e)


@router.get("/{persona_id}", response_model=PersonasResponse)
def read_persona(persona_id: str = Depends(valid_persona_id)):
    try:
        persona = get_persona(persona_id)
        return PersonasResponse(**persona.to_mongo(use_db_field=False))
    except Exception as e:
        handle_error(e)


@router.post("/", response_model=PersonasResponse)
def create_persona(
    persona_in: Persona, auth_response: dict = Depends(get_auth_response)
):
    userId = auth_response["user_info"]["id"]
    try:
        persona = Personas(
            personaName=persona_in.personaName,
            callScenario=persona_in.callScenario,
            difficultyLevel=persona_in.difficultyLevel,
            userId=userId,
            linkedInUrl=persona_in.linkedInUrl,
        )
        persona = persona.save()
        return PersonasResponse(**persona.to_mongo(use_db_field=False))
    except Exception as e:
        handle_error(e)


@router.put("/{persona_id}", response_model=PersonasResponse)
def update_persona(
    new_persona: Persona,
    persona_id: str = Depends(valid_persona_id),
    auth_response: dict = Depends(get_auth_response),
):
    userId = auth_response["user_info"]["id"]
    try:
        persona = get_persona(persona_id)
        persona_update_status = persona.modify(
            updatedAt=datetime.now(),
            personaName=new_persona.personaName,
            callScenario=new_persona.callScenario,
            difficultyLevel=new_persona.difficultyLevel,
            userId=userId,
            linkedInUrl=new_persona.linkedInUrl,
        )
        persona.reload()
        if persona_update_status:
            return PersonasResponse(**persona.to_mongo(use_db_field=False))
        else:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail="Unable to Update Persona",
            )

    except Exception as e:
        handle_error(e)


@router.delete("/{persona_id}")
def delete_persona(persona_id: str = Depends(valid_persona_id)):
    try:
        persona = get_persona(persona_id)
        persona.delete()
        return {"message": "success"}
    except Exception as e:
        handle_error(e)
