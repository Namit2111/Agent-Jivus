# HubSpot Notes API Documentation

This document details the HubSpot Notes API, allowing you to manage notes associated with CRM records.  Notes can contain text, attachments, and associations with other HubSpot objects.

## API Endpoints

All endpoints are located under the `/crm/v3/objects/notes` base path.  Remember to replace placeholders like `{noteId}`, `{toObjectId}`, and `{associationTypeId}` with actual values.


## 1. Create a Note

**Endpoint:** `/crm/v3/objects/notes`

**Method:** `POST`

**Request Body:**

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27T12:00:00Z",  // Required. Unix timestamp (milliseconds) or UTC format.
    "hs_note_body": "Meeting notes: discussed project X.", // Note text (max 65,536 characters).
    "hubspot_owner_id": "12345", // ID of the note owner.
    "hs_attachment_ids": "67890;123456" // Semicolon-separated IDs of attached files.
  },
  "associations": [
    {
      "to": {
        "id": 77777 // ID of the associated object (e.g., Contact, Company).
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 190 // Association type ID (see note below).
        }
      ]
    }
  ]
}
```

**Response:**  A JSON object representing the created note, including its ID.

**Note:** `associationTypeId` values are defined within HubSpot.  Consult the HubSpot documentation or Associations API to find the correct ID for your association type (e.g., note_to_contact).


## 2. Retrieve Notes

**Endpoint:** `/crm/v3/objects/notes` (all notes) or `/crm/v3/objects/notes/{noteId}` (single note)

**Method:** `GET`

**Query Parameters:**

* `properties`: Comma-separated list of properties to return (e.g., `hs_note_body,hubspot_owner_id`).
* `associations`: Comma-separated list of object types to retrieve associated IDs for (e.g., `contact,company`).
* `limit`: Number of notes to retrieve (for `/crm/v3/objects/notes`).


**Example Request:**

`https://api.hubapi.com/crm/v3/objects/notes?properties=hs_note_body&associations=contact&archived=false`


**Response:**  A JSON object or array of JSON objects representing the requested notes.


## 3. Update a Note

**Endpoint:** `/crm/v3/objects/notes/{noteId}`

**Method:** `PATCH`

**Request Body:**

```json
{
  "properties": {
    "hs_note_body": "Updated meeting notes.",
    "hs_attachment_ids": "123456" // Update or clear attachment IDs.
  }
}
```

**Response:** A JSON object representing the updated note.


## 4. Associate Existing Notes with Records

**Endpoint:** `/crm/v3/objects/notes/{noteId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `PUT`

**Parameters:**

* `{noteId}`: ID of the note.
* `{toObjectType}`: Object type (e.g., `contact`, `company`).
* `{toObjectId}`: ID of the record to associate with.
* `{associationTypeId}`: Association type ID.

**Example Request:**

`https://api.hubspot.com/crm/v3/objects/notes/12345/associations/contact/67890/190`

**Response:** Success/failure indication.


## 5. Remove an Association

**Endpoint:** `/crm/v3/objects/notes/{noteId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `DELETE`

**Parameters:**  Same as above for associating notes.


## 6. Pin a Note (Indirectly)

Pinning is not a direct API call.  To pin a note on a record, include the note's `id` in the `hs_pinned_engagement_id` field when creating or updating the record using its respective object API (Contacts, Companies, Deals, etc.).


## 7. Delete a Note

**Endpoint:** `/crm/v3/objects/notes/{noteId}`

**Method:** `DELETE`

**Response:** Success/failure indication.  Deleted notes go to the recycling bin in HubSpot.



## Error Handling

The API will return standard HTTP status codes to indicate success or failure. Error responses will typically include a JSON object with details about the error.


This documentation provides a concise overview. Refer to the official HubSpot API documentation for a complete and up-to-date reference.
