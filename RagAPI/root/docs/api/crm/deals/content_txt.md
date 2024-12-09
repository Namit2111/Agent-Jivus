# HubSpot CRM API: Deals

This document details the HubSpot CRM API endpoints for managing deals.  Deals represent transactions with contacts or companies and are tracked through pipeline stages until won or lost.  These endpoints allow for creating, managing, and syncing deal data between HubSpot and external systems.

## Understanding the CRM

For a comprehensive understanding of objects, records, properties, and associations APIs, refer to the [Understanding the CRM](<link_to_understanding_crm_guide>) guide.  For general information on managing your CRM database, see [Managing your CRM Database](<link_to_managing_crm_database>).


## Create Deals

**Endpoint:** `POST /crm/v3/objects/deals`

Create new deals by sending a `POST` request to the above endpoint. The request body should include a `properties` object containing deal data and an optional `associations` object to link the new deal with existing records (contacts, companies) or activities (meetings, notes).

**Required Properties:**

* `dealname`: The name of the deal.
* `dealstage`: The stage of the deal (use internal ID).
* `pipeline`: The pipeline the deal belongs to (use internal ID, defaults to the default pipeline if omitted).

**Example Request Body:**

```json
{
  "properties": {
    "amount": "1500.00",
    "closedate": "2019-12-07T16:50:06.678Z",
    "dealname": "New deal",
    "pipeline": "default",  // Replace "default" with the actual pipeline's internal ID
    "dealstage": "contractsent", // Replace "contractsent" with the actual deal stage's internal ID
    "hubspot_owner_id": "910901"
  }
}
```

**Note:** Use internal IDs for deal stages and pipelines.  These IDs can be found in your [deal pipeline settings](<link_to_deal_pipeline_settings>).  You can retrieve a list of your account's deal properties via a `GET` request to `/crm/v3/properties/deals`.  Learn more about the [properties API](<link_to_properties_api>).


## Associations

When creating a deal, associate it with existing records or activities using the `associations` object.

**Example Request Body (with associations):**

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
      "to": { "id": 201 }, // Contact ID
      "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 5 } ]
    },
    {
      "to": { "id": 301 }, // Company ID
      "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 3 } ]
    }
  ]
}
```

**Parameters:**

* `to.id`: The ID of the record or activity to associate.
* `types`:  An array defining the association type.  `associationCategory` is usually "HUBSPOT_DEFINED".  `associationTypeId` can be found in the [list of default association types](<link_to_default_association_types>) or retrieved via the [associations API](<link_to_associations_api>).


## Retrieve Deals

Deals can be retrieved individually or in batches.

**Individual Deal:**

**Endpoint:** `GET /crm/v3/objects/deals/{dealId}`

**List of Deals:**

**Endpoint:** `GET /crm/v3/objects/deals`

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `associations`: Comma-separated list of associated objects to retrieve IDs for.

**Batch Retrieval:**

**Endpoint:** `POST /crm/v3/objects/deals/batch/read`

This endpoint allows retrieving a batch of deals by record ID (`hs_object_id`) or a custom unique identifier property.  Associations cannot be retrieved using this endpoint.  Use the `idProperty` parameter for custom unique identifier properties.

**Example Request Body (Record ID):**

```json
{
  "properties": ["dealname", "dealstage", "pipeline"],
  "inputs": [
    { "id": "7891023" },
    { "id": "987654" }
  ]
}
```

**Example Request Body (Custom Unique Property):**

```json
{
  "properties": ["dealname", "dealstage", "pipeline"],
  "idProperty": "uniqueordernumber",
  "inputs": [
    { "id": "0001111" },
    { "id": "0001112" }
  ]
}
```


**Example Request Body (with historical values):**

```json
{
  "propertiesWithHistory": ["dealstage"],
  "inputs": [
    { "id": "7891023" },
    { "id": "987654" }
  ]
}
```

## Update Deals

Deals can be updated individually or in batches.

**Individual Deal:**

**Endpoint:** `PATCH /crm/v3/objects/deals/{dealId}`

**Batch Update:**

**Endpoint:** `POST /crm/v3/objects/deals/batch/update`


## Associate Existing Deals

**Endpoint:** `PUT /crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

Associates a deal with other CRM records or activities.  Obtain `associationTypeId` from the [list of default values](<link_to_default_association_types>) or via a `GET` request to `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`.


## Remove an Association

**Endpoint:** `DELETE /crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


## Pin an Activity

Pin an activity to a deal record using the `hs_pinned_engagement_id` property (containing the activity ID from the [engagements APIs](<link_to_engagements_api>)).  Only one activity can be pinned per deal.  The activity must already be associated with the deal.

**Example Request Body (PATCH):**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```

**Example Request Body (POST - create and pin):**

```json
{
  "properties": {
    "dealname": "New deal",
    "pipeline": "default",
    "dealstage": "contractsent",
    "hs_pinned_engagement_id": 123456789
  },
  "associations": [
    {
      "to": { "id": 123456789 },
      "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 213 } ]
    }
  ]
}
```

## Delete Deals

Deals can be deleted individually or in batches (sent to the recycling bin).  See the [Endpoints](<link_to_endpoints_tab>) tab for batch deletion information.

**Individual Deal:**

**Endpoint:** `DELETE /crm/v3/objects/deals/{dealId}`


**Note:** Replace placeholders like `<link_to_understanding_crm_guide>` with actual links.  Add any missing links to the relevant sections within the HubSpot documentation.
