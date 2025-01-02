# HubSpot CRM API: Companies

This document describes the HubSpot CRM API endpoints for managing companies.  Companies in HubSpot store information about organizations interacting with your business.  These endpoints allow creation, management, and synchronization of company data between HubSpot and other systems.

## Understanding the CRM

For a comprehensive understanding of objects, records, properties, and associations within the HubSpot CRM API, refer to the [Understanding the CRM guide](link_to_understanding_crm_guide).  Information on managing your CRM database can be found [here](link_to_managing_crm_database).

## API Endpoints

All endpoints are under the `/crm/v3/objects/companies` base path unless otherwise specified.  Replace `{companyId}` with the actual company ID.

### 1. Create Companies

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/companies`

**Request Body (JSON):**

The request body must include a `properties` object containing company details.  At least one of `name` or `domain` is required.  `domain` is strongly recommended as the primary unique identifier.  Multiple domains can be added using the `hs_additional_domains` field (e.g., `"hs_additional_domains": "domain.com;domain2.com"`).  You can also include an `associations` object to link the new company with existing records or activities.

```json
{
  "properties": {
    "name": "HubSpot",
    "domain": "hubspot.com",
    "city": "Cambridge",
    "industry": "Technology",
    "phone": "555-555-555",
    "state": "Massachusetts",
    "lifecyclestage": "51439524" // Use internal name or ID for lifecycle stage
  },
  "associations": [
    {
      "to": { "id": 101 }, // Existing contact ID
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 280 }] // Association type
    },
    {
      "to": { "id": 556677 }, // Existing email ID
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 185 }] // Association type
    }
  ]
}
```

**Response (JSON):**  A successful response will contain the created company's data, including its ID.  See the HubSpot API documentation for the exact structure.


### 2. Retrieve Companies

**a) Individual Company:**

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/companies/{companyId}`

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `associations`: Comma-separated list of associated objects to retrieve.

**b) List of Companies:**

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/companies`

**Query Parameters:** Same as individual company retrieval.

**c) Batch Retrieval:**

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/companies/batch/read`

**Request Body (JSON):**

```json
{
  "properties": ["name", "domain"],
  "inputs": [
    { "id": "56789" }, // Company ID or custom unique identifier
    { "id": "23456" }
  ],
  "idProperty": "uniquepropertyexample" // Optional: Use if retrieving by custom unique identifier
}
```

**Response (JSON):** An array of company data matching the input IDs.

### 3. Update Companies

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/companies/{companyId}`

**Request Body (JSON):**  An object containing the properties to update.

```json
{
  "properties": {
    "name": "Updated Name",
    "city": "New City"
  }
}
```

**Note:** Updating `lifecyclestage` only allows forward movement in the stage order.


### 4. Associate Existing Companies

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

* `{toObjectType}`: Type of object to associate (e.g., `contacts`, `deals`).
* `{toObjectId}`: ID of the object to associate.
* `{associationTypeId}`: ID of the association type.  Obtain from the default list or the associations API.


### 5. Remove Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


### 6. Pin an Activity

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/companies/{companyId}`

**Request Body (JSON):**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789 // Activity ID
  }
}
```

You can also pin during creation.


### 7. Delete Companies

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/companies/{companyId}`


##  Properties API

Retrieve available company properties using `GET /crm/v3/properties/companies`.  See [properties API documentation](link_to_properties_api) for details.


## Associations API

For more details on associations, including default association type IDs and batch operations, refer to the [associations API documentation](link_to_associations_api).


Remember to replace placeholder IDs and values with your actual data.  Consult the official HubSpot API documentation for the most up-to-date information and detailed response structures.  This markdown provides a concise overview.
