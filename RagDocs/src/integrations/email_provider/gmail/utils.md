```markdown
# get_valid_gmail_credentials.py

This module provides a function to retrieve and validate Gmail credentials for a given user ID.


## Function: `get_valid_gmail_credentials(user_id: int)`

This function retrieves valid Google OAuth2 credentials for a user's Gmail account.  It checks the database for an existing integration, verifies the presence of an access token, and constructs `google.oauth2.credentials.Credentials` object.

**Parameters:**

* `user_id: int`: The ID of the user whose Gmail credentials are required.

**Returns:**

* `google.oauth2.credentials.Credentials`: A `Credentials` object containing the user's Gmail access and refresh tokens, ready to be used with Google APIs.

**Raises:**

* `fastapi.HTTPException(status_code=404, detail="No access token found. Please connect your HubSpot account.")`:  If no integration is found for the given user ID or if the integration data is missing the `access_token`.


**Dependencies:**

* `src.db.models`:  Provides the `Integrations` model for accessing user integration data.
* `src.config`: Contains configuration settings, including Google OAuth 2 client credentials (`GOOGLE_TOKEN_URI`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`).
* `google.oauth2.credentials`: Used for constructing the `Credentials` object.
* `fastapi`: Used for raising HTTP exceptions.


**Logic:**

1. **Retrieve Integration:** Queries the `Integrations` database collection to find an integration entry for the given `user_id` and `service="gmail"`.
2. **Check Access Token:** Verifies that the retrieved integration exists and contains an `access_token` in its `data` field.  If not, it raises a 404 HTTPException.
3. **Create Credentials Object:** Constructs a `google.oauth2.credentials.Credentials` object using the retrieved `access_token`, `refresh_token`, and configuration parameters from `src.config`.
4. **Return Credentials:** Returns the constructed `Credentials` object.

**Example Usage:**

```python
from get_valid_gmail_credentials import get_valid_gmail_credentials

try:
    creds = get_valid_gmail_credentials(user_id=123)
    # Use the creds object to access Google Gmail API
except HTTPException as e:
    print(f"Error: {e.detail}")
```
```
