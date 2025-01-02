# HubSpot CRM API: Pipelines

This document describes the HubSpot CRM API endpoints for managing pipelines and their stages.  Pipelines track records through stages (e.g., sales pipelines track deals, service pipelines track tickets).  The available object types for pipelines depend on your HubSpot subscription.

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


## API Endpoints

All endpoints are prefixed with `/crm/v3/pipelines/`.  Replace `{objectType}` with the appropriate object type (e.g., `deals`, `tickets`).  Replace `{pipelineId}` and `{stageId}` with the respective IDs.


### Pipelines

#### Create a Pipeline (POST `/crm/v3/pipelines/{objectType}`)

Creates a new pipeline.

**Request Body:**

```json
{
  "displayOrder": 3,  // Order in which the pipeline is displayed. Pipelines with the same order are sorted alphabetically by label.
  "label": "New deal pipeline", // Pipeline name displayed in HubSpot.
  "stages": [
    {
      "label": "In Progress",
      "metadata": {
        "probability": "0.2" // Required for deals; 0.0-1.0, 0.0 = Closed Lost, 1.0 = Closed Won.  For tickets: ticketState (OPEN/CLOSED)
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
      }' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

**Response (200 OK):**  A JSON representation of the newly created pipeline, including its ID.


#### Replace a Pipeline (PUT `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Replaces an existing pipeline.

**Request Body:** Same as creating a new pipeline.

**Response (200 OK):**  A JSON representation of the updated pipeline.


#### Retrieve Pipelines (GET `/crm/v3/pipelines/{objectType}`)

Retrieves all pipelines for a given object type.

**Response (200 OK):** A JSON array of pipelines, each containing `id`, `label`, `displayOrder`, creation and update timestamps.

#### Retrieve a Pipeline (GET `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Retrieves a specific pipeline.

**Response (200 OK):** A JSON representation of the pipeline.

#### Update a Pipeline (PATCH `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Updates properties of an existing pipeline (e.g., `label`, `displayOrder`).  Does *not* update stages.

**Request Body:**  A JSON object containing the properties to update.

**Response (200 OK):** A JSON representation of the updated pipeline.

#### Delete a Pipeline (DELETE `/crm/v3/pipelines/{objectType}/{pipelineId}`)

Deletes a pipeline.

**Query Parameter:** `validateReferencesBeforeDelete=true` (optional) Checks for records in the pipeline before deletion.  If records exist, a 404 error with details is returned.

**Response (204 No Content):** Successful deletion.
**Response (404 Bad Request):** If `validateReferencesBeforeDelete=true` and records exist, a JSON error message indicating which stages are in use by which object IDs. Example:

```json
{
  "status": "error",
  "message": "Stage IDs: [...] are being referenced by object IDs: [...]",
  // ... other error details
}
```


### Pipeline Stages

#### Create a Stage (POST `/crm/v3/pipelines/{objectType}/{pipelineId}/stages`)

Adds a new stage to a pipeline.

**Request Body:**

```json
{
  "displayOrder": 4, // Order within the pipeline.
  "label": "Contract signed", // Stage name. Must be unique within the pipeline.
  "metadata": {
    "probability": "0.8" // Required for deals; 0.0-1.0. For tickets: ticketState (OPEN/CLOSED)
  }
}
```

**Response (200 OK):** A JSON representation of the newly created stage.


#### Replace a Stage (PUT `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Replaces an existing stage.

**Request Body:** Same as creating a new stage.

**Response (200 OK):** A JSON representation of the updated stage.


#### Retrieve Stages (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/stages`)

Retrieves all stages for a pipeline.

**Response (200 OK):** A JSON array of stages.


#### Retrieve a Stage (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Retrieves a specific stage.

**Response (200 OK):** A JSON representation of the stage.


#### Update a Stage (PATCH `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Updates properties of an existing stage.

**Request Body:** A JSON object containing the properties to update.

**Response (200 OK):** A JSON representation of the updated stage.


#### Delete a Stage (DELETE `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}`)

Deletes a stage.

**Response (204 No Content):** Successful deletion.


### Audit Logs

#### Pipeline Audit Log (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/audit`)

Retrieves audit log entries for a pipeline.

**Response (200 OK):**  A JSON object containing an array of audit log entries. Each entry includes `action`, `timestamp`, `message`, and `rawObject` (the changed data).

#### Stage Audit Log (GET `/crm/v3/pipelines/{objectType}/{pipelineId}/stages/{stageId}/audit`)

Retrieves audit log entries for a specific stage.

**Response (200 OK):** Similar to pipeline audit log.


## Stage and Pipeline Limits

* Appointment, course, listing, lead, order, and service pipelines: Up to 30 stages.
* Deal, ticket, and custom object pipelines: Up to 100 stages.


This documentation provides a comprehensive overview of the HubSpot CRM API's pipeline management functionalities. Remember to replace placeholders like `{objectType}`, `{pipelineId}`, and `{stageId}` with the actual values.  Always refer to the official HubSpot API documentation for the most up-to-date information and details.
