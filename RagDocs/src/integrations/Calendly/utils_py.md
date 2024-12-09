# Calendly API Interaction Functions

This document describes the functions used to interact with the Calendly API.  These functions handle retrieving a user's PAT token, fetching user information, and retrieving event types.

## Functions

### `get_valid_PAT_token(user_id: int)`

Retrieves a valid Personal Access Token (PAT) for a given user ID from the database.

**Parameters:**

* `user_id: int`: The ID of the user.

**Returns:**

* `str`: The user's PAT token.

**Raises:**

* `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No PAT token found. Please connect your Calendly account.")`: If no PAT token is found for the user in the database.


### `getUserURI(user_id: int)`

Retrieves the Calendly URI for a given user ID.

**Parameters:**

* `user_id: int`: The ID of the user.

**Returns:**

* `str`: The user's Calendly URI.

**Raises:**

* `HTTPException`: If the Calendly API request fails (status code != 200). The detail of the exception will contain the JSON response from the Calendly API.


### `getUserEventTypes(user_id)`

Retrieves a list of event types for a given user ID.

**Parameters:**

* `user_id`: The ID of the user.

**Returns:**

* `list`: A list of event type dictionaries from the Calendly API.

**Raises:**

* `HTTPException`: If the Calendly API request fails (status code != 200). The detail of the exception will contain the JSON response from the Calendly API.


## Dependencies

* `fastapi`: For exception handling.
* `requests`: For making HTTP requests to the Calendly API.
* `src.db.models`: For accessing the database model `Integrations`.


## Usage Example

```python
from your_module import getUserEventTypes

user_id = 123  # Replace with actual user ID

try:
    event_types = getUserEventTypes(user_id)
    print(event_types)
except HTTPException as e:
    print(f"Error: {e.detail}")
```

This example shows how to use the `getUserEventTypes` function to retrieve event types for a user.  Error handling is included to catch potential `HTTPException`s.  Remember to replace `"your_module"` with the actual name of the module containing these functions.
