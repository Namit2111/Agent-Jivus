# HubSpot CRM API: Companies

This document details the HubSpot CRM API endpoints for managing companies.  Companies in HubSpot store information about organizations interacting with your business.  These endpoints allow creation, management, and synchronization of company data between HubSpot and other systems.

## Understanding the CRM

For a comprehensive understanding of objects, records, properties, and associations within the HubSpot CRM API, refer to the [Understanding the CRM guide](link_to_guide).  Information on managing your CRM database can be found [here](link_to_db_management).

## API Endpoints

All endpoints are under the `/crm/v3/objects/companies` base path unless otherwise specified.  All requests require proper authentication.

### 1. Create Companies

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/companies`

**Request Body (JSON):**

The request body must include a `properties` object containing company data.  At least one of `name` or `domain` is required.  `domain` is strongly recommended as the primary unique identifier to prevent duplicates.  Multiple domains can be added using the `hs_additional_domains` field (e.g., `"hs_additional_domains": "domain.com;domain2.com"`).

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
  "associations": [ //Optional: Associate with existing records/activities
    {
      "to": { "id": 101 },
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 280 }]
    },
    {
      "to": { "id": 556677 },
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 185 }]
    }
  ]
}
```

**Response (JSON):**  A successful response will include the newly created company's ID and other properties.

**Note:**  If `lifecyclestage` is included, use the internal name (e.g., "subscriber", "marketingqualifiedlead") for default stages or the numeric ID for custom stages.  Find the ID in your lifecycle stage settings or via the API.


### 2. Retrieve Companies

**a) Individual Company:**

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/companies/{companyId}`

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `associations`: Comma-separated list of associated objects to retrieve IDs for.


**b) List of Companies:**

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/companies`

**Query Parameters:**  Same as above (a).

**c) Batch Read:**

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/companies/batch/read`

**Request Body (JSON):**

```json
{
  "properties": ["name", "domain"],
  "inputs": [
    { "id": "56789" },  //Record ID (hs_object_id)
    { "id": "23456" }
  ]
}
```

Or, using a custom unique identifier property:

```json
{
  "properties": ["name", "domain"],
  "idProperty": "uniquepropertyexample",
  "inputs": [
    { "id": "abc" },
    { "id": "def" }
  ]
}
```

**Response (JSON):**  An array of company objects.  Associations are *not* retrieved via this endpoint.


### 3. Update Companies

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/companies/{companyId}`

**Request Body (JSON):**  Include only the properties to be updated.

**Note:** Updating `lifecyclestage` only allows moving *forward* in the stage order.  To move backward, clear the existing value manually, via workflow, or integration.


### 4. Associate Existing Companies

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

* `{toObjectType}`:  The type of object to associate (e.g., "contacts").
* `{toObjectId}`: The ID of the object to associate.
* `{associationTypeId}`: The ID of the association type (see default list or use the Associations API).


### 5. Remove Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


### 6. Pin an Activity

**a) Update Existing Company:**

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/companies/{companyId}`

**Request Body (JSON):**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```

**b) Create Company and Pin Activity (Simultaneous):**

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/companies`

**Request Body (JSON):** (Similar to Create Companies, but includes `hs_pinned_engagement_id` and relevant association.)


### 7. Delete Companies

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/companies/{companyId}`

Refer to the reference documentation for batch deletion.


## Properties API

Retrieve all available company properties using a `GET` request to `/crm/v3/properties/companies`.  Learn more in the [Properties API documentation](link_to_properties_api).

## Associations API

Learn more about managing associations via the [Associations API documentation](link_to_associations_api).  This includes retrieving association type IDs and batch reading associations.  Note that the batch read endpoint for companies does *not* support retrieving associations.


This documentation provides a comprehensive overview of the HubSpot CRM API's Companies endpoints. Remember to replace placeholder values (e.g., `{companyId}`, `{toObjectId}`, etc.) with actual values.  Always consult the official HubSpot API documentation for the most up-to-date information and details.
