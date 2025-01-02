# HubSpot Account | Users API

This document details the HubSpot Users API, allowing you to retrieve and update user information within your HubSpot account.  This is particularly useful for syncing HubSpot user data with external systems.

## API Endpoints

The Users API uses the following endpoints:

* **Retrieve Users:**
    * **GET `/crm/v3/objects/users/`:** Retrieves all users.
    * **GET `/crm/v3/objects/users/{userId}`:** Retrieves a specific user by ID.  Example: `/crm/v3/objects/users/207838823235`
    * **POST `/crm/v3/objects/users/batch/read`:** Retrieves a batch of users by ID or another unique identifier property.
    * **POST `/crm/v3/objects/users/search`:** Retrieves users matching specific criteria (see [Searching the CRM](link-to-crm-search-docs)).


* **Update Users:**
    * **PATCH `/crm/v3/objects/users/{userId}`:** Updates a specific user by ID.
    * **POST `/crm/v3/objects/users/batch/update`:** Updates a batch of users.


* **User Properties:**
    * **GET `/crm/v3/properties/user`:** Retrieves a list of all available user properties.


##  Retrieve Users - Examples

**1. Retrieving all users:**

```bash
GET /crm/v3/objects/users/
```

**Response (example):**

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

**2. Retrieving specific properties:**

```bash
GET /crm/v3/objects/users?properties=hs_job_title,hs_additional_phone
```

**Response (example):**

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

**3. Batch read with internal ID:**

```bash
POST /crm/v3/objects/users/batch/read
```

**Request Body:**

```json
{
  "properties": ["hs_job_title", "hs_additional_phone"],
  "inputs": [
    {"id": "207838823235"},
    {"id": "207840253600"}
  ]
}
```


**4. Batch read with unique property ID:**

```bash
POST /crm/v3/objects/users/batch/read
```

**Request Body:**

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

## Update Users - Example

```bash
PATCH /crm/v3/objects/users/207838823235
```

**Request Body:**

```json
{
  "properties": {
    "hs_standard_time_zone": "America/Detroit",
    "hs_working_hours": "[{\"days\":\"SATURDAY\",\"startMinute\":540,\"endMinute\":1020},{\"days\":\"WEDNESDAY\",\"startMinute\":540,\"endMinute\":1020}]"
  }
}
```

## User Properties

| Parameter                     | Type    | Description                                                                                                                                   |
|---------------------------------|---------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| `hs_additional_phone`          | String  | User's additional phone number.                                                                                                                  |
| `hs_availability_status`       | String  | User's availability status ("available" or "away").                                                                                             |
| `hs_job_title`                 | String  | User's job title.                                                                                                                            |
| `hs_main_user_language_skill` | String  | User's main language skill (must match an existing language skill).                                                                             |
| `hs_out_of_office_hours`      | String  | User's out-of-office hours (JSON array of date ranges: `[{"startTimestamp": 1678886400000,"endTimestamp": 1679059200000}]`).                    |
| `hs_secondary_user_language_skill` | String  | User's secondary language skill (must match an existing language skill).                                                                            |
| `hs_standard_time_zone`       | String  | User's timezone (standard TZ identifier, e.g., "America/New_York").  Must be set before setting `hs_working_hours`.                         |
| `hs_uncategorized_skills`     | String  | User's custom uncategorized skill (must match an existing skill).                                                                                 |
| `hs_working_hours`            | String  | User's working hours (stringified JSON array of objects). See "Working Hours" section below.                                                    |


## Working Hours

The `hs_working_hours` property uses a stringified JSON array.

**Format:** `"[{\"days\":\"VALUE\",\"startMinute\":number,\"endMinute\":number}]"`

| Parameter     | Type           | Description                                                                        |
|---------------|-----------------|------------------------------------------------------------------------------------|
| `days`        | Stringified JSON | Days (MONDAY_TO_FRIDAY, SATURDAY_SUNDAY, EVERY_DAY, MONDAY, TUESDAY, etc.)          |
| `startMinute` | Number          | Start time in minutes (0-1440, 0 = 12:00 AM).                                      |
| `endMinute`   | Number          | End time in minutes (0-1440).                                                        |

**Example:** Monday to Friday, 9:00 AM to 5:00 PM: `"[{\"days\":\"MONDAY_TO_FRIDAY\",\"startMinute\":540,\"endMinute\":1020}]"`


## Out of Office Hours

The `hs_out_of_office_hours` property accepts a JSON array of date ranges.

**Format:** `"[{\"startTimestamp\":timestamp,\"endTimestamp\":timestamp}]"`

* `startTimestamp`: Start time in milliseconds since epoch.
* `endTimestamp`: End time in milliseconds since epoch.

**Example:** October 31st 2024 9:00 AM to 5:00 PM and November 28th 2024 9:00 AM to 5:00 PM:  `"[{\"startTimestamp\": 1730379600000,\"endTimestamp\": 1730408400000},{\"startTimestamp\": 1732802400000,\"endTimestamp\": 1732831200000}]"`


## Language Skills

`hs_main_user_language_skill` and `hs_secondary_user_language_skill` must match a value from this list:


```json
[
  {"label": "Dansk", "value": "da"},
  {"label": "Deutsch", "value": "de"},
  {"label": "English", "value": "en"},
  // ... more languages
]
```

## Important Notes

* `id` and `hs_object_id` are the same in the Users API response and represent a user *only* within the HubSpot account from which the data was requested.
*  `hs_standard_time_zone` must be set before setting `hs_working_hours`.
* Working hours and out-of-office hours cannot overlap.


This markdown provides a comprehensive overview of the HubSpot Users API.  Remember to replace placeholder IDs and values with your actual data.  Consult the official HubSpot API documentation for the most up-to-date information and details.
