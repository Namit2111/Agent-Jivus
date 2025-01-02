# HubSpot Tasks API Documentation

This document details the HubSpot Tasks API, allowing you to create, manage, and retrieve tasks within HubSpot.

## API Endpoints

All endpoints are under the `/crm/v3/objects/tasks` base path.  Remember to replace `{taskId}` and `{toObjectId}` with the appropriate IDs.

## 1. Create a Task (POST `/crm/v3/objects/tasks`)

Creates a new task in HubSpot.

**Request Body:**

```json
{
  "properties": {
    "hs_timestamp": "2024-03-15T12:00:00Z",  // Required. Due date in UTC or Unix timestamp (milliseconds)
    "hs_task_body": "Send follow-up email",     // Task description
    "hubspot_owner_id": "12345",                 // ID of the assigned user
    "hs_task_subject": "Client onboarding",      // Task title
    "hs_task_status": "NOT_STARTED",             // "COMPLETED" or "NOT_STARTED"
    "hs_task_priority": "HIGH",                  // "LOW", "MEDIUM", or "HIGH"
    "hs_task_type": "EMAIL",                     // "EMAIL", "CALL", or "TODO"
    "hs_task_reminders": 1678900000000           // Reminder timestamp (Unix milliseconds) - Optional
  },
  "associations": [                             // Optional. Associate with existing records
    {
      "to": {
        "id": 101
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 204  //  See default association type IDs or use Associations API for custom types.
        }
      ]
    }
  ]
}
```

**Response:**  A JSON object representing the newly created task, including its ID.

**Example Response (truncated):**

```json
{
  "id": "12345678",
  // ... other properties ...
}
```


## 2. Retrieve Tasks

### 2.1 Retrieve a Single Task (GET `/crm/v3/objects/tasks/{taskId}`)

Retrieves a specific task by its ID.

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.


### 2.2 Retrieve a List of Tasks (GET `/crm/v3/objects/tasks`)

Retrieves a list of tasks.

**Query Parameters:**

* `limit`: Maximum number of results per page.
* `properties`: Comma-separated list of properties to return.


## 3. Update a Task (PATCH `/crm/v3/objects/tasks/{taskId}`)

Updates an existing task.

**Request Body:**

```json
{
  "properties": {
    "hs_task_status": "COMPLETED",
    "hs_task_body": "Updated task description"
  }
}
```

**Response:** A JSON object representing the updated task.


## 4. Associate Existing Task with Records (PUT `/crm/v3/objects/tasks/{taskId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates an existing task with a record.

**Path Parameters:**

* `taskId`: The ID of the task.
* `toObjectType`: The type of object (e.g., "contacts", "companies").
* `toObjectId`: The ID of the record.
* `associationTypeId`:  The ID of the association type (use Associations API or default IDs).


## 5. Remove an Association (DELETE `/crm/v3/objects/tasks/{taskId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Removes an association between a task and a record.  Uses the same path parameters as the association creation endpoint.


## 6. Pin a Task (Update Record via Object APIs)

Pin a task to a record using the `hs_pinned_engagement_id` field when creating or updating the record via its respective object API (e.g., contacts, companies).


## 7. Delete a Task (DELETE `/crm/v3/objects/tasks/{taskId}`)

Deletes a task (moves it to the recycling bin).


##  Important Notes:

* **Error Handling:** The API returns standard HTTP status codes and JSON error responses.
* **Authentication:** Requires HubSpot API key authentication.
* **Rate Limits:**  Be mindful of HubSpot's API rate limits.
* **Associations API:** Refer to the HubSpot Associations API documentation for details on association types and IDs.  Default IDs are mentioned in the original text but are not provided.  You would need to find that additional documentation.
* **Batch Operations:** The documentation mentions batch capabilities for creating, updating, and deleting tasks.  Consult the "Endpoints" tab (not provided in the text) for more details.


This markdown provides a structured overview of the HubSpot Tasks API. Remember to refer to the official HubSpot API documentation for the most up-to-date information and complete details.
