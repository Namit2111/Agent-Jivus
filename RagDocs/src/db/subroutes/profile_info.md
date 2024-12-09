# Profile API Documentation

This document describes the API endpoints for managing profile information.  The API uses FastAPI and interacts with a MongoDB database.

## Table of Contents

* [Import Statements](#import-statements)
* [Router Definition](#router-definition)
* [Helper Function: `get_profile`](#helper-function-get_profile)
* [API Endpoints](#api-endpoints)
    * [/linkedin (POST)](#linkedin-post)
    * [/linkedin (PATCH)](#linkedin-patch)
    * /{profile_id} (GET)](#profile_id-get)
    * /{profile_id} (POST)](#profile_id-post)
    * /{profile_id} (PUT)](#profile_id-put)
    * /{profile_id} (DELETE)](#profile_id-delete)

## Import Statements

The API relies on several libraries:

* `datetime`: For handling timestamps.
* `bson.ObjectId`: For MongoDB object IDs.
* `fastapi`: The web framework.
* `pydantic`: For data validation.
* `src.db.models`:  Database models (presumably `LinkedInInfos` and `ProfileInfos`).
* `src.db.schemas`: Pydantic schemas (`HubspotInfo`, `LinkedInInfo`, `ProductInfo`, `ProfileInfo`, `ProfileInfoResponse`).
* `src.db.utils`: Utility functions, including `handle_error` and `valid_profile_id`.
* `src.enums`: Enumerations, specifically `ProfileTypes`.
* `src.pre_call.utils`: Utility functions, including `linkedin_summary_generation`.


## Router Definition

```python
router = APIRouter(prefix="/profile", tags=["personas"])
```

The API endpoints are defined under the `/profile` prefix and grouped under the "personas" tag.


## Helper Function: `get_profile`

```python
def get_profile(profile_id: str = Depends(valid_profile_id)):
    return ProfileInfos.objects(id=profile_id).first()
```

This function retrieves a profile from the database based on the provided `profile_id`.  It uses the `valid_profile_id` dependency to validate the ID.


## API Endpoints

### `/linkedin` (POST)

Creates a new profile from a LinkedIn URL.

* **Path:** `/profile/linkedin`
* **Method:** `POST`
* **Request Body:**
    * `linkedinUrl`: `str` - The LinkedIn profile URL.
    * `profileType`: `ProfileTypes` - The type of profile.
    * `hubspotInfo`: `HubspotInfo | None` - Optional HubSpot information.
    * `productInfo`: `ProductInfo | None` - Optional product information.
* **Response:** `ProfileInfoResponse` - The created profile information.
* **Error Handling:** Uses `handle_error` to manage exceptions.


### `/linkedin` (PATCH)

Updates an existing LinkedIn profile information.

* **Path:** `/profile/linkedin`
* **Method:** `PATCH`
* **Request Body:**
    * `linkedIN_data`: `LinkedInInfo` - Updated LinkedIn information.
    * `profile_id`: `str` (Depends on `valid_profile_id`) - The ID of the profile to update.
* **Response:** `bool` - `True` if successful, `False` otherwise.
* **Error Handling:** Uses `handle_error` to manage exceptions.


### /{profile_id} (GET)

Retrieves a profile by ID.

* **Path:** `/profile/{profile_id}`
* **Method:** `GET`
* **Path Parameters:**
    * `profile_id`: `str` (Depends on `valid_profile_id`) - The ID of the profile to retrieve.
* **Response:** `ProfileInfoResponse` - The profile information.
* **Error Handling:** Uses `handle_error` to manage exceptions.


### /{profile_id} (POST)

Creates a new profile.

* **Path:** `/profile/{profile_id}`
* **Method:** `POST`
* **Request Body:** `ProfileInfo` - The profile information to create.
* **Response:** `ProfileInfoResponse` - The created profile information.
* **Error Handling:** Uses `handle_error` to manage exceptions.


### /{profile_id} (PUT)

Updates an existing profile.

* **Path:** `/profile/{profile_id}`
* **Method:** `PUT`
* **Request Body:** `ProfileInfo` - The updated profile information.
* **Path Parameters:**
    * `profile_id`: `str` (Depends on `valid_profile_id`) - The ID of the profile to update.
* **Response:** `ProfileInfoResponse` - The updated profile information.  Returns 424 error if update fails.
* **Error Handling:** Uses `handle_error` to manage exceptions.


### /{profile_id} (DELETE)

Deletes a profile by ID.

* **Path:** `/profile/{profile_id}`
* **Method:** `DELETE`
* **Path Parameters:**
    * `profile_id`: `str` (Depends on `valid_profile_id`) - The ID of the profile to delete.
* **Response:** `{"message": "success"}` - A success message.
* **Error Handling:** Uses `handle_error` to manage exceptions.


This documentation provides a comprehensive overview of the Profile API.  Remember to consult the source code for detailed implementation specifics and schema definitions.
