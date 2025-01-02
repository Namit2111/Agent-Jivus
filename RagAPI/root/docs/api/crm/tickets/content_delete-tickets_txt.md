# HubSpot CRM API: Tickets

This document details the HubSpot CRM API endpoints for managing tickets. Tickets represent customer requests for help and are tracked through your support process until closure.  These endpoints allow for creating, managing, and syncing ticket data between HubSpot and other systems.

## Understanding the CRM

For a comprehensive understanding of objects, records, properties, and associations within the HubSpot CRM API, refer to the [Understanding the CRM guide](<link_to_guide_here>).  Information on managing your CRM database can be found [here](<link_to_database_management_here>).


## API Endpoints

All endpoints are prefixed with `/crm/v3/objects/tickets`.  Replace `{ticketId}` with the actual ticket ID.

### 1. Create Tickets (POST `/crm/v3/objects/tickets`)

Creates a new ticket.  The request body must include a `properties` object and optionally an `associations` object.

**Request Body:**

```json
{
  "properties": {
    "hs_pipeline": "0", // Internal ID of the pipeline (get from pipeline settings)
    "hs_pipeline_stage": "1", // Internal ID of the pipeline stage (get from pipeline settings)
    "hs_ticket_priority": "HIGH",
    "subject": "troubleshoot report"
  },
  "associations": [ // Optional
    {
      "to": {
        "id": 201 // ID of the associated record (e.g., contact ID)
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 16 // Association type ID (see default IDs or use associations API)
        }
      ]
    },
    {
      "to": {
        "id": 301 // ID of another associated record (e.g., company ID)
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 26 // Association type ID
        }
      ]
    }
  ]
}
```

**Response:**  A JSON object representing the newly created ticket, including its ID.

**Important:**  Use the *internal IDs* for pipeline and pipeline stages, obtained from your HubSpot ticket pipeline settings.


### 2. Retrieve Tickets

**a) Retrieve Individual Ticket (GET `/crm/v3/objects/tickets/{ticketId}`)**

Retrieves a single ticket by its ID.

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `associations`: Comma-separated list of associated object types to retrieve.

**b) Retrieve All Tickets (GET `/crm/v3/objects/tickets`)**

Retrieves a list of all tickets.  Uses the same query parameters as above.

**c) Batch Retrieve Tickets (POST `/crm/v3/objects/tickets/batch/read`)**

Retrieves a batch of tickets by their record IDs or a custom unique identifier property.

**Request Body:**

```json
{
  "properties": ["subject", "hs_pipeline_stage", "hs_pipeline"],
  "inputs": [
    { "id": "4444888856" },
    { "id": "666699988" }
  ]
}
```

or using a custom unique identifier property:

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


**Response:** A JSON object containing an array of tickets.  Note that the batch endpoint does *not* retrieve associations.


### 3. Update Tickets

**a) Update Individual Ticket (PATCH `/crm/v3/objects/tickets/{ticketId}`)**

Updates a single ticket.  Provide the properties to update in the request body.

**b) Batch Update Tickets (POST `/crm/v3/objects/tickets/batch/update`)**

Updates multiple tickets.  The request body should contain an array of ticket identifiers and the properties to update for each.


### 4. Associate/Dissociate Tickets (PUT/DELETE `/crm/v3/objects/tickets/{ticketId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates or dissociates a ticket with other records or activities.  Use PUT to associate and DELETE to dissociate.  `{toObjectType}`, `{toObjectId}`, and `{associationTypeId}` specify the target object, its ID, and the type of association.  Retrieve `associationTypeId` from the default list or the associations API.


### 5. Pin an Activity (PATCH `/crm/v3/objects/tickets/{ticketId}`)

Pins an activity to a ticket using the `hs_pinned_engagement_id` property.  The activity ID must be obtained from the engagements APIs.

**Request Body:**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```

You can also pin during ticket creation.


### 6. Delete Tickets (DELETE `/crm/v3/objects/tickets/{ticketId}`)

Deletes a ticket (moves it to the recycle bin).  Batch deletion is also available (see documentation for details).


##  Associations API

The Associations API provides detailed information about association types and is crucial for managing associations between tickets and other HubSpot objects.  See the [Associations API documentation](<link_to_associations_api_here>) for more information.


## Properties API

The Properties API allows you to retrieve and manage ticket properties, including creating custom properties.  Refer to the [Properties API documentation](<link_to_properties_api_here>) for more details.  Note that creating tickets via the API requires using internal IDs for properties.



This documentation provides a concise overview.  Always consult the official HubSpot API documentation for the most up-to-date information and detailed specifications. Remember to replace placeholder values like `<link_to_guide_here>` with the actual links.
