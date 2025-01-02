# HubSpot Notes API Documentation

This document details the HubSpot Notes API, allowing you to manage notes associated with CRM records.  Notes can contain text, attachments, and associations with other HubSpot objects.

## API Endpoints

All endpoints are under the `/crm/v3/objects/notes` base path.  Remember to replace placeholders like `{noteId}` with the actual ID.  Authentication is required for all API calls.

**Base URL:** `https://api.hubspot.com/crm/v3/objects/notes`


## Methods

### 1. Create a Note (POST `/crm/v3/objects/notes`)

Creates a new note.

**Request Body:**

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27T12:00:00Z", // Required. Unix timestamp (ms) or UTC string.
    "hs_note_body": "Meeting notes...", // Note text (max 65,536 characters).
    "hubspot_owner_id": "12345", // HubSpot ID of the note owner.
    "hs_attachment_ids": "67890;123456" // Semicolon-separated list of attachment IDs.
  },
  "associations": [
    {
      "to": { "id": 1001 }, // ID of the associated object (e.g., contact ID).
      "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 190 } ] // Association type.  See default types or use the associations API for custom types.
    }
  ]
}
```

**Response (201 Created):**  A JSON object representing the created note, including its ID.


**Example using curl:**

```bash
curl -X POST \
  https://api.hubspot.com/crm/v3/objects/notes \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -d '{
    "properties": {
      "hs_timestamp": "2024-10-27T12:00:00Z",
      "hs_note_body": "Meeting notes...",
      "hubspot_owner_id": "12345",
      "hs_attachment_ids": "67890;123456"
    },
    "associations": [
      {
        "to": { "id": 1001 },
        "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 190 } ]
      }
    ]
  }'
```

### 2. Retrieve a Note (GET `/crm/v3/objects/notes/{noteId}`)

Retrieves a single note by its ID.

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.

**Example URL:** `https://api.hubspot.com/crm/v3/objects/notes/123?properties=hs_note_body,hs_timestamp&associations=contact`

**Response (200 OK):** A JSON object representing the note.


### 3. Retrieve Notes (GET `/crm/v3/objects/notes`)

Retrieves a list of notes.  Use query parameters for pagination and filtering.

**Query Parameters:**

* `limit`: Number of notes to return per page (default 100, max 1000).
* `offset`: Starting index for pagination.
* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.
* `archived`:  Boolean to filter by archived status (true/false)

**Example URL:** `https://api.hubspot.com/crm/v3/objects/notes?limit=10&properties=hs_note_body&associations=contact&archived=false`

**Response (200 OK):** A JSON object containing a list of notes and pagination information.

### 4. Update a Note (PATCH `/crm/v3/objects/notes/{noteId}`)

Updates an existing note.  Only specified properties are updated.

**Request Body:**

```json
{
  "properties": {
    "hs_note_body": "Updated meeting notes...",
    "hs_attachment_ids": "123456" // Update or clear attachment IDs
  }
}
```

**Response (200 OK):** A JSON object representing the updated note.


### 5. Associate a Note with a Record (PUT `/crm/v3/objects/notes/{noteId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates an existing note with another HubSpot object.

**Path Parameters:**

* `{noteId}`: ID of the note.
* `{toObjectType}`: Object type (e.g., `contact`, `company`).
* `{toObjectId}`: ID of the object to associate with.
* `{associationTypeId}`:  ID of the association type.  Obtain from the Associations API.

**Response (204 No Content):**  Indicates successful association.

### 6. Remove an Association (DELETE `/crm/v3/objects/notes/{noteId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Removes an association between a note and another object.  Uses the same path parameters as the associate method.

**Response (204 No Content):** Indicates successful removal.

### 7. Pin a Note (When Creating/Updating Records)

To pin a note to a record's timeline, include the note's `id` in the `hs_pinned_engagement_id` field when creating or updating the record using the relevant object API (Contacts, Companies, Deals, etc.). Only one activity can be pinned per record.

### 8. Delete a Note (DELETE `/crm/v3/objects/notes/{noteId}`)

Deletes a note (moves it to the recycle bin).

**Response (204 No Content):** Indicates successful deletion.


## Error Handling

The API returns standard HTTP status codes to indicate success or failure.  Error responses will include a JSON object with details.


##  Rate Limits

Refer to HubSpot's API documentation for rate limit information.


This documentation provides a concise overview.  Refer to the official HubSpot API documentation for the most up-to-date information and details on batch operations.
