# Personas API Documentation

This document outlines the API endpoints for managing personas.  All endpoints are under the `/personas` prefix and use the `Personas` model for data manipulation.


## Imports

```python
from datetime import datetime
from src.db.schemas import LinkedInInfo, Persona, PersonasResponse
from src.utils.auth import get_auth_response
from src.db.utils import handle_error, valid_persona_id
from src.db.models import Personas
from fastapi import APIRouter, Depends, HTTPException, status
from src.enums import UserRoles
```

## Router

```python
router = APIRouter(prefix="/personas", tags=["personas"])
```

## Helper Function

```python
def get_persona(persona_id: str = Depends(valid_persona_id)) -> Personas:
    """Retrieves a persona object from the database using its ID.

    Args:
        persona_id (str, optional): The ID of the persona. Defaults to Depends(valid_persona_id).

    Returns:
        Personas: The Persona object.
    """
    return Personas.objects(id=persona_id).first()
```

## API Endpoints

### GET `/personas/user`

Reads all personas associated with the authenticated user.

* **Response:** `list[PersonasResponse]`
* **Authentication:** Requires authentication via `get_auth_response`.
* **Error Handling:** Uses `handle_error` for exception management.

```python
@router.get("/user", response_model=list[PersonasResponse])
def read_personas_of_user(auth_response: dict = Depends(get_auth_response)):
    # ... implementation ...
```


### GET `/personas/info/{persona_id}`

Retrieves LinkedIn information for a specific persona.

* **Path Parameter:**
    * `persona_id (str)`:  The ID of the persona.  Uses `Depends(valid_persona_id)` for validation.
* **Response:** `LinkedInInfo`
* **Error Handling:** Uses `handle_error` for exception management.

```python
@router.get("/info/{persona_id}", response_model=LinkedInInfo)
def read_persona_info(persona_id: str = Depends(valid_persona_id)):
    # ... implementation ...
```

### GET `/personas/{persona_id}`

Retrieves a specific persona.

* **Path Parameter:**
    * `persona_id (str)`: The ID of the persona. Uses `Depends(valid_persona_id)` for validation.
* **Response:** `PersonasResponse`
* **Error Handling:** Uses `handle_error` for exception management.

```python
@router.get("/{persona_id}", response_model=PersonasResponse)
def read_persona(persona_id: str = Depends(valid_persona_id)):
    # ... implementation ...
```

### POST `/personas/`

Creates a new persona.

* **Request Body:** `Persona`
* **Authentication:** Requires authentication via `get_auth_response`.
* **Response:** `PersonasResponse`
* **Error Handling:** Uses `handle_error` for exception management.

```python
@router.post("/", response_model=PersonasResponse)
def create_persona(persona_in: Persona, auth_response: dict = Depends(get_auth_response)):
    # ... implementation ...
```

### PUT `/personas/{persona_id}`

Updates an existing persona.

* **Path Parameter:**
    * `persona_id (str)`: The ID of the persona. Uses `Depends(valid_persona_id)` for validation.
* **Request Body:** `Persona`
* **Authentication:** Requires authentication via `get_auth_response`.
* **Response:** `PersonasResponse`
* **Error Handling:** Uses `handle_error` and raises `HTTPException` for update failures.

```python
@router.put("/{persona_id}", response_model=PersonasResponse)
def update_persona(new_persona: Persona, persona_id: str = Depends(valid_persona_id), auth_response: dict = Depends(get_auth_response)):
    # ... implementation ...
```

### DELETE `/personas/{persona_id}`

Deletes a persona.

* **Path Parameter:**
    * `persona_id (str)`: The ID of the persona. Uses `Depends(valid_persona_id)` for validation.
* **Response:** `{"message": "success"}`
* **Error Handling:** Uses `handle_error` for exception management.

```python
@router.delete("/{persona_id}")
def delete_persona(persona_id: str = Depends(valid_persona_id)):
    # ... implementation ...
```

This documentation provides a comprehensive overview of the Personas API endpoints, including their functionality, parameters, responses, and error handling mechanisms.  Remember to consult the `src.db.schemas` and `src.db.models` modules for details on the data structures used.
