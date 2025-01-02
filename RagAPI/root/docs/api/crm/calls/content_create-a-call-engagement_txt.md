# HubSpot Calls API Documentation

This document describes the HubSpot Calls API, allowing you to manage calls within the HubSpot CRM.  The API uses standard HTTP methods (POST, GET, PATCH, DELETE) and JSON for data exchange.  All endpoints are located under the `/crm/v3/objects/calls` base path.

## API Endpoints

All endpoints below use the base URL: `https://api.hubspot.com/crm/v3/objects/calls`

### 1. Create a Call Engagement (POST)

**Endpoint:** `/crm/v3/objects/calls`

**Method:** `POST`

**Request Body:**  JSON object with `properties` and optional `associations` objects.

**Properties:**

| Field                 | Description                                                                                                                                 | Type             | Required | Example                                     |
|----------------------|---------------------------------------------------------------------------------------------------------------------------------------------|-----------------|----------|---------------------------------------------|
| `hs_timestamp`       | Call creation time (Unix timestamp in milliseconds or UTC format). Determines timeline position.                                          | String/Number    | Yes      | `1679000000000` or `"2023-03-15T10:00:00Z"` |
| `hs_call_body`       | Call description and notes.                                                                                                                | String           | No       | "Discussed project X"                       |
| `hs_call_callee_object_id` | ID of the HubSpot record associated with the call (recipient for outbound, dialer for inbound).                                            | String           | No       | `12345`                                      |
| `hs_call_callee_object_type` | Object type of the associated record (e.g., "contact", "company").                                                                      | String           | No       | "contact"                                   |
| `hs_call_direction`  | Call direction ("INBOUND" or "OUTBOUND").                                                                                                 | String           | No       | "OUTBOUND"                                 |
| `hs_call_disposition` | Call outcome (use internal GUID; see below for defaults, or use the properties API for custom values).                                      | String           | No       | `"9d9162e7-6cf3-4944-bf63-4dff82258764"` (Busy) |
| `hs_call_duration`   | Call duration in milliseconds.                                                                                                             | Number           | No       | `360000`                                    |
| `hs_call_from_number`| Phone number the call originated from.                                                                                                      | String           | No       | "+15551234567"                             |
| `hs_call_recording_url` | URL of the call recording (HTTPS only, .mp3 or .wav).                                                                                     | String           | No       | "https://example.com/recording.mp3"         |
| `hs_call_status`     | Call status ("BUSY", "CALLING_CRM_USER", "CANCELED", "COMPLETED", "CONNECTING", "FAILED", "IN_PROGRESS", "NO_ANSWER", "QUEUED", "RINGING"). | String           | No       | "COMPLETED"                                 |
| `hs_call_title`      | Call title.                                                                                                                            | String           | No       | "Sales Call"                               |
| `hs_call_source`     | Call source. Required for recording/transcription pipeline; set to "INTEGRATIONS_PLATFORM".                                             | String           | No       | "INTEGRATIONS_PLATFORM"                     |
| `hs_call_to_number`  | Phone number the call was received by.                                                                                                  | String           | No       | "+15559876543"                             |
| `hubspot_owner_id`   | ID of the call owner.                                                                                                                      | String           | No       | `1234567`                                   |
| `hs_activity_type`   | Type of call (based on call types in your HubSpot account).                                                                                  | String           | No       | "Outbound Call"                            |
| `hs_attachment_ids`  | IDs of attached files (semicolon-separated).                                                                                             | String           | No       | "123;456"                                   |


**Associations:**

| Field       | Description                                                                                | Type    |
|-------------|--------------------------------------------------------------------------------------------|---------|
| `to`        | Object to associate ( `{id: <object_id>}` )                                              | Object  |
| `types`     | Association type (`{associationCategory: "HUBSPOT_DEFINED", associationTypeId: <id>}`) | Array   |


**Example Request:**

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27T12:00:00Z",
    "hs_call_title": "New Customer Call",
    "hubspot_owner_id": "12345",
    "hs_call_to_number": "+15555551212"
  },
  "associations": [
    {
      "to": {"id": 67890},
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 194}]
    }
  ]
}
```

**Response:**  Standard HubSpot API response including the newly created call's `id`.


### 2. Retrieve Calls (GET)

**Endpoint:** `/crm/v3/objects/calls`  (for all calls) or `/crm/v3/objects/calls/{callId}` (for a single call)

**Method:** `GET`

**Parameters (for all calls):**

| Parameter | Description                                     | Type    |
|-----------|-------------------------------------------------|---------|
| `limit`    | Max results per page.                          | Integer |
| `properties` | Comma-separated list of properties to return. | String  |
| `associations` | Comma-separated list of association types to return. | String |


**Parameters (for a single call):**

| Parameter | Description                                     | Type    |
|-----------|-------------------------------------------------|---------|
| `properties` | Comma-separated list of properties to return. | String  |
| `associations` | Comma-separated list of association types to return. | String |


**Response:** JSON array of calls (or a single call object).


### 3. Update a Call (PATCH)

**Endpoint:** `/crm/v3/objects/calls/{callId}`

**Method:** `PATCH`

**Request Body:** JSON object with the `properties` to update.  Omit properties to leave them unchanged. An empty string (`""`) will clear a property.

**Example Request:**

```json
{
  "properties": {
    "hs_call_body": "Follow up scheduled"
  }
}
```

**Response:** Standard HubSpot API response.


### 4. Associate Existing Calls with Records (PUT)

**Endpoint:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `PUT`

**Parameters:**

* `{callId}`: ID of the call.
* `{toObjectType}`: Object type to associate (e.g., "contact").
* `{toObjectId}`: ID of the object to associate.
* `{associationTypeId}`: Association type ID.


**Response:** Standard HubSpot API response.


### 5. Remove an Association (DELETE)

**Endpoint:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `DELETE`

**Parameters:**  Same as in section 4.

**Response:** Standard HubSpot API response.


### 6. Delete a Call (DELETE)

**Endpoint:** `/crm/v3/objects/calls/{callId}`

**Method:** `DELETE`

**Response:** Standard HubSpot API response.


##  Default `hs_call_disposition` GUIDs:

* Busy: `9d9162e7-6cf3-4944-bf63-4dff82258764`
* Connected: `f240bbac-87c9-4f6e-bf70-924b57d47db7`
* Left live message: `a4c4c377-d246-4b32-a13b-75a56a4cd0ff`
* Left voicemail: `b2cf5968-551e-4856-9783-52b3da59a7d0`
* No answer: `73a0d17f-1163-4015-bdd5-ec830791da20`
* Wrong number: `17b47fee-58de-441e-a44c-c6300d46f273`

Remember to replace placeholder values (IDs, object types, etc.) with your actual data.  Consult the HubSpot API documentation for details on error handling and authentication.
