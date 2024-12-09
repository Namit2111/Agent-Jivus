from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.db.utils import authenticate_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_auth_response(auth_token: str = Depends(oauth2_scheme)) -> dict:
    auth_response = authenticate_user(auth_token)
    if auth_response.get("status") != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=auth_response.get("message", "Invalid user auth token"),
        )
    return auth_response
