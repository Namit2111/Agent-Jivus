# Integrations API Documentation

This document describes the API endpoints for managing integrations within the application.  The API uses FastAPI and requires authentication via an OAuth2 token.

## Authentication

All endpoints require an OAuth2 token.  The token should be passed in the `Authorization` header as a Bearer token:

```
Authorization: Bearer <your_token>
```

The token is obtained through a separate authentication endpoint (not described here, assumed to be at `/token`).


## Endpoints

All endpoints are prefixed with `/integrations`.

### `/integrations/hubspot_integration_setup` (POST)

Sets up or updates a HubSpot integration for the authenticated user.

**Request Body:**

```json
{
  "access_token": "string",
  "refresh_token": "string",
  "expires_in": integer
}
```

* `access_token`: HubSpot access token.
* `refresh_token`: HubSpot refresh token.
* `expires_in`:  HubSpot token expiration time (in seconds).


**Response (200 OK):**

```json
{
  "message": "Hubspot integration setup successful"
}
```

**Error Responses:**

* **400 Bad Request:**  Invalid request data or integration setup failure.
* **401 Unauthorized:** Invalid authentication token.


### `/integrations/gmail_integration_setup` (POST)

Sets up or updates a Gmail integration for the authenticated user.

**Request Body:**

```json
{
  "access_token": "string",
  "refresh_token": "string",
  "expires_in": integer
}
```

* `access_token`: Gmail access token.
* `refresh_token`: Gmail refresh token.
* `expires_in`: Gmail token expiration time (in seconds).

**Response (200 OK):**

```json
{
  "message": "Gmail integration setup successful"
}
```

**Error Responses:**

* **400 Bad Request:** Invalid request data or integration setup failure.
* **401 Unauthorized:** Invalid authentication token.


### `/integrations/smtp_integration_setup` (POST)

Sets up or updates an SMTP integration for the authenticated user.

**Request Body:**

```json
{
  "email": "string",
  "smtp_password": "string"
}
```

* `email`:  SMTP email address.
* `smtp_password`: SMTP password.

**Response (200 OK):**

```json
{
  "message": "SMTP integration setup successful"
}
```

**Error Responses:**

* **400 Bad Request:** Invalid request data or integration setup failure.
* **401 Unauthorized:** Invalid authentication token.


### `/integrations/calendly_integration_setup` (POST)

Sets up or updates a Calendly integration for the authenticated user.

**Request Body:**

```json
{
  "pat_token": "string"
}
```

* `pat_token`: Calendly Personal Access Token.

**Response (200 OK):**

```json
{
  "message": "Calendly integration setup successful"
}
```

**Error Responses:**

* **400 Bad Request:** Invalid request data or integration setup failure.
* **401 Unauthorized:** Invalid authentication token.


### `/integrations/zoom_integration_setup` (POST)

Sets up a Zoom integration for the authenticated user.

**Request Body:**

```json
{
  "client_id": "string",
  "client_secret": "string",
  "account_id": "string"
}
```

* `client_id`: Zoom client ID.
* `client_secret`: Zoom client secret.
* `account_id`: Zoom account ID.

**Response (200 OK):**

```json
{
  "message": "Zoom integration setup successful"
}
```

**Error Responses:**

* **400 Bad Request:** Invalid request data, invalid client ID/secret, or invalid account ID.
* **401 Unauthorized:** Invalid authentication token.


### `/integrations/user/integration` (GET)

Retrieves the integration status for the authenticated user.

**Response (200 OK):**

```json
{
  "zoom": true/false,
  "hubspot": true/false,
  "gmail": true/false,
  "outlook": true/false,
  "smtp": true/false,
  "calendly": true/false
}
```

* `true`: Integration is set up.
* `false`: Integration is not set up.

**Error Responses:**

* **401 Unauthorized:** Invalid authentication token.
* **409 Conflict:** Other error during processing.
* **500 Internal Server Error:**  Unexpected error.


## Included Routers

The `/integrations` router includes the following sub-routers:

* `/integrations/objects`: (HubSpot Objects - details not provided)
* `/integrations/gmail`: (Gmail - details not provided)
* `/integrations/smtp`: (SMTP - details not provided)
* `/integrations/calendly`: (Calendly - details not provided)


This documentation assumes familiarity with HTTP methods (POST, GET) and common HTTP status codes.  Further details on the sub-routers and specific data models (e.g., `HubspotIntegrationSetupRequest`) are required for a complete specification.
