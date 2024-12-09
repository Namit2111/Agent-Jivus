# HubSpot CRM API: Deals

This document details the HubSpot CRM API endpoints for managing deals. Deals in HubSpot represent transactions with contacts or companies, tracked through pipeline stages until won or lost.  These endpoints allow managing deal records and syncing deal data with other systems.

For a broader understanding of objects, records, properties, and associations within the HubSpot API, refer to the [Understanding the CRM](link_to_understanding_crm_guide) guide.  General information on managing your CRM database can be found [here](link_to_crm_database_management).


## Create Deals

Use a `POST` request to `/crm/v3/objects/deals` to create new deals.  The request body should include a `properties` object with deal data and an optional `associations` object to link the new deal with existing records (contacts, companies) or activities (meetings, notes).

**Required Properties:**

* `dealname`: Name of the deal.
* `dealstage`: Stage of the deal (use internal ID, see note below).
* `pipeline`: Pipeline the deal belongs to (use internal ID, defaults to the account's default pipeline if omitted).

**Note:** Use the internal ID of a deal stage or pipeline.  These IDs are found in your [deal pipeline settings](link_to_deal_pipeline_settings).  The API will return these internal IDs when retrieving deals.

**Example Request Body:**

```json
{
  "properties": {
    "amount": "1500.00",
    "closedate": "2019-12-07T16:50:06.678Z",
    "dealname": "New deal",
    "pipeline": "default", // Replace 'default' with the internal ID of your pipeline
    "dealstage": "contractsent", // Replace 'contractsent' with the internal ID of your deal stage
    "hubspot_owner_id": "910901"
  }
}
```

To view all available properties, make a `GET` request to `/crm/v3/properties/deals`.  Learn more about the [properties API](link_to_properties_api).


## Associations

When creating a deal, associate it with existing records or activities using the `associations` object.

**Example Request Body (with Associations):**

```json
{
  "properties": {
    "amount": "1500.00",
    "closedate": "2019-12-07T16:50:06.678Z",
    "dealname": "New deal",
    "pipeline": "default", // Replace 'default' with the internal ID of your pipeline
    "dealstage": "contractsent", // Replace 'contractsent' with the internal ID of your deal stage
    "hubspot_owner_id": "910901"
  },
  "associations": [
    {
      "to": {
        "id": 201 // ID of the contact
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 5 // Association type ID
        }
      ]
    },
    {
      "to": {
        "id": 301 // ID of the company
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 3 // Association type ID
        }
      ]
    }
  ]
}
```

* **`to.id`**: Unique ID of the record or activity.
* **`types`**: Association type.  Use the default association type IDs found [here](link_to_association_type_ids) or retrieve custom association types via the [associations API](link_to_associations_api).


## Retrieve Deals

Retrieve deals individually or in batches.

**Individual Deal:**  `GET` request to `/crm/v3/objects/deals/{dealId}`.

**List of Deals:** `GET` request to `/crm/v3/objects/deals`.

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties (including historical values) to return.
* `associations`: Comma-separated list of associated objects to retrieve IDs for.

**Batch Retrieval:** `POST` request to `/crm/v3/objects/deals/batch/read`.  Use the `idProperty` parameter for custom unique identifier properties; otherwise, it defaults to the record ID (`hs_object_id`).  The batch endpoint does *not* retrieve associations. Use the [associations API](link_to_associations_api) for batch association retrieval.

**Example Batch Request Body (with record IDs):**

```json
{
  "properties": ["dealname", "dealstage", "pipeline"],
  "inputs": [
    {"id": "7891023"},
    {"id": "987654"}
  ]
}
```

**Example Batch Request Body (with unique value property):**

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


## Update Deals

Update deals individually or in batches.  Use the record ID or a custom unique identifier property.

**Individual Deal:** `PATCH` request to `/crm/v3/objects/deals/{dealId}`.

**Batch Update:** `POST` request to `/crm/v3/objects/deals/batch/update`.


## Associate Existing Deals

Associate a deal with other records or activities: `PUT` request to `/crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`. Obtain `associationTypeId` from the list of default values or via a `GET` request to `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`.  See the [associations API](link_to_associations_api) for details.

## Remove Association

Remove an association: `DELETE` request to `/crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`.


## Pin an Activity

Pin an activity to a deal record using the `hs_pinned_engagement_id` property (activity ID from the [engagements APIs](link_to_engagements_api)).  Only one activity can be pinned per record; the activity must already be associated with the deal.


**Example Request Body (PATCH):**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```

**Example Request Body (POST - create and pin simultaneously):**

```json
{
  "properties": {
    "dealname": "New deal",
    "pipelines": "default", // Replace 'default' with the internal ID of your pipeline
    "dealstage": "contractsent", // Replace 'contractsent' with the internal ID of your deal stage
    "hs_pinned_engagement_id": 123456789
  },
  "associations": [
    {
      "to": {
        "id": 123456789 // ID of the activity
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 213 // Association type ID
        }
      ]
    }
  ]
}
```


## Delete Deals

Delete deals individually or in batches (moves them to the recycling bin).  See the [Endpoints](link_to_endpoints_tab) tab for batch deletion information.

**Individual Deal:** `DELETE` request to `/crm/v3/objects/deals/{dealId}`.  Deals can be restored within HubSpot.


**(Remember to replace placeholder links like `link_to_understanding_crm_guide` with the actual links.)**
