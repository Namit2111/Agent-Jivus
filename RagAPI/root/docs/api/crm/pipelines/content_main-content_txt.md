# HubSpot CRM API: Pipelines

This document describes the HubSpot CRM API endpoints for managing pipelines and their stages.  Pipelines track records through stages (e.g., sales pipelines track deals, service pipelines track tickets).  The availability of pipelines depends on your HubSpot subscription.

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

Creates a new pipeline. Requires a `POST` request.

**Request Body:**

```json
{
  "displayOrder": 3,  // Integer, determines display order. Pipelines with the same order are sorted alphabetically by label.
  "label": "New deal pipeline", // String, the pipeline's name.
  "stages": [
    {
      "label": "In Progress",
      "metadata": {
        "probability": "0.2" // Required for deals (0.0-1.0), optional for other objects.  For tickets, use "ticketState": "OPEN" or "CLOSED".
      },
      "displayOrder": 0 // Integer, determines display order within the pipeline.
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

**Response (200 OK):**  A JSON object representing the newly created pipeline, including its ID.


### 2. Replace a Pipeline (PUT `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Replaces an existing pipeline.  Uses a `PUT` request.  `{pipelineId}` is the ID of the pipeline to replace.

**Request Body:** Same as creating a new pipeline.

**Response (200 OK):** A JSON object representing the updated pipeline.


### 3. Retrieve Pipelines (GET `/crm/v3/pipelines/{objectType}`)

Retrieves all pipelines for a given object type. Uses a `GET` request.

**Response (200 OK):** A JSON object containing an array of pipelines. Each pipeline includes `id`, `label`, `displayOrder`, and timestamps.


### 4. Retrieve a Pipeline (GET `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Retrieves a specific pipeline. Uses a `GET` request.

**Response (200 OK):** A JSON object representing the pipeline.


### 5. Update a Pipeline (PATCH `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Updates a pipeline's details (label, display order). Uses a `PATCH` request.

**Request Body:**  An object containing only the properties to update.

**Response (200 OK):** A JSON object representing the updated pipeline.


### 6. Delete a Pipeline (DELETE `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Deletes a pipeline. Uses a `DELETE` request.

**Query Parameter:** `validateReferencesBeforeDelete=true` (optional) - Checks for records in the pipeline before deletion. If records exist, returns a 404 error with details.

**Response (204 No Content) / (404 Bad Request - if `validateReferencesBeforeDelete=true` and records exist):**

**404 Bad Request Example:**

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


## Pipeline Stages Endpoints

All endpoints are under the base URL `/crm/v3/pipelines/{objectType}/{pipelineId}/stages`


### 1. Create a Stage (POST `/crm/v3/pipelines/{objectType}/{pipelineId}/stages`)

Creates a new stage in a pipeline. Uses a `POST` request.

**Request Body:**

```json
{
  "displayOrder": 4, // Integer, determines the display order within the pipeline.
  "label": "Contract signed", // String, the stage's name. Must be unique within the pipeline.
  "metadata": {
    "probability": "0.8" // Required for deals (0.0-1.0), optional for other objects. For tickets, use "ticketState": "OPEN" or "CLOSED".
  }
}
```

**Response (200 OK):** A JSON object representing the newly created stage.


### 2. Replace a Stage (PUT `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Replaces an existing stage. Uses a `PUT` request. `{stageId}` is the ID of the stage to replace.

**Request Body:** Same as creating a new stage.


### 3. Retrieve Stages (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/stages`)

Retrieves all stages in a pipeline. Uses a `GET` request.


### 4. Retrieve a Stage (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Retrieves a specific stage. Uses a `GET` request.


### 5. Update a Stage (PATCH `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Updates a stage's details. Uses a `PATCH` request.


### 6. Delete a Stage (DELETE `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Deletes a stage. Uses a `DELETE` request.


## Audit Endpoints

Track changes to pipelines and stages using the audit endpoints:

* **Pipeline Audit (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/audit`):** Retrieves a list of changes made to a pipeline.
* **Stage Audit (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}/audit`):** Retrieves a list of changes made to a stage.

**Response (200 OK):** A JSON object containing an array of audit records.  Each record includes `action`, `timestamp`, `message`, and `rawObject` (the object before the change).


## Stage and Pipeline Limits

* Appointment, course, listing, lead, order, and service pipelines: Up to 30 stages.
* Deal, ticket, and custom object pipelines: Up to 100 stages.


This documentation provides a comprehensive overview of the HubSpot CRM API for managing pipelines and stages.  Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
