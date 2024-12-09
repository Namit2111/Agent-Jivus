# Calendly API Integration

This document describes the API endpoints for interacting with Calendly.  This API uses FastAPI and requires authentication via an OAuth2 token.

## Dependencies

- `datetime`
- `timedelta`
- `fastapi`
- `fastapi.security`
- `requests`
- `src.db.utils` (Assumed to contain the `authenticate_user` function)
- `src.integrations.Calendly.utils` (Assumed to contain `get_valid_PAT_token`, `getUserEventTypes`, and `getUserURI` functions)


## API Endpoints

All endpoints are prefixed with `/calendly`.  Authentication is required for all endpoints and is handled via an OAuth2 token passed in the `Authorization` header.

### `/user` (GET)

Retrieves the Calendly URI for the authenticated user.

**Request Parameters:**

- `auth_token` (str): OAuth2 authentication token.  Automatically handled by `Depends(oauth2_scheme)`.

**Response:**

- **200 OK:**  The Calendly URI of the user (JSON).  Example: `{"uri": "https://calendly.com/user123"}`
- **401 Unauthorized:** Invalid or missing authentication token.
- **400 Bad Request:**  Generic error during processing.


### `/user-event-types` (GET)

Retrieves the event types for the authenticated user.

**Request Parameters:**

- `auth_token` (str): OAuth2 authentication token.  Automatically handled by `Depends(oauth2_scheme)`.

**Response:**

- **200 OK:**  A list of user's event types (JSON).  Example: `[{"uri": "event_type_uri_1", ...}, {"uri": "event_type_uri_2", ...}]`
- **401 Unauthorized:** Invalid or missing authentication token.
- **400 Bad Request:**  Generic error during processing.


### `/check-availability` (GET)

Checks the availability of the user within a specified time range for a specific event type.

**Request Parameters:**

- `start_time` (str): Start time in ISO 8601 format (e.g., "2024-03-08T10:00:00Z").
- `end_time` (str): End time in ISO 8601 format (e.g., "2024-03-08T11:00:00Z").
- `auth_token` (str): OAuth2 authentication token.  Automatically handled by `Depends(oauth2_scheme)`.


**Response:**

- **200 OK:** Calendly availability data (JSON).  The exact structure depends on Calendly's API response.
- **401 Unauthorized:** Invalid or missing authentication token.
- **400 Bad Request:** Generic error during processing.
- **404 Not Found:** No valid event type found for the user.
- Other status codes:  Will reflect the status code returned by the Calendly API.


## Error Handling

The API uses standard HTTP status codes to indicate success or failure.  Generic errors are returned as a JSON object with a `detail` field containing a descriptive message.  Specific error handling is implemented within each endpoint to catch and handle exceptions appropriately.


## Authentication

Authentication is handled using an OAuth2 flow.  The `oauth2_scheme` utilizes a `tokenUrl` to obtain the access token.  The `authenticate_user` function (located in `src.db.utils`) is responsible for validating the token and retrieving user information.  The access token is used to authorize subsequent requests to the Calendly API.


## Notes

- The code assumes the existence of several functions within `src.db.utils` and `src.integrations.Calendly.utils`.  These functions are not defined here but are crucial for the API to function correctly.
- Error handling could be improved by providing more specific error messages and potentially using a custom exception class.
- Input validation (e.g., for `start_time` and `end_time`) should be added for robustness.

