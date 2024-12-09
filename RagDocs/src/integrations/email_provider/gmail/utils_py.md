# `get_valid_gmail_credentials` Function Documentation

## Description

This function retrieves and validates Google Gmail credentials for a given user ID.  It checks for the existence of a valid access token in the database and constructs a `google.oauth2.credentials.Credentials` object if found.  If no valid token is found, it raises an HTTPException.


## Parameters

* `user_id` (int): The ID of the user whose Gmail credentials are to be retrieved.


## Returns

* `google.oauth2.credentials.Credentials`: A `Credentials` object containing the user's Gmail access and refresh tokens,  token URI, client ID, and client secret if found.


## Raises

* `fastapi.HTTPException`:  If no integration record is found for the given user ID or if the 'access_token' is missing from the integration data, a 404 Not Found exception is raised with a descriptive message.


## Imports

* `Integrations`: From `src.db.models`, this is presumed to be a model for storing user integrations.
* `config`: From `src.config`, this is presumed to be a configuration module containing Google API credentials.
* `Credentials`: From `google.oauth2.credentials`, this is used to create the credentials object.
* `HTTPException`, `status`: From `fastapi`, used for error handling.


## Usage Example

```python
from src.auth.gmail import get_valid_gmail_credentials

try:
    creds = get_valid_gmail_credentials(user_id=123)
    # Use the 'creds' object to access Gmail API
except HTTPException as e:
    print(f"Error retrieving credentials: {e.detail}") 
```


## Notes

* The function relies on a database model (`Integrations`) to store user integration data, including access and refresh tokens.
* Configuration values for the Google API (token URI, client ID, client secret) are loaded from the `config` module.
* Error handling is implemented using FastAPI's `HTTPException` to provide informative error responses.


