# HubSpot CRM API Pipelines Documentation

This document details the HubSpot CRM API endpoints for managing pipelines and their stages. Pipelines track records through various stages; examples include sales pipelines (predicting revenue) and service pipelines (managing ticket statuses).  The availability of multiple pipelines per object depends on your HubSpot subscription.

**Supported Objects:**

* Deals
* Tickets
* Appointments
* Courses
* Listings
* Orders
* Services
* Leads (Sales Hub Professional and Enterprise only)
* Custom objects (Enterprise only)


## I. Pipeline Management

### A. Create a Pipeline

**API Call:** `POST /crm/v3/pipelines/{objectType}`

**Request Body:**

```json
{
  "displayOrder": 3,  // Order in the display (lower numbers appear first, ties broken alphabetically by label)
  "label": "New deal pipeline", // Pipeline name displayed in HubSpot
  "stages": [
    {
      "label": "In Progress",
      "metadata": {
        "probability": "0.2" // Required for deals, 0.0-1.0 (0.0 = Closed Lost, 1.0 = Closed Won).  For tickets: ticketState (OPEN or CLOSED)
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

```json
POST /crm/v3/pipelines/deals
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


### B. Replace a Pipeline

**API Call:** `PUT /crm/v3/pipelines/{objectType}/{pipelineId}`

**Request Body:** Same as creating a new pipeline. This request overwrites the existing pipeline with the provided data.


### C. Retrieve Pipelines

**API Call (All Pipelines):** `GET /crm/v3/pipelines/{objectType}`

**Response:** Returns a list of pipelines, each containing `id`, `label`, `displayOrder`, and creation/update timestamps.

**API Call (Single Pipeline):** `GET /crm/v3/pipelines/{objectType}/{pipelineId}`

**Response:** Returns details of a single pipeline.


### D. Update a Pipeline

**API Call:** `PATCH /crm/v3/pipelines/{objectType}/{pipelineId}`

**Request Body:** Include only the properties you want to update (e.g., `label`, `displayOrder`).  Use stage endpoints to modify stages.


### E. Delete a Pipeline

**API Call:** `DELETE /crm/v3/pipelines/{objectType}/{pipelineId}`

**Parameter:** `validateReferencesBeforeDelete=true` (optional).  If included and records exist in the pipeline, a 404 error with details will be returned.

**Error Response Example:**

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


## II. Pipeline Stage Management

### A. Create a Stage

**API Call:** `POST /crm/v3/pipelines/{objectType}/{pipelineId}/stages`

**Request Body:**

```json
{
  "displayOrder": 4,
  "label": "Contract signed",
  "metadata": {
    "probability": "0.8" // Required for deals; For tickets: ticketState (OPEN or CLOSED)
  }
}
```


### B. Replace a Stage

**API Call:** `PUT /crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`

**Request Body:** Same as creating a new stage. This overwrites the existing stage.


### C. Retrieve Stages

**API Call (All Stages):** `GET /crm/v3/pipelines/{objectType}/{pipelineId}/stages`

**Response:** Returns a list of stages, each with `id`, `label`, `displayOrder`, and timestamps.

**API Call (Single Stage):** `GET /crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`

**Response:** Returns details of a single stage.


### D. Update a Stage

**API Call:** `PATCH /crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`

**Request Body:** Include only the properties to update.


### E. Delete a Stage

**API Call:** `DELETE /crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`


## III. Auditing Pipeline Changes

**API Call (Pipeline Audit):** `GET /crm/v3/pipelines/{objectType}/{pipelineId}/audit`

**API Call (Stage Audit):** `GET /crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}/audit`

**Response:**  Returns a list of updates in reverse chronological order, including `action`, `timestamp`, `message`, and `rawObject` (the changed data).

**Example Audit Response (Pipeline):**  (A large example is provided in the original text, omitted here for brevity.  It shows a series of UPDATE and CREATE actions with detailed timestamps and changed data.)


This documentation provides a comprehensive overview of the HubSpot CRM API for pipeline management.  Remember to replace placeholders like `{objectType}`, `{pipelineId}`, and `{stageId}` with the actual values.  Refer to the HubSpot API documentation for detailed error handling and authentication information.
