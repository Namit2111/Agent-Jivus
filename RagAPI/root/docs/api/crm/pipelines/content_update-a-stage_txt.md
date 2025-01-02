# HubSpot CRM API: Pipelines

This document describes the HubSpot CRM API endpoints for managing pipelines and their stages. Pipelines track records through various stages (e.g., sales, service).  The available objects for pipelines include: Deals, Tickets, Appointments, Courses, Listings, Orders, Services, Leads (Sales Hub Professional and Enterprise only), and Custom objects (Enterprise only).

## API Endpoints

All endpoints below are prefixed with `/crm/v3/pipelines/`.  Replace `{objectType}` with the appropriate object type (e.g., `deals`, `tickets`).  Replace `{pipelineId}` and `{stageId}` with the respective IDs.

### Pipelines

#### Create a Pipeline (POST)

Endpoint: `{objectType}`

Request Body:

```json
{
  "displayOrder": 3,  // Pipeline display order (numeric)
  "label": "New deal pipeline", // Pipeline name
  "stages": [          // Array of stages
    {
      "label": "In Progress",
      "metadata": {
        "probability": "0.2" // Required for deals (0.0-1.0), optional for others
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

* **Note:**  `probability` in `metadata` is required for deal stages, ranging from 0.0 (Closed Lost) to 1.0 (Closed Won). For tickets, `ticketState` ("OPEN" or "CLOSED") can be included in `metadata`.  Maximum stages: 30 for appointment, course, listing, lead, order, and service; 100 for deal, ticket, and custom object.

Example Request (creating a deal pipeline):

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
      // ... more stages
    ]
  }'
```


#### Replace a Pipeline (PUT)

Endpoint: `{objectType}/{pipelineId}`

Request Body: Same as creating a pipeline.  This overwrites the existing pipeline.

#### Retrieve Pipelines (GET)

Endpoint: `{objectType}`

Response: Returns an array of pipelines with `id`, `label`, `displayOrder`, creation and update timestamps.

Endpoint: `{objectType}/{pipelineId}`

Response: Returns details of a single pipeline.


#### Update a Pipeline (PATCH)

Endpoint: `{objectType}/{pipelineId}`

Request Body:  Include only the properties to update (e.g., `label`, `displayOrder`).

#### Delete a Pipeline (DELETE)

Endpoint: `{objectType}/{pipelineId}`

Query Parameter: `validateReferencesBeforeDelete=true` (optional, but recommended). If `true`, returns an error if records exist in the pipeline.

Example Error Response (404 Bad Request):

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

#### Create a Stage (POST)

Endpoint: `{objectType}/{pipelineId}/stages`

Request Body:

```json
{
  "displayOrder": 4,
  "label": "Contract signed",
  "metadata": {
    "probability": "0.8" // Required for deals, optional for others
  }
}
```

#### Replace a Stage (PUT)

Endpoint: `{objectType}/{pipelineId}/stages/{stageId}`

Request Body: Same as creating a stage. This overwrites the existing stage.

#### Retrieve Stages (GET)

Endpoint: `{objectType}/{pipelineId}/stages`

Response: Returns an array of stages with `id`, `label`, `displayOrder`, creation and update timestamps.

Endpoint: `{objectType}/{pipelineId}/stages/{stageId}`

Response: Returns details of a single stage.

#### Update a Stage (PATCH)

Endpoint: `{objectType}/{pipelineId}/stages/{stageId}`

Request Body: Include only the properties to update (e.g., `label`, `displayOrder`).

#### Delete a Stage (DELETE)

Endpoint: `{objectType}/{pipelineId}/stages/{stageId}`


### Audit Logs (GET)

#### Pipeline Audit Log

Endpoint: `{objectType}/{pipelineId}/audit`

Response:  Returns a list of changes made to the pipeline, in reverse chronological order.  Each entry includes `action` (CREATE, UPDATE, DELETE), `timestamp`, `message`, and `rawObject` (the complete object before the change).

#### Stage Audit Log

Endpoint: `{objectType}/{pipelineId}/stages/{stageId}/audit`

Response: Similar to pipeline audit log, but for changes to a specific stage.


## Authentication

To use the HubSpot CRM API, you'll need a HubSpot API key.  Include this key in the `hapikey` query parameter in your API requests.  See HubSpot's documentation for details on obtaining an API key and authentication methods.


This markdown documentation provides a concise overview of the HubSpot CRM API for pipelines. Refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications.
