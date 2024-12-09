# HubSpot CRM API: Deals

This document details the HubSpot CRM API endpoints for managing deals. Deals in HubSpot represent transactions with contacts or companies, tracked through sales pipelines until won or lost.  These endpoints allow for creation, management, and synchronization of deal data between HubSpot and external systems.

## Understanding the CRM

For a comprehensive understanding of objects, records, properties, and associations within the HubSpot CRM API, refer to the [Understanding the CRM guide](link_to_guide_needed).  For general CRM database management, see [how to manage your CRM database](link_to_guide_needed).


## Create Deals

To create new deals, send a `POST` request to `/crm/v3/objects/deals`.

The request body should include a `properties` object containing deal data and optionally an `associations` object to link the new deal with existing records (contacts, companies) or activities (meetings, notes).

**Required Properties:**

* `dealname`: The name of the deal.
* `dealstage`: The stage of the deal in the sales pipeline (use the internal ID).
* `pipeline`:  The pipeline the deal belongs to (use the internal ID; defaults to the account's default pipeline if omitted).

**Example Request Body (JSON):**

```json
{
  "properties": {
    "amount": "1500.00",
    "closedate": "2019-12-07T16:50:06.678Z",
    "dealname": "New deal",
    "pipeline": "default",  // Replace "default" with the actual pipeline ID
    "dealstage": "contractsent", // Replace "contractsent" with the actual deal stage ID
    "hubspot_owner_id": "910901"
  }
}
```

**Retrieving Property IDs:**  Obtain a list of available properties (including internal IDs) via a `GET` request to `/crm/v3/properties/deals`. Learn more about the [properties API](link_to_properties_api_needed).

**Important:** Use internal IDs for deal stages and pipelines. These IDs are found in your [deal pipeline settings](link_to_pipeline_settings_needed).


## Associations

When creating a deal, associate it with existing records or activities using the `associations` object.

**Example Request Body (JSON):**

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
          "associationTypeId": 5 // Association type ID for Contact
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
          "associationTypeId": 3 // Association type ID for Company
        }
      ]
    }
  ]
}
```

* **`to.id`:** The ID of the record or activity.
* **`types`:** Defines the association type.  `associationCategory` is typically "HUBSPOT_DEFINED".  `associationTypeId` can be found in the [list of default association type IDs](link_to_association_types_needed) or retrieved via the [associations API](link_to_associations_api_needed).


## Retrieve Deals

Retrieve deals individually or in batches.

**Individual Deal:**  `GET /crm/v3/objects/deals/{dealId}`

**List of Deals:** `GET /crm/v3/objects/deals`

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `associations`: Comma-separated list of associated objects to retrieve.


**Batch Retrieval:** `POST /crm/v3/objects/deals/batch/read`

This endpoint allows retrieving multiple deals by record ID (`hs_object_id`) or a custom unique identifier property.  Specify `idProperty` if using a custom property.  Associations cannot be retrieved via this endpoint.

**Example Request Body (using record IDs):**

```json
{
  "properties": ["dealname", "dealstage", "pipeline"],
  "inputs": [
    {"id": "7891023"},
    {"id": "987654"}
  ]
}
```

**Example Request Body (using a custom unique identifier property):**

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

**Example Request Body (with historical values):**

```json
{
  "propertiesWithHistory": ["dealstage"],
  "inputs": [
    {"id": "7891023"},
    {"id": "987654"}
  ]
}
```


## Update Deals

Update deals individually or in batches.

**Individual Deal:** `PATCH /crm/v3/objects/deals/{dealId}`

**Batch Update:** `POST /crm/v3/objects/deals/batch/update`  (Requires an array of deal identifiers and properties to update).


## Associate Existing Deals

Associate a deal with other CRM records or activities:

`PUT /crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

Retrieve `associationTypeId` from the [list of default values](link_to_association_types_needed) or via `GET /crm/v4/associations/{fromObjectType}/{toObjectType}/labels`. Learn more in the [associations API](link_to_associations_api_needed) documentation.


## Remove an Association

Remove an association:

`DELETE /crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


## Pin an Activity

Pin an activity to a deal using the `hs_pinned_engagement_id` property (requires the activity ID from the [engagements APIs](link_to_engagements_api_needed)).  Only one activity can be pinned per deal.

**Example Request Body (PATCH):**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```

Pinning during deal creation is also supported.



## Delete Deals

Delete deals individually or in batches (moves deals to the recycle bin; they can be restored).

**Individual Deal:** `DELETE /crm/v3/objects/deals/{dealId}`

Batch deletion details are available on the [Endpoints](link_to_endpoints_tab_needed) tab.


**(Remember to replace placeholder links with actual links from the HubSpot API documentation.)**
