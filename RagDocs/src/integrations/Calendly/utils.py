from fastapi import HTTPException, status
import requests
from src.db.models import Integrations


def get_valid_PAT_token(user_id: int):
    integration = Integrations.objects(
                userId=user_id, service="calendly"
            ).first()
    
    # Check if the access token exists
    if not integration or "pat_token" not in integration.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No PAT token found. Please connect your Calendly account."
        )
        
    return integration.data.get("pat_token")

def getUserURI(user_id: int):
    ACCESS_TOKEN = get_valid_PAT_token(user_id);
    
    url = "https://api.calendly.com/users/me"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        user_data = response.json()
        return user_data["resource"]["uri"] 

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

def getUserEventTypes(user_id):
    ACCESS_TOKEN = get_valid_PAT_token(user_id);
    
    url = f"https://api.calendly.com/event_types"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    params = {"user": getUserURI(user_id)}
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data["collection"]

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    