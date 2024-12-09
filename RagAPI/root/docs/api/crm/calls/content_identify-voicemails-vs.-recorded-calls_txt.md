# HubSpot API Guides: Engagements | Calls

This document details the HubSpot API endpoints for managing call engagements.  You can log calls within HubSpot or via the API.  This guide covers the basic methods; for a complete list of endpoints and requirements, refer to the "Endpoints" tab (assumed to be present in the original context).

## Creating a Call Engagement

To create a call engagement, send a `POST` request to `/crm/v3/objects/calls`.

The request body requires a `properties` object containing call details and an optional `associations` object to link the call to existing records (e.g., contacts, companies).


### Properties

The following properties are available.  Custom properties can be created using the properties API.

| Field                  | Description                                                                                                                                                                                                                                     |
|-------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `hs_timestamp`          | **Required.** Call creation time. Use a Unix timestamp (milliseconds) or UTC format. Determines call position on the record timeline.                                                                                                              |
| `hs_call_body`          | Call description and notes.                                                                                                                                                                                                                  |
| `hs_call_callee_object_id` | ID of the HubSpot record associated with the call.  Recipient for outbound calls, dialer for inbound calls.                                                                                                                                |
| `hs_call_callee_object_type` | Type of the associated record (e.g., "contact", "company"). Recipient object for outbound calls, dialer object for inbound calls.                                                                                                              |
| `hs_call_direction`     | Call direction from the HubSpot user's perspective. `"INBOUND"` if the user received the call, `"OUTBOUND"` if initiated.                                                                                                                      |
| `hs_call_disposition`   | Call outcome. Use the internal GUID value.  Custom call outcomes can be found using [this API](placeholder_link_to_custom_call_outcomes_api). Default values: <br>Busy: `9d9162e7-6cf3-4944-bf63-4dff82258764`<br>Connected: `f240bbac-87c9-4f6e-bf70-924b57d47db7`<br>Left live message: `a4c4c377-d246-4b32-a13b-75a56a4cd0ff`<br>Left voicemail: `b2cf5968-551e-4856-9783-52b3da59a7d0`<br>No answer: `73a0d17f-1163-4015-bdd5-ec830791da20`<br>Wrong number: `17b47fee-58de-441e-a44c-c6300d46f273` |
| `hs_call_duration`      | Call duration in milliseconds.                                                                                                                                                                                                                   |
| `hs_call_from_number`   | Calling phone number.                                                                                                                                                                                                                        |
| `hs_call_recording_url` | URL of the call recording (.mp3 or .wav). Must be a secure HTTPS URL.                                                                                                                                                                     |
| `hs_call_status`        | Call status. Options: `"BUSY"`, `"CALLING_CRM_USER"`, `"CANCELED"`, `"COMPLETED"`, `"CONNECTING"`, `"FAILED"`, `"IN_PROGRESS"`, `"NO_ANSWER"`, `"QUEUED"`, `"RINGING"`.                                                                 |
| `hs_call_title`         | Call title.                                                                                                                                                                                                                                |
| `hs_call_source`        | Call source.  Required for the recording and transcriptions pipeline. If set, must be `"INTEGRATIONS_PLATFORM"`.                                                                                                                            |
| `hs_call_to_number`     | Called phone number.                                                                                                                                                                                                                        |
| `hubspot_owner_id`      | ID of the call's owner (determines the creator listed on the record timeline).                                                                                                                                                                 |
| `hs_activity_type`      | Call type (based on call types configured in your HubSpot account).                                                                                                                                                                             |
| `hs_attachment_ids`     | IDs of call attachments (semicolon-separated).                                                                                                                                                                                               |


### Associations

To associate the call with existing records, include an `associations` object.  Example:

```json
{
  "properties": { ... },
  "associations": [
    {
      "to": { "id": 500 },
      "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 194 } ]
    },
    {
      "to": { "id": 1234 },
      "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 220 } ]
    }
  ]
}
```

| Field             | Description                                                                                                    |
|----------------------|-------------------------------------------------------------------------------------------------------------|
| `to.id`            | ID of the record to associate.                                                                               |
| `types[].associationCategory` | Association category.                                                                                        |
| `types[].associationTypeId` | Association type ID.  Default IDs are listed [here](placeholder_link_to_default_association_types).  Custom types can be retrieved via the associations API. |


## Retrieving Calls

Calls can be retrieved individually or in bulk.

* **Individual Call:** `GET /crm/v3/objects/calls/{callId}`.  Parameters: `properties` (comma-separated list), `associations` (comma-separated list of object types).

* **All Calls:** `GET /crm/v3/objects/calls`. Parameters: `limit`, `properties`.


## Identifying Voicemails vs. Recorded Calls

For voicemails and recorded calls, the recording URL is in `hs_call_recording_url`. To differentiate between completed recorded calls and inbound voicemails (requires inbound calling access): use `hs_call_status` and `hs_call_has_voicemail`. A voicemail will have `hs_call_status: "missed"` and `hs_call_has_voicemail: true`.


## Updating Calls

Calls can be updated individually or in batches.

* **Individual Call:** `PATCH /crm/v3/objects/calls/{callId}`. The request body contains the properties to update.  HubSpot ignores read-only and non-existent properties.  An empty string clears a property value.


## Associating Existing Calls with Records

`PUT /crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

| Field             | Description                                                                     |
|----------------------|-----------------------------------------------------------------------------|
| `callId`           | Call ID.                                                                     |
| `toObjectType`     | Object type to associate (e.g., "contact", "company").                       |
| `toObjectId`       | Record ID to associate.                                                        |
| `associationTypeId` | Association type ID (numeric or snake case, retrievable via the associations API). |


## Removing an Association

`DELETE /crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


## Pinning a Call on a Record

Pin a call to a record's timeline using `hs_pinned_engagement_id` when creating or updating the record via object APIs (companies, contacts, deals, tickets, custom objects).


## Deleting Calls

Calls can be deleted individually or in batches (moves to recycling bin; restorable from the record timeline).

* **Individual Call:** `DELETE /crm/v3/objects/calls/{callId}`


**(Placeholder links need to be replaced with actual links to the relevant API documentation.)**
