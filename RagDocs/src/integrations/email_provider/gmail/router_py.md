# Gmail and Google Calendar Integration API

This API provides endpoints for sending emails via Gmail and creating Google Calendar events.  It uses FastAPI and requires authentication via OAuth2.

## Dependencies

- `fastapi`
- `fastapi.security`
- `requests`
- `datetime`
- `google.oauth2.credentials`
- `googleapiclient.discovery`
- `pydantic`
- `base64`
- Custom modules: `src.db.models`, `src.db.utils`, `src.integrations.email_provider.gmail.utils`, `src.logger`, `src.config`


## Authentication

The API uses OAuth2 Password Bearer token authentication.  The token is obtained through a separate authentication endpoint (not shown in this code snippet, assumed to be at `/token`).  The `authenticate_user` function (from `src.db.utils`) is used to validate the token and retrieve user information.


## Endpoints

### `/gmail/send-email`

**POST**

Sends an email using the authenticated user's Gmail account.

**Request Body:**

```json
{
  "to": "recipient@example.com",
  "subject": "Email Subject",
  "message": "Email Body"
}
```

* **`to` (str):**  Recipient's email address.
* **`subject` (str):** Email subject.
* **`message` (str):** Email body.


**Response (Success):**

```json
{
  "status": "Email sent successfully",
  "messageId": "uniqueMessageId" 
}
```

**Response (Error):**

Returns an HTTP error code (400, 401, or 500) with a descriptive error message.  401 is returned for authentication failures.

### `/gmail/create-event`

**POST**

Creates a Google Calendar event using the provided credentials.  Note that this endpoint currently hardcodes event details; a more robust implementation would use the `event_request` parameters.


**Request Body:**

```json
{
    "summary": "Event Summary",
    "description": "Event Description",
    "start_time": "YYYY-MM-DDTHH:mm:ss+TZD", // ISO 8601 format
    "end_time": "YYYY-MM-DDTHH:mm:ss+TZD",   // ISO 8601 format
    "attendees": ["attendee1@example.com", "attendee2@example.com"],
    "access_token": "your_access_token",
    "refresh_token": "your_refresh_token",
    "token_uri": "your_token_uri",
    "client_id": "your_client_id",
    "client_secret": "your_client_secret"
}
```

* **`summary` (str):** Event summary.
* **`description` (str):** Event description.
* **`start_time` (str):** Event start time in ISO 8601 format.
* **`end_time` (str):** Event end time in ISO 8601 format.
* **`attendees` (list):** List of attendee email addresses.
* **`access_token`, `refresh_token`, `token_uri`, `client_id`, `client_secret` (str):** OAuth2 credentials for Google Calendar API access.


**Response (Success):**

```json
{
  "status": "Event created successfully",
  "eventId": "uniqueEventId"
}
```

**Response (Error):**

Returns an HTTP error code (500) with a descriptive error message.


## Error Handling

The API includes basic error handling using `try...except` blocks.  HTTP exceptions are raised for various error conditions with appropriate status codes.  Generic exceptions are caught and returned as a 400 Bad Request.


## Logging

The code uses a custom logger (`src.logger`) for debugging purposes.  Log messages are written to a file or console.  The log level can be configured via the `src.config` module.


## Note:

The `/create-event` endpoint currently has a hardcoded example event. The request body parameters are not used in the current implementation, but the structure is provided for future expansion.  Remember to replace placeholder values in the request body with actual OAuth credentials.  Also, ensure that the necessary Google Calendar API scopes are included when obtaining the access token.
