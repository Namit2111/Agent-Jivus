# HubSpot CRM API: Pipelines

This document details the HubSpot CRM API endpoints for managing pipelines and their stages. Pipelines track records through stages (e.g., sales, service).  The available objects for pipelines include Deals, Tickets, Appointments, Courses, Listings, Orders, Services, Leads (Sales Hub Professional and Enterprise only), and Custom objects (Enterprise only).


## API Endpoints

All endpoints are prefixed with `/crm/v3/pipelines/`.  Replace `{objectType}` with the appropriate object type (e.g., `deals`, `tickets`).  Replace `{pipelineId}` and `{stageId}` with the respective IDs.

### Pipelines

#### Create a Pipeline (POST `/crm/v3/pipelines/{objectType}`)

Creates a new pipeline.

**Request Body:**

```json
{
  "displayOrder": 3, // Order in the list of pipelines.  Same numbers are ordered alphabetically by label.
  "label": "New deal pipeline", // Display name of the pipeline
  "stages": [
    {
      "label": "In Progress",
      "metadata": {
        "probability": "0.2" // Required for deals; 0.0 = Closed Lost, 1.0 = Closed Won.  For tickets: ticketState (OPEN/CLOSED).
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

**Response (200 OK):**  A JSON representation of the created pipeline, including its ID.

**Note:**  Appointment, course, listing, lead, order, and service pipelines can have up to 30 stages. Deal, ticket, and custom object pipelines can have up to 100 stages.


#### Replace a Pipeline (PUT `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Replaces an existing pipeline with the provided data.  The entire pipeline definition is overwritten.

**Request Body:** Same as creating a new pipeline.

**Response (200 OK):** A JSON representation of the updated pipeline.


#### Retrieve Pipelines (GET `/crm/v3/pipelines/{objectType}`)

Retrieves all pipelines for a given object type.

**Response (200 OK):** An array of JSON objects, each representing a pipeline with `id`, `label`, `displayOrder`, and timestamp information.


#### Retrieve a Pipeline (GET `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Retrieves a specific pipeline.

**Response (200 OK):** A JSON object representing the pipeline.


#### Update a Pipeline (PATCH `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Updates specific properties of a pipeline (e.g., label, displayOrder).  Does *not* update stages.

**Request Body:**  A JSON object containing only the properties to be updated.

**Response (200 OK):**  A JSON representation of the updated pipeline.


#### Delete a Pipeline (DELETE `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Deletes a pipeline.

**Query Parameter:** `validateReferencesBeforeDelete=true` (optional) - Checks for records in the pipeline. If true and records exist, returns a 404 error with details of the existing records.

**Response (204 No Content):** Successful deletion.
**Response (404 Bad Request):**  If `validateReferencesBeforeDelete=true` and records exist in the pipeline.  Example:

```json
{
  "status": "error",
  "message": "Stage IDs: [...] are being referenced by object IDs: [...]",
  "correlationId": "...",
  "context": { "stageIds": [...], "objectIds": [...] },
  "category": "VALIDATION_ERROR",
  "subCategory": "PipelineError.STAGE_ID_IN_USE"
}
```


### Pipeline Stages

#### Create a Stage (POST `/crm/v3/pipelines/{objectType}/{pipelineId}/stages`)

Creates a new stage within a pipeline.

**Request Body:**

```json
{
  "displayOrder": 4, // Order within the pipeline
  "label": "Contract signed", // Name of the stage
  "metadata": {
    "probability": "0.8" // Required for deals; For tickets: ticketState (OPEN/CLOSED)
  }
}
```

**Response (200 OK):** JSON representation of the created stage, including its ID.


#### Replace a Stage (PUT `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Replaces an existing stage.

**Request Body:** Same as creating a new stage.

**Response (200 OK):** JSON representation of the updated stage.


#### Retrieve Stages (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/stages`)

Retrieves all stages of a pipeline.

**Response (200 OK):** An array of JSON objects representing stages.


#### Retrieve a Stage (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Retrieves a specific stage.

**Response (200 OK):** A JSON object representing the stage.


#### Update a Stage (PATCH `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Updates properties of a stage.

**Request Body:** A JSON object containing only the properties to be updated.

**Response (200 OK):** JSON representation of the updated stage.


#### Delete a Stage (DELETE `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Deletes a stage.

**Response (204 No Content):** Successful deletion.


### Audit Logs

#### Pipeline Audit Log (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/audit`)

Retrieves the audit log for a pipeline.

**Response (200 OK):** An array of audit log entries, listed in reverse chronological order, including `action`, `timestamp`, `message`, and `rawObject` (the change details).


#### Stage Audit Log (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}/audit`)

Retrieves the audit log for a specific stage.

**Response (200 OK):** Similar to pipeline audit log.


## Example: Creating a Deal Pipeline

This example uses curl to create a new deal pipeline.  Remember to replace `YOUR_API_KEY` with your actual HubSpot API key and adapt the URL accordingly.

```bash
curl -X POST \
  https://api.hubapi.com/crm/v3/pipelines/deals \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -d '{
  "displayOrder": 3,
  "label": "My New Deal Pipeline",
  "stages": [
    {
      "label": "Prospecting",
      "metadata": { "probability": "0.1" },
      "displayOrder": 0
    },
    {
      "label": "Proposal",
      "metadata": { "probability": "0.5" },
      "displayOrder": 1
    },
    {
      "label": "Closed Won",
      "metadata": { "probability": "1.0" },
      "displayOrder": 2
    },
    {
      "label": "Closed Lost",
      "metadata": { "probability": "0.0" },
      "displayOrder": 3
    }
  ]
}'
```


This documentation provides a comprehensive overview of the HubSpot CRM API for managing pipelines and stages.  Refer to the official HubSpot API documentation for the most up-to-date information and details.
