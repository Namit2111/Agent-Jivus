# HubSpot CRM API: Companies

This document details the HubSpot CRM API endpoints for managing companies.  Companies in HubSpot store information about organizations interacting with your business.  These endpoints allow creation, management, and synchronization of company data between HubSpot and external systems.

## Understanding the CRM (Prerequisites)

Before using these APIs, familiarize yourself with HubSpot's [Understanding the CRM](link_to_hubspot_crm_guide) guide and learn how to [manage your CRM database](link_to_hubspot_crm_management).  This includes understanding objects, records, properties, and associations.


## API Endpoints

All endpoints below are under the base URL `/crm/v3/objects/companies`.  Replace `{companyId}` with the actual company ID.  Requests require proper authentication (API key).


### 1. Create Companies (POST `/crm/v3/objects/companies`)

Creates a new company record.  Requires at least `name` or `domain` property.  `domain` is strongly recommended as the primary unique identifier to prevent duplicates.  Multiple domains can be added using the `hs_additional_domains` property (e.g., `"hs_additional_domains": "domain.com;domain2.com"`).

**Request Body (JSON):**

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
      "to": { "id": 101 }, // ID of associated record (e.g., contact)
      "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 280 } ] // Association type
    },
    {
      "to": { "id": 556677 }, // ID of another associated record (e.g., deal)
      "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 185 } ] // Association type
    }
  ]
}
```

**Response (JSON):**  A successful response will contain the newly created company's ID and other properties.  Refer to HubSpot's API documentation for the exact structure.


**Lifecycle Stage Note:**  If including `lifecyclestage`, use the internal name (e.g., `"subscriber"`, `"marketingqualifiedlead"`) for default stages or the numeric ID for custom stages.  Obtain the ID from lifecycle stage settings or via the API.


### 2. Retrieve Companies

#### 2.1. Retrieve a Single Company (GET `/crm/v3/objects/companies/{companyId}`)

Retrieves a single company by its ID.

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `associations`: Comma-separated list of associated objects to retrieve.

#### 2.2. Retrieve Multiple Companies (GET `/crm/v3/objects/companies`)

Retrieves a list of companies.  Query parameters are the same as above.

#### 2.3. Batch Read Companies (POST `/crm/v3/objects/companies/batch/read`)

Retrieves a batch of companies by ID or custom unique identifier.  Does *not* support retrieving associations.

**Request Body (JSON):**

```json
{
  "properties": ["name", "domain"],
  "inputs": [ { "id": "56789" }, { "id": "23456" } ] // IDs (record IDs or custom IDs if idProperty is specified)
  "idProperty": "uniquepropertyexample" // Optional: Use a custom unique identifier property
}
```

### 3. Update Companies (PATCH `/crm/v3/objects/companies/{companyId}`)

Updates an existing company.

**Request Body (JSON):**  Similar to create, but only include properties to update.

**Lifecycle Stage Note:**  Updating `lifecyclestage` only allows moving *forward* in the stage order.  To move backward, first clear the existing value manually, via a workflow, or a data-syncing integration.

### 4. Associate Existing Companies (PUT `/crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates a company with other records or activities.

* `{toObjectType}`: Type of object to associate (e.g., `contacts`, `deals`).
* `{toObjectId}`: ID of the object to associate.
* `{associationTypeId}`: ID of the association type (obtain from default list or associations API).


### 5. Remove Association (DELETE `/crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Removes an association between a company and another record or activity.


### 6. Pin an Activity (PATCH `/crm/v3/objects/companies/{companyId}`)

Pins an activity to a company record.  Requires the `hs_pinned_engagement_id` property with the activity's ID.  Only one activity can be pinned per record. The activity must already be associated with the company.


### 7. Delete Companies (DELETE `/crm/v3/objects/companies/{companyId}`)

Deletes a company (moves to the recycling bin).


##  Error Handling

The API will return appropriate HTTP status codes (e.g., 400 for bad requests, 404 for not found) and error messages in the response body to indicate success or failure. Refer to HubSpot's API documentation for details on error handling.


##  Rate Limits

Be aware of HubSpot's API rate limits to avoid exceeding allowed requests per minute/hour.  Implement appropriate retry logic if necessary.


This documentation provides a summary.  Always refer to the official HubSpot API documentation for the most up-to-date information, detailed specifications, and complete error handling details.
