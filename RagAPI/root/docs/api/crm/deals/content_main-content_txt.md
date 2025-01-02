# HubSpot CRM API: Deals

This document details the HubSpot CRM API endpoints for managing deals. Deals represent transactions with contacts or companies, tracked through pipeline stages until won or lost.  These endpoints allow creation, management, and synchronization of deal data between HubSpot and other systems.

## Understanding the CRM (Refer to [Understanding the CRM guide](link_to_guide))

Before using these APIs, familiarize yourself with HubSpot's CRM concepts: objects, records, properties, and associations.


## 1. Create Deals

**Endpoint:** `POST /crm/v3/objects/deals`

**Request Body:**  JSON

The request body must include a `properties` object containing deal details.  You can optionally include an `associations` object to link the new deal with existing contacts, companies, or activities.

**Required Properties:**

* `dealname`: (String) Name of the deal.
* `dealstage`: (String)  Internal ID of the deal stage.  Retrieve IDs from your [deal pipeline settings](link_to_settings).
* `pipeline`: (String, Optional) Internal ID of the pipeline. If omitted, the default pipeline is used.  Retrieve IDs from your [deal pipeline settings](link_to_settings).

**Optional Properties:** (See `/crm/v3/properties/deals` GET request for a complete list)

* `amount`: (Number) Deal amount.
* `closedate`: (DateTime) Expected closing date.
* `hubspot_owner_id`: (Number) ID of the deal owner.

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

**Response:**  JSON containing the newly created deal's details, including its ID.


## 2. Retrieve Deals

**Individual Deal:**

**Endpoint:** `GET /crm/v3/objects/deals/{dealId}`

**Query Parameters:**

* `properties`: (String) Comma-separated list of properties to return.
* `propertiesWithHistory`: (String) Comma-separated list of properties to return, including historical values.
* `associations`: (String) Comma-separated list of associated objects to retrieve IDs for.

**Example Request:** `GET /crm/v3/objects/deals/123?properties=dealname,dealstage`


**All Deals:**

**Endpoint:** `GET /crm/v3/objects/deals`

**Query Parameters:**  Same as individual deal retrieval.

**Batch Retrieval:**

**Endpoint:** `POST /crm/v3/objects/deals/batch/read`

**Request Body:** JSON

```json
{
  "properties": ["dealname", "dealstage", "pipeline"],
  "inputs": [
    { "id": "7891023" },
    { "id": "987654" }
  ]
}
```

* `properties`: (Array of Strings) List of properties to return.
* `inputs`: (Array of Objects) Array of IDs.  Uses `hs_object_id` by default, or specify `idProperty` for a custom identifier.
* `idProperty`: (String, Optional) Name of the custom unique identifier property.

**Response:** JSON containing an array of deals.  The batch endpoint does not return associations.



## 3. Update Deals

**Individual Deal:**

**Endpoint:** `PATCH /crm/v3/objects/deals/{dealId}`

**Request Body:** JSON containing the properties to update.

**Example:**

```json
{
  "properties": {
    "dealstage": "closedwon"
  }
}
```

**Batch Update:**

**Endpoint:** `POST /crm/v3/objects/deals/batch/update`

**Request Body:** JSON containing an array of updates.  Each update specifies the deal ID and properties to modify.  (Details omitted for brevity, but similar structure to batch read).

## 4. Associate Existing Deals

**Endpoint:** `PUT /crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

* `{dealId}`: ID of the deal.
* `{toObjectType}`: Type of the associated object (e.g., contacts, companies).
* `{toObjectId}`: ID of the associated object.
* `{associationTypeId}`: ID of the association type.  Retrieve from [default list](link_to_list) or `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels` GET request.


## 5. Remove Association

**Endpoint:** `DELETE /crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

Parameters are the same as for associating deals.

## 6. Pin an Activity

**Endpoint:** `PATCH /crm/v3/objects/deals/{dealId}`

Include `hs_pinned_engagement_id` in the request body with the activity ID to pin.


## 7. Delete Deals

**Individual Deal:**

**Endpoint:** `DELETE /crm/v3/objects/deals/{dealId}`

**Batch Delete:** (Details omitted, refer to the original document's "Endpoints" tab)


**Note:**  Replace placeholder links (`link_to_guide`, `link_to_settings`, `link_to_list`) with actual links from the HubSpot documentation.  Also, consider adding error handling and response codes to each section for a more complete API reference.
