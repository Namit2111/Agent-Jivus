from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.db.schemas import HubspotInfo
from src.db.utils import authenticate_user
import requests
from src.integrations.hubspot.utils import get_valid_access_token, validate_object_type
from src.logger import Logger
import json

logger = Logger("hubspot_objects")

router = APIRouter(prefix='/hubspot', tags=["hubspot"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

HUBSPOT_BASE_URL = "https://api.hubapi.com"

@router.get("/{object_type}")
async def read_objects(object_type: str, auth_token: str = Depends(oauth2_scheme)):

    try:
        auth_response = authenticate_user(auth_token)
        if auth_response.get("status") != 200:
            # You might want to use a more appropriate status code like 401 for Unauthorized
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=auth_response.get("message", "Invalid user auth token"),
            )
        
        user_id = auth_response.get("user_info").get("id")  # type:ignore
        ACCESS_TOKEN = get_valid_access_token(user_id);
        
        if not await validate_object_type(object_type):
            raise HTTPException(status_code=400, detail="Invalid object type")
    
        url = f"{HUBSPOT_BASE_URL}/crm/v3/objects/{object_type}"
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        return response.json()

    except HTTPException as http_exc:
        # Re-raise the HTTPException if it's been explicitly raised
        raise http_exc
    except Exception as e:
        # Handle other exceptions and return an appropriate error code
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/engagements")
async def create_engagement(data: dict = Body(...), auth_token: str = Depends(oauth2_scheme)):

    try:
        auth_response = authenticate_user(auth_token)
        if auth_response.get("status") != 200:
            # You might want to use a more appropriate status code like 401 for Unauthorized
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=auth_response.get("message", "Invalid user auth token"),
            )
        
        user_id = auth_response.get("user_info").get("id")  # type:ignore
        ACCESS_TOKEN = get_valid_access_token(user_id);
        
        if not await validate_object_type("contacts"):
            raise HTTPException(status_code=400, detail="Invalid object type")
            
        url = f"{HUBSPOT_BASE_URL}/engagements/v1/engagements"
                
        # Headers including Authorization with access token
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

        # Make the POST request to create the note
        response = requests.post(url, headers=headers, data=json.dumps(data))

        # Check the response
        if response.status_code == 200:
            print("Engagement created successfully:", response.json())
        else:
            raise HTTPException(status_code=response.status_code, detail=f"Failed to create note: {response.text}")
        

    except HTTPException as http_exc:
        # Re-raise the HTTPException if it's been explicitly raised
        raise http_exc
    except Exception as e:
        # Handle other exceptions and return an appropriate error code
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{object_type}/{object_id}")
async def get_object_by_id(object_type: str, object_id:str, properties: str | None = None, auth_token: str = Depends(oauth2_scheme)):

    try:
        auth_response = authenticate_user(auth_token)
        if auth_response.get("status") != 200:
            # You might want to use a more appropriate status code like 401 for Unauthorized
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=auth_response.get("message", "Invalid user auth token"),
            )
        
        user_id = auth_response.get("user_info").get("id")  # type:ignore
        ACCESS_TOKEN = get_valid_access_token(user_id);

        if not await validate_object_type(object_type):
            raise HTTPException(status_code=400, detail="Invalid object type")
    
        url = f"{HUBSPOT_BASE_URL}/crm/v3/objects/{object_type}/{object_id}"
        params = {}
        if properties:
            params['properties'] = properties.split(',')
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        return response.json()

    except HTTPException as http_exc:
        # Re-raise the HTTPException if it's been explicitly raised
        raise http_exc
    except Exception as e:
        # Handle other exceptions and return an appropriate error code
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/{object_type}")
async def add_object(
    object_type: str,
    object_data: dict,
    auth_token: str = Depends(oauth2_scheme)
):
    try:
        auth_response = authenticate_user(auth_token)
        if auth_response.get("status") != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=auth_response.get("message", "Invalid user auth token"),
            )
        user_id = auth_response.get("user_info").get("id")  # type:ignore
        ACCESS_TOKEN = get_valid_access_token(user_id);

        if not await validate_object_type(object_type):
            raise HTTPException(status_code=400, detail="Invalid object type")

        url = f"{HUBSPOT_BASE_URL}/crm/v3/objects/{object_type}"
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, headers=headers, json=object_data)

        if response.status_code != 201:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        return response.json()

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{object_type}/{object_id}")
async def edit_object(
    object_type: str,
    object_id: str,
    update_data: dict,
    auth_token: str = Depends(oauth2_scheme)
):
    try:
        auth_response = authenticate_user(auth_token)
        if auth_response.get("status") != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=auth_response.get("message", "Invalid user auth token"),
            )
        
        user_id = auth_response.get("user_info").get("id")  # type:ignore
        ACCESS_TOKEN = get_valid_access_token(user_id);

        if not await validate_object_type(object_type):
            raise HTTPException(status_code=400, detail="Invalid object type")

        url = f"{HUBSPOT_BASE_URL}/crm/v3/objects/{object_type}/{object_id}"
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        response = requests.patch(url, headers=headers, json=update_data)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        return response.json()

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{object_type}/{object_id}")
async def remove_object(
    object_type: str,
    object_id: str,
    auth_token: str = Depends(oauth2_scheme)
):
    try:
        auth_response = authenticate_user(auth_token)
        if auth_response.get("status") != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=auth_response.get("message", "Invalid user auth token"),
            )
        
        user_id = auth_response.get("user_info").get("id")  # type:ignore
        ACCESS_TOKEN = get_valid_access_token(user_id);

        if not await validate_object_type(object_type):
            raise HTTPException(status_code=400, detail="Invalid object type")

        url = f"{HUBSPOT_BASE_URL}/crm/v3/objects/{object_type}/{object_id}"
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        response = requests.delete(url, headers=headers)

        if response.status_code != 204:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        return {"message": "Object deleted successfully"}

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    