# `get_valid_smtp_credentials` Function Documentation

## Description

This function retrieves valid SMTP email and password credentials from the database for a given user ID.  It checks for the existence of the credentials and raises an HTTPException if they are missing.

## Parameters

* `user_id` (int): The ID of the user whose SMTP credentials are to be retrieved.

## Returns

A tuple containing:

* `email` (str): The user's SMTP email address.
* `smtpPassword` (str): The user's SMTP password.

## Raises

* `HTTPException`:  If no integration with service type "smtp" is found for the given user ID, or if the `email` or `smtpPassword` keys are missing from the integration data. The HTTP status code will be 404 (Not Found), and the detail message will indicate that the email and/or password are missing, prompting the user to connect their account with SMTP.


## Imports

* `Integrations` from `src.db.models`:  Presumably a model for managing integrations, providing access to database operations (`.objects`).  It's assumed that `Integrations` objects have a `userId`, `service` and `data` attribute (where `data` is a dictionary).
* `HTTPException`, `status` from `fastapi`: Used for exception handling and setting HTTP status codes.


## Example Usage

```python
try:
    email, password = get_valid_smtp_credentials(user_id=123)
    print(f"Email: {email}, Password: {password}")
except HTTPException as e:
    print(f"Error: {e.detail}")
```
