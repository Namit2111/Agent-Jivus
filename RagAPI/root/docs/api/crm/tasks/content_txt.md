# HubSpot Tasks API Documentation

This document describes the HubSpot Tasks API, allowing you to create, manage, and interact with tasks within HubSpot.

## API Endpoints

All endpoints are under the `/crm/v3/objects/tasks` base path.  Remember to replace `{taskId}` and other placeholders with actual values.

### 1. Create a Task (POST `/crm/v3/objects/tasks`)

Creates a new task in HubSpot.

**Request Body:**

```json
{
  "properties": {
    "hs_timestamp": "2024-03-15T12:00:00Z", // Required. Due date (UTC or Unix timestamp in milliseconds)
    "hs_task_body": "Send follow-up email",
    "hubspot_owner_id": "12345", // ID of the task owner
    "hs_task_subject": "Client Project Update",
    "hs_task_status": "NOT_STARTED", // or "COMPLETED"
    "hs_task_priority": "HIGH", // or "LOW", "MEDIUM"
    "hs_task_type": "EMAIL", // or "CALL", "TODO"
    "hs_task_reminders": 1700000000000 // Reminder timestamp (Unix timestamp in milliseconds)
  },
  "associations": [
    {
      "to": {
        "id": 67890 // ID of the associated record (e.g., contact)
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 204 // Association type ID.  See notes below.
        }
      ]
    }
  ]
}
```

**Response:**  A JSON object representing the newly created task, including its ID.

**Notes:**

* `hs_timestamp` is required.  Unix timestamps are milliseconds since the epoch.
* `associationTypeId` defaults are documented in the HubSpot documentation.  For custom association types, use the Associations API.


### 2. Retrieve Tasks (GET `/crm/v3/objects/tasks`)

Retrieves tasks.  Can retrieve a single task or a list of tasks.

**Retrieve a single task (GET `/crm/v3/objects/tasks/{taskId}`):**

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.

**Retrieve multiple tasks (GET `/crm/v3/objects/tasks`):**

**Query Parameters:**

* `limit`: Maximum number of results per page.
* `properties`: Comma-separated list of properties to return.


**Response:** A JSON object (single task) or a JSON array (multiple tasks).


### 3. Update a Task (PATCH `/crm/v3/objects/tasks/{taskId}`)

Updates an existing task.

**Request Body:**

```json
{
  "properties": {
    "hs_task_status": "COMPLETED",
    "hs_task_body": "Updated task notes"
  }
}
```

**Response:** A JSON object representing the updated task.


### 4. Associate Existing Task with Records (PUT `/crm/v3/objects/tasks/{taskId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates an existing task with a record.

**Path Parameters:**

* `taskId`: ID of the task.
* `toObjectType`: Type of object (e.g., `contacts`, `deals`).
* `toObjectId`: ID of the record.
* `associationTypeId`: Association type ID.


**Response:**  A success/failure indicator.


### 5. Remove an Association (DELETE `/crm/v3/objects/tasks/{taskId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Removes an association between a task and a record.  Uses the same path parameters as the `Associate Existing Task` endpoint.

**Response:** A success/failure indicator.


### 6. Pin a Task (Update Record via Object APIs)

Pinning a task requires updating the associated record (contact, deal, etc.) using its respective object API.  Include the task's ID in the `hs_pinned_engagement_id` field.  See the HubSpot documentation for details on the specific object APIs.


### 7. Delete a Task (DELETE `/crm/v3/objects/tasks/{taskId}`)

Deletes a task (moves it to the recycling bin).

**Response:** A success/failure indicator.


## Error Handling

The API will return standard HTTP status codes (e.g., 400 Bad Request, 404 Not Found, 500 Internal Server Error) along with JSON error responses providing details about the failure.


##  Authentication

You will need a HubSpot API key for authentication.  Refer to the HubSpot API documentation for details on obtaining and using API keys.
