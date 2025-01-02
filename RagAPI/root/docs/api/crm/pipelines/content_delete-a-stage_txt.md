# HubSpot CRM API Pipelines Documentation

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


## Managing Pipelines

### Create a Pipeline (POST `/crm/v3/pipelines/{objectType}`)

Creates a new pipeline for the specified `objectType`.

**Request Body:**

```json
{
  "displayOrder": 3, // Integer representing display order. Pipelines with the same order are listed alphabetically.
  "label": "New deal pipeline", // String: Pipeline name as displayed in HubSpot.
  "stages": [
    {
      "label": "In Progress", // String: Stage name (must be unique within the pipeline).
      "metadata": {
        "probability": "0.2" // Required for deals (0.0 - 1.0), optional for others.  For tickets, use "ticketState": "OPEN" or "CLOSED".
      },
      "displayOrder": 0 // Integer: Stage display order within the pipeline.
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
  -H 'Authorization: Bearer YOUR_API_KEY' \
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

**Response (201 Created):**  Returns the created pipeline's details including its ID.

**Stage Limits:** Appointment, course, listing, lead, order, and service pipelines can have up to 30 stages. Deal, ticket, and custom object pipelines can have up to 100 stages.


### Replace a Pipeline (PUT `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Replaces an existing pipeline.  Use the `pipelineId` to specify the pipeline to replace.  The request body uses the same structure as creating a new pipeline; it overwrites the existing data.

### Retrieve Pipelines (GET `/crm/v3/pipelines/{objectType}`)

Retrieves all pipelines for a given `objectType`.

**Response:** Returns an array of pipelines, each containing `id`, `label`, `displayOrder`, and creation/update timestamps.

### Retrieve a Pipeline (GET `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Retrieves a single pipeline by its `pipelineId`.

### Update a Pipeline (PATCH `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Updates a pipeline's properties (e.g., `label`, `displayOrder`).  Only specify the fields to update in the request body.  Use stage endpoints to update pipeline stages.

### Delete a Pipeline (DELETE `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Deletes a pipeline.

**`validateReferencesBeforeDelete` Parameter:**  Setting `validateReferencesBeforeDelete=true` checks for records in the pipeline. If records exist, the request returns a 404 error with details about the records preventing deletion.

**Example 404 Response (Bad Request):**

```json
{
  "status": "error",
  "message": "Stage IDs: [renter_viewing, renter_security_deposit_paid, renter_new_lead, renter_closed_won, renter_closed_lost] are being referenced by object IDs: [22901690010]",
  "correlationId": "1fb9ac01-f574-4919-bf55-2c8c25ac1507",
  "context": {
    "stageIds": ["[renter_viewing, renter_security_deposit_paid, renter_new_lead, renter_closed_won, renter_closed_lost]"],
    "objectIds": ["[22901690010]"]
  },
  "category": "VALIDATION_ERROR",
  "subCategory": "PipelineError.STAGE_ID_IN_USE"
}
```


## Managing Pipeline Stages

### Create a Stage (POST `/crm/v3/pipelines/{objectType}/{pipelineId}/stages`)

Adds a new stage to an existing pipeline.

**Request Body:**

```json
{
  "displayOrder": 4, // Integer: Stage display order within the pipeline.
  "label": "Contract signed", // String: Stage name (must be unique within the pipeline).
  "metadata": {
    "probability": "0.8" // Required for deals (0.0 - 1.0), optional for others. For tickets, use "ticketState": "OPEN" or "CLOSED".
  }
}
```

### Replace a Stage (PUT `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Replaces an existing stage. Use the `stageId` to specify the stage. The request body is the same as creating a new stage.


### Retrieve Stages (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/stages`)

Retrieves all stages for a given pipeline.

### Retrieve a Stage (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Retrieves a single stage by its `stageId`.

### Update a Stage (PATCH `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Updates a stage's properties.

### Delete a Stage (DELETE `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Deletes a stage.


## Tracking Changes (Audit Logs)

Use the audit endpoints to track changes to pipelines and stages:

* **Pipelines:** GET `/crm/v3/pipelines/{objectType}/{pipelineId}/audit`
* **Stages:** GET `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}/audit`

**Response:** Returns an array of audit log entries, listed in reverse chronological order.  Each entry includes `action` (CREATE, UPDATE, DELETE), `timestamp`, `message`, and `rawObject` (the previous and current state of the object).


**Example 200 Response (GET `/crm/v3/pipelines/deals/11348541/audit`):**  (This is a large example, shortened for brevity. The full response is available in the original text.) The response includes a list of objects that detail the history of changes made to the pipeline. Each object shows the action (CREATE, UPDATE), timestamp, message and the rawObject which details the changes made in the pipeline.

```json
{
  "results": [
    // ... multiple audit log entries ...
  ]
}
```

Remember to replace placeholders like `{objectType}`, `{pipelineId}`, `{stageId}`, and `YOUR_API_KEY` with actual values.  Refer to the HubSpot API documentation for detailed information on authentication and error handling.
