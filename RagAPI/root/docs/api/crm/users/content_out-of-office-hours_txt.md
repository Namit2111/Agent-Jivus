# HubSpot Account | Users API

This document details the HubSpot Users API, allowing you to retrieve and update user information within your HubSpot account.  This is particularly useful for synchronizing HubSpot user data with external systems.

## API Endpoints

The Users API uses the following endpoints:

* **Retrieve Users:**
    * **GET `/crm/v3/objects/users/`**: Retrieves all users.
    * **GET `/crm/v3/objects/users/{userId}`**: Retrieves a specific user by ID.  Replace `{userId}` with the user's HubSpot ID.
    * **POST `/crm/v3/objects/users/batch/read`**: Retrieves a batch of users by ID or another unique identifier property.
    * **POST `/crm/v3/objects/users/search`**: Retrieves users matching specific criteria (see [Searching the CRM](link_to_crm_search_docs)).

* **Update Users:**
    * **PATCH `/crm/v3/objects/users/{userId}`**: Updates a specific user by ID.
    * **POST `/crm/v3/objects/users/batch/update`**: Updates a batch of users.


##  Retrieve Users Examples

**1. Retrieving All Users:**

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

**2. Retrieving a Specific User:**

```bash
GET /crm/v3/objects/users/207838823235
```

**3. Retrieving Users with Specific Properties:**

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

**5. Batch Read (by unique identifier property):**

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


## Update Users Example

**Updating a User:**

```bash
PATCH /crm/v3/objects/users/207838823235
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


## User Properties

| Parameter                     | Type    | Description                                                                                                  |
|---------------------------------|---------|--------------------------------------------------------------------------------------------------------------|
| `hs_additional_phone`         | String  | User's additional phone number.                                                                              |
| `hs_availability_status`      | String  | "available" or "away".                                                                                       |
| `hs_job_title`                | String  | User's job title.                                                                                            |
| `hs_main_user_language_skill` | String  | User's main language skill (must match existing skill).                                                    |
| `hs_out_of_office_hours`      | String  | Array of date ranges (startTimestamp, endTimestamp),  must not overlap.                                   |
| `hs_secondary_user_language_skill` | String  | User's secondary language skill (must match existing skill).                                                 |
| `hs_standard_time_zone`       | String  | User's timezone (standard TZ identifier, e.g., "America/New_York"). Must be set before `hs_working_hours`. |
| `hs_uncategorized_skills`     | String  | User's custom uncategorized skill.                                                                         |
| `hs_working_hours`            | String  | Stringified JSON array of working hour objects (see below).                                                |


## Working Hours Format

`hs_working_hours` is a stringified JSON array. Each object represents a set of working hours:

```json
"[{\"days\":\"VALUE\",\"startMinute\":number,\"endMinute\":number}]"
```

* **`days`**:  `MONDAY_TO_FRIDAY`, `SATURDAY_SUNDAY`, `EVERY_DAY`, `MONDAY`, `TUESDAY`, `WEDNESDAY`, `THURSDAY`, `FRIDAY`, `SATURDAY`, `SUNDAY`
* **`startMinute`**: Start time in minutes (0-1440, 0 = 12:00 AM).
* **`endMinute`**: End time in minutes (0-1440).

**Example:** Monday-Friday, 9 AM to 5 PM:

```json
"[{\"days\":\"MONDAY_TO_FRIDAY\",\"startMinute\":540,\"endMinute\":1020}]"
```

**Example:** Monday 9 AM - 5 PM and Saturday 11 AM - 2 PM:

```json
"[{\"days\":\"MONDAY\",\"startMinute\":540,\"endMinute\":1020},{\"days\":\"SATURDAY\",\"startMinute\":660,\"endMinute\":840}]"
```

## Out of Office Hours Format

`hs_out_of_office_hours` is a stringified JSON array of date ranges:

```json
"[{\"startTimestamp\": timestamp,\"endTimestamp\": timestamp}]"
```

* **`startTimestamp`**: Start time in milliseconds since epoch.
* **`endTimestamp`**: End time in milliseconds since epoch.

**Example:**

```json
"[{\"startTimestamp\": 1730379600000,\"endTimestamp\": 1730408400000},{\"startTimestamp\": 1732802400000,\"endTimestamp\": 1732831200000}]"
```


## Language Skills Format

Use the `value` from the following list for `hs_main_user_language_skill` or `hs_secondary_user_language_skill`:

```json
[
  {"label": "Dansk", "value": "da"},
  {"label": "Deutsch", "value": "de"},
  {"label": "English", "value": "en"},
  // ... more languages
]
```

## Important Notes

* `id` and `hs_object_id` are the same and represent a user *only* within the requesting HubSpot account. This differs from IDs in other HubSpot APIs.
* Working hours cannot overlap.
* `hs_standard_time_zone` must be set before `hs_working_hours`.
* Out-of-office date ranges cannot overlap.


This markdown provides a comprehensive overview of the HubSpot Users API. Remember to replace placeholder IDs and values with your actual data.  Always refer to the official HubSpot API documentation for the most up-to-date information and details.
