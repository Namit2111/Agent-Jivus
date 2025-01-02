# HubSpot Communications API Documentation

This document details the HubSpot Communications API, allowing you to log external communications (WhatsApp, LinkedIn, SMS) on CRM records.  Note: This API does *not* apply to marketing SMS messages.

## API Endpoints

All endpoints are under the base URL: `https://api.hubapi.com/crm/v3/objects/`

### 1. Create a Communication

**Endpoint:** `/communications`

**Method:** `POST`

**Request Body:**

The request body contains a `properties` object and an optional `associations` object.

* **`properties` object:**

| Parameter                 | Description                                                                                                  | Type      | Example                                      |
|--------------------------|--------------------------------------------------------------------------------------------------------------|-----------|----------------------------------------------|
| `hs_communication_channel_type` | Channel type (WHATS_APP, LINKEDIN_MESSAGE, SMS)                                                              | String    | `"SMS"`                                        |
| `hs_communication_logged_from` | Must be "CRM"                                                                                                  | String    | `"CRM"`                                        |
| `hs_communication_body`     | Message text body                                                                                             | String    | `"Texted Linda to confirm the contract."`       |
| `hubspot_owner_id`         | ID of the message owner (HubSpot user)                                                                        | Integer   | `1234567`                                     |
| `hs_timestamp`             | Message creation time (Unix timestamp in milliseconds or UTC format)                                           | String    | `"2024-03-08T10:00:00Z"` or `1678326400000` |


* **`associations` object (optional):**  Associates the message with CRM records.

```json
[
  {
    "to": { "id": 9001 }, // ID of the associated record (e.g., Contact ID)
    "types": [
      {
        "associationCategory": "HUBSPOT_DEFINED",
        "associationTypeId": 87 // Association type ID (see HubSpot docs for default IDs)
      }
    ]
  },
  {
    "to": { "id": 1234 }, // ID of another associated record (e.g., Company ID)
    "types": [
      {
        "associationCategory": "HUBSPOT_DEFINED",
        "associationTypeId": 81
      }
    ]
  }
]
```

**Example Request:**

```json
{
  "properties": {
    "hs_communication_channel_type": "SMS",
    "hs_communication_logged_from": "CRM",
    "hs_communication_body": "Texted Linda to confirm the contract.",
    "hs_timestamp": "2024-03-08T10:00:00Z",
    "hubspot_owner_id": 1234567
  },
  "associations": [
    {
      "to": { "id": 9001 },
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 87 }]
    }
  ]
}
```

**Response:**

```json
{
  "id": "12021896773",
  "properties": {
    "hs_communication_channel_type": "SMS",
    "hs_communication_logged_from": "CRM",
    "hs_communication_body": "Texted John to confirm the contract.",
    "hs_timestamp": "2022-11-12T15:48:22Z",
    "hs_createdate": "2024-03-08T10:00:00Z",
    "hs_lastmodifieddate": "2024-03-08T10:00:00Z",
    "hs_object_id": "12021896773"
  },
  "createdAt": "2024-03-08T10:00:00Z",
  "updatedAt": "2024-03-08T10:00:00Z",
  "archived": false
}
```

The response includes the newly created communication's ID.


### 2. Retrieve Communications

**Endpoint:** `/communications` or `/communications/{communicationId}`

**Method:** `GET`

**Query Parameters (for `/communications`):**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.
* `limit`: Number of records to return (default 100).  (For `/communications` only)
* `archived`: Boolean (true/false) to filter by archived status. (For `/communications` only)


**Example Request (retrieve all SMS communications with body and associated contact):**

`https://api.hubapi.com/crm/v3/objects/communications?properties=hs_communication_body&associations=contact&archived=false`


**Response:**  A list of communication objects (for `/communications`) or a single communication object (for `/communications/{communicationId}`).  The structure is similar to the response from the POST request.


### 3. Update a Communication

**Endpoint:** `/communications/{communicationId}`

**Method:** `PATCH`

**Request Body:**

```json
{
  "properties": {
    "hs_communication_body": "Sent a follow-up message to Carla."
  }
}
```

Only the properties you want to update need to be included.  HubSpot ignores read-only and non-existent properties.  To clear a property, pass an empty string.


### 4. Associate an Existing Communication with a Record

**Endpoint:** `/communications/{communicationId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `PUT`

**Path Parameters:**

* `communicationId`: ID of the communication.
* `toObjectType`: Object type (e.g., "contact", "company").
* `toObjectId`: ID of the record to associate.
* `associationTypeId`: Association type ID (obtainable via the Associations API).


### 5. Remove an Association

**Endpoint:** `/communications/{communicationId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `DELETE`

Same endpoint as associating, but uses the DELETE method to remove the association.


### 6. Pin a Message on a Record

Pinning is done indirectly through the `hs_pinned_engagement_id` field when creating or updating records using other HubSpot object APIs (Contacts, Companies, etc.).


### 7. Delete a Communication

**Endpoint:** `/communications/{communicationId}`

**Method:** `DELETE`


This documentation provides a concise overview. Refer to the official HubSpot API documentation for the most up-to-date information and details on error handling, rate limits, and authentication.
