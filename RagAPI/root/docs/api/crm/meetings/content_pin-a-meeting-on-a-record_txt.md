# HubSpot Meetings API Documentation

This document details the HubSpot Meetings API, allowing you to manage meeting engagements within the HubSpot CRM.  You can log, retrieve, update, and delete meeting engagements created manually, scheduled via the meetings tool, or integrated with Google Calendar/Office 365.

## API Endpoints Base URL: `/crm/v3/objects/meetings`

All API requests use the base URL `/crm/v3/objects/meetings`  followed by the specific endpoint path.  Authentication is required (details not provided in the source text, consult HubSpot's API documentation for authentication methods).


## API Methods

### 1. Create a Meeting (POST `/crm/v3/objects/meetings`)

Creates a new meeting engagement.

**Request Body:**

The request body contains a `properties` object and an optional `associations` object.

**`properties` Object:**

| Field                  | Description                                                                                                  | Required | Data Type     | Example                               |
|-----------------------|--------------------------------------------------------------------------------------------------------------|----------|----------------|---------------------------------------|
| `hs_timestamp`         | Date and time the meeting occurred (Unix timestamp in milliseconds or UTC format). Defaults to `hs_meeting_start_time` if missing. | Yes      | String/Number  | `1677000000000` or `2023-02-20T12:00:00Z` |
| `hs_meeting_title`    | Meeting title                                                                                                 | No       | String         | "Project Kickoff"                      |
| `hubspot_owner_id`     | ID of the meeting owner.                                                                                      | No       | String         | "11349275740"                         |
| `hs_meeting_body`     | Meeting description                                                                                           | No       | String         | "Discuss project goals and timeline."   |
| `hs_internal_meeting_notes` | Internal notes for your team (not visible to attendees).                                                    | No       | String         | "Action items: ..."                   |
| `hs_meeting_external_url` | External URL for the calendar event (e.g., Google Calendar, Outlook link).                               | No       | String         | "https://zoom.us/..."                 |
| `hs_meeting_location` | Meeting location (physical address, conference room, videoconference link, or phone number).                 | No       | String         | "Conference Room A" or "Zoom Meeting" |
| `hs_meeting_start_time` | Meeting start date and time (UTC format).                                                                   | No       | String         | "2023-02-20T12:00:00Z"                |
| `hs_meeting_end_time`   | Meeting end date and time (UTC format).                                                                     | No       | String         | "2023-02-20T13:00:00Z"                |
| `hs_meeting_outcome`  | Meeting outcome (SCHEDULED, COMPLETED, RESCHEDULED, NO SHOW, CANCELED).                                     | No       | String         | "COMPLETED"                            |
| `hs_activity_type`    | Type of meeting (based on meeting types in your HubSpot account).                                            | No       | String         | "Sales Meeting"                        |
| `hs_attachment_ids`   | IDs of meeting attachments (semicolon-separated).                                                           | No       | String         | "123;456"                             |


**`associations` Object:**

This object allows associating the meeting with existing records (e.g., contacts, companies).

| Field           | Description                                                                          | Required | Data Type |
|-----------------|--------------------------------------------------------------------------------------|----------|------------|
| `to`            | Object to associate (contains `id` field representing the record ID).                | Yes      | Object     |
| `types`         | Association type (contains `associationCategory` and `associationTypeId`).           | Yes      | Array      |


**Example Request:**

```json
{
  "properties": {
    "hs_timestamp": "2024-10-26T10:00:00Z",
    "hs_meeting_title": "Demo Call",
    "hubspot_owner_id": "12345",
    "hs_meeting_start_time": "2024-10-26T10:00:00Z"
  },
  "associations": [
    {
      "to": {"id": 67890},
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 200}]
    }
  ]
}
```

**Response:**  A JSON object representing the created meeting, including its ID.


### 2. Retrieve Meetings (GET `/crm/v3/objects/meetings` or GET `/crm/v3/objects/meetings/{meetingId}`)

**Individual Meeting:**

Retrieves a single meeting by its `meetingId`.

**Parameters:**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of associated objects to retrieve.

**Example Request:**  `GET /crm/v3/objects/meetings/12345`


**All Meetings:**

Retrieves a list of meetings.

**Parameters:**

* `limit`: Maximum number of results per page.
* `properties`: Comma-separated list of properties to return.

**Example Request:** `GET /crm/v3/objects/meetings?limit=10`


**Response:** A JSON object containing the requested meeting(s) or a paginated list of meetings.


### 3. Update a Meeting (PATCH `/crm/v3/objects/meetings/{meetingId}`)

Updates an existing meeting.

**Request Body:**

Contains a `properties` object with the fields to update.  HubSpot ignores read-only and non-existent properties.  An empty string clears a property value.


**Example Request:**

```json
{
  "properties": {
    "hs_meeting_outcome": "COMPLETED"
  }
}
```

**Response:** A JSON object representing the updated meeting.


### 4. Associate Existing Meetings with Records (PUT `/crm/v3/objects/meetings/{meetingId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates an existing meeting with a record.

**Path Parameters:**

* `meetingId`: ID of the meeting.
* `toObjectType`: Type of object (e.g., "contact", "company").
* `toObjectId`: ID of the record.
* `associationTypeId`: ID of the association type.


**Example Request:** `PUT /crm/v3/objects/meetings/12345/associations/contact/67890/200`


**Response:**  A success/failure indication.


### 5. Remove an Association (DELETE `/crm/v3/objects/meetings/{meetingId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Removes an association between a meeting and a record.  Uses the same URL structure as the `Associate Existing Meetings` endpoint.


### 6. Pin a Meeting on a Record

Pins a meeting to the top of a record's timeline.  This is done by including the meeting's `id` in the `hs_pinned_engagement_id` field when creating or updating a record using other HubSpot object APIs (contacts, companies, etc.).


### 7. Delete a Meeting (DELETE `/crm/v3/objects/meetings/{meetingId}`)

Deletes a meeting (moves it to the recycling bin).

**Response:** A success/failure indication.


## Error Handling

(Error handling details are not provided in the source text; refer to the official HubSpot API documentation for specific error codes and messages).


This documentation provides a summary based on the provided text.  Always refer to the official HubSpot API documentation for the most up-to-date and complete information.
