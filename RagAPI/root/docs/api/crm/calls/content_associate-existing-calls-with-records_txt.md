# HubSpot Calls API Documentation

This document details the HubSpot Calls API, allowing you to log and manage calls within the HubSpot CRM.  This API interacts with call engagements, enabling creation, retrieval, updating, association, and deletion of call records.

## API Endpoints

All endpoints are located under the `/crm/v3/objects/calls` base path.  Remember to replace `{callId}` and other placeholders with the appropriate values.  Authentication is required for all API calls.

### 1. Create a Call Engagement (POST `/crm/v3/objects/calls`)

Creates a new call engagement.

**Request Body:**

The request body must contain a `properties` object and optionally an `associations` object.

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27T12:00:00Z", // Required. Unix timestamp (milliseconds) or UTC format.
    "hs_call_body": "Call summary notes.",
    "hs_call_callee_object_id": "12345", // ID of the associated HubSpot record.
    "hs_call_callee_object_type": "CONTACT", // Type of the associated record (e.g., CONTACT, COMPANY).
    "hs_call_direction": "OUTBOUND", // INBOUND or OUTBOUND.
    "hs_call_disposition": "f240bbac-87c9-4f6e-bf70-924b57d47db7", // GUID for call outcome (e.g., Connected).  See table below for defaults.
    "hs_call_duration": 360000, // Duration in milliseconds.
    "hs_call_from_number": "+15551234567",
    "hs_call_recording_url": "https://example.com/recording.mp3", // HTTPS URL only.
    "hs_call_status": "COMPLETED", // See table below for possible statuses.
    "hs_call_title": "Initial Consultation",
    "hs_call_source": "INTEGRATIONS_PLATFORM", // Required for recording/transcription pipeline.
    "hs_call_to_number": "+15559876543",
    "hubspot_owner_id": "123456", // ID of the owner.
    "hs_activity_type": "Sales Call", // Depends on your HubSpot account call types.
    "hs_attachment_ids": "1;2;3" // Semicolon-separated IDs of attachments.
  },
  "associations": [
    {
      "to": { "id": 500 },
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 194 }]
    }
  ]
}
```

**Default `hs_call_disposition` Values:**

| Label             | GUID                                      |
|----------------------|------------------------------------------|
| Busy               | 9d9162e7-6cf3-4944-bf63-4dff82258764     |
| Connected           | f240bbac-87c9-4f6e-bf70-924b57d47db7     |
| Left live message   | a4c4c377-d246-4b32-a13b-75a56a4cd0ff     |
| Left voicemail      | b2cf5968-551e-4856-9783-52b3da59a7d0     |
| No answer           | 73a0d17f-1163-4015-bdd5-ec830791da20     |
| Wrong number        | 17b47fee-58de-441e-a44c-c6300d46f273     |


**Default `hs_call_status` Values:**

BUSY, CALLING_CRM_USER, CANCELED, COMPLETED, CONNECTING, FAILED, IN_PROGRESS, NO_ANSWER, QUEUED, RINGING


**Response:**  A JSON object representing the created call, including the `callId`.


### 2. Retrieve Calls (GET `/crm/v3/objects/calls`)

Retrieves calls. Can retrieve a single call by ID or a list of calls.


**Individual Call (GET `/crm/v3/objects/calls/{callId}`):**

**Parameters:**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.

**Response:** A JSON object representing the call.

**List of Calls (GET `/crm/v3/objects/calls`):**

**Parameters:**

* `limit`: Maximum number of results per page.
* `properties`: Comma-separated list of properties to return.

**Response:** A JSON object containing a list of calls and pagination information.


### 3. Identify Voicemails (GET `/crm/v3/objects/calls/{callId}`)

To distinguish between recorded calls and voicemails, include `hs_call_status` and `hs_call_has_voicemail` in your GET request:

* `hs_call_status`:  `missed` for voicemails.
* `hs_call_has_voicemail`: `true` for voicemails, `false` for missed calls without voicemails, `null` for other statuses.


### 4. Update a Call (PATCH `/crm/v3/objects/calls/{callId}`)

Updates an existing call.

**Request Body:**

```json
{
  "properties": {
    "hs_call_body": "Updated call notes."
  }
}
```

**Response:** A JSON object representing the updated call.


### 5. Associate Existing Calls (PUT `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates an existing call with a record.

**Path Parameters:**

* `callId`: The ID of the call.
* `toObjectType`: The type of object (e.g., `contact`, `company`).
* `toObjectId`: The ID of the record.
* `associationTypeId`: The ID of the association type.


### 6. Remove an Association (DELETE `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Removes an association between a call and a record.


### 7. Pin a Call (Update record via object APIs)

Pin a call to the top of a record's timeline by including the call's `id` in the `hs_pinned_engagement_id` field when updating the associated record (contact, company, etc.) using their respective object APIs.


### 8. Delete a Call (DELETE `/crm/v3/objects/calls/{callId}`)

Deletes a call (moves it to the recycling bin).


## Error Handling

The API will return standard HTTP status codes to indicate success or failure. Error responses will include detailed JSON messages explaining the issue.


This documentation provides a comprehensive overview of the HubSpot Calls API.  Refer to the HubSpot developer documentation for the most up-to-date information and details on batch operations and advanced features.
