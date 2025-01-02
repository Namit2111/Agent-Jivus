# HubSpot CRM API: Deals

This document details the HubSpot CRM API endpoints for managing deals.  Deals represent transactions with contacts or companies, tracked through pipeline stages until won or lost.  These endpoints allow creating, managing, and syncing deal data.

## Understanding the CRM (Recommended Reading)

Before using these APIs, review the [HubSpot Understanding the CRM guide](link_to_guide_here). This guide explains objects, records, properties, and associations within the HubSpot CRM.  Also, learn how to [manage your CRM database](link_to_database_management_here).


## 1. Create Deals

**Endpoint:** `POST /crm/v3/objects/deals`

**Method:** `POST`

**Request Body:** JSON containing `properties` and optionally `associations`.

**Properties:** Deal details are stored in properties.  There are default HubSpot properties and the ability to create custom ones.  For creation, these are required: `dealname`, `dealstage`, and `pipeline` (if multiple pipelines exist; otherwise, the default pipeline is used).  Retrieve all available properties using: `GET /crm/v3/properties/deals`.

**Example Request Body (with properties only):**

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

**Associations:**  Associate the new deal with existing records (contacts, companies) or activities (meetings, notes) using the `associations` object.

**Example Request Body (with properties and associations):**

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

**Note:** Use internal IDs for deal stages and pipelines (found in deal pipeline settings).


## 2. Retrieve Deals

**Individual Deal:**

**Endpoint:** `GET /crm/v3/objects/deals/{dealId}`

**Method:** `GET`

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `associations`: Comma-separated list of associated objects to retrieve IDs for.


**All Deals:**

**Endpoint:** `GET /crm/v3/objects/deals`

**Method:** `GET`

**Query Parameters:**  Same as individual deal retrieval.


**Batch Deal Retrieval:**

**Endpoint:** `POST /crm/v3/objects/deals/batch/read`

**Method:** `POST`

**Request Body:**

```json
{
  "properties": ["dealname", "dealstage", "pipeline"],
  "inputs": [
    { "id": "7891023" },
    { "id": "987654" }
  ]
}
```

* `properties`:  List of properties to return.
* `inputs`: Array of deal IDs.  Use `idProperty` for custom unique identifier properties.  (e.g., `"idProperty": "uniqueordernumber"`).  If not specified, `id` refers to `hs_object_id`.

**Example with Custom Unique Identifier:**

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

**Note:** Batch retrieval cannot retrieve associations.


## 3. Update Deals

**Individual Deal:**

**Endpoint:** `PATCH /crm/v3/objects/deals/{dealId}`

**Method:** `PATCH`

**Request Body:** JSON containing properties to update.


**Batch Deal Update:**

**Endpoint:** `POST /crm/v3/objects/deals/batch/update`

**Method:** `POST`

**Request Body:**  Array of deals to update, each with identifiers and properties to update.


## 4. Associate Existing Deals

**Endpoint:** `PUT /crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `PUT`

Retrieve `associationTypeId` from the list of default values or via `GET /crm/v4/associations/{fromObjectType}/{toObjectType}/labels`.


## 5. Remove Association

**Endpoint:** `DELETE /crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `DELETE`


## 6. Pin an Activity

**Update existing deal:**

**Endpoint:** `PATCH /crm/v3/objects/deals/{dealId}`

**Method:** `PATCH`

**Request Body:**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```

**Create and Pin in single request:**

**Endpoint:** `POST /crm/v3/objects/deals`

**Method:** `POST`

**Request Body:** (Example combining creation, association, and pinning)


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


## 7. Delete Deals

**Individual Deal:**

**Endpoint:** `DELETE /crm/v3/objects/deals/{dealId}`

**Method:** `DELETE`

**Batch Deal Deletion:**  Refer to the "Endpoints" tab (link provided in original text) for batch deletion information.


This markdown provides a comprehensive overview of the HubSpot CRM Deals API. Remember to replace placeholder URLs and IDs with your actual values.  Always consult the official HubSpot API documentation for the most up-to-date information.
