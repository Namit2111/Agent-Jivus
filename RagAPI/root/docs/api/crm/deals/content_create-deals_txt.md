# HubSpot CRM API: Deals

This document details the HubSpot CRM API endpoints for managing deals. Deals in HubSpot represent transactions with contacts or companies, tracked through sales pipelines until won or lost.  These endpoints allow for creating, managing, and syncing deal data between HubSpot and other systems.

For a broader understanding of objects, records, properties, and associations APIs, refer to the [Understanding the CRM guide](link-to-understanding-crm-guide).  For general information on managing your CRM database, see [how to manage your CRM database](link-to-crm-database-management).


## Create Deals

**Endpoint:** `POST /crm/v3/objects/deals`

Create new deals using a `POST` request to this endpoint.  The request body should include a `properties` object containing deal data and an optional `associations` object to link the new deal with existing records (contacts, companies) or activities (meetings, notes).

**Required Properties:**

* `dealname`:  The name of the deal.
* `dealstage`: The stage of the deal (use the internal ID, found in your [deal pipeline settings](link-to-deal-pipeline-settings)).
* `pipeline`: (If you have multiple pipelines) The pipeline the deal belongs to (use the internal ID). If omitted, the default pipeline is used.

**Example Request Body:**

```json
{
  "properties": {
    "amount": "1500.00",
    "closedate": "2019-12-07T16:50:06.678Z",
    "dealname": "New deal",
    "pipeline": "default",  // Replace 'default' with your pipeline's internal ID if needed.
    "dealstage": "contractsent", // Replace 'contractsent' with your deal stage's internal ID.
    "hubspot_owner_id": "910901"
  }
}
```

To view all available properties, use a `GET` request to `/crm/v3/properties/deals`. Learn more about the [properties API](link-to-properties-api).


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

* **`to.id`:** The ID of the record or activity to associate.
* **`types`:** An array defining the association type.  `associationCategory` and `associationTypeId` are required.  See the [list of default association type IDs](link-to-default-association-types) or use the [associations API](link-to-associations-api) for custom types.


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

This endpoint allows retrieving a batch of deals by record ID (`hs_object_id`) or a custom unique identifier property.  It *cannot* retrieve associations.  Use the [associations API](link-to-associations-api) for batch association retrieval.

* **`idProperty` (optional):**  Specify a custom unique identifier property if not using record IDs.


**Example Request Body (Batch, with record IDs):**

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

**Example Request Body (Batch, with custom unique identifier):**

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


## Update Deals

Deals can be updated individually or in batches.

**Individual Deal:**

**Endpoint:** `PATCH /crm/v3/objects/deals/{dealId}`

**Batch Update:**

**Endpoint:** `POST /crm/v3/objects/deals/batch/update`


## Associate Existing Deals

**Endpoint:** `PUT /crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

Associates a deal with other CRM records or activities.  Obtain the `associationTypeId` from the [list of default values](link-to-default-association-types) or via a `GET` request to `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`.  Learn more in the [associations API](link-to-associations-api).


## Remove Association

**Endpoint:** `DELETE /crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


## Pin an Activity

Pin an activity to a deal record using the `hs_pinned_engagement_id` property (containing the activity's ID, obtained from the [engagements APIs](link-to-engagements-api)).  Only one activity can be pinned per record, and the activity must already be associated with the deal.


**Example Request Body (PATCH):**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```

**Example Request Body (POST, creating and associating):**

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

Deals can be deleted individually or in batches (moving them to the recycling bin).  See the [Endpoints tab](link-to-endpoints-tab) for batch deletion information.  Deleted deals can be restored within HubSpot.

**Individual Deal:**

**Endpoint:** `DELETE /crm/v3/objects/deals/{dealId}`


**(Remember to replace placeholder links like `link-to-understanding-crm-guide` with the actual links.)**
