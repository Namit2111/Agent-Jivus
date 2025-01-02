# HubSpot Account | Users API

This document details the HubSpot Users API, allowing you to retrieve and update information about users within your HubSpot account.  This is particularly useful for syncing HubSpot user data with external systems.

## API Endpoints

The Users API uses the following endpoints:

* **Retrieve Users:**
    * **GET `/crm/v3/objects/users/`**: Retrieves all users.
    * **GET `/crm/v3/objects/users/{userId}`**: Retrieves a specific user by ID.  Example: `/crm/v3/objects/users/207838823235`
    * **POST `/crm/v3/objects/users/batch/read`**: Retrieves a batch of users by ID or a unique identifier property.
    * **POST `/crm/v3/objects/users/search`**: Retrieves users matching specific criteria (see [Searching the CRM](link_to_crm_search_documentation)).

* **Update Users:**
    * **PATCH `/crm/v3/objects/users/{userId}`**: Updates a specific user by ID.
    * **POST `/crm/v3/objects/users/batch/update`**: Updates a batch of users.


## Retrieve Users Examples

**Example 1: Retrieving all users**

```bash
GET /crm/v3/objects/users/
```

**Example 2: Retrieving a specific user (ID 207838823235)**

```bash
GET /crm/v3/objects/users/207838823235
```

**Example 3: Retrieving users with specific properties**

```bash
GET /crm/v3/objects/users?properties=hs_job_title,hs_additional_phone
```

**Example Response (for Examples 1 & 3):**

```json
{
  "results": [
    {
      "id": "207838823235",
      "properties": {
        "hs_createdate": "2021-01-10T20:36:06.761Z",
        "hs_lastmodifieddate": "2023-08-29T18:17:55.697Z",
        "hs_object_id": "207838823235",
        "hs_job_title": "CEO",
        "hs_additional_phone": "+1123456780" 
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
        "hs_object_id": "207840253600",
        "hs_job_title": "Vice President",
        "hs_additional_phone": "+1238675309"
      },
      "createdAt": "2017-12-22T12:22:12.212Z",
      "updatedAt": "2023-08-29T18:17:55.697Z",
      "archived": false
    }
  ]
}
```

**Example 4: Batch Read by ID**

```json
POST /crm/v3/objects/users/batch/read

{
  "properties": ["hs_job_title", "hs_additional_phone"],
  "inputs": [
    {"id": "207838823235"},
    {"id": "207840253600"}
  ]
}
```

**Example 5: Batch Read by Unique Property**

```json
POST /crm/v3/objects/users/batch/read

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

```bash
PATCH /crm/v3/objects/users/207838823235

{
  "properties": {
    "hs_standard_time_zone": "America/Detroit",
    "hs_working_hours": "[{\"days\":\"SATURDAY\",\"startMinute\":540,\"endMinute\":1020},{\"days\":\"WEDNESDAY\",\"startMinute\":540,\"endMinute\":1020}]"
  }
}
```

## User Properties

| Parameter                     | Type    | Description                                                                                                                                |
|---------------------------------|---------|---------------------------------------------------------------------------------------------------------------------------------------------|
| `hs_additional_phone`         | String  | User's additional phone number.                                                                                                                 |
| `hs_availability_status`      | String  | User's availability status ("available" or "away").                                                                                           |
| `hs_job_title`                | String  | User's job title.                                                                                                                            |
| `hs_main_user_language_skill` | String  | User's main language skill (must match an existing language skill). See "Language Skills" section.                                          |
| `hs_out_of_office_hours`      | String  | User's out-of-office hours (JSON array of date ranges). See "Out of Office Hours" section.                                                   |
| `hs_secondary_user_language_skill` | String  | User's secondary language skill (must match an existing language skill). See "Language Skills" section.                                     |
| `hs_standard_time_zone`       | String  | User's timezone (standard TZ identifier, e.g., "America/New_York"). Must be set before `hs_working_hours`.                                |
| `hs_uncategorized_skills`     | String  | User's custom uncategorized skill (must match an existing custom uncategorized skill).                                                       |
| `hs_working_hours`            | String  | User's working hours (stringified JSON array of objects). See "Working Hours" section.                                                     |


## Working Hours

The `hs_working_hours` property uses a stringified JSON array: `"[{\"days\":\"VALUE\",\"startMinute\":number,\"endMinute\":number}]"`

* **days**:  `MONDAY_TO_FRIDAY`, `SATURDAY_SUNDAY`, `EVERY_DAY`, `MONDAY`, `TUESDAY`, `WEDNESDAY`, `THURSDAY`, `FRIDAY`, `SATURDAY`, `SUNDAY`
* **startMinute**:  Start time in minutes (0-1440, 0 = 12:00 AM).
* **endMinute**: End time in minutes (0-1440).

**Example:** Monday-Friday, 9:00 AM to 5:00 PM: `"[{\"days\":\"MONDAY_TO_FRIDAY\",\"startMinute\":540,\"endMinute\":1020}]"`


## Out of Office Hours

The `hs_out_of_office_hours` property accepts a stringified JSON array of date ranges: `"[{\"startTimestamp\":number,\"endTimestamp\":number}]"`

* **startTimestamp**: Start timestamp in milliseconds since epoch.
* **endTimestamp**: End timestamp in milliseconds since epoch.

**Example:** October 31st 2024, 9:00 AM to 5:00 PM and November 28th 2024, 9:00 AM to 5:00 PM: `"[{\"startTimestamp\": 17303796000,\"endTimestamp\": 17304084000},{\"startTimestamp\": 17328024000,\"endTimestamp\": 17328312000}]"`


## Language Skills

Valid language skill values are provided in a JSON array.  Example:

```json
[
  {"label": "English", "value": "en"},
  {"label": "Español", "value": "es"},
  // ... other languages
]
```

Remember to replace `link_to_crm_search_documentation` with the actual link to HubSpot's CRM search documentation.  This markdown provides a comprehensive and well-structured overview of the HubSpot Users API.
