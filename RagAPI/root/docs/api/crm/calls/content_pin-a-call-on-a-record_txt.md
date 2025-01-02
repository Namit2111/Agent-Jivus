# HubSpot Calls API Documentation

This document details the HubSpot Calls API, allowing you to manage calls within the HubSpot CRM.  It covers creating, retrieving, updating, associating, and deleting calls.

## API Endpoint Base URL

All API endpoints begin with: `/crm/v3/objects/calls`


## 1. Create a Call Engagement

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/calls`

**Request Body:**  The request body contains a `properties` object and optionally an `associations` object.

**Properties Object:**

| Field                 | Description                                                                                                                               | Type             | Required | Example                                    |
|-----------------------|-------------------------------------------------------------------------------------------------------------------------------------------|-----------------|----------|---------------------------------------------|
| `hs_timestamp`        | Call creation time (Unix timestamp in milliseconds or UTC format).                                                                       | String/Number    | Yes      | `1679000000000` or `"2023-03-17T01:32:44.872Z"` |
| `hs_call_body`        | Call description and notes.                                                                                                              | String           | No       | "Discussed project X"                       |
| `hs_call_callee_object_id` | ID of the HubSpot record associated with the call (recipient for outbound, dialer for inbound).                                         | String           | No       | `12345`                                     |
| `hs_call_callee_object_type` | Type of the associated record (e.g., "contact", "company").                                                                            | String           | No       | "contact"                                   |
| `hs_call_direction`   | Call direction ("INBOUND" or "OUTBOUND").                                                                                           | String           | No       | "OUTBOUND"                                 |
| `hs_call_disposition` | Call outcome (use internal GUID; see below for defaults).  Custom outcomes require fetching GUIDs via the properties API.                | String           | No       | `"9d9162e7-6cf3-4944-bf63-4dff82258764"` (Busy) |
| `hs_call_duration`    | Call duration in milliseconds.                                                                                                           | String/Number    | No       | `360000`                                    |
| `hs_call_from_number` | Phone number the call originated from.                                                                                                 | String           | No       | "+15551234567"                             |
| `hs_call_recording_url` | URL of the call recording (HTTPS only, .mp3 or .wav).                                                                                   | String           | No       | "https://example.com/recording.mp3"        |
| `hs_call_status`      | Call status ("BUSY", "CALLING_CRM_USER", "CANCELED", "COMPLETED", "CONNECTING", "FAILED", "IN_PROGRESS", "NO_ANSWER", "QUEUED", "RINGING"). | String           | No       | "COMPLETED"                                |
| `hs_call_title`       | Call title.                                                                                                                            | String           | No       | "Sales Call"                               |
| `hs_call_source`      | Call source ("INTEGRATIONS_PLATFORM" if using recording/transcription pipeline).                                                      | String           | No       | "INTEGRATIONS_PLATFORM"                     |
| `hs_call_to_number`   | Phone number the call was received on.                                                                                                | String           | No       | "+15559876543"                             |
| `hubspot_owner_id`    | ID of the call owner (HubSpot user).                                                                                                  | String           | No       | `1234567`                                  |
| `hs_activity_type`    | Type of call (based on call types in your HubSpot account).                                                                             | String           | No       | "Outbound Call"                           |
| `hs_attachment_ids`   | IDs of call attachments (semicolon-separated).                                                                                       | String           | No       | "123;456"                                   |


**Associations Object:** (Optional)

Used to associate the call with existing HubSpot records.

| Field       | Description                                                                         | Type          | Required | Example                                     |
|-------------|-------------------------------------------------------------------------------------|---------------|----------|---------------------------------------------|
| `to`        | Object to associate (ID).                                                         | Object        | Yes      | `{"id": 500}`                              |
| `types`     | Association type (category and ID; see below).                                   | Array         | Yes      | `[{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 194}]` |


**Example Request (with Associations):**

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27T12:00:00Z",
    "hs_call_title": "Client Check-in",
    "hubspot_owner_id": "12345",
    "hs_call_body": "Discussed next steps",
    "hs_call_duration": 60000,
    "hs_call_from_number": "+15551112222",
    "hs_call_to_number": "+15553334444",
    "hs_call_status": "COMPLETED"
  },
  "associations": [
    {
      "to": {"id": 67890},
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 194}]
    }
  ]
}
```

**Response:**  A JSON object containing the created call's details, including the `callId`.


## 2. Retrieve Calls

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/calls` (for all calls) or `/crm/v3/objects/calls/{callId}` (for a specific call)

**Parameters:**

| Parameter     | Description                                           | Type    |
|---------------|-------------------------------------------------------|---------|
| `callId`      | (For single call retrieval) ID of the call to retrieve. | String  |
| `limit`       | Maximum number of results per page (for all calls).   | Integer |
| `properties`  | Comma-separated list of properties to return.         | String  |
| `associations`| Comma-separated list of object types to retrieve associated IDs for. | String  |


**Example Request (all calls, limit 10):**

`/crm/v3/objects/calls?limit=10&properties=hs_call_title,hs_call_duration`

**Example Request (single call):**

`/crm/v3/objects/calls/12345?properties=hs_call_title,hs_call_duration,associations=contact`


**Response:** A JSON object or array of JSON objects containing call details.


## 3. Update Calls

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/calls/{callId}`

**Request Body:**  A `properties` object containing the properties to update.  Omit properties to keep their current values.  An empty string (`""`) will clear a property's value.

**Example Request:**

```json
{
  "properties": {
    "hs_call_body": "Added follow-up notes"
  }
}
```

**Response:** A JSON object containing the updated call's details.


## 4. Associate Existing Calls with Records

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Parameters:**

| Parameter       | Description                                         | Type    |
|-----------------|-----------------------------------------------------|---------|
| `callId`         | ID of the call.                                     | String  |
| `toObjectType`   | Type of object to associate (e.g., "contact", "company"). | String  |
| `toObjectId`     | ID of the object to associate.                       | String  |
| `associationTypeId` | ID of the association type.                        | String/Integer |


**Example URL:**

`/crm/v3/objects/calls/12345/associations/contact/67890/194`


**Response:**  A success or error message.


## 5. Remove an Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Parameters:** (Same as Associate Existing Calls)

**Response:** A success or error message.


## 6. Pin a Call on a Record

Pinning is accomplished by including the call's `id` in the `hs_pinned_engagement_id` field when creating or updating a record via the relevant object APIs (contacts, companies, etc.).


## 7. Delete Calls

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/calls/{callId}`

**Response:** A success or error message.


## Default `hs_call_disposition` GUIDs:

* Busy: `9d9162e7-6cf3-4944-bf63-4dff82258764`
* Connected: `f240bbac-87c9-4f6e-bf70-924b57d47db7`
* Left live message: `a4c4c377-d246-4b32-a13b-75a56a4cd0ff`
* Left voicemail: `b2cf5968-551e-4856-9783-52b3da59a7d0`
* No answer: `73a0d17f-1163-4015-bdd5-ec830791da20`
* Wrong number: `17b47fee-58de-441e-a44c-c6300d46f273`


This documentation provides a comprehensive overview.  Refer to the HubSpot API documentation for complete details on all endpoints, error handling, and rate limits.  Remember to replace placeholder IDs with your actual HubSpot IDs.
