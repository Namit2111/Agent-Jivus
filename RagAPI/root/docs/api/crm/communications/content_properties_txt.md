# HubSpot Communications API Documentation

This document details the HubSpot Communications API, allowing you to log external communications (WhatsApp, LinkedIn, SMS) on CRM records.  Note: This API does *not* apply to marketing SMS messages.

## API Endpoints

All endpoints are based on `/crm/v3/objects/communications`.  Replace `{communicationId}` with the ID of the specific communication.

### 1. Create a Communication (POST `/crm/v3/objects/communications`)

Creates a new communication record.

**Request Body:**

```json
{
  "properties": {
    "hs_communication_channel_type": "SMS", // WHATS_APP, LINKEDIN_MESSAGE, SMS
    "hs_communication_logged_from": "CRM",
    "hs_communication_body": "Message text",
    "hubspot_owner_id": 1234567, // HubSpot user ID
    "hs_timestamp": "2024-10-27T10:00:00Z" // UTC or Unix timestamp (milliseconds)
  },
  "associations": [
    {
      "to": {
        "id": 9001 // ID of the associated record (Contact, Company, etc.)
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

**Response:**

```json
{
  "id": "12021896773",
  "properties": {
    // ... properties including hs_createdate, hs_lastmodifieddate, hs_object_id ...
  },
  "createdAt": "...",
  "updatedAt": "...",
  "archived": false
}
```

**Notes:**

* `associationTypeId`:  Default IDs are listed in HubSpot's documentation.  Use the Associations API to retrieve IDs for custom association types.  `87` often represents a contact association, and `81` a company association.


### 2. Retrieve Communications (GET `/crm/v3/objects/communications` or GET `/crm/v3/objects/communications/{communicationId}`)

Retrieves communications.  Use the singular endpoint for a specific communication by ID, and the plural for a list.

**Query Parameters (for both endpoints):**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.
* `archived`: `true` or `false` to filter archived communications.  Defaults to `false`.
* `limit`: Limits the number of results returned (only for plural endpoint).

**Example GET Request:**

`https://api.hubapi.com/crm/v3/objects/communications?limit=10&properties=hs_communication_body&associations=contact&archived=false`


### 3. Update a Communication (PATCH `/crm/v3/objects/communications/{communicationId}`)

Updates an existing communication.

**Request Body:**

```json
{
  "properties": {
    "hs_communication_body": "Updated message text"
  }
}
```

HubSpot ignores read-only and non-existent properties.  Use an empty string to clear a property value.


### 4. Associate an Existing Communication (PUT `/crm/v3/objects/communications/{communicationId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates an existing communication with a CRM record.

**Path Parameters:**

* `communicationId`: ID of the communication.
* `toObjectType`: Type of object (e.g., `contact`, `company`).
* `toObjectId`: ID of the object.
* `associationTypeId`: Association type ID.


### 5. Remove an Association (DELETE `/crm/v3/objects/communications/{communicationId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Removes an association between a communication and a record.  Uses the same URL as the associate endpoint.


### 6. Pin a Communication

Pinning is handled indirectly. Include the communication's `id` in the `hs_pinned_engagement_id` field when creating or updating a record via the relevant object API (Contacts, Companies, etc.). Only one activity can be pinned per record.


### 7. Delete a Communication (DELETE `/crm/v3/objects/communications/{communicationId}`)

Deletes a communication (moves it to the recycle bin).


## Error Handling

Refer to the HubSpot API documentation for details on error codes and responses.


## Rate Limits

Be mindful of HubSpot's API rate limits to avoid throttling.  See the HubSpot API documentation for details.
