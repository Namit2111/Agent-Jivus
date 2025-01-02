# HubSpot Communications API Documentation

This document details the HubSpot Communications API, allowing you to log external communications (WhatsApp, LinkedIn, SMS) to CRM records.  Note: This API does *not* apply to marketing SMS messages.

## API Endpoints

All endpoints are under the base URL: `https://api.hubapi.com/crm/v3/objects/`


### 1. Create a Communication (POST)

**Endpoint:** `/communications`

**Method:** `POST`

**Request Body:**

The request body must contain a `properties` object and optionally an `associations` array.

**`properties` object:**

| Parameter                 | Description                                                                                                | Type      | Required | Example                                      |
|--------------------------|------------------------------------------------------------------------------------------------------------|-----------|----------|----------------------------------------------|
| `hs_communication_channel_type` | The communication channel (WHATS_APP, LINKEDIN_MESSAGE, SMS).                                               | String    | Yes      | `"SMS"`                                        |
| `hs_communication_logged_from` | Must be set to "CRM".                                                                                       | String    | Yes      | `"CRM"`                                        |
| `hs_communication_body`    | The text body of the message.                                                                              | String    | Yes      | `"Texted Linda to confirm the contract."`       |
| `hubspot_owner_id`         | The ID of the HubSpot user associated with the message.                                                    | Integer   | Yes      | `1234567`                                    |
| `hs_timestamp`             | Message creation timestamp (Unix timestamp in milliseconds or UTC format).                               | String/Integer | Yes      | `"2024-03-08T10:00:00Z"` or `1678348800000` |


**`associations` array (optional):**

Each element in the array associates the communication with a record.

| Field          | Description                                                                  | Type       | Required | Example                               |
|-----------------|------------------------------------------------------------------------------|------------|----------|---------------------------------------|
| `to.id`         | ID of the record to associate with (e.g., contact ID, company ID).           | Integer    | Yes      | `9001`                               |
| `types[0].associationCategory` | Association category (usually "HUBSPOT_DEFINED").                            | String     | Yes      | `"HUBSPOT_DEFINED"`                     |
| `types[0].associationTypeId` | Association type ID.  See [Default Association Type IDs](link-to-ids) or use the Associations API. | Integer    | Yes      | `87` (contact) or `81` (company)      |


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
      "to": {"id": 9001},
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 87}]
    }
  ]
}
```

**Example Response:**

```json
{
  "id": "1234567890",
  "properties": {
    // ...properties...
  },
  "createdAt": "...",
  "updatedAt": "...",
  "archived": false
}
```


### 2. Retrieve a Communication (GET)

**Endpoint:** `/communications/{communicationId}`

**Method:** `GET`

**Query Parameters:**

| Parameter     | Description                                                                   | Type      |
|----------------|-------------------------------------------------------------------------------|-----------|
| `properties`  | Comma-separated list of properties to return.                              | String    |
| `associations` | Comma-separated list of object types to retrieve associated IDs for.         | String    |


**Endpoint:** `/communications` (to retrieve a list of communications)

**Method:** `GET`


**Query Parameters (same as above)**
Also includes:
* `limit` : limits the number of results returned.

**Example Request (list):**
`https://api.hubapi.com/crm/v3/objects/communications?limit=10&properties=hs_communication_body&associations=contact&archived=false`

### 3. Update a Communication (PATCH)

**Endpoint:** `/communications/{communicationId}`

**Method:** `PATCH`

**Request Body:**

Only include the properties you want to update.  HubSpot ignores read-only and non-existent properties.  To clear a property, send an empty string.

**Example Request:**

```json
{
  "properties": {
    "hs_communication_body": "Sent a follow-up message to Carla."
  }
}
```

### 4. Associate an Existing Communication with a Record (PUT)

**Endpoint:** `/communications/{communicationId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `PUT`

**Path Parameters:**

| Parameter        | Description                                      | Type    |
|-------------------|--------------------------------------------------|---------|
| `communicationId` | ID of the communication.                         | String  |
| `toObjectType`   | Type of object to associate (e.g., "contact"). | String  |
| `toObjectId`     | ID of the object to associate.                   | String  |
| `associationTypeId` | ID of the association type.                    | Integer |


### 5. Remove an Association (DELETE)

**Endpoint:** `/communications/{communicationId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `DELETE`  (Same endpoint as PUT for associating)


### 6. Pin a Message (Update Record via Object APIs)

Pinning is done indirectly by including the message's `id` in the `hs_pinned_engagement_id` field when creating or updating a record using the relevant object API (Contacts, Companies, Deals, etc.).

### 7. Delete a Communication (DELETE)

**Endpoint:** `/communications/{communicationId}`

**Method:** `DELETE`


## Error Handling

The API will return standard HTTP status codes and error responses in JSON format to indicate success or failure.  Refer to HubSpot's API documentation for detailed error codes.


This documentation provides a comprehensive overview of the HubSpot Communications API.  Remember to consult the official HubSpot API documentation for the most up-to-date information and detailed specifications.  Replace  `link-to-ids` with the actual link to the default association type IDs in the HubSpot documentation.
