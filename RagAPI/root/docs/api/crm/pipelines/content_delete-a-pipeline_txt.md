# HubSpot CRM API: Pipelines

This document describes the HubSpot CRM API endpoints for managing pipelines and their stages. Pipelines track records through stages (e.g., sales, service).  The available object types vary based on your HubSpot subscription.

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

All endpoints below use the base URL `/crm/v3/pipelines/{objectType}` where `{objectType}` is one of the objects listed above (e.g., `deals`, `tickets`).  `{pipelineId}` and `{stageId}` represent the respective IDs.


### 1. Create a Pipeline (POST)

**Endpoint:** `/crm/v3/pipelines/{objectType}`

**Request Body:**

```json
{
  "displayOrder": 3, // Integer, determines display order.  Same numbers are ordered alphabetically by label.
  "label": "New deal pipeline", // String, pipeline name
  "stages": [ // Array of stage objects
    {
      "label": "In Progress",
      "metadata": {
        "probability": "0.2" // Required for deals (0.0-1.0), optional for others.  For tickets, use 'ticketState': 'OPEN' or 'CLOSED'.
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
  https://api.hubapi.com/crm/v3/pipelines/deals \
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

**Response:** (Success -  will vary based on HubSpot's response structure)  A successful response will include the newly created pipeline's details including its ID.

**Stage Limits:** Appointment, course, listing, lead, order, and service pipelines: up to 30 stages. Deal, ticket, and custom object pipelines: up to 100 stages.


### 2. Replace a Pipeline (PUT)

**Endpoint:** `/crm/v3/pipelines/{objectType}/{pipelineId}`

**Request Body:** Same as creating a pipeline.  This will completely overwrite the existing pipeline.


### 3. Retrieve Pipelines (GET)

**Endpoint:** `/crm/v3/pipelines/{objectType}`

**Response:** Returns a list of pipelines for the specified object type, including `id`, `label`, `displayOrder`, creation and update timestamps.


**Endpoint (Individual Pipeline):** `/crm/v3/pipelines/{objectType}/{pipelineId}`

**Response:** Returns details for a single pipeline.


### 4. Update a Pipeline (PATCH)

**Endpoint:** `/crm/v3/pipelines/{objectType}/{pipelineId}`

**Request Body:** Include only the properties you want to update (e.g., `label`, `displayOrder`).


### 5. Delete a Pipeline (DELETE)

**Endpoint:** `/crm/v3/pipelines/{objectType}/{pipelineId}`

**Query Parameter:** `validateReferencesBeforeDelete=true` (optional).  If `true`, the API checks for associated records. If records exist, it returns a 404 error with details of the records preventing deletion.

**Example 404 Error Response:**

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

These endpoints use the base URL `/crm/v3/pipelines/{objectType}/{pipelineId}/stages`.


### 1. Create a Stage (POST)

**Endpoint:** `/crm/v3/pipelines/{objectType}/{pipelineId}/stages`

**Request Body:**

```json
{
  "displayOrder": 4, // Integer, stage display order
  "label": "Contract signed", // String, stage name
  "metadata": {
    "probability": "0.8" // Required for deals (0.0-1.0), optional for others.  For tickets, use 'ticketState': 'OPEN' or 'CLOSED'.
  }
}
```

### 2. Replace a Stage (PUT)

**Endpoint:** `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`

**Request Body:** Same as creating a stage; this overwrites the existing stage.


### 3. Retrieve Stages (GET)

**Endpoint:** `/crm/v3/pipelines/{objectType}/{pipelineId}/stages`

**Response:** Returns a list of stages in the pipeline.

**Endpoint (Individual Stage):** `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`

**Response:** Returns details for a single stage.


### 4. Update a Stage (PATCH)

**Endpoint:** `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`

**Request Body:**  Only the properties to update.


### 5. Delete a Stage (DELETE)

**Endpoint:** `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`


## Audit Endpoints

Track changes to pipelines and stages using audit endpoints.  These endpoints use the base URLs `/crm/v3/pipelines/{objectType}/{pipelineId}/audit` and `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}/audit`.  The responses provide a history of changes in reverse chronological order, including action type, timestamp, and user ID.  Example 200 response is included in the provided text.


This documentation provides a comprehensive overview of the HubSpot CRM API for pipeline management. Remember to replace placeholders like `{objectType}`, `{pipelineId}`, and `{stageId}` with actual values.  Refer to the HubSpot API documentation for authentication details and further specifics.
