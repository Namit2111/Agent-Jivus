# HubSpot CRM API: Tickets

This document details the HubSpot CRM API endpoints for managing tickets. Tickets represent customer requests for help and are tracked through pipeline statuses until closure.  These endpoints allow for creating, managing, and syncing ticket data between HubSpot and other systems.

## Understanding the CRM (Prerequisites)

Before using these APIs, familiarize yourself with HubSpot's CRM concepts:

* **Objects:**  Represent data types (e.g., Contacts, Companies, Tickets).
* **Records:** Individual instances of an object (e.g., a specific contact, company, or ticket).
* **Properties:**  Attributes of an object (e.g., `subject`, `hs_pipeline_stage` for tickets).
* **Associations:** Links between records of different objects (e.g., associating a ticket with a contact).

See the [Understanding the CRM guide](link_to_hubspot_guide_here) and [managing your CRM database](link_to_hubspot_guide_here) for more details.


## API Endpoints

All endpoints are under the `/crm/v3/objects/tickets` base path unless otherwise specified.  Replace `{ticketId}` with the actual ticket ID.  Internal IDs (numeric) are required for pipeline stages and pipelines.


### 1. Create Tickets (POST `/crm/v3/objects/tickets`)

Creates a new ticket.

**Request Body (JSON):**

```json
{
  "properties": {
    "hs_pipeline": "0", // Internal ID of the pipeline (required if multiple pipelines exist)
    "hs_pipeline_stage": "1", // Internal ID of the pipeline stage (required)
    "hs_ticket_priority": "HIGH", // Example custom property
    "subject": "troubleshoot report"
  },
  "associations": [ // Optional: Associate with existing records/activities
    {
      "to": {
        "id": 201 // ID of the record (contact, company etc.)
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 16 // Association type ID (see below)
        }
      ]
    },
    {
      "to": {
        "id": 301 // ID of another record
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 26 // Another association type ID
        }
      ]
    }
  ]
}
```

**Response (JSON):**  A JSON representation of the created ticket, including its ID.

**Associations:**  `associationTypeId` values can be found in the [default association type list](link_to_hubspot_list_here) or retrieved via the [associations API](link_to_hubspot_api_here).  `to.id` is the ID of the associated record.


### 2. Retrieve Tickets

#### 2.1. Retrieve a Single Ticket (GET `/crm/v3/objects/tickets/{ticketId}`)

Retrieves a specific ticket by its ID.

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return with history.
* `associations`: Comma-separated list of associated objects to retrieve.

#### 2.2. Retrieve All Tickets (GET `/crm/v3/objects/tickets`)

Retrieves a list of all tickets.  Uses the same query parameters as above.

#### 2.3. Batch Read Tickets (POST `/crm/v3/objects/tickets/batch/read`)

Retrieves a batch of tickets by ID (record ID or custom unique identifier).  Associations cannot be retrieved via this endpoint.

**Request Body (JSON):**

```json
{
  "properties": ["subject", "hs_pipeline_stage", "hs_pipeline"],
  "inputs": [
    { "id": "4444888856" }, // Record ID or custom ID if 'idProperty' is specified
    { "id": "666699988" }
  ],
  "idProperty": "uniquepropertyexample" // Optional: Use a custom unique identifier property
}
```


### 3. Update Tickets

#### 3.1. Update a Single Ticket (PATCH `/crm/v3/objects/tickets/{ticketId}`)

Updates a single ticket.

**Request Body (JSON):**  Only include properties you wish to modify.

#### 3.2. Batch Update Tickets (POST `/crm/v3/objects/tickets/batch/update`)

Updates multiple tickets.

**Request Body (JSON):**  An array of objects, each specifying ticket IDs and properties to update.


### 4. Associate Existing Tickets (PUT `/crm/v3/objects/tickets/{ticketId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates an existing ticket with another record or activity.

### 5. Remove Association (DELETE `/crm/v3/objects/tickets/{ticketId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Removes an association between a ticket and another record or activity.


### 6. Pin an Activity (PATCH `/crm/v3/objects/tickets/{ticketId}`)

Pins an activity to a ticket using the `hs_pinned_engagement_id` property.  The activity must already be associated with the ticket.

**Request Body (JSON):**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789 // ID of the activity to pin
  }
}
```


### 7. Delete Tickets (DELETE `/crm/v3/objects/tickets/{ticketId}`)

Deletes a ticket (moves it to the recycling bin).  Batch deletion is mentioned but not detailed in the provided text.


## Error Handling

The API will return appropriate HTTP status codes (e.g., 400 for bad requests, 404 for not found) and JSON error responses with details.


## Rate Limits

Consult HubSpot's API documentation for rate limit information.


This documentation provides a comprehensive overview of the HubSpot CRM API for managing tickets.  Remember to replace placeholder IDs and values with your actual data.  Always refer to the official HubSpot API documentation for the most up-to-date information and details.
