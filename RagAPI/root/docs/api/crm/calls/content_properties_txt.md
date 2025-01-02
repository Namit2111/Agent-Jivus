# HubSpot Calls API Documentation

This document details the HubSpot Calls API, allowing you to log and manage calls within the HubSpot CRM.  You can interact with calls either directly within HubSpot or programmatically through this API.

## API Endpoints

All endpoints are under the base URL `/crm/v3/objects/calls`.  Replace `{callId}` with the specific call ID.

### 1. Create a Call Engagement (POST /crm/v3/objects/calls)

Creates a new call engagement.

**Request Body:**

The request body must include a `properties` object and optionally an `associations` object.

**Properties Object:**

| Field                 | Description                                                                                                          | Type             | Required | Example                                      |
|----------------------|----------------------------------------------------------------------------------------------------------------------|-----------------|----------|----------------------------------------------|
| `hs_timestamp`       | Call creation time (Unix timestamp in milliseconds or UTC format).                                                   | string/number   | Yes      | `1679088000000` or `"2023-03-17T00:00:00Z"` |
| `hs_call_body`       | Call description and notes.                                                                                            | string           | No       | "Discussed project X"                       |
| `hs_call_callee_object_id` | HubSpot ID of the record associated with the call (recipient for outbound, dialer for inbound).                         | string           | No       | `12345`                                     |
| `hs_call_callee_object_type` | Object type of the associated record (e.g., `contact`, `company`).                                                  | string           | No       | `contact`                                   |
| `hs_call_direction`  | Call direction (`INBOUND` or `OUTBOUND`).                                                                          | string           | No       | `OUTBOUND`                                  |
| `hs_call_disposition` | Call outcome (use internal GUID; see default values below).  Use the [properties API](link_to_properties_api) for custom values. | string           | No       | `9d9162e7-6cf3-4944-bf63-4dff82258764` (Busy)|
| `hs_call_duration`   | Call duration in milliseconds.                                                                                       | number           | No       | `360000` (6 minutes)                        |
| `hs_call_from_number` | Caller's phone number.                                                                                             | string           | No       | `(555) 123-4567`                             |
| `hs_call_recording_url` | URL of the call recording (HTTPS only, .mp3 or .wav).                                                            | string           | No       | `https://example.com/recording.mp3`          |
| `hs_call_status`     | Call status (`BUSY`, `CALLING_CRM_USER`, `CANCELED`, `COMPLETED`, `CONNECTING`, `FAILED`, `IN_PROGRESS`, `NO_ANSWER`, `QUEUED`, `RINGING`). | string           | No       | `COMPLETED`                                 |
| `hs_call_title`      | Call title.                                                                                                           | string           | No       | "Sales Call"                               |
| `hs_call_source`     | Call source (required for recording/transcription pipeline; use `INTEGRATIONS_PLATFORM`).                          | string           | No       | `INTEGRATIONS_PLATFORM`                     |
| `hs_call_to_number`   | Recipient's phone number.                                                                                           | string           | No       | `(555) 987-6543`                             |
| `hubspot_owner_id`   | ID of the call owner.                                                                                                 | string           | No       | `1234567`                                  |
| `hs_activity_type`   | Type of call (based on call types in your HubSpot account).                                                        | string           | No       |  "Sales Call"                              |
| `hs_attachment_ids`  | IDs of call attachments (semicolon-separated).                                                                     | string           | No       | "1;2;3"                                     |


**Default `hs_call_disposition` Values:**

* Busy: `9d9162e7-6cf3-4944-bf63-4dff82258764`
* Connected: `f240bbac-87c9-4f6e-bf70-924b57d47db7`
* Left live message: `a4c4c377-d246-4b32-a13b-75a56a4cd0ff`
* Left voicemail: `b2cf5968-551e-4856-9783-52b3da59a7d0`
* No answer: `73a0d17f-1163-4015-bdd5-ec830791da20`
* Wrong number: `17b47fee-58de-441e-a44c-c6300d46f273`


**Associations Object:**

(Optional) Associates the call with existing HubSpot records.

| Field       | Description                                                                   | Type    | Example                                  |
|-------------|-------------------------------------------------------------------------------|---------|-------------------------------------------|
| `to.id`     | ID of the record to associate.                                               | number  | `12345`                                 |
| `types`     | Array of association types.                                                   | array   | `[{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 194}]` |
| `types[].associationCategory` | Association category (`HUBSPOT_DEFINED`).                              | string  | `HUBSPOT_DEFINED`                         |
| `types[].associationTypeId` | Association type ID (see [Associations API](link_to_associations_api)). | number  | `194` (e.g., contact to call association) |


**Example Request (JSON):**

```json
{
  "properties": {
    "hs_timestamp": "2024-07-26T12:00:00Z",
    "hs_call_title": "Initial Contact",
    "hubspot_owner_id": "12345",
    "hs_call_from_number": "+15551234567",
    "hs_call_to_number": "+15559876543",
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

**Response (JSON):**  A successful response will contain the newly created call's properties, including the `callId`.


### 2. Retrieve Calls (GET /crm/v3/objects/calls)

Retrieves calls.  Can retrieve a single call by ID or a list of calls.

**Retrieving a Single Call (GET /crm/v3/objects/calls/{callId}):**

* **Parameters:**
    * `properties`: Comma-separated list of properties to return.
    * `associations`: Comma-separated list of object types to retrieve associated IDs for.

**Retrieving a List of Calls (GET /crm/v3/objects/calls):**

* **Parameters:**
    * `limit`: Maximum number of results per page.
    * `properties`: Comma-separated list of properties to return.


**Response (JSON):** An array of call objects for list requests; a single call object for individual call requests.


### 3. Update Calls (PATCH /crm/v3/objects/calls/{callId})

Updates an existing call.

**Request Body:**  A `properties` object containing the properties to update.  Omit properties to keep existing values.  Use an empty string to clear a property value.

**Example Request (JSON):**

```json
{
  "properties": {
    "hs_call_body": "Added follow-up notes"
  }
}
```

**Response (JSON):** The updated call object.


### 4. Associate Existing Calls with Records (PUT /crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId})

Associates a call with another HubSpot record.

* **Parameters:**
    * `callId`: The call's ID.
    * `toObjectType`: The type of object to associate (e.g., `contact`, `company`).
    * `toObjectId`: The ID of the object to associate.
    * `associationTypeId`: The ID of the association type.

**Response:** Success/failure indication.


### 5. Remove an Association (DELETE /crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId})

Removes an association between a call and another record.  Uses the same URL parameters as the associate endpoint.

**Response:** Success/failure indication.


### 6. Pin a Call (Update Record via Object APIs)

Pins a call to the top of a record's timeline.  This requires updating the record using the relevant object API (contacts, companies, etc.) and including the call's `id` in the `hs_pinned_engagement_id` field.


### 7. Delete Calls (DELETE /crm/v3/objects/calls/{callId})

Deletes a call (moves it to the recycle bin).

**Response:** Success/failure indication.


## Identifying Voicemails vs. Recorded Calls

To differentiate between recorded calls and voicemails, check the `hs_call_status` and `hs_call_has_voicemail` properties.  A voicemail will have `hs_call_status: missed` and `hs_call_has_voicemail: true`.


This documentation provides a concise overview. Refer to the HubSpot developer documentation for complete details and further examples.  Remember to replace placeholder values (IDs, URLs, etc.) with your actual data.  Ensure you have the necessary HubSpot API key and permissions.
