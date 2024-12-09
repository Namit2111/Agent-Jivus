# HubSpot CRM API: Deals

This document details the HubSpot CRM API endpoints for managing deals.  Deals in HubSpot represent transactions with contacts or companies, tracked through sales pipelines until won or lost.  These endpoints allow for creating, managing, and syncing deal data between HubSpot and external systems.

For a broader understanding of objects, records, properties, and associations within the HubSpot CRM API, refer to the [Understanding the CRM](link-to-understanding-crm-guide) guide. For general CRM database management, see [Managing your CRM database](link-to-crm-database-management).


## Create Deals

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/deals`

Create new deals by sending a `POST` request to the specified endpoint. The request body should include a `properties` object containing deal data and optionally an `associations` object to link the new deal with existing records (contacts, companies) or activities (meetings, notes).

**Required Properties:**

* `dealname`: Deal name.
* `dealstage`: Deal stage (use internal ID, see note below).
* `pipeline`: Pipeline (use internal ID, use default if omitted).

**Optional Properties:**  (See [Default HubSpot Deal Properties](link-to-default-properties) and information on [Creating Custom Properties](link-to-creating-custom-properties)).  You can retrieve all available properties via a `GET` request to `/crm/v3/properties/deals`.  Learn more about the [Properties API](link-to-properties-api).

**Note:** Use the internal ID for deal stages and pipelines.  These IDs are found in your [deal pipeline settings](link-to-deal-pipeline-settings).


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

**`associations` Object Parameters:**

| Parameter       | Description                                                                                             |
|-----------------|---------------------------------------------------------------------------------------------------------|
| `to.id`         | ID of the record or activity to associate.                                                             |
| `types`         | Array of association types.  Each type includes `associationCategory` and `associationTypeId`.       |
| `associationCategory` | Typically "HUBSPOT_DEFINED".                                                                         |
| `associationTypeId` | ID specifying the association type.  See [default association type IDs](link-to-association-type-ids) or use the [Associations API](link-to-associations-api) for custom types. |


## Retrieve Deals

Deals can be retrieved individually or in batches.

**Retrieve Individual Deal:**

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/deals/{dealId}`

**Retrieve All Deals:**

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/deals`

**Query Parameters (for both GET endpoints):**

| Parameter           | Description                                                                                                         |
|----------------------|---------------------------------------------------------------------------------------------------------------------|
| `properties`         | Comma-separated list of properties to return.  Missing properties are omitted from the response.                      |
| `propertiesWithHistory` | Comma-separated list of properties to return, including historical values. Missing properties are omitted.          |
| `associations`       | Comma-separated list of associated objects to retrieve IDs for.  Non-existent associations are omitted.  See [Associations API](link-to-associations-api). |


**Batch Retrieve Deals:**

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/deals/batch/read`

Retrieves deals in batches using record IDs (`hs_object_id`) or a custom unique identifier property.  This endpoint does *not* retrieve associations.  Use the [Associations API](link-to-associations-api) for batch association retrieval.

**Request Body (Record ID):**

```json
{
  "properties": ["dealname", "dealstage", "pipeline"],
  "inputs": [
    { "id": "7891023" },
    { "id": "987654" }
  ]
}
```

**Request Body (Custom Unique Identifier):**

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


**Request Body (with historical values):**

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

Deals can be updated individually or in batches. Use the record ID or a custom unique identifier property.

**Update Individual Deal:**

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/deals/{dealId}`


**Batch Update Deals:**

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/deals/batch/update`  (Details omitted for brevity; refer to HubSpot documentation)


## Associate/Disassociate Deals

**Associate:**

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Disassociate:**

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


## Pin an Activity

Pin an activity to a deal record using the `hs_pinned_engagement_id` property (requires the activity ID from the [Engagements APIs](link-to-engagements-api)). Only one activity can be pinned per deal.  The activity must already be associated with the deal.

**Example Request Body (PATCH):**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```

**Example Request Body (POST, create and pin simultaneously):**

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

Deals can be deleted individually or in batches (sent to the recycling bin; can be restored later).

**Delete Individual Deal:**

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/deals/{dealId}`

**Batch Delete:** (Details omitted for brevity; refer to HubSpot documentation's "Endpoints" tab).  See [Restoring Deals in HubSpot](link-to-restore-deals)


**Remember to replace placeholder values (e.g., `{dealId}`, IDs, etc.) with actual values.**  All links are placeholders and should be replaced with actual links to the relevant HubSpot documentation.
