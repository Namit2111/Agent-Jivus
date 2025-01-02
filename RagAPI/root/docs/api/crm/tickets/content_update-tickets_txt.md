# HubSpot CRM API: Tickets

This document details the HubSpot CRM API endpoints for managing tickets. Tickets represent customer requests for help and are tracked through pipeline statuses until closure.  This API allows management and synchronization of ticket data between HubSpot and other systems.

## Understanding the CRM

For a comprehensive understanding of objects, records, properties, and associations within the HubSpot CRM API, refer to the [Understanding the CRM](<link_to_understanding_crm_guide>) guide and [Managing your CRM database](<link_to_crm_database_management>).

## API Endpoints

All endpoints are under the base URL `/crm/v3/objects/tickets`.  Replace `{ticketId}` with the actual ticket ID.

### 1. Create Tickets

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/tickets`

**Request Body:** JSON

This endpoint creates new tickets. The request body must include a `properties` object and optionally an `associations` object.

**Required Properties:**

* `subject`: (string) The ticket's name.
* `hs_pipeline_stage`: (integer) The ticket's initial status (internal ID required).
* `hs_pipeline`: (integer, optional) The pipeline ID (internal ID required, defaults to the account's default pipeline if omitted).  Multiple pipelines require specifying this field.

**Optional Properties:**

* Any other custom ticket properties.  Use `/crm/v3/properties/tickets` (GET request) to retrieve all available properties.

**Associations (Optional):**

The `associations` object allows associating the new ticket with existing records (e.g., contacts, companies) or activities (e.g., meetings, notes).  Each association requires:

* `to`:  An object with an `id` property specifying the record or activity ID.
* `types`: An array of objects, each defining the association type:
    * `associationCategory`: (string) Usually "HUBSPOT_DEFINED".
    * `associationTypeId`: (integer) The association type ID.  See the [default association type IDs](<link_to_default_association_types>) or use the Associations API to get custom association type IDs.


**Example Request (with associations):**

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
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 16 }]
    },
    {
      "to": { "id": 301 },
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 26 }]
    }
  ]
}
```

**Response:** A JSON object representing the created ticket, including its ID.


### 2. Retrieve Tickets

**Individual Ticket:**

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/tickets/{ticketId}`

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `associations`: Comma-separated list of association types to retrieve.


**All Tickets:**

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/tickets`

**Query Parameters:** Same as individual ticket retrieval.

**Batch Retrieval:**

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/tickets/batch/read`

**Request Body:** JSON

This endpoint allows retrieving multiple tickets by ID (`inputs` array with `id` property) or by a custom unique identifier property (using `idProperty` parameter).  Associations cannot be retrieved with this endpoint.


**Example Request (batch retrieval by record ID):**

```json
{
  "properties": ["subject", "hs_pipeline_stage", "hs_pipeline"],
  "inputs": [
    { "id": "4444888856" },
    { "id": "666699988" }
  ]
}
```

**Example Request (batch retrieval by custom unique property):**

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

**Response:** A JSON object containing an array of ticket objects.


### 3. Update Tickets

**Individual Ticket:**

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/tickets/{ticketId}`

**Request Body:** JSON containing the properties to update.

**Batch Update:**

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/tickets/batch/update`

**Request Body:** JSON containing an array of objects, each specifying ticket ID and properties to update.


### 4. Associate/Disassociate Tickets

**Associate:**

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/tickets/{ticketId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Disassociate:**

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/tickets/{ticketId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


### 5. Pin an Activity

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/tickets/{ticketId}`

**Request Body:** JSON, including the `hs_pinned_engagement_id` property with the activity ID to pin.

### 6. Delete Tickets

**Individual Ticket:**

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/tickets/{ticketId}`

**(Batch deletion details are missing from the provided text and would need to be added based on HubSpot's documentation.)**


**Note:** Internal IDs are required for pipeline stages and pipelines.  These can be found in your HubSpot ticket pipeline settings.  Always refer to the official HubSpot API documentation for the most up-to-date information and details.
