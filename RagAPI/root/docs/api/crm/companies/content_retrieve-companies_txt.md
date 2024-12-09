# HubSpot CRM API: Companies

This document details the HubSpot CRM API endpoints for managing companies.  Companies in HubSpot store information about organizations interacting with your business.  These endpoints allow you to create, manage, and sync company data between HubSpot and other systems.

For a broader understanding of objects, records, properties, and associations within the HubSpot API, refer to the [Understanding the CRM](link_to_understanding_crm_guide) guide.  For general CRM database management, see [how to manage your CRM database](link_to_crm_database_management).


## Create Companies

Use a `POST` request to `/crm/v3/objects/companies` to create new companies.  The request body should include a `properties` object containing company data and an optional `associations` object to link the new company to existing records or activities.

**Required Properties:** At least one of the following properties is required:

*   `name`: The name of the company.
*   `domain`: The company's domain (recommended as the primary unique identifier to prevent duplicates).  Multiple domains can be added using the `hs_additional_domains` field (e.g., `"hs_additional_domains" : "domain.com; domain2.com; domain3.com"`).

**Example Request Body (JSON):**

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
  }
}
```

**Lifecycle Stage Note:** If including `lifecyclestage`, use the internal name (text for default stages, numeric for custom stages). Find the internal ID in your lifecycle stage settings or via the lifecycle stage property API.


## Properties

Company details are stored in properties.  HubSpot provides default properties, and you can create custom ones.  To view available properties, make a `GET` request to `/crm/v3/properties/companies`.  Learn more about the [properties API](link_to_properties_api).


## Associations

When creating a company, you can associate it with existing records or activities using the `associations` object.

**Example Request Body (JSON):**

```json
{
  "properties": {
    "name": "HubSpot",
    "domain": "hubspot.com",
    // ... other properties
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

*   `to.id`: The ID of the record or activity to associate.
*   `types`: The association type, including `associationCategory` and `associationTypeId`.  See [this list](link_to_association_type_list) of default IDs or use the [associations API](link_to_associations_api) for custom types.


## Retrieve Companies

**Individual Company:** `GET` `/crm/v3/objects/companies/{companyId}`

**List of Companies:** `GET` `/crm/v3/objects/companies`

**Batch Read:** `POST` `/crm/v3/objects/companies/batch/read` (allows retrieval by record ID or custom unique identifier property using `idProperty`).  Associations cannot be retrieved with this endpoint; use the [associations API](link_to_associations_api) for batch association reads.

**Query Parameters:**

*   `properties`: Comma-separated list of properties to return.
*   `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
*   `associations`: Comma-separated list of associated objects to retrieve IDs for.
*   `idProperty`: (For batch read) Custom unique identifier property to use for retrieval (default is `hs_object_id`).

**Example Request Bodies (JSON):**

**(Record ID)**

```json
{
  "properties": ["name", "domain"],
  "inputs": [
    {"id": "56789"},
    {"id": "23456"}
  ]
}
```

**(Unique Value Property)**

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

**(Record ID, current and historical values)**

```json
{
  "propertiesWithHistory": ["name"],
  "inputs": [
    {"id": "56789"},
    {"id": "23456"}
  ]
}
```


## Update Companies

**Individual Company:** `PATCH` `/crm/v3/objects/companies/{companyId}`

**Batch Update:** *(Details not provided in source text)*

**Lifecycle Stage Note:**  When updating `lifecyclestage`, you can only move forward in the stage order. To move backward, clear the existing value manually, via a workflow, or through a data-syncing integration.


## Associate Existing Companies

`PUT` `/crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


## Remove an Association

`DELETE` `/crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


## Pin an Activity

Use the `hs_pinned_engagement_id` property (containing the activity ID from the [engagements APIs](link_to_engagements_api)) to pin an activity to a company record.  Only one activity can be pinned per record, and the activity must already be associated with the company.

**Example Request Body (JSON - PATCH):**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```

You can also pin an activity during company creation.


## Delete Companies

**Individual Company:** `DELETE` `/crm/v3/objects/companies/{companyId}`

**Batch Delete:** *(Details not provided in source text, refer to reference documentation.)*  Deleted companies are moved to the recycling bin and can be restored.


**(Remember to replace placeholder links like `link_to_understanding_crm_guide` with the actual links.)**
