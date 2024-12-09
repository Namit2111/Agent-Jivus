# HubSpot CRM API: Companies

This document details the HubSpot CRM API endpoints for managing companies.  Companies in HubSpot store information about organizations interacting with your business.  These endpoints allow you to create, manage, and synchronize company data between HubSpot and other systems.

For a broader understanding of objects, records, properties, and associations APIs, refer to the [Understanding the CRM guide](link_to_understanding_crm_guide).  For general CRM database management information, see [how to manage your CRM database](link_to_crm_database_management).


## Create Companies

Use a `POST` request to `/crm/v3/objects/companies` to create new companies.  Include company data within a `properties` object.  You can also add an `associations` object to associate the new company with existing records (e.g., contacts, deals) or activities (e.g., meetings, notes).

### Properties

Company details are stored in properties.  HubSpot provides [default company properties](link_to_default_properties), but you can also [create custom properties](link_to_creating_custom_properties).

When creating a company, include at least one of the following properties:

* `name`
* `domain` (recommended as the primary unique identifier to prevent duplicates)

If a company has multiple domains, use the `hs_additional_domains` field, separating domains with semicolons (e.g., `"hs_additional_domains" : "domain.com; domain2.com; domain3.com"`).

Retrieve a list of your account's company properties using a `GET` request to `/crm/v3/properties/companies`. Learn more about the [properties API](link_to_properties_api).

**Note:** If including `lifecyclestage`, use the internal name (not the label). Default stage internal names are text values; custom stage internal names are numeric values. Find these IDs in your lifecycle stage settings or by retrieving the lifecycle stage property via the API.


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

### Associations

When creating a company, associate it with existing records or activities using the `associations` object.

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

| Parameter      | Description                                                                        |
|-----------------|------------------------------------------------------------------------------------|
| `to`           | Record or activity ID to associate.                                                |
| `types`        | Association type. Include `associationCategory` and `associationTypeId`.  See [default association type IDs](link_to_default_association_types) or use the [associations API](link_to_associations_api) for custom types. |


## Retrieve Companies

Retrieve companies individually or in batches.

* **Individual Company:** `GET` `/crm/v3/objects/companies/{companyId}`
* **List of Companies:** `GET` `/crm/v3/objects/companies`
* **Batch Retrieval:** `POST` `/crm/v3/objects/companies/batch/read` (cannot retrieve associations)

**Query Parameters (for individual and list requests):**

| Parameter           | Description                                                                                                 |
|-----------------------|-------------------------------------------------------------------------------------------------------------|
| `properties`          | Comma-separated list of properties to return.  Missing properties are omitted from the response.             |
| `propertiesWithHistory` | Comma-separated list of properties to return, including historical values. Missing properties are omitted. |
| `associations`        | Comma-separated list of objects to retrieve associated IDs for.  Nonexistent associations are omitted.     |


**Batch Retrieval (`POST` /crm/v3/objects/companies/batch/read):**

Uses `idProperty` (optional) to specify a custom unique identifier property.  Defaults to `hs_object_id` (record ID).

**Example Request Body (JSON - Record ID):**

```json
{
  "properties": ["name", "domain"],
  "inputs": [
    { "id": "56789" },
    { "id": "23456" }
  ]
}
```

**Example Request Body (JSON - Unique Property):**

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

**Example Request Body (JSON - Historical Values):**

```json
{
  "propertiesWithHistory": ["name"],
  "inputs": [
    { "id": "56789" },
    { "id": "23456" }
  ]
}
```


## Update Companies

Update companies individually or in batches.  Use the company's record ID to update.

* **Individual Company:** `PATCH` `/crm/v3/objects/companies/{companyId}`
* **Batch Update:** (Refer to [reference documentation](link_to_batch_update_docs))

**Note:** When updating `lifecyclestage`, you can only move *forward* in the stage order. To move backward, first clear the existing value manually or using a workflow/integration.


## Associate Existing Companies

Associate a company with other CRM records or activities using a `PUT` request to:

`/crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

Retrieve `associationTypeId` from the [list of default values](link_to_default_association_types) or using a `GET` request to `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`.  Learn more in the [associations API](link_to_associations_api).


## Remove an Association

Use a `DELETE` request to:

`/crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


## Pin an Activity

Pin an activity to a company record using the `hs_pinned_engagement_id` field (containing the activity ID, retrieved via the [engagements APIs](link_to_engagements_api)).  Only one activity can be pinned per record; the activity must already be associated.

**Example Request Body (JSON - PATCH):**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```

**Example Request Body (JSON - POST, create and pin):**

```json
{
  "properties": {
    "domain": "example.com",
    "name": "Example Company",
    "hs_pinned_engagement_id": 123456789
  },
  "associations": [
    {
      "to": { "id": 123456789 },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 189
        }
      ]
    }
  ]
}
```


## Delete Companies

Delete companies individually or in batches (moving them to the recycling bin; they can be restored later).

* **Individual Company:** `DELETE` `/crm/v3/objects/companies/{companyId}`
* **Batch Deletion:** (Refer to [reference documentation](link_to_batch_delete_docs))


**Remember to replace placeholder links (e.g., `link_to_understanding_crm_guide`) with the actual links to the relevant HubSpot documentation.**
