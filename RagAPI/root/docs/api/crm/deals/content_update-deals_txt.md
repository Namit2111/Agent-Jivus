# HubSpot CRM API: Deals

This document details the HubSpot CRM API endpoints for managing deals. Deals in HubSpot represent transactions with contacts or companies, tracked through pipeline stages until won or lost.  These endpoints enable managing deal records and syncing data between HubSpot and other systems.

For a broader understanding of objects, records, properties, and associations APIs, refer to the [Understanding the CRM guide](<link_to_understanding_crm_guide_if_available>). For general CRM database management, see [how to manage your CRM database](<link_to_crm_database_management_if_available>).


## Create Deals

**Endpoint:** `POST /crm/v3/objects/deals`

Create new deals by sending a `POST` request to this endpoint.  Include deal data within a `properties` object.  An optional `associations` object can associate the new deal with existing records (contacts, companies) or activities (meetings, notes).

**Required Properties:**

* `dealname`: Deal name.
* `dealstage`: Deal stage (use internal ID, see note below).
* `pipeline`: Pipeline (use internal ID, defaults to the account's default pipeline if omitted).

**Note:** Use the internal ID for deal stages and pipelines.  These IDs are returned when retrieving deals via the API and can be found in your [deal pipeline settings](<link_to_deal_pipeline_settings_if_available>).


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

**Associations:**

The `associations` object allows associating the new deal with existing records or activities.

**Example Request Body (with Associations):**

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

* **`to.id`**:  Unique ID of the record or activity.
* **`types`**: Association type.  `associationCategory` and `associationTypeId` are required. Default association type IDs are listed [here](<link_to_default_association_type_ids_if_available>).  Custom association types can be retrieved via the [associations API](<link_to_associations_api_if_available>).


## Retrieve Deals

**Individual Deal:** `GET /crm/v3/objects/deals/{dealId}`

**All Deals:** `GET /crm/v3/objects/deals`

**Batch Read:** `POST /crm/v3/objects/deals/batch/read`

Retrieve deals individually using the deal ID or in batches.  The batch endpoint allows retrieving by record ID (`hs_object_id`) or a custom unique identifier property.  The batch endpoint does *not* retrieve associations.

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `associations`: Comma-separated list of associated objects to retrieve IDs for.

**Batch Read Example (Record ID):**

```json
{
  "properties": ["dealname", "dealstage", "pipeline"],
  "inputs": [
    { "id": "7891023" },
    { "id": "987654" }
  ]
}
```

**Batch Read Example (Custom Unique Property):**

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


## Update Deals

**Individual Deal:** `PATCH /crm/v3/objects/deals/{dealId}`

**Batch Update:** `POST /crm/v3/objects/deals/batch/update`

Update deals individually or in batches.  Use the record ID or a custom unique identifier property to identify deals.


## Associate/Disassociate Deals

**Associate:** `PUT /crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Disassociate:** `DELETE /crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

Associate or disassociate deals with other CRM records or activities.  Retrieve `associationTypeId` values from the list of defaults or via a `GET` request to `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`.


## Pin an Activity

Pin an activity to a deal record by including the `hs_pinned_engagement_id` property (activity ID) in a `PATCH` or `POST` request.  The activity must already be associated with the deal.


**Example Request Body (PATCH):**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```

## Delete Deals

**Individual Deal:** `DELETE /crm/v3/objects/deals/{dealId}`

Delete deals individually or in batches (see "Endpoints" tab for batch deletion details).  Deleted deals are moved to the recycling bin and can be restored.


This markdown documentation provides a comprehensive overview of the HubSpot CRM API for managing deals.  Remember to replace placeholder links with the actual links from the HubSpot documentation.
