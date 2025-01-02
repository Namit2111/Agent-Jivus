# HubSpot Communications API Documentation

This document details the HubSpot Communications API, allowing you to log external communications (WhatsApp, LinkedIn, SMS) to CRM records.  Note: This API does *not* apply to marketing SMS messages.

## API Endpoints

All endpoints are under the base URL: `https://api.hubapi.com/crm/v3/objects/`

### 1. Create a Communication (POST)

**Endpoint:** `/communications`

**Method:** `POST`

**Request Body:**

```json
{
  "properties": {
    "hs_communication_channel_type": "SMS", // or "WHATS_APP", "LINKEDIN_MESSAGE"
    "hs_communication_logged_from": "CRM",
    "hs_communication_body": "Your message text here",
    "hs_timestamp": "2024-10-27T10:30:00Z", // UTC format or Unix timestamp in milliseconds
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
          "associationTypeId": 87 // Association type ID (see default IDs or use Associations API)
        }
      ]
    },
    {
      "to": {
        "id": 1234 // ID of another associated record (optional)
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 81 // Another association type ID
        }
      ]
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


**`properties` Field Details:**

| Parameter                  | Description                                                                   |
|---------------------------|-------------------------------------------------------------------------------|
| `hs_communication_channel_type` | `WHATS_APP`, `LINKEDIN_MESSAGE`, or `SMS`                                   |
| `hs_communication_logged_from` | Must be `"CRM"`                                                              |
| `hs_communication_body`     | The message text.                                                            |
| `hubspot_owner_id`         | ID of the HubSpot user associated with the message.                          |
| `hs_timestamp`             | Message creation time (UTC format or Unix timestamp in milliseconds).           |


**`associations` Field Details:**

| Field        | Description                                                                     |
|--------------|---------------------------------------------------------------------------------|
| `to.id`      | ID of the record to associate with (e.g., Contact ID).                         |
| `types`      | Array of association types.                                                     |
| `types[].associationCategory` | `"HUBSPOT_DEFINED"`                                                          |
| `types[].associationTypeId`  | Unique ID for association type (find default IDs in HubSpot documentation). |


### 2. Retrieve Communications (GET)

**Endpoint:** `/communications` or `/communications/{communicationId}`

**Method:** `GET`

**Query Parameters (for `/communications`):**

| Parameter    | Description                                                                       |
|--------------|-----------------------------------------------------------------------------------|
| `properties` | Comma-separated list of properties to return.                                     |
| `associations` | Comma-separated list of object types to retrieve associated IDs for.             |
| `limit`       | Number of results to return (default is 100).                                   |
| `archived`     | `true` or `false` (default is `false`).                                         |


**Example Request:**  `https://api.hubapi.com/crm/v3/objects/communications?limit=10&properties=hs_communication_body&associations=contact&archived=false`


### 3. Update a Communication (PATCH)

**Endpoint:** `/communications/{communicationId}`

**Method:** `PATCH`

**Request Body:**

```json
{
  "properties": {
    "hs_communication_body": "Updated message text"
  }
}
```

### 4. Associate an Existing Communication (PUT)

**Endpoint:** `/communications/{communicationId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `PUT`

**Path Parameters:**

| Parameter       | Description                                                                 |
|-----------------|-----------------------------------------------------------------------------|
| `communicationId` | ID of the communication.                                                    |
| `toObjectType`   | Object type (e.g., `contact`, `company`).                                     |
| `toObjectId`     | ID of the object to associate.                                               |
| `associationTypeId` | Association type ID (numerical or snake case, retrieved via Associations API). |


### 5. Remove an Association (DELETE)

**Endpoint:** `/communications/{communicationId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `DELETE`


### 6. Delete a Communication (DELETE)

**Endpoint:** `/communications/{communicationId}`

**Method:** `DELETE`


### 7. Pin a Message (Update Record via Object APIs)

To pin a message, include the message's `id` in the `hs_pinned_engagement_id` field when creating or updating a record using the relevant object API (Contacts, Companies, Deals, etc.).


## Error Handling

The API will return standard HTTP status codes to indicate success or failure.  Error responses will include details about the error.


This documentation provides a concise overview. Refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications.
