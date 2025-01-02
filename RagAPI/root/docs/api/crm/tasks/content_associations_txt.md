# HubSpot Tasks API Documentation

This document details the HubSpot Tasks API, allowing you to create, manage, and interact with tasks within the HubSpot CRM.

## API Endpoints

All endpoints are under the base URL `/crm/v3/objects/tasks`.  Remember to replace placeholders like `{taskId}` with actual IDs.

### 1. Create a Task (POST /crm/v3/objects/tasks)

Creates a new task.

**Request Body:**

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27T12:00:00Z",  // Required. Due date (UTC or Unix timestamp in milliseconds)
    "hs_task_body": "Send follow-up email",     // Task notes
    "hubspot_owner_id": "12345",                // Owner's ID
    "hs_task_subject": "Client X Follow Up",    // Task title
    "hs_task_status": "NOT_STARTED",            // Status: COMPLETED or NOT_STARTED
    "hs_task_priority": "HIGH",                 // Priority: LOW, MEDIUM, HIGH
    "hs_task_type": "EMAIL",                    // Type: EMAIL, CALL, TODO
    "hs_task_reminders": 1677628800000          // Reminder timestamp (Unix milliseconds)
  },
  "associations": [                         // Optional: Associate with records
    {
      "to": { "id": 67890 },                // ID of the record
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 204          // Association type ID (see notes below)
        }
      ]
    }
  ]
}
```

**Response:**  A JSON object representing the newly created task, including its ID.

**Notes:**  `associationTypeId` values are defined within HubSpot.  You can find common IDs in the HubSpot documentation or use the Associations API to retrieve IDs for custom associations.


### 2. Retrieve Tasks

#### 2.1 Retrieve a Single Task (GET /crm/v3/objects/tasks/{taskId})

Retrieves a specific task by its ID.

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.

**Response:** A JSON object representing the task.

#### 2.2 Retrieve Multiple Tasks (GET /crm/v3/objects/tasks)

Retrieves a list of tasks.

**Query Parameters:**

* `limit`: Maximum number of results per page.
* `properties`: Comma-separated list of properties to return.


**Response:** A JSON object containing a list of tasks and pagination information.


### 3. Update a Task (PATCH /crm/v3/objects/tasks/{taskId})

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

**Notes:** HubSpot ignores properties not specified or that are read-only.  To clear a property, send an empty string (`""`).


### 4. Associate an Existing Task with a Record (PUT /crm/v3/objects/tasks/{taskId}/associations/{toObjectType}/{toObjectId}/{associationTypeId})

Associates an existing task with another HubSpot record.

**Path Parameters:**

* `taskId`: ID of the task.
* `toObjectType`: Type of object (e.g., `contacts`, `companies`).
* `toObjectId`: ID of the record to associate.
* `associationTypeId`:  Association type ID.


**Response:**  A success message or error.


### 5. Remove an Association (DELETE /crm/v3/objects/tasks/{taskId}/associations/{toObjectType}/{toObjectId}/{associationTypeId})

Removes an association between a task and a record.  Uses the same path parameters as the association endpoint.


### 6. Pin a Task (Create/Update Record via Object APIs)

Pinning a task is done indirectly by including the task's ID (`id`) in the `hs_pinned_engagement_id` field when creating or updating the associated record (contact, company, deal, etc.) via their respective object APIs.  Only one activity can be pinned per record.


### 7. Delete a Task (DELETE /crm/v3/objects/tasks/{taskId})

Deletes a task (moves it to the recycling bin).


## Error Handling

The API will return standard HTTP status codes and JSON error responses to indicate success or failure.  Refer to the HubSpot API documentation for specific error codes and their meanings.


## Authentication

You'll need a HubSpot API key for authentication.  Refer to the HubSpot developer documentation for details on obtaining and using API keys.  The typical authentication method is via an API key in the request header.


This documentation provides a concise overview. For complete details and advanced usage, consult the official HubSpot API documentation.
