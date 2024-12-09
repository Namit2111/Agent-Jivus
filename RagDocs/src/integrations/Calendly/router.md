# Calendly API Integration

This document outlines the functionality of the `calendly.py` file, which provides an API for interacting with the Calendly platform.  The API uses FastAPI for routing and handling requests.


## Imports

The file starts by importing necessary modules:

* `datetime`, `timedelta`: For date and time manipulation (although not directly used in the provided code).
* `APIRouter`, `Depends`, `HTTPException`, `status`: FastAPI components for creating API endpoints, dependency injection, error handling, and HTTP status codes.
* `OAuth2PasswordBearer`:  For OAuth2 authentication.
* `authenticate_user`: A function (presumably from `src.db.utils`) for user authentication.
* `requests`: For making HTTP requests to the Calendly API.
* `get_valid_PAT_token`, `getUserEventTypes`, `getUserURI`: Functions from `src.integrations.Calendly.utils` for interacting with Calendly.


## API Router

An `APIRouter` is initialized with the prefix `/calendly`, which means all routes defined within this router will start with this prefix.  An OAuth2 authentication scheme (`oauth2_scheme`) is defined using `OAuth2PasswordBearer`, indicating that authentication is required for all endpoints.


## API Endpoints

The file defines three API endpoints:

### `/calendly/user` (GET)

This endpoint retrieves user information.

**Parameters:**

* `auth_token: str = Depends(oauth2_scheme)`:  The authentication token (obtained via OAuth2).

**Functionality:**

1. Authenticates the user using `authenticate_user`.
2. If authentication fails, raises a `HTTPException` with a 401 Unauthorized status.
3. Retrieves the user ID from the authentication response.
4. Calls `getUserURI` to get the user's URI and returns it.
5. Includes comprehensive error handling for both `HTTPException` and other exceptions, returning appropriate HTTP status codes.


### `/calendly/user-event-types` (GET)

This endpoint retrieves a user's event types.

**Parameters:**

* `auth_token: str = Depends(oauth2_scheme)`: The authentication token.

**Functionality:**

1. Authenticates the user.
2. If authentication fails, raises a `HTTPException` with a 401 Unauthorized status.
3. Retrieves the user ID from the authentication response.
4. Calls `getUserEventTypes` to get the user's event types and returns them.
5. Includes comprehensive error handling for exceptions.


### `/calendly/check-availability` (GET)

This endpoint checks user availability within a given time range.

**Parameters:**

* `start_time: str`: The start time of the availability check.
* `end_time: str`: The end time of the availability check.
* `auth_token: str = Depends(oauth2_scheme)`: The authentication token.

**Functionality:**

1. Authenticates the user.
2. If authentication fails, raises a `HTTPException` with a 401 Unauthorized status.
3. Retrieves the user ID.
4. Obtains a valid Calendly Personal Access Token (PAT) using `get_valid_PAT_token`.
5. Retrieves the user's event types using `getUserEventTypes`.  If no event types are found, raises a 404 Not Found error.
6. Makes a request to the Calendly API (`https://api.calendly.com/event_type_available_times`) using the PAT, start time, end time, and the URI of the first event type.
7. Returns the API response if successful (status code 200).
8. Raises a `HTTPException` with the appropriate status code and details if the Calendly API request fails.
9. Includes comprehensive error handling for exceptions.



## Error Handling

All endpoints include robust error handling.  `HTTPException`s are caught and re-raised, while other exceptions are caught and converted to `HTTPException`s with a 400 Bad Request status code.  This ensures that appropriate HTTP status codes are returned to the client in all scenarios.
