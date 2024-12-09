# HubSpot Calls API Documentation

This document details the HubSpot API endpoints for managing call engagements.  It covers creating, retrieving, updating, associating, and deleting calls.

## Calls Endpoint Reference

Use the Calls engagement API to log and manage calls on CRM records and on the calls index page. You can log calls either in HubSpot or through the Calls API.

### Create a Call Engagement

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/calls`

**Request Body:**  The request body should include a `properties` object and optionally an `associations` object.

#### Properties

| Field                   | Description                                                                                                                                                                  | Required | Notes                                                                                                                                                                        |
|------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `hs_timestamp`          | Required. The call's creation time. Use a Unix timestamp in milliseconds or UTC format (e.g., "2024-10-27T10:00:00Z").                                                            | Yes      |                                                                                                                                                                                |
| `hs_call_body`          | Description of the call, including notes.                                                                                                                                    | No       |                                                                                                                                                                                |
| `hs_call_callee_object_id` | ID of the HubSpot record associated with the call. Recipient for outbound calls, dialer for inbound calls.                                                                    | No       |                                                                                                                                                                                |
| `hs_call_callee_object_type` | Type of the object (`contact`, `company`, etc.) the associated record belongs to. Recipient's object for outbound, dialer's object for inbound calls.                              | No       |                                                                                                                                                                                |
| `hs_call_direction`     | Call direction from the HubSpot user's perspective (`INBOUND` or `OUTBOUND`).                                                                                             | No       |                                                                                                                                                                                |
| `hs_call_disposition`   | Call outcome. Use the internal GUID value.  See default values below.  Custom values can be retrieved via the properties API.                                                  | No       |                                                                                                                                                                                |
| `hs_call_duration`      | Call duration in milliseconds.                                                                                                                                             | No       |                                                                                                                                                                                |
| `hs_call_from_number`   | Phone number the call originated from.                                                                                                                                  | No       |                                                                                                                                                                                |
| `hs_call_recording_url` | URL of the call recording (HTTPS URLs for `.mp3` or `.wav` only).                                                                                                       | No       |                                                                                                                                                                                |
| `hs_call_status`        | Call status (`BUSY`, `CALLING_CRM_USER`, `CANCELED`, `COMPLETED`, `CONNECTING`, `FAILED`, `IN_PROGRESS`, `NO_ANSWER`, `QUEUED`, `RINGING`).                               | No       |                                                                                                                                                                                |
| `hs_call_title`         | Title of the call.                                                                                                                                                       | No       |                                                                                                                                                                                |
| `hs_call_source`        | Source of the call. Required for the recording and transcriptions pipeline; if set, must be `INTEGRATIONS_PLATFORM`.                                                        | No       |                                                                                                                                                                                |
| `hs_call_to_number`     | Phone number that received the call.                                                                                                                                  | No       |                                                                                                                                                                                |
| `hubspot_owner_id`      | ID of the call's owner (determines the creator listed on the record timeline).                                                                                             | No       |                                                                                                                                                                                |
| `hs_activity_type`      | Type of call (based on call types set in your HubSpot account).                                                                                                         | No       |                                                                                                                                                                                |
| `hs_attachment_ids`     | IDs of call attachments (semicolon-separated).                                                                                                                          | No       |                                                                                                                                                                                |


**Default `hs_call_disposition` Values:**

* Busy: `9d9162e7-6cf3-4944-bf63-4dff82258764`
* Connected: `f240bbac-87c9-4f6e-bf70-924b57d47db7`
* Left live message: `a4c4c377-d246-4b32-a13b-75a56a4cd0ff`
* Left voicemail: `b2cf5968-551e-4856-9783-52b3da59a7d0`
* No answer: `73a0d17f-1163-4015-bdd5-ec830791da20`
* Wrong number: `17b47fee-58de-441e-a44c-c6300d46f273`


#### Associations

To associate the call with existing records, include an `associations` object.

| Field       | Description                                                                                             |
|-------------|---------------------------------------------------------------------------------------------------------|
| `to`        | The record to associate (specified by its `id`).                                                    |
| `types`     | The association type between the call and the record (`associationCategory` and `associationTypeId`). |


**Example Request Body:** (See example in original text)


### Retrieve Calls

**Retrieve Individual Call:**

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/calls/{callId}`

**Parameters:**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.


**Retrieve All Calls:**

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/calls`

**Parameters:**

* `limit`: Maximum number of results per page.
* `properties`: Comma-separated list of properties to return.


### Identify Voicemails vs. Recorded Calls

To differentiate between recorded calls and voicemails, use `hs_call_status` and `hs_call_has_voicemail` properties:

* Voicemail: `hs_call_status` = `missed`, `hs_call_has_voicemail` = `true`
* Recorded call (not voicemail): `hs_call_status` = other than `missed`, `hs_call_has_voicemail` = `false` or `null`


### Update Calls

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/calls/{callId}`

**Request Body:**  Include the `properties` object with the fields to update.  Empty strings clear property values. (See example in original text)


### Associate Existing Calls with Records

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Parameters:**

* `callId`: The ID of the call.
* `toObjectType`: The type of object to associate (e.g., `contact`, `company`).
* `toObjectId`: The ID of the record to associate.
* `associationTypeId`: Unique identifier for the association type (can be retrieved via the associations API).


### Remove an Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


### Pin a Call on a Record

Pin a call using the `hs_pinned_engagement_id` field when creating or updating a record via object APIs (companies, contacts, deals, tickets, custom objects).


### Delete Calls

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/calls/{callId}`


This documentation provides a comprehensive overview of the HubSpot Calls API.  Remember to consult the HubSpot Developer Documentation for the most up-to-date information and details on error handling and authentication.
