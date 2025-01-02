# HubSpot CRM API Pipelines Documentation

This document details the HubSpot CRM API endpoints for managing pipelines and their stages. Pipelines track records through stages (e.g., sales pipelines track deals, service pipelines track tickets).  The availability of multiple pipelines per object depends on your HubSpot subscription.

## Supported Objects

Pipelines are available for the following objects:

* Deals
* Tickets
* Appointments
* Courses
* Listings
* Orders
* Services
* Leads (Sales Hub Professional and Enterprise only)
* Custom objects (Enterprise only)


## Pipelines Endpoints

All endpoints are under the base URL `/crm/v3/pipelines/{objectType}` where `{objectType}` represents the object type (e.g., `deals`, `tickets`).

### 1. Create a Pipeline (POST `/crm/v3/pipelines/{objectType}`)

Creates a new pipeline for a specified object type.

**Request Body:**

```json
{
  "displayOrder": 3,  // Order in the display list. Pipelines with the same order are sorted alphabetically.
  "label": "New deal pipeline", // Pipeline name displayed in HubSpot.
  "stages": [
    {
      "label": "In Progress",
      "metadata": {
        "probability": "0.2" // Required for deals; 0.0-1.0, 0.0=Closed Lost, 1.0=Closed Won.  For tickets: ticketState (OPEN/CLOSED)
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
    // ... more stages
  ]
}
```

**Example Request (Deals):**

```bash
curl -X POST \
  'https://api.hubapi.com/crm/v3/pipelines/deals' \
  -H 'Content-Type: application/json' \
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
      // ... more stages
    ]
  }' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

**Response (Success):**  A JSON representation of the created pipeline, including its ID.


### 2. Replace a Pipeline (PUT `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Replaces an existing pipeline with the data provided in the request body.

**Request Body:**  Same as creating a new pipeline.

**Response (Success):** A JSON representation of the updated pipeline.


### 3. Retrieve Pipelines (GET `/crm/v3/pipelines/{objectType}`)

Retrieves all pipelines for a given object type.

**Response:** A JSON array of pipelines, each containing `id`, `label`, `displayOrder`, creation and update timestamps.


### 4. Retrieve a Pipeline (GET `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Retrieves a single pipeline by its ID.

**Response:** A JSON representation of the pipeline.


### 5. Update a Pipeline (PATCH `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Updates specific properties of a pipeline (e.g., `label`, `displayOrder`).  Does *not* update stages. Use stage endpoints for that.

**Request Body:** JSON object containing only the properties to update.

**Response (Success):** A JSON representation of the updated pipeline.


### 6. Delete a Pipeline (DELETE `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Deletes a pipeline.

**Query Parameter:** `validateReferencesBeforeDelete=true` (optional) - Checks for records in the pipeline before deletion.  If `true` and records exist, a 404 error with details will be returned.

**Response (Success):**  Empty body or a success message.

**Response (Error - Records Exist):**

```json
{
  "status": "error",
  "message": "Stage IDs: [...] are being referenced by object IDs: [...]",
  "correlationId": "...",
  "context": { ... },
  "category": "VALIDATION_ERROR",
  "subCategory": "PipelineError.STAGE_ID_IN_USE"
}
```


## Pipeline Stages Endpoints

All endpoints are under the base URL `/crm/v3/pipelines/{objectType}/{pipelineId}/stages`


### 1. Create a Stage (POST `/crm/v3/pipelines/{objectType}/{pipelineId}/stages`)

Adds a new stage to a pipeline.

**Request Body:**

```json
{
  "displayOrder": 4, // Order within the pipeline. Stages with the same order are sorted alphabetically.
  "label": "Contract signed", // Stage name. Must be unique within the pipeline.
  "metadata": {
    "probability": "0.8" // Required for deals; 0.0-1.0. For tickets: ticketState (OPEN/CLOSED).
  }
}
```

**Response (Success):**  A JSON representation of the created stage, including its ID.


### 2. Replace a Stage (PUT `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Replaces an existing stage with the data provided in the request body.

**Request Body:** Same as creating a new stage.

**Response (Success):** A JSON representation of the updated stage.


### 3. Retrieve Stages (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/stages`)

Retrieves all stages for a given pipeline.

**Response:** A JSON array of stages, each containing `id`, `label`, `displayOrder`, creation and update timestamps.


### 4. Retrieve a Stage (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Retrieves a single stage by its ID.

**Response:** A JSON representation of the stage.


### 5. Update a Stage (PATCH `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Updates specific properties of a stage (e.g., `label`, `displayOrder`).

**Request Body:** JSON object containing only the properties to update.

**Response (Success):** A JSON representation of the updated stage.


### 6. Delete a Stage (DELETE `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Deletes a pipeline stage.

**Response (Success):** Empty body or a success message.


## Audit Endpoints

Track changes to pipelines and stages using audit endpoints:

* **Pipeline Audit (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/audit`):**  Returns a list of changes to the pipeline in reverse chronological order.
* **Stage Audit (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}/audit`):** Returns a list of changes to a specific stage.

**Response:** A JSON array of audit entries, each containing details about the action, timestamp, user, and the change itself (`rawObject`).


**Note:** Replace `{objectType}`, `{pipelineId}`, and `{stageId}` with the actual values.  Remember to include your HubSpot API key in the `Authorization` header of your requests.  The example responses provided show the structure; actual values will vary.
