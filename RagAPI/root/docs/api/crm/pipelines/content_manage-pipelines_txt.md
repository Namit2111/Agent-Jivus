# HubSpot CRM API: Pipelines

This document details the HubSpot CRM API endpoints for managing pipelines and their stages. Pipelines track records through stages (e.g., sales pipelines, service pipelines).  The availability of multiple pipelines per object depends on your HubSpot subscription.

Supported Objects:

* Deals
* Tickets
* Appointments
* Courses
* Listings
* Orders
* Services
* Leads (Sales Hub Professional and Enterprise only)
* Custom objects (Enterprise only)


## I. Managing Pipelines

### A. Create a Pipeline (POST `/crm/v3/pipelines/{objectType}`)

Creates a new pipeline for the specified object type.

**Request Body:**

```json
{
  "displayOrder": 3, // Integer: Pipeline display order.  Lower numbers appear first. Ties are broken alphabetically by label.
  "label": "New deal pipeline", // String: Pipeline name.
  "stages": [ // Array of stage objects.
    {
      "label": "In Progress",
      "metadata": {
        "probability": "0.2" // Required for deals (0.0-1.0), optional for others.  For tickets, use "ticketState": "OPEN" or "CLOSED"
      },
      "displayOrder": 0
    },
    // ... more stages
  ]
}
```

**Example Request (Deals):**

```bash
curl -X POST \
  'https://api.hubapi.com/crm/v3/pipelines/deals' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -d '{
    "displayOrder": 3,
    "label": "New deal pipeline",
    "stages": [
      {
        "label": "In Progress",
        "metadata": {
          "probability": "0.2"
        },
        "displayOrder": 0
      },
      {
        "label": "Contract signed",
        "metadata": {
          "probability": "0.8"
        },
        "displayOrder": 1
      },
      {
        "label": "Closed Won",
        "metadata": {
          "probability": "1.0"
        },
        "displayOrder": 2
      },
      {
        "label": "Closed Lost",
        "metadata": {
          "probability": "0.0"
        },
        "displayOrder": 3
      }
    ]
  }'
```

**Response (Success):**  A JSON object representing the newly created pipeline, including its ID.

**Note:**  `appointment`, `course`, `listing`, `lead`, `order`, and `service` pipelines can have up to 30 stages. `deal`, `ticket`, and `custom object` pipelines can have up to 100 stages.


### B. Replace a Pipeline (PUT `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Replaces an existing pipeline with the data provided in the request body.

**Request Body:** Same as creating a new pipeline.

**Response (Success):** A JSON object representing the updated pipeline.


### C. Retrieve Pipelines (GET `/crm/v3/pipelines/{objectType}`)

Retrieves all pipelines for a given object type.

**Response:** A JSON object containing an array of pipeline objects. Each object includes `id`, `label`, `displayOrder`, and timestamps.


### D. Retrieve a Pipeline (GET `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Retrieves a specific pipeline by ID.

**Response:** A JSON object representing the pipeline.


### E. Update a Pipeline (PATCH `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Updates specific properties of a pipeline (e.g., `label`, `displayOrder`).  Use stage endpoints to update stages.

**Request Body:** A JSON object containing the properties to update.

**Response (Success):** A JSON object representing the updated pipeline.


### F. Delete a Pipeline (DELETE `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Deletes a pipeline.

**Query Parameter:** `validateReferencesBeforeDelete=true` (optional) - Checks for associated records. If records exist, returns a 404 error with details.

**Response (Success):**  A success message.

**Response (Error - Records Exist):**

```json
{
  "status": "error",
  "message": "Stage IDs: [...] are being referenced by object IDs: [...]",
  "correlationId": "...",
  "context": {
    "stageIds": [...],
    "objectIds": [...]
  },
  "category": "VALIDATION_ERROR",
  "subCategory": "PipelineError.STAGE_ID_IN_USE"
}
```



## II. Managing Pipeline Stages

### A. Create a Stage (POST `/crm/v3/pipelines/{objectType}/{pipelineId}/stages`)

Creates a new stage within a specified pipeline.

**Request Body:**

```json
{
  "displayOrder": 4, // Integer: Stage display order within the pipeline.
  "label": "Contract signed", // String: Stage name. Must be unique within the pipeline.
  "metadata": {
    "probability": "0.8" // Required for deals (0.0-1.0), optional for others. For tickets, use "ticketState": "OPEN" or "CLOSED"
  }
}
```

**Response (Success):** A JSON object representing the newly created stage, including its ID.


### B. Replace a Stage (PUT `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Replaces an existing stage with the data provided in the request body.

**Request Body:** Same as creating a new stage.

**Response (Success):** A JSON object representing the updated stage.


### C. Retrieve Stages (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/stages`)

Retrieves all stages for a given pipeline.

**Response:** A JSON object containing an array of stage objects.


### D. Retrieve a Stage (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Retrieves a specific stage by ID.

**Response:** A JSON object representing the stage.


### E. Update a Stage (PATCH `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Updates specific properties of a stage (e.g., `label`, `displayOrder`).

**Request Body:** A JSON object containing the properties to update.

**Response (Success):** A JSON object representing the updated stage.


### F. Delete a Stage (DELETE `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Deletes a pipeline stage.

**Response (Success):** A success message.


## III. Tracking Changes (Audit Logs)

Audit endpoints provide a history of changes to pipelines and stages.

### A. Pipeline Audit Log (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/audit`)

Retrieves the audit log for a pipeline.

**Response:** A JSON object with an array of audit entries, listed in reverse chronological order. Each entry includes `action`, `timestamp`, `message`, and `rawObject` (the data before/after the change).


### B. Stage Audit Log (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}/audit`)

Retrieves the audit log for a specific stage.

**Response:** Similar to the pipeline audit log.


**Example Audit Log Response (Partial):**

```json
{
  "results": [
    {
      "portalId": 123456,
      "identifier": "123456:11348541",
      "action": "UPDATE",
      "timestamp": "2024-10-07T20:58:57.414Z",
      "message": "Pipeline update",
      "rawObject": "{...}" ,
      "fromUserId": 9586504
    },
    // ... more audit entries
  ]
}
```


Remember to replace `YOUR_API_KEY` with your actual HubSpot API key.  All endpoints are under the `/crm/v3` namespace.  Error responses will typically include a `status`, `message`, and other relevant details.
