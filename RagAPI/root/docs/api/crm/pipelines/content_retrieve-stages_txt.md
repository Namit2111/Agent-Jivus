# HubSpot CRM API Pipelines Documentation

This document details the HubSpot CRM API endpoints for managing pipelines and their stages.  Pipelines track records through stages (e.g., sales, service).  Subscription level affects the number of pipelines available per object.

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


## I. Pipeline Management

### A. Create a Pipeline

**API Call:** `POST /crm/v3/pipelines/{objectType}`

**Request Body:**

```json
{
  "displayOrder": 3,  // Pipeline display order (lower numbers appear first)
  "label": "New deal pipeline", // Pipeline name
  "stages": [
    {
      "label": "In Progress",
      "metadata": {
        "probability": "0.2" // Required for deals; 0.0 - Closed Lost, 1.0 - Closed Won.  For tickets, use "ticketState": "OPEN" or "CLOSED"
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

**Response:**  A successful response will include the newly created pipeline's ID and other details.

**Stage Limits:** Appointment, course, listing, lead, order, and service pipelines: up to 30 stages. Deal, ticket, and custom object pipelines: up to 100 stages.


### B. Replace a Pipeline

**API Call:** `PUT /crm/v3/pipelines/{objectType}/{pipelineId}`

**Request Body:**  Same as creating a new pipeline. This request overwrites the existing pipeline.

### C. Retrieve Pipelines

**API Call (All pipelines):** `GET /crm/v3/pipelines/{objectType}`

**API Call (Single pipeline):** `GET /crm/v3/pipelines/{objectType}/{pipelineId}`

**Response:** Returns pipeline details (ID, label, displayOrder, creation/update timestamps).


### D. Update a Pipeline

**API Call:** `PATCH /crm/v3/pipelines/{objectType}/{pipelineId}`

**Request Body:** Include only the properties to update (e.g., `label`, `displayOrder`).  Use stage endpoints to modify stages.


### E. Delete a Pipeline

**API Call:** `DELETE /crm/v3/pipelines/{objectType}/{pipelineId}`

**Query Parameter:** `validateReferencesBeforeDelete=true` (optional) - Checks for existing records in the pipeline. If records exist, the request will fail with a 404 error indicating the referenced records.

**Error Response (Example):**

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
  "displayOrder": 4, // Stage display order within the pipeline
  "label": "Contract signed", // Stage name (must be unique within the pipeline)
  "metadata": {
    "probability": "0.8" // Required for deals; For tickets, use "ticketState": "OPEN" or "CLOSED"
  }
}
```

### B. Replace a Stage

**API Call:** `PUT /crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`

**Request Body:** Same as creating a new stage. This request overwrites the existing stage.

### C. Retrieve Stages

**API Call (All stages):** `GET /crm/v3/pipelines/{objectType}/{pipelineId}/stages`

**API Call (Single stage):** `GET /crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`

**Response:** Returns stage details (ID, label, displayOrder, creation/update timestamps).


### D. Update a Stage

**API Call:** `PATCH /crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`

**Request Body:** Include only the properties to update (e.g., `label`, `displayOrder`, `metadata`).


### E. Delete a Stage

**API Call:** `DELETE /crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`



## III. Audit Logging

Track changes to pipelines and stages using audit endpoints:

**API Call (Pipeline audit):** `GET /crm/v3/pipelines/{objectType}/{pipelineId}/audit`

**API Call (Stage audit):** `GET /crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}/audit`

**Response:** Returns a list of changes in reverse chronological order, including action type, timestamp, user ID, and the `rawObject` representing the state change.


**Example Audit Response (Pipeline):**  (A large example is already present in the original text; this is omitted for brevity)  The response shows a list of objects, each detailing a specific change (CREATE, UPDATE) with a timestamp and the `rawObject` showing the pipeline state before and after the change.


This documentation provides a comprehensive overview of the HubSpot CRM API for pipeline and stage management. Remember to replace `{objectType}`, `{pipelineId}`, and `{stageId}` with the appropriate values.  Always refer to the official HubSpot API documentation for the most up-to-date information and details.
