# HubSpot Communications API Documentation

This document details the HubSpot Communications API, allowing you to log external communications (WhatsApp, LinkedIn, SMS) to CRM records.  Note: This API does *not* apply to marketing SMS messages.

## API Endpoints

All endpoints are prefixed with `/crm/v3/objects/`.  Replace `{communicationId}` and `{toObjectId}` with the appropriate IDs.

### 1. Create a Communication

**Method:** `POST`

**Endpoint:** `/communications`

**Request Body:**

The request body requires a `properties` object and optionally an `associations` object.

**Properties Object:**

| Parameter                  | Description                                                                                                  | Type     | Required | Example                                       |
|---------------------------|--------------------------------------------------------------------------------------------------------------|----------|----------|-----------------------------------------------|
| `hs_communication_channel_type` | Channel type (WHATS_APP, LINKEDIN_MESSAGE, SMS)                                                             | String   | Yes      | `"SMS"`                                         |
| `hs_communication_logged_from` | Must be "CRM"                                                                                                | String   | Yes      | `"CRM"`                                         |
| `hs_communication_body`     | Message text body                                                                                            | String   | Yes      | `"Texted Linda to confirm the contract."`     |
| `hubspot_owner_id`          | ID of the owner associated with the message (determines creator on record timeline)                        | Integer  | Yes      | `1234567`                                     |
| `hs_timestamp`              | Message creation time (Unix timestamp in milliseconds or UTC format)                                         | String   | Yes      | `"2024-03-08T10:00:00Z"` or `1678326400000` |


**Associations Object (Optional):**

Associates the message with existing records (contacts, companies, etc.).

```json
"associations": [
  {
    "to": { "id": 9001 }, // ID of the record to associate
    "types": [
      {
        "associationCategory": "HUBSPOT_DEFINED",
        "associationTypeId": 87 // Association type ID (see default IDs or use Associations API for custom types)
      }
    ]
  },
  {
    "to": { "id": 1234 },
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

**Example Response:**

```json
{
  "id": "12021896773",
  "properties": { ... },
  "createdAt": "2024-03-08T10:05:00.484Z",
  "updatedAt": "2024-03-08T10:05:00.484Z",
  "archived": false
}
```


### 2. Retrieve Communications

**Method:** `GET`

**Endpoint:** `/communications` (for all) or `/communication/{communicationId}` (for a specific communication)

**Query Parameters:**

| Parameter    | Description                                                                             |
|--------------|-----------------------------------------------------------------------------------------|
| `properties` | Comma-separated list of properties to return.                                         |
| `associations` | Comma-separated list of object types to retrieve associated IDs for.                     |
| `archived`   | `true` or `false` to filter archived or unarchived communications. Defaults to `false`. |
| `limit`      | Number of results to return per page (for `/communications` endpoint).               |

**Example Request (All):**

`https://api.hubapi.com/crm/v3/objects/communications?limit=10&properties=hs_communication_body&associations=contact&archived=false`

**Example Response (Single):**  Similar to the create response, but with existing data.


### 3. Update a Communication

**Method:** `PATCH`

**Endpoint:** `/communications/{communicationId}`

**Request Body:**

```json
{
  "properties": {
    "hs_communication_body": "Sent a follow-up message to Carla."
  }
}
```

**Example Request:**

```json
{
    "properties": {
        "hs_communication_body": "Updated message text"
    }
}
```

### 4. Associate an Existing Communication with a Record

**Method:** `PUT`

**Endpoint:** `/communications/{communicationId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

| Field           | Description                                                                      |
|-----------------|----------------------------------------------------------------------------------|
| `communicationId` | ID of the communication.                                                          |
| `toObjectType`   | Object type (e.g., "contact", "company").                                         |
| `toObjectId`     | ID of the record to associate with.                                               |
| `associationTypeId` | Unique association type ID (obtainable via Associations API).                     |

**Example Request:**

`PUT https://api.hubapi.com/crm/v3/objects/communications/12345/associations/contact/67890/communication_to_contact`


### 5. Remove an Association

**Method:** `DELETE`

**Endpoint:** `/communications/{communicationId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`  (Same as association)


### 6. Pin a Message (Indirectly)

Pinning is done by including the `communicationId` in the `hs_pinned_engagement_id` field when creating or updating a record via the relevant object API (contacts, companies, etc.).

### 7. Delete a Communication

**Method:** `DELETE`

**Endpoint:** `/communications/{communicationId}`


## Default Association Type IDs

You'll need to look up this section in the actual HubSpot documentation, as it's not included in your provided text.


## Error Handling

The API will return standard HTTP status codes to indicate success or failure.  Consult the HubSpot API documentation for details on specific error responses and codes.


This markdown documentation provides a more structured and comprehensive overview of the HubSpot Communications API compared to the original text.  Remember to consult the official HubSpot API documentation for the most up-to-date information and details on error handling and rate limits.
