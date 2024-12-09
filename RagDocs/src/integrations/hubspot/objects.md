# Hubspot API Router

This document details the functions of the `hubspot_objects.py` file, which provides a FastAPI router for interacting with the Hubspot API.

## Imports

The file begins by importing necessary libraries:

* `fastapi`: For building the API.
* `requests`: For making HTTP requests to the Hubspot API.
* `src.db.schemas`: For Hubspot data schemas (presumably).
* `src.db.utils`: For user authentication (`authenticate_user`).
* `src.integrations.hubspot.utils`: For helper functions like `get_valid_access_token` and `validate_object_type`.
* `src.logger`: For logging.
* `json`: For JSON handling.


## Constants

* `HUBSPOT_BASE_URL`: Sets the base URL for the Hubspot API ("https://api.hubapi.com").

## Router Setup

An APIRouter is initialized with the prefix `/hubspot` and tag "hubspot":

```python
router = APIRouter(prefix='/hubspot', tags=["hubspot"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
```

`oauth2_scheme` is configured for OAuth2 authentication.


## API Endpoints

The file defines several API endpoints for interacting with Hubspot objects:


### 1. GET `/hubspot/{object_type}` - Read Objects

* **Path Parameter:**
    * `object_type`:  The type of Hubspot object (e.g., "contacts", "companies").
* **Query Parameter (Implicit):**
    * `auth_token`: OAuth2 authentication token (obtained via `token` endpoint).
* **Functionality:** Retrieves a list of Hubspot objects of the specified type.  Authenticates the user, validates the object type, fetches data from the Hubspot API, and returns the JSON response.  Handles HTTP exceptions and other errors.

### 2. POST `/hubspot/engagements` - Create Engagement

* **Body Parameter:**
    * `data`: A dictionary containing the engagement data.
* **Query Parameter (Implicit):**
    * `auth_token`: OAuth2 authentication token.
* **Functionality:** Creates a new Hubspot engagement.  Authenticates the user, validates that the object type is "contacts", sends a POST request to the Hubspot API, and returns the JSON response or raises an exception upon failure.


### 3. GET `/hubspot/{object_type}/{object_id}` - Get Object by ID

* **Path Parameters:**
    * `object_type`: The type of Hubspot object.
    * `object_id`: The ID of the object to retrieve.
* **Query Parameter:**
    * `properties`: (Optional) Comma-separated list of properties to retrieve.
* **Query Parameter (Implicit):**
    * `auth_token`: OAuth2 authentication token.
* **Functionality:** Retrieves a specific Hubspot object by its ID.  Handles optional property filtering.


### 4. POST `/hubspot/{object_type}` - Add Object

* **Path Parameter:**
    * `object_type`: The type of Hubspot object.
* **Body Parameter:**
    * `object_data`: A dictionary containing the data for the new object.
* **Query Parameter (Implicit):**
    * `auth_token`: OAuth2 authentication token.
* **Functionality:** Creates a new Hubspot object.


### 5. PUT `/hubspot/{object_type}/{object_id}` - Edit Object

* **Path Parameters:**
    * `object_type`: The type of Hubspot object.
    * `object_id`: The ID of the object to update.
* **Body Parameter:**
    * `update_data`: A dictionary containing the data to update.
* **Query Parameter (Implicit):**
    * `auth_token`: OAuth2 authentication token.
* **Functionality:** Updates an existing Hubspot object. Uses the PATCH method for partial updates.


### 6. DELETE `/hubspot/{object_type}/{object_id}` - Remove Object

* **Path Parameters:**
    * `object_type`: The type of Hubspot object.
    * `object_id`: The ID of the object to delete.
* **Query Parameter (Implicit):**
    * `auth_token`: OAuth2 authentication token.
* **Functionality:** Deletes a Hubspot object.


## Error Handling

All endpoints include comprehensive error handling using `try...except` blocks.  HTTPExceptions are raised for various scenarios, providing informative error messages to the client.

## Logging

A logger (`logger = Logger("hubspot_objects")`) is initialized for logging purposes.  However, its usage within the code is not explicitly shown.


This documentation provides a comprehensive overview of the provided Python file.  More detailed information might be required if the internal functions like `authenticate_user`, `get_valid_access_token`, and `validate_object_type` need further explanation.
