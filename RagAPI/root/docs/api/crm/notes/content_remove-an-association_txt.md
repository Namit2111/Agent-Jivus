# HubSpot Notes API Documentation

This document details the HubSpot Notes API, allowing you to manage notes associated with HubSpot CRM records.  Notes can contain text, attachments, and be linked to multiple records.

## API Endpoints Base URL: `/crm/v3/objects/notes`

All API endpoints below are relative to this base URL.  Replace `{noteId}` and `{toObjectId}` with the appropriate IDs.

## 1. Create a Note

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/notes`

**Request Body:**

The request body must contain a `properties` object, and optionally an `associations` object.

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27T12:00:00Z", // Required. Unix timestamp (milliseconds) or UTC format.
    "hs_note_body": "Meeting notes: discussed project X.", // Note text (max 65,536 characters).
    "hubspot_owner_id": "12345", // ID of the note owner.
    "hs_attachment_ids": "67890;123456" // IDs of attached files (semicolon separated).
  },
  "associations": [
    {
      "to": {
        "id": 77777, // ID of the associated record (e.g., contact, company).
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 190 //  Default association type ID (see HubSpot documentation for specifics)
        }
      ]
    }
  ]
}
```

**Response:**  A JSON object representing the created note, including its ID.  Check HubSpot's API documentation for the exact response structure.

**Example cURL Request:**

```bash
curl -X POST \
  https://api.hubspot.com/crm/v3/objects/notes \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{your_request_body}'
```


## 2. Retrieve Notes

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/notes`  (for all notes) or `/crm/v3/objects/notes/{noteId}` (for a single note)

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.
* `archived`:  `true` or `false` to filter for archived notes. (default: `false`)
* `limit`: Number of notes to return (for multiple notes retrieval).

**Example GET request for all notes with specific properties and associations:**

```bash
curl -X GET \
  'https://api.hubspot.com/crm/v3/objects/notes?properties=hs_note_body,hubspot_owner_id&associations=contact,company' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

**Response:** A JSON array of note objects or a single note object.


## 3. Update a Note

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/notes/{noteId}`

**Request Body:**

```json
{
  "properties": {
    "hs_note_body": "Updated meeting notes.",
    "hs_attachment_ids": "123456" // Updated attachment IDs.  An empty string clears the field.
  }
}
```

**Response:** A JSON object representing the updated note.


## 4. Associate Existing Note with Record

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/notes/{noteId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

* `{toObjectType}`:  e.g., `contact`, `company`, `deal`.
* `{toObjectId}`: ID of the record to associate with.
* `{associationTypeId}`:  Association type ID (see HubSpot documentation).

**Example:**

```bash
curl -X PUT \
  'https://api.hubspot.com/crm/v3/objects/notes/123/associations/contact/456/190' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```


## 5. Remove an Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/notes/{noteId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

Same endpoint as associating a note; DELETE method removes the association.


## 6. Pin a Note (Indirectly)

Pinning is not a direct API call. To pin a note to a record's timeline, include the note's ID in the `hs_pinned_engagement_id` field when creating or updating the record using the relevant object API (Contacts, Companies, Deals, etc.).


## 7. Delete a Note

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/notes/{noteId}`

**Response:** A success or error message.


**Note:**  Replace `YOUR_API_KEY` with your actual HubSpot API key.  Refer to the official HubSpot API documentation for detailed information on error handling, rate limits, and complete field descriptions.  The association type IDs may vary; consult the HubSpot documentation for the most up-to-date values.
