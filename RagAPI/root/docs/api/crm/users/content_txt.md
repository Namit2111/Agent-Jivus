# HubSpot Account | Users API

This document details the HubSpot Users API, allowing you to retrieve and update information about users within your HubSpot account.  This is particularly useful for syncing HubSpot user data with external systems.

## API Endpoints

The Users API utilizes several endpoints:

* **Retrieve Users:**
    * **GET `/crm/v3/objects/users/`**: Retrieves all users.
    * **GET `/crm/v3/objects/users/{userId}`**: Retrieves a specific user by ID.  Example: `/crm/v3/objects/users/207838823235`
    * **POST `/crm/v3/objects/users/batch/read`**: Retrieves a batch of users by ID or another unique identifier property.
    * **POST `/crm/v3/objects/users/search`**: Retrieves users matching specific criteria (see [Searching the CRM](link-to-crm-search-docs)).

* **Update Users:**
    * **PATCH `/crm/v3/objects/users/{userId}`**: Updates an individual user.
    * **POST `/crm/v3/objects/users/batch/update`**: Updates a batch of users.


* **User Properties:**
    * **GET `/crm/v3/properties/user`**: Retrieves a list of all available user properties.


##  Retrieve Users - Examples

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
      // ... rest of the response
    }
    // ... other users
  ]
}
```

**3. Batch Read (using IDs):**

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

**4. Batch Read (using a unique property):**

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
PATCH /crm/v3/objects/users/{userId}
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

| Parameter                     | Type    | Description                                                                                                   |
|---------------------------------|---------|---------------------------------------------------------------------------------------------------------------|
| `hs_additional_phone`         | String  | User's additional phone number.                                                                                  |
| `hs_availability_status`      | String  | User's availability status ("available" or "away").                                                             |
| `hs_job_title`                | String  | User's job title.                                                                                             |
| `hs_main_user_language_skill` | String  | User's main language skill (must match an existing language skill).                                             |
| `hs_out_of_office_hours`      | String  | User's out-of-office hours (JSON array of date ranges).  See "Out of Office Hours" section below for format. |
| `hs_secondary_user_language_skill` | String  | User's secondary language skill (must match an existing language skill).                                          |
| `hs_standard_time_zone`       | String  | User's timezone (standard TZ identifier, e.g., "America/New_York").                                          |
| `hs_uncategorized_skills`     | String  | User's custom uncategorized skill.                                                                            |
| `hs_working_hours`            | String  | User's working hours (stringified JSON). See "Working Hours" section below for format.                         |


## Working Hours

The `hs_working_hours` property uses a stringified JSON array.

**Format:** `"[{\"days\":\"VALUE\",\"startMinute\":number,\"endMinute\":number}]"`

* **`days`**:  `MONDAY_TO_FRIDAY`, `SATURDAY_SUNDAY`, `EVERY_DAY`, `MONDAY`, `TUESDAY`, `WEDNESDAY`, `THURSDAY`, `FRIDAY`, `SATURDAY`, `SUNDAY`
* **`startMinute`**: Number (0-1440, representing minutes past midnight).
* **`endMinute`**: Number (0-1440).

**Example:** Monday-Friday, 9:00 AM to 5:00 PM: `"[{\"days\":\"MONDAY_TO_FRIDAY\",\"startMinute\":540,\"endMinute\":1020}]"`

## Out of Office Hours

The `hs_out_of_office_hours` property uses a stringified JSON array of date ranges.

**Format:** `"[{\"startTimestamp\":number,\"endTimestamp\":number}]"`

* **`startTimestamp`**: Unix timestamp (milliseconds).
* **`endTimestamp`**: Unix timestamp (milliseconds).

**Example:** Oct 31st 2024, 9:00 AM to 5:00 PM and Nov 28th 2024, 9:00 AM to 5:00 PM: `"[{\"startTimestamp\": 17303796000,\"endTimestamp\": 17304084000},{\"startTimestamp\": 17328024000,\"endTimestamp\": 17328312000}]"`


## Language Skills

Valid language skill values:

```json
[
  {"label": "Dansk", "value": "da"},
  {"label": "Deutsch", "value": "de"},
  {"label": "English", "value": "en"},
  // ... other languages
]
```

**Note:**  `hs_object_id` and `id` are the same within a single HubSpot account and represent only users within that account.  This differs from other HubSpot APIs' ID values.


This markdown documentation provides a comprehensive overview of the HubSpot Users API, including examples and details on data formats.  Remember to replace placeholder IDs and values with your actual data.  Consult the HubSpot developer documentation for the most up-to-date information and authentication details.
