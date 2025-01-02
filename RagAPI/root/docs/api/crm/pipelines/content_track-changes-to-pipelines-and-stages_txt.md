# HubSpot CRM API: Pipelines

This document details the HubSpot CRM API endpoints for managing pipelines and their stages. Pipelines track records through various stages (e.g., sales, service).  Subscription level impacts the number of pipelines available per object.

## Supported Objects

Pipelines are available for:

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

All endpoints use the base URL `/crm/v3/pipelines/{objectType}` where `{objectType}` represents the object type (e.g., `deals`, `tickets`).

### 1. Create a Pipeline (POST)

**Endpoint:** `/crm/v3/pipelines/{objectType}`

**Request Body:**

```json
{
  "displayOrder": 3,  // Pipeline display order (numeric)
  "label": "New deal pipeline", // Pipeline name
  "stages": [
    {
      "label": "In Progress",
      "metadata": {
        "probability": "0.2" // Required for deals (0.0-1.0), optional for others.  For tickets, use 'ticketState': 'OPEN' or 'CLOSED'
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

**Response (Success):**  A JSON object representing the newly created pipeline, including its `id`.

**Note:**  Appointment, course, listing, lead, order, and service pipelines can have up to 30 stages. Deal, ticket, and custom object pipelines can have up to 100 stages.


### 2. Replace a Pipeline (PUT)

**Endpoint:** `/crm/v3/pipelines/{objectType}/{pipelineId}`

**Request Body:** Same as creating a new pipeline.  This overwrites the existing pipeline.

### 3. Retrieve Pipelines (GET)

**Endpoint:** `/crm/v3/pipelines/{objectType}` (all pipelines) or `/crm/v3/pipelines/{objectType}/{pipelineId}` (single pipeline)

**Response:** A JSON array (for all pipelines) or object (for a single pipeline) containing `id`, `label`, `displayOrder`, and timestamps.


### 4. Update a Pipeline (PATCH)

**Endpoint:** `/crm/v3/pipelines/{objectType}/{pipelineId}`

**Request Body:**  A JSON object containing only the fields to update (e.g., `label`, `displayOrder`).


### 5. Delete a Pipeline (DELETE)

**Endpoint:** `/crm/v3/pipelines/{objectType}/{pipelineId}`

**Query Parameter:** `validateReferencesBeforeDelete=true` (optional, but recommended to check for existing records before deletion).

**Response (Success):**  A success message.

**Response (Failure - Records Exist):**

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

All endpoints use the base URL `/crm/v3/pipelines/{objectType}/{pipelineId}/stages` where `{pipelineId}` is the ID of the pipeline.

### 1. Create a Stage (POST)

**Endpoint:** `/crm/v3/pipelines/{objectType}/{pipelineId}/stages`

**Request Body:**

```json
{
  "displayOrder": 4,
  "label": "Contract signed",
  "metadata": {
    "probability": "0.8" // Required for deals (0.0-1.0), optional for others. For tickets use 'ticketState': 'OPEN' or 'CLOSED'
  }
}
```

### 2. Replace a Stage (PUT)

**Endpoint:** `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`

**Request Body:** Same as creating a new stage. This overwrites the existing stage.


### 3. Retrieve Stages (GET)

**Endpoint:** `/crm/v3/pipelines/{objectType}/{pipelineId}/stages` (all stages) or `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}` (single stage).

**Response:**  A JSON array (for all stages) or object (for a single stage) containing `id`, `label`, `displayOrder`, and timestamps.

### 4. Update a Stage (PATCH)

**Endpoint:** `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`

**Request Body:** A JSON object containing only the fields to update.


### 5. Delete a Stage (DELETE)

**Endpoint:** `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`


## Audit Endpoints

To track changes to pipelines and stages:

* **Pipelines:** `/crm/v3/pipelines/{objectType}/{pipelineId}/audit` (GET)
* **Stages:** `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}/audit` (GET)

**Response:** A JSON object with a list of updates in reverse chronological order, including `action`, `timestamp`, `message`, and `rawObject` (the changed data).  Example response shown in the original text.


This comprehensive documentation provides a complete overview of the HubSpot CRM API endpoints for pipeline management, including detailed request and response examples. Remember to replace placeholders like `{objectType}`, `{pipelineId}`, and `{stageId}` with actual values.  Always refer to the official HubSpot API documentation for the most up-to-date information and authentication details.
