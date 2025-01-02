# HubSpot Calls API Documentation

This document details the HubSpot Calls API, allowing you to manage calls within the HubSpot CRM.  It covers creating, retrieving, updating, associating, and deleting calls.

## API Endpoints Base URL: `/crm/v3/objects/calls`

All endpoints below are relative to this base URL.  Replace `{callId}` with the actual call ID.

## 1. Create a Call Engagement (POST)

Creates a new call engagement.

**Request:**

* **Method:** `POST`
* **URL:** `/crm/v3/objects/calls`
* **Headers:**  `Authorization: Bearer <your_api_key>`
* **Body (JSON):**

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27T12:00:00Z", // Required. UTC timestamp or Unix timestamp in milliseconds.
    "hs_call_body": "Call summary...",
    "hs_call_callee_object_id": 123, // ID of associated HubSpot record (Contact, Company, etc.)
    "hs_call_callee_object_type": "CONTACT", // Type of associated record
    "hs_call_direction": "OUTBOUND", // or "INBOUND"
    "hs_call_disposition": "f240bbac-87c9-4f6e-bf70-924b57d47db7", // GUID for call outcome (e.g., "Connected")  See below for default values.
    "hs_call_duration": 360000, // Duration in milliseconds
    "hs_call_from_number": "+15551234567",
    "hs_call_recording_url": "https://example.com/recording.mp3", // HTTPS URL only
    "hs_call_status": "COMPLETED", // See API reference for possible values
    "hs_call_title": "Client Check-in",
    "hs_call_source": "INTEGRATIONS_PLATFORM", // Required for recording/transcription pipeline
    "hs_call_to_number": "+15559876543",
    "hubspot_owner_id": 1, // ID of the HubSpot user
    "hs_activity_type": "Phone Call", //Based on call types in your HubSpot account
    "hs_attachment_ids": "123;456" //Multiple attachment IDs separated by semicolon
  },
  "associations": [
    {
      "to": {"id": 123},
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 194}] //Example association to contact
    }
  ]
}
```

**Default `hs_call_disposition` GUIDs:**

* Busy: `9d9162e7-6cf3-4944-bf63-4dff82258764`
* Connected: `f240bbac-87c9-4f6e-bf70-924b57d47db7`
* Left live message: `a4c4c377-d246-4b32-a13b-75a56a4cd0ff`
* Left voicemail: `b2cf5968-551e-4856-9783-52b3da59a7d0`
* No answer: `73a0d17f-1163-4015-bdd5-ec830791da20`
* Wrong number: `17b47fee-58de-441e-a44c-c6300d46f273`


**Response (JSON):**  A JSON object representing the created call, including the `callId`.


## 2. Retrieve Calls (GET)

**A. Retrieve a Single Call:**

* **Method:** `GET`
* **URL:** `/crm/v3/objects/calls/{callId}?properties=hs_call_title,hs_call_duration&associations=contact`
* **Parameters:**
    * `properties`: Comma-separated list of properties to return.
    * `associations`: Comma-separated list of object types to retrieve associated IDs for.

**B. Retrieve a List of Calls:**

* **Method:** `GET`
* **URL:** `/crm/v3/objects/calls?limit=10&properties=hs_call_title`
* **Parameters:**
    * `limit`: Maximum number of results per page.
    * `properties`: Comma-separated list of properties to return.

**Response (JSON):** A JSON object containing the requested call(s) or a paginated list of calls.


## 3. Update a Call (PATCH)

Updates an existing call.

* **Method:** `PATCH`
* **URL:** `/crm/v3/objects/calls/{callId}`
* **Body (JSON):**  Similar to the POST request body, but only include the properties you want to update.


## 4. Associate Existing Calls with Records (PUT)

Associates an existing call with a record (e.g., Contact, Company).

* **Method:** `PUT`
* **URL:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`
* **Parameters:**
    * `{toObjectType}`:  e.g., `contact`, `company`
    * `{toObjectId}`: ID of the record to associate.
    * `{associationTypeId}`: Association type ID (obtainable via the Associations API).


## 5. Remove an Association (DELETE)

Removes an association between a call and a record.

* **Method:** `DELETE`
* **URL:** `/crm/v3/objects/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


## 6. Pin a Call on a Record

Pinning is done through the record's API (Contacts, Companies, etc.) by including the call's `id` in the `hs_pinned_engagement_id` property when creating or updating the record.


## 7. Delete a Call (DELETE)

Deletes a call (moves it to the recycling bin).

* **Method:** `DELETE`
* **URL:** `/crm/v3/objects/calls/{callId}`


##  Error Handling

The API will return appropriate HTTP status codes (e.g., 400 Bad Request, 404 Not Found, etc.) and JSON error responses with details.


This documentation provides a concise overview. Refer to the official HubSpot API documentation for comprehensive details and the full list of endpoints and their capabilities. Remember to replace placeholders like `<your_api_key>`, `{callId}`, etc., with your actual values.
