```markdown
# get_valid_smtp_credentials.py

This module provides a function to retrieve valid SMTP credentials from the database for a given user ID.


## Function: `get_valid_smtp_credentials(user_id: int)`

Retrieves SMTP email and password for a given user ID.

**Parameters:**

* `user_id (int)`: The ID of the user.

**Returns:**

* `tuple(str, str)`: A tuple containing the email address and SMTP password if found.  Returns None if credentials are not found.

**Raises:**

* `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No email or password found. Please connect your account with SMTP.")`: If no integration with service "smtp" is found for the given user ID, or if the 'email' or 'smtpPassword' keys are missing from the integration data.

**Functionality:**

1. Queries the `Integrations` model to find an integration record matching the given `user_id` and `service="smtp"`.
2. Checks if an integration record exists and if it contains both 'email' and 'smtpPassword' keys within its `data` field.
3. If the integration record or required keys are missing, it raises an HTTPException indicating that the user needs to connect their account with SMTP.
4. If both email and password are found, it returns them as a tuple.

**Example Usage:**

```python
from src.get_valid_smtp_credentials import get_valid_smtp_credentials

try:
    email, password = get_valid_smtp_credentials(user_id=123)
    print(f"Email: {email}, Password: {password}")
except HTTPException as e:
    print(f"Error: {e.detail}")
```

**Dependencies:**

* `src.db.models`:  Contains the `Integrations` model.
* `fastapi`: For handling HTTP exceptions.

```
