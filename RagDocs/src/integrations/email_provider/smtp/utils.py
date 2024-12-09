from src.db.models import Integrations
from fastapi import HTTPException, status

def get_valid_smtp_credentials(user_id: int):
    integration = Integrations.objects(
            userId = user_id,
            service="smtp"
        ).first()
    
    # Check if the access token exists
    if not integration or "email" not in integration.data  or "smtpPassword" not in integration.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No email or password found. Please connect your account with SMTP."
        )
            
    return integration.data['email'], integration.data['smtpPassword']
    
    
        