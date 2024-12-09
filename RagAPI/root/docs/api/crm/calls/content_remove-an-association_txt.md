# HubSpot Calls API Documentation

This document details the HubSpot API endpoints for managing call engagements.

## Calls Endpoint Reference

The Calls engagement API allows you to log and manage calls on CRM records and the calls index page.  Calls can be logged within HubSpot or through the API.

### Create a Call Engagement

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/calls`

**Request Body:**  The request body must contain a `properties` object with call details and an optional `associations` object to link the call to existing records (e.g., contacts, companies).

#### Properties

| Field                  | Description                                                                                                                                                                                                       |
|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `hs_timestamp`         | **Required.** Call creation time. Use a Unix timestamp in milliseconds or UTC format.                                                                                                                           |
| `hs_call_body`         | Call description and notes.                                                                                                                                                                                    |
| `hs_call_callee_object_id` | ID of the HubSpot record associated with the call. Recipient for OUTBOUND calls, dialer for INBOUND calls.                                                                                                   |
| `hs_call_callee_object_type` | Type of the associated record (e.g., `contact`, `company`). Recipient's object for OUTBOUND calls, dialer's object for INBOUND calls.                                                                        |
| `hs_call_direction`    | Call direction from the HubSpot user's perspective. `INBOUND` or `OUTBOUND`.                                                                                                                              |
| `hs_call_disposition` | Call outcome. Use the internal GUID value.  See default values below.  Custom values can be retrieved using the [properties API](link-to-properties-api).                                                |
| `hs_call_duration`     | Call duration in milliseconds.                                                                                                                                                                                |
| `hs_call_from_number`  | Call origin phone number.                                                                                                                                                                                  |
| `hs_call_recording_url` | URL of the call recording (.mp3 or .wav). Must be a secure HTTPS URL.                                                                                                                                     |
| `hs_call_status`       | Call status: `BUSY`, `CALLING_CRM_USER`, `CANCELED`, `COMPLETED`, `CONNECTING`, `FAILED`, `IN_PROGRESS`, `NO_ANSWER`, `QUEUED`, `RINGING`.                                                                 |
| `hs_call_title`        | Call title.                                                                                                                                                                                              |
| `hs_call_source`       | Call source.  Required for using the recording and transcriptions pipeline. Must be set to `INTEGRATIONS_PLATFORM`.                                                                                             |
| `hs_call_to_number`    | Call recipient phone number.                                                                                                                                                                                  |
| `hubspot_owner_id`     | ID of the call owner (user). Determines the call creator listed on the record timeline.                                                                                                                       |
| `hs_activity_type`     | Type of call (based on call types set in your HubSpot account).                                                                                                                                               |
| `hs_attachment_ids`    | IDs of call attachments (separated by semicolons).                                                                                                                                                           |

**Default `hs_call_disposition` values:**

* Busy: `9d9162e7-6cf3-4944-bf63-4dff82258764`
* Connected: `f240bbac-87c9-4f6e-bf70-924b57d47db7`
* Left live message: `a4c4c377-d246-4b32-a13b-75a56a4cd0ff`
* Left voicemail: `b2cf5968-551e-4856-9783-52b3da59a7d0`
* No answer: `73a0d17f-1163-4015-bdd5-ec830791da20`
* Wrong number: `17b47fee-58de-441e-a44c-c6300d46f273`

#### Associations

The `associations` object allows you to associate the call with existing records.

| Field       | Description                                                                                                                                  |
|-------------|-------------------------------------------------------------------------------------------------------------------------------|
| `to`        | The record to associate (specified by its `id`).                                                                                   |
| `types`     | The association type.  Includes `associationCategory` (`HUBSPOT_DEFINED`) and `associationTypeId` (see [associations API](link-to-associations-api)). |


### Retrieve Calls

**Individual Call:**

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/calls/{callId}`

**Parameters:**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.


**All Calls:**

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/calls`

**Parameters:**

* `limit`: Maximum number of results per page.
* `properties`: Comma-separated list of properties to return.

The response includes the `callId`, which can be used for updating and deleting calls.


### Identify Voicemails vs. Recorded Calls

For recorded calls and voicemails, a recording is stored in `hs_call_recording_url`.  To differentiate between completed recorded calls and inbound calls with voicemails (requires inbound calling access), check `hs_call_status` and `hs_call_has_voicemail`. A voicemail will have `hs_call_status` as `missed` and `hs_call_has_voicemail` as `true`.


### Update Calls

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/calls/{callId}`

**Request Body:**  Include the properties to update.  Empty strings clear property values.  Read-only and non-existent properties are ignored.


### Associate Existing Calls with Records

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Parameters:**

* `callId`: The call ID.
* `toObjectType`: Object type to associate (e.g., `contact`, `company`).
* `toObjectId`: The record ID.
* `associationTypeId`: Association type ID (can be numerical or snake case; retrieve via the [associations API](link-to-associations-api)).


### Remove an Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


### Pin a Call on a Record

Pin a call to the top of a record's timeline using the `hs_pinned_engagement_id` field when creating or updating a record via the object APIs (companies, contacts, deals, tickets, custom objects). The call must already be associated with the record. Only one activity can be pinned per record.


### Delete Calls

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/calls/{callId}`

Deleted calls are moved to the recycling bin and can be restored.


**(Note:  Replace `link-to-properties-api` and `link-to-associations-api` with the actual links to the respective API documentation.)**
