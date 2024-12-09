# SMTP Email Sending API

This document describes the API endpoint for sending emails using SMTP, specifically designed for integration with a user authentication system.

## File: `smtp_api.py`

This file defines a FastAPI router for handling email sending requests via SMTP.  It utilizes user authentication, retrieves SMTP credentials securely, and sends emails using the `smtplib` library.

### Imports:

* `fastapi`:  Provides the framework for building the API.
* `OAuth2PasswordBearer`:  Used for token-based authentication.
* `src.db.models`: Imports the `Integrations` model (presumably for storing integration settings).
* `src.db.utils`: Imports the `authenticate_user` function for user authentication.
* `requests`: Used for making external HTTP requests (though not directly used in this snippet).
* `datetime`, `timedelta`: Used for date and time manipulation (not directly used in this snippet).
* `src.integrations.email_provider.gmail.utils`: Imports `get_valid_gmail_credentials` (although the code uses SMTP, this import suggests potential for Gmail integration elsewhere).
* `src.integrations.email_provider.smtp.utils`: Imports `get_valid_smtp_credentials` for retrieving user SMTP credentials.
* `src.logger`: Imports the `Logger` class for logging.
* `src.config`: Imports the `config` object (presumably for configuration settings).
* `google.oauth2.credentials`: Imports `Credentials` (likely unused in this specific snippet, suggesting potential for Google API integration elsewhere).
* `googleapiclient.discovery`: Imports `build` (likely unused in this specific snippet, suggesting potential for Google API integration elsewhere).
* `pydantic`: Imports `BaseModel` for data validation.
* `base64`, `smtplib`, `email.mime.multipart`, `email.mime.text`: Used for email construction and sending.


### Logger:

```python
logger = Logger("smtp")
```

A logger instance is created for logging SMTP-related events.

### Router:

```python
router = APIRouter(prefix='/smtp')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
```

An APIRouter is defined with the prefix `/smtp` for all its endpoints.  `OAuth2PasswordBearer` is used to handle OAuth2 authentication.


### EmailRequest Model:

```python
class EmailRequest(BaseModel):
    to: str
    subject: str
    message: str
```

A Pydantic model defining the structure of email requests.


### `/send-email` Endpoint:

```python
@router.post("/send-email")
async def send_email(email_request: EmailRequest, auth_token: str = Depends(oauth2_scheme)):
    # ... (Implementation detailed below) ...
```

This endpoint handles POST requests to `/smtp/send-email`.  It requires an `EmailRequest` body and an authentication token.


#### Endpoint Implementation:

1. **Authentication:**  The `authenticate_user` function verifies the provided authentication token.  If authentication fails, a 401 Unauthorized HTTPException is raised.

2. **Credential Retrieval:** `get_valid_smtp_credentials` retrieves the sender's email address and SMTP password based on the authenticated user ID.

3. **Email Construction:** An email message is created using `MIMEMultipart` and `MIMEText`.

4. **SMTP Connection and Sending:** An SMTP connection is established to the specified server (`smtp.gmail.com` in this case), login credentials are used, and the email is sent.

5. **Error Handling:**  `try...except` blocks handle potential `HTTPException` and other exceptions, returning appropriate HTTP status codes and error messages.

### Notes:

* The code uses hardcoded `smtp.gmail.com` and port 587.  Ideally, these should be configurable.
* Error handling could be improved by providing more specific error messages based on the type of exception caught.
* Security considerations: Storing SMTP passwords directly is a security risk.  Consider using more secure methods like environment variables or a secrets management system.


This documentation provides a comprehensive overview of the `smtp_api.py` file's functionality and structure.  It highlights key aspects, potential improvements, and security considerations.
