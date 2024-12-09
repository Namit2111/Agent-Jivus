
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.db.models import Integrations
from src.db.utils import authenticate_user
import requests
from datetime import datetime, timedelta
from src.integrations.email_provider.gmail.utils import get_valid_gmail_credentials
from src.logger import Logger
from src.config import config
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from pydantic import BaseModel
import base64

logger = Logger("gmail")

router = APIRouter(prefix='/gmail')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class EmailRequest(BaseModel):
    to: str
    subject: str
    message: str

@router.post("/send-email")
async def send_email(email_request: EmailRequest, auth_token: str = Depends(oauth2_scheme)):

    try:
        auth_response = authenticate_user(auth_token)
        if auth_response.get("status") != 200:
            # You might want to use a more appropriate status code like 401 for Unauthorized
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=auth_response.get("message", "Invalid user auth token"),
            )
        
        user_id = auth_response.get("user_info").get("id")  # type:ignore
        creds = get_valid_gmail_credentials(user_id);

         # Build the Gmail service
        service = build('gmail', 'v1', credentials=creds)
        
        # Create the email
        message = {
            'raw': base64.urlsafe_b64encode(
                f"To: {email_request.to}\r\nSubject: {email_request.subject}\r\n\r\n{email_request.message}".encode('utf-8')
            ).decode('utf-8')
        }

        # Send the email
        send_response = service.users().messages().send(userId='me', body=message).execute()

        logger.debug(send_response)

        if send_response.get('id'):
            return {"status": "Email sent successfully", "messageId": send_response.get('id')}
        else:
            raise HTTPException(status_code=500, detail="Failed to send email")

    except HTTPException as http_exc:
        # Re-raise the HTTPException if it's been explicitly raised
        raise http_exc
    except Exception as e:
        # Handle other exceptions and return an appropriate error code
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


class EventRequest(BaseModel):
    summary: str
    description: str
    start_time: str
    end_time: str
    attendees: list
    access_token: str
    refresh_token: str 
    token_uri: str     
    client_id: str     
    client_secret: str
    
@router.post("/create-event")
def create_event(event_request: EventRequest, auth_token: str = Depends(oauth2_scheme)):
    try:
        auth_response = authenticate_user(auth_token)
        if auth_response.get("status") != 200:
            # You might want to use a more appropriate status code like 401 for Unauthorized
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=auth_response.get("message", "Invalid user auth token"),
            )
        # Load the credentials from the access token
        creds = Credentials(
            token=event_request.access_token,
            refresh_token=event_request.refresh_token,
            token_uri=event_request.token_uri,
            client_id=event_request.client_id,
            client_secret=event_request.client_secret
        )

        # Build the Google Calendar service
        service = build('calendar', 'v3', credentials=creds)

        # Create the event
        # event = {
        #     'summary': event_request.summary,
        #     'description': event_request.description,
        #     'start': {
        #         'dateTime': event_request.start_time,
        #         'timeZone': 'America/Los_Angeles',  # Update the timezone as needed
        #     },
        #     'end': {
        #         'dateTime': event_request.end_time,
        #         'timeZone': 'America/Los_Angeles',  # Update the timezone as needed
        #     },
        #     'attendees': [{'email': email} for email in event_request.attendees],
        # }

        event = {
            "summary": "Team Meeting",
            "description": "Discussing project updates.",
            "start": {
                "dateTime": "2024-09-04T15:00:00+05:30",
                "timeZone": "Asia/Kolkata"
            },
            "end": {
                "dateTime": "2024-09-04T16:00:00+05:30",
                "timeZone": "Asia/Kolkata"
            },
            "attendees": [
                { "email": "vasutiwari442@gmail.com" },
            ],
            "sendUpdates": "all"
        }
        

        # Insert the event into the calendar
        event_result = service.events().insert(
            calendarId='primary',
            body=event,
            sendUpdates='all'  # Send invites to attendees
        ).execute()

        logger.debug(event_result)
        return {"status": "Event created successfully", "eventId": event_result['id']}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))