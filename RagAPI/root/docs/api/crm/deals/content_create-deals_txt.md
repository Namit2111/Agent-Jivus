# HubSpot CRM API: Deals

This document describes the HubSpot CRM API endpoints for managing deals. Deals represent transactions with contacts or companies, tracked through pipeline stages until won or lost.  These endpoints allow creating, managing, and syncing deal data between HubSpot and other systems.

## Understanding the CRM (Prerequisite)

Before using these APIs, familiarize yourself with HubSpot's [Understanding the CRM](<link_to_hubspot_crm_guide>) guide. This guide explains objects, records, properties, and associations within the HubSpot CRM.  Also, learn how to [manage your CRM database](<link_to_hubspot_crm_management>).


## API Endpoints

All endpoints are prefixed with `/crm/v3/objects/deals`.  Replace `{dealId}` with the actual deal ID.


### 1. Create Deals

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/deals`

**Request Body:** JSON

The request body includes a `properties` object containing deal data and an optional `associations` object to link the deal with existing records or activities.

**Required Properties:**

* `dealname` (string): Name of the deal.
* `dealstage` (string): Internal ID of the deal stage.
* `pipeline` (string, optional): Internal ID of the pipeline. If omitted, the default pipeline is used.  (Find IDs in your deal pipeline settings.)

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

**Response:** JSON (includes the newly created deal's ID and properties)


### 2. Retrieve Deals

**Method:** `GET` (single deal) or `GET` (all deals) or `POST` (batch)

**Endpoints:**

* **Single Deal:** `/crm/v3/objects/deals/{dealId}`
* **All Deals:** `/crm/v3/objects/deals`
* **Batch Read:** `/crm/v3/objects/deals/batch/read`

**Query Parameters (for GET requests):**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return with history.
* `associations`: Comma-separated list of associated objects to retrieve IDs for.

**Batch Read Request Body (POST):**

```json
{
  "properties": ["dealname", "dealstage", "pipeline"],
  "inputs": [
    { "id": "7891023" },
    { "id": "987654" }
  ]
}
```

Or, using a custom unique identifier property:

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

**Response:** JSON (deal data or array of deal data)


### 3. Update Deals

**Method:** `PATCH` (single deal) or `POST` (batch)

**Endpoints:**

* **Single Deal:** `/crm/v3/objects/deals/{dealId}`
* **Batch Update:** `/crm/v3/objects/deals/batch/update`

**Request Body (PATCH - single deal):** JSON containing properties to update.

**Request Body (POST - batch update):** JSON array of deal updates (specify IDs and properties to update).

**Response:** JSON (updated deal data or array of updated deal data).


### 4. Associate Existing Deals

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

* `{toObjectType}`: Type of object to associate (e.g., `contacts`, `companies`).
* `{toObjectId}`: ID of the object to associate.
* `{associationTypeId}`: ID of the association type.  (See default IDs or use the Associations API to retrieve custom type IDs).

**Response:**  Confirmation of association.


### 5. Remove Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Response:** Confirmation of association removal.


### 6. Pin an Activity

**Method:** `PATCH` (update existing deal) or `POST` (create deal and pin simultaneously)

**Endpoint:** `/crm/v3/objects/deals/{dealId}` (PATCH) or `/crm/v3/objects/deals` (POST)


**Request Body (PATCH):**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789 
  }
}
```

**Request Body (POST - Create and Pin):**

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
      "to": {
        "id": 123456789
      },
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

**Response:**  Confirmation of pinned activity.


### 7. Delete Deals

**Method:** `DELETE` (single deal)

**Endpoint:** `/crm/v3/objects/deals/{dealId}`

**Response:** Confirmation of deletion (moves deal to recycling bin).


##  Additional Notes

* **Error Handling:**  The API will return appropriate HTTP status codes and error messages.
* **Authentication:** You need a HubSpot API key for authentication.
* **Rate Limiting:**  Be mindful of HubSpot's API rate limits.
* **Pagination:** For large datasets, use pagination parameters as provided in the HubSpot API documentation.
* **Batch Operations:** Batch endpoints improve efficiency when working with multiple deals.
* **Associations API:**  Consult the HubSpot [Associations API](<link_to_hubspot_associations_api>) documentation for detailed information on managing associations.
* **Custom Properties:** The ability to create and utilize custom properties adds considerable flexibility to the deal management process. Remember to obtain their internal IDs for API calls.

This documentation provides a concise overview.  Refer to the official HubSpot API documentation for the most up-to-date and comprehensive information. Remember to replace placeholder IDs and values with your actual data.
