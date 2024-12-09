
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.db.models import Integrations
from src.db.utils import authenticate_user
import requests
from datetime import datetime, timedelta
from src.integrations.email_provider.gmail.utils import get_valid_gmail_credentials
from src.integrations.email_provider.smtp.utils import get_valid_smtp_credentials
from src.logger import Logger
from src.config import config
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from pydantic import BaseModel
import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = Logger("smtp")

router = APIRouter(prefix='/smtp')
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
        sender_email, smtpPassword = get_valid_smtp_credentials(user_id=user_id);

        # SMTP server configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Create the email content
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = email_request.to
        message['Subject'] = email_request.subject

        # Body of the email
        body = email_request.message
        message.attach(MIMEText(body, 'plain'))

        # Establish a connection with Gmail's SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Upgrade the connection to a secure one using TLS

        # Login to the email account
        server.login(sender_email, smtpPassword)

        # Send the email
        server.sendmail(sender_email, email_request.to, message.as_string())
        # Terminate the SMTP session
        server.quit()
        return {"status": "Email sent successfully"}

    except HTTPException as http_exc:
        # Re-raise the HTTPException if it's been explicitly raised
        raise http_exc
    except Exception as e:
        # Handle other exceptions and return an appropriate error code
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to send email str(e)")