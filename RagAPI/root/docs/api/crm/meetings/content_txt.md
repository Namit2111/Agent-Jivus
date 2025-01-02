# HubSpot Meetings API Documentation

This document describes the HubSpot Meetings API, allowing you to manage meeting engagements within the HubSpot CRM.  You can create, retrieve, update, associate, and delete meeting engagements programmatically.

## API Endpoints Base URL: `/crm/v3/objects/meetings`

All API requests use the base URL `/crm/v3/objects/meetings` followed by specific endpoints for different actions.  Authentication is required for all requests (details not provided in source text, assume standard HubSpot API authentication).


## 1. Create a Meeting (POST `/crm/v3/objects/meetings`)

Creates a new meeting engagement.

**Request Body:**

The request body is a JSON object containing `properties` and optionally `associations`.

* **`properties` (object):**  Contains meeting details.  Required fields are marked with an asterisk (*).

| Field                     | Description                                                                                                         | Type             | Example                               |
|--------------------------|---------------------------------------------------------------------------------------------------------------------|-----------------|---------------------------------------|
| `hs_timestamp`*          | Date and time the meeting occurred (Unix timestamp in milliseconds or UTC format). Defaults to `hs_meeting_start_time` if missing. | String           | `"2024-10-27T10:00:00Z"`            |
| `hs_meeting_title`       | Meeting title.                                                                                                      | String           | `"Project Kickoff"`                 |
| `hubspot_owner_id`*      | HubSpot ID of the meeting owner.                                                                                    | String           | `"1234567"`                         |
| `hs_meeting_body`        | Meeting description.                                                                                                  | String           | `"Discussion of project goals"`       |
| `hs_internal_meeting_notes` | Internal notes (not visible to attendees).                                                                            | String           | `"Next steps: ..."`                 |
| `hs_meeting_external_url`| External URL to the calendar event (e.g., Zoom link).                                                              | String           | `"https://example.com/meeting"`      |
| `hs_meeting_location`    | Meeting location (physical address, videoconference link, etc.).                                                    | String           | `"Conference Room A" or "Zoom call"` |
| `hs_meeting_start_time`  | Meeting start time (UTC format).                                                                                   | String           | `"2024-10-27T10:00:00Z"`            |
| `hs_meeting_end_time`    | Meeting end time (UTC format).                                                                                     | String           | `"2024-10-27T11:00:00Z"`            |
| `hs_meeting_outcome`     | Meeting outcome (e.g., `SCHEDULED`, `COMPLETED`, `RESCHEDULED`, `NO SHOW`, `CANCELED`).                            | String           | `"COMPLETED"`                        |
| `hs_activity_type`       | Type of meeting (based on meeting types in your HubSpot account).                                                   | String           | `"Sales Meeting"`                    |
| `hs_attachment_ids`      | IDs of attached files (semicolon-separated).                                                                      | String           | `"1;2;3"`                           |


* **`associations` (array of objects):**  Associates the meeting with existing HubSpot records (e.g., contacts, companies).

| Field      | Description                                                       | Type    | Example                                    |
|------------|-------------------------------------------------------------------|---------|---------------------------------------------|
| `to`       | Object to associate with (contains `id`).                         | Object  | `{"id": 123}`                             |
| `types`    | Association type (contains `associationCategory` and `associationTypeId`). | Array   | `[{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 200}]` |


**Example Request (JSON):**

```json
{
  "properties": {
    "hs_timestamp": "1698387200000",
    "hubspot_owner_id": "1234567",
    "hs_meeting_title": "Project Kickoff",
    "hs_meeting_start_time": "2024-10-27T10:00:00Z",
    "hs_meeting_end_time": "2024-10-27T11:00:00Z",
    "hs_meeting_outcome": "SCHEDULED"
  },
  "associations": [
    {
      "to": {"id": 876543},
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 200}]
    }
  ]
}
```

**Response (JSON - example):**  A successful response will include the newly created meeting's ID and other properties.

```json
{
  "id": "987654321",
  // ... other properties ...
}
```


## 2. Retrieve Meetings (GET)

* **GET `/crm/v3/objects/meetings/{meetingId}`:** Retrieves a single meeting by its ID.  `properties` and `associations` parameters can filter the returned data.

* **GET `/crm/v3/objects/meetings`:** Retrieves a list of meetings.  `limit` and `properties` parameters control the results.

**Parameters:**

| Parameter    | Description                                                | Type     |
|--------------|------------------------------------------------------------|----------|
| `meetingId`  | (Only for single meeting retrieval) The ID of the meeting. | String   |
| `limit`      | Maximum number of results per page (for list retrieval).     | Integer  |
| `properties` | Comma-separated list of properties to return.                | String   |
| `associations` | Comma-separated list of associated objects to return.       | String   |


## 3. Update a Meeting (PATCH `/crm/v3/objects/meetings/{meetingId}`)

Updates an existing meeting.  Provide only the properties you wish to modify.

**Request Body (JSON):**  Similar structure to the `properties` object in the create request.

## 4. Associate Existing Meetings with Records (PUT `/crm/v3/objects/meetings/{meetingId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates a meeting with another HubSpot record.

**Parameters:**

| Parameter       | Description                                            | Type     |
|-----------------|--------------------------------------------------------|----------|
| `meetingId`     | ID of the meeting.                                      | String   |
| `toObjectType`  | Type of object to associate (e.g., `contact`, `company`). | String   |
| `toObjectId`    | ID of the object to associate.                           | String   |
| `associationTypeId` | ID of the association type.                             | String   |


## 5. Remove an Association (DELETE `/crm/v3/objects/meetings/{meetingId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Removes an association between a meeting and another record.  Uses the same URL as the associate endpoint.


## 6. Pin a Meeting (Update Record using `hs_pinned_engagement_id`)

Pins a meeting to the top of a record's timeline using the `hs_pinned_engagement_id` field when updating the associated record (contact, company, etc.) via their respective object APIs.  Only one activity can be pinned per record.


## 7. Delete a Meeting (DELETE `/crm/v3/objects/meetings/{meetingId}`)

Deletes a meeting (moves it to the recycling bin).


## Error Handling

The API will return standard HTTP status codes to indicate success or failure.  Error responses will include details in the response body (specific format not provided in source text, assume standard HubSpot API error response structure).


This documentation provides a concise overview.  Refer to the HubSpot developer documentation for complete details on all endpoints, parameters, and error handling.
