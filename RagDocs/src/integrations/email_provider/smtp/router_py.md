# SMTP Email Sending API

This document describes the API endpoint for sending emails using SMTP.  The API is built using FastAPI and requires authentication.

## Endpoint: `/smtp/send-email`

This endpoint allows authenticated users to send emails via SMTP.

**Method:** `POST`

**Request Body:**

```json
{
  "to": "recipient@example.com",
  "subject": "Email Subject",
  "message": "Email body text"
}
```

* **`to` (required):**  The recipient's email address.  (String)
* **`subject` (required):** The subject of the email. (String)
* **`message` (required):** The body of the email. (String)


**Request Headers:**

* **`Authorization`:** Bearer token obtained from the `/token` endpoint.


**Response:**

**Success (200 OK):**

```json
{
  "status": "Email sent successfully"
}
```

**Error Responses:**

* **400 Bad Request:**  A general error occurred while sending the email. The response body will include a `detail` field with more information about the error.  This might be due to issues with the SMTP server, invalid email credentials, or malformed request data.
* **401 Unauthorized:** The provided authentication token is invalid or expired.


## Authentication

The API uses OAuth2 Password Bearer token authentication.  A valid access token must be provided in the `Authorization` header using the Bearer scheme (e.g., `Authorization: Bearer <your_token>`).  The token is obtained through a separate authentication endpoint (not detailed here, assumed to be `/token`).


## Dependencies

* **FastAPI:** For building the API.
* **OAuth2PasswordBearer:** For authentication.
* **`src.db.models`:** Database models (Integrations).
* **`src.db.utils`:** Database utility functions (authenticate_user).
* **`requests`:** For making HTTP requests (likely not used directly in this endpoint, but potentially used by dependency functions).
* **`datetime`:** For date and time manipulation.
* **`src.integrations.email_provider.gmail.utils`:** Utilities for retrieving Gmail credentials.
* **`src.integrations.email_provider.smtp.utils`:** Utilities for retrieving SMTP credentials.
* **`src.logger`:** Custom logging module.
* **`src.config`:** Application configuration.
* **`google.oauth2.credentials`:** For Google OAuth2 credentials (likely used by Gmail integration).
* **`googleapiclient.discovery`:** For building Google APIs clients (likely used by Gmail integration).
* **`pydantic`:** For data validation.
* **`base64`:** For base64 encoding/decoding (potentially used for credential handling).
* **`smtplib`:** For SMTP communication.
* **`email.mime.multipart` and `email.mime.text`:** For creating MIME email messages.


## Error Handling

The API includes comprehensive error handling.  Specific HTTP exception codes are returned to indicate the type of error that occurred.  Generic exceptions are caught and returned as 400 Bad Request errors with a descriptive message.

## Security Considerations

* **Credential Management:** The code retrieves SMTP credentials using a helper function (`get_valid_smtp_credentials`).  It's crucial that this function securely retrieves and handles these credentials, avoiding hardcoding or insecure storage practices.
* **Input Validation:** Pydantic is used for input validation, which helps prevent common security vulnerabilities like injection attacks.
* **Authentication:**  Proper authentication ensures only authorized users can send emails.


## Code Example (Python):

The provided Python code implements the API endpoint.  Note that the credential management and authentication aspects are crucial for security and are abstracted in this example.

