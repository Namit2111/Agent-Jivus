# HubSpot Tasks API Documentation

This document details the HubSpot Tasks API, allowing you to create, manage, and interact with tasks within the HubSpot CRM.

## API Endpoints

All endpoints are under the base URL: `/crm/v3/objects/tasks`

## 1. Create a Task

**Method:** `POST /crm/v3/objects/tasks`

**Request Body:**  JSON object with `properties` and optional `associations` objects.

**Properties Object:**

| Field             | Description                                                              | Type             | Required | Example                               |
|----------------------|--------------------------------------------------------------------------|-----------------|----------|---------------------------------------|
| `hs_timestamp`     | Due date (Unix timestamp in milliseconds or UTC format)                 | String/Number   | Yes      | `1678886400000` or `"2024-03-15T12:00:00Z"` |
| `hs_task_body`     | Task notes                                                              | String           | No       | "Send proposal"                       |
| `hubspot_owner_id` | ID of the user assigned to the task                                      | String           | No       | "64492917"                           |
| `hs_task_subject`  | Task title                                                              | String           | No       | "Follow-up with client"              |
| `hs_task_status`   | Task status (`COMPLETED` or `NOT_STARTED`)                             | String           | No       | "NOT_STARTED"                        |
| `hs_task_priority` | Task priority (`LOW`, `MEDIUM`, or `HIGH`)                               | String           | No       | "HIGH"                               |
| `hs_task_type`     | Task type (`EMAIL`, `CALL`, or `TODO`)                                   | String           | No       | "CALL"                                |
| `hs_task_reminders`| Timestamp for reminder (Unix timestamp in milliseconds)                   | Number           | No       | `1678886400000`                       |


**Associations Object:** (Optional, for associating with existing records)

```json
"associations": [
  {
    "to": {
      "id": 101 // ID of the record to associate with
    },
    "types": [
      {
        "associationCategory": "HUBSPOT_DEFINED",
        "associationTypeId": 204 // Association type ID (see HubSpot docs for available IDs)
      }
    ]
  }
]
```

**Example Request:**

```json
{
  "properties": {
    "hs_timestamp": "2024-03-15T12:00:00Z",
    "hs_task_body": "Send proposal",
    "hubspot_owner_id": "64492917",
    "hs_task_subject": "Follow up with client",
    "hs_task_priority": "HIGH",
    "hs_task_type": "CALL"
  },
  "associations": [
    {
      "to": {"id": 123},
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 204}]
    }
  ]
}
```

**Response:**  JSON object containing the created task details, including its ID.


## 2. Retrieve Tasks

**Method:** `GET /crm/v3/objects/tasks` (for all tasks) or `GET /crm/v3/objects/tasks/{taskId}` (for a single task)

**Parameters:**

| Parameter     | Description                                      | Type    |
|---------------|--------------------------------------------------|---------|
| `limit`       | Maximum number of results per page               | Integer |
| `properties`  | Comma-separated list of properties to return    | String  |
| `associations`| Comma-separated list of object types for associations | String  |


**Example Request (single task):** `GET /crm/v3/objects/tasks/123?properties=hs_task_subject,hs_timestamp`

**Response:** JSON object or array of JSON objects representing the task(s).


## 3. Update a Task

**Method:** `PATCH /crm/v3/objects/tasks/{taskId}`

**Request Body:** JSON object with `properties` object containing the fields to update.

**Example Request:**

```json
{
  "properties": {
    "hs_task_status": "COMPLETED",
    "hs_task_body": "Proposal sent"
  }
}
```

**Response:** JSON object representing the updated task.


## 4. Associate Existing Task with Records

**Method:** `PUT /crm/v3/objects/tasks/{taskId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Parameters:**

| Parameter       | Description                                    | Type    |
|-----------------|------------------------------------------------|---------|
| `taskId`         | ID of the task                                  | Integer |
| `toObjectType`  | Type of object to associate (e.g., "contacts") | String  |
| `toObjectId`    | ID of the object to associate                 | Integer |
| `associationTypeId` | ID of the association type                     | Integer |


**Example Request:** `PUT /crm/v3/objects/tasks/123/associations/contacts/456/204`


## 5. Remove an Association

**Method:** `DELETE /crm/v3/objects/tasks/{taskId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Parameters:** Same as for associating a task.


## 6. Pin a Task

Pinning is done by including the task `id` in the `hs_pinned_engagement_id` field when creating or updating a record via the relevant object APIs (contacts, companies, deals, etc.).


## 7. Delete a Task

**Method:** `DELETE /crm/v3/objects/tasks/{taskId}`

**Response:**  A success or error message.


**Note:**  This documentation provides a summary. Refer to the official HubSpot API documentation for complete details, including error handling, rate limits, and authentication.  The `associationTypeId` values need to be retrieved from the HubSpot association API as mentioned in the original text.  Batch operations are also available as indicated in the original text but details are omitted here for brevity.
