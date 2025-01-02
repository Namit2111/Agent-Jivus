# HubSpot Meetings API Documentation

This document details the HubSpot Meetings API, allowing you to manage meeting engagements within the HubSpot CRM.  You can create, retrieve, update, associate, and delete meetings via various HTTP requests.

## API Endpoint Base URL:

`/crm/v3/objects/meetings`


## 1. Create a Meeting (POST)

**Endpoint:** `/crm/v3/objects/meetings`

**Method:** `POST`

**Request Body:**  JSON payload containing `properties` and optionally `associations`.

**Properties Object:**

| Field                   | Description                                                                                                      | Required | Data Type    | Example                               |
|------------------------|------------------------------------------------------------------------------------------------------------------|----------|---------------|---------------------------------------|
| `hs_timestamp`          | Date and time the meeting occurred (Unix timestamp in milliseconds or UTC format). Defaults to `hs_meeting_start_time` if missing. | Yes      | String/Number | `1677000000000` or `"2023-02-20T10:00:00Z"` |
| `hs_meeting_title`     | Meeting title                                                                                                   | No       | String        | `"Project Kickoff"`                    |
| `hubspot_owner_id`      | HubSpot ID of the meeting owner.                                                                                 | No       | String        | `"1234567"`                           |
| `hs_meeting_body`       | Meeting description                                                                                                | No       | String        | `"Discuss project goals and timeline."` |
| `hs_internal_meeting_notes` | Internal notes for your team.                                                                                     | No       | String        | `"Action items discussed..."`          |
| `hs_meeting_external_url` | External URL (e.g., Zoom link).                                                                                  | No       | String        | `"https://zoom.us/..."`              |
| `hs_meeting_location`   | Meeting location.                                                                                               | No       | String        | `"Conference Room A"`                 |
| `hs_meeting_start_time` | Meeting start time (UTC format).                                                                                  | No       | String        | `"2023-02-20T10:00:00Z"`             |
| `hs_meeting_end_time`   | Meeting end time (UTC format).                                                                                    | No       | String        | `"2023-02-20T11:00:00Z"`             |
| `hs_meeting_outcome`    | Meeting outcome (e.g., `SCHEDULED`, `COMPLETED`, `RESCHEDULED`, `NO_SHOW`, `CANCELED`).                           | No       | String        | `"COMPLETED"`                         |
| `hs_activity_type`      | Meeting type (based on your HubSpot account settings).                                                          | No       | String        | `"Sales Meeting"`                     |
| `hs_attachment_ids`     | IDs of attached files (semicolon-separated).                                                                    | No       | String        | `"123;456"`                           |


**Associations Object:** (Optional)  Associates the meeting with existing records.

| Field       | Description                                                              | Example                                     |
|-------------|--------------------------------------------------------------------------|---------------------------------------------|
| `to.id`     | ID of the record to associate (e.g., Contact ID).                     | `101`                                       |
| `types`     | Association type.                                                      | `[{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 200 }]` |


**Example Request:**

```json
{
  "properties": {
    "hs_timestamp": "2024-03-08T14:00:00Z",
    "hs_meeting_title": "Client Meeting",
    "hubspot_owner_id": "1234567"
  },
  "associations": [
    {
      "to": { "id": 101 },
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 200 }]
    }
  ]
}
```

**Response:**  JSON object representing the created meeting, including its ID.


## 2. Retrieve Meetings (GET)

**Endpoint:** `/crm/v3/objects/meetings/{meetingId}` (individual) or `/crm/v3/objects/meetings` (list)

**Method:** `GET`

**Parameters (for list):**

| Parameter | Description                                      |
|-----------|--------------------------------------------------|
| `limit`   | Maximum number of results per page.              |
| `properties` | Comma-separated list of properties to return.   |
| `associations` | Comma-separated list of associated objects to retrieve. |


**Parameters (for individual):**

| Parameter | Description                                      |
|-----------|--------------------------------------------------|
| `properties` | Comma-separated list of properties to return.   |
| `associations` | Comma-separated list of associated objects to retrieve. |


**Response:** JSON object (individual) or array of JSON objects (list) representing the meeting(s).


## 3. Update a Meeting (PATCH)

**Endpoint:** `/crm/v3/objects/meetings/{meetingId}`

**Method:** `PATCH`

**Request Body:** JSON payload containing `properties` to update.  Omit properties to leave them unchanged or send an empty string to clear a property.

**Example Request:**

```json
{
  "properties": {
    "hs_meeting_outcome": "COMPLETED"
  }
}
```

**Response:** JSON object representing the updated meeting.


## 4. Associate Existing Meetings with Records (PUT)

**Endpoint:** `/crm/v3/objects/meetings/{meetingId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `PUT`

**Parameters:**

| Parameter       | Description                                           |
|-----------------|-------------------------------------------------------|
| `meetingId`      | ID of the meeting.                                    |
| `toObjectType`  | Object type to associate (e.g., `contact`, `company`). |
| `toObjectId`    | ID of the record to associate.                         |
| `associationTypeId` | ID of the association type.                           |


**Response:** Success or error message.


## 5. Remove an Association (DELETE)

**Endpoint:** `/crm/v3/objects/meetings/{meetingId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `DELETE`

**Parameters:**  Same as Associate Existing Meetings.

**Response:** Success or error message.


## 6. Pin a Meeting on a Record

Pinning is done by including the meeting's `id` in the `hs_pinned_engagement_id` field when creating or updating a record via other HubSpot object APIs (contacts, companies, deals, etc.).


## 7. Delete a Meeting (DELETE)

**Endpoint:** `/crm/v3/objects/meetings/{meetingId}`

**Method:** `DELETE`

**Response:** Success or error message.


**Note:**  Error handling and authentication details (API key, etc.) are not explicitly covered in the provided text and would need to be included in a complete documentation.  This markdown provides a structured overview based on the given text.  The "Endpoints" tab mentioned in the original text likely contains further details on batch operations, error codes, and rate limits.
