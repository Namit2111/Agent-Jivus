
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.db.utils import authenticate_user
import requests

from src.integrations.Calendly.utils import get_valid_PAT_token, getUserEventTypes, getUserURI

router = APIRouter(prefix='/calendly')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/user")
def get_user_info(auth_token: str = Depends(oauth2_scheme)):
    try:
        auth_response = authenticate_user(auth_token)
        if auth_response.get("status") != 200:
            # You might want to use a more appropriate status code like 401 for Unauthorized
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=auth_response.get("message", "Invalid user auth token"),
            )
        
        user_id = auth_response.get("user_info").get("id")  # type:ignore
        return getUserURI(user_id)

    except HTTPException as http_exc:
        # Re-raise the HTTPException if it's been explicitly raised
        raise http_exc
    except Exception as e:
        # Handle other exceptions and return an appropriate error code
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.get("/user-event-types")
def get_user_event_types(auth_token: str = Depends(oauth2_scheme)):
    try:
        auth_response = authenticate_user(auth_token)
        if auth_response.get("status") != 200:
            # You might want to use a more appropriate status code like 401 for Unauthorized
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=auth_response.get("message", "Invalid user auth token"),
            )
        
        user_id = auth_response.get("user_info").get("id")  # type:ignore
        return getUserEventTypes(user_id=user_id)    

    except HTTPException as http_exc:
        # Re-raise the HTTPException if it's been explicitly raised
        raise http_exc
    except Exception as e:
        # Handle other exceptions and return an appropriate error code
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    

@router.get("/check-availability")
def get_user_availability(start_time:str, end_time: str, auth_token: str = Depends(oauth2_scheme)):
    try:
        auth_response = authenticate_user(auth_token)
        if auth_response.get("status") != 200:
            # You might want to use a more appropriate status code like 401 for Unauthorized
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=auth_response.get("message", "Invalid user auth token"),
            )
        
        user_id = auth_response.get("user_info").get("id")  # type:ignore
        ACCESS_TOKEN = get_valid_PAT_token(user_id);
    
        # url = "https://api.calendly.com/user_availability_schedules"
        url = "https://api.calendly.com/event_type_available_times"
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Fetch event type and validate
        event_types = getUserEventTypes(user_id=user_id)
        if not event_types or "uri" not in event_types[0]:
            raise HTTPException(status_code=404, detail="No valid event type found for user")

        event_type_uri = event_types[0]["uri"]

        # Define parameters
        params = {
            "event_type": event_type_uri,
            "start_time": start_time,
            "end_time": end_time,
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            return data

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())
    

    except HTTPException as http_exc:
        # Re-raise the HTTPException if it's been explicitly raised
        raise http_exc
    except Exception as e:
        # Handle other exceptions and return an appropriate error code
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
