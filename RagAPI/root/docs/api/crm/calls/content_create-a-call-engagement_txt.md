# HubSpot API Guide: Calls

This document details the HubSpot API endpoints for managing call engagements.  This includes creating, retrieving, updating, associating, and deleting calls.

## Calls Endpoint Reference

Use the calls engagement API to log and manage calls on CRM records and on the calls index page. You can log calls either in HubSpot or through the calls API.

### Create a Call Engagement

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/calls`

**Request Body:**

The request body should contain a `properties` object and optionally an `associations` object.

#### Properties

| Field                  | Description                                                                                                                                                                                                  | Required | Data Type       | Example                                      |
|-----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|-----------------|----------------------------------------------|
| `hs_timestamp`         | Required. Call creation time (Unix timestamp in milliseconds or UTC format).                                                                                                                                 | Yes      | String/Number    | `1679092800000` or `2023-03-17T01:32:44.872Z` |
| `hs_call_body`         | Call description and notes.                                                                                                                                                                                 | No       | String           | "Resolved issue"                             |
| `hs_call_callee_object_id` | ID of the HubSpot record associated with the call (recipient for outbound, dialer for inbound).                                                                                                                 | No       | String           | `12345`                                       |
| `hs_call_callee_object_type` | Type of the associated record (e.g., `contact`, `company`).                                                                                                                                                    | No       | String           | `contact`                                     |
| `hs_call_direction`    | Call direction from the HubSpot user's perspective (`INBOUND` or `OUTBOUND`).                                                                                                                            | No       | String           | `OUTBOUND`                                   |
| `hs_call_disposition`  | Call outcome (use internal GUID).  Default values are listed below.  Custom values can be retrieved via the [properties API](link_to_properties_api).                                                        | No       | String           | `9d9162e7-6cf3-4944-bf63-4dff82258764` (Busy) |
| `hs_call_duration`     | Call duration in milliseconds.                                                                                                                                                                               | No       | Number           | `3800`                                        |
| `hs_call_from_number`  | Phone number the call originated from.                                                                                                                                                                     | No       | String           | `(857) 829 5489`                            |
| `hs_call_recording_url` | URL of the call recording (HTTPS URLs for `.mp3` or `.wav` files only).                                                                                                                                | No       | String           | `https://example.com/recording.mp3`          |
| `hs_call_status`       | Call status (`BUSY`, `CALLING_CRM_USER`, `CANCELED`, `COMPLETED`, `CONNECTING`, `FAILED`, `IN_PROGRESS`, `NO_ANSWER`, `QUEUED`, `RINGING`).                                                            | No       | String           | `COMPLETED`                                    |
| `hs_call_title`        | Call title.                                                                                                                                                                                              | No       | String           | "Support call"                               |
| `hs_call_source`       | Call source (required for recording and transcription pipeline; must be `INTEGRATIONS_PLATFORM`).                                                                                                          | No       | String           | `INTEGRATIONS_PLATFORM`                      |
| `hs_call_to_number`    | Phone number that received the call.                                                                                                                                                                     | No       | String           | `(509) 999 9999`                            |
| `hubspot_owner_id`     | ID of the call's owner.                                                                                                                                                                                    | No       | String           | `11349275740`                               |
| `hs_activity_type`     | Type of call (based on call types in your HubSpot account).                                                                                                                                                 | No       | String           | ...                                          |
| `hs_attachment_ids`    | IDs of call attachments (semicolon-separated).                                                                                                                                                           | No       | String           | `1;2;3`                                        |


#### Associations

To associate the call with existing records, include an `associations` array. Each element should have a `to` object specifying the record ID and a `types` array specifying the association type.

| Field          | Description                                                                              |
|-----------------|------------------------------------------------------------------------------------------|
| `to.id`         | ID of the record to associate with.                                                    |
| `types[].associationCategory` | Association category (`HUBSPOT_DEFINED`).                                         |
| `types[].associationTypeId`   | Association type ID (default IDs are listed [here](link_to_default_ids), custom IDs can be retrieved via the [associations API](link_to_associations_api)). |


### Retrieve Calls

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/calls` (for list) or `/crm/v3/objects/calls/{callId}` (for individual call)

**Parameters:**

* **`limit`**: (List endpoint only) Maximum number of results per page.
* **`properties`**: Comma-separated list of properties to return.
* **`associations`**: Comma-separated list of object types to retrieve associated IDs for.


### Identify Voicemails vs. Recorded Calls

To differentiate between recorded calls and voicemails, check the `hs_call_status` and `hs_call_has_voicemail` properties. A voicemail will have `hs_call_status: missed` and `hs_call_has_voicemail: true`.


### Update Calls

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/calls/{callId}`

**Request Body:**

Include the `properties` object with the fields you want to update.  Empty strings can be used to clear property values.


### Associate Existing Calls with Records

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Parameters:**

* `callId`: Call ID.
* `toObjectType`: Object type (e.g., `contact`, `company`).
* `toObjectId`: Record ID.
* `associationTypeId`: Association type ID.


### Remove an Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


### Pin a Call on a Record

To pin a call to a record's timeline, include the call's `id` in the `hs_pinned_engagement_id` field when creating or updating the record via the relevant object API (companies, contacts, deals, tickets, custom objects).


### Delete Calls

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/calls/{callId}`


**Note:**  Remember to replace placeholders like `{callId}`, `{toObjectType}`, `{toObjectId}`, and `{associationTypeId}` with actual values.  Links to related APIs (properties, associations, etc.) should be added where indicated.  The example code snippets should be properly formatted for readability within the markdown.
