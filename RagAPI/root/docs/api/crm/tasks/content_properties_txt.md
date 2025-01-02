# HubSpot Tasks API Documentation

This document details the HubSpot Tasks API, allowing you to create, manage, and interact with tasks within the HubSpot CRM.

## API Endpoints

All endpoints are under the base URL `/crm/v3/objects/tasks`.  Replace `{taskId}` and `{toObjectId}` with the relevant IDs.


## 1. Create a Task (POST `/crm/v3/objects/tasks`)

Creates a new task in HubSpot.

**Request Body:**

```json
{
  "properties": {
    "hs_timestamp": "2024-03-08T12:00:00Z", // Required. Due date (UTC or Unix timestamp in milliseconds)
    "hs_task_body": "Send follow-up email", // Task notes
    "hubspot_owner_id": "12345", // ID of the assigned user
    "hs_task_subject": "Client Project Update", // Task title
    "hs_task_status": "NOT_STARTED", // "COMPLETED" or "NOT_STARTED"
    "hs_task_priority": "HIGH", // "LOW", "MEDIUM", or "HIGH"
    "hs_task_type": "EMAIL", // "EMAIL", "CALL", or "TODO"
    "hs_task_reminders": 1678387200000 // Reminder timestamp (Unix timestamp in milliseconds)
  },
  "associations": [ // Optional. Associate with existing records
    {
      "to": {
        "id": 101 // ID of the record (e.g., contact ID)
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


**Association Type IDs:**  Default association type IDs are documented in the HubSpot API documentation.  Custom association types can be retrieved via the HubSpot Associations API.  `associationTypeId: 204` is commonly used for associating tasks with contacts.


**Example cURL Request:**

```bash
curl -X POST \
  https://api.hubspot.com/crm/v3/objects/tasks \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{your request body}'
```

## 2. Retrieve Tasks

### 2.1 Get a Single Task (GET `/crm/v3/objects/tasks/{taskId}`)

Retrieves a specific task by its ID.

**Parameters:**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.

**Example:**

```bash
curl -X GET \
  https://api.hubspot.com/crm/v3/objects/tasks/12345 \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -G \
  --data-urlencode 'properties=hs_task_subject,hs_task_body' \
  --data-urlencode 'associations=contacts'
```


### 2.2 Get All Tasks (GET `/crm/v3/objects/tasks`)

Retrieves a list of tasks.

**Parameters:**

* `limit`: Maximum number of results per page.
* `properties`: Comma-separated list of properties to return.

## 3. Update a Task (PATCH `/crm/v3/objects/tasks/{taskId}`)

Updates an existing task.  Only provide the properties you want to change.

**Request Body:**

```json
{
  "properties": {
    "hs_task_status": "COMPLETED"
  }
}
```

## 4. Associate Existing Task with Records (PUT `/crm/v3/objects/tasks/{taskId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates an existing task with a record.

**Parameters:**

* `taskId`: Task ID
* `toObjectType`: Object type (e.g., `contacts`, `companies`)
* `toObjectId`: ID of the record
* `associationTypeId`: Association type ID


## 5. Remove an Association (DELETE `/crm/v3/objects/tasks/{taskId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Removes an association between a task and a record.  Uses the same URL structure as associating.


## 6. Pin a Task (Update Record via Object APIs)

Pinning a task involves updating the record (e.g., contact, company) it's associated with, using the `hs_pinned_engagement_id` field.  See the HubSpot documentation for contacts, companies, etc. APIs for details.


## 7. Delete a Task (DELETE `/crm/v3/objects/tasks/{taskId}`)

Deletes a task (moves it to the recycle bin).


**Note:**  Batch operations (create, update, delete, retrieve) are also supported via other endpoints; refer to the HubSpot API documentation for details.  Remember to replace `YOUR_API_KEY` with your actual HubSpot API key.  Error handling and authentication details are not included here but are crucial for production implementation.  Consult HubSpot's API documentation for a comprehensive understanding of error codes and best practices.
