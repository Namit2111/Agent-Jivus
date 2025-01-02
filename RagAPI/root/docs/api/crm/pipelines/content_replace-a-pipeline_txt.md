# HubSpot CRM API: Pipelines

This document details the HubSpot CRM API endpoints for managing pipelines and their stages.  Pipelines track records through various stages (e.g., sales pipelines for deals, service pipelines for tickets).  The available object types for pipelines are: Deals, Tickets, Appointments, Courses, Listings, Orders, Services, Leads (Sales Hub Professional and Enterprise only), and Custom objects (Enterprise only).

## Pipelines Endpoints

All endpoints are under the base URL `/crm/v3/pipelines/{objectType}` where `{objectType}` represents the object type (e.g., `deals`, `tickets`).

**1. Create a Pipeline (POST /crm/v3/pipelines/{objectType})**

Creates a new pipeline. Requires a `POST` request with the following JSON body:

* `displayOrder` (integer): Determines the pipeline's display order. Pipelines with the same order are sorted alphabetically by label.
* `label` (string): The pipeline's display name in HubSpot.
* `stages` (array): An array of stage objects. Each stage object requires:
    * `displayOrder` (integer): Determines the stage's display order within the pipeline. Stages with the same order are sorted alphabetically by label.
    * `label` (string): The stage's display name. Must be unique within the pipeline.
    * `metadata` (object):  Optional for all objects except deals. For deals, `probability` (float between 0.0 and 1.0) is required (0.0 = Closed Lost, 1.0 = Closed Won). For tickets, `ticketState` ("OPEN" or "CLOSED") can be included.


**Example Request Body (POST /crm/v3/pipelines/deals):**

```json
{
  "displayOrder": 3,
  "label": "New deal pipeline",
  "stages": [
    {
      "label": "In Progress",
      "metadata": {
        "probability": 0.2
      },
      "displayOrder": 0
    },
    {
      "label": "Contract signed",
      "metadata": {
        "probability": 0.8
      },
      "displayOrder": 1
    },
    {
      "label": "Closed Won",
      "metadata": {
        "probability": 1.0
      },
      "displayOrder": 2
    },
    {
      "label": "Closed Lost",
      "metadata": {
        "probability": 0.0
      },
      "displayOrder": 3
    }
  ]
}
```

**2. Replace a Pipeline (PUT /crm/v3/pipelines/{objectType}/{pipelineId})**

Replaces an existing pipeline. Requires a `PUT` request with the pipeline ID (`{pipelineId}`) and the same JSON body as creating a new pipeline. This overwrites the existing pipeline's data.

**3. Retrieve Pipelines (GET /crm/v3/pipelines/{objectType})**

Retrieves all pipelines for a given object type. Returns an array of pipeline objects, each containing `id`, `label`, `displayOrder`, creation and update timestamps.

**4. Retrieve a Pipeline (GET /crm/v3/pipelines/{objectType}/{pipelineId})**

Retrieves a specific pipeline by ID.

**5. Update a Pipeline (PATCH /crm/v3/pipelines/{objectType}/{pipelineId})**

Updates a pipeline's properties (label, displayOrder). Use stage endpoints to modify stages. Requires a `PATCH` request with the properties to update.

**6. Delete a Pipeline (DELETE /crm/v3/pipelines/{objectType}/{pipelineId})**

Deletes a pipeline.  The optional parameter `validateReferencesBeforeDelete=true` checks for associated records. If records exist, a `404 Bad Request` error is returned with details of the records preventing deletion.

**Example 404 Bad Request Response:**

```json
{
  "status": "error",
  "message": "Stage IDs: [renter_viewing, renter_security_deposit_paid, renter_new_lead, renter_closed_won, renter_closed_lost] are being referenced by object IDs: [22901690010]",
  "correlationId": "1fb9ac01-f574-4919-bf55-2c8c25ac1507",
  "category": "VALIDATION_ERROR",
  "subCategory": "PipelineError.STAGE_ID_IN_USE"
}
```


## Pipeline Stages Endpoints

All endpoints are under the base URL `/crm/v3/pipelines/{objectType}/{pipelineId}/stages`.

**1. Create a Stage (POST /crm/v3/pipelines/{objectType}/{pipelineId}/stages)**

Creates a new stage in a pipeline.  Requires a `POST` request with the following JSON body:

* `displayOrder` (integer):  Stage display order within the pipeline.
* `label` (string): Stage display name. Must be unique within the pipeline.
* `metadata` (object): Optional except for deals (requires `probability`), and tickets (can include `ticketState`).


**Example Request Body:**

```json
{
  "metadata": {
    "probability": 0.8
  },
  "displayOrder": 4,
  "label": "Contract signed"
}
```

**2. Replace a Stage (PUT /crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId})**

Replaces an existing stage. Requires a `PUT` request with the stage ID (`{stageId}`) and the same JSON body as creating a new stage.

**3. Retrieve Stages (GET /crm/v3/pipelines/{objectType}/{pipelineId}/stages)**

Retrieves all stages for a pipeline.

**4. Retrieve a Stage (GET /crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId})**

Retrieves a specific stage by ID.

**5. Update a Stage (PATCH /crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId})**

Updates a stage's properties (label, displayOrder).

**6. Delete a Stage (DELETE /crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId})**

Deletes a stage.


## Audit Endpoints

Track changes to pipelines and stages using audit endpoints:

* **Pipelines:** `GET /crm/v3/pipelines/{objectType}/{pipelineId}/audit`
* **Stages:** `GET /crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}/audit`

Responses are lists of updates in reverse chronological order, including action type, timestamp, and user ID.

**Example 200 Response (GET /crm/v3/pipelines/deals/11348541/audit):**  (A heavily truncated example is provided due to the length of the original response).  The full response contains many more audit entries.

```json
{
  "results": [
    // ... many audit entries ...
  ]
}
```

**Note:**  The `rawObject` field in the audit response contains the complete JSON representation of the pipeline or stage *after* the change.  This is a very large JSON object and only a portion is shown in the original text.


This API documentation provides a comprehensive overview of HubSpot's CRM pipeline management endpoints. Remember to consult the official HubSpot API documentation for the most up-to-date information and details on authentication and rate limits.
