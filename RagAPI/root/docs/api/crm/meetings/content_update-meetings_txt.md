# HubSpot Meetings API Documentation

This document details the HubSpot Meetings API, allowing you to manage meeting engagements within the HubSpot CRM.  You can create, retrieve, update, associate, and delete meetings through various API endpoints.

## API Endpoints

All endpoints are under the base URL: `/crm/v3/objects/meetings`

### 1. Create a Meeting (POST `/crm/v3/objects/meetings`)

Creates a new meeting engagement.

**Request Body:**

The request body is a JSON object containing `properties` and optionally `associations`.

**Properties:** (All properties are optional except `hs_timestamp`)

| Field                   | Description                                                                                                           | Type             | Example                                      |
|------------------------|-----------------------------------------------------------------------------------------------------------------------|-----------------|----------------------------------------------|
| `hs_timestamp`         | Required. Meeting date and time (Unix timestamp in milliseconds or UTC format). Defaults to `hs_meeting_start_time` if missing. | String/Number   | `1677011200000` (Unix timestamp) or `"2023-02-20T12:00:00Z"` (UTC) |
| `hs_meeting_title`     | Meeting title.                                                                                                        | String           | `"Project Kickoff"`                           |
| `hubspot_owner_id`     | ID of the meeting owner (HubSpot user ID).                                                                             | String           | `"1234567"`                                  |
| `hs_meeting_body`      | Meeting description.                                                                                                   | String           | `"Discuss project details and next steps"`     |
| `hs_internal_meeting_notes` | Internal notes for your team (not visible to attendees).                                                               | String           | `"Action items: X, Y, Z"`                     |
| `hs_meeting_external_url` | External URL for the calendar event (e.g., Zoom link).                                                               | String           | `"https://zoom.us/j/1234567890"`           |
| `hs_meeting_location`  | Meeting location (physical address, videoconference link, etc.).                                                    | String           | `"Conference Room A" or "https://meet.google.com/abc"` |
| `hs_meeting_start_time`| Meeting start date and time (UTC format).                                                                            | String           | `"2023-02-20T12:00:00Z"`                       |
| `hs_meeting_end_time`  | Meeting end date and time (UTC format).                                                                              | String           | `"2023-02-20T13:00:00Z"`                       |
| `hs_meeting_outcome`   | Meeting outcome (e.g., `SCHEDULED`, `COMPLETED`, `RESCHEDULED`, `NO_SHOW`, `CANCELED`).                               | String           | `"SCHEDULED"`                               |
| `hs_activity_type`    | Type of meeting (based on your HubSpot account's meeting types).                                                      | String           | `"Sales Meeting"`                             |
| `hs_attachment_ids`   | IDs of attached files (semicolon-separated).                                                                           | String           | `"1;2;3"`                                     |


**Associations:**

To associate the meeting with existing HubSpot records (e.g., contacts, companies):

```json
{
  "to": {
    "id": 101 // HubSpot ID of the record
  },
  "types": [
    {
      "associationCategory": "HUBSPOT_DEFINED",
      "associationTypeId": 200 // Default association type ID (check HubSpot documentation for others)
    }
  ]
}
```

**Example Request:**

```json
{
  "properties": {
    "hs_timestamp": "2024-03-08T10:00:00Z",
    "hs_meeting_title": "Client Meeting",
    "hubspot_owner_id": "12345",
    "hs_meeting_start_time": "2024-03-08T10:00:00Z"
  },
  "associations": [
    {
      "to": { "id": 67890 }, // Contact ID
      "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 200 } ]
    }
  ]
}
```

**Response:** (JSON containing the created meeting's details, including its ID)


### 2. Retrieve Meetings (GET)

**Retrieve a Single Meeting (GET `/crm/v3/objects/meetings/{meetingId}`)**

Retrieves a specific meeting by its ID.

**Parameters:**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of associated objects to retrieve.

**Example:**  `/crm/v3/objects/meetings/123?properties=hs_meeting_title,hs_meeting_start_time&associations=contacts`


**Retrieve All Meetings (GET `/crm/v3/objects/meetings`)**

Retrieves a list of meetings.

**Parameters:**

* `limit`: Maximum number of results per page.
* `properties`: Comma-separated list of properties to return.

**Example:** `/crm/v3/objects/meetings?limit=10&properties=hs_meeting_title`


**Response:** (JSON array of meeting objects or a single meeting object)


### 3. Update a Meeting (PATCH `/crm/v3/objects/meetings/{meetingId}`)

Updates an existing meeting.

**Request Body:**

JSON object containing the `properties` to update.  HubSpot ignores read-only and non-existent properties.  Use an empty string to clear a property value.

**Example Request:**

```json
{
  "properties": {
    "hs_meeting_outcome": "COMPLETED"
  }
}
```

**Response:** (JSON containing the updated meeting's details)


### 4. Associate Existing Meetings with Records (PUT `/crm/v3/objects/meetings/{meetingId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates a meeting with a record.

**Parameters:**

* `meetingId`: ID of the meeting.
* `toObjectType`: Type of object (e.g., `contact`, `company`).
* `toObjectId`: ID of the record.
* `associationTypeId`: ID of the association type.


**Example URL:** `/crm/v3/objects/meetings/456/associations/contact/789/200`

**Response:** (Success or error message)


### 5. Remove an Association (DELETE `/crm/v3/objects/meetings/{meetingId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Removes an association between a meeting and a record.  Uses the same URL structure as the associate endpoint.

**Response:** (Success or error message)


### 6. Pin a Meeting on a Record

Pinning is handled indirectly through the record object APIs (contacts, companies, etc.).  Include the meeting's ID in the `hs_pinned_engagement_id` field when creating or updating the record.


### 7. Delete a Meeting (DELETE `/crm/v3/objects/meetings/{meetingId}`)

Deletes a meeting (moves it to the recycle bin).

**Response:** (Success or error message)


## Error Handling

The API will return standard HTTP status codes and JSON error responses detailing the reason for failure.  Refer to HubSpot's API documentation for detailed error codes.


##  Authentication

You'll need a HubSpot API key to authenticate your requests.  Include the key in the `Authorization` header: `Authorization: Bearer YOUR_API_KEY`


This documentation provides a summary.  Always refer to the official HubSpot API documentation for the most up-to-date information and complete details on all available endpoints and parameters.
