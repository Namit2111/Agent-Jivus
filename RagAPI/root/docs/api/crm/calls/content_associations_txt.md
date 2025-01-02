# HubSpot Calls API Documentation

This document details the HubSpot Calls API, allowing you to manage call engagements within the HubSpot CRM.  This includes creating, retrieving, updating, associating, and deleting calls.

## API Endpoint Base URL:

`/crm/v3/objects/calls`

## Authentication:

This API requires HubSpot API Key authentication.  Refer to the HubSpot API documentation for details on obtaining and using an API key.


## 1. Create a Call Engagement (POST)

**Endpoint:** `/crm/v3/objects/calls`

**Method:** `POST`

**Request Body:**

The request body contains a `properties` object and an optional `associations` object.

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27T12:00:00.000Z", // Required.  Unix timestamp (milliseconds) or UTC format.
    "hs_call_body": "Call discussion notes.",
    "hs_call_callee_object_id": "123", // HubSpot ID of the recipient (outbound) or dialer (inbound).
    "hs_call_callee_object_type": "contact", // Object type of the recipient (outbound) or dialer (inbound) (e.g., contact, company).
    "hs_call_direction": "OUTBOUND", // Or "INBOUND"
    "hs_call_disposition": "f240bbac-87c9-4f6e-bf70-924b57d47db7", // GUID for call outcome (e.g., Connected).  See below for default values.
    "hs_call_duration": 360000, // Duration in milliseconds.
    "hs_call_from_number": "+15551234567",
    "hs_call_recording_url": "https://example.com/recording.mp3", // HTTPS URL only.
    "hs_call_status": "COMPLETED", // BUSY, CALLING_CRM_USER, CANCELED, COMPLETED, CONNECTING, FAILED, IN_PROGRESS, NO_ANSWER, QUEUED, RINGING
    "hs_call_title": "Customer Support Call",
    "hs_call_source": "INTEGRATIONS_PLATFORM", // Required for recording and transcription pipelines.
    "hs_call_to_number": "+15559876543",
    "hubspot_owner_id": "12345", // HubSpot ID of the call owner.
    "hs_activity_type": "Phone Call", // Based on call types in your HubSpot account.
    "hs_attachment_ids": "1;2;3" // IDs of attachments, separated by semicolons.
  },
  "associations": [
    {
      "to": { "id": 500 },
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 194 }] // Contact association.  See below for details.
    }
  ]
}
```

**Default Call Disposition GUIDs:**

* Busy: `9d9162e7-6cf3-4944-bf63-4dff82258764`
* Connected: `f240bbac-87c9-4f6e-bf70-924b57d47db7`
* Left live message: `a4c4c377-d246-4b32-a13b-75a56a4cd0ff`
* Left voicemail: `b2cf5968-551e-4856-9783-52b3da59a7d0`
* No answer: `73a0d17f-1163-4015-bdd5-ec830791da20`
* Wrong number: `17b47fee-58de-441e-a44c-c6300d46f273`


**Response:**  A JSON object representing the created call, including its `callId`.


## 2. Retrieve Calls (GET)

**Endpoint:** `/crm/v3/objects/calls`  (for all calls) or `/crm/v3/objects/calls/{callId}` (for a single call)

**Method:** `GET`

**Parameters (for all calls):**

* `limit`:  Maximum number of results per page.
* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.

**Parameters (for a single call):**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.

**Response:**  A JSON object containing the requested call(s) data.


## 3. Update a Call (PATCH)

**Endpoint:** `/crm/v3/objects/calls/{callId}`

**Method:** `PATCH`

**Request Body:**  A JSON object with a `properties` object containing the fields to update.  Omit fields you don't want to change.  Use an empty string (`""`) to clear a property value.

```json
{
  "properties": {
    "hs_call_body": "Updated call notes."
  }
}
```

**Response:** A JSON object representing the updated call.



## 4. Associate Existing Calls with Records (PUT)

**Endpoint:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `PUT`

* `{callId}`: The ID of the call.
* `{toObjectType}`:  Object type (e.g., contact, company).
* `{toObjectId}`: ID of the record to associate.
* `{associationTypeId}`:  Association type ID (obtainable via the Associations API).


## 5. Remove an Association (DELETE)

**Endpoint:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `DELETE`


## 6. Pin a Call on a Record

Pinning is done via the `hs_pinned_engagement_id` field when creating or updating records using other HubSpot object APIs (contacts, companies, etc.).


## 7. Delete a Call (DELETE)

**Endpoint:** `/crm/v3/objects/calls/{callId}`

**Method:** `DELETE`

This moves the call to the recycle bin; it can be restored later.


## Error Handling:

The API will return standard HTTP status codes and JSON error responses to indicate success or failure.  Refer to HubSpot's API documentation for details on error handling.


This documentation provides a concise overview.  Consult the official HubSpot API documentation for comprehensive details, including rate limits, detailed error codes, and batch operations.
