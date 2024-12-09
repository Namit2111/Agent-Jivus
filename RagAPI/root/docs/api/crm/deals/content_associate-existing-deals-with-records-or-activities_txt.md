# HubSpot CRM API: Deals

This document details the HubSpot CRM API endpoints for managing deals. Deals in HubSpot represent transactions with contacts or companies, tracked through pipeline stages until won or lost.  These endpoints allow for creation, management, and synchronization of deal data between HubSpot and other systems.

For a broader understanding of objects, records, properties, and associations APIs, refer to the [Understanding the CRM guide](<replace_with_link>). For general CRM database management, see [how to manage your CRM database](<replace_with_link>).


## Create Deals

Use a `POST` request to `/crm/v3/objects/deals` to create new deals.  The request body should include a `properties` object containing deal data and optionally an `associations` object to link the deal with existing records (contacts, companies) or activities (meetings, notes).

**Required Properties:**

* `dealname`: Name of the deal.
* `dealstage`: Stage of the deal (use internal ID, see note below).
* `pipeline`: Pipeline the deal belongs to (use internal ID, defaults to the primary pipeline if omitted).

**Note:** Use the internal ID for deal stages and pipelines. These IDs are found in your [deal pipeline settings](<replace_with_link>).  The API returns these IDs when retrieving deals.

**Example Request Body:**

```json
{
  "properties": {
    "amount": "1500.00",
    "closedate": "2019-12-07T16:50:06.678Z",
    "dealname": "New deal",
    "pipeline": "default",  // Replace "default" with the actual pipeline ID
    "dealstage": "contractsent", // Replace "contractsent" with the actual stage ID
    "hubspot_owner_id": "910901"
  }
}
```

### Associations

The `associations` object allows associating the new deal with existing records or activities.

**Example Request Body (with Associations):**

```json
{
  "properties": {
    "amount": "1500.00",
    "closedate": "2019-12-07T16:50:06.678Z",
    "dealname": "New deal",
    "pipeline": "default", // Replace "default" with the actual pipeline ID
    "dealstage": "contractsent", // Replace "contractsent" with the actual stage ID
    "hubspot_owner_id": "910901"
  },
  "associations": [
    {
      "to": { "id": 201 }, // ID of the associated record/activity
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 5 // Association type ID (see default IDs or Associations API)
        }
      ]
    },
    {
      "to": { "id": 301 }, // ID of the associated record/activity
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 3 // Association type ID (see default IDs or Associations API)
        }
      ]
    }
  ]
}
```

* **`to.id`**: Unique ID of the record or activity.
* **`types.associationCategory`**:  Category of the association (usually `HUBSPOT_DEFINED`).
* **`types.associationTypeId`**:  Specific type of association.  See [default association type IDs](<replace_with_link>) or use the [Associations API](<replace_with_link>) for custom types.


## Retrieve Deals

Deals can be retrieved individually or in batches.

### Retrieve Individual Deal

Use a `GET` request to `/crm/v3/objects/deals/{dealId}`.

### Retrieve List of Deals

Use a `GET` request to `/crm/v3/objects/deals`.

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.  Missing properties are omitted from the response.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values. Missing properties are omitted from the response.
* `associations`: Comma-separated list of associated objects to retrieve IDs for.  Missing associations are omitted.

### Batch Retrieve Deals

Use a `POST` request to `/crm/v3/objects/deals/batch/read`. This endpoint does *not* retrieve associations. Use the [Associations API](<replace_with_link>) for batch association retrieval.

**Request Body:**

* `properties`: List of properties to return.
* `inputs`: Array of objects, each with an `id` property.  This ID is the record ID (`hs_object_id`) unless `idProperty` is specified.
* `idProperty`: (Optional) Name of a custom unique identifier property to use for retrieving deals instead of the record ID.

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

**Example Request Body (Custom Unique Identifier):**

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

**Example Request Body (with History):**

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

### Update Individual Deal

Use a `PATCH` request to `/crm/v3/objects/deals/{dealId}`. Include only the properties to be updated.

### Batch Update Deals

Use a `POST` request to `/crm/v3/objects/deals/batch/update`.  The request body should contain an array of objects, each specifying the deal ID and properties to update.


## Associate Existing Deals

Use a `PUT` request to `/crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}` to associate a deal with another record or activity. Use the [Associations API](<replace_with_link>) to retrieve `associationTypeId`.


## Remove Association

Use a `DELETE` request to `/crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}` to remove an association.


## Pin an Activity

Pin an activity to a deal record using the `hs_pinned_engagement_id` property (containing the activity ID obtained from the [Engagements APIs](<replace_with_link>)).  Only one activity can be pinned per deal. The activity must already be associated with the deal.

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
    "pipeline": "default", // Replace "default" with the actual pipeline ID
    "dealstage": "contractsent", // Replace "contractsent" with the actual stage ID
    "hs_pinned_engagement_id": 123456789
  },
  "associations": [
    {
      "to": { "id": 123456789 },
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

Deals can be deleted individually or in batches (moved to the recycling bin; see [restore deals](<replace_with_link>) ).

### Delete Individual Deal

Use a `DELETE` request to `/crm/v3/objects/deals/{dealId}`.

### Batch Delete Deals

(See the [Endpoints](<replace_with_link>) tab for information on batch deletion).  Remember to replace placeholders like `<replace_with_link>` with the actual links from the original HubSpot documentation.
