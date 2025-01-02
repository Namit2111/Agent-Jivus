# HubSpot Account | Users API

This document details the HubSpot Users API, allowing you to retrieve and update information about users within your HubSpot account.  This is particularly useful for synchronizing HubSpot user data with external systems.

## API Endpoints

The Users API utilizes several endpoints:

* **Retrieve Users:**
    * **GET `/crm/v3/objects/users/`:** Retrieves all users.
    * **GET `/crm/v3/objects/users/{userId}`:** Retrieves a specific user by their `userId`.  Example: `/crm/v3/objects/users/207838823235`
    * **POST `/crm/v3/objects/users/batch/read`:** Retrieves a batch of users by ID or another unique identifier property.
    * **POST `/crm/v3/objects/users/search`:** Retrieves users matching specific criteria (see [Searching the CRM](link-to-crm-search-documentation)).


* **Update Users:**
    * **PATCH `/crm/v3/objects/users/{userId}`:** Updates an individual user.
    * **POST `/crm/v3/objects/users/batch/update`:** Updates a batch of users.


* **User Properties:**
    * **GET `/crm/v3/properties/user`:** Retrieves a list of all available user properties.


**Important Note:**  `id` and `hs_object_id` in API responses uniquely identify a user *only* within the HubSpot account from which the data was requested. This differs from `hs_internal_user_id` (User Provisioning API) and `hubspot_owner_id` (Owners API).


## API Calls and Responses

### Retrieving Users

**1. Retrieving All Users:**

* **Request:**
    ```bash
    GET /crm/v3/objects/users/
    ```
* **Response (Example):**

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
    {
      "id": "207840253600",
      "properties": {
        "hs_createdate": "2017-12-22T12:22:12.212Z",
        "hs_lastmodifieddate": "2023-08-29T18:17:55.697Z",
        "hs_object_id": "207840253600"
      },
      "createdAt": "2017-12-22T12:22:12.212Z",
      "updatedAt": "2023-08-29T18:17:55.697Z",
      "archived": false
    }
  ]
}
```

**2. Retrieving Specific Properties:**

* **Request:**
    ```bash
    GET /crm/v3/objects/users/?properties=hs_job_title,hs_additional_phone
    ```
* **Response (Example):**

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
      "createdAt": "2021-01-10T20:36:06.761Z",
      "updatedAt": "2023-08-29T18:17:55.697Z",
      "archived": false
    }
    // ... more users
  ]
}
```

**3. Batch Read (by ID):**

* **Request (POST `/crm/v3/objects/users/batch/read`):**
```json
{
  "properties": ["hs_job_title", "hs_additional_phone"],
  "inputs": [
    { "id": "207838823235" },
    { "id": "207840253600" }
  ]
}
```

**4. Batch Read (by unique property):**

* **Request (POST `/crm/v3/objects/users/batch/read`):**
```json
{
  "properties": ["hs_job_title", "hs_additional_phone"],
  "idProperty": "externalIdProperty",
  "inputs": [
    { "id": "0001111" },
    { "id": "0001112" }
  ]
}
```


### Updating Users

**1. Updating Individual User:**

* **Request (PATCH `/crm/v3/objects/users/{userId}`):**
```json
{
  "properties": {
    "hs_standard_time_zone": "America/Detroit",
    "hs_working_hours": "[{\"days\":\"SATURDAY\",\"startMinute\":540,\"endMinute\":1020},{\"days\":\"WEDNESDAY\",\"startMinute\":540,\"endMinute\":1020}]"
  }
}
```

**2. Batch Update:** Similar to batch read, but using the `POST /crm/v3/objects/users/batch/update` endpoint with a request body specifying the users to update and their new properties.


## User Properties

The following properties are updatable via this API:

| Parameter                     | Type    | Description                                                                                                          |
|---------------------------------|---------|----------------------------------------------------------------------------------------------------------------------|
| `hs_additional_phone`         | String  | User's additional phone number.                                                                                        |
| `hs_availability_status`      | String  | "available" or "away".                                                                                             |
| `hs_job_title`                | String  | User's job title.                                                                                                   |
| `hs_main_user_language_skill` | String  | User's main language skill (must match existing skill).                                                             |
| `hs_out_of_office_hours`      | String  | JSON array of date ranges (see below).                                                                                |
| `hs_secondary_user_language_skill` | String  | User's secondary language skill (must match existing skill).                                                           |
| `hs_standard_time_zone`       | String  | User's timezone (TZ identifier, e.g., "America/New_York"). Must be set before `hs_working_hours`.                     |
| `hs_uncategorized_skills`     | String  | User's custom uncategorized skill (must match an existing custom skill).                                            |
| `hs_working_hours`            | String  | JSON string representing working hours (see below).                                                                  |


### Working Hours Format

`hs_working_hours` uses a JSON string: `"[{\"days\":\"VALUE\",\"startMinute\":number,\"endMinute\":number}]"`

* **`days`:**  `MONDAY_TO_FRIDAY`, `SATURDAY_SUNDAY`, `EVERY_DAY`, or individual days (MONDAY, TUESDAY, etc.).
* **`startMinute`:** Start time in minutes (0-1440).
* **`endMinute`:** End time in minutes (0-1440).

**Example:** Monday-Friday, 9 AM to 5 PM: `"[{\"days\":\"MONDAY_TO_FRIDAY\",\"startMinute\":540,\"endMinute\":1020}]"`


### Out of Office Hours Format

`hs_out_of_office_hours` is a JSON array of date ranges: `"[{\"startTimestamp\": timestamp, \"endTimestamp\": timestamp}]"`

* **`startTimestamp`:** Start time in milliseconds since epoch.
* **`endTimestamp`:** End time in milliseconds since epoch.

**Example:**  October 31st 2024, 9 AM to 5 PM; November 28th 2024, 9 AM to 5 PM:
`"[{\"startTimestamp\": 17303796000,\"endTimestamp\": 17304084000},{\"startTimestamp\": 17328024000,\"endTimestamp\": 17328312000}]"`


### Language Skills

`hs_main_user_language_skill` and `hs_secondary_user_language_skill` must be one of the following `value`s:

```json
[
  {"label": "Dansk", "value": "da"},
  {"label": "Deutsch", "value": "de"},
  {"label": "English", "value": "en"},
  // ... other languages
]
```

This provides a comprehensive overview of the HubSpot Users API.  Remember to consult the official HubSpot documentation for the most up-to-date information and details on authentication and error handling.
