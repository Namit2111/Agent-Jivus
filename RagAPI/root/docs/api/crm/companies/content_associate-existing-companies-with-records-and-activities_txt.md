# HubSpot CRM API: Companies

This document details the HubSpot CRM API endpoints for managing companies.  Companies in HubSpot store information about organizations interacting with your business.  These endpoints allow for creation, management, and synchronization of company data between HubSpot and other systems.

## Understanding the CRM

For a comprehensive understanding of objects, records, properties, and associations within the HubSpot CRM API, refer to the [Understanding the CRM guide](link_to_guide_here).  For general information on managing your CRM database, see [how to manage your CRM database](link_to_guide_here).


## API Endpoints

All endpoints are under the `/crm/v3/objects/companies` base path unless otherwise specified.


### 1. Create Companies

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/companies`

**Request Body:** JSON

This endpoint creates new company records.  The request body must include a `properties` object containing company details.  An optional `associations` object can associate the new company with existing records or activities.

**Required Properties:** At least one of `name` or `domain` is required.  `domain` is strongly recommended as the primary unique identifier to prevent duplicates.  Multiple domains can be added using the `hs_additional_domains` property (e.g., `"hs_additional_domains": "domain.com;domain2.com"`).

**Example Request Body:**

```json
{
  "properties": {
    "name": "HubSpot",
    "domain": "hubspot.com",
    "city": "Cambridge",
    "industry": "Technology",
    "phone": "555-555-555",
    "state": "Massachusetts",
    "lifecyclestage": "51439524" //Use internal name or ID for lifecycle stage
  },
  "associations": [
    {
      "to": {
        "id": 101
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 280
        }
      ]
    },
    {
      "to": {
        "id": 556677
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 185
        }
      ]
    }
  ]
}
```

**Response:**  A JSON object representing the newly created company, including its ID.


### 2. Retrieve Companies

**Method:** `GET` (individual), `GET` (list), `POST` (batch)

**Endpoints:**

* Individual: `/crm/v3/objects/companies/{companyId}`
* List: `/crm/v3/objects/companies`
* Batch: `/crm/v3/objects/companies/batch/read`

**Query Parameters (for individual and list GET requests):**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `associations`: Comma-separated list of associated objects to retrieve IDs for.


**Batch Read Request Body:** JSON

* `properties`: Array of properties to return.
* `propertiesWithHistory`: Array of properties to return with history (batch read doesn't support associations).
* `inputs`: Array of objects, each with an `id` property representing the company ID or a custom unique identifier.
* `idProperty`: (Optional) The name of a custom unique identifier property to use instead of the record ID.


**Example Batch Read Request (with record IDs):**

```json
{
  "properties": ["name", "domain"],
  "inputs": [
    {"id": "56789"},
    {"id": "23456"}
  ]
}
```

**Example Batch Read Request (with custom unique identifier):**

```json
{
  "properties": ["name", "domain"],
  "idProperty": "uniquepropertyexample",
  "inputs": [
    {"id": "abc"},
    {"id": "def"}
  ]
}
```

**Response:** JSON object (individual) or JSON array (list or batch) containing company data.


### 3. Update Companies

**Method:** `PATCH` (individual),  `PATCH` (batch - not explicitly detailed but likely similar to read)

**Endpoint:** `/crm/v3/objects/companies/{companyId}`

**Request Body:** JSON object containing the properties to update.

**Note:** Updating `lifecyclestage` only allows moving forward in the stage order.  To move backward, clear the existing value manually or through a workflow/integration.


### 4. Associate Existing Companies

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

Associates a company with another record or activity.  `associationTypeId` can be found in the list of default values or retrieved via the associations API.


### 5. Remove an Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

Removes an association between a company and another record or activity.


### 6. Pin an Activity

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/companies/{companyId}`

Pins an activity to a company record using the `hs_pinned_engagement_id` property. The activity ID must be obtained via the Engagements API and must already be associated with the company.


### 7. Delete Companies

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/companies/{companyId}`

Deletes a company (moves it to the recycling bin).  Batch deletion is mentioned but not detailed here, see the [reference documentation](link_to_ref_doc_here).


## Properties API

To view available company properties, make a `GET` request to `/crm/v3/properties/companies`.  Learn more about the Properties API at [link_to_properties_api_doc_here].

## Associations API

Learn more about the Associations API at [link_to_associations_api_doc_here].  This API is crucial for understanding association types and IDs used in creating and managing company associations.  This includes retrieving `associationTypeId` values for associating companies with other objects.

## Engagements API

To retrieve activity IDs for pinning, refer to the [Engagements API documentation](link_to_engagements_api_here).


Remember to replace placeholders like `{companyId}`, `{toObjectType}`, `{toObjectId}`, and `{associationTypeId}` with the appropriate values.  Always refer to the official HubSpot API documentation for the most up-to-date information.
