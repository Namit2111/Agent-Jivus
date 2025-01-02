# HubSpot Notes API Documentation

This document details the HubSpot Notes API, allowing you to manage notes associated with CRM records.  Notes can contain text, attachments, and associations with other HubSpot objects.

## API Endpoints

All endpoints are under the base URL: `https://api.hubspot.com/crm/v3/objects/notes`

You will need a valid HubSpot API key for authentication.


## 1. Create a Note

**Method:** `POST /crm/v3/objects/notes`

**Request Body:**

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27T10:00:00Z", // Required. Unix timestamp (milliseconds) or UTC format.
    "hs_note_body": "Meeting notes: discussed project X.", // Note text (max 65,536 characters)
    "hubspot_owner_id": "12345", // ID of the note's owner.
    "hs_attachment_ids": "67890;123456" // IDs of attached files (semicolon-separated).
  },
  "associations": [ // Optional: Associate with other records
    {
      "to": {
        "id": 101 // ID of the associated record (e.g., contact ID).
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 190 // Association type ID. See notes below.
        }
      ]
    }
  ]
}
```

**Response:**  A JSON object representing the created note, including its ID.

**Example Response:**

```json
{
  "id": "77777",
  "properties": {
    "hs_timestamp": "2024-10-27T10:00:00Z",
    "hs_note_body": "Meeting notes: discussed project X.",
    "hubspot_owner_id": "12345",
    "hs_attachment_ids": "67890;123456"
  },
  // ... other properties ...
}
```

**Association Type IDs:**  Default association type IDs are listed in the HubSpot documentation. You can also retrieve custom association type IDs using the HubSpot Associations API.  `associationTypeId` 190 is a common example for associating with a contact.


## 2. Retrieve Notes

**Method:** `GET /crm/v3/objects/notes` or `GET /crm/v3/objects/notes/{noteId}`

**Query Parameters:**

* `properties`: Comma-separated list of properties to return (e.g., `hs_note_body,hubspot_owner_id`).
* `associations`: Comma-separated list of object types to retrieve associated IDs for (e.g., `contact,company`).
* `limit`:  Number of notes to retrieve (for GET /crm/v3/objects/notes).

**Example Request (GET all notes with note body and contact associations):**

`https://api.hubspot.com/crm/v3/objects/notes?properties=hs_note_body&associations=contact`


**Example Response (GET single note):**

(Similar to the create note response, but only containing the specified properties and associations)


## 3. Update a Note

**Method:** `PATCH /crm/v3/objects/notes/{noteId}`

**Request Body:**

```json
{
  "properties": {
    "hs_note_body": "Updated meeting notes.",
    "hs_attachment_ids": "123456" // Update or remove attachment IDs
  }
}
```

**Response:** A JSON object representing the updated note.


## 4. Associate an Existing Note with a Record

**Method:** `PUT /crm/v3/objects/notes/{noteId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

* `{noteId}`: ID of the note.
* `{toObjectType}`: Object type (e.g., `contact`, `company`).
* `{toObjectId}`: ID of the record to associate with.
* `{associationTypeId}`: Association type ID.


**Example Request:**

`https://api.hubspot.com/crm/v3/objects/notes/77777/associations/contact/101/190`


## 5. Remove an Association

**Method:** `DELETE /crm/v3/objects/notes/{noteId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

Use the same URL structure as associating a note.


## 6. Pin a Note

Pinning a note is done indirectly. When creating or updating a record (contact, company, deal, etc.) via its respective object API, include the note's ID in the `hs_pinned_engagement_id` field.  Only one activity can be pinned per record.


## 7. Delete a Note

**Method:** `DELETE /crm/v3/objects/notes/{noteId}`

**Response:**  A success or error message.  Deletion moves the note to the recycle bin; it can be restored later.


## Error Handling

The API will return appropriate HTTP status codes (e.g., 400 Bad Request, 404 Not Found) and JSON error responses to indicate failures.  Check the response body for details.


This documentation provides a concise overview. Refer to the official HubSpot API documentation for the most up-to-date information and details on batch operations, rate limits, and other advanced features.
