# HubSpot CRM API: Tickets

This document details the HubSpot CRM API endpoints for managing tickets. Tickets represent customer requests for help and are tracked through pipeline statuses until closure.  These endpoints allow for creating, managing, and syncing ticket data between HubSpot and other systems.

## Understanding the CRM (Prerequisites)

Before using these APIs, familiarize yourself with HubSpot's [CRM object model](link-to-hubspot-crm-object-model-documentation), [properties](link-to-hubspot-properties-api-documentation), and [associations](link-to-hubspot-associations-api-documentation).  Understanding how to [manage your CRM database](link-to-hubspot-crm-database-management) is also beneficial.

## API Endpoints

All endpoints are under the `/crm/v3/objects/tickets` base path unless otherwise specified.  Remember to replace placeholders like `{ticketId}` with actual values.

### 1. Create Tickets

**Method:** `POST /crm/v3/objects/tickets`

**Request Body:** JSON

This endpoint creates a new ticket.  The request body requires a `properties` object, and optionally an `associations` object.

**Required Properties:**

* `subject` (string): The ticket's name.
* `hs_pipeline_stage` (integer): The ticket's initial status (internal ID).
* `hs_pipeline` (integer, optional): The pipeline ID (internal ID). If omitted, the default pipeline is used.

**Optional Properties:**  All other custom and default ticket properties.  Retrieve available properties using the `/crm/v3/properties/tickets` endpoint (GET request).

**Optional Associations:**

The `associations` array allows associating the ticket with existing records (contacts, companies) or activities (meetings, notes).  Each association object requires:

* `to`:  An object with an `id` property specifying the record or activity ID.
* `types`: An array of objects, each specifying the association type with `associationCategory` ("HUBSPOT_DEFINED") and `associationTypeId` (see [default association types](link-to-hubspot-default-association-types) or use the Associations API).


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

**Response:**  A JSON object representing the newly created ticket, including its ID and properties.


### 2. Retrieve Tickets

**Method:** `GET /crm/v3/objects/tickets/{ticketId}` (individual) or `GET /crm/v3/objects/tickets` (list) or `POST /crm/v3/objects/tickets/batch/read` (batch)

**Individual Ticket:** Retrieves a single ticket by its ID.

**List of Tickets:** Retrieves a list of all tickets.

**Batch Read:** Retrieves multiple tickets by record ID (`hs_object_id`) or a custom unique identifier property.

**Query Parameters (for GET requests):**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return with their history.
* `associations`: Comma-separated list of associated objects to retrieve.

**Batch Read Request Body:**

```json
{
  "properties": ["subject", "hs_pipeline_stage", "hs_pipeline"],
  "inputs": [
    { "id": "4444888856" },
    { "id": "666699988" }
  ]
}
```

(Use `idProperty` parameter for custom unique identifiers)

**Response:** JSON object(s) representing the retrieved ticket(s).


### 3. Update Tickets

**Method:** `PATCH /crm/v3/objects/tickets/{ticketId}` (individual) or `POST /crm/v3/objects/tickets/batch/update` (batch)

**Individual Update:** Updates a single ticket by its ID.

**Batch Update:** Updates multiple tickets.  The request body contains an array of updates, each specifying the ticket ID and the properties to modify.

**Request Body (individual):**  JSON object with the properties to update.

**Response:** JSON object representing the updated ticket(s).


### 4. Associate/Disassociate Tickets

**Method:** `PUT` (associate) or `DELETE` (disassociate) `/crm/v3/objects/tickets/{ticketId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

Associates or disassociates a ticket with a record or activity.  `toObjectType`, `toObjectId`, and `associationTypeId` identify the target record/activity and the association type.


### 5. Pin an Activity

**Method:** `PATCH /crm/v3/objects/tickets/{ticketId}`

Pins an activity to a ticket using `hs_pinned_engagement_id` property.  The activity must already be associated with the ticket.

**Example Request:**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```


### 6. Delete Tickets

**Method:** `DELETE /crm/v3/objects/tickets/{ticketId}` (individual)


## Error Handling

The API returns standard HTTP status codes to indicate success or failure.  Refer to the HubSpot API documentation for detailed error codes and messages.


This documentation provides a concise overview. Consult the official HubSpot API documentation for the most up-to-date information and detailed specifications.  Remember to obtain the necessary API keys and authorization before making any requests.
