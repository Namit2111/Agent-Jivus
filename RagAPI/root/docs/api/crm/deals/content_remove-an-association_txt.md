# HubSpot CRM API: Deals

This document details the HubSpot CRM API endpoints for managing deals. Deals in HubSpot represent transactions with contacts or companies, tracked through sales pipelines until won or lost.  These endpoints allow for creating, managing, and syncing deal data between HubSpot and external systems.

## Understanding the CRM

For a comprehensive understanding of objects, records, properties, and association APIs within the HubSpot CRM, refer to the [Understanding the CRM](<link_to_understanding_crm_guide>) guide.  Learn more about managing your CRM database [here](<link_to_crm_database_management>).

## Create Deals

To create a new deal, send a `POST` request to `/crm/v3/objects/deals`.  The request body should include a `properties` object containing deal data and an optional `associations` object to link the deal with existing records (contacts, companies) or activities (meetings, notes).

**Required Properties:**

* `dealname`: The name of the deal.
* `dealstage`: The stage of the deal in the pipeline (use internal ID).
* `pipeline`: The pipeline the deal belongs to (use internal ID, defaults to the account's default pipeline if omitted).

**Example Request Body (JSON):**

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

To view all available properties, send a `GET` request to `/crm/v3/properties/deals`.  Learn more about the [properties API](<link_to_properties_api>).  **Note:** Use internal IDs for deal stages and pipelines.  Find these IDs in your [deal pipeline settings](<link_to_deal_pipeline_settings>).


## Associations

When creating a deal, associate it with existing records or activities using the `associations` object.

**Example Request Body (JSON):**

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

* **`to.id`**: The ID of the record or activity to associate.
* **`types`**:  An array defining the association type.  `associationCategory` is usually "HUBSPOT_DEFINED".  `associationTypeId` can be found in the [list of default association type IDs](<link_to_association_type_ids>) or retrieved via the [associations API](<link_to_associations_api>).

## Retrieve Deals

Retrieve deals individually or in batches.

* **Individual Deal:** `GET /crm/v3/objects/deals/{dealId}`
* **List of Deals:** `GET /crm/v3/objects/deals`
* **Batch Read:** `POST /crm/v3/objects/deals/batch/read` (can't retrieve associations)

**Query Parameters (for individual and list endpoints):**

* **`properties`**: Comma-separated list of properties to return.
* **`propertiesWithHistory`**: Comma-separated list of properties to return, including historical values.
* **`associations`**: Comma-separated list of associated objects to retrieve IDs for.

**Batch Read Example (JSON - using record ID):**

```json
{
  "properties": ["dealname", "dealstage", "pipeline"],
  "inputs": [
    { "id": "7891023" },
    { "id": "987654" }
  ]
}
```

**Batch Read Example (JSON - using a custom unique identifier property):**

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

Update deals individually or in batches.

* **Individual Deal:** `PATCH /crm/v3/objects/deals/{dealId}`
* **Batch Update:** `POST /crm/v3/objects/deals/batch/update`

## Associate Existing Deals

Associate a deal with other records or activities: `PUT /crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`.  Get `associationTypeId` from the [list of default values](<link_to_association_type_ids>) or via `GET /crm/v4/associations/{fromObjectType}/{toObjectType}/labels`.  Learn more in the [associations API](<link_to_associations_api>).


## Remove an Association

Remove an association: `DELETE /crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`.

## Pin an Activity

Pin an activity to a deal record by including `hs_pinned_engagement_id` (activity ID from [engagements APIs](<link_to_engagements_api>)) in a `PATCH` or `POST` request.  Only one activity can be pinned per record.

**Example Request Body (JSON - PATCH):**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```

## Delete Deals

Delete deals individually or in batches (moves them to the recycling bin):

* **Individual Deal:** `DELETE /crm/v3/objects/deals/{dealId}`
* **Batch Delete:**  (See the "Endpoints" tab of this article for batch deletion details).  Deals can be restored within HubSpot.


Remember to replace placeholder IDs and values with your actual data.  Links within the square brackets `< >` need to be replaced with the actual HubSpot documentation URLs.
