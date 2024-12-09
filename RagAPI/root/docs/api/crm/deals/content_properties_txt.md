# HubSpot CRM API: Deals

This document details the HubSpot CRM API endpoints for managing deals.  Deals in HubSpot represent transactions with contacts or companies, tracked through pipeline stages until won or lost.  These endpoints allow for creating, managing, and syncing deal data between HubSpot and other systems.

For a broader understanding of objects, records, properties, and associations within the HubSpot CRM API, refer to the [Understanding the CRM](link-to-understanding-crm-guide) guide. For general CRM database management, see [managing your CRM database](link-to-crm-database-management).

## Create Deals

To create a new deal, send a `POST` request to `/crm/v3/objects/deals`.

The request body should include a `properties` object containing deal data, and optionally an `associations` object to link the deal with existing records (contacts, companies) or activities (meetings, notes).

**Required Properties:**

* `dealname`: The name of the deal.
* `dealstage`: The stage of the deal in the pipeline (use the internal ID).
* `pipeline`: The pipeline the deal belongs to (use the internal ID; defaults to the account's default pipeline if omitted).

**Example Request Body (JSON):**

```json
{
  "properties": {
    "amount": "1500.00",
    "closedate": "2019-12-07T16:50:06.678Z",
    "dealname": "New deal",
    "pipeline": "default",  // Replace 'default' with the actual pipeline ID
    "dealstage": "contractsent", // Replace 'contractsent' with the actual deal stage ID
    "hubspot_owner_id": "910901"
  }
}
```

**Note:**  Use internal IDs for deal stages and pipelines.  These IDs can be found in your [deal pipeline settings](link-to-deal-pipeline-settings).  You can retrieve a list of available properties via a `GET` request to `/crm/v3/properties/deals`.  Learn more about the [properties API](link-to-properties-api).


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
      "to": { "id": 201 }, // Contact ID
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 5 }]
    },
    {
      "to": { "id": 301 }, // Company ID
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 3 }]
    }
  ]
}
```

**Parameters:**

* `to.id`: The ID of the record or activity.
* `types`:  An array defining the association type.  `associationCategory` is usually "HUBSPOT_DEFINED".  `associationTypeId` can be found in the [list of default association types](link-to-default-association-types) or retrieved via the [associations API](link-to-associations-api).


## Retrieve Deals

Deals can be retrieved individually or in batches.

* **Individual Deal:** `GET /crm/v3/objects/deals/{dealId}`
* **List of Deals:** `GET /crm/v3/objects/deals`
* **Batch Read:** `POST /crm/v3/objects/deals/batch/read`

**Query Parameters (for individual and list retrieval):**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `associations`: Comma-separated list of associated objects to retrieve IDs for.

**Batch Read Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `inputs`: An array of objects, each containing an `id` (record ID or custom unique identifier).
* `idProperty`: (Optional) The name of a custom unique identifier property to use for retrieval (defaults to `hs_object_id`).


**Example Batch Read Request Body (using record IDs):**

```json
{
  "properties": ["dealname", "dealstage", "pipeline"],
  "inputs": [
    { "id": "7891023" },
    { "id": "987654" }
  ]
}
```

**Example Batch Read Request Body (using a custom unique identifier property):**

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

**Note:** The batch read endpoint cannot retrieve associations. Use the [associations API](link-to-associations-api) for batch association retrieval.


## Update Deals

Deals can be updated individually or in batches.

* **Individual Deal:** `PATCH /crm/v3/objects/deals/{dealId}`
* **Batch Update:** `POST /crm/v3/objects/deals/batch/update`


## Associate Existing Deals

Associate a deal with other records or activities using: `PUT /crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`.  Retrieve `associationTypeId` from the [list of default values](link-to-default-association-types) or via a `GET` request to `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`.  Learn more in the [associations API](link-to-associations-api) documentation.


## Remove an Association

Remove an association using: `DELETE /crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`.


## Pin an Activity

Pin an activity to a deal using the `hs_pinned_engagement_id` property (containing the activity ID from the [engagements APIs](link-to-engagements-api)).  Only one activity can be pinned per deal, and the activity must already be associated with the deal.


## Delete Deals

Deals can be deleted individually or in batches (sent to the recycling bin).

* **Individual Deal:** `DELETE /crm/v3/objects/deals/{dealId}`

Batch delete information can be found on the [Endpoints](link-to-endpoints-tab) tab.  Deleted deals can be restored within HubSpot.


**Remember to replace placeholder IDs and values with your actual data.**  All links marked `link-to-XXX` should be replaced with the actual URLs to the relevant HubSpot documentation pages.
