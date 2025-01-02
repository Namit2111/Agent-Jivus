# HubSpot CRM API: Pipelines

This document details the HubSpot CRM API endpoints for managing pipelines and their stages.  Pipelines track records through various stages (e.g., sales, service).  The available object types for pipelines are: Deals, Tickets, Appointments, Courses, Listings, Orders, Services, Leads (Sales Hub Professional and Enterprise only), and Custom objects (Enterprise only).

## API Endpoint Reference

All endpoints below are under the base URL `/crm/v3/pipelines`.  Replace `{objectType}` with the appropriate object type (e.g., `deals`, `tickets`), and `{pipelineId}` and `{stageId}` with their respective IDs.

### Pipelines

#### Create a Pipeline (POST `/crm/v3/pipelines/{objectType}`)

Creates a new pipeline.

**Request Body:**

```json
{
  "displayOrder": 3,  // Pipeline display order (numeric)
  "label": "New deal pipeline", // Pipeline name
  "stages": [
    {
      "label": "In Progress",
      "metadata": {
        "probability": "0.2" // Required for deals; 0.0-1.0, 0.0 = Closed Lost, 1.0 = Closed Won.  For tickets, use "ticketState": "OPEN" or "CLOSED"
      },
      "displayOrder": 0
    },
    // ... more stages
  ]
}
```

**Example Request (deals):**

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

**Response (200 OK):**  The created pipeline object, including its ID.

#### Replace a Pipeline (PUT `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Replaces an existing pipeline.  The request body is the same as for creating a pipeline.

#### Retrieve Pipelines (GET `/crm/v3/pipelines/{objectType}`)

Retrieves all pipelines for a given object type.

**Response (200 OK):** An array of pipeline objects, each containing `id`, `label`, `displayOrder`, creation and update timestamps.

#### Retrieve a Pipeline (GET `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Retrieves a single pipeline.


#### Update a Pipeline (PATCH `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Updates a pipeline's properties (e.g., `label`, `displayOrder`).  Only include the fields to be updated in the request body.  Use stage endpoints to update stages.


#### Delete a Pipeline (DELETE `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Deletes a pipeline.

**Query Parameter:**

* `validateReferencesBeforeDelete=true`: (Optional) Checks for existing records in the pipeline. If records exist, a 404 Bad Request is returned with details of the records preventing deletion.

**Example 404 Bad Request Response:**

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

### Pipeline Stages

#### Create a Stage (POST `/crm/v3/pipelines/{objectType}/{pipelineId}/stages`)

Creates a new stage within a pipeline.

**Request Body:**  Similar to stage creation within pipeline creation.  `pipelineId` is specified in the URL.

#### Replace a Stage (PUT `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Replaces an existing stage.

#### Retrieve Stages (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/stages`)

Retrieves all stages within a pipeline.

#### Retrieve a Stage (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Retrieves a single stage.

#### Update a Stage (PATCH `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Updates a stage's properties.

#### Delete a Stage (DELETE `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Deletes a stage.

### Auditing Changes

#### Pipeline Audit (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/audit`)

Retrieves the audit trail for a pipeline.

#### Stage Audit (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}/audit`)

Retrieves the audit trail for a specific stage.

**Response (200 OK for both):** An array of audit entries, each containing `portalId`, `identifier`, `action`, `timestamp`, `message`, `rawObject`, and `fromUserId`.  Entries are in reverse chronological order.


**Note:**  Remember to replace placeholders like `{objectType}`, `{pipelineId}`, and `{stageId}` with actual values.  Error handling and authentication (API keys) are not explicitly shown here but are crucial for successful API calls.  Refer to the HubSpot API documentation for details on authentication and error codes.
