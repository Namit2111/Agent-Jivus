# HubSpot CRM API: Tickets

This document details the HubSpot CRM API endpoints for managing tickets.  Tickets represent customer requests for help and are tracked through pipeline statuses until closure.  These endpoints allow for creation, management, and synchronization of ticket data between HubSpot and external systems.

## Understanding the CRM

Before using the API, familiarize yourself with HubSpot's [Understanding the CRM](<link_to_hubspot_crm_guide>) and [managing your CRM database](<link_to_hubspot_crm_management>) guides.  These provide context on objects, records, properties, and associations.

## API Endpoints

All endpoints are under the `/crm/v3/objects/tickets` base path unless otherwise specified.  Requests require proper authentication (API key).


### 1. Create Tickets

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/tickets`

**Request Body:** JSON

The request body must include a `properties` object containing ticket details. You can optionally include an `associations` object to link the ticket to existing records or activities.

**Required Properties:**

* `subject` (string): Ticket name.
* `hs_pipeline_stage` (integer): Ticket status ID (obtain from pipeline settings).
* `hs_pipeline` (integer, optional): Pipeline ID (if multiple pipelines exist). If omitted, the default pipeline is used.

**Optional Properties:**  (See [default HubSpot ticket properties](<link_to_hubspot_default_properties>) and [creating custom properties](<link_to_hubspot_custom_properties>)) for a complete list.  Example: `hs_ticket_priority`.

**Example Request Body (with associations):**

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
      "to": { "id": 201 }, // Contact ID
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 16 }]
    },
    {
      "to": { "id": 301 }, // Company ID
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 26 }]
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

* `properties` (string): Comma-separated list of properties to return.
* `propertiesWithHistory` (string): Comma-separated list of properties to return, including historical values.
* `associations` (string): Comma-separated list of associated objects to retrieve.


**All Tickets:**

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/tickets`

**Query Parameters:** Same as above.


**Batch Read:**

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/tickets/batch/read`

**Request Body:** JSON

```json
{
  "properties": ["subject", "hs_pipeline_stage", "hs_pipeline"],
  "inputs": [
    { "id": "4444888856" }, // Ticket ID or custom ID if idProperty is specified.
    { "id": "666699988" }
  ],
  "idProperty": "uniquepropertyexample" // Optional: Use a custom unique identifier property.
}
```

**Response:** JSON containing an array of tickets.


### 3. Update Tickets

**Individual Ticket:**

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/tickets/{ticketId}`

**Request Body:** JSON containing the properties to update.


**Batch Update:**

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/tickets/batch/update`

**Request Body:** JSON containing an array of updates, each specifying the ticket ID and properties to modify.


### 4. Associate/Disassociate Tickets

**Associate:**

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/tickets/{ticketId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

* `{toObjectType}`: Type of object to associate (e.g., `contacts`, `companies`).
* `{toObjectId}`: ID of the object.
* `{associationTypeId}`: Association type ID (obtain from [default values](<link_to_hubspot_default_association_types>) or the associations API).


**Disassociate:**

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/tickets/{ticketId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


### 5. Pin an Activity

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/tickets/{ticketId}`

**Request Body:**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789 // Activity ID
  }
}
```

You can also pin during creation (see example in Create Tickets section).


### 6. Delete Tickets

**Individual Ticket:**

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/tickets/{ticketId}`

**Batch Delete:**  (Refer to the "Endpoints" tab on the original HubSpot documentation for batch delete details.)


**Note:** Deleting moves tickets to the recycle bin; they can be restored.

##  Association Type IDs

Default association type IDs can be found at [<link_to_hubspot_default_association_types>].  Custom association types can be retrieved using the associations API.


This documentation provides a concise overview. Refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications.  Remember to replace placeholder IDs and values with your actual data.
