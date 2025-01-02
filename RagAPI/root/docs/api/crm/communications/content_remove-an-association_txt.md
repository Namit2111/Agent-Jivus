# HubSpot Communications API Documentation

This document details the HubSpot Communications API, allowing you to log external communications (WhatsApp, LinkedIn, SMS) on CRM records.  Note: This API does *not* apply to marketing SMS messages.

## API Endpoints

All endpoints are under the base URL: `https://api.hubapi.com/crm/v3/objects/`.

### 1. Create a Communication

**Method:** `POST`

**Endpoint:** `/communications`

**Request Body:**

The request body requires a `properties` object and optionally an `associations` object.

**`properties` object:**

| Parameter                  | Description                                                                                             | Type     | Required | Example                                    |
|---------------------------|---------------------------------------------------------------------------------------------------------|----------|----------|---------------------------------------------|
| `hs_communication_channel_type` | The communication channel (WHATS_APP, LINKEDIN_MESSAGE, SMS).                                           | String   | Yes      | `"SMS"`                                      |
| `hs_communication_logged_from` | Must be "CRM".                                                                                       | String   | Yes      | `"CRM"`                                       |
| `hs_communication_body`      | The message text body.                                                                                 | String   | Yes      | `"Texted Linda to confirm the contract."`     |
| `hubspot_owner_id`          | The ID of the HubSpot user associated with the message.                                               | Integer  | Yes      | `1234567`                                   |
| `hs_timestamp`              | Message creation timestamp (Unix timestamp in milliseconds or UTC format).                            | String   | Yes      | `"2024-03-08T10:00:00Z"` or `1678326400000` |


**`associations` object:** (Optional)

This object allows associating the message with existing HubSpot records (e.g., contacts, companies).  Multiple associations are allowed.

```json
"associations": [
  {
    "to": {
      "id": 9001 // ID of the record
    },
    "types": [
      {
        "associationCategory": "HUBSPOT_DEFINED",
        "associationTypeId": 87 // Association type ID (see HubSpot docs for default IDs)
      }
    ]
  },
  {
    "to": {
      "id": 1234
    },
    "types": [
      {
        "associationCategory": "HUBSPOT_DEFINED",
        "associationTypeId": 81
      }
    ]
  }
]
```

**Request Example:**

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
      "to": {"id": 9001},
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 87}]
    }
  ]
}
```

**Response Example:**

```json
{
  "id": "12021896773",
  "properties": {
    "hs_communication_channel_type": "SMS",
    "hs_communication_logged_from": "CRM",
    "hs_communication_body": "Texted John to confirm the contract.",
    "hs_timestamp": "2022-11-12T15:48:22Z",
    "hs_createdate": "2022-11-29T18:35:00.484Z",
    "hs_lastmodifieddate": "2022-11-29T18:35:00.484Z",
    "hs_object_id": "12021896773"
  },
  "createdAt": "2022-11-29T18:35:00.484Z",
  "updatedAt": "2022-11-29T18:35:00.484Z",
  "archived": false
}
```


### 2. Retrieve Communications

**Method:** `GET`

**Endpoint:** `/communications`  (for all communications) or `/communications/{communicationId}` (for a single communication)

**Query Parameters:**

| Parameter     | Description                                                                         | Type     |
|---------------|-------------------------------------------------------------------------------------|----------|
| `properties`  | Comma-separated list of properties to return.                                      | String   |
| `associations`| Comma-separated list of object types to retrieve associated IDs for.                 | String   |
| `limit`       | Number of results to return (for `/communications` endpoint only).                | Integer  |
| `archived`    | Filter by archived status (`true` or `false`).                                  | Boolean  |


**Example Request (Retrieving all SMS messages with body and associated contacts):**

`https://api.hubapi.com/crm/v3/objects/communications?properties=hs_communication_body&associations=contact&archived=false&limit=10`


### 3. Update a Communication

**Method:** `PATCH`

**Endpoint:** `/communications/{communicationId}`

**Request Body:**

Only include the properties you want to update.  HubSpot ignores read-only and non-existent properties.  Use an empty string to clear a property value.

**Example Request:**

```json
{
  "properties": {
    "hs_communication_body": "Sent a follow-up message to Carla."
  }
}
```


### 4. Associate an Existing Communication with a Record

**Method:** `PUT`

**Endpoint:** `/communications/{communicationId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

| Parameter        | Description                                                              |
|-------------------|--------------------------------------------------------------------------|
| `communicationId`| ID of the communication.                                                |
| `toObjectType`   | Type of object to associate (e.g., "contact", "company").                 |
| `toObjectId`     | ID of the object to associate.                                          |
| `associationTypeId` | ID of the association type (retrieve via the Associations API).          |


**Example Request URL:**

`https://api.hubapi.com/crm/v3/objects/communications/12021896773/associations/contact/581751/communication_to_contact`


### 5. Remove an Association

**Method:** `DELETE`

**Endpoint:** `/communications/{communicationId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`  (same as associate)


### 6. Pin a Message (Indirectly)

Pinning is achieved by including the message's `id` in the `hs_pinned_engagement_id` field when creating or updating a record via other HubSpot object APIs (Contacts, Companies, etc.).


### 7. Delete a Communication

**Method:** `DELETE`

**Endpoint:** `/communications/{communicationId}`


##  Error Handling

The API will return standard HTTP status codes (e.g., 400 Bad Request, 404 Not Found, 500 Internal Server Error) along with JSON error responses providing details about the failure.  Refer to the HubSpot API documentation for details on error codes and responses.


This documentation provides a concise overview. Always refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications.
