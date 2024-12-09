# HubSpot API Guides: Engagements | Calls

This document details the HubSpot API endpoints for managing call engagements.  It covers creating, retrieving, updating, associating, and deleting calls, as well as identifying voicemails versus recorded calls and pinning calls to records.

## Calls Endpoint Reference

Use the calls engagement API to log and manage calls on CRM records and on the calls index page. You can log calls either in HubSpot or through the calls API.

### Create a Call Engagement

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/calls`

**Request Body:**

The request body should include a `properties` object containing call details and an optional `associations` object to link the call with existing records (e.g., contacts, companies).

#### Properties

| Field                     | Description                                                                                                                                                                                                                         |
|--------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `hs_timestamp`            | **Required.** Call creation time. Use a Unix timestamp in milliseconds or UTC format.                                                                                                                                          |
| `hs_call_body`           | Call description and notes.                                                                                                                                                                                                   |
| `hs_call_callee_object_id` | ID of the HubSpot record associated with the call. Recipient for outbound calls, dialer for inbound calls.                                                                                                                      |
| `hs_call_callee_object_type` | Type of the associated record (e.g., `contact`, `company`). Recipient's object type for outbound calls, dialer's object type for inbound calls.                                                                                      |
| `hs_call_direction`       | Call direction from the HubSpot user's perspective (`INBOUND` or `OUTBOUND`).                                                                                                                                                   |
| `hs_call_disposition`    | Call outcome. Use the internal GUID value.  Custom call outcomes' GUIDs can be found via [this API](link_to_api_needed). Default HubSpot outcomes: <br> `Busy`: `9d9162e7-6cf3-4944-bf63-4dff82258764` <br> `Connected`: `f240bbac-87c9-4f6e-bf70-924b57d47db7` <br> `Left live message`: `a4c4c377-d246-4b32-a13b-75a56a4cd0ff` <br> `Left voicemail`: `b2cf5968-551e-4856-9783-52b3da59a7d0` <br> `No answer`: `73a0d17f-1163-4015-bdd5-ec830791da20` <br> `Wrong number`: `17b47fee-58de-441e-a44c-c6300d46f273` |
| `hs_call_duration`       | Call duration in milliseconds.                                                                                                                                                                                                 |
| `hs_call_from_number`    | Caller's phone number.                                                                                                                                                                                                    |
| `hs_call_recording_url`  | URL of the call recording (HTTPS URLs for `.mp3` or `.wav` files only).                                                                                                                                                       |
| `hs_call_status`         | Call status (`BUSY`, `CALLING_CRM_USER`, `CANCELED`, `COMPLETED`, `CONNECTING`, `FAILED`, `IN_PROGRESS`, `NO_ANSWER`, `QUEUED`, `RINGING`).                                                                                  |
| `hs_call_title`          | Call title.                                                                                                                                                                                                                  |
| `hs_call_source`         | Call source.  Required for recording and transcriptions pipeline; must be `INTEGRATIONS_PLATFORM` if set.                                                                                                               |
| `hs_call_to_number`      | Recipient's phone number.                                                                                                                                                                                                  |
| `hubspot_owner_id`       | ID of the call's owner (determines the creator listed on the record timeline).                                                                                                                                               |
| `hs_activity_type`       | Type of call (based on call types set in your HubSpot account).                                                                                                                                                            |
| `hs_attachment_ids`      | IDs of call attachments (semicolon-separated).                                                                                                                                                                              |


#### Associations

To associate the call with existing records, include an `associations` object:

| Field          | Description                                                                                                                           |
|-----------------|---------------------------------------------------------------------------------------------------------------------------------------|
| `to.id`         | ID of the record to associate.                                                                                                           |
| `types`         | Array of association types.                                                                                                             |
| `types[].associationCategory` | `HUBSPOT_DEFINED`                                                                                                                   |
| `types[].associationTypeId`   | Association type ID (default IDs are listed [here](link_to_default_ids_needed); retrieve custom type IDs via the associations API). |

*(Example request body provided in original text)*

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


### Identify Voicemails vs. Recorded Calls

For voicemails and recorded calls, check `hs_call_recording_url`. To differentiate between completed recorded calls and inbound calls with voicemails, use `hs_call_status` and `hs_call_has_voicemail`:

* Voicemail: `hs_call_status` = `missed`, `hs_call_has_voicemail` = `true`
* No voicemail: `hs_call_status` = other than `missed`, `hs_call_has_voicemail` = `false` or `null`


### Update Calls

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/calls/{callId}`

**Request Body:**

Include the `properties` object with the fields you want to update.  Empty strings clear property values.

*(Example request body provided in original text)*


### Associate Existing Calls with Records

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Fields:**

* `callId`: Call ID.
* `toObjectType`: Object type to associate (e.g., `contact`, `company`).
* `toObjectId`: ID of the record to associate.
* `associationTypeId`: Unique association type ID (retrieve via the associations API).


### Remove an Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


### Pin a Call on a Record

Pin a call to the top of a record's timeline by including its ID in the `hs_pinned_engagement_id` field when creating or updating the record via object APIs (companies, contacts, deals, tickets, custom objects).


### Delete Calls

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/calls/{callId}`

*(Note:  Many sections mention batch operations via the "Endpoints" tab.  Links to those endpoints would improve this documentation.)*
