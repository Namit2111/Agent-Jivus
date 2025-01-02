# HubSpot Communications API Documentation

This document details the HubSpot Communications API, allowing you to log external communications (WhatsApp, LinkedIn, SMS) on CRM records.  Note: This API does *not* apply to marketing SMS messages.

## API Endpoints

All endpoints are located under the `/crm/v3/objects/communications` base path.  Replace `{communicationId}` with the ID of the specific communication.


## 1. Create a Communication (POST `/crm/v3/objects/communications`)

Creates a new WhatsApp, LinkedIn, or SMS message.

**Request Body:**

```json
{
  "properties": {
    "hs_communication_channel_type": "SMS", // "WHATS_APP", "LINKEDIN_MESSAGE", or "SMS"
    "hs_communication_logged_from": "CRM",
    "hs_communication_body": "Your message text here",
    "hs_timestamp": "2024-03-08T10:00:00Z", // UTC timestamp or Unix timestamp in milliseconds
    "hubspot_owner_id": 1234567 // HubSpot user ID
  },
  "associations": [
    {
      "to": {
        "id": 9001 // ID of the associated record (e.g., contact, company)
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 87 // Association type ID (see details below)
        }
      ]
    }
  ]
}
```

**Properties:**

| Parameter                  | Description                                                                        |
|---------------------------|------------------------------------------------------------------------------------|
| `hs_communication_channel_type` | The communication channel (WHATS_APP, LINKEDIN_MESSAGE, SMS).                     |
| `hs_communication_logged_from` | Must be "CRM".                                                                     |
| `hs_communication_body`     | The message text.                                                                   |
| `hubspot_owner_id`         | The ID of the HubSpot user who sent/received the message.                         |
| `hs_timestamp`             | The message timestamp (UTC or Unix milliseconds).                                  |


**Associations:**

| Field          | Description                                                                        |
|-----------------|------------------------------------------------------------------------------------|
| `to.id`         | The ID of the record to associate with (e.g., contact ID).                         |
| `types[].associationCategory` | Should be "HUBSPOT_DEFINED".                                                     |
| `types[].associationTypeId` | The ID of the association type.  Use the Associations API to retrieve IDs.  |


**Response:**

```json
{
  "id": "1234567890",
  "properties": { ... },
  "createdAt": "...",
  "updatedAt": "...",
  "archived": false
}
```

## 2. Retrieve Communications

**GET `/crm/v3/objects/communications` (List)**

Retrieves a list of communications.

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.
* `limit`: Number of results to return (default 100).
* `archived`: `true` or `false` to filter archived communications.

**Example:** `https://api.hubapi.com/crm/v3/objects/communications?limit=10&properties=hs_communication_body&associations=contact&archived=false`


**GET `/crm/v3/objects/communications/{communicationId}` (Single)**

Retrieves a single communication by its ID.  Uses the same query parameters as the list endpoint.


## 3. Update a Communication (PATCH `/crm/v3/objects/communications/{communicationId}`)

Updates an existing communication.

**Request Body:**

```json
{
  "properties": {
    "hs_communication_body": "Updated message text"
  }
}
```

Only provided properties will be updated; others remain unchanged.  To clear a property, set its value to an empty string.


## 4. Associate an Existing Communication (PUT `/crm/v3/objects/communications/{communicationId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates a communication with another CRM record.

* `{toObjectType}`:  The type of object (e.g., `contact`, `company`).
* `{toObjectId}`: The ID of the object.
* `{associationTypeId}`: The association type ID.


## 5. Remove an Association (DELETE `/crm/v3/objects/communications/{communicationId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Removes an association between a communication and a record.  Uses the same URL structure as the association creation endpoint.


## 6. Pin a Message

Pinning a message is handled indirectly. When creating or updating a record (contact, company, deal, etc.) via its respective API, include the message's `id` in the `hs_pinned_engagement_id` field.


## 7. Delete a Communication (DELETE `/crm/v3/objects/communications/{communicationId}`)

Deletes a communication (moves it to the recycle bin).


##  Error Handling

The API will return standard HTTP status codes to indicate success or failure (e.g., 200 OK, 400 Bad Request, 404 Not Found). Error details will be provided in the response body.


##  Authentication

You will need a valid HubSpot API key to use these endpoints.  Refer to the HubSpot developer documentation for authentication details.


This documentation provides a concise overview.  Refer to the official HubSpot API documentation for the most up-to-date information and comprehensive details, including handling of batch operations and further error conditions.
