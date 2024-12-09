# HubSpot CRM API: Deals

This document details the HubSpot CRM API endpoints for managing deals. Deals in HubSpot represent transactions with contacts or companies, tracked through pipeline stages until won or lost.  These endpoints allow for creating, managing, and syncing deal data between HubSpot and external systems.

For a broader understanding of objects, records, properties, and associations APIs, refer to the [Understanding the CRM](<link_to_understanding_crm_guide>) guide.  For general information on managing your CRM database, see [Managing your CRM Database](<link_to_crm_database_management>).


## Create Deals

To create new deals, send a `POST` request to `/crm/v3/objects/deals`.

The request body should include a `properties` object containing deal data.  An optional `associations` object can be included to associate the new deal with existing records (contacts, companies) or activities (meetings, notes).

**Required Properties:**

* `dealname`: (String) Name of the deal.
* `dealstage`: (String) Stage of the deal. Use the internal ID (obtained from deal pipeline settings).
* `pipeline`: (String, Optional) Pipeline the deal belongs to.  If omitted, the default pipeline is used. Use the internal ID (obtained from deal pipeline settings).

**Example Request Body:**

```json
{
  "properties": {
    "amount": "1500.00",
    "closedate": "2019-12-07T16:50:06.678Z",
    "dealname": "New deal",
    "pipeline": "default", // Replace 'default' with the actual pipeline ID
    "dealstage": "contractsent", // Replace 'contractsent' with the actual deal stage ID
    "hubspot_owner_id": "910901"
  }
}
```

**Note:**  Use internal IDs for deal stages and pipelines.  These IDs are found in your deal pipeline settings.  You can retrieve a list of available properties via a `GET` request to `/crm/v3/properties/deals`.  Learn more about the [properties API](<link_to_properties_api>).


## Associations

When creating a deal, associate it with existing records or activities using the `associations` object.

**Example Request Body (with Associations):**

```json
{
  "properties": {
    "amount": "1500.00",
    "closedate": "2019-12-07T16:50:06.678Z",
    "dealname": "New deal",
    "pipeline": "default", // Replace 'default' with the actual pipeline ID
    "dealstage": "contractsent", // Replace 'contractsent' with the actual deal stage ID
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
* **`types`**: Array defining the association type.  `associationCategory` and `associationTypeId` are required.  See the [list of default association type IDs](<link_to_association_type_ids>) or use the [associations API](<link_to_associations_api>) for custom types.


## Retrieve Deals

Deals can be retrieved individually or in batches.

* **Individual Deal:**  `GET /crm/v3/objects/deals/{dealId}`
* **List of Deals:** `GET /crm/v3/objects/deals`
* **Batch Read:** `POST /crm/v3/objects/deals/batch/read`

**Query Parameters (for individual and list retrieval):**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `associations`: Comma-separated list of associated objects to retrieve IDs for.


**Batch Read Parameters:**

* `properties`:  Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `idProperty`: (Optional)  Name of a custom unique identifier property to use for retrieving deals instead of the record ID (`hs_object_id`).
* `inputs`: Array of objects, each with an `id` property representing the deal ID (or custom ID if `idProperty` is specified).


**Example Batch Read Request (with record ID):**

```json
{
  "properties": ["dealname", "dealstage", "pipeline"],
  "inputs": [
    { "id": "7891023" },
    { "id": "987654" }
  ]
}
```

**Example Batch Read Request (with custom unique identifier property):**

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

The batch endpoint does *not* retrieve associations. Use the [associations API](<link_to_associations_api>) for batch association retrieval.


## Update Deals

Deals can be updated individually or in batches.

* **Individual Deal:** `PATCH /crm/v3/objects/deals/{dealId}`
* **Batch Update:** `POST /crm/v3/objects/deals/batch/update`


## Associate Existing Deals

Associate a deal with other CRM records or activities: `PUT /crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`.  Obtain the `associationTypeId` from the [list of default values](<link_to_association_type_ids>) or via a `GET` request to `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`. Learn more in the [associations API](<link_to_associations_api>).


## Remove an Association

Remove an association: `DELETE /crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`.


## Pin an Activity

Pin an activity to a deal record by including the `hs_pinned_engagement_id` property (the activity's ID) in a `PATCH` request to `/crm/v3/objects/deals/{dealId}`.  Activity IDs are retrieved via the [engagements APIs](<link_to_engagements_api>). Only one activity can be pinned per deal, and the activity must already be associated with the deal.


## Delete Deals

Delete deals individually or in batches (moves them to the recycling bin):

* **Individual Deal:** `DELETE /crm/v3/objects/deals/{dealId}`
* **Batch Delete:**  (See the Endpoints tab in the original document for batch delete details).  Deals can be restored from the recycling bin within HubSpot.


**Remember to replace placeholder IDs and values with your actual data.**  Ensure you have the necessary API keys and authentication set up.  All links marked `<link_to_...>` need to be replaced with the appropriate HubSpot documentation URLs.
