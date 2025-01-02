# HubSpot Tasks API Documentation

This document details the HubSpot Tasks API, allowing for the creation, retrieval, updating, association, and deletion of tasks within the HubSpot CRM.

## API Endpoints Base URL: `/crm/v3/objects/tasks`

All endpoints below use this base URL unless otherwise specified.  Remember to replace `{taskId}` and other placeholders with actual IDs.

## 1. Create a Task

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/tasks`

**Request Body:**  JSON object with `properties` and optionally `associations` objects.

**Properties Object:**

| Field             | Description                                                                 | Type             | Required | Example                      |
|----------------------|-----------------------------------------------------------------------------|-----------------|----------|------------------------------|
| `hs_timestamp`      | Due date. Unix timestamp (milliseconds) or UTC format ("YYYY-MM-DDTHH:mm:ss.SSSZ"). | String/Number    | Yes      | `1678886400000` or `"2024-03-15T12:00:00Z"` |
| `hs_task_body`       | Task notes.                                                              | String           | No       | `"Send proposal"`             |
| `hubspot_owner_id`   | ID of the assigned user.                                                  | String           | No       | `"64492917"`                 |
| `hs_task_subject`    | Task title.                                                                | String           | No       | `"Follow-up with client"`     |
| `hs_task_status`     | Task status ("COMPLETED" or "NOT_STARTED").                               | String           | No       | `"NOT_STARTED"`              |
| `hs_task_priority`  | Task priority ("LOW", "MEDIUM", or "HIGH").                              | String           | No       | `"HIGH"`                      |
| `hs_task_type`       | Task type ("EMAIL", "CALL", or "TODO").                                   | String           | No       | `"CALL"`                      |
| `hs_task_reminders`  | Reminder timestamp (Unix timestamp in milliseconds).                       | Number           | No       | `1678972800000`             |


**Associations Object:** (Optional, for associating with existing records)

```json
"associations": [
  {
    "to": { "id": 101 },
    "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 204 } ]
  },
  {
    "to": { "id": 102 },
    "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 204 } ]
  }
]
```

* `to.id`: ID of the record to associate.
* `types`: Association type.  `associationTypeId` may vary depending on the object type.  Refer to HubSpot's [associations API](link_to_associations_api_docs) for details.


**Example Request:**

```json
{
  "properties": {
    "hs_timestamp": "2024-03-15T12:00:00Z",
    "hs_task_body": "Send proposal",
    "hubspot_owner_id": "12345",
    "hs_task_subject": "Project X Proposal",
    "hs_task_priority": "HIGH"
  }
}
```

**Response:**  JSON object containing the created task's details, including its ID.


## 2. Retrieve Tasks

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/tasks` (for all tasks) or `/crm/v3/objects/tasks/{taskId}` (for a specific task)

**Parameters (for `/crm/v3/objects/tasks`):**

* `limit`:  Maximum number of results per page.
* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.

**Parameters (for `/crm/v3/objects/tasks/{taskId}`):**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.

**Response:** JSON object or array of JSON objects containing task details.


## 3. Update a Task

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/tasks/{taskId}`

**Request Body:** JSON object containing the `properties` object with the fields to update.  Omit fields to leave them unchanged.  An empty string ("") clears a property value.

**Example Request:**

```json
{
  "properties": {
    "hs_task_status": "COMPLETED",
    "hs_task_body": "Proposal sent"
  }
}
```

**Response:** JSON object containing the updated task's details.


## 4. Associate Existing Task with Records

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/tasks/{taskId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

* `{taskId}`: ID of the task.
* `{toObjectType}`: Type of object (e.g., "contacts", "companies").
* `{toObjectId}`: ID of the record.
* `{associationTypeId}`: Association type ID (obtain from HubSpot's associations API).

**Response:**  Success or error indication.


## 5. Remove an Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/tasks/{taskId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Response:** Success or error indication.


## 6. Pin a Task (Indirectly)

Pinning is done by including the task's `id` in the `hs_pinned_engagement_id` field when creating or updating a record via other HubSpot object APIs (Contacts, Companies, etc.).


## 7. Delete a Task

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/tasks/{taskId}`

**Response:** Success or error indication.


**Note:**  This documentation summarizes the key aspects.  Consult the official HubSpot API documentation for comprehensive details, error handling, rate limits, and authentication information.  Remember to replace placeholders like `{taskId}`, `{toObjectId}`, and `{associationTypeId}` with actual values.
