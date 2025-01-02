# HubSpot Notes API Documentation

This document details the HubSpot API endpoints for managing notes associated with CRM records.  Notes allow you to add information and attachments to a record's timeline, visible to other users in the account.

## API Endpoints

All API endpoints are located under the `/crm/v3/objects/notes` base path.  Remember to replace placeholders like `{noteId}` with the actual ID.  Authentication is required; refer to HubSpot's API documentation for details.

### 1. Create a Note

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/notes`

**Request Body:**

The request body contains a `properties` object and an optional `associations` object.

**`properties` Object:**

| Field             | Description                                                                     | Type             | Required | Example                     |
|----------------------|---------------------------------------------------------------------------------|-----------------|----------|------------------------------|
| `hs_timestamp`     | Note creation time (Unix timestamp in milliseconds or UTC format).             | String/Number   | Yes      | `"2024-07-26T10:00:00Z"` or `1700000000` |
| `hs_note_body`     | Note text content (max 65,536 characters).                                      | String           | No       | `"Meeting with client discussed proposal."` |
| `hubspot_owner_id` | HubSpot user ID of the note creator.                                           | String           | No       | `"12345"`                     |
| `hs_attachment_ids` | IDs of associated attachments (semicolon-separated).                         | String           | No       | `"1;2;3"`                     |


**`associations` Object (Optional):**

This object allows associating the note with existing CRM records.  Multiple associations are possible.

```json
"associations": [
  {
    "to": {
      "id": 301  // ID of the record
    },
    "types": [
      {
        "associationCategory": "HUBSPOT_DEFINED",
        "associationTypeId": 190 // Association type ID (see HubSpot docs for defaults and custom types)
      }
    ]
  }
]
```

**Example Request:**

```json
{
  "properties": {
    "hs_timestamp": "2024-07-26T10:00:00Z",
    "hs_note_body": "Meeting with client discussed proposal.",
    "hubspot_owner_id": "12345",
    "hs_attachment_ids": "1;2"
  },
  "associations": [
    {
      "to": {"id": 123},
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 190}]
    }
  ]
}
```

**Response:**  A JSON object representing the created note, including its ID.


### 2. Retrieve Notes

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/notes` (for all notes) or `/crm/v3/objects/notes/{noteId}` (for a single note)

**Query Parameters:**

| Parameter     | Description                                                                   | Type     |
|-----------------|-------------------------------------------------------------------------------|----------|
| `properties`   | Comma-separated list of properties to return.                               | String   |
| `associations` | Comma-separated list of object types to retrieve associated IDs for.          | String   |
| `archived`     | Whether to include archived notes (true/false).                              | Boolean  |
| `limit`         | Limit the number of results returned (for GET /crm/v3/objects/notes only)   | Integer  |


**Example Request (Retrieve all notes with body and contact associations):**

```
https://api.hubapi.com/crm/v3/objects/notes?properties=hs_note_body&associations=contact&archived=false&limit=10
```

**Response:** A JSON object containing a list of notes (or a single note if using the single note endpoint).  Only requested properties and associations will be included.


### 3. Update a Note

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/notes/{noteId}`

**Request Body:**  A JSON object containing the `properties` object with fields to update.  Omitted fields remain unchanged.  Empty strings clear existing property values.

**Example Request:**

```json
{
  "properties": {
    "hs_note_body": "Updated note text."
  }
}
```

**Response:** A JSON object representing the updated note.


### 4. Associate Existing Note with Records

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/notes/{noteId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Path Parameters:**

| Parameter       | Description                                         |
|-----------------|-----------------------------------------------------|
| `noteId`        | ID of the note.                                    |
| `toObjectType`  | Type of object to associate (e.g., `contact`, `company`). |
| `toObjectId`    | ID of the object to associate.                        |
| `associationTypeId` | ID of the association type.                         |

**Response:**  A success/failure indicator.


### 5. Remove an Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/notes/{noteId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Path Parameters:** (Same as Associate Existing Note)

**Response:** A success/failure indicator.


### 6. Pin a Note (Indirectly)

Pinning is not a direct API call. To pin a note, include the note's `id` in the `hs_pinned_engagement_id` field when creating or updating a record (contact, company, deal, etc.) using the respective object APIs.


### 7. Delete a Note

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/notes/{noteId}`

**Response:** A success/failure indicator.


## Error Handling

The API returns standard HTTP status codes to indicate success or failure.  Refer to HubSpot's API documentation for detailed error responses.


This documentation provides a concise overview.  Consult the official HubSpot API documentation for the most up-to-date information and detailed specifications, including specifics on association type IDs and batch operations.
