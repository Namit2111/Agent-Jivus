# HubSpot Account | Users API

This document details the HubSpot Users API, allowing you to retrieve and update information about users within your HubSpot account.  This API is particularly useful for synchronizing HubSpot user data with external systems.

## API Endpoints

The Users API uses several endpoints for different operations:

* **Retrieve Users:**
    * **GET `/crm/v3/objects/users/`**: Retrieves all users.
    * **GET `/crm/v3/objects/users/{userId}`**: Retrieves a specific user by their `userId`.  Example: `/crm/v3/objects/users/207838823235`
    * **POST `/crm/v3/objects/users/batch/read`**: Retrieves a batch of users by ID or another unique identifier property.
    * **POST `/crm/v3/objects/users/search`**: Retrieves users based on specific criteria (see [Searching the CRM](link-to-crm-search-documentation)).


* **Update Users:**
    * **PATCH `/crm/v3/objects/users/{userId}`**: Updates an individual user by their `userId`.
    * **POST `/crm/v3/objects/users/batch/update`**: Updates a batch of users.


* **User Properties:**
    * **GET `/crm/v3/properties/user`**: Retrieves a list of all available user properties.


**Note:**  `id` and `hs_object_id` in API responses represent a user *only* within the HubSpot account from which the data was requested. This differs from `hs_internal_user_id` (user provisioning API) and `hubspot_owner_id` (owners API).


## Retrieve Users Examples

**1. Retrieving all users:**

```bash
GET /crm/v3/objects/users/
```

**Response (Example):**

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

**2. Retrieving a specific user:**

```bash
GET /crm/v3/objects/users/207838823235
```

**3. Retrieving users with specific properties:**

```bash
GET /crm/v3/objects/users?properties=hs_job_title,hs_additional_phone
```

**Response (Example):**

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

**4. Batch Read (by ID):**

```bash
POST /crm/v3/objects/users/batch/read
```

**Request Body (Example):**

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

**Request Body (Example):**

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


## Update Users Examples

**1. Updating an individual user:**

```bash
PATCH /crm/v3/objects/users/{userId}
```

**Request Body (Example):**

```json
{
  "properties": {
    "hs_standard_time_zone": "America/Detroit",
    "hs_working_hours": "[{\"days\":\"SATURDAY\",\"startMinute\":540,\"endMinute\":1020},{\"days\":\"WEDNESDAY\",\"startMinute\":540,\"endMinute\":1020}]"
  }
}
```

**2. Batch Update:**  Similar to batch read, but uses the `/crm/v3/objects/users/batch/update` endpoint and a corresponding request body.


## User Properties

| Parameter                     | Type    | Description                                                                                                       |
|---------------------------------|---------|-------------------------------------------------------------------------------------------------------------------|
| `hs_additional_phone`         | String  | User's additional phone number.                                                                                      |
| `hs_availability_status`      | String  | "available" or "away"                                                                                             |
| `hs_job_title`                | String  | User's job title.                                                                                                 |
| `hs_main_user_language_skill` | String  | User's main language skill (must match an existing language skill).                                                |
| `hs_out_of_office_hours`      | String  | JSON array of date ranges (see "Out of Office Hours" section).                                                   |
| `hs_secondary_user_language_skill` | String  | User's secondary language skill (must match an existing language skill).                                             |
| `hs_standard_time_zone`       | String  | User's timezone (must use standard TZ identifiers, e.g., "America/New_York"). Must be set before `hs_working_hours`. |
| `hs_uncategorized_skills`     | String  | User's custom uncategorized skill.                                                                                  |
| `hs_working_hours`            | String  | JSON array of working hour objects (see "Working Hours" section).                                                  |


## Working Hours Format

`hs_working_hours` uses a stringified JSON array:

```json
"[{\"days\":\"VALUE\",\"startMinute\":number,\"endMinute\":number}]"
```

* **`days`**:  `MONDAY_TO_FRIDAY`, `SATURDAY_SUNDAY`, `EVERY_DAY`, `MONDAY`, `TUESDAY`, `WEDNESDAY`, `THURSDAY`, `FRIDAY`, `SATURDAY`, `SUNDAY`
* **`startMinute`**:  Minutes since midnight (0-1440).
* **`endMinute`**: Minutes since midnight (0-1440).

**Example:** Monday to Friday, 9:00 AM to 5:00 PM

```json
"[{\"days\":\"MONDAY_TO_FRIDAY\",\"startMinute\":540,\"endMinute\":1020}]"
```


## Out of Office Hours Format

`hs_out_of_office_hours` uses a stringified JSON array of date ranges:

```json
"[{\"startTimestamp\": number, \"endTimestamp\": number}]"
```

* **`startTimestamp`**:  Unix timestamp (milliseconds).
* **`endTimestamp`**: Unix timestamp (milliseconds).

**Example:**

```json
"[{\"startTimestamp\": 17303796000,\"endTimestamp\": 17304084000},{\"startTimestamp\": 17328024000,\"endTimestamp\": 17328312000}]"
```


## Language Skills

Use the `value` field from the following list for `hs_main_user_language_skill` or `hs_secondary_user_language_skill`:

```json
[
  {"label": "Dansk", "value": "da"},
  {"label": "Deutsch", "value": "de"},
  {"label": "English", "value": "en"},
  // ... more languages
]
```


This documentation provides a comprehensive overview of the HubSpot Users API.  Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
