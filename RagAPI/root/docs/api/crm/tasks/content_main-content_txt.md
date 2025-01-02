# HubSpot Tasks API Documentation

This document describes the HubSpot Tasks API, allowing you to create, manage, and retrieve tasks within HubSpot.

## API Endpoints

All endpoints are located under the `/crm/v3/objects/tasks` base path.  Remember to replace placeholders like `{taskId}` with the actual ID.

### 1. Create a Task (POST `/crm/v3/objects/tasks`)

Creates a new task in HubSpot.

**Request Body:**

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27T12:00:00Z", // Required. Due date (Unix timestamp in milliseconds or UTC format)
    "hs_task_body": "Send follow-up email", // Task notes
    "hubspot_owner_id": "12345", // ID of the task owner
    "hs_task_subject": "Client Project Update", // Task title
    "hs_task_status": "NOT_STARTED", // "COMPLETED" or "NOT_STARTED"
    "hs_task_priority": "HIGH", // "LOW", "MEDIUM", or "HIGH"
    "hs_task_type": "EMAIL", // "EMAIL", "CALL", or "TODO"
    "hs_task_reminders": 1677452800000 // Reminder timestamp (Unix timestamp in milliseconds)
  },
  "associations": [
    {
      "to": {
        "id": 67890 // ID of the associated record (e.g., contact ID)
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 204 // Association type ID. See notes below.
        }
      ]
    }
  ]
}
```

**Response:**  A JSON object representing the created task, including its ID.

**Notes:**

* `hs_timestamp` is required.
* `associationTypeId` defaults are listed in the HubSpot documentation; for custom types, use the Associations API.


### 2. Retrieve Tasks

#### 2.1 Get a Single Task (GET `/crm/v3/objects/tasks/{taskId}`)

Retrieves a single task by its ID.

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.

**Example:** `/crm/v3/objects/tasks/12345?properties=hs_task_subject,hs_task_body&associations=contacts`

**Response:** A JSON object representing the task.

#### 2.2 Get All Tasks (GET `/crm/v3/objects/tasks`)

Retrieves a list of tasks.

**Query Parameters:**

* `limit`: Maximum number of results per page.
* `properties`: Comma-separated list of properties to return.

**Response:** A JSON object containing a list of tasks and pagination information.


### 3. Update a Task (PATCH `/crm/v3/objects/tasks/{taskId}`)

Updates an existing task.

**Request Body:**

```json
{
  "properties": {
    "hs_task_status": "COMPLETED"
  }
}
```

**Response:** A JSON object representing the updated task.

**Note:** HubSpot ignores read-only and non-existent properties.  To clear a property, pass an empty string.


### 4. Associate Existing Task with Records (PUT `/crm/v3/objects/tasks/{taskId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates an existing task with a record.

**Path Parameters:**

* `taskId`: ID of the task.
* `toObjectType`: Type of object (e.g., "contacts", "deals").
* `toObjectId`: ID of the record.
* `associationTypeId`: Association type ID.


### 5. Remove Association (DELETE `/crm/v3/objects/tasks/{taskId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Removes an association between a task and a record.  Uses the same path parameters as the association creation endpoint.


### 6. Pin a Task (Update Record via Object APIs)

Pins a task to a record's timeline using the `hs_pinned_engagement_id` field when updating the record via its respective object API (contacts, companies, etc.).


### 7. Delete a Task (DELETE `/crm/v3/objects/tasks/{taskId}`)

Deletes a task (moves it to the recycling bin).


## Error Handling

The API will return standard HTTP status codes and JSON error responses indicating the nature of any problems encountered.  Refer to the HubSpot API documentation for details on specific error codes.


## Rate Limits

Be mindful of the HubSpot API rate limits to avoid throttling.


This documentation provides a concise overview.  Consult the official HubSpot API documentation for comprehensive details and the most up-to-date information.
