# HubSpot Calls API Documentation

This document details the HubSpot Calls API, allowing you to log and manage calls within the HubSpot CRM.  This API interacts with calls logged both directly in HubSpot and through external integrations.

## API Endpoints Base URL: `/crm/v3/objects/calls`

All endpoints below use this base URL unless otherwise specified.  Replace `{callId}` with the specific call ID.

## I. Create a Call Engagement (POST)

Creates a new call engagement.

**Request:**

* **Method:** `POST`
* **URL:** `/crm/v3/objects/calls`
* **Headers:**  `Content-Type: application/json`,  HubSpot API Key
* **Body:** JSON object with `properties` and optionally `associations`

**Example Request Body:**

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27T12:00:00Z",  // UTC timestamp or Unix timestamp in milliseconds
    "hs_call_body": "Discussion about new project.",
    "hs_call_callee_object_id": "12345", // HubSpot ID of the contact/company
    "hs_call_callee_object_type": "CONTACT", // CONTACT or COMPANY
    "hs_call_direction": "OUTBOUND", // OUTBOUND or INBOUND
    "hs_call_disposition": "f240bbac-87c9-4f6e-bf70-924b57d47db7", // GUID for call outcome (e.g., Connected)
    "hs_call_duration": 360000, // Duration in milliseconds
    "hs_call_from_number": "+15551234567",
    "hs_call_recording_url": "https://example.com/recording.mp3",
    "hs_call_status": "COMPLETED",
    "hs_call_title": "Project Kickoff",
    "hs_call_source": "INTEGRATIONS_PLATFORM", //Required for recording/transcription pipeline
    "hs_call_to_number": "+15559876543",
    "hubspot_owner_id": "67890", // HubSpot ID of the owner
    "hs_activity_type": "Sales Call" //Based on call types in your HubSpot account
  },
  "associations": [
    {
      "to": { "id": 12345 },
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 194 }] //194 is example, check HubSpot docs for your associationTypeId.
    }
  ]
}
```

**Response:** (Successful)

```json
{
  "id": "newlyCreatedCallId",
  // ... other properties ...
}
```

**Properties:**  See detailed description in original text.


## II. Retrieve Calls (GET)

**A. Retrieve a Single Call:**

* **Method:** `GET`
* **URL:** `/crm/v3/objects/calls/{callId}`
* **Parameters:** `properties` (comma-separated list), `associations` (comma-separated list of object types)

**B. Retrieve Multiple Calls:**

* **Method:** `GET`
* **URL:** `/crm/v3/objects/calls`
* **Parameters:** `limit` (maximum results per page), `properties` (comma-separated list)


## III. Identify Voicemails vs. Recorded Calls (GET)

Retrieve a call using `GET /crm/v3/objects/calls/{callId}` and check the `hs_call_status` and `hs_call_has_voicemail` properties.  `hs_call_has_voicemail: true` and `hs_call_status: missed` indicates a voicemail.


## IV. Update a Call (PATCH)

Updates an existing call.

* **Method:** `PATCH`
* **URL:** `/crm/v3/objects/calls/{callId}`
* **Body:** JSON object with `properties` to update.  Omit properties to leave them unchanged.  Use an empty string to clear a property value.


**Example Request Body:**

```json
{
  "properties": {
    "hs_call_body": "Updated call notes."
  }
}
```


## V. Associate Existing Calls with Records (PUT)

Associates an existing call with a record.

* **Method:** `PUT`
* **URL:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


## VI. Remove an Association (DELETE)

Removes an association between a call and a record.

* **Method:** `DELETE`
* **URL:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


## VII. Pin a Call on a Record

Pinning is done through the record's API (contacts, companies, etc.), using the `hs_pinned_engagement_id` property when creating or updating the record.


## VIII. Delete a Call (DELETE)

Deletes a call (moves it to the recycling bin).

* **Method:** `DELETE`
* **URL:** `/crm/v3/objects/calls/{callId}`


**Note:**  The above descriptions provide a high-level overview.  Refer to the HubSpot API documentation for detailed information on parameters, error handling, rate limits, and more.  Always check the official HubSpot documentation for the most up-to-date information and specific GUIDs for call dispositions and association types.
