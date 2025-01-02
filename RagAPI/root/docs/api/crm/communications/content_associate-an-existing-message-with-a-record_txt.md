# HubSpot Communications API Documentation

This document details the HubSpot Communications API, allowing you to log external communications (WhatsApp, LinkedIn, SMS) on CRM records.  Note: This API does *not* apply to marketing SMS messages.

## API Endpoints

All endpoints are under the base URL: `https://api.hubapi.com/crm/v3/objects/communications`


### 1. Create a Communication (POST)

**Endpoint:** `/crm/v3/objects/communications`

**Method:** `POST`

**Request Body:**

The request body requires a `properties` object and optionally an `associations` object.

**`properties` object:**

| Parameter                     | Description                                                                                                | Type     | Example                                          |
|---------------------------------|------------------------------------------------------------------------------------------------------------|----------|-------------------------------------------------|
| `hs_communication_channel_type` | The communication channel (WHATS_APP, LINKEDIN_MESSAGE, SMS).                                           | String   | `"SMS"`                                           |
| `hs_communication_logged_from` | Must be set to "CRM".                                                                                    | String   | `"CRM"`                                           |
| `hs_communication_body`       | The message body.                                                                                          | String   | `"Texted Linda to confirm the contract."`          |
| `hubspot_owner_id`            | ID of the HubSpot user associated with the message.                                                       | Integer  | `1234567`                                       |
| `hs_timestamp`                 | Message creation timestamp (Unix timestamp in milliseconds or UTC format).                               | String   | `"2024-03-08T10:00:00Z"` or `1678326400000` |


**`associations` object (optional):**

Associates the message with existing CRM records.  This is an array of objects.

| Field             | Description                                                                       | Type      | Example                    |
|----------------------|-----------------------------------------------------------------------------------|-----------|-----------------------------|
| `to.id`             | ID of the record to associate (e.g., Contact ID).                              | Integer   | `9001`                       |
| `types[0].associationCategory` | Association category ("HUBSPOT_DEFINED").                                         | String    | `"HUBSPOT_DEFINED"`          |
| `types[0].associationTypeId`  | Association type ID (see [default IDs](placeholder_link_to_default_ids) or use the Associations API). | Integer   | `87` (e.g., contact association) |


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
      "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 87 } ]
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


### 2. Retrieve Communications (GET)

**Endpoint:** `/crm/v3/objects/communications`  or `/crm/v3/objects/communication/{communicationId}`

**Method:** `GET`

* **`/crm/v3/objects/communications`**: Retrieves a list of communications.  Use query parameters for filtering and pagination.
* **`/crm/v3/objects/communication/{communicationId}`**: Retrieves a single communication by its ID.

**Query Parameters (for list retrieval):**

| Parameter    | Description                                                                          | Type     |
|---------------|--------------------------------------------------------------------------------------|----------|
| `properties` | Comma-separated list of properties to return.                                     | String   |
| `associations`| Comma-separated list of object types to retrieve associated IDs for.               | String   |
| `limit`       | Number of results to return per page.                                              | Integer  |
| `archived`    | Filter by archived status (true/false).                                            | Boolean  |


**Example GET Request (list):**

`https://api.hubapi.com/crm/v3/objects/communications?limit=10&properties=hs_communication_body&associations=contact&archived=false`


### 3. Update a Communication (PATCH)

**Endpoint:** `/crm/v3/objects/communications/{communicationId}`

**Method:** `PATCH`

**Request Body:**  Only include the properties you want to update.

```json
{
  "properties": {
    "hs_communication_body": "Sent a follow-up message to Carla."
  }
}
```

### 4. Associate an Existing Communication with a Record (PUT)

**Endpoint:** `/crm/v3/objects/communications/{communicationId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `PUT`

**Path Parameters:**

| Parameter        | Description                                                              |
|-------------------|--------------------------------------------------------------------------|
| `communicationId` | ID of the communication.                                                  |
| `toObjectType`   | Type of object to associate (e.g., "contact", "company").                 |
| `toObjectId`     | ID of the object to associate.                                            |
| `associationTypeId` | ID of the association type (use Associations API to find the correct ID). |


### 5. Remove an Association (DELETE)

**Endpoint:** `/crm/v3/objects/communications/{communicationId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `DELETE`  (Same endpoint as PUT association)


### 6. Pin a Message (using Object APIs)

Pinning is done via the `hs_pinned_engagement_id` field when creating or updating records using the respective object APIs (Contacts, Companies, etc.).


### 7. Delete a Communication (DELETE)

**Endpoint:** `/crm/v3/objects/communications/{communicationId}`

**Method:** `DELETE`


This documentation provides a comprehensive overview. Refer to the HubSpot Developer portal for the most up-to-date information, including details on error handling, rate limits, and authentication.  Remember to replace placeholder links with actual links from the HubSpot documentation.
