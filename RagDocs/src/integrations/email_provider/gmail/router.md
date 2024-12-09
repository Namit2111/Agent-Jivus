# Gmail and Google Calendar Integration API

This document describes the API endpoints for sending emails via Gmail and creating Google Calendar events.  The API uses FastAPI and requires authentication via OAuth2.

## Dependencies

*   `fastapi`
*   `fastapi.security`
*   `requests`
*   `datetime`
*   `google.oauth2.credentials`
*   `googleapiclient.discovery`
*   `pydantic`
*   `base64`
*   Project specific modules: `src.db.models`, `src.db.utils`, `src.integrations.email_provider.gmail.utils`, `src.logger`, `src.config`


## Authentication

All endpoints require authentication using an OAuth2 token.  The token is obtained through a separate authentication endpoint (not defined in this file, assumed to be at `/token`).


## Endpoints

### `/gmail/send-email`

**Method:** `POST`

**Request Body:**

```json
{
  "to": "recipient@example.com",
  "subject": "Email Subject",
  "message": "Email Body"
}
```

*   `to` (str): Recipient email address.
*   `subject` (str): Email subject.
*   `message` (str): Email body.

**Response:**

On Success (200 OK):

```json
{
  "status": "Email sent successfully",
  "messageId": "<Gmail Message ID>"
}
```

On Error (401 Unauthorized):

```json
{
  "detail": "Invalid user auth token" 
}
```

On Error (400 Bad Request) or (500 Internal Server Error):

```json
{
  "detail": "Error message"
}
```


### `/gmail/create-event`

**Method:** `POST`

**Request Body:**

```json
{
    "summary": "Event Summary",
    "description": "Event Description",
    "start_time": "YYYY-MM-DDTHH:mm:ss+HH:mm", //ISO 8601 format
    "end_time": "YYYY-MM-DDTHH:mm:ss+HH:mm",  //ISO 8601 format
    "attendees": ["attendee1@example.com", "attendee2@example.com"],
    "access_token": "<Google Calendar Access Token>",
    "refresh_token": "<Google Calendar Refresh Token>",
    "token_uri": "<Google Calendar Token URI>",
    "client_id": "<Google Calendar Client ID>",
    "client_secret": "<Google Calendar Client Secret>"
}
```

*   `summary` (str): Event summary.
*   `description` (str): Event description.
*   `start_time` (str): Event start time in ISO 8601 format.
*   `end_time` (str): Event end time in ISO 8601 format.
*   `attendees` (list): List of attendee email addresses.
*   `access_token`, `refresh_token`, `token_uri`, `client_id`, `client_secret` (str): Google Calendar OAuth2 credentials.


**Response:**

On Success (200 OK):

```json
{
  "status": "Event created successfully",
  "eventId": "<Google Calendar Event ID>"
}
```

On Error (401 Unauthorized):

```json
{
  "detail": "Invalid user auth token"
}
```

On Error (500 Internal Server Error):

```json
{
  "detail": "Error message"
}
```

**Note:** The `/gmail/create-event` endpoint currently uses hardcoded event details instead of the values received from `event_request`. This should be updated to use the provided `event_request` data for a fully functional implementation.  The example provided is for illustrative purposes only.


## Error Handling

The API uses standard HTTP status codes to indicate success or failure.  Error responses include a `detail` field providing more information about the error.


## Logging

The API uses a custom logger (`src.logger.Logger`) to log debug information.
