# HubSpot CRM API: Deals

This document details the HubSpot CRM API endpoints for managing deals.  Deals represent transactions with contacts or companies, tracked through pipeline stages until won or lost.  This API allows creation, management, and synchronization of deal data.

## Understanding the CRM Guide

For a comprehensive understanding of HubSpot's object, record, property, and association APIs, refer to the [Understanding the CRM](link_to_understanding_crm_guide) guide.  For general information on managing your CRM database, see [Managing your CRM database](link_to_managing_crm_database).


## Endpoints

All endpoints are under the `/crm/v3/objects/deals` base path unless otherwise specified.  Remember to replace placeholders like `{dealId}` with actual values.


### 1. Create Deals (POST `/crm/v3/objects/deals`)

Creates a new deal.  The request body must include a `properties` object, and optionally an `associations` object.

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
      "to": { "id": 201 },
      "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 5 } ]
    },
    {
      "to": { "id": 301 },
      "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 3 } ]
    }
  ]
}
```

* **properties:**  A JSON object containing deal properties.  `dealname`, `dealstage`, and (if multiple pipelines exist) `pipeline` are required. Use internal IDs for `dealstage` and `pipeline` (found in deal pipeline settings).  See [Default HubSpot deal properties](link_to_default_properties) and learn how to [create custom properties](link_to_custom_properties).
* **associations:** (Optional) An array of objects associating the deal with existing records or activities.  See section on Associations below.

**Response:**  A JSON object representing the created deal, including its ID.


### 2. Retrieve Deals

#### 2.1. Retrieve a Single Deal (GET `/crm/v3/objects/deals/{dealId}`)

Retrieves a single deal by its ID.

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `associations`: Comma-separated list of associated objects to retrieve IDs for.

#### 2.2. Retrieve a List of Deals (GET `/crm/v3/objects/deals`)

Retrieves a list of deals.  Uses the same query parameters as retrieving a single deal.

#### 2.3. Batch Read Deals (POST `/crm/v3/objects/deals/batch/read`)

Retrieves a batch of deals by record ID or custom unique identifier property.  Associations cannot be retrieved using this endpoint.

**Request Body (Example - Record ID):**

```json
{
  "properties": ["dealname", "dealstage", "pipeline"],
  "inputs": [ { "id": "7891023" }, { "id": "987654" } ]
}
```

**Request Body (Example - Unique Property):**

```json
{
  "properties": ["dealname", "dealstage", "pipeline"],
  "idProperty": "uniqueordernumber",
  "inputs": [ { "id": "0001111" }, { "id": "0001112" } ]
}
```

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `idProperty`: (Optional) The name of a custom unique identifier property.  If omitted, `id` refers to the record ID (`hs_object_id`).
* `inputs`: An array of objects, each with an `id` property representing the deal identifier.


### 3. Update Deals

#### 3.1. Update a Single Deal (PATCH `/crm/v3/objects/deals/{dealId}`)

Updates a single deal by its ID.

**Request Body (Example):**

```json
{
  "properties": {
    "dealstage": "closedwon"
  }
}
```

#### 3.2. Batch Update Deals (POST `/crm/v3/objects/deals/batch/update`)

Updates multiple deals.

**Request Body:**  An array of objects, each with an `id` property (record ID or custom unique identifier) and a `properties` object containing the updates.


### 4. Associations

#### 4.1. Associate Existing Deals (PUT `/crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates a deal with other CRM records or activities.

* `{toObjectType}`: The type of the object to associate (e.g., `contacts`, `companies`).
* `{toObjectId}`: The ID of the object to associate.
* `{associationTypeId}`: The ID of the association type.  See [Default association type IDs](link_to_default_association_types) or use the Associations API to get custom association types.

#### 4.2. Remove an Association (DELETE `/crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Removes an association between a deal and another object.


### 5. Pin an Activity (PATCH `/crm/v3/objects/deals/{dealId}`)

Pins an activity to a deal record.  Requires the `hs_pinned_engagement_id` property in the request body, containing the ID of the activity to pin (obtained from the [Engagements APIs](link_to_engagements_api)).  Only one activity can be pinned per deal.

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


##  Error Handling

The API will return appropriate HTTP status codes and error messages in the response body to indicate success or failure.  Consult the HubSpot API documentation for details on error codes.


## Rate Limits

Be aware of HubSpot's API rate limits to avoid exceeding allowed request frequency.


**(Remember to replace the placeholder links with the actual links from the HubSpot documentation.)**
