# HubSpot Meetings API Documentation

This document details the HubSpot Meetings API, allowing you to manage meeting engagements within the HubSpot CRM.  You can log, retrieve, update, and delete meeting data, and associate meetings with CRM records.

## API Endpoints

All endpoints are under the base URL: `/crm/v3/objects/meetings`

**Note:**  Replace `{meetingId}` and `{toObjectId}` with the respective IDs.


### 1. Create a Meeting (POST `/crm/v3/objects/meetings`)

Creates a new meeting engagement.

**Request Body:**

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27T10:00:00.000Z", // Required. Unix timestamp in milliseconds or UTC format. Defaults to hs_meeting_start_time if missing.
    "hs_meeting_title": "Project Kickoff",
    "hubspot_owner_id": "1234567", // HubSpot ID of the meeting owner.
    "hs_meeting_body": "Discussion of project goals and next steps.",
    "hs_internal_meeting_notes": "Internal notes for the team.",
    "hs_meeting_external_url": "https://example.com/meetinglink",
    "hs_meeting_location": "Conference Room A",
    "hs_meeting_start_time": "2024-10-27T10:00:00.000Z",
    "hs_meeting_end_time": "2024-10-27T11:00:00.000Z",
    "hs_meeting_outcome": "SCHEDULED", // Options: SCHEDULED, COMPLETED, RESCHEDULED, NO_SHOW, CANCELED
    "hs_activity_type": "Client Meeting", // Based on meeting types in your HubSpot account.
    "hs_attachment_ids": "123;456" // Multiple attachment IDs separated by semicolons.
  },
  "associations": [
    {
      "to": {
        "id": 789 // ID of the associated record (e.g., contact, company).
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 200 // Default association type ID or custom ID.
        }
      ]
    }
  ]
}
```

**Response:**  A JSON object representing the created meeting, including its ID.

### 2. Retrieve Meetings (GET `/crm/v3/objects/meetings`)

Retrieves meetings.  Can retrieve individual meetings or a list.

**Individual Meeting (GET `/crm/v3/objects/meetings/{meetingId}`):**

**Parameters:**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of associated objects to retrieve.

**List of Meetings:**

**Parameters:**

* `limit`: Maximum number of results per page.
* `properties`: Comma-separated list of properties to return.


**Response:** A JSON object or array of JSON objects representing the retrieved meetings.


### 3. Update a Meeting (PATCH `/crm/v3/objects/meetings/{meetingId}`)

Updates an existing meeting.

**Request Body:**

```json
{
  "properties": {
    "hs_meeting_outcome": "COMPLETED"
  }
}
```

**Response:** A JSON object representing the updated meeting.


### 4. Associate Existing Meetings with Records (PUT `/crm/v3/objects/meetings/{meetingId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates a meeting with a record (e.g., contact, company).

**Path Parameters:**

* `meetingId`: The ID of the meeting.
* `toObjectType`: The type of object (e.g., `contact`, `company`).
* `toObjectId`: The ID of the record.
* `associationTypeId`: The ID of the association type.

**Response:**  A success or error response.


### 5. Remove an Association (DELETE `/crm/v3/objects/meetings/{meetingId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Removes an association between a meeting and a record.  Uses the same path parameters as the association PUT request.

**Response:** A success or error response.


### 6. Pin a Meeting on a Record

Pinning is done indirectly by including the meeting's `id` in the `hs_pinned_engagement_id` field when creating or updating a record via the object APIs (contacts, companies, deals, tickets, custom objects).


### 7. Delete a Meeting (DELETE `/crm/v3/objects/meetings/{meetingId}`)

Deletes a meeting (moves it to the recycle bin).

**Response:** A success or error response.


## Error Handling

The API will return standard HTTP status codes to indicate success or failure.  Error responses will include a JSON object with details about the error.


## Authentication

Authentication details are not included in this documentation but are necessary to use the API.  Refer to HubSpot's API documentation for authentication methods.


This documentation provides a concise overview.  Refer to the official HubSpot API documentation for complete details and the latest information.