# HubSpot Account | Users API

This document details the HubSpot Users API, allowing you to retrieve and update information about users within your HubSpot account.  This API is particularly useful for synchronizing HubSpot user data with external systems like workforce management tools.

## API Endpoints

The Users API uses the following endpoints:

* **Retrieve Users:**
    * **GET `/crm/v3/objects/users/`**: Retrieves all users.
    * **GET `/crm/v3/objects/users/{userId}`**: Retrieves a specific user by their `userId`.  Example: `/crm/v3/objects/users/207838823235`
    * **POST `/crm/v3/objects/users/batch/read`**: Retrieves a batch of users by ID or by a unique identifier property.
    * **POST `/crm/v3/objects/users/search`**: Retrieves users matching specific criteria (see [Searching the CRM](link-to-crm-search-documentation-if-available)).

* **Update Users:**
    * **PATCH `/crm/v3/objects/users/{userId}`**: Updates a specific user by their `userId`.
    * **POST `/crm/v3/objects/users/batch/update`**: Updates a batch of users.


* **Get User Properties:**
    * **GET `/crm/v3/properties/user`**: Retrieves a list of all available user properties.


**Note:**  `id` and `hs_object_id` in the response represent a user *only* within the HubSpot account from which the data was requested. This differs from `hs_internal_user_id` (User Provisioning API) and `hubspot_owner_id` (Owners API).


## API Calls and Responses

### Retrieving Users

**1. Retrieving All Users:**

```bash
GET /crm/v3/objects/users/
```

**Example Response:**

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

Add the `properties` query parameter to specify desired properties:

```bash
GET /crm/v3/objects/users/?properties=hs_job_title,hs_additional_phone
```

**Example Response:**

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
    // ...more users
  ]
}
```


**3. Batch Read (by ID):**

```bash
POST /crm/v3/objects/users/batch/read
```

**Example Request Body:**

```json
{
  "properties": ["hs_job_title", "hs_additional_phone"],
  "inputs": [
    {"id": "207838823235"},
    {"id": "207840253600"}
  ]
}
```

**4. Batch Read (by unique property):**

```bash
POST /crm/v3/objects/users/batch/read
```

**Example Request Body:**

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

```bash
PATCH /crm/v3/objects/users/{userId}
```

**Example Request Body:**

```json
{
  "properties": {
    "hs_standard_time_zone": "America/Detroit",
    "hs_working_hours": "[{\"days\":\"SATURDAY\",\"startMinute\":540,\"endMinute\":1020},{\"days\":\"WEDNESDAY\",\"startMinute\":540,\"endMinute\":1020}]"
  }
}
```

**2. Batch Update:**  Similar to batch read, but uses the `/batch/update` endpoint.


## User Properties

The following properties can be set via the API (some are read-only):

| Parameter                     | Type    | Description                                                                                                       |
|---------------------------------|---------|-------------------------------------------------------------------------------------------------------------------|
| `hs_additional_phone`         | String  | User's additional phone number.                                                                                   |
| `hs_availability_status`      | String  | "available" or "away".                                                                                          |
| `hs_job_title`                | String  | User's job title.                                                                                             |
| `hs_main_user_language_skill` | String  | User's main language skill (must match an existing language skill).                                              |
| `hs_out_of_office_hours`      | String  | Array of date ranges (JSON).  See "Out of Office Hours" section below.                                         |
| `hs_secondary_user_language_skill` | String  | User's secondary language skill (must match an existing language skill).                                           |
| `hs_standard_time_zone`       | String  | User's timezone (TZ identifier, e.g., "America/New_York"). Must be set before `hs_working_hours`.             |
| `hs_uncategorized_skills`     | String | User's custom uncategorized skill.  Must match an existing custom skill in the portal.                        |
| `hs_working_hours`            | String  | User's working hours (JSON). See "Working Hours" section below.                                               |


### Working Hours (`hs_working_hours`)

This property accepts a JSON string representing an array of working hour objects:

```json
"[{\"days\":\"VALUE\",\"startMinute\":number,\"endMinute\":number}]"
```

* **`days`**:  `MONDAY_TO_FRIDAY`, `SATURDAY_SUNDAY`, `EVERY_DAY`, `MONDAY`, `TUESDAY`, `WEDNESDAY`, `THURSDAY`, `FRIDAY`, `SATURDAY`, `SUNDAY`
* **`startMinute`**:  Start time in minutes (0-1440, 0 = 12:00 AM).
* **`endMinute`**: End time in minutes (0-1440).

**Example:** Monday-Friday, 9 AM to 5 PM:

```json
"[{\"days\":\"MONDAY_TO_FRIDAY\",\"startMinute\":540,\"endMinute\":1020}]"
```

### Out of Office Hours (`hs_out_of_office_hours`)

This property accepts a JSON string representing an array of date range objects:

```json
"[{\"startTimestamp\":timestamp,\"endTimestamp\":timestamp}]"
```

* **`startTimestamp`**: Start time in milliseconds since the epoch.
* **`endTimestamp`**: End time in milliseconds since the epoch.

**Example:**

```json
"[{\"startTimestamp\": 17303796000,\"endTimestamp\": 17304084000},{\"startTimestamp\": 17328024000,\"endTimestamp\": 17328312000}]"
```


### Language Skills

`hs_main_user_language_skill` and `hs_secondary_user_language_skill` values must match the `value` field from this list:


```json
[
  {"label": "Dansk", "value": "da"},
  {"label": "Deutsch", "value": "de"},
  {"label": "English", "value": "en"},
  // ... more languages
]
```

This is a comprehensive documentation. Remember to replace placeholder links like `[Searching the CRM]` and `[Understanding the CRM]` with actual links if available.  Also, adjust the code snippets to conform to a standard markdown code block style if needed.
