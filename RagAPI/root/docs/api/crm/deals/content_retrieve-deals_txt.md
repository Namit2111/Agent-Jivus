# HubSpot CRM API: Deals

This document details the HubSpot CRM API endpoints for managing deals. Deals represent transactions with contacts or companies, tracked through pipeline stages until won or lost.  These endpoints allow creation, management, and synchronization of deal data.

## Understanding the CRM

Before using these APIs, familiarize yourself with HubSpot's [CRM object model](link_to_hubspot_crm_object_model_documentation), including objects, records, properties, and associations.  Understanding [how to manage your CRM database](link_to_hubspot_crm_database_management) is also beneficial.

## API Endpoints

All endpoints below are prefixed with `/crm/v3/objects/deals`.  Replace `{dealId}` with the actual deal ID.  Requests require proper authentication (see HubSpot API documentation for details).

### 1. Create Deals (POST)

Creates a new deal.

**Endpoint:** `/crm/v3/objects/deals`

**Request Method:** `POST`

**Request Body (JSON):**

```json
{
  "properties": {
    "amount": "1500.00",
    "closedate": "2019-12-07T16:50:06.678Z",
    "dealname": "New deal",
    "pipeline": "default",  // Use default pipeline if not specified.  Must use internal ID for other pipelines.
    "dealstage": "contractsent", // Must use internal ID.
    "hubspot_owner_id": "910901"
  },
  "associations": [
    {
      "to": { "id": 201 }, // ID of associated contact (example)
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 5 }] // Association type ID. See below.
    },
    {
      "to": { "id": 301 }, // ID of associated company (example)
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 3 }] // Association type ID. See below.
    }
  ]
}
```

**Properties:**

* `amount`: Deal amount (string).
* `closedate`: Closing date (ISO 8601 format).
* `dealname`: Deal name (string, required).
* `pipeline`: Pipeline ID (string, required if multiple pipelines exist; use internal ID).
* `dealstage`: Deal stage ID (string, required; use internal ID).
* `hubspot_owner_id`: ID of the owner (string).
* **Other properties:** See [default HubSpot deal properties](link_to_hubspot_default_properties) and [creating custom properties](link_to_hubspot_custom_properties).

**Associations:**  Use the `associations` array to link the deal to existing contacts, companies, or activities.  `associationTypeId` values are found in [this list](link_to_hubspot_association_type_ids) of default types or obtained via the [associations API](link_to_hubspot_associations_api).

**Response (JSON):**  A JSON object representing the newly created deal, including its ID.

### 2. Retrieve Deals (GET & POST)

Retrieves deals individually or in batches.

**a) Individual Deal (GET):**

**Endpoint:** `/crm/v3/objects/deals/{dealId}`

**Request Method:** `GET`

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return with history.
* `associations`: Comma-separated list of associated objects to retrieve.


**b) List of Deals (GET):**

**Endpoint:** `/crm/v3/objects/deals`

**Request Method:** `GET`

**Query Parameters:** (Same as individual deal retrieval)


**c) Batch Deal Retrieval (POST):**

**Endpoint:** `/crm/v3/objects/deals/batch/read`

**Request Method:** `POST`

**Request Body (JSON):**

```json
{
  "properties": ["dealname", "dealstage", "pipeline"],
  "inputs": [
    { "id": "7891023" }, // deal ID
    { "id": "987654" }  // deal ID
  ],
  "idProperty": "uniqueordernumber" // Optional: Use a custom unique identifier property.
}
```

**Response (JSON):** An array of JSON objects, each representing a retrieved deal.


### 3. Update Deals (PATCH & POST)

Updates deals individually or in batches.

**a) Individual Deal (PATCH):**

**Endpoint:** `/crm/v3/objects/deals/{dealId}`

**Request Method:** `PATCH`

**Request Body (JSON):**  Includes only the properties to update.


**b) Batch Deal Update (POST):**

**Endpoint:** `/crm/v3/objects/deals/batch/update`

**Request Method:** `POST`

**Request Body (JSON):**  An array of objects, each specifying a deal ID and properties to update.


### 4. Associate/Disassociate Deals (PUT & DELETE)

Manages associations between deals and other records/activities.

**a) Associate (PUT):**

**Endpoint:** `/crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Request Method:** `PUT`


**b) Disassociate (DELETE):**

**Endpoint:** `/crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Request Method:** `DELETE`


### 5. Pin an Activity (PATCH)

Pins an activity to a deal record.

**Endpoint:** `/crm/v3/objects/deals/{dealId}`

**Request Method:** `PATCH`

**Request Body (JSON):**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789 // Activity ID
  }
}
```


### 6. Delete Deals (DELETE)

Deletes deals (moves them to the recycle bin).

**Endpoint:** `/crm/v3/objects/deals/{dealId}`

**Request Method:** `DELETE`


## Error Handling

The API will return appropriate HTTP status codes and error messages in the response body to indicate success or failure. Consult the HubSpot API documentation for detailed error codes and handling.


This documentation provides a comprehensive overview.  For detailed specifications, including specific data types and limitations, refer to the official HubSpot API documentation.  Remember to replace placeholder IDs and values with your actual data.
