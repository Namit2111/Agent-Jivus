# HubSpot Calls API Documentation

This document details the HubSpot Calls API, allowing you to manage call engagements within the HubSpot CRM.  The API uses standard HTTP methods (POST, GET, PATCH, DELETE) and JSON for data exchange.  Authentication requires a HubSpot API key.


## API Endpoints

All endpoints are located under the `/crm/v3/objects/calls` base URL.


### 1. Create a Call Engagement (POST `/crm/v3/objects/calls`)

Creates a new call engagement in HubSpot.

**Request Body:**

The request body is a JSON object with two main sections: `properties` and `associations`.

* **`properties` (object):** Contains call details.  Required fields are marked with an asterisk (*).

    | Field                  | Description                                                                                                 | Type             | Example                                      |
    |-----------------------|-------------------------------------------------------------------------------------------------------------|-----------------|-----------------------------------------------|
    | `hs_timestamp`*       | Call creation timestamp (Unix timestamp in milliseconds or UTC format).                                     | string/number    | `1679076800000` or `"2023-03-17T00:00:00Z"` |
    | `hs_call_body`        | Call description and notes.                                                                                | string           | "Discussed project X"                         |
    | `hs_call_callee_object_id` | HubSpot ID of the record associated with the call (recipient for outbound, dialer for inbound).            | string           | `12345`                                      |
    | `hs_call_callee_object_type` | Object type of the associated record (e.g., `contact`, `company`).                                      | string           | `contact`                                     |
    | `hs_call_direction`*  | Call direction (`INBOUND` or `OUTBOUND`).                                                              | string           | `OUTBOUND`                                   |
    | `hs_call_disposition` | Call outcome (use internal GUID; see below for defaults).                                                | string           | `f240bbac-87c9-4f6e-bf70-924b57d47db7` (Connected) |
    | `hs_call_duration`    | Call duration in milliseconds.                                                                           | number           | `360000` (6 minutes)                        |
    | `hs_call_from_number` | Caller's phone number.                                                                                   | string           | `+15551234567`                              |
    | `hs_call_recording_url` | URL of the call recording (HTTPS only, `.mp3` or `.wav`).                                               | string           | `https://example.com/recording.mp3`           |
    | `hs_call_status`      | Call status (`BUSY`, `CALLING_CRM_USER`, `CANCELED`, `COMPLETED`, `CONNECTING`, `FAILED`, `IN_PROGRESS`, `NO_ANSWER`, `QUEUED`, `RINGING`). | string           | `COMPLETED`                                  |
    | `hs_call_title`       | Call title.                                                                                             | string           | "Sales Call"                                  |
    | `hs_call_source`      | Call source (required for recording/transcription pipeline; use `INTEGRATIONS_PLATFORM`).                 | string           | `INTEGRATIONS_PLATFORM`                       |
    | `hs_call_to_number`   | Recipient's phone number.                                                                               | string           | `+15559876543`                              |
    | `hubspot_owner_id`*   | HubSpot ID of the call owner.                                                                            | string           | `1234567`                                    |
    | `hs_activity_type`   | Type of call (based on HubSpot account settings).                                                        | string           |  "Sales Call"                               |
    | `hs_attachment_ids`  | IDs of attached files (semicolon-separated).                                                            | string           | "123;456"                                     |


    **Default `hs_call_disposition` GUIDs:**

    * Busy: `9d9162e7-6cf3-4944-bf63-4dff82258764`
    * Connected: `f240bbac-87c9-4f6e-bf70-924b57d47db7`
    * Left live message: `a4c4c377-d246-4b32-a13b-75a56a4cd0ff`
    * Left voicemail: `b2cf5968-551e-4856-9783-52b3da59a7d0`
    * No answer: `73a0d17f-1163-4015-bdd5-ec830791da20`
    * Wrong number: `17b47fee-58de-441e-a44c-c6300d46f273`

* **`associations` (array of objects):**  Associates the call with other HubSpot records.

    | Field       | Description                                                                | Type     | Example                               |
    |-------------|----------------------------------------------------------------------------|----------|---------------------------------------|
    | `to` (object)| Record to associate with (must include `id`).                           | object   | `{"id": 500}`                        |
    | `types` (array of objects) | Association type (must include `associationCategory` and `associationTypeId`). | array    | `[{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 194}]` |


**Example Request (using curl):**

```bash
curl -X POST \
  https://api.hubspot.com/crm/v3/objects/calls \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "properties": {
      "hs_timestamp": "2024-10-27T10:00:00Z",
      "hs_call_title": "New Customer Call",
      "hubspot_owner_id": "12345",
      "hs_call_body": "Initial consultation",
      "hs_call_direction": "OUTBOUND",
      "hs_call_disposition": "f240bbac-87c9-4f6e-bf70-924b57d47db7",
      "hs_call_duration": 60000,
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
  }'
```

**Response:**  A JSON object containing the newly created call's details, including its `id`.


### 2. Retrieve Calls (GET `/crm/v3/objects/calls` or GET `/crm/v3/objects/calls/{callId}`)

Retrieves call information.

* **Individual Call (GET `/crm/v3/objects/calls/{callId}`):** Retrieves a single call by its ID.

    **Parameters:**

    * `properties`: Comma-separated list of properties to return.
    * `associations`: Comma-separated list of object types to retrieve associated IDs for.

* **List of Calls (GET `/crm/v3/objects/calls`):** Retrieves a list of calls.

    **Parameters:**

    * `limit`: Maximum number of results per page.
    * `properties`: Comma-separated list of properties to return.


**Example Request (curl, individual call):**

```bash
curl -X GET \
  https://api.hubspot.com/crm/v3/objects/calls/12345 \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

**Response:** A JSON object containing the call details or a paginated list of calls.


### 3. Update a Call (PATCH `/crm/v3/objects/calls/{callId}`)

Updates an existing call.

**Request Body:**

A JSON object with a `properties` object containing the fields to update.  HubSpot ignores read-only and non-existent properties.  To clear a property, send an empty string.

**Example Request (curl):**

```bash
curl -X PATCH \
  https://api.hubspot.com/crm/v3/objects/calls/12345 \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{ "properties": { "hs_call_body": "Updated notes" } }'
```

**Response:** A JSON object containing the updated call details.


### 4. Associate Existing Calls with Records (PUT `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates a call with another HubSpot record.

**Parameters:**

* `callId`: The call's ID.
* `toObjectType`: The type of object (e.g., `contact`, `company`).
* `toObjectId`: The ID of the object to associate.
* `associationTypeId`: The association type ID (obtainable via the Associations API).


### 5. Remove an Association (DELETE `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Removes an association between a call and a record.  Uses the same URL as the association endpoint.


### 6. Pin a Call (Update Record via Object APIs)

Pins a call to the top of a record's timeline.  This is done by including the call's `id` in the `hs_pinned_engagement_id` field when updating the associated record (contact, company, etc.) using the respective object API.


### 7. Delete a Call (DELETE `/crm/v3/objects/calls/{callId}`)

Deletes a call (moves it to the recycling bin).


## Identifying Voicemails vs. Recorded Calls

To differentiate:

* Include `hs_call_status` and `hs_call_has_voicemail` in your GET request.
* If `hs_call_status` is `missed` and `hs_call_has_voicemail` is `true`, it's a voicemail.
* `hs_call_has_voicemail` will be `false` for a completed, recorded inbound call or `null` for other statuses.


## Error Handling

The API returns standard HTTP status codes to indicate success or failure.  Error responses will include details in the JSON body.


This documentation provides a concise overview.  Refer to the HubSpot Developer documentation for complete details and further information on batch operations and error handling.
