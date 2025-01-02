# HubSpot CRM API: Deals

This document details the HubSpot CRM API endpoints for managing deals.  Deals represent transactions with contacts or companies, tracked through pipeline stages until won or lost.  These endpoints allow creating, managing, and syncing deal data between HubSpot and other systems.

## Understanding the CRM

For a comprehensive understanding of objects, records, properties, and associations within the HubSpot CRM API, refer to the [Understanding the CRM](<link_to_understanding_crm_guide>) guide.  Learn how to [manage your CRM database](<link_to_crm_database_management>) for more general information.

## API Endpoints

All endpoints below are part of the `/crm/v3/objects/deals` base path unless otherwise specified.  Replace `{dealId}` and `{toObjectId}` with the respective IDs.


### 1. Create Deals (POST `/crm/v3/objects/deals`)

Creates a new deal.  The request body must include a `properties` object with deal details. Optionally, include an `associations` object to link the deal with existing records or activities.

**Request Body (JSON):**

```json
{
  "properties": {
    "amount": "1500.00",
    "closedate": "2019-12-07T16:50:06.678Z",
    "dealname": "New deal",
    "pipeline": "default",  // Use default pipeline if not specified.  Replace with internal pipeline ID if needed.
    "dealstage": "contractsent", // Use internal deal stage ID.
    "hubspot_owner_id": "910901"
  },
  "associations": [
    {
      "to": { "id": 201 }, // ID of the associated record (e.g., contact)
      "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 5 } ] // Association type.  See below for details.
    },
    {
      "to": { "id": 301 }, // ID of another associated record (e.g., company)
      "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 3 } ]
    }
  ]
}
```

**Response (JSON):**  A JSON object representing the newly created deal, including its ID.

**Properties:**  Deal details are stored in properties.  Use default HubSpot properties or create custom ones.  Essential properties for creation include `dealname`, `dealstage`, and optionally `pipeline`.  Retrieve all available properties using a GET request to `/crm/v3/properties/deals`.

**Associations:**  Associate deals with existing records (contacts, companies) or activities (meetings, notes) using the `associations` object.  `associationTypeId` values can be found in the [default association type IDs list](<link_to_association_type_ids>) or retrieved via the associations API.


### 2. Retrieve Deals

**a) Get Individual Deal (GET `/crm/v3/objects/deals/{dealId}`)**

Retrieves a specific deal by its ID.

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `associations`: Comma-separated list of associated objects to retrieve.


**b) Get All Deals (GET `/crm/v3/objects/deals`)**

Retrieves a list of all deals.  Uses the same query parameters as above.

**c) Batch Read Deals (POST `/crm/v3/objects/deals/batch/read`)**

Retrieves a batch of deals by record ID (`hs_object_id`) or a custom unique identifier property.  Associations cannot be retrieved using this endpoint.

**Request Body (JSON):**

```json
{
  "properties": ["dealname", "dealstage", "pipeline"],
  "inputs": [ { "id": "7891023" }, { "id": "987654" } ], // IDs can be record IDs or custom IDs if idProperty is specified
  "idProperty": "uniqueordernumber" // Optional: Specify a custom unique identifier property
}
```

**Response (JSON):** An array of deal objects.


### 3. Update Deals

**a) Update Individual Deal (PATCH `/crm/v3/objects/deals/{dealId}`)**

Updates a specific deal.  Include only the properties to modify in the request body.

**b) Batch Update Deals (POST `/crm/v3/objects/deals/batch/update`)**

Updates multiple deals. The request body should include an array of deal identifiers and the properties to update.


### 4. Associate Existing Deals (PUT `/crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates a deal with another record or activity.  `associationTypeId` can be found in the [default association type IDs list](<link_to_association_type_ids>) or retrieved via the associations API.


### 5. Remove Association (DELETE `/crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Removes an association between a deal and a record or activity.


### 6. Pin an Activity (PATCH `/crm/v3/objects/deals/{dealId}`)

Pins an activity to a deal record.  Use the `hs_pinned_engagement_id` property with the activity's ID.  Only one activity can be pinned per deal.


### 7. Delete Deals (DELETE `/crm/v3/objects/deals/{dealId}`)

Deletes a deal (moves it to the recycling bin).


## Error Handling

The API will return appropriate HTTP status codes and error messages in the response body to indicate success or failure.  Refer to the HubSpot API documentation for detailed error codes and their meanings.


## Rate Limits

Be aware of HubSpot's API rate limits to avoid exceeding allowed request volume.


This documentation provides a high-level overview. Refer to the official HubSpot API documentation for comprehensive details, including examples for all HTTP methods and complete response structures.  Remember to replace placeholder values like `<link_to_understanding_crm_guide>` with actual links to relevant HubSpot documentation.
