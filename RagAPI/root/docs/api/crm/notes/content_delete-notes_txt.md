# HubSpot Notes API Documentation

This document details the HubSpot API endpoints for managing notes associated with CRM records.  Notes can be used to log information, such as offline conversations, and attach documents to records.  All API calls require proper authentication with a HubSpot API key.

## API Endpoints

All endpoints are under the `/crm/v3/objects/notes` base path.

### 1. Create a Note

**Method:** `POST /crm/v3/objects/notes`

**Request Body:**

The request body must contain a `properties` object and optionally an `associations` object.

**`properties` object:**

| Field             | Description                                                                         | Type             | Required | Example                                      |
|----------------------|-------------------------------------------------------------------------------------|-----------------|----------|----------------------------------------------|
| `hs_timestamp`     | Note creation timestamp. Use Unix timestamp (milliseconds) or UTC format (e.g., "2024-07-27T10:00:00Z"). | String           | Yes       | `1690460800000` or `"2024-07-27T10:00:00Z"` |
| `hs_note_body`     | Note text content (max 65,536 characters).                                         | String           | No        | "Meeting with client discussed project X"      |
| `hubspot_owner_id` | ID of the note's owner (HubSpot user ID).                                        | String           | No        | `12345`                                     |
| `hs_attachment_ids`| IDs of attached files (semicolon-separated).                                      | String           | No        | `111;222;333`                               |


**`associations` object:** (Optional, for associating with existing records)

This is an array of objects, each associating the note with a specific record.

| Field       | Description                                           | Type     | Required | Example            |
|--------------|-------------------------------------------------------|----------|----------|---------------------|
| `to.id`     | ID of the record to associate with.                     | Integer  | Yes       | `123`              |
| `types[0].associationCategory` | Association category. Usually "HUBSPOT_DEFINED".       | String   | Yes       | `"HUBSPOT_DEFINED"` |
| `types[0].associationTypeId` | Association type ID (see [default IDs](link_to_default_ids_if_available) or use Associations API). | Integer  | Yes       | `190`              |


**Example Request:**

```json
{
  "properties": {
    "hs_timestamp": "2024-07-27T10:00:00Z",
    "hs_note_body": "Spoke with decision maker Carla. Attached the proposal.",
    "hubspot_owner_id": "14240720",
    "hs_attachment_ids": "24332474034"
  },
  "associations": [
    {
      "to": { "id": 301 },
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 190 }]
    }
  ]
}
```

**Response:**  A JSON object representing the created note, including its ID.


### 2. Retrieve Notes

**Method:** `GET /crm/v3/objects/notes`  or `GET /crm/v3/objects/notes/{noteId}`

**Parameters:**

| Parameter      | Description                                                                | Type    |
|-----------------|----------------------------------------------------------------------------|---------|
| `noteId`       | (Optional, for individual note retrieval) ID of the note to retrieve.    | Integer |
| `properties`   | Comma-separated list of properties to return.                             | String  |
| `associations` | Comma-separated list of object types to retrieve associated IDs for.      | String  |
| `limit`        | (For GET /crm/v3/objects/notes)  Maximum number of notes to return.        | Integer |
| `archived`     | (For GET /crm/v3/objects/notes)  Filter for archived (true) or unarchived (false) notes. | Boolean |

**Example Request (retrieving multiple notes):**

`https://api.hubapi.com/crm/v3/objects/notes?limit=10&properties=hs_note_body&associations=contact&archived=false`


**Response:** A JSON object containing an array of notes or a single note object, depending on the request.


### 3. Update a Note

**Method:** `PATCH /crm/v3/objects/notes/{noteId}`

**Request Body:**

A JSON object containing a `properties` object with the fields to update.  HubSpot ignores read-only and non-existent properties.  To clear a property, set its value to an empty string.


**Example Request:**

```json
{
  "properties": {
    "hs_note_body": "Updated note text.",
    "hs_attachment_ids": "" // Clears attachments
  }
}
```

**Response:** A JSON object representing the updated note.


### 4. Associate Existing Note with Records

**Method:** `PUT /crm/v3/objects/notes/{noteId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Path Parameters:**

| Parameter       | Description                                    | Type     |
|-----------------|------------------------------------------------|----------|
| `noteId`        | ID of the note to associate.                   | Integer  |
| `toObjectType`  | Type of object (e.g., "contact", "company"). | String   |
| `toObjectId`    | ID of the object to associate with.           | Integer  |
| `associationTypeId` | Association type ID.                          | Integer  |

**Response:**  Success/failure status.


### 5. Remove an Association

**Method:** `DELETE /crm/v3/objects/notes/{noteId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Path Parameters:** (Same as Associate Existing Note)

**Response:** Success/failure status.


### 6. Pin a Note (Indirectly through Record APIs)

Pinning a note is done indirectly by including the note's ID in the `hs_pinned_engagement_id` field when creating or updating a record using the relevant object API (Contacts, Companies, Deals, etc.).


### 7. Delete a Note

**Method:** `DELETE /crm/v3/objects/notes/{noteId}`

**Path Parameters:**

| Parameter | Description | Type     |
|-----------|-------------|----------|
| `noteId`  | ID of the note to delete. | Integer  |

**Response:** Success/failure status.  The note is moved to the recycle bin, not permanently deleted.


This documentation provides a comprehensive overview of the HubSpot Notes API.  Remember to consult the official HubSpot developer documentation for the most up-to-date information and details on error handling and rate limits.
