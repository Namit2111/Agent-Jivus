# Personas API Documentation

This document outlines the API endpoints for managing personas.

## Dependencies

* `datetime`: Used for timestamping updates.
* `src.db.schemas`: Defines Pydantic schemas for Personas, LinkedInInfo, and API responses.
* `src.utils.auth`: Handles authentication and authorization.  Provides `get_auth_response`.
* `src.db.utils`: Contains utility functions, including `handle_error` and `valid_persona_id`.
* `src.db.models`: Contains the `Personas` model for database interaction.
* `fastapi`: The FastAPI framework.
* `src.enums`: Contains UserRoles enum (not directly used in this code snippet but implied by context).


## API Endpoints

All endpoints are under the `/personas` prefix and are tagged as "personas".

### `/personas/user` (GET)

Returns a list of `PersonasResponse` objects for the currently authenticated user.

* **Request:**
    * Requires authentication via `Depends(get_auth_response)`.
* **Response:**
    * `200 OK`: A list of `PersonasResponse` objects.  Each object represents a persona.
    * `5xx`: Generic server error, handled by `handle_error`.


### `/personas/info/{persona_id}` (GET)

Returns detailed information about a persona, including LinkedIn data.

* **Request:**
    * `persona_id`: The ID of the persona (validated by `Depends(valid_persona_id)`).
* **Response:**
    * `200 OK`: A `LinkedInInfo` object containing LinkedIn API response, summary, LinkedIn URL, and buying style information.
    * `5xx`: Generic server error, handled by `handle_error`.
    * Uses `src.pre_call.utils.get_persona_profile_info` to fetch LinkedIn data.

### `/personas/{persona_id}` (GET)

Returns a single `PersonasResponse` object for a given persona ID.

* **Request:**
    * `persona_id`: The ID of the persona (validated by `Depends(valid_persona_id)`).
* **Response:**
    * `200 OK`: A `PersonasResponse` object.
    * `5xx`: Generic server error, handled by `handle_error`.


### `/personas/` (POST)

Creates a new persona.

* **Request:**
    * `persona_in`: A `Persona` object containing the persona data.
    * Requires authentication via `Depends(get_auth_response)`.
* **Response:**
    * `200 OK`: A `PersonasResponse` object representing the newly created persona.
    * `5xx`: Generic server error, handled by `handle_error`.


### `/personas/{persona_id}` (PUT)

Updates an existing persona.

* **Request:**
    * `new_persona`: A `Persona` object containing the updated persona data.
    * `persona_id`: The ID of the persona to update (validated by `Depends(valid_persona_id)`).
    * Requires authentication via `Depends(get_auth_response)`.
* **Response:**
    * `200 OK`: A `PersonasResponse` object representing the updated persona.
    * `424 Failed Dependency`: If the update fails.
    * `5xx`: Generic server error, handled by `handle_error`.


### `/personas/{persona_id}` (DELETE)

Deletes a persona.

* **Request:**
    * `persona_id`: The ID of the persona to delete (validated by `Depends(valid_persona_id)`).
* **Response:**
    * `200 OK`: `{"message": "success"}`
    * `5xx`: Generic server error, handled by `handle_error`.


## Error Handling

Generic exceptions are caught and handled by the `handle_error` function.  Specific error handling is implemented for the update endpoint.


## Data Models

The API uses several data models:

* **`Personas`:**  The database model for personas.
* **`Persona`:** The Pydantic schema for creating and updating personas.
* **`PersonasResponse`:** The Pydantic schema for API responses representing personas.
* **`LinkedInInfo`:** The Pydantic schema for LinkedIn profile information.


This documentation provides a comprehensive overview of the Personas API endpoints and their functionality.  Refer to the source code for detailed implementation details.
