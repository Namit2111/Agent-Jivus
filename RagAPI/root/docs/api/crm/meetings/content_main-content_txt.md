# HubSpot Meetings API Documentation

This document details the HubSpot Meetings API, allowing you to manage meeting engagements within HubSpot.  You can create, retrieve, update, associate, and delete meetings via API calls.

## API Endpoints Base URL: `/crm/v3/objects/meetings`

All API endpoints below are relative to this base URL.  Remember to replace `{meetingId}` and other placeholders with the appropriate values.

## 1. Create a Meeting

**Method:** `POST`
**Endpoint:** `/crm/v3/objects/meetings`

Creates a new meeting engagement.  The request body requires a `properties` object and optionally an `associations` object.

**Request Body:**

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27T12:00:00.000Z", // Required. Unix timestamp (milliseconds) or UTC format. Defaults to hs_meeting_start_time if missing.
    "hs_meeting_title": "Project Kickoff",
    "hubspot_owner_id": "1234567", // HubSpot ID of the meeting owner.
    "hs_meeting_body": "Meeting agenda...",
    "hs_internal_meeting_notes": "Internal notes...",
    "hs_meeting_external_url": "https://example.com/meeting",
    "hs_meeting_location": "Conference Room A",
    "hs_meeting_start_time": "2024-10-27T12:00:00.000Z",
    "hs_meeting_end_time": "2024-10-27T13:00:00.000Z",
    "hs_meeting_outcome": "SCHEDULED", // Options: SCHEDULED, COMPLETED, RESCHEDULED, NO SHOW, CANCELED
    "hs_activity_type": "Client Meeting" // Based on meeting types in your HubSpot account.
    "hs_attachment_ids": "123;456" // Multiple IDs separated by semicolons.
  },
  "associations": [
    {
      "to": {
        "id": 101 // ID of the associated record (e.g., contact ID).
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 200 // Default or custom association type ID.
        }
      ]
    }
  ]
}
```

**Response:**  A JSON object representing the created meeting, including its ID.

## 2. Retrieve Meetings

**Method:** `GET`

**Endpoint (Individual Meeting):** `/crm/v3/objects/meetings/{meetingId}`

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of associated objects to retrieve.

**Endpoint (All Meetings):** `/crm/v3/objects/meetings`

**Query Parameters:**

* `limit`: Maximum number of results per page.
* `properties`: Comma-separated list of properties to return.

**Response:** A JSON object or array of JSON objects representing the meeting(s).


## 3. Update a Meeting

**Method:** `PATCH`
**Endpoint:** `/crm/v3/objects/meetings/{meetingId}`

Updates an existing meeting.  The request body only needs to include the properties you want to modify.  Empty strings clear property values.

**Request Body (Example):**

```json
{
  "properties": {
    "hs_meeting_outcome": "COMPLETED"
  }
}
```

**Response:** A JSON object representing the updated meeting.

## 4. Associate Existing Meetings with Records

**Method:** `PUT`
**Endpoint:** `/crm/v3/objects/meetings/{meetingId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

Associates a meeting with a record (e.g., contact, company).

**Path Parameters:**

* `meetingId`: The ID of the meeting.
* `toObjectType`: The type of object (e.g., `contact`, `company`).
* `toObjectId`: The ID of the record.
* `associationTypeId`: The ID of the association type.

**Response:** A confirmation or error message.

## 5. Remove an Association

**Method:** `DELETE`
**Endpoint:** `/crm/v3/objects/meetings/{meetingId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

Removes an association between a meeting and a record.  Uses the same endpoint as association creation.

**Response:** A confirmation or error message.

## 6. Pin a Meeting on a Record

Pinning a meeting to a record is done indirectly.  Include the meeting's `id` in the `hs_pinned_engagement_id` field when creating or updating the record via its respective object API (contacts, companies, deals, etc.).


## 7. Delete a Meeting

**Method:** `DELETE`
**Endpoint:** `/crm/v3/objects/meetings/{meetingId}`

Deletes a meeting (moves it to the recycling bin).

**Response:** A confirmation or error message.


**Note:**  Error handling, authentication details (API keys, etc.), and rate limits are not explicitly covered here but are crucial aspects of API usage. Refer to the HubSpot API documentation for complete details.  Batch operations are also available for creating, updating, and deleting meetings; consult the HubSpot documentation for details on those endpoints.
