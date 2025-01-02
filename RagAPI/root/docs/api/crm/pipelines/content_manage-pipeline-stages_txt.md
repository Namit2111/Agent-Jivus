# HubSpot CRM API: Pipelines

This document details the HubSpot CRM API endpoints for managing pipelines and their stages.  Pipelines track records through stages (e.g., sales, service).  The availability of multiple pipelines per object depends on your HubSpot subscription.

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


## Managing Pipelines

### Create a Pipeline (POST `/crm/v3/pipelines/{objectType}`)

Creates a new pipeline for a specified object type.

**Request Body:**

```json
{
  "displayOrder": 3,  // Numerical order for display (lower number = higher priority)
  "label": "New deal pipeline", // Pipeline name
  "stages": [
    {
      "label": "In Progress",
      "metadata": {
        "probability": "0.2" // Required for deals; 0.0-1.0, where 0.0 is Closed Lost and 1.0 is Closed Won.  For tickets, use "ticketState": "OPEN" or "CLOSED".
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

**Example (Deals):**

```json
{
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
}
```

**Stage Limits:**

* Appointment, course, listing, lead, order, and service pipelines: Up to 30 stages.
* Deal, ticket, and custom object pipelines: Up to 100 stages.


### Replace a Pipeline (PUT `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Replaces an existing pipeline.  Use the `pipelineId` to specify the pipeline to replace. The request body uses the same structure as creating a new pipeline.


### Retrieve Pipelines (GET `/crm/v3/pipelines/{objectType}`)

Retrieves all pipelines for a given object type.

**Response:** Returns an array of pipelines, each with `id`, `label`, `displayOrder`, creation and update timestamps.


### Retrieve a Pipeline (GET `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Retrieves a specific pipeline by its `pipelineId`.


### Update a Pipeline (PATCH `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Updates properties of an existing pipeline (e.g., `label`, `displayOrder`).  Use the request body to specify the fields to update.  To update stages, use the stage endpoints.


### Delete a Pipeline (DELETE `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Deletes a pipeline.  Include `validateReferencesBeforeDelete=true` to check for existing records in the pipeline before deletion.  If records exist, a 404 error with details will be returned.

**Example 404 Response:**

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


## Managing Pipeline Stages

### Create a Stage (POST `/crm/v3/pipelines/{objectType}/{pipelineId}/stages`)

Adds a new stage to a pipeline.

**Request Body:**

```json
{
  "displayOrder": 4, // Order within the pipeline
  "label": "Contract signed", // Stage name
  "metadata": {
    "probability": "0.8" // Required for deals; For tickets, use "ticketState": "OPEN" or "CLOSED"
  }
}
```

### Replace a Stage (PUT `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Replaces an existing stage. Use `stageId` to identify the stage. The request body is the same as creating a new stage.


### Retrieve Stages (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/stages`)

Retrieves all stages for a specified pipeline.


### Retrieve a Stage (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Retrieves a specific stage by its `stageId`.


### Update a Stage (PATCH `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Updates properties of an existing stage.


### Delete a Stage (DELETE `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Deletes a stage.


## Tracking Changes (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/audit` or `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}/audit`)

Use audit endpoints to track changes to pipelines and stages.  Responses list updates in reverse chronological order with action type, timestamp, and user details.

**Example 200 Response (Pipeline Audit):**

(A large JSON response example is provided in the original text.  It's too extensive to reproduce here, but the structure includes an array of `results`, each with `portalId`, `identifier`, `action`, `timestamp`, `message`, `rawObject`, and `fromUserId`.)


This comprehensive documentation provides a detailed overview of the HubSpot CRM API's pipeline management capabilities.  Remember to replace placeholders like `{objectType}`, `{pipelineId}`, and `{stageId}` with the appropriate values.  Refer to the HubSpot API documentation for authentication details and further information.
