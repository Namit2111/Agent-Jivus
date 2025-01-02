# HubSpot CRM API: Tickets

This document details the HubSpot CRM API endpoints for managing tickets.  Tickets represent customer requests for help and are tracked through pipeline statuses until closure.  These endpoints allow for creating, managing, and syncing ticket data between HubSpot and external systems.

## Understanding the CRM

For a comprehensive understanding of objects, records, properties, and associations within the HubSpot CRM API, refer to the [Understanding the CRM](<link_to_understanding_crm_guide>) guide and [managing your CRM database](<link_to_crm_database_management>).


## API Endpoints

All endpoints are prefixed with `/crm/v3/objects/tickets`.  Replace `{ticketId}` with the actual ticket ID.

**Note:** Internal IDs (numerical values) are required for pipeline stages and pipelines when using the API. These IDs are obtained from your ticket pipeline settings.


### 1. Create Tickets (POST `/crm/v3/objects/tickets`)

Creates a new ticket.

**Request Body (JSON):**

```json
{
  "properties": {
    "hs_pipeline": "0", // Internal ID of the pipeline
    "hs_pipeline_stage": "1", // Internal ID of the pipeline stage
    "hs_ticket_priority": "HIGH",
    "subject": "troubleshoot report"
  },
  "associations": [ // Optional: Associate with existing records/activities
    {
      "to": {
        "id": 201 // ID of the record/activity
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 16 // Association type ID (see default IDs or use the Associations API)
        }
      ]
    },
    {
      "to": {
        "id": 301 // ID of another record/activity
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


### 2. Retrieve Tickets

**a) Retrieve a Single Ticket (GET `/crm/v3/objects/tickets/{ticketId}`)**

Retrieves a specific ticket by its ID.

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `associations`: Comma-separated list of associated objects to retrieve.


**b) Retrieve All Tickets (GET `/crm/v3/objects/tickets`)**

Retrieves a list of all tickets.  Uses the same query parameters as retrieving a single ticket.


**c) Batch Retrieve Tickets (POST `/crm/v3/objects/tickets/batch/read`)**

Retrieves a batch of tickets.  Associations cannot be retrieved using this endpoint.

**Request Body (JSON):**

```json
{
  "properties": ["subject", "hs_pipeline_stage", "hs_pipeline"],
  "inputs": [
    {"id": "4444888856"}, // Record ID or custom unique identifier
    {"id": "666699988"}
  ],
  "idProperty": "uniquepropertyexample" // Optional: Use a custom unique identifier property
}
```

**Response:** A JSON object containing an array of tickets.


### 3. Update Tickets

**a) Update a Single Ticket (PATCH `/crm/v3/objects/tickets/{ticketId}`)**

Updates a specific ticket.

**Request Body (JSON):**  Only include the properties you want to modify.

```json
{
  "properties": {
    "hs_pipeline_stage": "3" // New pipeline stage ID
  }
}
```

**b) Batch Update Tickets (POST `/crm/v3/objects/tickets/batch/update`)**

Updates multiple tickets.


### 4. Associate/Dissociate Tickets (PUT/DELETE `/crm/v3/objects/tickets/{ticketId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

**a) Associate:**  Associates a ticket with a record or activity.  Use a PUT request.

**b) Dissociate:** Removes an association. Use a DELETE request.

`toObjectType`:  The type of the object (e.g., "contacts", "companies").
`toObjectId`: The ID of the object.
`associationTypeId`:  The ID of the association type (obtain from the Associations API or the provided list of default IDs).


### 5. Pin an Activity (PATCH `/crm/v3/objects/tickets/{ticketId}`)

Pins an activity to a ticket.

**Request Body (JSON):**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789 // ID of the activity to pin
  }
}
```


### 6. Delete Tickets (DELETE `/crm/v3/objects/tickets/{ticketId}`)

Deletes a ticket (moves it to the recycle bin).


## Properties API

To view all available ticket properties, make a GET request to `/crm/v3/properties/tickets`.  Refer to the [Properties API](<link_to_properties_api>) documentation for more details.

## Associations API

For detailed information on associations, including default association type IDs and managing custom association types, refer to the [Associations API](<link_to_associations_api>).


## Error Handling

The API will return standard HTTP status codes to indicate success or failure. Error responses will include detailed JSON messages explaining the issue.  Check the HubSpot API documentation for a complete list of error codes and their meanings.
