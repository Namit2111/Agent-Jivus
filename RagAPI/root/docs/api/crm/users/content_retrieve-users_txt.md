# HubSpot Account | Users API

This document details the HubSpot Account Users API, allowing retrieval and update of user information within a HubSpot account.  This API is particularly useful for synchronizing HubSpot user data with external systems like workforce management tools.

## API Endpoints

The Users API uses several endpoints for different operations:

* **Retrieve Users:**
    * **GET `/crm/v3/objects/users/`**: Retrieves all users in the account.
    * **GET `/crm/v3/objects/users/{userId}`**: Retrieves a specific user by their `userId`.  Example: `/crm/v3/objects/users/207838823235`
    * **POST `/crm/v3/objects/users/batch/read`**: Retrieves a batch of users by ID or another unique identifier property.
    * **POST `/crm/v3/objects/users/search`**: Retrieves users matching specific criteria (see [Searching the CRM](link_to_crm_search_docs)).

* **Update Users:**
    * **PATCH `/crm/v3/objects/users/{userId}`**: Updates an individual user by their `userId`.
    * **POST `/crm/v3/objects/users/batch/update`**: Updates a batch of users.


* **Properties:**
    * **GET `/crm/v3/properties/user`**: Retrieves a list of all available user properties.

**Note:** `id` and `hs_object_id` in the response represent a user *only* within the requesting HubSpot account.  This differs from IDs in the User Provisioning API (`hs_internal_user_id`) and Owners API (`hubspot_owner_id`).


## API Calls & Responses

### Retrieving Users

**1. Retrieving All Users:**

* **Method:** `GET`
* **URL:** `/crm/v3/objects/users/`
* **Example Response:**

```json
{
  "results": [
    {
      "id": "207838823235",
      "properties": {
        "hs_createdate": "2021-01-10T20:36:06.761Z",
        "hs_lastmodifieddate": "2023-08-29T18:17:55.697Z",
        "hs_object_id": "207838823235"
      },
      "createdAt": "2021-01-10T20:36:06.761Z",
      "updatedAt": "2023-08-29T18:17:55.697Z",
      "archived": false
    },
    // ... more users
  ]
}
```

**2. Retrieving Specific Properties:**

* **Method:** `GET`
* **URL:** `/crm/v3/objects/users/?properties=hs_job_title,hs_additional_phone`
* **Example Response:**

```json
{
  "results": [
    {
      "id": "207838823235",
      "properties": {
        "hs_additional_phone": "+1123456780",
        "hs_createdate": "2021-01-10T20:36:06.761Z",
        "hs_job_title": "CEO",
        "hs_lastmodifieddate": "2023-08-29T18:17:55.697Z",
        "hs_object_id": "207838823235"
      },
      // ...
    },
    // ... more users
  ]
}
```

**3. Batch Read (by ID):**

* **Method:** `POST`
* **URL:** `/crm/v3/objects/users/batch/read`
* **Request Body:**

```json
{
  "properties": ["hs_job_title", "hs_additional_phone"],
  "inputs": [
    {"id": "207838823235"},
    {"id": "207840253600"}
  ]
}
```

**4. Batch Read (by Unique Property):**

* **Method:** `POST`
* **URL:** `/crm/v3/objects/users/batch/read`
* **Request Body:**

```json
{
  "properties": ["hs_job_title", "hs_additional_phone"],
  "idProperty": "externalIdProperty",
  "inputs": [
    {"id": "0001111"},
    {"id": "0001112"}
  ]
}
```


### Updating Users

**1. Updating Individual User:**

* **Method:** `PATCH`
* **URL:** `/crm/v3/objects/users/{userId}`
* **Request Body:**

```json
{
  "properties": {
    "hs_standard_time_zone": "America/Detroit",
    "hs_working_hours": "[{\"days\":\"SATURDAY\",\"startMinute\":540,\"endMinute\":1020},{\"days\":\"WEDNESDAY\",\"startMinute\":540,\"endMinute\":1020}]"
  }
}
```

**2. Batch Update:**  Similar to batch read, but using the `/crm/v3/objects/users/batch/update` endpoint and a request body containing the users to update and their new properties.


## User Properties

The following properties are updatable via this API:

| Parameter                     | Type    | Description                                                                                             |
|---------------------------------|---------|---------------------------------------------------------------------------------------------------------|
| `hs_additional_phone`         | String  | User's additional phone number.                                                                         |
| `hs_availability_status`       | String  | User's availability status ("available" or "away").                                                    |
| `hs_job_title`                 | String  | User's job title.                                                                                       |
| `hs_main_user_language_skill` | String  | User's main language skill (must match an existing language skill).                                     |
| `hs_out_of_office_hours`      | String  | User's out-of-office hours (JSON array of date ranges).  See "Out of Office Hours" section below.       |
| `hs_secondary_user_language_skill` | String | User's secondary language skill (must match an existing language skill).                               |
| `hs_standard_time_zone`       | String  | User's timezone (standard TZ identifier, e.g., "America/New_York"). Must be set before `hs_working_hours`. |
| `hs_uncategorized_skills`     | String  | User's custom uncategorized skill (must match an existing custom skill).                               |
| `hs_working_hours`            | String  | User's working hours (JSON array of working hour objects). See "Working Hours" section below.          |


### Working Hours Format

`hs_working_hours` uses a JSON string array:

```json
"[{\"days\":\"VALUE\",\"startMinute\":number,\"endMinute\":number}]"
```

* **`days`**:  `MONDAY_TO_FRIDAY`, `SATURDAY_SUNDAY`, `EVERY_DAY`, `MONDAY`, `TUESDAY`, `WEDNESDAY`, `THURSDAY`, `FRIDAY`, `SATURDAY`, `SUNDAY`
* **`startMinute`**:  Start time in minutes (0-1440).
* **`endMinute`**: End time in minutes (0-1440).

**Example:** Monday-Friday 9 AM to 5 PM: `"[{\"days\":\"MONDAY_TO_FRIDAY\",\"startMinute\":540,\"endMinute\":1020}]"`


### Out of Office Hours Format

`hs_out_of_office_hours` uses a JSON string array of date ranges:

```json
"[{\"startTimestamp\":number,\"endTimestamp\":number}]"
```

* **`startTimestamp`**: Start time in milliseconds since epoch.
* **`endTimestamp`**: End time in milliseconds since epoch.


### Language Skills

Language skills must match the following values:

```json
[
  {"label": "Dansk", "value": "da"},
  {"label": "Deutsch", "value": "de"},
  // ... more languages
]
```


This markdown provides a comprehensive overview of the HubSpot Account Users API. Remember to replace placeholder URLs and IDs with your actual values.  Consult the official HubSpot API documentation for the most up-to-date information and details.
