# HubSpot Notes API Documentation

This document details the HubSpot Notes API, allowing you to manage notes associated with CRM records.  Notes can contain text, attachments, and associations with other HubSpot objects.

## API Endpoints

All endpoints are located under the `/crm/v3/objects/notes` base URL.  Remember to replace `{noteId}` and other placeholders with actual values.

### 1. Create a Note

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/notes`

**Request Body:**

The request body should be a JSON object containing `properties` and optionally `associations`.

* **`properties` (object):**
    * **`hs_timestamp` (string, required):**  Note creation timestamp.  Use either a Unix timestamp in milliseconds or UTC format (e.g., "2024-10-27T10:30:00Z").
    * **`hs_note_body` (string):** Note text content (max 65,536 characters).
    * **`hubspot_owner_id` (string):** ID of the note's owner (HubSpot user).
    * **`hs_attachment_ids` (string):** Semicolon-separated IDs of attached files.

* **`associations` (array, optional):**  An array of objects, each associating the note with a record.
    * **`to` (object):**
        * **`id` (integer):** ID of the record to associate with.
    * **`types` (array):**
        * **`associationCategory` (string):** Usually "HUBSPOT_DEFINED".
        * **`associationTypeId` (integer):**  ID specifying the association type.  See [default association type IDs](link_to_default_ids) or use the Associations API for custom types.


**Example Request:**

```json
{
  "properties": {
    "hs_timestamp": "1703660200000",  // Unix timestamp in milliseconds
    "hs_note_body": "Meeting with John Doe. Discussed project X.",
    "hubspot_owner_id": "12345",
    "hs_attachment_ids": "67890;123456"
  },
  "associations": [
    {
      "to": {"id": 777},
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 190}] //Example association with a contact
    }
  ]
}
```

**Response:**  A JSON object representing the newly created note, including its ID.


### 2. Retrieve Notes

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/notes`  (for all notes) or `/crm/v3/objects/notes/{noteId}` (for a single note)

**Query Parameters:**

* **`properties` (string):** Comma-separated list of properties to return.
* **`associations` (string):** Comma-separated list of object types to retrieve associated IDs for.
* `limit` (integer): Number of notes to retrieve


**Example Request (retrieving all notes with note body and contact associations):**

```
https://api.hubapi.com/crm/v3/objects/notes?properties=hs_note_body&associations=contact
```

**Response:**  A JSON object or array of JSON objects representing the requested notes.


### 3. Update a Note

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/notes/{noteId}`

**Request Body:**

A JSON object containing the `properties` to update.  Only specified properties will be modified; others remain unchanged.  To clear a property, set its value to an empty string.

**Example Request:**

```json
{
  "properties": {
    "hs_note_body": "Meeting rescheduled to tomorrow."
  }
}
```

**Response:** A JSON object representing the updated note.


### 4. Associate Existing Note with Records

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/notes/{noteId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

* **`noteId` (integer):** ID of the note.
* **`toObjectType` (string):** Object type (e.g., "contact", "company").
* **`toObjectId` (integer):** ID of the record to associate.
* **`associationTypeId` (integer or string):** Association type ID (numeric or snake_case).


### 5. Remove an Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/notes/{noteId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


### 6. Pin a Note (Indirectly)

Pinning is done indirectly. When creating or updating a record (contact, company, etc.) using the respective object APIs, include the note's ID in the `hs_pinned_engagement_id` field.


### 7. Delete a Note

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/notes/{noteId}`

**Response:** A success or error message.


## Error Handling

The API will return standard HTTP status codes and JSON error responses to indicate success or failure.  Refer to the HubSpot API documentation for details on error codes.


## Rate Limiting

Be aware of HubSpot's API rate limits to avoid exceeding allowed requests per minute/hour.



This documentation provides a concise overview. For complete details and advanced features (batch operations, etc.), refer to the official HubSpot API documentation.
