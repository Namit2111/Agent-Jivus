# HubSpot CRM API: Deals

This document details the HubSpot CRM API endpoints for managing deals.  Deals represent transactions with contacts or companies, tracked through pipeline stages until won or lost.  These endpoints allow creation, management, and synchronization of deal data between HubSpot and other systems.

## Understanding the CRM Guide

For a comprehensive understanding of objects, records, properties, and associations within the HubSpot CRM API, refer to the [Understanding the CRM](<link_to_understanding_crm_guide>) guide.  Information on managing your CRM database can be found [here](<link_to_crm_database_management>).


## Endpoints

All endpoints are under the `/crm/v3/objects/deals` base path unless otherwise specified.


### 1. Create Deals

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/deals`

**Request Body:** JSON

This endpoint creates new deals.  The request body must include a `properties` object containing deal data. An optional `associations` object can associate the new deal with existing records (contacts, companies) or activities (meetings, notes).

**Required Properties:**

* `dealname` (string): The name of the deal.
* `dealstage` (string): The ID of the deal stage.  Use the internal ID, not the display name.
* `pipeline` (string, optional): The ID of the pipeline.  If omitted, the default pipeline is used.  Use the internal ID, not the display name.


**Example Request (with associations):**

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

**Response:** JSON (including the newly created deal's ID and properties)


**Getting Deal Stage and Pipeline IDs:** Find these IDs in your [deal pipeline settings](<link_to_deal_pipeline_settings>).


**Available Properties:** Retrieve all available properties with a `GET` request to `/crm/v3/properties/deals`.  Learn more about the [properties API](<link_to_properties_api>).



### 2. Retrieve Deals

**Method:** `GET` (individual), `GET` (list), `POST` (batch)

**Endpoints:**

* **Individual Deal:** `/crm/v3/objects/deals/{dealId}`
* **List of Deals:** `/crm/v3/objects/deals`
* **Batch Read:** `/crm/v3/objects/deals/batch/read`

**Query Parameters (for GET requests):**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `associations`: Comma-separated list of associated objects to retrieve IDs for.


**Batch Read Request Body (JSON):**

This endpoint allows retrieving deals by record ID (`hs_object_id`) or a custom unique identifier property.

* **By Record ID:**

```json
{
  "properties": ["dealname", "dealstage", "pipeline"],
  "inputs": [
    { "id": "7891023" },
    { "id": "987654" }
  ]
}
```

* **By Custom Unique Identifier Property:**

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

**Response:** JSON (containing the requested deal(s) and their properties)


### 3. Update Deals

**Method:** `PATCH` (individual), `POST` (batch)

**Endpoints:**

* **Individual Deal:** `/crm/v3/objects/deals/{dealId}`
* **Batch Update:** `/crm/v3/objects/deals/batch/update`

**Request Body (JSON):**  Contains the properties to update.

**Example (PATCH individual):**

```json
{
  "properties": {
    "dealstage": "closedwon"
  }
}
```

**Batch update requires a specific format in the request body, which is not detailed in the provided text but would be an array of objects, each object containing the deal ID and properties to update.**

**Response:** JSON (confirmation or updated deal data)


### 4. Associate Existing Deals

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

Associates a deal with other CRM records or activities.  `associationTypeId` can be found in the list of default values or retrieved via the [associations API](<link_to_associations_api>).

### 5. Remove Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

Removes an association between a deal and a record or activity.


### 6. Pin an Activity

**Method:** `PATCH` (or included in a `POST` to create a deal)

**Endpoint:** `/crm/v3/objects/deals/{dealId}` (or `/crm/v3/objects/deals`)

Uses the `hs_pinned_engagement_id` property to pin an activity to the deal. The activity ID can be retrieved via the [engagements APIs](<link_to_engagements_api>).


### 7. Delete Deals

**Method:** `DELETE` (individual),  **(Batch delete endpoint not specified in the provided text)**

**Endpoint:** `/crm/v3/objects/deals/{dealId}`

Deletes a deal (moves it to the recycling bin).


**Note:** Replace `{dealId}`, `{toObjectType}`, `{toObjectId}`, and `{associationTypeId}` with the appropriate values.  All IDs should be internal HubSpot IDs.  Links within brackets `<...>` should be replaced with the actual URLs from the HubSpot documentation.
