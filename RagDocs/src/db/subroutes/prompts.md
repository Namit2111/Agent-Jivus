# Prompts API Documentation

This document outlines the API endpoints for managing prompts.  All endpoints require administrator privileges.

## Imports

```python
from datetime import datetime
from src.enums import UserRoles
from src.logger import Logger
from src.db.schemas import PromptCreationInput, PromptResponse, PromptUpdateInput
from src.db.utils import handle_error, valid_prompt_id
from src.db.models import Prompts
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.utils.auth import get_auth_response
from src.utils.prompts import resolve_prompt_name
```

## Authentication

The API uses OAuth2 for authentication.  The token URL is `/token`.

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
```

## Router

The API is defined using FastAPI's `APIRouter`.

```python
router = APIRouter(prefix="/prompts", tags=["prompts"])
logger = Logger("prompts")
```

## Authentication Middleware

This middleware ensures that only ADMIN or SUPER_ADMIN users can access the API endpoints.

```python
def ensure_admin_user(auth_response=Depends(get_auth_response)):
    # ... (Implementation details)
```

## Helper Function

This function retrieves a prompt by ID, raising an exception if not found.

```python
def get_prompt(id: str = Depends(valid_prompt_id)) -> Prompts:
    # ... (Implementation details)
```

## API Endpoints

### List Prompts (GET /prompts/list)

```http
GET /prompts/list
```

Lists all prompts.  Requires ADMIN or SUPER_ADMIN privileges.

**Response:**

* `200 OK`: A list of `PromptResponse` objects.
* `401 Unauthorized`: If the user is not an administrator.

**TODO:**  This endpoint is marked as TODO in the code.

### Read Prompt (GET /prompts/{id})

```http
GET /prompts/{id}
```

Retrieves a specific prompt by ID. Requires ADMIN or SUPER_ADMIN privileges.

**Path Parameters:**

* `id`: The ID of the prompt.

**Response:**

* `200 OK`: A `PromptResponse` object.
* `401 Unauthorized`: If the user is not an administrator.
* `404 Not Found`: If the prompt is not found.
* `500 Internal Server Error`: If an error occurs during processing.


### Create Prompt (POST /prompts)

```http
POST /prompts
```

Creates a new prompt. Requires ADMIN or SUPER_ADMIN privileges.

**Request Body:**

* `PromptCreationInput`:  Details for creating a prompt.

**Response:**

* `200 OK`: A `PromptResponse` object representing the newly created prompt.
* `401 Unauthorized`: If the user is not an administrator.
* `500 Internal Server Error`: If an error occurs during processing.


### Update Prompt (PUT /prompts/{id})

```http
PUT /prompts/{id}
```

Updates a specific prompt by ID. Requires ADMIN or SUPER_ADMIN privileges.

**Path Parameters:**

* `id`: The ID of the prompt.

**Request Body:**

* `PromptUpdateInput`: Details for updating a prompt.

**Response:**

* `200 OK`: A `PromptResponse` object representing the updated prompt.
* `401 Unauthorized`: If the user is not an administrator.
* `404 Not Found`: If the prompt is not found.
* `424 Failed Dependency`: If the prompt update fails.
* `500 Internal Server Error`: If an error occurs during processing.


### Delete Prompt (DELETE /prompts/{id})

```http
DELETE /prompts/{id}
```

Deletes a specific prompt by ID. Requires ADMIN or SUPER_ADMIN privileges.

**Path Parameters:**

* `id`: The ID of the prompt.

**Response:**

* `200 OK`: `{"message": "success"}`
* `401 Unauthorized`: If the user is not an administrator.
* `404 Not Found`: If the prompt is not found.
* `500 Internal Server Error`: If an error occurs during processing.


## Error Handling

The `handle_error` function is used to handle exceptions gracefully, likely logging the error and returning a generic error response to the client.  Specific error handling is described in individual endpoint responses.

