# HubSpot CRM API: Companies

This document details the HubSpot CRM API endpoints for managing companies.  Companies in HubSpot store information about organizations interacting with your business.  These endpoints allow for creating, managing, and syncing company data between HubSpot and other systems.

## Understanding the CRM

For a comprehensive understanding of objects, records, properties, and associations within the HubSpot CRM API, refer to the [Understanding the CRM guide](<Insert Link Here>).  For general CRM database management, see [Managing your CRM database](<Insert Link Here>).


## API Endpoints

All endpoints below are under the `/crm/v3/objects/companies` base path unless otherwise specified.  All examples assume you have the necessary API key and authorization.


### 1. Create Companies

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/companies`

**Request Body (JSON):**

This endpoint requires at least one of the `name` or `domain` properties.  `domain` is the recommended primary unique identifier to prevent duplicates.  Multiple domains can be added using the `hs_additional_domains` property (e.g., `"hs_additional_domains": "domain.com;domain2.com"`).

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
      "to": {
        "id": 101 // ID of associated record (e.g., contact)
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 280 // Association type ID
        }
      ]
    },
    {
      "to": {
        "id": 556677 // ID of associated activity (e.g., email)
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 185 // Association type ID
        }
      ]
    }
  ]
}
```

**Response (JSON):**  A successful response will contain the newly created company's ID and other properties.  The exact structure depends on the requested properties.  Check the HubSpot API documentation for details.


**Lifecycle Stage Note:**  If `lifecyclestage` is included, use the internal name (e.g., `"subscriber"`, `"marketingqualifiedlead"`) for default stages or the numeric ID for custom stages.  Find the ID in your lifecycle stage settings or via the properties API.


### 2. Retrieve Companies

**a) Individual Company:**

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/companies/{companyId}`

**Query Parameters:**

*   `properties`: Comma-separated list of properties to return.
*   `propertiesWithHistory`: Comma-separated list of properties to return with history.
*   `associations`: Comma-separated list of associated objects to retrieve IDs for.

**Example:** `/crm/v3/objects/companies/123?properties=name,domain`


**b) List of Companies:**

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/companies`

**Query Parameters:** Same as above.


**c) Batch Read:**

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/companies/batch/read`

**Request Body (JSON):**

```json
{
  "properties": ["name", "domain"],
  "inputs": [
    { "id": "56789" }, // Record ID or custom ID (if idProperty is specified)
    { "id": "23456" }
  ],
  "idProperty": "uniquepropertyexample" // Optional: Use for custom unique identifier property
}
```

**Response (JSON):** A list of companies matching the provided IDs.


### 3. Update Companies

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/companies/{companyId}`

**Request Body (JSON):**

Include only the properties you want to update.

```json
{
  "properties": {
    "name": "Updated Company Name",
    "city": "New City"
  }
}
```

**Lifecycle Stage Note:** Updating `lifecyclestage` only allows moving *forward* in the stage order. To move backward, clear the existing value first (manually, via workflow, or integration).


### 4. Associate Existing Companies

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

*   `{companyId}`: ID of the company.
*   `{toObjectType}`: Type of object to associate (e.g., `contacts`, `deals`).
*   `{toObjectId}`: ID of the object to associate.
*   `{associationTypeId}`: ID of the association type (see default list or use the associations API).


### 5. Remove an Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


### 6. Pin an Activity

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/companies/{companyId}`

**Request Body (JSON):**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789 // ID of the activity to pin
  }
}
```

You can also pin an activity during company creation using the `hs_pinned_engagement_id` property in the `POST /crm/v3/objects/companies` request.


### 7. Delete Companies

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/companies/{companyId}`

This moves the company to the recycling bin; it can be restored later.  See the reference documentation for batch deletion.


## Properties API

Use the `/crm/v3/properties/companies` endpoint (GET request) to retrieve a list of available company properties.  See the [properties API documentation](<Insert Link Here>) for details.

## Associations API

Use the associations API to manage associations between companies and other objects.  Refer to the [associations API documentation](<Insert Link Here>) for details on association types and management.


This markdown provides a concise overview.  Refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications. Remember to replace `<Insert Link Here>` placeholders with actual links to the relevant HubSpot documentation pages.
