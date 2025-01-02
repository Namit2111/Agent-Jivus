# HubSpot CRM API: Pipelines

This document details the HubSpot CRM API endpoints for managing pipelines and their stages. Pipelines track records through stages (e.g., sales pipelines for revenue prediction, service pipelines for ticket status management).  Depending on your subscription, you can create multiple pipelines for a given object type.

## Supported Objects

Pipelines are available for the following object types:

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

All endpoints are under the base URL `/crm/v3/pipelines`.  Replace `{objectType}` with the actual object type (e.g., `deals`, `tickets`), and `{pipelineId}` and `{stageId}` with their respective IDs.

### Pipelines

#### Create a Pipeline (POST `/crm/v3/pipelines/{objectType}`)

Creates a new pipeline. Requires a `POST` request with the following JSON body:

* `displayOrder` (integer): Determines pipeline display order. Pipelines with the same order are listed alphabetically by label.
* `label` (string):  The pipeline's displayed name.
* `stages` (array): An array of stage objects. Each stage object requires:
    * `displayOrder` (integer): Determines stage display order within the pipeline. Stages with the same order are listed alphabetically by label.
    * `label` (string): The stage's displayed name (must be unique within the pipeline).
    * `metadata` (object):  Optional for all objects except deals.
        * **Deals:** Requires `probability` (float) between 0.0 (Closed Lost) and 1.0 (Closed Won).
        * **Tickets:** Allows `ticketState` (string) with value `OPEN` or `CLOSED`.


**Example Request Body (Deals):**

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

**Stage Limits:**  Appointment, course, listing, lead, order, and service pipelines can have up to 30 stages. Deal, ticket, and custom object pipelines can have up to 100 stages.


#### Replace a Pipeline (PUT `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Replaces an existing pipeline. Uses a `PUT` request with the pipeline ID and the same JSON body structure as creating a new pipeline.  This overwrites the existing pipeline's data.


#### Retrieve Pipelines (GET `/crm/v3/pipelines/{objectType}`)

Retrieves all pipelines for a given object type.  A `GET` request returns an array of pipeline objects, each containing `id`, `label`, `displayOrder`, creation and update timestamps.


#### Retrieve a Pipeline (GET `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Retrieves a single pipeline by ID.


#### Update a Pipeline (PATCH `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Updates a pipeline's properties (label, display order). Uses a `PATCH` request with the pipeline ID and a JSON body containing only the properties to be updated.  Use stage endpoints to update stages.


#### Delete a Pipeline (DELETE `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Deletes a pipeline. Uses a `DELETE` request.  Include the query parameter `validateReferencesBeforeDelete=true` to check for existing records in the pipeline before deletion. If records exist, a 404 error with details will be returned.

**Example 404 Error Response:**

```json
{
  "status": "error",
  "message": "Stage IDs: [renter_viewing, renter_security_deposit_paid, renter_new_lead, renter_closed_won, renter_closed_lost] are being referenced by object IDs: [22901690010]",
  "correlationId": "1fb9ac01-f574-4919-bf55-2c8c25ac1507",
  "context": {
    "stageIds": [
      "renter_viewing, renter_security_deposit_paid, renter_new_lead, renter_closed_won, renter_closed_lost"
    ],
    "objectIds": ["22901690010"]
  },
  "category": "VALIDATION_ERROR",
  "subCategory": "PipelineError.STAGE_ID_IN_USE"
}
```


### Pipeline Stages

#### Create a Stage (POST `/crm/v3/pipelines/{objectType}/{pipelineId}/stages`)

Adds a new stage to a pipeline. Uses a `POST` request with the pipeline ID and the following JSON body:

* `displayOrder` (integer): Stage display order within the pipeline.
* `label` (string):  The stage's displayed name.
* `metadata` (object): Optional for all objects except deals.  Same rules as creating a pipeline apply.


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

#### Replace a Stage (PUT `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Replaces an existing stage. Uses a `PUT` request with the pipeline and stage IDs, and the same JSON body as creating a new stage.


#### Retrieve Stages (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/stages`)

Retrieves all stages in a pipeline.


#### Retrieve a Stage (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Retrieves a single stage by ID.


#### Update a Stage (PATCH `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Updates a stage's properties.


#### Delete a Stage (DELETE `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Deletes a stage.


### Audit Logs

#### Pipeline Audit Log (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/audit`)

Retrieves audit logs for a pipeline.  Returns updates in reverse chronological order.


#### Stage Audit Log (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}/audit`)

Retrieves audit logs for a specific stage.


**Example 200 Response (Pipeline Audit Log):**

(The example response is too long to include here but is present in the original text.  It shows a JSON array of audit log entries, each with details like `action`, `timestamp`, `message`, and the `rawObject` representing the change.)


## Authentication

[Include details on how to authenticate with the HubSpot API here.  This usually involves API keys or OAuth 2.0.]


## Error Handling

[Include details on common error codes and their meanings here.]
