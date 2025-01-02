# HubSpot Meetings API Documentation

This document details the HubSpot Meetings API, allowing you to manage meeting engagements within the HubSpot CRM.  You can log, retrieve, update, and delete meetings, and associate them with other HubSpot records.

## API Endpoints Base URL: `/crm/v3/objects/meetings`

All API endpoints below are relative to the base URL above.  Remember to replace placeholders like `{meetingId}`, `{toObjectId}`, etc. with the appropriate values.  Authentication is required for all API calls; refer to HubSpot's authentication documentation for details.

## 1. Create a Meeting (POST)

Creates a new meeting engagement.

**Request:**

* **Method:** `POST`
* **URL:** `/crm/v3/objects/meetings`
* **Body:** JSON payload with `properties` and optional `associations` objects.

**Properties Object:**

| Field                  | Description                                                                                                    | Type           | Required | Example                                   |
|------------------------|----------------------------------------------------------------------------------------------------------------|----------------|----------|-------------------------------------------|
| `hs_timestamp`         | Date and time the meeting occurred (Unix timestamp in milliseconds or UTC format). Defaults to `hs_meeting_start_time` if missing. | String/Number | Yes      | `1677062400000` (Unix timestamp) or `"2023-02-20T12:00:00Z"` (UTC) |
| `hs_meeting_title`     | Meeting title.                                                                                             | String         | No       | `"Project Kickoff"`                     |
| `hubspot_owner_id`     | ID of the meeting owner.                                                                                     | String         | No       | `"1234567"`                            |
| `hs_meeting_body`      | Meeting description.                                                                                           | String         | No       | `"Discuss project goals and timeline."`     |
| `hs_internal_meeting_notes` | Internal notes for your team (not visible to attendees).                                                      | String         | No       | `"Action items: ..."`                    |
| `hs_meeting_external_url` | External URL for the calendar event (e.g., Google Calendar link).                                           | String         | No       | `"https://calendar.google.com/event..."` |
| `hs_meeting_location`  | Meeting location (physical address, conference room, videoconference link, phone number).                     | String         | No       | `"Conference Room A"`                   |
| `hs_meeting_start_time`| Meeting start date and time (UTC format).                                                                    | String         | No       | `"2023-02-20T12:00:00Z"`                |
| `hs_meeting_end_time`  | Meeting end date and time (UTC format).                                                                      | String         | No       | `"2023-02-20T13:00:00Z"`                |
| `hs_meeting_outcome`   | Meeting outcome (SCHEDULED, COMPLETED, RESCHEDULED, NO_SHOW, CANCELED).                                      | String         | No       | `"COMPLETED"`                           |
| `hs_activity_type`     | Type of meeting (based on your HubSpot account's meeting types).                                             | String         | No       | `"Sales Meeting"`                       |
| `hs_attachment_ids`    | IDs of attached files (semicolon-separated).                                                              | String         | No       | `"123;456"`                             |


**Associations Object (Optional):**

Associates the meeting with existing HubSpot records.

| Field      | Description                                            | Type    | Required | Example          |
|------------|--------------------------------------------------------|---------|----------|-----------------|
| `to`       | Object to associate with (ID).                         | Object  | Yes      | `{"id": 101}`   |
| `types`    | Association type.                                      | Array   | Yes      | `[{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 200}]` |


**Example Request Body:**

```json
{
  "properties": {
    "hs_timestamp": "2024-03-08T10:00:00Z",
    "hs_meeting_title": "Client Meeting",
    "hubspot_owner_id": "12345"
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


## 2. Retrieve Meetings (GET)

Retrieves meetings.  Can retrieve individual meetings or a list.


**2.1 Retrieve a Single Meeting:**

* **Method:** `GET`
* **URL:** `/crm/v3/objects/meetings/{meetingId}`
* **Parameters:**
    * `properties`: Comma-separated list of properties to return.
    * `associations`: Comma-separated list of associated objects to retrieve.

**2.2 Retrieve a List of Meetings:**

* **Method:** `GET`
* **URL:** `/crm/v3/objects/meetings`
* **Parameters:**
    * `limit`: Maximum number of results per page.
    * `properties`: Comma-separated list of properties to return.


**Response:** A JSON object (single meeting) or a JSON array (list of meetings).


## 3. Update a Meeting (PATCH)

Updates an existing meeting.

* **Method:** `PATCH`
* **URL:** `/crm/v3/objects/meetings/{meetingId}`
* **Body:** JSON payload with the properties to update.  Omit properties to leave them unchanged.  Use an empty string (`""`) to clear a property value.

**Example Request Body:**

```json
{
  "properties": {
    "hs_meeting_outcome": "COMPLETED"
  }
}
```

**Response:** A JSON object representing the updated meeting.


## 4. Associate Existing Meetings with Records (PUT)

Associates an existing meeting with a record.

* **Method:** `PUT`
* **URL:** `/crm/v3/objects/meetings/{meetingId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`
* **Parameters:**
    * `meetingId`: ID of the meeting.
    * `toObjectType`: Type of object (e.g., "contact", "company").
    * `toObjectId`: ID of the record.
    * `associationTypeId`: ID of the association type (obtainable via the Associations API).


## 5. Remove an Association (DELETE)

Removes an association between a meeting and a record.

* **Method:** `DELETE`
* **URL:** `/crm/v3/objects/meetings/{meetingId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`
* **Parameters (same as PUT):**
    * `meetingId`: ID of the meeting.
    * `toObjectType`: Type of object.
    * `toObjectId`: ID of the record.
    * `associationTypeId`: ID of the association type.


## 6. Pin a Meeting on a Record

Pins a meeting to the top of a record's timeline. This is done by including the meeting's `id` in the `hs_pinned_engagement_id` field when creating or updating the record via the relevant object API (contacts, companies, etc.).


## 7. Delete a Meeting (DELETE)

Deletes a meeting (moves it to the recycling bin).

* **Method:** `DELETE`
* **URL:** `/crm/v3/objects/meetings/{meetingId}`


**Note:**  Error handling and detailed response codes are not included here for brevity but are crucial for production-level integration. Refer to the official HubSpot API documentation for complete details.  Also, remember to consult HubSpot's rate limits to avoid exceeding API usage allowances.
