# HubSpot CRM API: Companies

This document details the HubSpot CRM API endpoints for managing companies.  Companies in HubSpot store information about organizations interacting with your business. These endpoints allow for creating, managing, and syncing company data between HubSpot and other systems.

## Understanding the CRM

For a comprehensive understanding of HubSpot's objects, records, properties, and associations APIs, refer to the [Understanding the CRM](link_to_understanding_crm_guide) guide.  For general CRM database management, see [Managing your CRM database](link_to_crm_database_management).

## API Endpoints

All endpoints use the `/crm/v3/objects/companies` base path unless otherwise specified.  Replace `{companyId}` and `{toObjectId}` with the respective IDs.

### 1. Create Companies

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/companies`

**Request Body (JSON):**

This endpoint requires at least one of `name` or `domain` properties.  `domain` is strongly recommended as it's the primary unique identifier.  Multiple domains can be added using the `hs_additional_domains` property (e.g., `"hs_additional_domains": "domain.com;domain2.com"`).

```json
{
  "properties": {
    "name": "HubSpot",
    "domain": "hubspot.com",
    "city": "Cambridge",
    "industry": "Technology",
    "phone": "555-555-555",
    "state": "Massachusetts",
    "lifecyclestage": "51439524" // Use internal lifecycle stage name or ID
  },
  "associations": [ // Optional: Associate with existing records/activities
    {
      "to": { "id": 101 }, // ID of the record/activity
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 280 // Association type ID
        }
      ]
    }
  ]
}
```

**Response (JSON):**  A successful response will include the newly created company's ID and other properties.

**Note on `lifecyclestage`:**  Use the internal name (e.g., `"subscriber"`, `"marketingqualifiedlead"`) for default lifecycle stages or the numeric ID for custom stages.


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

**Query Parameters:** Same as above.

**c) Batch Read:**

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/companies/batch/read`

**Request Body (JSON):**

```json
{
  "properties": ["name", "domain"],
  "inputs": [
    { "id": "56789" }, // Record ID or custom unique identifier
    { "id": "23456" }
  ],
  "idProperty": "uniquepropertyexample" // Optional: Use if using a custom unique identifier property
}
```

**Response (JSON):** An array of company objects.  Associations are not retrieved via this endpoint.


### 3. Update Companies

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/companies/{companyId}`

**Request Body (JSON):**  Include only the properties you want to update.

```json
{
  "properties": {
    "name": "Updated Company Name",
    "hs_pinned_engagement_id": 123456789 // To pin an activity
  }
}
```

**Note on `lifecyclestage`:**  Updating `lifecyclestage` only allows moving forward in the stage order.  To move backward, clear the existing value first.


### 4. Associate Existing Companies

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

* `{toObjectType}`: Type of the object to associate (e.g., `contacts`, `deals`).
* `{toObjectId}`: ID of the object to associate.
* `{associationTypeId}`: ID of the association type.  Find default IDs [here](link_to_default_association_types) or retrieve custom ones via the associations API.


### 5. Remove Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


### 6. Delete Companies

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/companies/{companyId}`

(Batch deletion details are in the [reference documentation](link_to_reference_documentation)).


## Properties API

Retrieve a list of available company properties via a `GET` request to `/crm/v3/properties/companies`.  See the [properties API documentation](link_to_properties_api) for details.

## Associations API

Learn more about managing associations via the [associations API documentation](link_to_associations_api).


**(Remember to replace placeholder links with actual links to the relevant HubSpot documentation.)**
