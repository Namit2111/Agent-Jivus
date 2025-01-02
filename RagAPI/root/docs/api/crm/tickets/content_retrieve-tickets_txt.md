# HubSpot CRM API: Tickets

This document details the HubSpot CRM API endpoints for managing tickets. Tickets represent customer requests for help, tracked through pipeline statuses until closure.  These endpoints allow for creation, management, and synchronization of ticket data between HubSpot and external systems.

## Understanding the CRM

For a comprehensive understanding of objects, records, properties, and associations within the HubSpot CRM API, refer to the [Understanding the CRM](link_to_understanding_crm_guide) guide and [managing your CRM database](link_to_crm_database_management).

## API Endpoints

All endpoints below are under the base URL `/crm/v3/objects/tickets`.  Replace `{ticketId}` with the actual ticket ID.

### 1. Create Tickets

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/tickets`

**Request Body:** JSON

This endpoint creates new ticket records.  The request body requires a `properties` object, and optionally an `associations` object.

**Properties:**

* `hs_pipeline`: (String, required if multiple pipelines exist) Internal ID of the pipeline.  Obtain this ID from your ticket pipeline settings.
* `hs_pipeline_stage`: (String, required) Internal ID of the pipeline stage (status). Obtain this ID from your ticket pipeline settings.
* `hs_ticket_priority`: (String) Ticket priority (e.g., "HIGH", "MEDIUM", "LOW").
* `subject`: (String, required) Ticket subject/name.
* **Other custom properties:** You can include other custom ticket properties.  Retrieve available properties using the `/crm/v3/properties/tickets` endpoint (see below).

**Associations:** (Optional)  Associates the ticket with existing records or activities.

* **Format:** An array of association objects.  Each object contains:
    * `to`: Object containing `id` (integer, required): The ID of the record or activity to associate.
    * `types`: Array of objects, each containing:
        * `associationCategory`: String (usually "HUBSPOT_DEFINED")
        * `associationTypeId`: Integer:  The association type ID.  See the [default association type IDs](link_to_default_association_ids) or use the Associations API to retrieve custom association types.


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
      "to": {"id": 201},
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 16}]
    },
    {
      "to": {"id": 301},
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 26}]
    }
  ]
}
```

**Response:**  A JSON object representing the newly created ticket, including its ID.


### 2. Retrieve Tickets

**Method:** `GET` (individual) or `POST` (batch)

**Endpoint:**

* **Individual:** `/crm/v3/objects/tickets/{ticketId}`
* **Batch:** `/crm/v3/objects/tickets/batch/read`

**Query Parameters (GET):**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `associations`: Comma-separated list of associated objects to retrieve IDs for.

**Request Body (POST):**

* `properties`: Array of properties to return.
* `idProperty`: (Optional) The name of a custom unique identifier property to use for retrieving tickets (default is `hs_object_id`).
* `inputs`: Array of objects, each containing `id`: The ID of the ticket to retrieve (based on `idProperty` or `hs_object_id`).

**Example Request (GET, individual):**

```
/crm/v3/objects/tickets/123?properties=subject,hs_pipeline_stage
```

**Example Request (POST, batch, with record IDs):**

```json
{
  "properties": ["subject", "hs_pipeline_stage", "hs_pipeline"],
  "inputs": [
    {"id": "4444888856"},
    {"id": "666699988"}
  ]
}
```

**Example Request (POST, batch, with custom unique identifier):**

```json
{
  "properties": ["subject", "hs_pipeline_stage", "hs_pipeline"],
  "idProperty": "uniquepropertyexample",
  "inputs": [
    {"id": "abc"},
    {"id": "def"}
  ]
}
```

**Response:** JSON object (individual) or JSON array (batch) containing the requested ticket data.


### 3. Update Tickets

**Method:** `PATCH` (individual) or `POST` (batch)

**Endpoint:**

* **Individual:** `/crm/v3/objects/tickets/{ticketId}`
* **Batch:** `/crm/v3/objects/tickets/batch/update`

**Request Body (PATCH):** JSON object containing the properties to update.

**Request Body (POST):** JSON array of objects, each containing:

* `id`: The ID of the ticket to update.
* `properties`: Object of properties to update.

**Example Request (PATCH):**

```json
{
  "properties": {
    "hs_pipeline_stage": "2",
    "subject": "Updated subject"
  }
}
```

**Response:** JSON object representing the updated ticket.


### 4. Associate/Disassociate Tickets

**Method:** `PUT` (associate), `DELETE` (disassociate)

**Endpoint:** `/crm/v3/objects/tickets/{ticketId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

* `{toObjectType}`: The type of the object to associate (e.g., "contacts", "companies").
* `{toObjectId}`: The ID of the object to associate.
* `{associationTypeId}`: The ID of the association type.


### 5. Pin an Activity

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/tickets/{ticketId}`

**Request Body:** JSON object containing `properties`:  `{"hs_pinned_engagement_id": 123456789}` (replace with the activity ID).


### 6. Delete Tickets

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/tickets/{ticketId}`


##  Error Handling

The API will return appropriate HTTP status codes and JSON error responses to indicate success or failure.  Refer to the HubSpot API documentation for details on error handling.


## Rate Limits

Be aware of HubSpot's API rate limits to avoid exceeding allowed requests.


This documentation provides a high-level overview.  Refer to the official HubSpot API documentation for the most up-to-date and detailed information. Remember to replace placeholder IDs and values with your actual data.  Always check the response codes and error messages for proper error handling.
