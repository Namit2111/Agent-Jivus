# HubSpot Calls API Documentation

This document details the HubSpot Calls API, allowing you to manage calls within the HubSpot CRM.  It covers creating, retrieving, updating, associating, and deleting calls, along with handling voicemails and recordings.

## API Endpoint Base URL:

`/crm/v3/objects/calls`


## 1. Create a Call Engagement (POST)

**Endpoint:** `/crm/v3/objects/calls`

**Method:** `POST`

**Request Body:**  The request body must contain a `properties` object with call details and an optional `associations` object to link the call to existing HubSpot records (e.g., contacts, companies).

**Properties:**

| Field                     | Description                                                                                                                                   | Type             | Required | Example                                      |
|--------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|-----------------|----------|-----------------------------------------------|
| `hs_timestamp`           | Required. Call creation time (Unix timestamp in milliseconds or UTC format).                                                              | String/Number    | Yes      | `1679011200000` or `2023-03-17T01:32:44.872Z` |
| `hs_call_body`           | Call description and notes.                                                                                                                  | String           | No       | "Support call resolved."                       |
| `hs_call_callee_object_id` | ID of the associated HubSpot record (recipient for outbound, dialer for inbound calls).                                                    | String           | No       | `12345`                                      |
| `hs_call_callee_object_type` | Type of the associated HubSpot record (e.g., `contact`, `company`).                                                                        | String           | No       | `contact`                                    |
| `hs_call_direction`      | Call direction (`INBOUND` or `OUTBOUND`).                                                                                                 | String           | No       | `OUTBOUND`                                  |
| `hs_call_disposition`   | Call outcome (use internal GUID; see default values below).  Custom values can be obtained via the properties API.                   | String           | No       | `9d9162e7-6cf3-4944-bf63-4dff82258764` (Busy) |
| `hs_call_duration`       | Call duration in milliseconds.                                                                                                              | Number           | No       | `3800`                                       |
| `hs_call_from_number`    | Calling phone number.                                                                                                                      | String           | No       | `(857) 829 5489`                             |
| `hs_call_recording_url` | URL of the call recording (HTTPS only).                                                                                                     | String           | No       | `https://example.com/recording.mp3`         |
| `hs_call_status`         | Call status (`BUSY`, `CALLING_CRM_USER`, `CANCELED`, `COMPLETED`, `CONNECTING`, `FAILED`, `IN_PROGRESS`, `NO_ANSWER`, `QUEUED`, `RINGING`). | String           | No       | `COMPLETED`                                  |
| `hs_call_title`          | Call title.                                                                                                                               | String           | No       | "Sales Call"                                |
| `hs_call_source`         | Call source (required for recording/transcription pipeline; set to `INTEGRATIONS_PLATFORM`).                                              | String           | No       | `INTEGRATIONS_PLATFORM`                      |
| `hs_call_to_number`      | Receiving phone number.                                                                                                                     | String           | No       | `(509) 999 9999`                             |
| `hubspot_owner_id`       | ID of the HubSpot user who owns the call.                                                                                                  | String           | No       | `11349275740`                               |
| `hs_activity_type`       | Type of call (based on call types in your HubSpot account).                                                                                | String           | No       |  "Outbound Call"                            |
| `hs_attachment_ids`      | IDs of associated attachments (semicolon-separated).                                                                                       | String           | No       | "123;456"                                    |


**Associations:**

| Field           | Description                                                                                      | Type          | Required | Example                               |
|-----------------|--------------------------------------------------------------------------------------------------|---------------|----------|---------------------------------------|
| `to.id`         | ID of the record to associate.                                                                 | Number/String | Yes      | `500`                               |
| `types[].associationCategory` | Association category (`HUBSPOT_DEFINED`).                                                   | String        | Yes      | `HUBSPOT_DEFINED`                     |
| `types[].associationTypeId`  | Association type ID (default IDs listed in documentation; retrieve custom IDs via Associations API). | Number/String | Yes      | `194`                               |


**Example Request Body:**

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27T12:00:00Z",
    "hs_call_title": "New Customer Call",
    "hubspot_owner_id": "12345",
    "hs_call_body": "Initial consultation",
    "hs_call_duration": "60000"
  },
  "associations": [
    {
      "to": {"id": 67890},
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 194}]
    }
  ]
}
```

**Response:**  A JSON object representing the newly created call, including its `callId`.


## 2. Retrieve Calls (GET)

**a) Retrieve a Single Call:**

**Endpoint:** `/crm/v3/objects/calls/{callId}`

**Method:** `GET`

**Parameters:**

| Parameter    | Description                                                                              | Type     |
|---------------|------------------------------------------------------------------------------------------|----------|
| `properties` | Comma-separated list of properties to return.                                           | String   |
| `associations` | Comma-separated list of object types to retrieve associated IDs for.                   | String   |


**b) Retrieve All Calls:**

**Endpoint:** `/crm/v3/objects/calls`

**Method:** `GET`

**Parameters:**

| Parameter    | Description                                                                         | Type     |
|---------------|-------------------------------------------------------------------------------------|----------|
| `limit`       | Maximum number of results per page.                                                 | Number   |
| `properties` | Comma-separated list of properties to return.                                     | String   |


**Response:** A JSON object containing a list of calls and pagination information.


## 3. Update a Call (PATCH)

**Endpoint:** `/crm/v3/objects/calls/{callId}`

**Method:** `PATCH`

**Request Body:** A `properties` object containing the properties to update.  Empty strings clear property values.

**Example Request Body:**

```json
{
  "properties": {
    "hs_call_body": "Follow-up scheduled"
  }
}
```

**Response:**  A JSON object representing the updated call.


## 4. Associate Existing Calls with Records (PUT)

**Endpoint:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `PUT`

**Parameters:**

| Parameter       | Description                                                                       | Type          |
|-----------------|-----------------------------------------------------------------------------------|---------------|
| `callId`        | ID of the call.                                                                    | String        |
| `toObjectType`  | Type of object to associate (e.g., `contact`, `company`).                           | String        |
| `toObjectId`    | ID of the record to associate.                                                      | String/Number |
| `associationTypeId` | Unique association type ID (retrieve via Associations API).                       | String/Number |


**Response:** A confirmation of the association.


## 5. Remove an Association (DELETE)

**Endpoint:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `DELETE`

**Parameters:**  Same as for associating calls.

**Response:** A confirmation of the association removal.


## 6. Pin a Call on a Record

Pinning a call is done by including the call's `id` in the `hs_pinned_engagement_id` field when creating or updating a record using other HubSpot object APIs (contacts, companies, etc.).


## 7. Delete a Call (DELETE)

**Endpoint:** `/crm/v3/objects/calls/{callId}`

**Method:** `DELETE`

**Response:** A confirmation of the deletion (call is moved to the recycling bin).


##  Identifying Voicemails vs. Recorded Calls

To distinguish between recorded calls and voicemails, use the following properties in your request:

* `hs_call_status`: Will be `missed` for voicemails.
* `hs_call_has_voicemail`: Will be `true` for voicemails, `false` for missed calls without voicemails, or `null` for other call statuses.


This documentation provides a concise overview. For complete details on all endpoints, parameters, and error handling, refer to the full HubSpot API reference.  Remember to replace placeholders like `{callId}` with actual values.  Always consult the official HubSpot API documentation for the most up-to-date information.
