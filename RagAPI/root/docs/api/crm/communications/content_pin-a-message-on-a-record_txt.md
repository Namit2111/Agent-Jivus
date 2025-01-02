# HubSpot Communications API Documentation

This document details the HubSpot Communications API, allowing you to log external communications (WhatsApp, LinkedIn, SMS) to CRM records.  Note: This API does *not* apply to marketing SMS messages.

## API Endpoints

All endpoints are based on `/crm/v3/objects/communications`.  Replace `{communicationId}` with the ID of the specific communication.

### 1. Create a Communication (POST)

**Endpoint:** `/crm/v3/objects/communications`

**Method:** `POST`

**Request Body:**

The request body requires a `properties` object and optionally an `associations` array.

**`properties` Object:**

| Parameter                     | Description                                                                                             | Type     | Example                                      |
|---------------------------------|---------------------------------------------------------------------------------------------------------|----------|----------------------------------------------|
| `hs_communication_channel_type` | Channel type: `WHATS_APP`, `LINKEDIN_MESSAGE`, or `SMS`.                                                 | String   | `"SMS"`                                       |
| `hs_communication_logged_from` | Must be `"CRM"`.                                                                                      | String   | `"CRM"`                                       |
| `hs_communication_body`       | Message text body.                                                                                      | String   | `"Texted Linda to confirm the contract."`     |
| `hubspot_owner_id`            | ID of the owner associated with the message (determines the creator on the record timeline).         | Integer  | `1234567`                                    |
| `hs_timestamp`                 | Message creation time (Unix timestamp in milliseconds or UTC format).                              | String   | `"2024-03-08T10:00:00Z"` or `1678300000000` |


**`associations` Array (Optional):**

Associates the message with existing records.  Each element has:

| Field          | Description                                                   | Type      | Example          |
|-----------------|---------------------------------------------------------------|-----------|-------------------|
| `to`            | Record to associate (object ID).                              | Object    | `{"id": 9001}`    |
| `types`         | Association type.                                             | Array     | See below         |
| `types[].associationCategory` | Typically `HUBSPOT_DEFINED`.                             | String    | `"HUBSPOT_DEFINED"` |
| `types[].associationTypeId`  | Association type ID (see [Default Association Type IDs](link_to_default_ids) or use the Associations API). | Integer   | `87`              |


**Example Request:**

```json
{
  "properties": {
    "hs_communication_channel_type": "SMS",
    "hs_communication_logged_from": "CRM",
    "hs_communication_body": "Texted Linda...",
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
  "id": "12021896773",
  "properties": {
    "hs_communication_channel_type": "SMS",
    // ... other properties
  },
  "createdAt": "...",
  "updatedAt": "...",
  "archived": false
}
```


### 2. Retrieve a Communication (GET)

**Endpoint:** `/crm/v3/objects/communications/{communicationId}`  or `/crm/v3/objects/communications` (for batch retrieval)

**Method:** `GET`

**Query Parameters:**

| Parameter     | Description                                                                            | Type    |
|-----------------|----------------------------------------------------------------------------------------|---------|
| `properties`   | Comma-separated list of properties to return.                                         | String  |
| `associations` | Comma-separated list of object types to retrieve associated IDs for.                   | String  |
| `limit`         | (For batch retrieval) Limit the number of results.                                   | Integer |
| `archived`      | Filter for archived (true) or unarchived (false) communications. Default is `false`. | Boolean |


**Example Request (single):**

`GET /crm/v3/objects/communications/12021896773?properties=hs_communication_body`

**Example Request (batch):**

`GET /crm/v3/objects/communications?limit=10&properties=hs_communication_body,hs_timestamp&associations=contact`

**Example Response (single):**  Similar to the POST response, but only includes requested properties.

**Example Response (batch):** An array of communication objects, each similar to the single response.


### 3. Update a Communication (PATCH)

**Endpoint:** `/crm/v3/objects/communications/{communicationId}`

**Method:** `PATCH`

**Request Body:**

Only include the properties you wish to update.  HubSpot ignores read-only and non-existent properties.  An empty string clears a property value.


**Example Request:**

```json
{
  "properties": {
    "hs_communication_body": "Updated message text"
  }
}
```


### 4. Associate an Existing Communication (PUT)

**Endpoint:** `/crm/v3/objects/communications/{communicationId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `PUT`

**Path Parameters:**

| Parameter        | Description                                           | Example    |
|--------------------|-------------------------------------------------------|------------|
| `communicationId` | ID of the communication.                              | `12345`     |
| `toObjectType`   | Object type to associate (e.g., `contact`, `company`). | `contact`   |
| `toObjectId`     | ID of the object to associate.                         | `67890`     |
| `associationTypeId` | Association type ID.                                   | `87`        |


### 5. Remove an Association (DELETE)

**Endpoint:** `/crm/v3/objects/communications/{communicationId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `DELETE`  (Same endpoint as PUT for association)


### 6. Delete a Communication (DELETE)

**Endpoint:** `/crm/v3/objects/communications/{communicationId}`

**Method:** `DELETE`


### 7. Pin a Message (Update Record)

Pinning is achieved indirectly by including the message's `id` in the `hs_pinned_engagement_id` field when updating a record via the relevant object API (contacts, companies, etc.). This is not a direct API call to the communications endpoint.



This documentation provides a comprehensive overview.  Refer to the HubSpot developer portal for the most up-to-date information and detailed examples, including error handling and authentication details.  Remember to replace placeholder IDs and values with your actual data.
