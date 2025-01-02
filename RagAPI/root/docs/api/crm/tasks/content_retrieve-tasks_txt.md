# HubSpot Tasks API Documentation

This document describes the HubSpot Tasks API, allowing you to create, manage, and interact with tasks within the HubSpot CRM.

## API Endpoints

All endpoints are under the `/crm/v3/objects/tasks` base path.  Remember to replace `{taskId}` and other placeholders with actual values.  Authentication is required (details not provided in the source text).

### 1. Create a Task (POST `/crm/v3/objects/tasks`)

Creates a new task.

**Request Body:**

```json
{
  "properties": {
    "hs_timestamp": "2024-03-15T12:00:00Z", // Required. Due date in UTC format or Unix timestamp (milliseconds)
    "hs_task_body": "Send email to client",
    "hubspot_owner_id": "12345", // ID of the task owner
    "hs_task_subject": "Project X Update",
    "hs_task_status": "NOT_STARTED", // or "COMPLETED"
    "hs_task_priority": "HIGH", // or "MEDIUM", "LOW"
    "hs_task_type": "EMAIL", // or "CALL", "TODO"
    "hs_task_reminders": 1678900000000 // Unix timestamp (milliseconds) for reminder
  },
  "associations": [
    {
      "to": {
        "id": 67890 // ID of associated record (e.g., contact ID)
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 204 // Association type ID (see notes below)
        }
      ]
    }
  ]
}
```

**Response:**  A JSON object representing the newly created task, including its ID.

**Notes:**

* `associationTypeId`:  The default association type IDs are listed in the HubSpot documentation.  Custom association types can be retrieved via the HubSpot Associations API.  `204` is a common type.


### 2. Retrieve Tasks

**a) Retrieve a Single Task (GET `/crm/v3/objects/tasks/{taskId}`)**

Retrieves a specific task by its ID.

**Request Parameters:**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.

**Response:** A JSON object representing the task.


**b) Retrieve Multiple Tasks (GET `/crm/v3/objects/tasks`)**

Retrieves a list of tasks.

**Request Parameters:**

* `limit`: Maximum number of results per page.
* `properties`: Comma-separated list of properties to return.

**Response:** A JSON object containing a list of tasks and pagination information.


### 3. Update a Task (PATCH `/crm/v3/objects/tasks/{taskId}`)

Updates an existing task.

**Request Body:**

```json
{
  "properties": {
    "hs_task_subject": "Updated Task Subject",
    "hs_task_status": "COMPLETED"
  }
}
```

**Response:** A JSON object representing the updated task.

**Notes:** HubSpot ignores values for read-only and non-existent properties. To clear a property, send an empty string.


### 4. Associate Existing Task with Records (PUT `/crm/v3/objects/tasks/{taskId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates an existing task with another HubSpot record.

**Path Parameters:**

* `taskId`: ID of the task.
* `toObjectType`: Type of object (e.g., "contacts", "companies").
* `toObjectId`: ID of the object to associate with.
* `associationTypeId`: Association type ID.


**Response:**  Success/failure indication.


### 5. Remove Association (DELETE `/crm/v3/objects/tasks/{taskId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Removes an association between a task and a record. Uses the same path parameters as the associate endpoint.


### 6. Pin a Task (Indirectly via Object APIs)

Pinning a task is achieved by including the task's `id` in the `hs_pinned_engagement_id` field when creating or updating a record via other HubSpot object APIs (contacts, companies, deals, etc.).


### 7. Delete a Task (DELETE `/crm/v3/objects/tasks/{taskId}`)

Deletes a task (moves it to the recycling bin).

**Response:** Success/failure indication.


## Error Handling

The API will return standard HTTP status codes to indicate success or failure (e.g., 200 OK, 400 Bad Request, 404 Not Found).  Specific error details will be included in the response body as JSON.


This documentation provides a summary.  Refer to the official HubSpot API documentation for complete details, including rate limits, authentication methods, and advanced features.
