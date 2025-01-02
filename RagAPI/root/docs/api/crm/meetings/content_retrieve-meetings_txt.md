# HubSpot Meetings API Documentation

This document details the HubSpot Meetings API, allowing you to manage meeting engagements within the HubSpot CRM.  You can log, retrieve, update, and delete meeting engagements created manually, scheduled via the meetings tool, or integrated with Google Calendar/Office 365.

## API Endpoints

All endpoints are under the base URL `/crm/v3/objects/meetings`.  Replace `{meetingId}` with the actual meeting ID.

**Note:**  The full list of endpoints and their detailed specifications are assumed to be available on a separate "Endpoints" tab referenced throughout this document. This documentation focuses on the core functionality described in the provided text.

### 1. Create a Meeting (POST `/crm/v3/objects/meetings`)

Creates a new meeting engagement.

**Request Body:**

The request body is a JSON object with `properties` and optional `associations` objects.

* **`properties` (object):**  Meeting details.  Required fields are marked with an asterisk (*).

    | Field                   | Description                                                                                                     | Type             | Required | Example                                   |
    |------------------------|-----------------------------------------------------------------------------------------------------------------|-----------------|----------|-------------------------------------------|
    | `hs_timestamp`*        | Date and time the meeting occurred (Unix timestamp in milliseconds or UTC format). Defaults to `hs_meeting_start_time` if missing. | string/number    | yes      | `2024-10-27T10:00:00Z` or `1703632000000` |
    | `hs_meeting_title`     | Meeting title                                                                                                    | string           | no       | "Project Kickoff"                        |
    | `hubspot_owner_id`     | ID of the meeting owner.                                                                                       | string           | no       | "1234567890"                            |
    | `hs_meeting_body`      | Meeting description                                                                                               | string           | no       | "Discuss project requirements"            |
    | `hs_internal_meeting_notes` | Internal notes for your team.                                                                                   | string           | no       | "Next steps: Design mockups"             |
    | `hs_meeting_external_url` | External URL for the calendar event (e.g., Zoom link).                                                        | string           | no       | "https://zoom.us/mymeeting"             |
    | `hs_meeting_location`  | Meeting location (physical address, conference room, etc.).                                                   | string           | no       | "Conference Room A"                     |
    | `hs_meeting_start_time` | Meeting start date and time (should match `hs_timestamp`).                                                   | string           | no       | `2024-10-27T10:00:00Z`                   |
    | `hs_meeting_end_time`   | Meeting end date and time.                                                                                       | string           | no       | `2024-10-27T11:00:00Z`                   |
    | `hs_meeting_outcome`    | Meeting outcome (SCHEDULED, COMPLETED, RESCHEDULED, NO SHOW, CANCELED).                                         | string           | no       | "COMPLETED"                              |
    | `hs_activity_type`     | Type of meeting (based on meeting types in your HubSpot account).                                               | string           | no       | "Sales Meeting"                          |
    | `hs_attachment_ids`    | IDs of attached files (semicolon-separated).                                                                  | string           | no       | "123;456"                               |


* **`associations` (array of objects):** Associates the meeting with existing records (e.g., contacts, companies).

    | Field       | Description                                            | Type    | Required | Example                                      |
    |-------------|--------------------------------------------------------|---------|----------|----------------------------------------------|
    | `to`        | Object to associate (contains `id`).                   | object  | yes      | `{"id": 101}`                               |
    | `types`     | Association type (contains `associationCategory` and `associationTypeId`). | array   | yes      | `[{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 200}]` |


**Example Request (JSON):**

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27T10:00:00Z",
    "hs_meeting_title": "Project Kickoff",
    "hubspot_owner_id": "1234567890"
    // ... other properties
  },
  "associations": [
    {
      "to": {"id": 101},
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 200}]
    }
  ]
}
```

**Response:** A JSON object representing the newly created meeting.


### 2. Retrieve Meetings (GET `/crm/v3/objects/meetings` or GET `/crm/v3/objects/meetings/{meetingId}`)

Retrieves meetings.  Use the individual ID endpoint for a single meeting, otherwise use the base endpoint for a list.

* **Parameters (for both endpoints):**

    | Parameter    | Description                                         | Type    |
    |--------------|-----------------------------------------------------|---------|
    | `properties` | Comma-separated list of properties to return.        | string  |
    | `associations` | Comma-separated list of associated objects to retrieve. | string  |
    | `limit`       | Maximum number of results per page (for list endpoint).| integer |


* **Response:** A JSON object (single meeting) or array of JSON objects (list of meetings).


### 3. Update a Meeting (PATCH `/crm/v3/objects/meetings/{meetingId}`)

Updates an existing meeting.

**Request Body:**  A JSON object with the `properties` object containing the fields to update.  HubSpot ignores read-only and non-existent properties.  An empty string clears a property value.

**Example Request (JSON):**

```json
{
  "properties": {
    "hs_meeting_outcome": "COMPLETED"
  }
}
```

**Response:**  A JSON object representing the updated meeting.


### 4. Associate Existing Meetings with Records (PUT `/crm/v3/objects/meetings/{meetingId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates an existing meeting with a record.

**Parameters:**

* `{meetingId}`: ID of the meeting.
* `{toObjectType}`: Type of object (e.g., "contact", "company").
* `{toObjectId}`: ID of the object to associate.
* `{associationTypeId}`: ID of the association type.


**Response:** Confirmation of association.


### 5. Remove an Association (DELETE `/crm/v3/objects/meetings/{meetingId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Removes an association between a meeting and a record. Uses the same URL structure as the associate endpoint.

**Response:** Confirmation of removal.


### 6. Pin a Meeting (Implicit through record APIs)

Pinning is not a direct API call for meetings. Instead, you include the meeting's `id` in the `hs_pinned_engagement_id` field when creating or updating a record (contact, company, deal, etc.) via their respective object APIs.  Only one activity can be pinned per record.


### 7. Delete a Meeting (DELETE `/crm/v3/objects/meetings/{meetingId}`)

Deletes a meeting (moves it to the recycle bin).

**Response:** Confirmation of deletion.


## Error Handling

The API response will include error details in case of failures. Refer to the HubSpot API documentation for specific error codes and messages.


This documentation provides a high-level overview.  Refer to the complete HubSpot Meetings API documentation ("Endpoints" tab) for exhaustive details, including authentication, rate limits, and detailed error handling.
