# HubSpot Tasks API Documentation

This document details the HubSpot Tasks API, allowing you to create, manage, and interact with tasks within the HubSpot CRM.

## API Endpoints Base URL: `/crm/v3/objects/tasks`

All endpoints below use this base URL unless otherwise specified.  Replace `{taskId}` with the actual task ID.


## 1. Create a Task

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/tasks`

**Request Body:**

The request body must contain a `properties` object and optionally an `associations` object.

* **`properties` object:**  Contains task details.

| Field             | Description                                                              | Type             | Required | Example                               |
|----------------------|--------------------------------------------------------------------------|-----------------|----------|---------------------------------------|
| `hs_timestamp`      | Due date (Unix timestamp in milliseconds or UTC format)                   | String/Number   | Yes      | `1678886400000` (or `2023-03-15T00:00:00Z`) |
| `hs_task_body`       | Task notes                                                              | String           | No       | "Send Proposal"                       |
| `hubspot_owner_id`   | ID of the assigned user                                                  | String           | No       | "64492917"                           |
| `hs_task_subject`    | Task title                                                              | String           | No       | "Follow-up for Brian Buyer"          |
| `hs_task_status`     | Task status (`COMPLETED` or `NOT_STARTED`)                               | String           | No       | "WAITING"                             |
| `hs_task_priority`   | Task priority (`LOW`, `MEDIUM`, or `HIGH`)                              | String           | No       | "HIGH"                               |
| `hs_task_type`       | Task type (`EMAIL`, `CALL`, or `TODO`)                                   | String           | No       | "CALL"                               |
| `hs_task_reminders`  | Reminder timestamp (Unix timestamp in milliseconds)                      | Number           | No       | `1678886400000`                       |


* **`associations` object (optional):** Associates the task with existing records.

```json
[
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

* `to.id`: ID of the record to associate with.
* `types`: Association type.  `associationTypeId` can be obtained from the Associations API.  204 is a common default.


**Response:**  A JSON object representing the created task, including its ID.


**Example Request (cURL):**

```bash
curl -X POST \
  https://api.hubspot.com/crm/v3/objects/tasks \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -d '{
    "properties": {
      "hs_timestamp": "2024-03-15T12:00:00Z",
      "hs_task_body": "Send a follow-up email",
      "hubspot_owner_id": "12345",
      "hs_task_subject": "Project X Follow-up"
    }
  }'
```


## 2. Retrieve Tasks

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/tasks` (for all tasks) or `/crm/v3/objects/tasks/{taskId}` (for a single task)

**Parameters (for both endpoints):**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.


**Parameters (for `/crm/v3/objects/tasks` only):**

* `limit`: Maximum number of results per page.


**Response:**  A JSON object containing a list of tasks (for the all-tasks endpoint) or a single task object (for the single-task endpoint).


## 3. Update a Task

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/tasks/{taskId}`

**Request Body:**

A JSON object with a `properties` object containing the fields to update.  Leave out fields you don't want to change.  An empty string (`""`) will clear a property value.

**Example Request (cURL):**

```bash
curl -X PATCH \
  https://api.hubspot.com/crm/v3/objects/tasks/12345 \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -d '{
    "properties": {
      "hs_task_status": "COMPLETED"
    }
  }'
```

**Response:**  Updated task object.


## 4. Associate Existing Tasks with Records

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/tasks/{taskId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

| Field           | Description                                  | Example      |
|-----------------|----------------------------------------------|---------------|
| `taskId`        | ID of the task                              | `12345`       |
| `toObjectType`  | Object type (e.g., `contacts`, `companies`) | `contacts`    |
| `toObjectId`    | ID of the record to associate with           | `67890`       |
| `associationTypeId` | Association type ID (from Associations API) | `204`         |


**Response:**  Confirmation of association.


## 5. Remove an Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/tasks/{taskId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`  (Same as Associate)

**Response:** Confirmation of removal.


## 6. Pin a Task (Indirectly)

Pinning is done indirectly by including the task's `id` in the `hs_pinned_engagement_id` field when creating or updating a record (e.g., contact, company) via their respective object APIs. Only one activity can be pinned per record.


## 7. Delete a Task

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/tasks/{taskId}`

**Response:** Confirmation of deletion (moves to recycle bin).


**Note:**  Always replace placeholders like `{taskId}`, `YOUR_API_KEY`, etc., with your actual values.  Error handling and authentication are crucial in real-world implementations.  Consult the HubSpot API documentation for detailed error codes and best practices.
