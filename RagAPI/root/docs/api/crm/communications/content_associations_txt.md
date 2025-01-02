# HubSpot Communications API Documentation

This document details the HubSpot Communications API, allowing you to log external communications (WhatsApp, LinkedIn, SMS) to CRM records.  Note: This API does *not* apply to marketing SMS messages.

## API Endpoints

All endpoints are under the base URL: `https://api.hubapi.com/crm/v3/objects/`.

### 1. Create a Communication (POST `/communications`)

Creates a new communication record.

**Request:**

* **Method:** `POST`
* **URL:** `/communications`
* **Headers:**  `Content-Type: application/json`  (and your HubSpot API key)
* **Request Body (JSON):**

```json
{
  "properties": {
    "hs_communication_channel_type": "SMS", // WHATS_APP, LINKEDIN_MESSAGE, SMS
    "hs_communication_logged_from": "CRM",
    "hs_communication_body": "Your message text here",
    "hs_timestamp": "2024-10-27T10:30:00Z", // UTC timestamp or Unix timestamp in milliseconds
    "hubspot_owner_id": 1234567 // HubSpot user ID
  },
  "associations": [
    {
      "to": {
        "id": 9001 // ID of the associated record (e.g., contact ID)
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 87 // Association type ID (see notes below)
        }
      ]
    }
  ]
}
```

**Response (JSON):**  A successful response will include the newly created communication's ID.

```json
{
  "id": "12021896773",
  "properties": {
    "hs_communication_channel_type": "SMS",
    "hs_communication_logged_from": "CRM",
    "hs_communication_body": "Your message text here",
    "hs_timestamp": "2024-10-27T10:30:00Z",
    "hs_createdate": "2024-10-27T10:30:00.484Z",
    "hs_lastmodifieddate": "2024-10-27T10:30:00.484Z",
    "hs_object_id": "12021896773"
  },
  "createdAt": "2024-10-27T10:30:00.484Z",
  "updatedAt": "2024-10-27T10:30:00.484Z",
  "archived": false
}
```

**Notes:**

* `associationTypeId` values can be found in the HubSpot [associations API](<link_to_associations_api_if_available>).  Common types are listed in the original text.


### 2. Retrieve Communications (GET `/communications`)

Retrieves communication records.  Can retrieve individual messages or lists.

**Individual Message:**

* **Method:** `GET`
* **URL:** `/communications/{communicationId}`
* **Query Parameters:** `properties` (comma-separated list of properties), `associations` (comma-separated list of object types)


**List of Messages:**

* **Method:** `GET`
* **URL:** `/communications`
* **Query Parameters:** `properties`, `associations`, `limit`, `archived` (true/false)


**Example (List):**

`https://api.hubapi.com/crm/v3/objects/communications?limit=10&properties=hs_communication_body&associations=contact&archived=false`

### 3. Update a Communication (PATCH `/communications/{communicationId}`)

Updates an existing communication record.

* **Method:** `PATCH`
* **URL:** `/communications/{communicationId}`
* **Request Body (JSON):**

```json
{
  "properties": {
    "hs_communication_body": "Updated message text"
  }
}
```

### 4. Associate an Existing Communication with a Record (PUT `/communications/{communicationId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates a communication with another CRM record.

* **Method:** `PUT`
* **URL:** `/communications/{communicationId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`
  * `{communicationId}`: ID of the communication.
  * `{toObjectType}`: Object type (e.g., `contact`, `company`).
  * `{toObjectId}`: ID of the record to associate with.
  * `{associationTypeId}`: Association type ID.

### 5. Remove an Association (DELETE `/communications/{communicationId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Removes an association between a communication and a record.

* **Method:** `DELETE`
* **URL:** Same as PUT association endpoint.

### 6. Delete a Communication (DELETE `/communications/{communicationId}`)

Deletes a communication record (moves it to the recycle bin).

* **Method:** `DELETE`
* **URL:** `/communications/{communicationId}`


## Pinning Messages

To pin a message to a record's timeline, include its ID in the `hs_pinned_engagement_id` field when creating or updating the record using the relevant object API (contacts, companies, etc.). Only one activity can be pinned per record.


This documentation provides a concise overview. Refer to the HubSpot Developer portal for complete details and handling of error responses.
