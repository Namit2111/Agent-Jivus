# HubSpot Meetings API Documentation

This document details the HubSpot Meetings API, allowing you to manage meetings within the HubSpot CRM.  The API supports creating, retrieving, updating, associating, and deleting meeting engagements.

## API Endpoints

All endpoints are located under the `/crm/v3/objects/meetings` base path.  Remember to replace placeholders like `{meetingId}`, `{toObjectId}`, etc. with the actual IDs.

### 1. Create a Meeting (POST `/crm/v3/objects/meetings`)

Creates a new meeting engagement.

**Request Body:**

The request body is a JSON object with `properties` and optional `associations` fields.

* **`properties` (object):**  Contains meeting details.  Required fields are marked with `*`.

    | Field                  | Description                                                                                         | Type             | Required | Example                               |
    |-----------------------|-----------------------------------------------------------------------------------------------------|-----------------|----------|---------------------------------------|
    | `hs_timestamp`        | *Date and time the meeting occurred (Unix timestamp in milliseconds or UTC format). Defaults to `hs_meeting_start_time` if missing. | String/Number   | *        | `"2024-10-27T10:00:00Z"` or `1703632000000` |
    | `hs_meeting_title`    | Meeting title                                                                                      | String           |          | `"Project Kickoff"`                   |
    | `hubspot_owner_id`    | *ID of the meeting owner (HubSpot user ID).                                                      | String           | *        | `"1234567"`                         |
    | `hs_meeting_body`     | Meeting description                                                                                 | String           |          | `"Discuss project goals and timeline."` |
    | `hs_internal_meeting_notes` | Internal notes (not visible to attendees).                                                        | String           |          | `"Action items: ..."`                |
    | `hs_meeting_external_url` | External URL (e.g., Zoom link).                                                                  | String           |          | `"https://zoom.us/..."`             |
    | `hs_meeting_location` | Meeting location (physical address, conference room, etc.).                                         | String           |          | `"Conference Room A"`                |
    | `hs_meeting_start_time` | Date and time the meeting starts (UTC format).                                                    | String           |          | `"2024-10-27T10:00:00Z"`             |
    | `hs_meeting_end_time`   | Date and time the meeting ends (UTC format).                                                      | String           |          | `"2024-10-27T11:00:00Z"`             |
    | `hs_meeting_outcome`   | Meeting outcome (e.g., `SCHEDULED`, `COMPLETED`, `RESCHEDULED`, `NO SHOW`, `CANCELED`). | String           |          | `"COMPLETED"`                        |
    | `hs_activity_type`    | Type of meeting (based on your HubSpot account's meeting types).                                | String           |          | `"Sales Meeting"`                     |
    | `hs_attachment_ids`   | IDs of attached files (semicolon-separated).                                                    | String           |          | `"123;456"`                           |


* **`associations` (array of objects):**  Associates the meeting with existing records (e.g., contacts, companies).

    | Field       | Description                                                     | Type      | Required | Example                                  |
    |-------------|-----------------------------------------------------------------|-----------|----------|------------------------------------------|
    | `to`        | Object to associate with (ID and type).                         | Object    |          | `{"id": 101}`                          |
    | `types`     | Association type.                                               | Array     |          | `[{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 200}]` |


**Example Request:**

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27T10:00:00Z",
    "hubspot_owner_id": "1234567",
    "hs_meeting_title": "Project Kickoff",
    "hs_meeting_body": "Discuss project goals and timeline."
  },
  "associations": [
    {
      "to": {"id": 101},
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 200}]
    }
  ]
}
```

**Response:**  A JSON object representing the newly created meeting, including its ID.


### 2. Retrieve a Meeting (GET `/crm/v3/objects/meetings/{meetingId}`)

Retrieves a single meeting by its ID.

**Query Parameters:**

| Parameter    | Description                                          | Type     |
|--------------|------------------------------------------------------|----------|
| `properties` | Comma-separated list of properties to return.       | String   |
| `associations` | Comma-separated list of associated objects to retrieve. | String   |

**Example Request:**

`/crm/v3/objects/meetings/123?properties=hs_meeting_title,hs_meeting_start_time`

**Response:** A JSON object representing the meeting.


### 3. Retrieve Meetings (GET `/crm/v3/objects/meetings`)

Retrieves a list of meetings.

**Query Parameters:**

| Parameter    | Description                                    | Type     |
|--------------|------------------------------------------------|----------|
| `limit`      | Maximum number of results per page.            | Integer  |
| `properties` | Comma-separated list of properties to return.   | String   |


**Response:** A JSON object with a list of meetings and pagination information.


### 4. Update a Meeting (PATCH `/crm/v3/objects/meetings/{meetingId}`)

Updates an existing meeting.

**Request Body:**

A JSON object with the `properties` field containing the properties to update.  Omit properties you don't want to change.  An empty string (`""`) will clear a property value.

**Example Request:**

```json
{
  "properties": {
    "hs_meeting_title": "Updated Meeting Title"
  }
}
```

**Response:** A JSON object representing the updated meeting.


### 5. Associate a Meeting with Records (PUT `/crm/v3/objects/meetings/{meetingId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates an existing meeting with a record.

**Path Parameters:**

| Parameter       | Description                                         | Type     |
|-----------------|-----------------------------------------------------|----------|
| `meetingId`     | ID of the meeting.                                  | Integer  |
| `toObjectType`  | Type of object to associate (e.g., `contact`, `company`). | String   |
| `toObjectId`    | ID of the object to associate.                       | Integer  |
| `associationTypeId` | ID of the association type.                           | Integer  |

**Response:**  Success/failure indication.


### 6. Remove an Association (DELETE `/crm/v3/objects/meetings/{meetingId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Removes an association between a meeting and a record.  Uses the same path parameters as the association method.


### 7. Pin a Meeting (Update Record via Object APIs)

Pinning a meeting is done indirectly by including the meeting's `id` in the `hs_pinned_engagement_id` field when creating or updating a record (contact, company, deal, etc.) using their respective object APIs. Only one activity can be pinned per record.


### 8. Delete a Meeting (DELETE `/crm/v3/objects/meetings/{meetingId}`)

Deletes a meeting (moves it to the recycling bin).

**Response:** Success/failure indication.


## Error Handling

The API uses standard HTTP status codes to indicate success or failure. Error responses will contain details about the error.


This documentation provides a concise overview.  Refer to the HubSpot developer portal for the most up-to-date and complete information, including details on rate limits, authentication, and batch operations.  The "Endpoints" tab mentioned in the original text likely contains additional details not included here.
