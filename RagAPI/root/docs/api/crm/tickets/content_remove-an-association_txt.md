# HubSpot CRM API: Tickets

This document details the HubSpot CRM API endpoints for managing tickets.  Tickets represent customer requests for help and are tracked through pipeline statuses until closure.  These endpoints allow for creating, managing, and synchronizing ticket data between HubSpot and external systems.

## Understanding the CRM

Before using the API, familiarize yourself with HubSpot's [Understanding the CRM](link_to_hubspot_crm_guide) guide and [managing your CRM database](link_to_hubspot_crm_management) documentation.  This will provide context on objects, records, properties, and associations.

## API Endpoints

All endpoints below are prefixed with `/crm/v3/objects/tickets`.  Replace `{ticketId}` with the actual ticket ID.

### 1. Create Tickets

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/tickets`

**Request Body:** JSON

This endpoint creates new ticket records.  The request body must include a `properties` object containing ticket details.  An optional `associations` object can associate the new ticket with existing records (contacts, companies) or activities (meetings, notes).

**Required Properties:**

* `subject` (string): Ticket name.
* `hs_pipeline_stage` (integer):  Internal ID of the ticket's initial status.
* `hs_pipeline` (integer, optional): Internal ID of the pipeline. If omitted, the default pipeline is used.

**Example Request Body (with Associations):**

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

**Response:** JSON containing the created ticket's details, including its ID.


### 2. Retrieve Tickets

**Individual Ticket:**

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/tickets/{ticketId}`

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `associations`: Comma-separated list of associated objects to retrieve.


**All Tickets:**

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/tickets`

**Query Parameters:**  Same as above.


**Batch Retrieve:**

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/tickets/batch/read`

**Request Body:** JSON

This endpoint retrieves multiple tickets efficiently.  It accepts an array of `inputs` containing ticket IDs (`id`).  You can specify the `idProperty` to use a custom unique identifier instead of the record ID (`hs_object_id`).

**Example Request Body (with record IDs):**

```json
{
  "properties": ["subject", "hs_pipeline_stage", "hs_pipeline"],
  "inputs": [
    { "id": "4444888856" },
    { "id": "666699988" }
  ]
}
```

**Example Request Body (with custom unique identifier property):**

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

**Response:** JSON array containing the retrieved ticket details.


### 3. Update Tickets

**Individual Ticket:**

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/tickets/{ticketId}`

**Request Body:** JSON containing the properties to update.

**Batch Update:**

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/tickets/batch/update`

**Request Body:** JSON containing an array of updates, each specifying ticket ID and properties to modify.


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

**Request Body:** JSON including the `hs_pinned_engagement_id` property with the activity ID.


### 6. Delete Tickets

**Individual Ticket:**

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/tickets/{ticketId}`

**(Batch delete details are missing from the provided text and need to be added from the actual API documentation.)**


##  Property and Association APIs

Refer to the HubSpot documentation for details on the [properties API](link_to_hubspot_properties_api) and [associations API](link_to_hubspot_associations_api).  These APIs provide information on available ticket properties, association types, and how to manage them.


This markdown provides a structured overview. Remember to replace placeholder links with the actual HubSpot documentation links.  Furthermore,  add batch delete details once obtained from the official HubSpot API reference.
