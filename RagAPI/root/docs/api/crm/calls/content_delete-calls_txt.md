# HubSpot API Guide: Calls

This document details the HubSpot API endpoints for managing calls.  You can log calls within HubSpot or via the calls API.

## Calls Endpoint Reference

Use the calls engagement API to log and manage calls on CRM records and on the calls index page.

### Create a Call Engagement

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/calls`

**Request Body:**

The request body should include a `properties` object with call details and an optional `associations` object to link the call to existing records (e.g., contacts, companies).

**Properties Object:**

| Field                     | Description                                                                                                                                                                                          |
|--------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `hs_timestamp`           | **Required.** Call creation time (Unix timestamp in milliseconds or UTC format). Determines call position on the record timeline.                                                                    |
| `hs_call_body`           | Call description and notes.                                                                                                                                                                         |
| `hs_call_callee_object_id` | ID of the HubSpot record associated with the call. Recipient for outbound calls, dialer for inbound calls.                                                                                       |
| `hs_call_callee_object_type` | Object type of the associated record (e.g., `contact`, `company`). Recipient's object for outbound calls, dialer's object for inbound calls.                                                              |
| `hs_call_direction`      | Call direction from the HubSpot user's perspective (`INBOUND` or `OUTBOUND`).                                                                                                                  |
| `hs_call_disposition`    | Call outcome. Use the internal GUID value.  Custom call outcomes' GUIDs can be found via [this API](link_to_api_needed). Default HubSpot outcomes: <br> - Busy: `9d9162e7-6cf3-4944-bf63-4dff82258764` <br> - Connected: `f240bbac-87c9-4f6e-bf70-924b57d47db7` <br> - Left live message: `a4c4c377-d246-4b32-a13b-75a56a4cd0ff` <br> - Left voicemail: `b2cf5968-551e-4856-9783-52b3da59a7d0` <br> - No answer: `73a0d17f-1163-4015-bdd5-ec830791da20` <br> - Wrong number: `17b47fee-58de-441e-a44c-c6300d46f273` |
| `hs_call_duration`       | Call duration in milliseconds.                                                                                                                                                                     |
| `hs_call_from_number`    | Calling phone number.                                                                                                                                                                          |
| `hs_call_recording_url` | URL of the call recording (.mp3 or .wav, HTTPS only).                                                                                                                                              |
| `hs_call_status`         | Call status (`BUSY`, `CALLING_CRM_USER`, `CANCELED`, `COMPLETED`, `CONNECTING`, `FAILED`, `IN_PROGRESS`, `NO_ANSWER`, `QUEUED`, `RINGING`).                                                  |
| `hs_call_title`          | Call title.                                                                                                                                                                                       |
| `hs_call_source`         | Call source.  Required for recording and transcription pipelines; must be `INTEGRATIONS_PLATFORM`.                                                                                             |
| `hs_call_to_number`      | Called phone number.                                                                                                                                                                           |
| `hubspot_owner_id`       | ID of the call's owner (determines the creator listed on the record timeline).                                                                                                                    |
| `hs_activity_type`       | Type of call (based on call types in your HubSpot account).                                                                                                                                       |
| `hs_attachment_ids`      | IDs of call attachments (semicolon-separated).                                                                                                                                                     |


**Associations Object:**

The `associations` object is an array of objects, each associating the call with a record.

| Field          | Description                                                                                                  |
|-----------------|--------------------------------------------------------------------------------------------------------------|
| `to.id`         | ID of the record to associate.                                                                            |
| `types`         | Array of association types.                                                                                  |
| `types[].associationCategory` | `HUBSPOT_DEFINED`                                                                                       |
| `types[].associationTypeId`    | Unique association type ID.  Default IDs are listed [here](link_to_defaults_needed); custom types via [associations API](link_to_api_needed). |


**Example Request Body:** (See example in original text)


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

* `limit`: Maximum results per page.
* `properties`: Comma-separated list of properties to return.


### Identify Voicemails vs. Recorded Calls

Use `hs_call_status` and `hs_call_has_voicemail` properties.  A voicemail will have `hs_call_status: missed` and `hs_call_has_voicemail: true`.


### Update Calls

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/calls/{callId}`

**Request Body:**  `properties` object with properties to update.  Empty string clears a property value.  (See example in original text)


### Associate Existing Calls with Records

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Parameters:**

* `callId`: Call ID.
* `toObjectType`: Object type (e.g., `contact`, `company`).
* `toObjectId`: Record ID.
* `associationTypeId`: Association type ID (numeric or snake case, retrievable via [associations API](link_to_api_needed)).


### Remove an Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


### Pin a Call on a Record

Pin a call using the `hs_pinned_engagement_id` field when creating or updating a record via object APIs (companies, contacts, deals, tickets, custom objects).


### Delete Calls

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/calls/{callId}`


**(Note:  The markdown needs links to the referenced APIs to be complete.)**
