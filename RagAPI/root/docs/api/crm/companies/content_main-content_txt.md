# HubSpot CRM API: Companies

This document details the HubSpot CRM API endpoints for managing companies.  Companies in HubSpot store information about organizations interacting with your business.  These endpoints allow creation, management, and synchronization of company data between HubSpot and other systems.

## Understanding the CRM

For a comprehensive understanding of objects, records, properties, and associations within the HubSpot CRM API, refer to the [Understanding the CRM guide](link-to-understanding-crm-guide).  For general CRM database management, see [how to manage your CRM database](link-to-crm-database-management).


## API Endpoints

All endpoints below use the `/crm/v3/objects/companies` base path unless otherwise specified.  Replace `{companyId}` with the actual company ID.

### 1. Create Companies

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/companies`

**Request Body:** JSON

The request body must include a `properties` object containing company details.  At least one of `name` or `domain` is required.  `domain` is strongly recommended as the primary unique identifier to prevent duplicates.  Multiple domains can be added using the `hs_additional_domains` field (e.g., `"hs_additional_domains": "domain.com;domain2.com"`).  You can also include an `associations` object to associate the new company with existing records or activities.

**Example Request (with associations):**

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
      "to": { "id": 101 },
      "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 280 } ]
    },
    {
      "to": { "id": 556677 },
      "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 185 } ]
    }
  ]
}
```

**Response:** JSON containing the newly created company's data, including its ID.

**Note on `lifecyclestage`:** If included, use the internal name (e.g., "subscriber", "marketingqualifiedlead") for default stages or the numeric ID for custom stages.


### 2. Retrieve Companies

**Method:** `GET` (individual) or `GET` (list) or `POST` (batch)

**Endpoint:**
* Individual: `/crm/v3/objects/companies/{companyId}`
* List: `/crm/v3/objects/companies`
* Batch: `/crm/v3/objects/companies/batch/read`

**Query Parameters (GET requests):**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `associations`: Comma-separated list of associated objects to retrieve IDs for.

**Request Body (POST - batch):** JSON.  Includes `properties` (or `propertiesWithHistory`), `inputs` (array of `{id}` objects), and optionally `idProperty` (for custom unique identifier).

**Example Request (batch, by record ID):**

```json
{
  "properties": ["name", "domain"],
  "inputs": [ { "id": "56789" }, { "id": "23456" } ]
}
```

**Example Request (batch, by custom unique property):**

```json
{
  "properties": ["name", "domain"],
  "idProperty": "uniquepropertyexample",
  "inputs": [ { "id": "abc" }, { "id": "def" } ]
}
```

**Response:** JSON.  For individual retrieval, the company's data. For list retrieval, an array of company data. For batch retrieval, an array of company data corresponding to the input IDs.


### 3. Update Companies

**Method:** `PATCH` (individual)

**Endpoint:** `/crm/v3/objects/companies/{companyId}`

**Request Body:** JSON containing the properties to update.

**Note on `lifecyclestage`:** Updates can only move the stage forward in the order. To move backward, clear the existing value first (manually, via workflow, or integration).


### 4. Associate Existing Companies

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Parameters:**

* `{toObjectType}`: Type of object to associate (e.g., "contacts").
* `{toObjectId}`: ID of the object to associate.
* `{associationTypeId}`: ID of the association type (see default list or use the Associations API).

### 5. Remove Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Parameters:** Same as Associate Existing Companies.


### 6. Pin an Activity

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/companies/{companyId}`

**Request Body:** JSON including `"properties": { "hs_pinned_engagement_id": <activity_id> }`


### 7. Delete Companies

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/companies/{companyId}`

**(Batch deletion is not detailed here but can be found in the reference documentation.)**


##  Associations API

Further details on the Associations API, including default association type IDs and how to retrieve custom association types, are available at [link-to-associations-api].


## Properties API

For information on available company properties and how to create custom properties, see the [Properties API documentation](link-to-properties-api).

## Engagements APIs

Information on retrieving activity IDs for pinning can be found in the [Engagements APIs documentation](link-to-engagements-api).

Remember to replace placeholders like `{companyId}`, `{toObjectType}`, `{toObjectId}`, and `{associationTypeId}` with their respective values.  Always refer to the official HubSpot API documentation for the most up-to-date information.
