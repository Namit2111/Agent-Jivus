# HubSpot Calls API Documentation

This document details the HubSpot Calls API, allowing you to log and manage calls within the HubSpot CRM.  You can interact with calls via the HubSpot interface or directly through this API.

## Calls Endpoint Reference

The Calls API provides methods for creating, retrieving, updating, associating, and deleting call engagements.  For complete endpoint details and requirements, refer to the "Endpoints" tab (not included in provided text).


## 1. Create a Call Engagement

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/calls`

**Request Body:**

The request body requires a `properties` object containing call details and an optional `associations` object to link the call to existing records (e.g., contacts, companies).

### 1.1 Properties

| Field                     | Description                                                                                                                                                                                       |
|--------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `hs_timestamp`            | **Required.** Call creation timestamp. Use Unix timestamp (milliseconds) or UTC format.                                                                                                               |
| `hs_call_body`           | Call description and notes.                                                                                                                                                                    |
| `hs_call_callee_object_id` | ID of the HubSpot record associated with the call. Recipient for OUTBOUND calls, dialer for INBOUND calls.                                                                                       |
| `hs_call_callee_object_type` | Object type of the associated record (e.g., "contact", "company"). Recipient's object type for OUTBOUND, dialer's for INBOUND.                                                                        |
| `hs_call_direction`       | Call direction (INBOUND or OUTBOUND) from the HubSpot user's perspective.                                                                                                                         |
| `hs_call_disposition`     | Call outcome. Use internal GUID.  Default values: <br>Busy: `9d9162e7-6cf3-4944-bf63-4dff82258764` <br>Connected: `f240bbac-87c9-4f6e-bf70-924b57d47db7` <br>Left live message: `a4c4c377-d246-4b32-a13b-75a56a4cd0ff` <br>Left voicemail: `b2cf5968-551e-4856-9783-52b3da59a7d0` <br>No answer: `73a0d17f-1163-4015-bdd5-ec830791da20` <br>Wrong number: `17b47fee-58de-441e-a44c-c6300d46f273` |
| `hs_call_duration`        | Call duration in milliseconds.                                                                                                                                                                  |
| `hs_call_from_number`     | Caller's phone number.                                                                                                                                                                         |
| `hs_call_recording_url`   | URL of the call recording (HTTPS only, .mp3 or .wav).                                                                                                                                            |
| `hs_call_status`          | Call status (BUSY, CALLING_CRM_USER, CANCELED, COMPLETED, CONNECTING, FAILED, IN_PROGRESS, NO_ANSWER, QUEUED, RINGING).                                                                     |
| `hs_call_title`           | Call title.                                                                                                                                                                                   |
| `hs_call_source`          | Call source.  Required for recording and transcriptions pipeline; set to `INTEGRATIONS_PLATFORM`.                                                                                             |
| `hs_call_to_number`       | Recipient's phone number.                                                                                                                                                                        |
| `hubspot_owner_id`        | ID of the call owner (HubSpot user).                                                                                                                                                             |
| `hs_activity_type`        | Call type (based on your HubSpot account's call types).                                                                                                                                        |
| `hs_attachment_ids`       | IDs of call attachments (semicolon-separated).                                                                                                                                                      |


### 1.2 Associations

The `associations` object allows associating the call with existing records.

| Field          | Description                                                                                                                     |
|-----------------|----------------------------------------------------------------------------------------------------------------------------------|
| `to.id`         | ID of the record to associate.                                                                                                  |
| `types[].associationCategory` | Association category ("HUBSPOT_DEFINED").                                                                                    |
| `types[].associationTypeId`   | Association type ID (see default IDs or use the Associations API for custom types).                                          |


**Example Request Body:** (See provided example in the original text)


## 2. Retrieve Calls

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/calls` (for all calls) or `/crm/v3/objects/calls/{callId}` (for a single call)


**Parameters (for `/crm/v3/objects/calls`):**

| Parameter  | Description                                                                       |
|-------------|-----------------------------------------------------------------------------------|
| `limit`     | Maximum results per page.                                                        |
| `properties` | Comma-separated list of properties to return.                                  |


**Parameters (for `/crm/v3/objects/calls/{callId}`):**

| Parameter    | Description                                                                                                   |
|---------------|---------------------------------------------------------------------------------------------------------------|
| `properties`  | Comma-separated list of properties to return.                                                                |
| `associations`| Comma-separated list of object types to retrieve associated IDs for.  Non-existent associations are omitted. |


## 3. Identify Voicemails vs. Recorded Calls

To differentiate between recorded calls and voicemails (requires inbound calling access):

* Check `hs_call_status` (will be "missed" for voicemails).
* Check `hs_call_has_voicemail` (will be "true" for voicemails, "false" for recorded calls, or "null" for other statuses).


## 4. Update Calls

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/calls/{callId}`

**Request Body:**  Include the properties to update.  HubSpot ignores read-only and non-existent properties.  Use an empty string to clear a property value. (See provided example in the original text)


## 5. Associate Existing Calls with Records

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Parameters:**

| Field           | Description                                                                         |
|-----------------|-------------------------------------------------------------------------------------|
| `callId`         | ID of the call.                                                                    |
| `toObjectType`   | Object type to associate (e.g., "contact", "company").                             |
| `toObjectId`     | ID of the record to associate.                                                      |
| `associationTypeId` | Association type ID (numerical or snake_case; retrieve via the Associations API). |


## 6. Remove an Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`  (Same as associating)


## 7. Pin a Call on a Record

To pin a call to a record's timeline (only one activity per record), include the call's `id` in the `hs_pinned_engagement_id` field when creating or updating the record via the relevant object APIs (companies, contacts, deals, tickets, custom objects).


## 8. Delete Calls

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/calls/{callId}`

Deleted calls are moved to the recycling bin and can be restored.


This documentation provides a summary of the HubSpot Calls API. Refer to the  "Endpoints" tab (not included in provided text) for complete details and further information on batch operations.
