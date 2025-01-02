# HubSpot Notes API Documentation

This document details the HubSpot Notes API, allowing you to manage notes associated with CRM records.  Notes can contain text, attachments, and associations with other HubSpot objects.

## API Endpoints Base URL:

`/crm/v3/objects/notes`


## 1. Create a Note

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/notes`

**Request Body:**

The request body must contain a `properties` object with note details and an optional `associations` object to link the note to existing records.

**Properties Object:**

| Field             | Description                                                                     | Type             | Required | Example                                      |
|----------------------|---------------------------------------------------------------------------------|-----------------|----------|----------------------------------------------|
| `hs_timestamp`      | Note creation time (Unix timestamp in milliseconds or UTC format).              | String           | Yes       | `"2024-10-27T10:00:00Z"` or `1703715200000` |
| `hs_note_body`      | Note text content (max 65,536 characters).                                      | String           | No        | `"Meeting scheduled with client."`           |
| `hubspot_owner_id` | ID of the note's owner (HubSpot user ID).                                       | String           | No        | `"12345"`                                   |
| `hs_attachment_ids` | Semicolon-separated IDs of attached files.                                    | String           | No        | `"67890;12345"`                             |


**Associations Object:**

The `associations` object is an array of association objects. Each object links the note to a specific record.

| Field      | Description                                             | Type      | Required | Example                               |
|-------------|---------------------------------------------------------|-----------|----------|---------------------------------------|
| `to.id`    | ID of the record to associate with.                   | Integer   | Yes       | `12345`                              |
| `types[0].associationCategory` | Association category (e.g., "HUBSPOT_DEFINED"). | String    | Yes       | `"HUBSPOT_DEFINED"`                   |
| `types[0].associationTypeId`   | Association type ID (see [default IDs](<default_ids_link>) or use the Associations API for custom types). | Integer   | Yes       | `190` (e.g., note_to_company)         |


**Example Request:**

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27T10:00:00Z",
    "hs_note_body": "Meeting scheduled with client.",
    "hubspot_owner_id": "12345",
    "hs_attachment_ids": "67890;12345"
  },
  "associations": [
    {
      "to": { "id": 12345 },
      "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 190 } ]
    }
  ]
}
```

**Response:**  A JSON object representing the created note, including its ID.


## 2. Retrieve Notes

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/notes` (for all notes) or `/crm/v3/objects/notes/{noteId}` (for a single note)

**Query Parameters:**

| Parameter    | Description                                                              | Type     |
|---------------|--------------------------------------------------------------------------|----------|
| `properties` | Comma-separated list of properties to return.                             | String   |
| `associations` | Comma-separated list of object types to retrieve associated IDs for.       | String   |
| `archived` | Whether to include archived notes. Defaults to `false`.             | Boolean  |
| `limit` | Number of notes to return (for GET /crm/v3/objects/notes only)           | Integer  |


**Example Request (multiple notes):**

`https://api.hubapi.com/crm/v3/objects/notes?properties=hs_note_body&associations=contact&archived=false&limit=10`


**Example Request (single note):**

`https://api.hubapi.com/crm/v3/objects/notes/12345`

**Response:**  A JSON object or array of JSON objects representing the retrieved note(s).



## 3. Update a Note

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/notes/{noteId}`

**Request Body:**

A JSON object containing the `properties` to update.  Omitted properties are not changed.  An empty string (`""`) clears a property value.

**Example Request:**

```json
{
  "properties": {
    "hs_note_body": "Updated meeting details.",
    "hs_attachment_ids": "" // Clears existing attachments
  }
}
```

**Response:** A JSON object representing the updated note.


## 4. Associate an Existing Note with a Record

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/notes/{noteId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Path Parameters:**

| Parameter       | Description                                      | Example     |
|-----------------|--------------------------------------------------|-------------|
| `noteId`        | ID of the note.                                   | `12345`     |
| `toObjectType` | Type of object to associate (e.g., `contact`, `company`). | `contact`   |
| `toObjectId`    | ID of the object to associate.                     | `54321`     |
| `associationTypeId` | Association type ID (see [default IDs](<default_ids_link>) or Associations API). | `202`       |


**Response:**  A success or error message.


## 5. Remove an Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/notes/{noteId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Path Parameters:** (Same as Associate an Existing Note)

**Response:** A success or error message.


## 6. Pin a Note (Indirectly)

Pinning is not a direct API call. To pin a note, include its ID in the `hs_pinned_engagement_id` field when creating or updating a record using the relevant object API (Contacts, Companies, Deals, etc.).


## 7. Delete a Note

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/notes/{noteId}`

**Response:** A success or error message.

**Note:**  Deleting a note moves it to the recycle bin; it can be restored later.


**Remember to replace placeholder IDs and values with your actual data.**  Always refer to the official HubSpot API documentation for the most up-to-date information and details on error handling and rate limits.  Replace `<default_ids_link>` with the actual link provided by HubSpot to their default association type IDs.
