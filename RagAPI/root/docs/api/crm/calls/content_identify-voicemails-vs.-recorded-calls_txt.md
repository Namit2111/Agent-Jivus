# HubSpot Calls API Documentation

This document details the HubSpot Calls API, allowing you to manage calls within the HubSpot CRM.  It covers creating, retrieving, updating, associating, and deleting call engagements.

## API Endpoints Base URL: `/crm/v3/objects/calls`

All API calls use the base URL `/crm/v3/objects/calls` followed by specific endpoints for different actions.  Authentication is required; refer to HubSpot's API documentation for details.

## 1. Create a Call Engagement (POST)

**Endpoint:** `/crm/v3/objects/calls`

**Method:** `POST`

**Request Body:**  JSON object with `properties` and (optionally) `associations` objects.

**Properties:**

| Field                  | Description                                                                                                         | Type             | Required | Example                                      |
|-------------------------|---------------------------------------------------------------------------------------------------------------------|-----------------|----------|---------------------------------------------|
| `hs_timestamp`         | Call creation time (Unix timestamp in milliseconds or UTC format).                                                 | String/Number    | Yes      | `1679016800000` or `"2023-03-17T00:00:00Z"` |
| `hs_call_body`          | Call description and notes.                                                                                         | String           | No       | "Discussed project X"                       |
| `hs_call_callee_object_id` | ID of the HubSpot record associated with the call (recipient for outbound, dialer for inbound).                 | String           | No       | `12345`                                      |
| `hs_call_callee_object_type` | Type of the associated record (e.g., "contact", "company").                                                       | String           | No       | "contact"                                    |
| `hs_call_direction`     | Call direction ("INBOUND" or "OUTBOUND").                                                                       | String           | No       | "OUTBOUND"                                  |
| `hs_call_disposition`   | Call outcome (use internal GUID). See below for defaults; use the properties API for custom values.         | String           | No       | `9d9162e7-6cf3-4944-bf63-4dff82258764` (Busy)|
| `hs_call_duration`      | Call duration in milliseconds.                                                                                     | Number           | No       | `30000`                                      |
| `hs_call_from_number`   | Caller's phone number.                                                                                            | String           | No       | "+15551234567"                              |
| `hs_call_recording_url` | URL of the call recording (HTTPS only, .mp3 or .wav).                                                            | String           | No       | "https://example.com/recording.mp3"         |
| `hs_call_status`        | Call status ("BUSY", "CALLING_CRM_USER", "CANCELED", "COMPLETED", "CONNECTING", "FAILED", "IN_PROGRESS", "NO_ANSWER", "QUEUED", "RINGING"). | String           | No       | "COMPLETED"                                 |
| `hs_call_title`         | Call title.                                                                                                       | String           | No       | "Sales Call"                                |
| `hs_call_source`        | Call source. Required for recording/transcription pipeline; set to "INTEGRATIONS_PLATFORM".                      | String           | No       | "INTEGRATIONS_PLATFORM"                     |
| `hs_call_to_number`     | Recipient's phone number.                                                                                        | String           | No       | "+15559876543"                              |
| `hubspot_owner_id`      | ID of the call's owner.                                                                                           | String           | No       | `1234567`                                   |
| `hs_activity_type`      | Type of call (based on HubSpot account settings).                                                                 | String           | No       | "Outbound Call"                            |
| `hs_attachment_ids`     | IDs of attached files (semicolon-separated).                                                                     | String           | No       | "1;2;3"                                      |


**Default `hs_call_disposition` GUIDs:**

* Busy: `9d9162e7-6cf3-4944-bf63-4dff82258764`
* Connected: `f240bbac-87c9-4f6e-bf70-924b57d47db7`
* Left live message: `a4c4c377-d246-4b32-a13b-75a56a4cd0ff`
* Left voicemail: `b2cf5968-551e-4856-9783-52b3da59a7d0`
* No answer: `73a0d17f-1163-4015-bdd5-ec830791da20`
* Wrong number: `17b47fee-58de-441e-a44c-c6300d46f273`

**Associations:** (Optional)  Array of objects to associate the call with other HubSpot records.

| Field    | Description                                                   | Type     | Example     |
|----------|---------------------------------------------------------------|----------|-------------|
| `to.id`  | ID of the record to associate.                               | String   | `500`       |
| `types`  | Array of association types.                                  | Array    | `[{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 194 }]` |


**Example Request:**

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27T12:00:00Z",
    "hs_call_title": "Customer Support",
    "hubspot_owner_id": "12345",
    "hs_call_body": "Issue resolved successfully.",
    "hs_call_duration": 60000,
    "hs_call_from_number": "+15555551212",
    "hs_call_to_number": "+15555551213",
    "hs_call_status": "COMPLETED"
  },
  "associations": [
    {
      "to": { "id": 67890 },
      "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 194 } ]
    }
  ]
}
```

**Response:** (On success) JSON object containing the created call's details, including its `id`.


## 2. Retrieve Calls (GET)

**Endpoint:** `/crm/v3/objects/calls`  (for a list) or `/crm/v3/objects/calls/{callId}` (for a single call)

**Method:** `GET`

**Parameters (for list):**

| Parameter  | Description                                           | Type   |
|------------|-------------------------------------------------------|--------|
| `limit`    | Maximum number of results per page.                  | Integer |
| `properties` | Comma-separated list of properties to return.           | String |
| `associations` | Comma-separated list of object types for associated IDs.|String |

**Parameters (for single call):**

| Parameter  | Description                                           | Type   |
|------------|-------------------------------------------------------|--------|
| `properties` | Comma-separated list of properties to return.           | String |
| `associations` | Comma-separated list of object types for associated IDs.|String |


**Example Request (Single Call):** `/crm/v3/objects/calls/12345?properties=hs_call_title,hs_call_duration`

**Example Response (Single Call):**

```json
{
  "id": "12345",
  "properties": {
    "hs_call_title": "Sales Call",
    "hs_call_duration": 120000
  }
}
```


## 3. Update a Call (PATCH)

**Endpoint:** `/crm/v3/objects/calls/{callId}`

**Method:** `PATCH`

**Request Body:** JSON object with `properties` object containing the fields to update.  HubSpot ignores read-only and non-existent properties.  Use empty strings to clear property values.


**Example Request:**

```json
{
  "properties": {
    "hs_call_body": "Added follow-up notes.",
    "hs_call_status": "COMPLETED"
  }
}
```


## 4. Associate Existing Calls with Records (PUT)

**Endpoint:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `PUT`

**Path Parameters:**

* `callId`: ID of the call.
* `toObjectType`: Type of object to associate (e.g., "contact", "company").
* `toObjectId`: ID of the object to associate.
* `associationTypeId`: Association type ID (obtainable via the Associations API).


**Example URL:** `/crm/v3/objects/calls/12345/associations/contact/67890/194`


## 5. Remove an Association (DELETE)

**Endpoint:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `DELETE`


## 6. Pin a Call on a Record

This is achieved indirectly by including the call's `id` in the `hs_pinned_engagement_id` field when creating or updating a record (contact, company, deal, etc.) using the respective object APIs.


## 7. Delete a Call (DELETE)

**Endpoint:** `/crm/v3/objects/calls/{callId}`

**Method:** `DELETE`


## Error Handling

The API returns standard HTTP status codes to indicate success or failure.  Error responses will include detailed error messages in the body.  Refer to HubSpot's API documentation for details.


This documentation provides a concise overview.  Consult HubSpot's official API reference for the most up-to-date information, including details on batch operations and advanced features.
