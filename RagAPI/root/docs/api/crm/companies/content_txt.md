# HubSpot CRM API: Companies

This document details the HubSpot CRM API endpoints for managing companies.  Companies in HubSpot store information about organizations interacting with your business.  These endpoints allow for creation, management, and synchronization of company data with external systems.

## Understanding the CRM

For a comprehensive understanding of objects, records, properties, and associations within the HubSpot CRM API, refer to the [Understanding the CRM guide](link_to_guide_here).  For general CRM database management, see [how to manage your CRM database](link_to_guide_here).


## API Endpoints

All endpoints are under the `/crm/v3/objects/companies` base path unless otherwise specified.  Requests require proper authentication.

### 1. Create Companies

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/companies`

**Request Body:** JSON

The request body must include a `properties` object containing company data. At least one of `name` or `domain` is required.  `domain` is recommended as the primary unique identifier.  Multiple domains can be added using the `hs_additional_domains` field (e.g., `"hs_additional_domains": "domain.com;domain2.com"`).  You can also include an `associations` object to link the new company with existing records or activities.

**Example Request Body (with associations):**

```json
{
  "properties": {
    "name": "HubSpot",
    "domain": "hubspot.com",
    "city": "Cambridge",
    "industry": "Technology",
    "phone": "555-555-555",
    "state": "Massachusetts",
    "lifecyclestage": "51439524"
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

**Response:** JSON (Company object including newly assigned `id`)

**Note:** If `lifecyclestage` is included, use the internal name (numeric for custom stages, text for default stages).  Obtain internal IDs from lifecycle stage settings or the properties API.


### 2. Retrieve Companies

**a) Individual Company:**

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/companies/{companyId}`

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return with historical values.
* `associations`: Comma-separated list of associated objects to retrieve.


**b) List of Companies:**

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/companies`

**Query Parameters:** Same as individual company retrieval.


**c) Batch Retrieval:**

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/companies/batch/read`

**Request Body:** JSON

```json
{
  "properties": ["name", "domain"],
  "inputs": [
    {"id": "56789"},
    {"id": "23456"}
  ]
}
```

Use `idProperty` to specify a custom unique identifier property instead of the default `hs_object_id`.

**Example with custom ID property:**

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

**Response:** JSON (Array of company objects)


### 3. Update Companies

**a) Individual Company:**

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/companies/{companyId}`

**Request Body:** JSON (only include properties to update)

**Note:** Updating `lifecyclestage` only allows forward movement in the stage order.  To move backward, clear the existing value manually or via workflow/integration.


**b) Batch Update:** *(Endpoint not explicitly defined in the provided text, refer to HubSpot documentation)*


### 4. Associate Existing Companies

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

* `{toObjectType}`: Type of object to associate (e.g., `contacts`, `deals`).
* `{toObjectId}`: ID of the object to associate.
* `{associationTypeId}`:  ID of the association type.  Obtain from default list or `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`.


### 5. Remove Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


### 6. Pin an Activity

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/companies/{companyId}`

**Request Body (to pin):**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```

Can be included in `POST` request for company creation to pin an activity immediately.


### 7. Delete Companies

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/companies/{companyId}`

**Batch Deletion:** *(Endpoint not explicitly defined in the provided text, refer to HubSpot documentation)*


## Properties API

Use the `/crm/v3/properties/companies` endpoint (GET request) to retrieve a list of available company properties.  Refer to the [properties API documentation](link_to_properties_api_here) for details.


## Associations API

For detailed information on associations, including association type IDs and batch operations, refer to the [associations API documentation](link_to_associations_api_here).


Remember to replace placeholders like `{companyId}`, `{toObjectType}`, `{toObjectId}`, and `{associationTypeId}` with actual values.  Always consult the official HubSpot API documentation for the most up-to-date information and error handling.
