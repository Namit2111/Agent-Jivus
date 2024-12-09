# Integrations API Documentation

This document outlines the API endpoints for managing integrations within the application.  The API uses FastAPI and handles various integration types, including HubSpot, Gmail, SMTP, Calendly, and Zoom. Authentication is handled via an OAuth2 flow.

## Endpoints

All endpoints are prefixed with `/integrations`.

### `/integrations/hubspot_integration_setup` (POST)

**Description:** Sets up or updates a HubSpot integration for the authenticated user.

**Request Body:**

```json
{
  "access_token": "YOUR_HUBSPOT_ACCESS_TOKEN",
  "refresh_token": "YOUR_HUBSPOT_REFRESH_TOKEN",
  "expires_in": 3600 //Seconds
}
```

**Parameters:**

* `auth_token`: (str, required) OAuth2 authentication token.

**Response:**

* **200 OK:**  `{"message": "Hubspot integration setup successful"}`
* **400 BAD REQUEST:**  Error during integration setup or update.  Includes detailed error message.
* **401 UNAUTHORIZED:** Invalid authentication token.


### `/integrations/gmail_integration_setup` (POST)

**Description:** Sets up or updates a Gmail integration for the authenticated user.

**Request Body:**

```json
{
  "access_token": "YOUR_GMAIL_ACCESS_TOKEN",
  "refresh_token": "YOUR_GMAIL_REFRESH_TOKEN",
  "expires_in": 3600 //Seconds
}
```

**Parameters:**

* `auth_token`: (str, required) OAuth2 authentication token.

**Response:**

* **200 OK:**  `{"message": "Gmail integration setup successful"}`
* **400 BAD REQUEST:** Error during integration setup or update. Includes detailed error message.
* **401 UNAUTHORIZED:** Invalid authentication token.


### `/integrations/smtp_integration_setup` (POST)

**Description:** Sets up or updates an SMTP integration for the authenticated user.

**Request Body:**

```json
{
  "email": "your_email@example.com",
  "smtp_password": "your_smtp_password"
}
```

**Parameters:**

* `auth_token`: (str, required) OAuth2 authentication token.

**Response:**

* **200 OK:**  `{"message": "SMTP integration setup successful"}`
* **400 BAD REQUEST:** Error during integration setup or update. Includes detailed error message.
* **401 UNAUTHORIZED:** Invalid authentication token.


### `/integrations/calendly_integration_setup` (POST)

**Description:** Sets up or updates a Calendly integration for the authenticated user.

**Request Body:**

```json
{
  "pat_token": "YOUR_CALENDLY_PAT_TOKEN"
}
```

**Parameters:**

* `auth_token`: (str, required) OAuth2 authentication token.

**Response:**

* **200 OK:**  `{"message": "Calendly integration setup successful"}`
* **400 BAD REQUEST:** Error during integration setup or update. Includes detailed error message.
* **401 UNAUTHORIZED:** Invalid authentication token.


### `/integrations/zoom_integration_setup` (POST)

**Description:** Sets up a Zoom integration for the authenticated user.

**Request Body:**

```json
{
  "client_id": "YOUR_ZOOM_CLIENT_ID",
  "client_secret": "YOUR_ZOOM_CLIENT_SECRET",
  "account_id": "YOUR_ZOOM_ACCOUNT_ID"
}
```

**Parameters:**

* `auth_token`: (str, required) OAuth2 authentication token.

**Response:**

* **200 OK:**  `{"message": "Zoom integration setup successful"}`
* **400 BAD REQUEST:** Error during integration setup (invalid credentials or account ID). Includes detailed error message.
* **401 UNAUTHORIZED:** Invalid authentication token.


### `/integrations/user/integration` (GET)

**Description:** Retrieves the integration status for the authenticated user.

**Parameters:**

* `auth_token`: (str, required) OAuth2 authentication token.

**Response:**

* **200 OK:**  A JSON object indicating the status (true/false) of each supported integration:  `{"zoom": true, "hubspot": false, "gmail": true, ...}`
* **409 CONFLICT:**  Error during authentication. Includes detailed error message.
* **500 INTERNAL SERVER ERROR:**  Unexpected error. Includes detailed error message.


## Included Routers

The `/integrations` router includes the following sub-routers:

* `objects.router`: (HubSpot objects related endpoints - details not provided in the code snippet)
* `gmail.router`: (Gmail-specific endpoints - details not provided in the code snippet)
* `smtp.router`: (SMTP-specific endpoints - details not provided in the code snippet)
* `calendly.router`: (Calendly-specific endpoints - details not provided in the code snippet)


## Authentication

All endpoints require an OAuth2 authentication token obtained via the `/token` endpoint (not shown in the provided code).


## Error Handling

The API uses standard HTTP status codes to indicate success or failure.  Detailed error messages are included in the response body for 400 and 500 level errors.  Authentication errors result in a 401 Unauthorized response.


## Notes

* The commented-out section appears to be an alternative implementation for HubSpot callback handling, which is not currently in use.
* The code extensively uses error handling to catch and manage exceptions, returning appropriate HTTP status codes and messages.
* The `Integrations` model (from `src.db.models`) manages integration data persistence.
* The `authenticate_user` function (from `src.db.utils`) handles authentication verification.


This documentation provides a comprehensive overview of the provided API code.  For more detailed information on specific endpoints or sub-routers, please refer to their respective documentation (not included here).
