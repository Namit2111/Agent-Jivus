# HubSpot Calls API Documentation

This document details the HubSpot API endpoints for managing call engagements.  The API allows you to log, manage, and retrieve call information associated with CRM records.

## Calls Endpoint Reference

The primary endpoint for managing calls is `/crm/v3/objects/calls`.  This endpoint supports various HTTP methods for different operations.  For a complete list of available endpoints and their requirements, refer to the "Endpoints" tab (not included in the provided text).


## API Methods

### 1. Create a Call Engagement (POST /crm/v3/objects/calls)

This method creates a new call engagement in HubSpot.  The request body requires a `properties` object and optionally an `associations` object.

**Request Body:**

*   **`properties` (object):** Contains details about the call.  See the "Properties" section below for a list of available fields.  `hs_timestamp` is a required field.
*   **`associations` (array, optional):**  An array of objects to associate the call with existing HubSpot records (e.g., contacts, companies). See the "Associations" section below.

**Properties:**

| Field                   | Description                                                                                                                                                                                             |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `hs_timestamp`          | **Required.** Call creation timestamp (Unix timestamp in milliseconds or UTC format).                                                                                                                  |
| `hs_call_body`          | Call description and notes.                                                                                                                                                                      |
| `hs_call_callee_object_id` | ID of the HubSpot record associated with the call (recipient for outbound, dialer for inbound).                                                                                                    |
| `hs_call_callee_object_type` | Object type of the associated record (e.g., `contact`, `company`).                                                                                                                            |
| `hs_call_direction`     | Call direction (`INBOUND` or `OUTBOUND`).                                                                                                                                                         |
| `hs_call_disposition`   | Call outcome. Use internal GUID value.  Default values include:  Busy (9d9162e7-6cf3-4944-bf63-4dff82258764), Connected (f240bbac-87c9-4f6e-bf70-924b57d47db7), Left live message (a4c4c377-d246-4b32-a13b-75a56a4cd0ff), Left voicemail (b2cf5968-551e-4856-9783-52b3da59a7d0), No answer (73a0d17f-1163-4015-bdd5-ec830791da20), Wrong number (17b47fee-58de-441e-a44c-c6300d46f273). Custom values can be obtained via the properties API. |
| `hs_call_duration`      | Call duration in milliseconds.                                                                                                                                                                     |
| `hs_call_from_number`   | Caller's phone number.                                                                                                                                                                         |
| `hs_call_recording_url` | URL of the call recording (HTTPS only, .mp3 or .wav).                                                                                                                                             |
| `hs_call_status`        | Call status (BUSY, CALLING_CRM_USER, CANCELED, COMPLETED, CONNECTING, FAILED, IN_PROGRESS, NO_ANSWER, QUEUED, RINGING).                                                                   |
| `hs_call_title`         | Call title.                                                                                                                                                                                       |
| `hs_call_source`        | Call source.  Required for recording and transcriptions pipeline; must be `INTEGRATIONS_PLATFORM` if set.                                                                                       |
| `hs_call_to_number`     | Recipient's phone number.                                                                                                                                                                         |
| `hubspot_owner_id`      | ID of the call owner.                                                                                                                                                                              |
| `hs_activity_type`      | Type of call (based on call types in your HubSpot account).                                                                                                                                        |
| `hs_attachment_ids`     | IDs of call attachments (semicolon-separated).                                                                                                                                                     |


**Associations:**

| Field          | Description                                                                                                             |
| --------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `to.id`        | ID of the record to associate with the call.                                                                             |
| `types[0].associationCategory` | Association category (`HUBSPOT_DEFINED`).                                                                            |
| `types[0].associationTypeId`    | Association type ID (default IDs are listed in the documentation, custom IDs can be retrieved via the associations API). |


### 2. Retrieve Calls (GET /crm/v3/objects/calls/{callId} or GET /crm/v3/objects/calls)

*   **Individual Call (GET /crm/v3/objects/calls/{callId}):** Retrieves a single call by its ID.  Supports `properties` and `associations` parameters to specify the returned fields.
*   **All Calls (GET /crm/v3/objects/calls):** Retrieves a list of calls.  Supports `limit` and `properties` parameters.

**Parameters:**

*   `properties` (string): Comma-separated list of properties to return.
*   `associations` (string): Comma-separated list of object types to retrieve associated IDs for.
*   `limit` (integer): Maximum number of results per page (for GET /crm/v3/objects/calls).


### 3. Identify Voicemails vs. Recorded Calls

To distinguish between recorded calls and voicemails, check the `hs_call_status` and `hs_call_has_voicemail` properties.  A voicemail will have `hs_call_status: missed` and `hs_call_has_voicemail: true`.


### 4. Update Calls (PATCH /crm/v3/objects/calls/{callId})

Updates an existing call.  The request body contains the `properties` object with fields to update.  HubSpot ignores read-only and non-existent properties.  An empty string clears a property value.


### 5. Associate Existing Calls with Records (PUT /crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId})

Associates a call with a record.

**Parameters:**

*   `callId`
*   `toObjectType` (e.g., `contact`, `company`)
*   `toObjectId`
*   `associationTypeId`


### 6. Remove an Association (DELETE /crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId})

Removes an association between a call and a record. Uses the same URL as the associate method.


### 7. Pin a Call on a Record

Pins a call to the top of a record's timeline using the `hs_pinned_engagement_id` field when creating or updating the record via object APIs (companies, contacts, deals, tickets, custom objects).


### 8. Delete Calls (DELETE /crm/v3/objects/calls/{callId})

Deletes a call (moves it to the recycling bin).


All batch operations (create, update, delete, retrieve) are mentioned but the specifics are not detailed in the provided text; refer to the "Endpoints" tab for further details.
