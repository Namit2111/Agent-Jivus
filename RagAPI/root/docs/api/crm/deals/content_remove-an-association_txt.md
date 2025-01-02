# HubSpot CRM API: Deals

This document details the HubSpot CRM API endpoints for managing deals.  Deals represent transactions with contacts or companies, tracked through sales pipelines.  These endpoints allow creation, management, and synchronization of deal data.

## Understanding the CRM

For a comprehensive understanding of HubSpot's object, record, property, and association APIs, refer to the [Understanding the CRM](<link_to_understanding_crm_guide>) guide.  Learn more about managing your CRM database [here](<link_to_crm_database_management>).


## API Endpoints

All endpoints are under the `/crm/v3/objects/deals` base path unless otherwise specified.

### 1. Create Deals

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/deals`

**Request Body:**  JSON payload containing `properties` and optionally `associations`.

**Properties:** Deal details.  Required properties include `dealname`, `dealstage`, and optionally `pipeline` (defaults to the account's default pipeline).  Internal IDs (not display names) must be used for `dealstage` and `pipeline`.  Retrieve available properties via `/crm/v3/properties/deals` (GET request).

**Associations:** (Optional)  Associates the new deal with existing records (contacts, companies) or activities (meetings, notes).

**Example Request (Create with Associations):**

```json
{
  "properties": {
    "amount": "1500.00",
    "closedate": "2019-12-07T16:50:06.678Z",
    "dealname": "New deal",
    "pipeline": "default",  // Replace 'default' with the actual pipeline ID
    "dealstage": "contractsent", // Replace 'contractsent' with the actual deal stage ID
    "hubspot_owner_id": "910901"
  },
  "associations": [
    {
      "to": { "id": 201 }, // Contact ID
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 5 }]
    },
    {
      "to": { "id": 301 }, // Company ID
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 3 }]
    }
  ]
}
```

**Response:**  JSON object representing the newly created deal, including its ID.


### 2. Retrieve Deals

**Method:** `GET` (individual), `GET` (list), `POST` (batch)

**Endpoint:**
* Individual: `/crm/v3/objects/deals/{dealId}`
* List: `/crm/v3/objects/deals`
* Batch: `/crm/v3/objects/deals/batch/read`

**Query Parameters (Individual & List):**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `associations`: Comma-separated list of associated objects to retrieve IDs for.

**Request Body (Batch):**

* `properties`:  Array of properties to return.
* `inputs`: Array of objects, each with an `id` property representing the deal ID (or custom ID if `idProperty` is specified).
* `idProperty`: (Optional)  Name of a custom unique identifier property to use for retrieving deals instead of the record ID (`hs_object_id`).

**Example Request (Batch with Record IDs):**

```json
{
  "properties": ["dealname", "dealstage", "pipeline"],
  "inputs": [
    { "id": "7891023" },
    { "id": "987654" }
  ]
}
```

**Example Request (Batch with Custom ID Property):**

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

**Response:** JSON object (individual) or array of JSON objects (list or batch), each representing a deal.


### 3. Update Deals

**Method:** `PATCH` (individual), `POST` (batch)

**Endpoint:**
* Individual: `/crm/v3/objects/deals/{dealId}`
* Batch: `/crm/v3/objects/deals/batch/update`

**Request Body (Individual):** JSON payload with properties to update.

**Request Body (Batch):**  Array of objects, each specifying the deal ID (or custom ID) and properties to update.

**Example Request (Individual):**

```json
{
  "properties": {
    "dealstage": "closedwon" // Replace with actual deal stage ID
  }
}
```

**Response:** JSON object representing the updated deal (individual) or an array of success/failure statuses (batch).


### 4. Associate Existing Deals

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

* `{dealId}`: ID of the deal.
* `{toObjectType}`: Type of the object to associate (e.g., `contacts`, `companies`).
* `{toObjectId}`: ID of the object to associate.
* `{associationTypeId}`: ID of the association type.  Retrieve from the [list of default values](<link_to_default_association_types>) or via `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels` (GET).

**Response:** Confirmation of successful association.


### 5. Remove Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/deals/{dealId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Response:** Confirmation of successful removal.


### 6. Pin an Activity

**Method:** `PATCH` (update existing deal), `POST` (create deal with pinned activity)

**Endpoint:**
* Update: `/crm/v3/objects/deals/{dealId}`
* Create: `/crm/v3/objects/deals`

**Request Body:** Include the `hs_pinned_engagement_id` property with the ID of the activity to pin. The activity must already be associated with the deal.

**Example Request (PATCH):**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```

**Response:** JSON object representing the updated deal (PATCH).


### 7. Delete Deals

**Method:** `DELETE` (individual),  [Batch method described elsewhere](<link_to_batch_delete_deals>)

**Endpoint:** `/crm/v3/objects/deals/{dealId}`

**Response:** Confirmation of successful deletion (deal moved to recycling bin).


**Note:** Replace placeholder IDs and values with your actual data.  Remember to handle API errors appropriately.  Consult the official HubSpot API documentation for the most up-to-date information and error codes.
