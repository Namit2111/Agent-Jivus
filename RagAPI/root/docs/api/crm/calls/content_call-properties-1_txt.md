# HubSpot API Guides: Engagements | Calls

This document details the HubSpot API endpoints for managing call engagements.  You can log calls within HubSpot or through the Calls API.  This guide covers basic methods; for a complete list of endpoints and requirements, refer to the "Endpoints" tab (presumably within the HubSpot application itself).

## Create a Call Engagement

Use a `POST` request to `/crm/v3/objects/calls`.

The request body requires a `properties` object containing call details and an optional `associations` object to link the call to existing records (e.g., contacts, companies).

### Properties

| Field                  | Description                                                                                                                                                                                          |
|-------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `hs_timestamp`         | **Required.** Call creation time. Use a Unix timestamp in milliseconds or UTC format.                                                                                                              |
| `hs_call_body`         | Call description and notes.                                                                                                                                                                     |
| `hs_call_callee_object_id` | ID of the HubSpot record associated with the call. For outbound calls, this is the recipient; for inbound calls, it's the dialer.                                                              |
| `hs_call_callee_object_type` | Object type of the associated record (e.g., `contact`, `company`). For outbound calls, this is the recipient's object type; for inbound calls, it's the dialer's object type.                       |
| `hs_call_direction`    | Call direction from the HubSpot user's perspective: `INBOUND` or `OUTBOUND`.                                                                                                              |
| `hs_call_disposition` | Call outcome. Use the internal GUID value.  Custom call outcomes' GUIDs can be found using [this API](link_to_api_needed). Default values: <br> `Busy`: `9d9162e7-6cf3-4944-bf63-4dff82258764`<br>`Connected`: `f240bbac-87c9-4f6e-bf70-924b57d47db7`<br>`Left live message`: `a4c4c377-d246-4b32-a13b-75a56a4cd0ff`<br>`Left voicemail`: `b2cf5968-551e-4856-9783-52b3da59a7d0`<br>`No answer`: `73a0d17f-1163-4015-bdd5-ec830791da20`<br>`Wrong number`: `17b47fee-58de-441e-a44c-c6300d46f273` |
| `hs_call_duration`     | Call duration in milliseconds.                                                                                                                                                                   |
| `hs_call_from_number`  | Calling phone number.                                                                                                                                                                        |
| `hs_call_recording_url` | URL of the call recording (.mp3 or .wav; HTTPS only).                                                                                                                                      |
| `hs_call_status`       | Call status: `BUSY`, `CALLING_CRM_USER`, `CANCELED`, `COMPLETED`, `CONNECTING`, `FAILED`, `IN_PROGRESS`, `NO_ANSWER`, `QUEUED`, `RINGING`.                                                   |
| `hs_call_title`        | Call title.                                                                                                                                                                               |
| `hs_call_source`       | Call source (required for recording/transcription pipeline). Set to `INTEGRATIONS_PLATFORM` if used.                                                                                      |
| `hs_call_to_number`    | Receiving phone number.                                                                                                                                                                        |
| `hubspot_owner_id`     | ID of the call's owner (determines the creator on the record timeline).                                                                                                                        |
| `hs_activity_type`     | Call type (based on your HubSpot account's call types).                                                                                                                                     |
| `hs_attachment_ids`    | IDs of call attachments (semicolon-separated).                                                                                                                                                 |


### Associations

Include an `associations` object to associate the call with existing records.

| Field      | Description                                                                                           |
|------------|-------------------------------------------------------------------------------------------------------|
| `to`       | Record to associate (specified by its `id`).                                                            |
| `types`    | Association type between the call and the record (`associationCategory` and `associationTypeId`).      |


**Example Request Body:**  (See example in the original text)


## Retrieve Calls

Retrieve calls individually or in bulk.

* **Individual call:** `GET /crm/v3/objects/calls/{callId}`.  Parameters: `properties` (comma-separated list), `associations` (comma-separated list of object types).

* **All calls:** `GET /crm/v3/objects/calls`. Parameters: `limit`, `properties`.


## Identify Voicemails vs. Recorded Calls

For recorded calls and voicemails, the recording is in `hs_call_recording_url`.  To differentiate between completed recorded calls and inbound calls with voicemails (requires inbound calling access), use `hs_call_status` and `hs_call_has_voicemail`.  A voicemail has `hs_call_status: missed` and `hs_call_has_voicemail: true`.


## Update Calls

Update individual calls using a `PATCH` request to `/crm/v3/objects/calls/{callId}`.  Include the properties to update in the request body.  (See example in original text). HubSpot ignores read-only and non-existent properties; use an empty string to clear a property value.

## Associate Existing Calls with Records

Use a `PUT` request to `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`.

| Field           | Description                                                                    |
|-----------------|--------------------------------------------------------------------------------|
| `callId`        | Call ID.                                                                       |
| `toObjectType`  | Object type to associate (e.g., `contact`, `company`).                          |
| `toObjectId`    | ID of the record to associate.                                                  |
| `associationTypeId` | Association type ID (numerical or snake case, retrievable via the associations API). |


## Remove an Association

Use a `DELETE` request to the same URL as above.


## Pin a Call on a Record

Pin a call (must be already associated) using the `hs_pinned_engagement_id` field when creating or updating a record via object APIs (companies, contacts, deals, tickets, custom objects).


## Delete Calls

Delete individual calls using a `DELETE` request to `/crm/v3/objects/calls/{callId}`.  This moves the call to the recycling bin; it can be restored later.
