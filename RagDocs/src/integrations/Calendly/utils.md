# Calendly API Interaction Functions

This Python file provides functions to interact with the Calendly API, specifically for retrieving user information and event types.  It uses the `fastapi` library for exception handling and `requests` for making HTTP requests.

## Functions

### `get_valid_PAT_token(user_id: int)`

Retrieves a valid Calendly Personal Access Token (PAT) for a given user ID.

**Args:**

* `user_id: int`: The ID of the user.

**Returns:**

* `str`: The PAT token.

**Raises:**

* `HTTPException 404`: If no PAT token is found for the user.


### `getUserURI(user_id: int)`

Retrieves the URI of a Calendly user using their PAT token.

**Args:**

* `user_id: int`: The ID of the user.

**Returns:**

* `str`: The URI of the Calendly user.

**Raises:**

* `HTTPException`: If the Calendly API request fails (non-200 status code).  The detail of the exception will include the JSON response from the Calendly API.


### `getUserEventTypes(user_id)`

Retrieves a list of event types for a given user from the Calendly API.

**Args:**

* `user_id`: The ID of the user.

**Returns:**

* `list`: A list of Calendly event type dictionaries.

**Raises:**

* `HTTPException`: If the Calendly API request fails (non-200 status code). The detail of the exception will include the JSON response from the Calendly API.


## Dependencies

* `fastapi`
* `requests`
* `src.db.models.Integrations` (Assumed to be a custom model for storing user integration data, including the PAT token)


## Usage Example

```python
from calendly_api_functions import getUserEventTypes

try:
    event_types = getUserEventTypes(123) # Replace 123 with a valid user ID
    print(event_types)
except HTTPException as e:
    print(f"Error: {e.detail}")
```

This example shows how to use the `getUserEventTypes` function.  Remember to replace `123` with an actual user ID and ensure that the `Integrations` model is correctly configured and accessible.
