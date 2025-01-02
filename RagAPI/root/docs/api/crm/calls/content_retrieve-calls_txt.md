# HubSpot Calls API Documentation

This document details the HubSpot Calls API, allowing you to manage calls within the HubSpot CRM.  The API uses standard HTTP methods (POST, GET, PATCH, DELETE) and JSON for data exchange.  All endpoints are located under the `/crm/v3/objects/calls` base path.

## 1. Create a Call Engagement

**Endpoint:** `/crm/v3/objects/calls`

**Method:** `POST`

**Request Body:**

The request body is a JSON object containing two key fields: `properties` and (optionally) `associations`.

* **`properties` (object):** Contains the call details.  Required fields are marked with an asterisk (*).

    | Field                 | Description                                                                                                                                    | Data Type       | Example                                   |
    |----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|--------------------------------------------|
    | `hs_timestamp`*      | Call creation timestamp (Unix timestamp in milliseconds or UTC format). Determines timeline placement.                                             | string           | `1679068800000` or `2023-03-17T00:00:00Z` |
    | `hs_call_body`       | Call description and notes.                                                                                                                     | string           | "Discussed project X"                      |
    | `hs_call_callee_object_id` | ID of the associated HubSpot record (contact, company, etc.). Recipient for outbound, dialer for inbound calls.                                    | string           | `12345`                                  |
    | `hs_call_callee_object_type` | Type of the associated HubSpot record (e.g., `contact`, `company`). Recipient object for outbound, dialer object for inbound calls.           | string           | `contact`                               |
    | `hs_call_direction`  | Call direction (`INBOUND` or `OUTBOUND`) from the HubSpot user's perspective.                                                                | string           | `OUTBOUND`                               |
    | `hs_call_disposition` | Call outcome (use internal GUID).  See default values below.  Custom values can be obtained via the properties API.                           | string           | `9d9162e7-6cf3-4944-bf63-4dff82258764` (Busy) |
    | `hs_call_duration`   | Call duration in milliseconds.                                                                                                                 | string           | `360000`                                 |
    | `hs_call_from_number` | Caller's phone number.                                                                                                                         | string           | `(555) 123-4567`                          |
    | `hs_call_recording_url` | URL of the call recording (HTTPS only, .mp3 or .wav).                                                                                       | string           | `https://example.com/recording.mp3`       |
    | `hs_call_status`     | Call status (`BUSY`, `CALLING_CRM_USER`, `CANCELED`, `COMPLETED`, `CONNECTING`, `FAILED`, `IN_PROGRESS`, `NO_ANSWER`, `QUEUED`, `RINGING`). | string           | `COMPLETED`                              |
    | `hs_call_title`      | Call title.                                                                                                                                  | string           | "Sales Call"                             |
    | `hs_call_source`     | Call source (required for recording and transcription pipeline). Set to `INTEGRATIONS_PLATFORM` if used.                                     | string           | `INTEGRATIONS_PLATFORM`                   |
    | `hs_call_to_number`  | Recipient's phone number.                                                                                                                     | string           | `(555) 987-6543`                          |
    | `hubspot_owner_id`   | ID of the call owner (HubSpot user).                                                                                                        | string           | `1234567`                                 |
    | `hs_activity_type`   | Type of call (based on call types in your HubSpot account).                                                                                   | string           | "Outbound Sales Call"                     |
    | `hs_attachment_ids`  | IDs of call attachments (semicolon-separated).                                                                                             | string           | `1;2;3`                                   |

    **Default `hs_call_disposition` GUIDs:**

    * Busy: `9d9162e7-6cf3-4944-bf63-4dff82258764`
    * Connected: `f240bbac-87c9-4f6e-bf70-924b57d47db7`
    * Left live message: `a4c4c377-d246-4b32-a13b-75a56a4cd0ff`
    * Left voicemail: `b2cf5968-551e-4856-9783-52b3da59a7d0`
    * No answer: `73a0d17f-1163-4015-bdd5-ec830791da20`
    * Wrong number: `17b47fee-58de-441e-a44c-c6300d46f273`


* **`associations` (array, optional):**  Associates the call with existing HubSpot records.

    | Field       | Description                                                                        | Data Type     | Example                                      |
    |-------------|------------------------------------------------------------------------------------|----------------|-------------------------------------------------|
    | `to`        | Object to associate (contains `id` field).                                       | object         | `{"id": 500}`                                 |
    | `types`     | Association type (contains `associationCategory` and `associationTypeId`).          | array of objects | `[{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 194}]` |


**Example Request:**

```json
{
  "properties": {
    "hs_timestamp": "1679068800000",
    "hs_call_title": "Sales Call",
    "hubspot_owner_id": "1234567",
    "hs_call_body": "Initial contact",
    "hs_call_direction": "OUTBOUND",
    "hs_call_status": "COMPLETED",
    "hs_call_from_number": "+15551234567",
    "hs_call_to_number": "+15559876543"
  },
  "associations": [
    {
      "to": {"id": 500},
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 194}]
    }
  ]
}
```

**Response:** A JSON object representing the created call, including its `id`.


## 2. Retrieve Calls

**Endpoint:** `/crm/v3/objects/calls` (for multiple calls) or `/crm/v3/objects/calls/{callId}` (for a single call)

**Method:** `GET`

**Parameters (for multiple calls):**

* `limit`: Maximum number of results per page.
* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.

**Parameters (for a single call):**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.

**Example Request (single call):**

`/crm/v3/objects/calls/123?properties=hs_call_title,hs_call_duration`

**Response:**  A JSON object (single call) or an array of JSON objects (multiple calls), each representing a call with specified properties.


## 3. Update Calls

**Endpoint:** `/crm/v3/objects/calls/{callId}`

**Method:** `PATCH`

**Request Body:** JSON object with `properties` field containing the updated properties.  Omit properties to leave them unchanged.  An empty string will clear a property value.

**Example Request:**

```json
{
  "properties": {
    "hs_call_body": "Added additional notes"
  }
}
```

**Response:**  A JSON object representing the updated call.


## 4. Associate Existing Calls with Records

**Endpoint:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `PUT`

**Parameters:**

* `callId`: The ID of the call.
* `toObjectType`: Type of object to associate (e.g., `contact`, `company`).
* `toObjectId`: ID of the object to associate.
* `associationTypeId`: Association type ID (obtainable via the associations API).

**Example Request:**

`/crm/v3/objects/calls/123/associations/contact/456/194`


## 5. Remove an Association

**Endpoint:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `DELETE`

**Parameters:** Same as associating calls.


## 6. Pin a Call on a Record

This is done indirectly by including the call's `id` in the `hs_pinned_engagement_id` field when creating or updating a record via other HubSpot object APIs (contacts, companies, deals, etc.).


## 7. Delete Calls

**Endpoint:** `/crm/v3/objects/calls/{callId}`

**Method:** `DELETE`

**Parameters:** `callId` - The ID of the call to delete.

**Response:**  Confirmation of deletion.  Calls are moved to the recycling bin; they can be restored later.


## Error Handling

The API will return standard HTTP status codes to indicate success or failure. Error responses will typically include a JSON object detailing the error.

This documentation provides a concise overview. Refer to the HubSpot API documentation for a complete list of endpoints, parameters, and detailed error handling.
