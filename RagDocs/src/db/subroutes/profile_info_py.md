# Profile API Documentation

This document describes the API endpoints for managing profiles.  The API uses FastAPI and interacts with a MongoDB database.

## Table of Contents

* [Endpoints](#endpoints)
    * [/profile/linkedin (POST)](#profilelinkedin-post)
    * [/profile/linkedin (PATCH)](#profilelinkedin-patch)
    * [/profile/{profile_id} (GET)](#profileprofile_id-get)
    * [/profile/{profile_id} (POST)](#profileprofile_id-post)
    * [/profile/{profile_id} (PUT)](#profileprofile_id-put)
    * [/profile/{profile_id} (DELETE)](#profileprofile_id-delete)
* [Data Models](#data-models)
* [Error Handling](#error-handling)
* [Dependencies](#dependencies)


## Endpoints

All endpoints are prefixed with `/profile` and are tagged as `personas`.

### `/profile/linkedin (POST)`

Creates a new profile from a LinkedIn URL.

**Request:**

* `linkedinUrl`: (str, required) The LinkedIn profile URL.
* `profileType`: (ProfileTypes, required) The type of profile.  See [Data Models](#data-models) for details.
* `hubspotInfo`: (HubspotInfo, optional) Hubspot information. See [Data Models](#data-models) for details.
* `productInfo`: (ProductInfo, optional) Product information. See [Data Models](#data-models) for details.


**Response:**

* `200 OK`: Returns a `ProfileInfoResponse` object. See [Data Models](#data-models) for details.

**Example:**

```json
{
  "linkedinUrl": "https://www.linkedin.com/in/example",
  "profileType": "CUSTOMER",
  "hubspotInfo": { ... },
  "productInfo": { ... }
}
```

### `/profile/linkedin (PATCH)`

Updates the LinkedIn information for an existing profile.

**Request:**

* `linkedIN_data`: (LinkedInInfo, required) Updated LinkedIn information. See [Data Models](#data-models) for details.
* `profile_id`: (str, required) The ID of the profile to update.  This is automatically validated by `valid_profile_id` dependency.

**Response:**

* `200 OK`: Returns `true` on success, `false` on failure.


### `/profile/{profile_id} (GET)`

Retrieves a profile by its ID.

**Request:**

* `profile_id`: (str, required) The ID of the profile to retrieve. This is automatically validated by `valid_profile_id` dependency.

**Response:**

* `200 OK`: Returns a `ProfileInfoResponse` object. See [Data Models](#data-models) for details.
* `404 Not Found`: If the profile is not found.


### `/profile/{profile_id} (POST)`

Creates a new profile.  Note that the `profileId` should be provided as part of the `profile_in` body.

**Request:**

* `profile_in`: (ProfileInfo, required) The profile data. See [Data Models](#data-models) for details.

**Response:**

* `200 OK`: Returns a `ProfileInfoResponse` object. See [Data Models](#data-models) for details.


### `/profile/{profile_id} (PUT)`

Updates an existing profile.

**Request:**

* `new_profile`: (ProfileInfo, required) The updated profile data.  See [Data Models](#data-models) for details.
* `profile_id`: (str, required) The ID of the profile to update. This is automatically validated by `valid_profile_id` dependency.

**Response:**

* `200 OK`: Returns a `ProfileInfoResponse` object.
* `424 Failed Dependency`: If the update fails.


### `/profile/{profile_id} (DELETE)`

Deletes a profile by its ID.

**Request:**

* `profile_id`: (str, required) The ID of the profile to delete. This is automatically validated by `valid_profile_id` dependency.

**Response:**

* `200 OK`: Returns `{"message": "success"}` on success.


## Data Models

* **`ProfileInfos`:** MongoDB model for storing profile information.
* **`LinkedInInfos`:** MongoDB model for storing LinkedIn-specific profile information.
* **`ProfileInfo`:** Pydantic model for profile data in requests and responses.
* **`ProfileInfoResponse`:** Pydantic model for profile data in responses.
* **`HubspotInfo`:** Pydantic model for Hubspot data.
* **`ProductInfo`:** Pydantic model for product data.
* **`LinkedInInfo`:** Pydantic model for LinkedIn data.
* **`ProfileTypes`:** An enum defining the types of profiles (e.g., CUSTOMER, PROSPECT).


The exact structure of these models is not detailed here but can be inferred from the code.


## Error Handling

Errors are handled by the `handle_error` function.  Specific error codes might be returned depending on the error type.  Generally, 5xx errors indicate server-side issues, while 4xx errors indicate client-side issues (e.g., invalid input).


## Dependencies

* `valid_profile_id`: A dependency function that validates the profile ID.  This function likely performs checks to ensure the ID is valid and the profile exists.  It throws an exception if the profile ID is invalid.
