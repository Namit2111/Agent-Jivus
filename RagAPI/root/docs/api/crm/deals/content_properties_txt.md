# HubSpot CRM API: Deals

This document details the HubSpot CRM API endpoints for managing deals.  Deals represent transactions with contacts or companies and are tracked through pipeline stages until won or lost.  These endpoints allow for creating, managing, and syncing deal data.

## Understanding the CRM (Recommended Reading)

Before using these API endpoints, it's highly recommended to read the HubSpot documentation on [Understanding the CRM](link_to_hubspot_crm_understanding_doc). This will provide context on objects, records, properties, and associations within the HubSpot CRM.

## API Endpoints

All endpoints below are under the base URL `/crm/v3/objects/deals`.  Replace `{dealId}` with the actual deal ID.  All requests require proper authentication.

### 1. Create Deals (POST `/crm/v3/objects/deals`)

Creates a new deal. The request body must include a `properties` object with at least `dealname`, `dealstage`, and optionally `pipeline`.  The `pipeline` property is required if you have multiple pipelines configured. Use internal IDs for `dealstage` and `pipeline` (found in your deal pipeline settings).  You can also include an `associations` object to link the new deal with existing contacts, companies, or activities.

**Request Body (Example):**

```json
{
  "properties": {
    "amount": "1500.00",
    "closedate": "2019-12-07T16:50:06.678Z",
    "dealname": "New deal",
    "pipeline": "default",
    "dealstage": "contractsent",
    "hubspot_owner_id": "910901"
  },
  "associations": [
    {
      "to": {
        "id": 201 // Contact ID
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 5 // Contact to Deal association type ID
        }
      ]
    },
    {
      "to": {
        "id": 301 // Company ID
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 3 // Company to Deal association type ID
        }
      ]
    }
  ]
}
```

**Response (Example):**  A JSON object representing the newly created deal, including its ID and properties.

```json
{
  "id": "12345",
  "properties": {
    // ... properties of the newly created deal ...
  }
}
```


### 2. Retrieve Deals

**a) Get Single Deal (GET `/crm/v3/objects/deals/{dealId}`)**

Retrieves a specific deal by its ID.  Query parameters `properties`, `propertiesWithHistory`, and `associations` can filter the response.

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `associations`: Comma-separated list of associated objects to retrieve.


**b) Get All Deals (GET `/crm/v3/objects/deals`)**

Retrieves a list of deals.  Uses the same query parameters as the single deal retrieval.

**c) Batch Read Deals (POST `/crm/v3/objects/deals/batch/read`)**

Retrieves multiple deals efficiently.  Accepts an array of IDs (`inputs`) and optionally an `idProperty` for custom unique identifiers.  Does *not* retrieve associations.

**Request Body (Example - using record IDs):**

```json
{
  "properties": ["dealname", "dealstage", "pipeline"],
  "inputs": [
    {"id": "7891023"},
    {"id": "987654"}
  ]
}
```

**Request Body (Example - using custom unique identifier):**

```json
{
  "properties": ["dealname", "dealstage", "pipeline"],
  "idProperty": "uniqueordernumber",
  "inputs": [
    {"id": "0001111"},
    {"id": "0001112"}
  ]
}
```


### 3. Update Deals

**a) Update Single Deal (PATCH `/crm/v3/objects/deals/{dealId}`)**

Updates a single deal.  Provide only the properties you wish to modify.

**b) Batch Update Deals (POST `/crm/v3/objects/deals/batch/update`)**

Updates multiple deals.  The request body should contain an array of deals, each with its ID and the properties to update.


### 4. Associate/Dissociate Deals (PUT/DELETE `/crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates or removes associations between deals and other objects (contacts, companies, activities).  `associationTypeId` can be found in the HubSpot documentation or via the associations API.

### 5. Pin an Activity (PATCH `/crm/v3/objects/deals/{dealId}`)

Pins an activity to a deal record using the `hs_pinned_engagement_id` property.  The activity must already be associated with the deal.

**Request Body (Example):**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```


### 6. Delete Deals (DELETE `/crm/v3/objects/deals/{dealId}`)

Deletes a deal (moves it to the recycling bin).


## Error Handling

The API will return appropriate HTTP status codes and JSON error responses to indicate success or failure. Refer to the HubSpot API documentation for details on specific error codes and messages.


## Rate Limits

Be mindful of HubSpot's API rate limits to avoid throttling.


This documentation provides a comprehensive overview of the HubSpot CRM API for managing deals. Always refer to the official HubSpot API documentation for the most up-to-date information and details.
