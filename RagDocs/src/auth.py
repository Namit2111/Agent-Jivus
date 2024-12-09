from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(include_in_schema=False)


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if not form_data.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": form_data.password, "token_type": "bearer"}
