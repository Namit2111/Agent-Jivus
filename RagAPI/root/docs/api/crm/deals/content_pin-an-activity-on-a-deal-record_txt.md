# HubSpot CRM API: Deals

This document details the HubSpot CRM API endpoints for managing deals. Deals in HubSpot represent transactions with contacts or companies, tracked through pipeline stages until won or lost.  This API allows creating, managing, and syncing deal data between HubSpot and other systems.

## Understanding the CRM Guide

For a comprehensive understanding of objects, records, properties, and associations within the HubSpot CRM API, refer to the [Understanding the CRM](link_to_understanding_crm_guide) guide.  Learn how to [manage your CRM database](link_to_crm_database_management) for general information.


## 1. Create Deals

**Endpoint:** `POST /crm/v3/objects/deals`

**Request Body:** JSON

This endpoint creates new deal records.  The request body must include a `properties` object containing deal details.  Optionally, include an `associations` object to link the new deal with existing records (contacts, companies) or activities (meetings, notes).

**Required Properties:**

* `dealname` (string): The name of the deal.
* `dealstage` (string): The stage of the deal (use internal ID, see note below).
* `pipeline` (string, optional): The pipeline the deal belongs to (use internal ID, see note below).  If omitted, the default pipeline is used.


**Example Request Body (with associations):**

```json
{
  "properties": {
    "amount": "1500.00",
    "closedate": "2019-12-07T16:50:06.678Z",
    "dealname": "New deal",
    "pipeline": "default_pipeline_id", // Replace with actual pipeline ID
    "dealstage": "contractsent_id", // Replace with actual deal stage ID
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

**Note:**  Use the internal ID of deal stages and pipelines, which can be found in your [deal pipeline settings](link_to_deal_pipeline_settings).


**Response:** JSON (includes the newly created deal's ID and properties).


## 2. Retrieve Deals

**Individual Deal:**

**Endpoint:** `GET /crm/v3/objects/deals/{dealId}`

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `associations`: Comma-separated list of associated objects to retrieve IDs for.

**Example Request:** `GET /crm/v3/objects/deals/123?properties=dealname,dealstage`


**Batch Deals:**

**Endpoint:** `POST /crm/v3/objects/deals/batch/read`

**Request Body:** JSON

This endpoint retrieves a batch of deals.  Use the `inputs` array to specify deal IDs (using `hs_object_id` or a custom `idProperty`).

**Example Request Body (using record IDs):**

```json
{
  "properties": ["dealname", "dealstage", "pipeline"],
  "inputs": [
    { "id": "7891023" },
    { "id": "987654" }
  ]
}
```

**Example Request Body (using a custom unique identifier property):**

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

**Response:** JSON (array of deals).


## 3. Update Deals

**Individual Deal:**

**Endpoint:** `PATCH /crm/v3/objects/deals/{dealId}`

**Request Body:** JSON (contains properties to update)

**Example Request Body:**

```json
{
  "properties": {
    "dealstage": "closedwon_id" // Replace with actual deal stage ID
  }
}
```

**Batch Deals:**

**Endpoint:** `POST /crm/v3/objects/deals/batch/update`

**Request Body:** JSON (array of deals to update, each with properties to update).


## 4. Associate/Disassociate Deals

**Associate:**

**Endpoint:** `PUT /crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Disassociate:**

**Endpoint:** `DELETE /crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


## 5. Pin an Activity

**Endpoint:** `PATCH /crm/v3/objects/deals/{dealId}`

**Request Body:** JSON (includes `hs_pinned_engagement_id` with the activity ID).

**Example:**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```

## 6. Delete Deals

**Individual Deal:**

**Endpoint:** `DELETE /crm/v3/objects/deals/{dealId}`


**Note:** Deleting a deal moves it to the recycle bin; it can be restored later.  See documentation for batch delete.


##  Additional Resources

* **Properties API:** [link_to_properties_api]
* **Associations API:** [link_to_associations_api]
* **Engagements APIs:** [link_to_engagements_api]


Remember to replace placeholder IDs (e.g., `default_pipeline_id`, `contractsent_id`, `closedwon_id`, etc.) with the actual internal IDs from your HubSpot account.  Always refer to the official HubSpot API documentation for the most up-to-date information and details.
