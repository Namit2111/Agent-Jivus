# HubSpot Notes API Documentation

This document describes the HubSpot Notes API, allowing you to manage notes associated with CRM records.  Notes can contain text, attachments, and associations with other HubSpot objects.

## API Endpoints

All API endpoints are located under the `/crm/v3/objects/notes` base path.  Remember to replace `{noteId}` and `{toObjectId}` with the appropriate IDs.


## 1. Create a Note

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/notes`

**Request Body:**

The request body must contain a `properties` object and optionally an `associations` object.

* **`properties` (object):**
    * **`hs_timestamp` (string, required):**  Note creation timestamp.  Use either a Unix timestamp in milliseconds or UTC format (e.g., "2024-10-27T10:00:00Z").
    * **`hs_note_body` (string):** The note's text content (max 65,536 characters).
    * **`hubspot_owner_id` (string):** The ID of the note's owner (HubSpot user ID).
    * **`hs_attachment_ids` (string):** Semicolon-separated IDs of attached files.

* **`associations` (array, optional):**  Associates the note with other records.  Each element is an object:
    * **`to` (object):**
        * **`id` (integer):** The ID of the record to associate with (e.g., contact ID, company ID).
    * **`types` (array):**
        * **`associationCategory` (string):**  Usually "HUBSPOT_DEFINED".
        * **`associationTypeId` (integer):** The ID specifying the association type.  See [default association type IDs](link_to_default_ids) or use the Associations API to retrieve custom type IDs.


**Example Request:**

```json
{
  "properties": {
    "hs_timestamp": "1703712000000",  // Unix timestamp in milliseconds
    "hs_note_body": "Meeting with client to discuss project X.",
    "hubspot_owner_id": "12345",
    "hs_attachment_ids": "67890;123456"
  },
  "associations": [
    {
      "to": { "id": 1001 }, // Contact ID
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 190 }]
    }
  ]
}
```

**Response:**  A JSON object representing the newly created note, including its ID.


## 2. Retrieve Notes

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/notes` (for all notes) or `/crm/v3/objects/notes/{noteId}` (for a single note)

**Query Parameters (for both endpoints):**

* **`properties` (string):** Comma-separated list of properties to return.
* **`associations` (string):** Comma-separated list of object types to retrieve associated IDs for.
* **`limit` (integer):**  Limits the number of results returned (for `/crm/v3/objects/notes`).

**Example Request (retrieving all notes with note body and associated contact IDs):**

```
https://api.hubapi.com/crm/v3/objects/notes?properties=hs_note_body&associations=contact
```

**Response:** A JSON object containing a list of notes (for the `/crm/v3/objects/notes` endpoint) or a single note object (for the `/crm/v3/objects/notes/{noteId}` endpoint).


## 3. Update a Note

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/notes/{noteId}`

**Request Body:**

An object containing the `properties` to update.  Omitted properties will remain unchanged.  Use an empty string to clear a property value.

**Example Request:**

```json
{
  "properties": {
    "hs_note_body": "Updated meeting notes."
  }
}
```

**Response:**  A JSON object representing the updated note.


## 4. Associate Existing Note with Records

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/notes/{noteId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

* **`noteId`:** The ID of the note.
* **`toObjectType`:** The type of object (e.g., "contact", "company").
* **`toObjectId`:** The ID of the object to associate.
* **`associationTypeId`:**  The association type ID.


## 5. Remove an Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/notes/{noteId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`  (Same as associating)


## 6. Pin a Note

Pinning is handled indirectly through the `hs_pinned_engagement_id` property when creating or updating a record (contact, company, deal, etc.) via their respective object APIs.


## 7. Delete a Note

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/notes/{noteId}`

**Response:** A confirmation message.


## Error Handling

The API will return standard HTTP status codes and JSON error responses to indicate success or failure.  Check the documentation for specific error codes and their meanings.


This documentation provides a concise overview.  Refer to the HubSpot API documentation for complete details and advanced features.
