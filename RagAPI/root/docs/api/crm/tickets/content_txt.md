# HubSpot CRM API: Tickets

This document details the HubSpot CRM API endpoints for managing tickets. Tickets represent customer requests for help and are tracked through pipeline statuses until closure.  These endpoints allow for creation, management, and synchronization of ticket data between HubSpot and other systems.

## Understanding the CRM

Before using these API endpoints, familiarize yourself with the [HubSpot CRM Object APIs](link-to-hubspot-crm-object-apis-documentation) and [Associations API](link-to-hubspot-associations-api-documentation).  Also, understand how to [manage your CRM database](link-to-hubspot-crm-database-management).

## API Endpoints

All endpoints are under the `/crm/v3/objects/tickets` base path unless otherwise specified.  Remember to replace placeholders like `{ticketId}` with actual values.  Requests require proper authentication with a HubSpot API key.

### 1. Create Tickets

**Method:** `POST /crm/v3/objects/tickets`

**Request Body:** JSON

This endpoint creates new tickets.  The request body must include a `properties` object containing ticket details.  An optional `associations` object can be included to link the ticket to existing records (contacts, companies) or activities (meetings, notes).

**Required Properties:**

* `subject` (string): The ticket's name.
* `hs_pipeline` (integer): The ID of the pipeline the ticket belongs to.  If omitted, the default pipeline is used.  Obtain the ID from your ticket pipeline settings.
* `hs_pipeline_stage` (integer): The ID of the ticket's initial status within the pipeline. Obtain the ID from your ticket pipeline settings.


**Optional Properties:**

* `hs_ticket_priority` (string):  Priority level (e.g., "HIGH", "LOW", "MEDIUM").  Other custom properties can be added.

**Example Request Body:**

```json
{
  "properties": {
    "hs_pipeline": "0",
    "hs_pipeline_stage": "1",
    "hs_ticket_priority": "HIGH",
    "subject": "Troubleshoot Report"
  }
}
```

**Example with Associations:**

```json
{
  "properties": {
    "hs_pipeline": "0",
    "hs_pipeline_stage": "1",
    "hs_ticket_priority": "HIGH",
    "subject": "Troubleshoot Report"
  },
  "associations": [
    {
      "to": {
        "id": 201  // Contact ID
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 16 // Default association type ID for Contact
        }
      ]
    },
    {
      "to": {
        "id": 301  // Company ID
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 26 // Default association type ID for Company
        }
      ]
    }
  ]
}
```

**Response:**  JSON containing the created ticket's details, including its ID.


### 2. Retrieve Tickets

**Individual Ticket:**

**Method:** `GET /crm/v3/objects/tickets/{ticketId}`

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical data.
* `associations`: Comma-separated list of associated objects to retrieve.


**Batch Tickets:**

**Method:** `POST /crm/v3/objects/tickets/batch/read`

**Request Body:** JSON

This endpoint retrieves multiple tickets efficiently.

**Parameters:**

* `properties`:  Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical data.
* `inputs`: Array of objects, each with an `id` property representing the ticket ID (or a custom unique identifier if `idProperty` is specified).
* `idProperty`: (Optional) The name of a custom unique identifier property to use for retrieving tickets instead of the default `hs_object_id`.


**Example Request Body (by record ID):**

```json
{
  "properties": ["subject", "hs_pipeline_stage", "hs_pipeline"],
  "inputs": [
    {"id": "4444888856"},
    {"id": "666699988"}
  ]
}
```

**Example Request Body (by custom property):**

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

**Response:** JSON containing an array of ticket objects.


### 3. Update Tickets

**Individual Ticket:**

**Method:** `PATCH /crm/v3/objects/tickets/{ticketId}`

**Request Body:** JSON containing the properties to update.

**Batch Tickets:**

**Method:** `POST /crm/v3/objects/tickets/batch/update`

**Request Body:** JSON containing an array of updates, each specifying the ticket ID and properties to update.  This method allows updating tickets by their record ID or a custom unique identifier property.


### 4. Associate/Disassociate Tickets

**Associate:**

**Method:** `PUT /crm/v3/objects/tickets/{ticketId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Disassociate:**

**Method:** `DELETE /crm/v3/objects/tickets/{ticketId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

These endpoints manage associations between tickets and other objects.  `{toObjectType}` and `{toObjectId}` specify the object type and ID to associate/disassociate.  `{associationTypeId}` specifies the type of association (obtain from the [Associations API](link-to-hubspot-associations-api-documentation)).


### 5. Pin an Activity

**Method:** `PATCH /crm/v3/objects/tickets/{ticketId}`

Pins an activity to a ticket.  Include the `hs_pinned_engagement_id` property in the request body with the ID of the activity to pin.  The activity must already be associated with the ticket.

**Example Request Body:**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```

### 6. Delete Tickets

**Individual Ticket:**

**Method:** `DELETE /crm/v3/objects/tickets/{ticketId}`

**Batch Deletion:** (Details not provided in the source text; refer to the HubSpot documentation for batch deletion.)


## Error Handling

The API will return appropriate HTTP status codes and JSON error responses for failed requests.  Refer to the HubSpot API documentation for detailed error codes and handling.


This markdown documentation provides a comprehensive overview of the HubSpot CRM API for Tickets.  Remember to consult the official HubSpot API documentation for the most up-to-date information and detailed specifications.  Replace the placeholder links with the actual links from the HubSpot developer documentation.
