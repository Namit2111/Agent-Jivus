# HubSpot CRM API: Tickets

This document details the HubSpot CRM API endpoints for managing tickets.  Tickets represent customer requests for help and are tracked through pipeline statuses until closure.  These endpoints allow creation, management, and synchronization of ticket data between HubSpot and other systems.

## Understanding the CRM

For a comprehensive understanding of objects, records, properties, and associations within the HubSpot CRM API, refer to the [Understanding the CRM](<link_to_understanding_crm_guide>) guide and learn how to [manage your CRM database](<link_to_crm_database_management>).


## API Endpoints

All endpoints are prefixed with `/crm/v3/objects/tickets`.  Unless otherwise specified, requests should include your HubSpot API key in the header.


### 1. Create Tickets

**Endpoint:** `/crm/v3/objects/tickets`

**Method:** `POST`

**Request Body:** JSON

**Properties:**  The request body includes a `properties` object containing ticket details.  Required properties include `subject` (ticket name), `hs_pipeline_stage` (ticket status), and optionally `hs_pipeline` (if multiple pipelines exist). Use internal IDs for pipeline and stage (obtained from your ticket pipeline settings).  You can also include other custom properties.

**Associations:**  The request body can also include an `associations` object to link the ticket to existing records (contacts, companies) or activities (meetings, notes).

**Example Request (with Associations):**

```json
{
  "properties": {
    "hs_pipeline": "0",
    "hs_pipeline_stage": "1",
    "hs_ticket_priority": "HIGH",
    "subject": "troubleshoot report"
  },
  "associations": [
    {
      "to": { "id": 201 },
      "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 16 } ]
    },
    {
      "to": { "id": 301 },
      "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 26 } ]
    }
  ]
}
```

**Response:**  A JSON object representing the newly created ticket, including its ID.


### 2. Retrieve Tickets

**Individual Ticket:**

**Endpoint:** `/crm/v3/objects/tickets/{ticketId}`

**Method:** `GET`

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `associations`: Comma-separated list of associated objects to retrieve.

**Batch Tickets:**

**Endpoint:** `/crm/v3/objects/tickets/batch/read`

**Method:** `POST`

**Request Body:** JSON

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `idProperty`: (Optional)  The name of a custom unique identifier property to use for retrieval (default is `hs_object_id`).
* `inputs`: An array of objects, each with an `id` property representing the ticket ID (or custom ID if `idProperty` is specified).


**Example Request (Batch, with Record IDs):**

```json
{
  "properties": ["subject", "hs_pipeline_stage", "hs_pipeline"],
  "inputs": [
    { "id": "4444888856" },
    { "id": "666699988" }
  ]
}
```

**Example Request (Batch, with Custom ID Property):**

```json
{
  "properties": ["subject", "hs_pipeline_stage", "hs_pipeline"],
  "idProperty": "uniquepropertyexample",
  "inputs": [
    { "id": "abc" },
    { "id": "def" }
  ]
}
```


**Response:** JSON array of ticket objects.


### 3. Update Tickets

**Individual Ticket:**

**Endpoint:** `/crm/v3/objects/tickets/{ticketId}`

**Method:** `PATCH`

**Request Body:** JSON containing the properties to update.

**Batch Tickets:**

**Endpoint:** `/crm/v3/objects/tickets/batch/update`

**Method:** `POST`

**Request Body:** JSON array of ticket updates, each specifying the ID and properties to update.

**Response:** JSON object confirming the update.


### 4. Associate/Dissociate Tickets

**Associate:**

**Endpoint:** `/crm/v3/objects/tickets/{ticketId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `PUT`

**Dissociate:**

**Endpoint:** `/crm/v3/objects/tickets/{ticketId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `DELETE`


### 5. Pin an Activity

**Endpoint:** `/crm/v3/objects/tickets/{ticketId}`

**Method:** `PATCH`

**Request Body:** JSON including `properties.hs_pinned_engagement_id` with the activity ID.


### 6. Delete Tickets

**Individual Ticket:**

**Endpoint:** `/crm/v3/objects/tickets/{ticketId}`

**Method:** `DELETE`

**(Batch deletion details are omitted from the provided text but would follow a similar pattern to batch update/read.)**


##  Important Considerations

* **Internal IDs:** Use internal IDs for pipelines, stages, and association types.
* **Associations API:**  Refer to the [Associations API](<link_to_associations_api>) documentation for more details on association types.
* **Error Handling:** Implement proper error handling to manage API responses.
* **Rate Limits:** Be mindful of HubSpot's API rate limits.


This documentation provides a concise overview. Refer to the official HubSpot API documentation for comprehensive details and the most up-to-date information.  Remember to replace placeholder `<link>`s with actual links to relevant HubSpot documentation.
