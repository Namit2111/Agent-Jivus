# HubSpot Notes API Documentation

This document details the HubSpot API endpoints for managing notes associated with CRM records.  Notes can be used to log information, attach documents, and track interactions related to contacts, companies, deals, etc.

## API Endpoints

All API endpoints are located under the `/crm/v3/objects/notes` base path.  Remember to replace `{noteId}` and `{toObjectId}` with the appropriate IDs.

**Base URL:** `https://api.hubspot.com/crm/v3/objects/notes`


### 1. Create a Note

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/notes`

**Request Body:**

The request body must include a `properties` object and optionally an `associations` object.

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27T10:00:00Z", // Required. Unix timestamp (milliseconds) or UTC format.
    "hs_note_body": "Meeting with John Doe. Discussed project X.", // Note text (max 65,536 characters).
    "hubspot_owner_id": "12345", // ID of the note owner.
    "hs_attachment_ids": "67890;123456" // IDs of attached files (semicolon-separated).
  },
  "associations": [
    {
      "to": {
        "id": 7890, // ID of the associated record (e.g., contact ID).
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 190 // Association type ID (see documentation for default IDs).
        }
      ]
    }
  ]
}
```

**Response:**  A JSON object representing the newly created note, including its ID.


### 2. Retrieve Notes

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/notes`  (for all notes) or `/crm/v3/objects/notes/{noteId}` (for a single note)

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.  (e.g., `hs_note_body,hubspot_owner_id`)
* `associations`: Comma-separated list of object types to retrieve associated IDs for. (e.g., `contact,company`)
* `limit`: Number of notes to retrieve (for `/crm/v3/objects/notes`).

**Example URL (Retrieve notes with note body and associated contacts):**

`https://api.hubspot.com/crm/v3/objects/notes?properties=hs_note_body&associations=contact`

**Response:** A JSON object containing an array of notes (for `/crm/v3/objects/notes`) or a single note object (for `/crm/v3/objects/notes/{noteId}`).


### 3. Update a Note

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/notes/{noteId}`

**Request Body:**

```json
{
  "properties": {
    "hs_note_body": "Updated note text.",
    "hs_attachment_ids": "123456" // Update or replace attachment IDs.
  }
}
```

**Response:** A JSON object representing the updated note.


### 4. Associate an Existing Note with a Record

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/notes/{noteId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Path Parameters:**

* `{noteId}`: ID of the note.
* `{toObjectType}`: Type of object to associate (e.g., `contact`, `company`).
* `{toObjectId}`: ID of the object to associate.
* `{associationTypeId}`:  Association type ID.

**Response:** A confirmation (usually a 204 No Content status code).


### 5. Remove an Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/notes/{noteId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Path Parameters:** Same as above.

**Response:** A confirmation (usually a 204 No Content status code).


### 6. Pin a Note to a Record

Pinning is achieved indirectly. When creating or updating a record (using the respective object APIs like contacts, companies, deals, etc.), include the note's ID in the `hs_pinned_engagement_id` field.


### 7. Delete a Note

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/notes/{noteId}`

**Response:** A confirmation (usually a 204 No Content status code).


##  Association Type IDs

Default association type IDs are documented in the HubSpot API documentation.  You might need to retrieve IDs for custom association types using the HubSpot Associations API.


## Error Handling

The API will return appropriate HTTP status codes and JSON error responses in case of failures (e.g., 400 Bad Request, 404 Not Found, 500 Internal Server Error).  Refer to HubSpot's API documentation for detailed error codes and messages.


This documentation provides a concise overview. Refer to the official HubSpot API documentation for the most up-to-date and comprehensive information, including details on authentication, rate limits, and batch operations.
