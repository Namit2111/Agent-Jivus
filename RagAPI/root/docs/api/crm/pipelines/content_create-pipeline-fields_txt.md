# HubSpot CRM API: Pipelines

This document details the HubSpot CRM API endpoints for managing pipelines and their stages. Pipelines track records through stages; for example, sales pipelines predict revenue and identify roadblocks, while service pipelines manage ticket statuses.  Subscription level determines the number of pipelines available per object.


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

### 1. Create a Pipeline (POST)

**Endpoint:** `/crm/v3/pipelines/{objectType}`

**Request Body:**

```json
{
  "displayOrder": 3,  // Order of display among pipelines for the object.  Same order numbers are sorted alphabetically by label.
  "label": "New deal pipeline", // Pipeline name displayed in HubSpot.
  "stages": [
    {
      "label": "In Progress",
      "metadata": {
        "probability": "0.2" // Required for deals (0.0-1.0), optional for others.  For tickets, use 'ticketState' ('OPEN' or 'CLOSED').
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

**Stage Limits:** Appointment, course, listing, lead, order, and service pipelines: up to 30 stages. Deal, ticket, and custom object pipelines: up to 100 stages.


### 2. Replace a Pipeline (PUT)

**Endpoint:** `/crm/v3/pipelines/{objectType}/{pipelineId}`

**Request Body:** Same as creating a new pipeline.  Replaces the entire pipeline.


### 3. Retrieve Pipelines (GET)

**Endpoint:** `/crm/v3/pipelines/{objectType}`

**Response:** Returns all pipelines for the object, including `id`, `label`, `displayOrder`, creation and update timestamps.


**Endpoint:** `/crm/v3/pipelines/{objectType}/{pipelineId}`

**Response:** Returns a single pipeline.


### 4. Update a Pipeline (PATCH)

**Endpoint:** `/crm/v3/pipelines/{objectType}/{pipelineId}`

**Request Body:** Include only the properties to update (e.g., `label`, `displayOrder`).  Use stage endpoints to modify stages.


### 5. Delete a Pipeline (DELETE)

**Endpoint:** `/crm/v3/pipelines/{objectType}/{pipelineId}`

**Query Parameter:** `validateReferencesBeforeDelete=true` (optional).  If `true`, the API checks for records in the pipeline. If records exist, a 404 error with details of the referenced records is returned.

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

All endpoints are under the base URL `/crm/v3/pipelines/{objectType}/{pipelineId}/stages`.


### 1. Create a Stage (POST)

**Endpoint:** `/crm/v3/pipelines/{objectType}/{pipelineId}/stages`

**Request Body:**

```json
{
  "displayOrder": 4, // Order within the pipeline
  "label": "Contract signed", // Stage name
  "metadata": {
    "probability": "0.8" // Required for deals, optional for others. For tickets, use 'ticketState' ('OPEN' or 'CLOSED').
  }
}
```

### 2. Replace a Stage (PUT)

**Endpoint:** `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`

**Request Body:** Same as creating a new stage. Replaces the entire stage.


### 3. Retrieve Stages (GET)

**Endpoint:** `/crm/v3/pipelines/{objectType}/{pipelineId}/stages`

**Response:** Returns all stages in the pipeline, including `id`, `label`, `displayOrder`, creation and update timestamps.

**Endpoint:** `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`

**Response:** Returns a single stage.


### 4. Update a Stage (PATCH)

**Endpoint:** `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`

**Request Body:** Include only the properties to update (e.g., `label`, `displayOrder`).


### 5. Delete a Stage (DELETE)

**Endpoint:** `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`


## Audit Endpoints

Track changes to pipelines and stages using audit endpoints:

* **Pipeline Audit:** `/crm/v3/pipelines/{objectType}/{pipelineId}/audit` (GET)
* **Stage Audit:** `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}/audit` (GET)

**Response:** Returns a list of updates in reverse chronological order, including action type, timestamp, and user.  The `rawObject` field contains the complete object before the update.  Example response shown below.


**Example 200 Response (Pipeline Audit):**

```json
{
  "results": [
    {
      "portalId": 123456,
      "identifier": "123456:11348541",
      "action": "UPDATE",
      "timestamp": "2024-10-07T20:58:57.414Z",
      "message": "Pipeline update",
      "rawObject": "...", // Full JSON of pipeline object before the update.
      "fromUserId": 9586504
    },
    // ... more audit entries
  ]
}
```

This detailed documentation provides a comprehensive guide to the HubSpot CRM API for managing pipelines and their stages. Remember to replace placeholders like `{objectType}`, `{pipelineId}`, and `{stageId}` with actual values.
