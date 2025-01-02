# HubSpot Meetings API Documentation

This document details the HubSpot Meetings API, allowing you to manage meeting engagements within the HubSpot CRM.  You can create, retrieve, update, associate, and delete meeting engagements.

## API Endpoints

All endpoints are under the base URL `/crm/v3/objects/meetings`.  Replace `{meetingId}` with the actual meeting ID.  Authentication is required (details not provided in source).


##  1. Create a Meeting (POST `/crm/v3/objects/meetings`)

Creates a new meeting engagement.

**Request Body:**

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27T12:00:00.000Z", // Required.  Unix timestamp (milliseconds) or UTC format. Defaults to hs_meeting_start_time if missing.
    "hs_meeting_title": "Meeting Title",
    "hubspot_owner_id": "1234567", // ID of the meeting owner.
    "hs_meeting_body": "Meeting description",
    "hs_internal_meeting_notes": "Internal notes",
    "hs_meeting_external_url": "https://example.com/meeting",
    "hs_meeting_location": "Conference Room A",
    "hs_meeting_start_time": "2024-10-27T12:00:00.000Z",
    "hs_meeting_end_time": "2024-10-27T13:00:00.000Z",
    "hs_meeting_outcome": "SCHEDULED", // Options: SCHEDULED, COMPLETED, RESCHEDULED, NO SHOW, CANCELED
    "hs_activity_type": "Sales Meeting", // Based on your HubSpot account's meeting types.
    "hs_attachment_ids": "123;456" // Multiple IDs separated by semicolons.
  },
  "associations": [
    {
      "to": { "id": 101 }, // ID of the associated record (e.g., contact ID).
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 200 }] // Association type.  See default IDs or use Associations API for custom types.
    }
  ]
}
```

**Response:**  A JSON object representing the created meeting, including its ID.


## 2. Retrieve Meetings

**2.1 Retrieve a Single Meeting (GET `/crm/v3/objects/meetings/{meetingId}`)**

Retrieves a specific meeting by its ID.

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of associated objects to retrieve.

**Response:** A JSON object representing the meeting.


**2.2 Retrieve All Meetings (GET `/crm/v3/objects/meetings`)**

Retrieves a list of meetings.

**Query Parameters:**

* `limit`: Maximum number of results per page.
* `properties`: Comma-separated list of properties to return.

**Response:** A JSON object containing a list of meetings and pagination information.


## 3. Update a Meeting (PATCH `/crm/v3/objects/meetings/{meetingId}`)

Updates an existing meeting.

**Request Body:**

```json
{
  "properties": {
    "hs_meeting_title": "Updated Meeting Title",
    "hs_meeting_outcome": "COMPLETED"
  }
}
```

HubSpot ignores read-only and non-existent properties.  Use an empty string to clear a property value.

**Response:** A JSON object representing the updated meeting.


## 4. Associate Existing Meetings with Records (PUT `/crm/v3/objects/meetings/{meetingId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates a meeting with another HubSpot record.

**Path Parameters:**

* `meetingId`: ID of the meeting.
* `toObjectType`: Type of object (e.g., `contact`, `company`).
* `toObjectId`: ID of the record to associate.
* `associationTypeId`: ID of the association type (use Associations API for custom types).

**Response:**  Success or error status.


## 5. Remove an Association (DELETE `/crm/v3/objects/meetings/{meetingId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Removes an association between a meeting and a record.  Uses the same URL as the associate endpoint.

**Response:** Success or error status.


## 6. Pin a Meeting on a Record

Pinning a meeting keeps it at the top of a record's timeline.  This is done by including the meeting's `id` in the `hs_pinned_engagement_id` field when creating or updating the record using the relevant object API (Contacts, Companies, Deals, Tickets, Custom Objects).


## 7. Delete a Meeting (DELETE `/crm/v3/objects/meetings/{meetingId}`)

Deletes a meeting (moves it to the recycling bin).

**Response:** Success or error status.


## Note:

The documentation mentions batch operations (create, update, delete, retrieve).  The specifics of these batch operations are not included in the provided text but are referenced as available via the "Endpoints" tab (presumably on the original HubSpot documentation page).  Also, the provided code snippets are formatted inconsistently.  They are presented in a cleaner format above for improved readability.  Finally, error handling and HTTP status codes are not explicitly defined here, but are implicitly assumed to be part of a full API specification.
