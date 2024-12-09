# Prompts API Documentation

This document describes the API endpoints for managing prompts.  All endpoints require administrator-level authentication.

## Dependencies

- `datetime`: For timestamping updates.
- `src.enums`: Contains the `UserRoles` enum.
- `src.logger`:  Custom logging module.
- `src.db.schemas`: Defines input and output schemas (`PromptCreationInput`, `PromptResponse`, `PromptUpdateInput`).
- `src.db.utils`: Utility functions, including `handle_error` and `valid_prompt_id`.
- `src.db.models`:  Defines the `Prompts` model.
- `fastapi`: The FastAPI framework.
- `fastapi.security`: For OAuth2 authentication.
- `src.utils.auth`: Authentication utilities, including `get_auth_response`.
- `src.utils.prompts`: Utility functions, including `resolve_prompt_name`.


## Authentication

All endpoints use OAuth2 authentication with the token URL `/token`.  Access is restricted to users with `ADMIN` or `SUPER_ADMIN` roles.


## Endpoints

All endpoints are under the `/prompts` prefix.

### `/prompts/list` (GET)

**Description:** Lists all prompts.

**Request:**

- Requires administrator authentication (`ensure_admin_user` middleware).

**Response:**

- `200 OK`: A list of `PromptResponse` objects.
- `401 Unauthorized`: If the user is not an administrator.
- `500 Internal Server Error`: If an error occurs during processing.


**Example Response:**

```json
[
  {
    "id": "...",
    "name": "...",
    "body": "...",
    "modelSettings": { ... },
    "createdAt": "...",
    "updatedAt": "..."
  },
  // ... more prompts
]
```

### `/prompts/{id}` (GET)

**Description:** Retrieves a specific prompt by ID.

**Request:**

- `id`: The ID of the prompt.  Validated by `valid_prompt_id`.
- Requires administrator authentication (`ensure_admin_user` middleware).

**Response:**

- `200 OK`: A `PromptResponse` object.
- `401 Unauthorized`: If the user is not an administrator.
- `404 Not Found`: If the prompt is not found.
- `500 Internal Server Error`: If an error occurs during processing.

### `/prompts/` (POST)

**Description:** Creates a new prompt.

**Request:**

- `prompt`: A `PromptCreationInput` object.
- Requires administrator authentication (`ensure_admin_user` middleware).

**Response:**

- `200 OK`: A `PromptResponse` object representing the newly created prompt.
- `401 Unauthorized`: If the user is not an administrator.
- `500 Internal Server Error`: If an error occurs during processing.

### `/prompts/{id}` (PUT)

**Description:** Updates an existing prompt.

**Request:**

- `id`: The ID of the prompt to update.
- `new_prompt`: A `PromptUpdateInput` object containing the updated data.
- Requires administrator authentication (`ensure_admin_user` middleware).

**Response:**

- `200 OK`: A `PromptResponse` object representing the updated prompt.
- `401 Unauthorized`: If the user is not an administrator.
- `404 Not Found`: If the prompt is not found.
- `424 Failed Dependency`: If the prompt update fails.
- `500 Internal Server Error`: If an error occurs during processing.

### `/prompts/{id}` (DELETE)

**Description:** Deletes a prompt.

**Request:**

- `id`: The ID of the prompt to delete. Validated by `valid_prompt_id`.
- Requires administrator authentication (`ensure_admin_user` middleware).

**Response:**

- `200 OK`:  A JSON object `{ "message": "success" }`.
- `401 Unauthorized`: If the user is not an administrator.
- `404 Not Found`: If the prompt is not found.
- `500 Internal Server Error`: If an error occurs during processing.


## Error Handling

The `handle_error` function is used to handle exceptions gracefully.  Specific error codes are returned where appropriate (e.g., 401, 404, 500).

## TODO

- `/prompts/list`: The `list_prompts` endpoint is marked with a TODO.  Presumably, further implementation or refinement is required.


This documentation provides a comprehensive overview of the Prompts API.  Refer to the code for detailed implementation specifics.
