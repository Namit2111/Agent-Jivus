# HubSpot Meetings API Documentation

This document details the HubSpot Meetings API, allowing you to manage meetings within the HubSpot CRM.  You can create, retrieve, update, associate, and delete meeting engagements.

## API Endpoints Base URL: `/crm/v3/objects/meetings`

All endpoints below are relative to this base URL.  Remember to replace placeholders like `{meetingId}` with actual values.  Authentication via HubSpot's API key is required for all requests.

## 1. Create a Meeting (POST)

Creates a new meeting engagement.

**Endpoint:** `/crm/v3/objects/meetings`

**Method:** `POST`

**Request Body:**

The request body is a JSON object with `properties` and optional `associations` fields.

* **`properties` (object):**  Contains meeting details.  Required fields are marked with an asterisk (*).

| Field                  | Description                                                                        | Type             | Required | Example                                    |
|-----------------------|------------------------------------------------------------------------------------|-----------------|----------|---------------------------------------------|
| `hs_timestamp`*       | Date and time the meeting occurred (Unix timestamp in milliseconds or UTC format). If missing, defaults to `hs_meeting_start_time`. | string/number    | *        | `1677000000000` or `"2023-02-20T12:00:00Z"` |
| `hs_meeting_title`    | Meeting title                                                                      | string           |          | `"Project Kickoff"`                         |
| `hubspot_owner_id`*   | ID of the meeting owner.                                                          | string           | *        | `"1234567"`                               |
| `hs_meeting_body`     | Meeting description                                                                  | string           |          | `"Discuss project requirements"`            |
| `hs_internal_meeting_notes` | Internal notes for your team.                                                      | string           |          | `"Action items: ..."`                     |
| `hs_meeting_external_url` | External URL (e.g., Zoom link).                                                    | string           |          | `"https://example.com/meeting"`          |
| `hs_meeting_location` | Meeting location.                                                                  | string           |          | `"Conference Room A" or "Zoom call"`       |
| `hs_meeting_start_time` | Meeting start time (UTC format).                                                   | string           |          | `"2023-02-20T12:00:00Z"`                 |
| `hs_meeting_end_time`  | Meeting end time (UTC format).                                                     | string           |          | `"2023-02-20T13:00:00Z"`                 |
| `hs_meeting_outcome`  | Meeting outcome (SCHEDULED, COMPLETED, RESCHEDULED, NO SHOW, CANCELED).              | string           |          | `"COMPLETED"`                              |
| `hs_activity_type`    | Type of meeting (based on your HubSpot account's meeting types).                    | string           |          | `"Sales Meeting"`                           |
| `hs_attachment_ids`   | IDs of attached files (semicolon-separated).                                      | string           |          | `"1;2;3"`                                  |


* **`associations` (array, optional):**  Associates the meeting with existing records (contacts, companies, etc.).

    * **`to` (object):**
        * `id` (string): ID of the record to associate.
    * **`types` (array):**
        * `associationCategory` (string): "HUBSPOT_DEFINED"
        * `associationTypeId` (number):  Association type ID (see HubSpot documentation for defaults or use the Associations API).


**Example Request:**

```json
{
  "properties": {
    "hs_timestamp": "2024-03-08T10:00:00Z",
    "hubspot_owner_id": "1234567",
    "hs_meeting_title": "Client Meeting",
    "hs_meeting_start_time": "2024-03-08T10:00:00Z"
  },
  "associations": [
    {
      "to": { "id": "8765432" },
      "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 200 } ]
    }
  ]
}
```

**Response:** A JSON object representing the created meeting, including its ID.


## 2. Retrieve Meetings (GET)

Retrieves meetings.  Can retrieve individual meetings or a list.

**2.1 Retrieve Individual Meeting (GET):**

**Endpoint:** `/crm/v3/objects/meetings/{meetingId}`

**Method:** `GET`

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of associated objects to retrieve.


**2.2 Retrieve List of Meetings (GET):**

**Endpoint:** `/crm/v3/objects/meetings`

**Method:** `GET`

**Query Parameters:**

* `limit`: Maximum number of results per page.
* `properties`: Comma-separated list of properties to return.


## 3. Update a Meeting (PATCH)

Updates an existing meeting.

**Endpoint:** `/crm/v3/objects/meetings/{meetingId}`

**Method:** `PATCH`

**Request Body:**  JSON object with `properties` field containing the properties to update.  Omit properties you don't want to change.  An empty string ("") clears a property value.

**Example Request:**

```json
{
  "properties": {
    "hs_meeting_outcome": "COMPLETED"
  }
}
```


## 4. Associate Existing Meetings with Records (PUT)

Associates a meeting with a record.

**Endpoint:** `/crm/v3/objects/meetings/{meetingId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `PUT`

**Path Parameters:**

* `{meetingId}`: Meeting ID.
* `{toObjectType}`: Object type (e.g., `contact`, `company`).
* `{toObjectId}`: Object ID.
* `{associationTypeId}`: Association type ID.


## 5. Remove an Association (DELETE)

Removes an association between a meeting and a record.

**Endpoint:** `/crm/v3/objects/meetings/{meetingId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `DELETE`

**Path Parameters:** Same as in Associate Existing Meetings.


## 6. Pin a Meeting on a Record

Pin a meeting to the top of a record's timeline using the `hs_pinned_engagement_id` field when creating or updating the record via the relevant object API (Contacts, Companies, Deals, etc.).


## 7. Delete a Meeting (DELETE)

Deletes a meeting (moves it to the recycling bin).

**Endpoint:** `/crm/v3/objects/meetings/{meetingId}`

**Method:** `DELETE`


**Note:**  This documentation provides a summary.  Refer to the official HubSpot API documentation for complete details, including error handling and rate limits.  The "Endpoints" tab mentioned in the original text likely contains further details on batch operations and additional parameters.
