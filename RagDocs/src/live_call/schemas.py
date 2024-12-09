from pydantic import AnyUrl, BaseModel
from src.db.schemas import HubspotInfo


# Define a Pydantic model for the request body
class ZoomIntegrationSetupRequest(BaseModel):
    client_id: str
    client_secret: str
    account_id: str

class HubspotOAuthCallbackRequest(BaseModel):
    code: str


class HubspotIntegrationSetupRequest(BaseModel):
    # hubspot_api_key: str
    access_token:str
    refresh_token: str
    expires_in: int

class GmailIntegrationSetupRequest(BaseModel):
    # hubspot_api_key: str
    access_token:str
    refresh_token: str
    expires_in: int

class SMTPIntegrationSetupRequest(BaseModel):
    # hubspot_api_key: str
    email:str
    smtp_password: str
    
class CalendlyIntegrationSetupRequest(BaseModel):
    pat_token: str

class SetupParams(BaseModel):
    linkedinUrl: str
    hsContactID: str
    desiredOutcome: str
