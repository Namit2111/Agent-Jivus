# HubSpot Notes API Documentation

This document details the HubSpot Notes API, allowing you to manage notes associated with CRM records.  Notes can include text, attachments, and associations with other HubSpot objects.

## API Endpoints

All endpoints are under the `/crm/v3/objects/notes` base path.  Remember to replace `{noteId}` and `{toObjectId}` with the appropriate IDs.

**Base URL:** `https://api.hubspot.com/crm/v3/objects/notes`


## 1. Create a Note (POST)

**Endpoint:** `/crm/v3/objects/notes`

**Method:** `POST`

**Request Body:**

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27T10:00:00Z", // Required. Unix timestamp (milliseconds) or UTC format.
    "hs_note_body": "Meeting notes...", // Note text (max 65,536 characters)
    "hubspot_owner_id": "12345", // HubSpot ID of the note owner.
    "hs_attachment_ids": "67890;123456" // IDs of attached files (semicolon-separated).
  },
  "associations": [
    {
      "to": {
        "id": 1001, // ID of the associated object (e.g., contact, company).
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 190 // Association type ID (see HubSpot documentation for available IDs).
        }
      ]
    }
  ]
}
```

**Response:**  A JSON object representing the newly created note, including its ID.

**Example Request (using curl):**

```bash
curl -X POST \
  https://api.hubspot.com/crm/v3/objects/notes \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -d '{
    "properties": {
      "hs_timestamp": "2024-10-27T10:00:00Z",
      "hs_note_body": "Meeting notes...",
      "hubspot_owner_id": "12345",
      "hs_attachment_ids": "67890;123456"
    },
    "associations": [
      {
        "to": {
          "id": 1001
        },
        "types": [
          {
            "associationCategory": "HUBSPOT_DEFINED",
            "associationTypeId": 190
          }
        ]
      }
    ]
  }'
```


## 2. Retrieve a Note (GET)

**Endpoint:** `/crm/v3/objects/notes/{noteId}`

**Method:** `GET`

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.

**Example Request:**

```bash
curl -X GET \
  'https://api.hubspot.com/crm/v3/objects/notes/123?properties=hs_note_body,hs_timestamp&associations=contact' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

**Response:** A JSON object representing the note.


## 3. Update a Note (PATCH)

**Endpoint:** `/crm/v3/objects/notes/{noteId}`

**Method:** `PATCH`

**Request Body:**

```json
{
  "properties": {
    "hs_note_body": "Updated meeting notes...",
    "hs_attachment_ids": "123456" // Update or remove attachments.
  }
}
```

**Response:** A JSON object representing the updated note.


## 4. Associate Existing Note with Records (PUT)

**Endpoint:** `/crm/v3/objects/notes/{noteId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `PUT`

**Parameters:**

* `{noteId}`: ID of the note.
* `{toObjectType}`: Type of object (e.g., `contact`, `company`).
* `{toObjectId}`: ID of the object to associate.
* `{associationTypeId}`: Association type ID.

**Example:**  Associate note with ID 123 with contact ID 456.

```bash
curl -X PUT \
  'https://api.hubspot.com/crm/v3/objects/notes/123/associations/contact/456/190' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```


## 5. Remove an Association (DELETE)

**Endpoint:** `/crm/v3/objects/notes/{noteId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `DELETE`

**Parameters:** Same as Associate Existing Note with Records.


## 6. Pin a Note (Using Object APIs)

Pinning a note is done indirectly by including the note's `id` in the `hs_pinned_engagement_id` field when creating or updating a record using the relevant object API (contacts, companies, deals, etc.).


## 7. Delete a Note (DELETE)

**Endpoint:** `/crm/v3/objects/notes/{noteId}`

**Method:** `DELETE`

**Response:**  Confirmation of deletion.


##  Important Notes:

* Replace `YOUR_API_KEY` with your actual HubSpot API key.
* Consult the HubSpot API documentation for detailed information on association type IDs and other specifics.  The provided examples use placeholder IDs.
* Error handling (checking HTTP status codes) should be implemented in your application code.


This documentation provides a concise overview.  Refer to the official HubSpot API documentation for the most up-to-date information and detailed error handling.
