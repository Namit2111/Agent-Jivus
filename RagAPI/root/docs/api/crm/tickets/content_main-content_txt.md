# HubSpot CRM API: Tickets

This document details the HubSpot CRM API endpoints for managing tickets.  Tickets represent customer requests for help and are tracked through pipeline statuses until closure.  These endpoints allow for creating, managing, and syncing ticket data between HubSpot and other systems.

## Understanding the CRM

For a comprehensive understanding of objects, records, properties, and associations within the HubSpot CRM API, refer to the [Understanding the CRM](link_to_hubspot_crm_guide) guide and [managing your CRM database](link_to_hubspot_crm_management).


## Endpoints

All endpoints are located under the `/crm/v3/objects/tickets` base path unless otherwise specified.  Replace `{ticketId}` with the actual ticket ID.


### 1. Create Tickets

**Method:** `POST /crm/v3/objects/tickets`

**Request Body:** JSON

The request body must include a `properties` object containing ticket details.  Optionally, include an `associations` object to link the ticket with existing records or activities.

**Required Properties:**

* `subject`: Ticket's name (string).
* `hs_pipeline`:  The pipeline ID (integer).  If omitted, the default pipeline is used.
* `hs_pipeline_stage`: The pipeline stage ID (integer).  Use internal IDs from your [ticket pipeline settings](link_to_hubspot_pipeline_settings).

**Optional Properties:**

* `hs_ticket_priority`:  Ticket priority (e.g., "HIGH", "LOW").  Other custom properties can be added as needed.

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
      "to": {
        "id": 201 
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 16 
        }
      ]
    },
    {
      "to": {
        "id": 301 
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 26 
        }
      ]
    }
  ]
}
```

*Replace `201`, `16`, `301`, and `26` with your actual IDs.*  `associationTypeId` values are found in the [list of default values](link_to_default_association_types) or via the [associations API](link_to_associations_api).

**Response:** JSON containing the created ticket's details, including its ID.


### 2. Retrieve Tickets

**a) Individual Ticket:**

**Method:** `GET /crm/v3/objects/tickets/{ticketId}`

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `associations`: Comma-separated list of associated objects to retrieve.

**Response:** JSON containing the ticket's details.


**b) List of Tickets:**

**Method:** `GET /crm/v3/objects/tickets`

**Query Parameters:** Same as above.

**Response:** JSON containing a list of tickets.


**c) Batch Retrieval:**

**Method:** `POST /crm/v3/objects/tickets/batch/read`

**Request Body:** JSON

* `properties`:  Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `idProperty`: (Optional) The name of a custom unique identifier property to use for lookup (default is `hs_object_id`).
* `inputs`: Array of objects, each with an `id` property representing the ticket ID (or custom ID if `idProperty` is used).

**Example Request (by record ID):**

```json
{
  "properties": ["subject", "hs_pipeline_stage", "hs_pipeline"],
  "inputs": [
    {"id": "4444888856"},
    {"id": "666699988"}
  ]
}
```

**Example Request (by custom ID):**

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

**Response:** JSON containing an array of tickets.  Note: Associations cannot be retrieved via this endpoint.


### 3. Update Tickets

**a) Individual Ticket:**

**Method:** `PATCH /crm/v3/objects/tickets/{ticketId}`

**Request Body:** JSON containing the properties to update.

**Response:** JSON containing the updated ticket's details.


**b) Batch Update:**

**Method:** `POST /crm/v3/objects/tickets/batch/update`

**Request Body:** JSON containing an array of updates, each specifying the ticket ID and properties to update.  This requires further detail not provided in the source text.


### 4. Associate Existing Tickets

**Method:** `PUT /crm/v3/objects/tickets/{ticketId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

* `{toObjectType}`: Type of object to associate (e.g., `contacts`, `companies`).
* `{toObjectId}`: ID of the object to associate.
* `{associationTypeId}`: ID of the association type.


### 5. Remove Association

**Method:** `DELETE /crm/v3/objects/tickets/{ticketId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


### 6. Pin Activity

**Method:** `PATCH /crm/v3/objects/tickets/{ticketId}`

**Request Body:** JSON including the `hs_pinned_engagement_id` property with the activity ID.


### 7. Delete Tickets

**Method:** `DELETE /crm/v3/objects/tickets/{ticketId}`


**(Batch deletion details were not provided in the source text.)**


## Properties API

To retrieve a list of available ticket properties, use: `GET /crm/v3/properties/tickets`  For more details, see the [properties API](link_to_hubspot_properties_api) documentation.


## Associations API

For more information on associations, consult the [associations API](link_to_hubspot_associations_api) documentation.  This includes details on retrieving `associationTypeId` values.  Remember that the batch read endpoint does *not* retrieve associations.


Remember to replace placeholder IDs and values with your actual data.  Refer to the HubSpot Developer documentation for complete details and authentication instructions.  All links marked `link_to...` need to be replaced with appropriate HubSpot documentation links.
