# HubSpot Tasks API Documentation

This document details the HubSpot Tasks API, allowing you to create, manage, and interact with tasks within the HubSpot CRM.

## API Endpoints

All endpoints are located under the `/crm/v3/objects/tasks` base path.  Remember to replace `{taskId}` and `{toObjectId}` with the appropriate IDs.


## 1. Create a Task (POST `/crm/v3/objects/tasks`)

Creates a new task in HubSpot.

**Request Body:**

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27T12:00:00Z", // Required. Due date in UTC or Unix timestamp (milliseconds)
    "hs_task_body": "Send follow-up email",
    "hubspot_owner_id": "12345", // HubSpot ID of the task owner
    "hs_task_subject": "Project X Follow-up",
    "hs_task_status": "NOT_STARTED", // or "COMPLETED"
    "hs_task_priority": "HIGH", // or "LOW", "MEDIUM"
    "hs_task_type": "EMAIL", // or "CALL", "TODO"
    "hs_task_reminders": 1703732400000 //Reminder timestamp in milliseconds (Unix)
  },
  "associations": [
    {
      "to": {
        "id": 67890 // ID of the associated record (e.g., contact ID)
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 204 // Association type ID (See notes below)
        }
      ]
    }
  ]
}
```

**Response (Success):**  A JSON object representing the newly created task, including its ID.

**Notes:**

* `hs_timestamp` is **required**.
* `associationTypeId` represents the type of association (e.g., task to contact).  You can find default IDs in the HubSpot documentation or use the Associations API to retrieve IDs for custom associations.


## 2. Retrieve Tasks

### 2.1 Retrieve a Single Task (GET `/crm/v3/objects/tasks/{taskId}`)

Retrieves a single task by its ID.

**Request Parameters:**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.

**Response (Success):** A JSON object representing the task.

### 2.2 Retrieve Multiple Tasks (GET `/crm/v3/objects/tasks`)

Retrieves a list of tasks.

**Request Parameters:**

* `limit`: Maximum number of results per page.
* `properties`: Comma-separated list of properties to return.

**Response (Success):** A JSON object containing a list of tasks and pagination information.


## 3. Update a Task (PATCH `/crm/v3/objects/tasks/{taskId}`)

Updates an existing task.

**Request Body:**

```json
{
  "properties": {
    "hs_task_status": "COMPLETED",
    "hs_task_body": "Email sent successfully"
  }
}
```

**Response (Success):** A JSON object representing the updated task.

**Notes:** HubSpot ignores read-only and non-existent properties.  To clear a property, pass an empty string.


## 4. Associate Existing Task with Records (PUT `/crm/v3/objects/tasks/{taskId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates an existing task with a record.

**Request URL Parameters:**

* `taskId`: The ID of the task.
* `toObjectType`: The type of object (e.g., "contacts", "deals").
* `toObjectId`: The ID of the record.
* `associationTypeId`:  The ID of the association type.


**Response (Success):**  A successful response (typically an empty body or a 204 status code).


## 5. Remove an Association (DELETE `/crm/v3/objects/tasks/{taskId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Removes an association between a task and a record.  Uses the same URL as the associate endpoint.


**Response (Success):**  A successful response (typically an empty body or a 204 status code).


## 6. Pin a Task (Update Record using `hs_pinned_engagement_id`)

Pinning a task is done indirectly by including the task's ID in the `hs_pinned_engagement_id` field when creating or updating the associated record (e.g., using the Contacts API).


## 7. Delete a Task (DELETE `/crm/v3/objects/tasks/{taskId}`)

Deletes a task (moves it to the recycling bin).

**Response (Success):** A successful response (typically an empty body or a 204 status code).


## Error Handling

The API will return standard HTTP status codes to indicate success or failure.  Check the response body for detailed error messages.


## Authentication

You will need a HubSpot API key for authentication.  Refer to the HubSpot developer documentation for details on obtaining and using API keys.


This documentation provides a concise overview. For complete details, including batch operations and further specifics on request parameters, refer to the official HubSpot API documentation.
