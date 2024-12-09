# HubSpot API Documentation: Calls

This document details the HubSpot API endpoints for managing call engagements.  It covers creating, retrieving, updating, associating, and deleting calls.

## Calls Endpoint Reference

Use the calls engagement API to log and manage calls on CRM records and on the calls index page. You can log calls either in HubSpot or through the calls API.

### 1. Create a Call Engagement

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/calls`

**Request Body:**

The request body requires a `properties` object containing call details and an optional `associations` object to link the call to existing records (e.g., contacts, companies).

#### Properties:

| Field                  | Description                                                                                                                                                                 | Required | Data Type    | Example Value                                       |
|-------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|--------------|----------------------------------------------------|
| `hs_timestamp`         | Required. Call creation time. Use Unix timestamp (milliseconds) or UTC format.                                                                                             | Yes      | String       | `2024-10-27T12:00:00.000Z` or `1703708000000`      |
| `hs_call_body`          | Call description and notes.                                                                                                                                                   | No       | String       | "Discussed project X"                               |
| `hs_call_callee_object_id` | ID of the HubSpot record associated with the call. Recipient for OUTBOUND, dialer for INBOUND calls.                                                                         | No       | String       | `12345`                                            |
| `hs_call_callee_object_type` | Object type of the associated record (e.g., "contact", "company"). Recipient object for OUTBOUND, dialer object for INBOUND calls.                                                | No       | String       | "contact"                                           |
| `hs_call_direction`     | Call direction (INBOUND or OUTBOUND) from the HubSpot user's perspective.                                                                                                | No       | String       | "OUTBOUND"                                          |
| `hs_call_disposition`   | Call outcome. Use internal GUID.  See default values below.  Custom values can be retrieved via the properties API.                                                      | No       | String       | `9d9162e7-6cf3-4944-bf63-4dff82258764` (Busy)      |
| `hs_call_duration`      | Call duration in milliseconds.                                                                                                                                               | No       | String       | `360000` (6 minutes)                               |
| `hs_call_from_number`   | Calling phone number.                                                                                                                                                     | No       | String       | "(555) 123-4567"                                     |
| `hs_call_recording_url` | URL of the call recording (HTTPS only, .mp3 or .wav).                                                                                                                      | No       | String       | "https://example.com/recording.mp3"                 |
| `hs_call_status`        | Call status (BUSY, CALLING_CRM_USER, CANCELED, COMPLETED, CONNECTING, FAILED, IN_PROGRESS, NO_ANSWER, QUEUED, RINGING).                                                   | No       | String       | "COMPLETED"                                          |
| `hs_call_title`         | Call title.                                                                                                                                                                | No       | String       | "Sales Call"                                         |
| `hs_call_source`        | Call source. Required for recording and transcription pipeline; set to `INTEGRATIONS_PLATFORM`.                                                                            | No       | String       | "INTEGRATIONS_PLATFORM"                             |
| `hs_call_to_number`     | Receiving phone number.                                                                                                                                                    | No       | String       | "(555) 987-6543"                                     |
| `hubspot_owner_id`      | ID of the call owner (user).                                                                                                                                                 | No       | String       | `1234567`                                           |
| `hs_activity_type`      | Type of call (based on call types set in your HubSpot account).                                                                                                        | No       | String       | "Outbound Sales Call"                               |
| `hs_attachment_ids`     | IDs of call attachments (semicolon-separated).                                                                                                                            | No       | String       | "123;456"                                           |


**Default `hs_call_disposition` GUIDs:**

* Busy: `9d9162e7-6cf3-4944-bf63-4dff82258764`
* Connected: `f240bbac-87c9-4f6e-bf70-924b57d47db7`
* Left live message: `a4c4c377-d246-4b32-a13b-75a56a4cd0ff`
* Left voicemail: `b2cf5968-551e-4856-9783-52b3da59a7d0`
* No answer: `73a0d17f-1163-4015-bdd5-ec830791da20`
* Wrong number: `17b47fee-58de-441e-a44c-c6300d46f273`


#### Associations:

The `associations` object is an array of objects, each defining an association with a record.

| Field      | Description                                                                       |
|-------------|-----------------------------------------------------------------------------------|
| `to`        | Object containing the `id` of the record to associate with.                   |
| `types`     | Array of association type objects. Each object includes `associationCategory` (HUBSPOT_DEFINED) and `associationTypeId`. |


### 2. Retrieve Calls

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/calls` (for all calls) or `/crm/v3/objects/calls/{callId}` (for a specific call)

**Parameters:**

| Parameter    | Description                                                                          | Endpoint      |
|---------------|--------------------------------------------------------------------------------------|-----------------|
| `callId`      | (For individual call retrieval) The ID of the call.                               | `/crm/v3/objects/calls/{callId}` |
| `limit`       | (For all calls) Maximum number of results per page.                               | `/crm/v3/objects/calls` |
| `properties` | Comma-separated list of properties to return.                                     | Both            |
| `associations` | Comma-separated list of object types to retrieve associated IDs for.              | Both            |


### 3. Identify Voicemails vs. Recorded Calls

To differentiate between recorded calls and voicemails, check the `hs_call_status` and `hs_call_has_voicemail` properties.  A voicemail will have `hs_call_status: missed` and `hs_call_has_voicemail: true`.


### 4. Update Calls

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/calls/{callId}`

**Request Body:**  Similar to create, but only include properties to be updated.  Empty string clears a property value.


### 5. Associate Existing Calls with Records

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**URL Parameters:**

| Parameter       | Description                                                                 |
|-----------------|-----------------------------------------------------------------------------|
| `callId`        | ID of the call.                                                              |
| `toObjectType`  | Object type to associate (e.g., "contact", "company").                       |
| `toObjectId`    | ID of the record to associate.                                              |
| `associationTypeId` | Unique association type ID (retrievable via the associations API).        |


### 6. Remove an Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`  (Same as associating)


### 7. Pin a Call on a Record

Pin a call to a record's timeline using the `hs_pinned_engagement_id` field when creating or updating the record via the relevant object APIs (companies, contacts, deals, tickets, custom objects).


### 8. Delete Calls

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/calls/{callId}`

This moves the call to the recycling bin; it can be restored later.


**Note:**  Batch operations (create, retrieve, update, delete) are available via other endpoints; refer to the "Endpoints" tab (mentioned throughout the document) for details.  Also,  many links to other API references are included within the original text,  these are not reproduced here for brevity.
