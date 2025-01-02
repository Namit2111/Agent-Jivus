# HubSpot Calls API Documentation

This document details the HubSpot Calls API, allowing you to manage calls within the HubSpot CRM.  The API utilizes standard HTTP methods (POST, GET, PATCH, DELETE) for creating, retrieving, updating, and deleting call records.  All endpoints are under the `/crm/v3/objects/calls` base path.

## API Endpoints

All endpoints below use the base URL: `https://api.hubspot.com/crm/v3/objects/calls`

You will need a HubSpot API key for authentication.  Refer to the HubSpot developer documentation for authentication details.

### 1. Create a Call Engagement (POST `/crm/v3/objects/calls`)

Creates a new call record in HubSpot.

**Request Body:**

The request body is a JSON object with `properties` and optional `associations` fields.

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27T10:00:00Z", // Required.  UTC timestamp (or Unix milliseconds)
    "hs_call_body": "Call summary...",
    "hs_call_callee_object_id": "123", // ID of associated HubSpot record (contact, company, etc.)
    "hs_call_callee_object_type": "CONTACT", // Type of associated record
    "hs_call_direction": "OUTBOUND", // "INBOUND" or "OUTBOUND"
    "hs_call_disposition": "f240bbac-87c9-4f6e-bf70-924b57d47db7", // GUID for call outcome (see below)
    "hs_call_duration": 360000, // Duration in milliseconds
    "hs_call_from_number": "+15551234567",
    "hs_call_recording_url": "https://example.com/recording.mp3", // HTTPS URL only
    "hs_call_status": "COMPLETED", // See status options below
    "hs_call_title": "Client Call",
    "hs_call_source": "INTEGRATIONS_PLATFORM", // Required for recording/transcription pipeline
    "hs_call_to_number": "+15559876543",
    "hubspot_owner_id": "12345", // HubSpot user ID
    "hs_activity_type": "Phone Call", // Based on call types in your HubSpot account
    "hs_attachment_ids": "123;456" // Multiple IDs separated by semicolon
  },
  "associations": [
    {
      "to": { "id": 123 },
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 194 }] // Contact association
    }
  ]
}
```

**Response:**  A JSON object containing the created call's properties, including the `callId`.


**Default Call Outcomes (GUIDs):**

* Busy: `9d9162e7-6cf3-4944-bf63-4dff82258764`
* Connected: `f240bbac-87c9-4f6e-bf70-924b57d47db7`
* Left live message: `a4c4c377-d246-4b32-a13b-75a56a4cd0ff`
* Left voicemail: `b2cf5968-551e-4856-9783-52b3da59a7d0`
* No answer: `73a0d17f-1163-4015-bdd5-ec830791da20`
* Wrong number: `17b47fee-58de-441e-a44c-c6300d46f273`

**Call Statuses:** BUSY, CALLING_CRM_USER, CANCELED, COMPLETED, CONNECTING, FAILED, IN_PROGRESS, NO_ANSWER, QUEUED, RINGING


### 2. Retrieve Calls (GET `/crm/v3/objects/calls`)

Retrieves calls.  Can retrieve a single call by ID or multiple calls.

**GET `/crm/v3/objects/calls/{callId}` (Single Call):**

* **Parameters:** `properties` (comma-separated list), `associations` (comma-separated list of object types)

**GET `/crm/v3/objects/calls` (Multiple Calls):**

* **Parameters:** `limit`, `properties`

**Response:** A JSON object containing a list of calls (for multiple calls) or a single call (for a single call).


### 3. Update a Call (PATCH `/crm/v3/objects/calls/{callId}`)

Updates an existing call.

**Request Body:** Similar to the POST request, but only include properties to be updated.

**Response:** Updated call details.


### 4. Associate Existing Call with Records (PUT `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates a call with a record (e.g., contact, company).

* **Path Parameters:** `callId`, `toObjectType`, `toObjectId`, `associationTypeId`


### 5. Remove an Association (DELETE `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Removes an association between a call and a record.


### 6. Pin a Call (Update Record via Object APIs)

Pin a call to a record's timeline using the `hs_pinned_engagement_id` property when updating the record itself (Contacts, Companies, etc. APIs).


### 7. Delete a Call (DELETE `/crm/v3/objects/calls/{callId}`)

Deletes a call (moves it to the recycle bin).


##  Error Handling

The API returns standard HTTP status codes to indicate success or failure.  Error responses will contain details in the response body.

## Rate Limits

HubSpot APIs have rate limits.  Refer to the HubSpot developer documentation for details on rate limits and how to handle them.


This markdown documentation provides a concise overview.  Refer to the official HubSpot API documentation for the most up-to-date and comprehensive information, including details on batch operations and error handling.
