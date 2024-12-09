# HubSpot Calls API Documentation

This document details the HubSpot API endpoints for managing calls.  These endpoints allow you to log, manage, and retrieve call data within the HubSpot CRM.

## Calls Endpoint Reference

The Calls API allows you to log and manage calls on CRM records and the calls index page.  Calls can be logged within HubSpot or via the API.

**Base URL:** `/crm/v3/objects/calls`

### 1. Create a Call Engagement (POST `/crm/v3/objects/calls`)

This endpoint creates a new call engagement.

**Request Body:**

The request body requires a `properties` object containing call details and an optional `associations` object to link the call to existing records (e.g., contacts, companies).

#### Properties:

| Field                     | Description                                                                                                                                                                                      | Required | Data Type    | Example Value                                     |
|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|---------------|-------------------------------------------------|
| `hs_timestamp`           | Required. Call creation timestamp (Unix timestamp in milliseconds or UTC format).                                                                                                              | Yes      | String/Number | `1679078400000` or `"2023-03-17T00:00:00Z"`     |
| `hs_call_body`           | Call description and notes.                                                                                                                                                                     | No       | String        | "Discussed project X"                            |
| `hs_call_callee_object_id` | ID of the HubSpot record associated with the call. Recipient for outbound calls, dialer for inbound calls.                                                                                     | No       | String        | `12345`                                          |
| `hs_call_callee_object_type` | Object type of the associated record (e.g., `contact`, `company`). Recipient object for outbound calls, dialer object for inbound calls.                                                              | No       | String        | `contact`                                        |
| `hs_call_direction`       | Call direction from the HubSpot user's perspective (`INBOUND` or `OUTBOUND`).                                                                                                              | No       | String        | `OUTBOUND`                                      |
| `hs_call_disposition`     | Call outcome. Use internal GUID value.  Custom outcomes available via the properties API.                                                                                                  | No       | String        | `9d9162e7-6cf3-4944-bf63-4dff82258764` (Busy) |
| `hs_call_duration`       | Call duration in milliseconds.                                                                                                                                                                  | No       | String/Number | `30000`                                          |
| `hs_call_from_number`     | Calling phone number.                                                                                                                                                                         | No       | String        | `(555) 123-4567`                                 |
| `hs_call_recording_url`   | URL of the call recording (HTTPS URLs only, .mp3 or .wav).                                                                                                                                   | No       | String        | `https://example.com/recording.mp3`             |
| `hs_call_status`         | Call status (`BUSY`, `CALLING_CRM_USER`, `CANCELED`, `COMPLETED`, `CONNECTING`, `FAILED`, `IN_PROGRESS`, `NO_ANSWER`, `QUEUED`, `RINGING`).                                               | No       | String        | `COMPLETED`                                      |
| `hs_call_title`          | Call title.                                                                                                                                                                                     | No       | String        | "Sales Call"                                      |
| `hs_call_source`         | Call source (required for recording and transcriptions pipeline; must be `INTEGRATIONS_PLATFORM`).                                                                                             | No       | String        | `INTEGRATIONS_PLATFORM`                         |
| `hs_call_to_number`      | Receiving phone number.                                                                                                                                                                         | No       | String        | `(555) 987-6543`                                 |
| `hubspot_owner_id`       | ID of the call owner.                                                                                                                                                                          | No       | String        | `1234567`                                        |
| `hs_activity_type`       | Type of call (based on call types in your HubSpot account).                                                                                                                                    | No       | String        |  "Sales Call"                                    |
| `hs_attachment_ids`      | IDs of call attachments (semicolon-separated).                                                                                                                                               | No       | String        | `1;2;3`                                          |


#### Associations:

The `associations` object is an array of objects, each specifying an association with a record.

| Field          | Description                                                                  | Required | Data Type |
|-----------------|---------------------------------------------------------------|----------|-----------|
| `to.id`         | ID of the record to associate.                                     | Yes      | Number    |
| `types[0].associationCategory` | Association category (`HUBSPOT_DEFINED`).                       | Yes      | String    |
| `types[0].associationTypeId`    | Association type ID (retrieve via Associations API).             | Yes      | Number    |


### 2. Retrieve Calls (GET `/crm/v3/objects/calls` or GET `/crm/v3/objects/calls/{callId}`)

####  Retrieve Individual Call:

Use GET `/crm/v3/objects/calls/{callId}`.  Parameters:

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.

#### Retrieve All Calls:

Use GET `/crm/v3/objects/calls`. Parameters:

* `limit`: Maximum number of results per page.
* `properties`: Comma-separated list of properties to return.

The response includes the `callId`, which can be used for further operations.


### 3. Identify Voicemails vs. Recorded Calls

To differentiate, include `hs_call_status` and `hs_call_has_voicemail` in your request.  A voicemail has `hs_call_status: missed` and `hs_call_has_voicemail: true`.

### 4. Update a Call (PATCH `/crm/v3/objects/calls/{callId}`)

Update call properties.  HubSpot ignores read-only and non-existent properties.  Use an empty string to clear a property value.


### 5. Associate Existing Calls with Records (PUT `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates a call with records.

* `callId`: Call ID.
* `toObjectType`: Object type (e.g., `contact`, `company`).
* `toObjectId`: Record ID.
* `associationTypeId`: Association type ID (retrieve via Associations API).


### 6. Remove an Association (DELETE `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Removes an association between a call and a record.


### 7. Pin a Call on a Record

Pin a call to a record's timeline using the `hs_pinned_engagement_id` field when creating or updating the record via object APIs (companies, contacts, deals, tickets, custom objects).


### 8. Delete a Call (DELETE `/crm/v3/objects/calls/{callId}`)

Deletes a call (moves it to the recycling bin).  Can be restored later.


**Note:**  The documentation mentions batch operations for create, retrieve, update, and delete.  Refer to the "Endpoints" tab (mentioned throughout the document) for details on those batch endpoints.  Also,  many properties reference other HubSpot APIs (e.g., Associations API, Properties API) for more context.
