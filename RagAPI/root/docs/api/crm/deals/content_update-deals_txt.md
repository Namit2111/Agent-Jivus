# HubSpot CRM API: Deals

This document details the HubSpot CRM API endpoints for managing deals.  Deals represent transactions with contacts or companies, tracked through sales pipelines.  These endpoints allow creation, management, and synchronization of deal data.

## Understanding the CRM

For a comprehensive understanding of HubSpot's objects, records, properties, and associations APIs, refer to the [Understanding the CRM](link_to_understanding_crm_guide) guide.  Information on managing your CRM database can be found [here](link_to_crm_database_management).


## API Endpoints

All endpoints are under the `/crm/v3/objects/deals` base path unless otherwise specified.  Replace `{dealId}` with the actual deal ID.

**Note:**  Internal IDs (returned by the API) are required for deal stages and pipelines.  Find these in your deal pipeline settings.

### 1. Create Deals

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/deals`

**Request Body (JSON):**

This endpoint requires a `properties` object containing deal details and an optional `associations` object to link the deal with existing records or activities.

```json
{
  "properties": {
    "amount": "1500.00",
    "closedate": "2019-12-07T16:50:06.678Z",
    "dealname": "New deal",
    "pipeline": "default",  // Or pipeline ID
    "dealstage": "contractsent", // Or deal stage ID
    "hubspot_owner_id": "910901"
  },
  "associations": [
    {
      "to": {
        "id": 201 // Contact ID
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 5 // Association type ID (see below)
        }
      ]
    },
    {
      "to": {
        "id": 301 // Company ID
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 3 // Association type ID
        }
      ]
    }
  ]
}
```

**Required Properties:** `dealname`, `dealstage`, `pipeline` (if multiple pipelines exist).

**Associations:**

| Parameter     | Description                                                                 |
|---------------|-----------------------------------------------------------------------------|
| `to.id`       | ID of the record or activity to associate.                               |
| `types`       | Array of association types.  `associationCategory` and `associationTypeId` are required.  See [default association type IDs](link_to_default_association_types) or use the associations API to retrieve custom types. |


### 2. Retrieve Deals

**a) Individual Deal:**

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/deals/{dealId}`

**Query Parameters:**

| Parameter           | Description                                                                          |
|----------------------|--------------------------------------------------------------------------------------|
| `properties`         | Comma-separated list of properties to return.                                         |
| `propertiesWithHistory` | Comma-separated list of properties to return, including historical values.            |
| `associations`       | Comma-separated list of associated objects to retrieve IDs for.                       |

**b) List of Deals:**

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/deals`

**Query Parameters:** Same as individual deal retrieval.

**c) Batch Deal Retrieval:**

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/deals/batch/read`

**Request Body (JSON):**

```json
{
  "properties": ["dealname", "dealstage", "pipeline"],
  "inputs": [
    { "id": "7891023" }, // Deal ID or custom ID if idProperty is specified
    { "id": "987654" }
  ],
  "idProperty": "uniqueordernumber" // Optional: Use a custom unique identifier property
}
```

This endpoint does not support retrieving associations.


### 3. Update Deals

**a) Individual Deal:**

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/deals/{dealId}`

**Request Body (JSON):**  Only include properties to be updated.

**b) Batch Deal Update:**

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/deals/batch/update`

**Request Body (JSON):**  Array of updates, each with identifiers and properties to update.


### 4. Associate Existing Deals

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

* `{toObjectType}`: Object type (e.g., `contacts`, `companies`).
* `{toObjectId}`: ID of the record or activity.
* `{associationTypeId}`: Association type ID (from default list or associations API).


### 5. Remove Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


### 6. Pin an Activity

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/deals/{dealId}`

**Request Body (JSON):**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789 // Activity ID
  }
}
```

You can also pin during deal creation using the `hs_pinned_engagement_id` property and associations.


### 7. Delete Deals

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/deals/{dealId}`


**(Batch delete is mentioned but details are not provided in the source text.)**


##  Error Handling

The API responses will include standard HTTP status codes and error messages in the body to indicate success or failure of the requests.  Refer to HubSpot's API documentation for detailed error handling information.


This markdown provides a structured overview. Remember to replace placeholder links (e.g., `link_to_understanding_crm_guide`) with the actual URLs from the HubSpot documentation.  Also note the lack of response examples -  add those from the HubSpot docs for completeness.
