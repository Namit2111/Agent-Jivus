# HubSpot Calls API Documentation

This document details the HubSpot API endpoints for managing calls.  It covers creating, retrieving, updating, associating, and deleting call engagements.

## Calls Endpoint Reference

Use the Calls engagement API to log and manage calls on CRM records and on the calls index page. You can log calls either in HubSpot or through the Calls API.

### Create a Call Engagement

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/calls`

**Request Body:**

The request body requires a `properties` object containing call details and an optional `associations` object to link the call to existing records (e.g., contacts, companies).

#### Properties

| Field                 | Description                                                                                                                                                                                             |
|----------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `hs_timestamp`        | **Required.** Call creation timestamp. Use a Unix timestamp in milliseconds or UTC format.                                                                                                              |
| `hs_call_body`        | Call description and notes.                                                                                                                                                                         |
| `hs_call_callee_object_id` | ID of the HubSpot record associated with the call.  Recipient for outbound calls, dialer for inbound calls.                                                                                          |
| `hs_call_callee_object_type` | Object type of the associated record (e.g., `contact`, `company`). Recipient's object type for outbound, dialer's object type for inbound.                                                              |
| `hs_call_direction`   | Call direction from the HubSpot user's perspective (`INBOUND` or `OUTBOUND`).                                                                                                                  |
| `hs_call_disposition` | Call outcome. Use the internal GUID value.  Default values: <br> `Busy`: `9d9162e7-6cf3-4944-bf63-4dff82258764` <br> `Connected`: `f240bbac-87c9-4f6e-bf70-924b57d47db7` <br> `Left live message`: `a4c4c377-d246-4b32-a13b-75a56a4cd0ff` <br> `Left voicemail`: `b2cf5968-551e-4856-9783-52b3da59a7d0` <br> `No answer`: `73a0d17f-1163-4015-bdd5-ec830791da20` <br> `Wrong number`: `17b47fee-58de-441e-a44c-c6300d46f273` |
| `hs_call_duration`    | Call duration in milliseconds.                                                                                                                                                                          |
| `hs_call_from_number` | Caller's phone number.                                                                                                                                                                             |
| `hs_call_recording_url` | URL of the call recording (HTTPS URLs only, .mp3 or .wav).                                                                                                                                   |
| `hs_call_status`      | Call status (`BUSY`, `CALLING_CRM_USER`, `CANCELED`, `COMPLETED`, `CONNECTING`, `FAILED`, `IN_PROGRESS`, `NO_ANSWER`, `QUEUED`, `RINGING`).                                                      |
| `hs_call_title`       | Call title.                                                                                                                                                                                          |
| `hs_call_source`      | Call source.  Required for recording and transcriptions pipeline; must be `INTEGRATIONS_PLATFORM`.                                                                                             |
| `hs_call_to_number`   | Recipient's phone number.                                                                                                                                                                            |
| `hubspot_owner_id`    | ID of the call owner.                                                                                                                                                                                |
| `hs_activity_type`    | Type of call (based on call types in your HubSpot account).                                                                                                                                        |
| `hs_attachment_ids`   | IDs of call attachments (semicolon-separated).                                                                                                                                                       |


#### Associations

To associate a call with existing records, include an `associations` object in your request.

| Field       | Description                                                                                                         |
|-------------|---------------------------------------------------------------------------------------------------------------------|
| `to.id`     | ID of the record to associate.                                                                                      |
| `types`     | Array of association types. Each type includes `associationCategory` (`HUBSPOT_DEFINED`) and `associationTypeId`. |


**Example Request Body:** (See example in original text)


### Retrieve Calls

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/calls` (for all calls) or `/crm/v3/objects/calls/{callId}` (for a single call)


**Parameters:**

* **`limit`**: Maximum results per page (for `/crm/v3/objects/calls`).
* **`properties`**: Comma-separated list of properties to return.
* **`associations`**: Comma-separated list of object types to retrieve associated IDs for.


### Identify Voicemails vs. Recorded Calls

To differentiate between recorded calls and voicemails, check the `hs_call_status` (`missed`) and `hs_call_has_voicemail` (`true` for voicemail, `false` for recorded call, `null` otherwise) properties.


### Update Calls

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/calls/{callId}`

**Request Body:**  Include the properties to update.  Empty strings clear property values.  (See example in original text)


### Associate Existing Calls with Records

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Parameters:**

* `callId`: Call ID.
* `toObjectType`: Object type (e.g., `contact`, `company`).
* `toObjectId`: Record ID.
* `associationTypeId`: Association type ID (retrievable via the Associations API).


### Remove an Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


### Pin a Call on a Record

To pin a call, include its ID in the `hs_pinned_engagement_id` field when creating or updating a record using the object APIs (companies, contacts, deals, tickets, custom objects).


### Delete Calls

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/calls/{callId}`


**Note:** Deleting a call moves it to the recycling bin; it can be restored later.


This documentation is based on the provided text and may not be completely exhaustive.  Always refer to the official HubSpot API documentation for the most up-to-date information.
