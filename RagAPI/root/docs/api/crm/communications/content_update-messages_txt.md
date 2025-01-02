# HubSpot Communications API Documentation

This document describes the HubSpot Communications API, allowing you to log external communications (WhatsApp, LinkedIn, SMS) on CRM records.  Note: This API does *not* apply to marketing SMS messages.

## API Endpoints

All endpoints are under the base URL: `https://api.hubapi.com/crm/v3/objects/communications`

### 1. Create a Communication

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/communications`

**Request Body:**

The request body contains a `properties` object and an optional `associations` object.

**Properties Object:**

| Parameter                 | Description                                                                                   | Type      | Example                                     |
|--------------------------|-----------------------------------------------------------------------------------------------|-----------|---------------------------------------------|
| `hs_communication_channel_type` | The communication channel (WHATS_APP, LINKEDIN_MESSAGE, SMS).                              | String    | `"SMS"`                                      |
| `hs_communication_logged_from` | Must be set to `"CRM"`.                                                                       | String    | `"CRM"`                                      |
| `hs_communication_body`     | The message body.                                                                            | String    | `"Texted Linda to confirm the contract."`     |
| `hubspot_owner_id`         | ID of the owner associated with the message (determines the creator on the record timeline). | Integer   | `1234567`                                  |
| `hs_timestamp`            | Message creation time (Unix timestamp in milliseconds or UTC format).                        | String    | `"2024-03-08T10:00:00Z"` or `1678326400000` |


**Associations Object (Optional):**

This object associates the message with existing CRM records.  You can associate with multiple records.

```json
"associations": [
  {
    "to": { "id": 9001 }, // ID of the record
    "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 87 } ] // Association type (see below)
  },
  {
    "to": { "id": 1234 },
    "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 81 } ]
  }
]
```

* **`to.id`**: The ID of the record to associate with (e.g., Contact ID, Company ID).
* **`types`**:  An array defining the association type.  `associationTypeId` can be found using the HubSpot Associations API or using default values (listed in HubSpot's documentation).


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

**Response:**

```json
{
  "id": "12021896773",
  "properties": { ... },
  "createdAt": "...",
  "updatedAt": "...",
  "archived": false
}
```

The response includes the newly created communication's ID and other properties.


### 2. Retrieve Communications

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/communications`  or `/crm/v3/objects/communications/{communicationId}` (for individual retrieval)

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.
* `archived`: Boolean (true/false) to filter for archived communications (defaults to false).
* `limit`: Number of communications to return per page (pagination supported).


**Example Request (retrieving multiple):**

`https://api.hubapi.com/crm/v3/objects/communications?properties=hs_communication_body&associations=contact&archived=false&limit=10`


**Example Request (retrieving single):**

`https://api.hubapi.com/crm/v3/objects/communications/12021896773`


**Response:**  Similar structure to the create response, but will return a single object for individual retrieval and a list of objects for multiple retrieval.



### 3. Update a Communication

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/communications/{communicationId}`

**Request Body:**

Only include the properties you want to update.  HubSpot ignores read-only and non-existent properties.  To clear a property, pass an empty string.

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

**Endpoint:** `/crm/v3/objects/communications/{communicationId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Path Parameters:**

* `communicationId`: The ID of the communication.
* `toObjectType`: The object type (e.g., "contact", "company").
* `toObjectId`: The ID of the record.
* `associationTypeId`: The association type ID (obtainable via the Associations API).

### 5. Remove an Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/communications/{communicationId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`  (same as association endpoint)


### 6. Delete a Communication

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/communications/{communicationId}`


### 7. Pin a Message

Pinning is done indirectly by including the `hs_pinned_engagement_id` field in the `properties` object of the record using the relevant object API (Contacts, Companies, etc.). This field accepts the ID of the message to pin.  Only one activity per record can be pinned.


## Error Handling

The API will return standard HTTP status codes and JSON error responses indicating the nature of any errors.  Check the HubSpot API documentation for details.


This documentation provides a concise overview.  Refer to the official HubSpot API documentation for the most up-to-date and comprehensive information, including details on rate limits, authentication, and advanced features.
