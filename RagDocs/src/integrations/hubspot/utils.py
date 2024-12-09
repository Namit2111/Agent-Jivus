import requests
from src.config import config
from datetime import datetime, timedelta
from src.db.models import Integrations
from fastapi import HTTPException, status

  # Add other valid object types as needed
VALID_OBJECTS = {"contacts"}
HUBSPOT_BASE_URL = "https://api.hubapi.com"

async def validate_object_type(object_type: str):
    return object_type in VALID_OBJECTS

def refresh_access_token(integration, refresh_token: str):
    url = "https://api.hubapi.com/oauth/v1/token"
    params = {
        "grant_type": "refresh_token",
        "client_id": config["HUBSPOT_CLIENT_ID"],
        "client_secret": config["HUBSPOT_CLIENT_SECRET"],
        "refresh_token": refresh_token,
    }
    response = requests.post(url, data=params)
    response_data = response.json()

    new_access_token = response_data["access_token"]
    new_refresh_token = response_data.get("refresh_token", refresh_token)
    expires_in = response_data["expires_in"]
    
    integration.update(
        data={
            # "hubspot_api_key": setup_data.hubspot_api_key,
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "expires_in": int((datetime.now() + timedelta(seconds=expires_in)).timestamp()) ,
        },
    )
    
    return new_access_token

def get_valid_access_token(user_id: int):
    integration = Integrations.objects(
                userId=user_id, service="hubspot"
            ).first()
    
    # Check if the access token exists
    if not integration or "access_token" not in integration.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No access token found. Please connect your HubSpot account."
        )
    
    current_time_seconds = int(datetime.now().timestamp())
    
    if current_time_seconds >= integration.data.get("expires_in"):
        return refresh_access_token(integration, integration.data.get("refresh_token"))
        # raise HTTPException(
        #     status_code=status.HTTP_401_UNAUTHORIZED,
        #     detail="Access token has expired. Please reconnect your HubSpot account."
        # )
    
    return integration.data.get("access_token")
