# HubSpot API Integration

This document describes a FastAPI application that provides an interface for interacting with the HubSpot API.  The application handles various CRUD (Create, Read, Update, Delete) operations on HubSpot objects.

## Dependencies

*   `fastapi`
*   `requests`
*   `src.db.schemas` (Assumed to contain `HubspotInfo` schema)
*   `src.db.utils` (Assumed to contain `authenticate_user` function)
*   `src.integrations.hubspot.utils` (Assumed to contain `get_valid_access_token` and `validate_object_type` functions)
*   `src.logger` (Assumed to contain `Logger` class)


## API Endpoints

All endpoints are prefixed with `/hubspot` and are tagged as "hubspot".  Authentication is required for all endpoints using an OAuth2 token.

### `/hubspot/{object_type}`  `GET`

Reads a list of HubSpot objects of the specified type.

**Parameters:**

*   `object_type`:  (str, path) The type of HubSpot object (e.g., "contacts", "companies").
*   `auth_token`: (str, query, required) OAuth2 authentication token.

**Response:**

*   `200 OK`: A JSON array representing the HubSpot objects.
*   `400 Bad Request`: Invalid object type.
*   `401 Unauthorized`: Invalid authentication token.
*   Other Status Codes:  Error codes from HubSpot API.


### `/hubspot/engagements` `POST`

Creates a new HubSpot engagement.

**Parameters:**

*   `data`: (dict, body, required)  The engagement data to create.  The exact schema depends on the HubSpot API.
*   `auth_token`: (str, query, required) OAuth2 authentication token.

**Response:**

*   `200 OK`:  Engagement created successfully (JSON response from HubSpot).
*   `400 Bad Request`: Invalid object type or other errors.
*   `401 Unauthorized`: Invalid authentication token.
*   Other Status Codes: Error codes from HubSpot API.


### `/hubspot/{object_type}/{object_id}` `GET`

Retrieves a single HubSpot object by its ID.

**Parameters:**

*   `object_type`: (str, path) The type of HubSpot object.
*   `object_id`: (str, path) The ID of the HubSpot object.
*   `properties`: (str, query, optional) Comma-separated list of properties to retrieve. Defaults to all properties if omitted.
*   `auth_token`: (str, query, required) OAuth2 authentication token.

**Response:**

*   `200 OK`: A JSON object representing the HubSpot object.
*   `400 Bad Request`: Invalid object type.
*   `401 Unauthorized`: Invalid authentication token.
*   Other Status Codes: Error codes from HubSpot API.


### `/hubspot/{object_type}` `POST`

Adds a new HubSpot object.

**Parameters:**

*   `object_type`: (str, path) The type of HubSpot object.
*   `object_data`: (dict, body, required) The data for the new object.
*   `auth_token`: (str, query, required) OAuth2 authentication token.

**Response:**

*   `201 Created`: The newly created object (JSON response from HubSpot).
*   `400 Bad Request`: Invalid object type or data.
*   `401 Unauthorized`: Invalid authentication token.
*   Other Status Codes: Error codes from HubSpot API.


### `/hubspot/{object_type}/{object_id}` `PUT`

Updates an existing HubSpot object.

**Parameters:**

*   `object_type`: (str, path) The type of HubSpot object.
*   `object_id`: (str, path) The ID of the HubSpot object to update.
*   `update_data`: (dict, body, required) The data to update.
*   `auth_token`: (str, query, required) OAuth2 authentication token.

**Response:**

*   `200 OK`: The updated object (JSON response from HubSpot).
*   `400 Bad Request`: Invalid object type or data.
*   `401 Unauthorized`: Invalid authentication token.
*   Other Status Codes: Error codes from HubSpot API.


### `/hubspot/{object_type}/{object_id}` `DELETE`

Deletes a HubSpot object.

**Parameters:**

*   `object_type`: (str, path) The type of HubSpot object.
*   `object_id`: (str, path) The ID of the HubSpot object to delete.
*   `auth_token`: (str, query, required) OAuth2 authentication token.

**Response:**

*   `204 No Content`: Object deleted successfully.
*   `400 Bad Request`: Invalid object type.
*   `401 Unauthorized`: Invalid authentication token.
*   Other Status Codes: Error codes from HubSpot API.


## Error Handling

The application uses `HTTPException` to handle errors.  Generic exceptions are caught and returned as `400 Bad Request`.  Specific HTTP exceptions (like `401 Unauthorized`) are raised as appropriate.


## Authentication

Authentication is handled by the `authenticate_user` function (from `src.db.utils`), which validates the OAuth2 token.  The `get_valid_access_token` function (from `src.integrations.hubspot.utils`) retrieves a valid access token for making requests to the HubSpot API.  The token is obtained using the user id from successful authentication.
