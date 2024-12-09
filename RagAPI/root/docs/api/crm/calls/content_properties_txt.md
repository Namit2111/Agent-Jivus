# HubSpot Calls API Documentation

This document details the HubSpot API endpoints for managing call engagements.  This API allows you to log, manage, and retrieve call data within the HubSpot CRM.

## Calls Endpoint Reference

The Calls API provides methods for interacting with call records.  For a complete list of endpoints and their requirements, refer to the "Endpoints" tab (presumably within the HubSpot interface, not present in the provided text).

### Create a Call Engagement

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/calls`

Creates a new call engagement. The request body requires a `properties` object containing call details and an optional `associations` object to link the call to existing HubSpot records (e.g., contacts, companies).

#### Properties

| Field                     | Description                                                                                                                                                                                             |
|--------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `hs_timestamp`           | **Required.** Call creation timestamp. Use Unix timestamp in milliseconds or UTC format (e.g., "2024-10-27T10:30:00.000Z").                                                                               |
| `hs_call_body`           | Call description and notes.                                                                                                                                                                            |
| `hs_call_callee_object_id` | ID of the associated HubSpot record. For outbound calls, this is the recipient; for inbound calls, this is the caller.                                                                                  |
| `hs_call_callee_object_type` | Object type of the associated record (e.g., "contact", "company"). For outbound calls, this is the recipient's type; for inbound calls, this is the caller's type.                                           |
| `hs_call_direction`       | Call direction ("INBOUND" or "OUTBOUND") from the HubSpot user's perspective.                                                                                                                      |
| `hs_call_disposition`     | Call outcome. Use the internal GUID value. Default values and custom GUIDs can be found via the [properties API](link_to_properties_api_needed).  Examples: <br> `Busy`: `9d9162e7-6cf3-4944-bf63-4dff82258764` <br> `Connected`: `f240bbac-87c9-4f6e-bf70-924b57d47db7` |
| `hs_call_duration`        | Call duration in milliseconds.                                                                                                                                                                           |
| `hs_call_from_number`     | Calling phone number.                                                                                                                                                                                |
| `hs_call_recording_url`   | URL of the call recording (HTTPS only, .mp3 or .wav).                                                                                                                                               |
| `hs_call_status`          | Call status (e.g., "BUSY", "COMPLETED", "IN_PROGRESS").                                                                                                                                                  |
| `hs_call_title`           | Call title.                                                                                                                                                                                          |
| `hs_call_source`          | Call source.  Required for recording and transcription pipelines; must be "INTEGRATIONS_PLATFORM".                                                                                             |
| `hs_call_to_number`       | Called phone number.                                                                                                                                                                                |
| `hubspot_owner_id`        | ID of the HubSpot user associated with the call.                                                                                                                                                        |
| `hs_activity_type`        | Type of call (based on call types in your HubSpot account).                                                                                                                                            |
| `hs_attachment_ids`       | IDs of attached files (semicolon-separated).                                                                                                                                                           |


#### Associations

To associate the call with existing records, include an `associations` array in the request body. Each association object should contain:

| Field       | Description                                                                          |
|-------------|--------------------------------------------------------------------------------------|
| `to.id`     | ID of the record to associate.                                                      |
| `types`     | Array of association types. Each object needs `associationCategory` ("HUBSPOT_DEFINED") and `associationTypeId` (retrieve via the [associations API](link_to_associations_api_needed)). |


### Retrieve Calls

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/calls` (for all calls) or `/crm/v3/objects/calls/{callId}` (for a single call)

Retrieves call data.  Parameters such as `limit` (for pagination) and `properties` (to specify returned fields) can be used.  The `associations` parameter can retrieve associated record IDs.

### Identify Voicemails vs. Recorded Calls

To distinguish between recorded calls and voicemails, check the `hs_call_status` ("missed") and `hs_call_has_voicemail` (`true` for voicemail, `false` for recorded call, `null` otherwise) properties.  Requires inbound calling access.


### Update Calls

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/calls/{callId}`

Updates an existing call.  Provide a `properties` object with the fields to modify. HubSpot ignores read-only and non-existent properties.  An empty string clears a property value.

### Associate Existing Calls with Records

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

Associates a call with a record.

| Field           | Description                                                                    |
|-----------------|--------------------------------------------------------------------------------|
| `callId`         | ID of the call.                                                                 |
| `toObjectType`   | Object type (e.g., "contact", "company").                                          |
| `toObjectId`     | ID of the record.                                                               |
| `associationTypeId` | Association type ID (retrieve via the [associations API](link_to_associations_api_needed)). |

### Remove an Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

Removes an association between a call and a record. Uses the same endpoint as associating a call.

### Pin a Call on a Record

Pins a call to the top of a record's timeline. Requires pre-existing association. Use the `hs_pinned_engagement_id` field when creating or updating the record via the object APIs ([companies](link_to_companies_api_needed), [contacts](link_to_contacts_api_needed), [deals](link_to_deals_api_needed), [tickets](link_to_tickets_api_needed), [custom objects](link_to_custom_objects_api_needed) APIs).


### Delete Calls

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/calls/{callId}`

Deletes a call (moves it to the recycling bin).


**Note:**  Placeholders like `link_to_properties_api_needed` need to be replaced with actual links to the relevant HubSpot API documentation.  Similarly, the "Endpoints" tab reference needs clarification within the context of the HubSpot user interface.
