# HubSpot CRM API: Deals

This document details the HubSpot CRM API endpoints for managing deals.  Deals in HubSpot represent transactions with contacts or companies, tracked through pipeline stages until won or lost.  These endpoints allow managing deal records and syncing data between HubSpot and other systems.

For broader context on objects, records, properties, and associations within the HubSpot API, refer to the [Understanding the CRM](link_to_understanding_crm_guide) guide and learn how to [manage your CRM database](link_to_crm_database_management).


## Create Deals

**Endpoint:** `/crm/v3/objects/deals`

**Method:** `POST`

Create new deals using a `POST` request to the above endpoint.  The request body should include a `properties` object containing deal data and optionally an `associations` object to link the new deal with existing records (contacts, companies) or activities (meetings, notes).

**Required Properties:**

* `dealname`: (String) The name of the deal.
* `dealstage`: (String) The deal stage. Use the *internal ID* of the deal stage (found in your deal pipeline settings).
* `pipeline`: (String, Optional) The pipeline the deal belongs to.  Use the *internal ID* of the pipeline. If omitted, the default pipeline is used.


**Example Request Body:**

```json
{
  "properties": {
    "amount": "1500.00",
    "closedate": "2019-12-07T16:50:06.678Z",
    "dealname": "New deal",
    "pipeline": "default",
    "dealstage": "contractsent",
    "hubspot_owner_id": "910901"
  }
}
```

**Retrieving Available Properties:**  Use a `GET` request to `/crm/v3/properties/deals` to list all available deal properties (including default and custom).  Learn more about the [properties API](link_to_properties_api).

**Note:**  Always use internal IDs for deal stages and pipelines when interacting with the API.


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
      "to": {
        "id": 201
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 5
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
          "associationTypeId": 3
        }
      ]
    }
  ]
}
```

**Parameters:**

* `to.id`: (Integer) The ID of the record or activity to associate.
* `types`: (Array) An array of association types.  Each object requires `associationCategory` and `associationTypeId`.  Default association type IDs are listed [here](link_to_default_association_types).  Use the [associations API](link_to_associations_api) for custom association types.


## Retrieve Deals

Deals can be retrieved individually or in batches.

**Individual Deal:**

**Endpoint:** `/crm/v3/objects/deals/{dealId}`

**Method:** `GET`

**All Deals:**

**Endpoint:** `/crm/v3/objects/deals`

**Method:** `GET`

**Query Parameters:**

* `properties`: (String) Comma-separated list of properties to return.  Missing properties are omitted from the response.
* `propertiesWithHistory`: (String) Comma-separated list of properties to return, including historical values. Missing properties are omitted from the response.
* `associations`: (String) Comma-separated list of associated objects to retrieve IDs for.  Missing associations are omitted.


**Batch Retrieval:**

**Endpoint:** `/crm/v3/objects/deals/batch/read`

**Method:** `POST`

Retrieve a batch of deals by record ID (`hs_object_id`) or a custom unique identifier property.  This endpoint does *not* retrieve associations. Use the [associations API](link_to_associations_api) to retrieve associated data separately.

**Request Body (Example with record IDs):**

```json
{
  "properties": ["dealname", "dealstage", "pipeline"],
  "inputs": [
    {
      "id": "7891023"
    },
    {
      "id": "987654"
    }
  ]
}
```

**Request Body (Example with a unique identifier property):**

```json
{
  "properties": ["dealname", "dealstage", "pipeline"],
  "idProperty": "uniqueordernumber",
  "inputs": [
    {
      "id": "0001111"
    },
    {
      "id": "0001112"
    }
  ]
}
```

**Request Body (Example with record IDs and historical values):**

```json
{
  "propertiesWithHistory": ["dealstage"],
  "inputs": [
    {
      "id": "7891023"
    },
    {
      "id": "987654"
    }
  ]
}
```


## Update Deals

Deals can be updated individually or in batches.  Use the record ID or a custom unique identifier property to identify the deal.

**Individual Deal (by record ID):**

**Endpoint:** `/crm/v3/objects/deals/{dealId}`

**Method:** `PATCH`

**Batch Update:**

**Endpoint:** `/crm/v3/objects/deals/batch/update`

**Method:** `POST`


## Associate Existing Deals

Associate a deal with other CRM records or activities.

**Endpoint:** `/crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `PUT`

Retrieve `associationTypeId` values from the list of default values or via a `GET` request to `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`. Learn more about associating records with the [associations API](link_to_associations_api).


## Remove an Association

**Endpoint:** `/crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `DELETE`


## Pin an Activity

Pin an activity to a deal record using the `hs_pinned_engagement_id` property. The activity ID can be retrieved via the [engagements APIs](link_to_engagements_api). Only one activity can be pinned per record; the activity must already be associated with the deal.

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
    "pipelines": "default",
    "dealstage": "contractsent",
    "hs_pinned_engagement_id": 123456789
  },
  "associations": [
    {
      "to": {
        "id": 123456789
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 213
        }
      ]
    }
  ]
}
```


## Delete Deals

Deals can be deleted individually or in batches (moving them to the recycling bin).  Learn more about batch deletion on the Endpoints tab.

**Individual Deal:**

**Endpoint:** `/crm/v3/objects/deals/{dealId}`

**Method:** `DELETE`


**(Remember to replace placeholder links like `link_to_understanding_crm_guide` with the actual URLs.)**
