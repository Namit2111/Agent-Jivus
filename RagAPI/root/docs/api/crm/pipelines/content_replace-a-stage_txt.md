# HubSpot CRM API: Pipelines

This document details the HubSpot CRM API endpoints for managing pipelines and their stages.  Pipelines track records through stages (e.g., sales pipelines track deals, service pipelines track tickets).  The available objects for pipelines depend on your HubSpot subscription.

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


## API Endpoints

All endpoints use the `/crm/v3/pipelines` base path.  Replace `{objectType}` with the appropriate object type (e.g., `deals`, `tickets`), and `{pipelineId}` and `{stageId}` with their respective IDs.

### Pipelines

#### Create a Pipeline (POST `/crm/v3/pipelines/{objectType}`)

Creates a new pipeline.

**Request Body:**

```json
{
  "displayOrder": 3,  // Order in the display list (lower number is higher). Pipelines with the same displayOrder are ordered alphabetically.
  "label": "New deal pipeline", // Pipeline name
  "stages": [
    {
      "label": "In Progress",
      "metadata": {
        "probability": "0.2" // Required for deals; 0.0-1.0,  0.0 = Closed Lost, 1.0 = Closed Won. For tickets, use 'ticketState' ('OPEN' or 'CLOSED')
      },
      "displayOrder": 0 // Order within the pipeline
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

**Response (201 Created):**  Returns the created pipeline object with its ID.

#### Replace a Pipeline (PUT `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Replaces an existing pipeline.  The request body uses the same format as creating a new pipeline.

#### Retrieve Pipelines (GET `/crm/v3/pipelines/{objectType}`)

Retrieves all pipelines for a given object type.

**Response:** Returns an array of pipeline objects, each containing `id`, `label`, `displayOrder`, and timestamps.

#### Retrieve a Pipeline (GET `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Retrieves a single pipeline by ID.

#### Update a Pipeline (PATCH `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Updates a pipeline's properties (e.g., `label`, `displayOrder`).  Only send the fields you want to update.

#### Delete a Pipeline (DELETE `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Deletes a pipeline.  Include `validateReferencesBeforeDelete=true` to check for associated records.

**Response (404 Bad Request if records exist):**

```json
{
  "status": "error",
  "message": "Stage IDs: [...] are being referenced by object IDs: [...]",
  // ... other error details
}
```


### Pipeline Stages

#### Create a Stage (POST `/crm/v3/pipelines/{objectType}/{pipelineId}/stages`)

Creates a new stage within a pipeline.

**Request Body:**  Similar to creating a pipeline, but omits the `displayOrder` at the pipeline level.

```json
{
  "displayOrder": 4, // Order within the pipeline
  "label": "Contract signed",
  "metadata": {
    "probability": "0.8" // Required for deals; for tickets, use 'ticketState'
  }
}
```

#### Replace a Stage (PUT `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Replaces an existing stage.

#### Retrieve Stages (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/stages`)

Retrieves all stages for a given pipeline.

#### Retrieve a Stage (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Retrieves a single stage by ID.

#### Update a Stage (PATCH `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Updates a stage's properties.

#### Delete a Stage (DELETE `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Deletes a stage.

### Audit Logs (GET)

#### Pipeline Audit Log (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/audit`)

Retrieves audit logs for a specific pipeline.  Logs are in reverse chronological order.

#### Stage Audit Log (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}/audit`)

Retrieves audit logs for a specific pipeline stage.


**Note:**  All requests require authentication using your HubSpot API key.  Refer to the HubSpot API documentation for details on authentication and rate limits.  The maximum number of stages allowed per pipeline varies by object type.
