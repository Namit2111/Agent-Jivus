from src.db.models import Integrations
from src.config import config
from google.oauth2.credentials import Credentials
from fastapi import HTTPException, status

def get_valid_gmail_credentials(user_id: int):
    integration = Integrations.objects(
            userId = user_id,
            service="gmail"
        ).first()
    
    # Check if the access token exists
    if not integration or "access_token" not in integration.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No access token found. Please connect your HubSpot account."
        )
        
    # Load the credentials from the access token
    creds = Credentials(
        token=integration.data['access_token'],
        refresh_token=integration.data['refresh_token'],
        token_uri=config['GOOGLE_TOKEN_URI'],
        client_id=config['GOOGLE_CLIENT_ID'],
        client_secret=config['GOOGLE_CLIENT_SECRET']
    )
    
    return creds
    
    
        