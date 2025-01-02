# HubSpot Calls API Documentation

This document details the HubSpot Calls API, allowing you to manage calls within the HubSpot CRM.  The API uses standard HTTP methods (POST, GET, PATCH, PUT, DELETE) and JSON for data exchange.

## API Endpoints Base URL: `/crm/v3/objects/calls`

All API endpoints begin with this base URL.  Remember to replace placeholders like `{callId}`, `{toObjectId}`, and `{associationTypeId}` with actual values.

## 1. Create a Call Engagement (POST)

**Endpoint:** `/crm/v3/objects/calls`

**Method:** `POST`

**Request Body:**  JSON object with `properties` and optionally `associations` objects.

**Properties Object:**

| Field                     | Description                                                                                                                                                                       | Type             | Required | Example                                     |
|--------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|----------|---------------------------------------------|
| `hs_timestamp`           | Call creation timestamp (Unix timestamp in milliseconds or UTC format).                                                                                                            | String/Number    | Yes      | `1679011200000` (milliseconds) or `2023-03-15T12:00:00Z` (UTC) |
| `hs_call_body`           | Call description and notes.                                                                                                                                                        | String           | No       | `"Discussed project proposal"`               |
| `hs_call_callee_object_id` | ID of the HubSpot record associated with the call (recipient for outbound, dialer for inbound).                                                                                   | String           | No       | `"12345"`                                  |
| `hs_call_callee_object_type` | Type of the associated record (e.g., `contact`, `company`).                                                                                                                        | String           | No       | `"contact"`                               |
| `hs_call_direction`      | Call direction (`INBOUND` or `OUTBOUND`).                                                                                                                                        | String           | No       | `"OUTBOUND"`                              |
| `hs_call_disposition`    | Call outcome (use internal GUID).  See default values below.  Custom values obtainable via the properties API.                                                              | String           | No       | `"f240bbac-87c9-4f6e-bf70-924b57d47db7"` (Connected) |
| `hs_call_duration`       | Call duration in milliseconds.                                                                                                                                                     | String/Number    | No       | `"30000"`                                  |
| `hs_call_from_number`    | Caller's phone number.                                                                                                                                                           | String           | No       | `"+15551234567"`                           |
| `hs_call_recording_url`  | URL of the call recording (HTTPS only, .mp3 or .wav).                                                                                                                            | String           | No       | `"https://example.com/recording.mp3"`       |
| `hs_call_status`         | Call status (`BUSY`, `CALLING_CRM_USER`, `CANCELED`, `COMPLETED`, `CONNECTING`, `FAILED`, `IN_PROGRESS`, `NO_ANSWER`, `QUEUED`, `RINGING`).                                      | String           | No       | `"COMPLETED"`                              |
| `hs_call_title`          | Call title.                                                                                                                                                                  | String           | No       | `"Sales Call"`                             |
| `hs_call_source`         | Call source.  Required for recording/transcription pipeline. Set to `"INTEGRATIONS_PLATFORM"`.                                                                                   | String           | No       | `"INTEGRATIONS_PLATFORM"`                 |
| `hs_call_to_number`      | Recipient's phone number.                                                                                                                                                         | String           | No       | `"+15559876543"`                           |
| `hubspot_owner_id`       | ID of the call owner.                                                                                                                                                           | String           | No       | `"1234567"`                               |
| `hs_activity_type`       | Type of call (based on call types in your HubSpot account).                                                                                                                      | String           | No       | `"Outbound Call"`                         |
| `hs_attachment_ids`      | IDs of call attachments (semicolon-separated).                                                                                                                                    | String           | No       | `"1;2;3"`                                 |


**Default `hs_call_disposition` GUIDs:**

* Busy: `9d9162e7-6cf3-4944-bf63-4dff82258764`
* Connected: `f240bbac-87c9-4f6e-bf70-924b57d47db7`
* Left live message: `a4c4c377-d246-4b32-a13b-75a56a4cd0ff`
* Left voicemail: `b2cf5968-551e-4856-9783-52b3da59a7d0`
* No answer: `73a0d17f-1163-4015-bdd5-ec830791da20`
* Wrong number: `17b47fee-58de-441e-a44c-c6300d46f273`

**Associations Object (Optional):**

| Field       | Description                                                                                | Type    | Example       |
|-------------|--------------------------------------------------------------------------------------------|---------|----------------|
| `to`        | Object to associate (ID).                                                               | Object  | `{"id": 500}` |
| `types`     | Association type (category and ID).                                                       | Array   | See below     |

**Example `types` Array:**

```json
[
  {
    "associationCategory": "HUBSPOT_DEFINED",
    "associationTypeId": 194  // Example ID; retrieve from Associations API
  }
]
```

**Example Request:**

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27T10:00:00Z",
    "hs_call_title": "Customer Support",
    "hubspot_owner_id": "12345",
    "hs_call_body": "Issue resolved.",
    "hs_call_duration": "60000",
    "hs_call_from_number": "+15555551212",
    "hs_call_to_number": "+15555559876",
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

**Response:**  JSON object containing the created call's details, including the `callId`.


## 2. Retrieve Calls (GET)

**Endpoint:** `/crm/v3/objects/calls` (for all calls) or `/crm/v3/objects/calls/{callId}` (for a single call)

**Method:** `GET`

**Parameters (for all calls):**

| Parameter | Description                                   | Type    |
|-----------|-----------------------------------------------|---------|
| `limit`   | Max results per page.                         | Integer |
| `properties` | Comma-separated list of properties to return. | String  |
| `associations` | Comma-separated list of object types to retrieve associated IDs for. | String |


**Parameters (for single call):**

| Parameter | Description                                   | Type    |
|-----------|-----------------------------------------------|---------|
| `properties` | Comma-separated list of properties to return. | String  |
| `associations` | Comma-separated list of object types to retrieve associated IDs for. | String |


**Response:**  JSON object (or array for all calls) containing call details.


## 3. Update a Call (PATCH)

**Endpoint:** `/crm/v3/objects/calls/{callId}`

**Method:** `PATCH`

**Request Body:** JSON object with `properties` object containing the fields to update.  Omit fields to keep existing values.  Use an empty string to clear a field's value.

**Response:** JSON object containing the updated call's details.


## 4. Associate Existing Calls with Records (PUT)

**Endpoint:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `PUT`

**Path Parameters:**

| Parameter       | Description                                   | Type    |
|-----------------|-----------------------------------------------|---------|
| `callId`         | ID of the call.                               | String  |
| `toObjectType`   | Type of object to associate (e.g., `contact`). | String  |
| `toObjectId`     | ID of the object to associate.                | String  |
| `associationTypeId` | Unique association type ID.                   | String/Integer |


**Response:**  Success/failure indication.


## 5. Remove an Association (DELETE)

**Endpoint:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `DELETE`

**Path Parameters:** (Same as above)

**Response:** Success/failure indication.


## 6. Pin a Call on a Record

This is not a direct API call.  To pin a call, include its `id` in the `hs_pinned_engagement_id` field when creating or updating a record (contact, company, deal, ticket, etc.) via their respective object APIs.


## 7. Delete a Call (DELETE)

**Endpoint:** `/crm/v3/objects/calls/{callId}`

**Method:** `DELETE`

**Response:** Success/failure indication.


**Note:**  Batch operations (creating, retrieving, updating, deleting) are available via additional endpoints documented in the "Endpoints" tab (mentioned throughout the original text) of the HubSpot documentation.  This markdown provides a summary of the core functionalities. Remember to consult the official HubSpot API documentation for the most up-to-date information and complete details on error handling and rate limits.
