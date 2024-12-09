# HubSpot CRM API: Companies

This document details the HubSpot CRM API endpoints for managing companies.  Companies in HubSpot store information about organizations interacting with your business. These endpoints allow you to create, manage, and synchronize company data between HubSpot and other systems.

For a broader understanding of objects, records, properties, and associations within the HubSpot API, refer to the [Understanding the CRM](link_to_understanding_crm_guide) guide.  For general CRM database management, see [how to manage your CRM database](link_to_crm_database_management).


## Create Companies

To create new companies, send a `POST` request to:

`/crm/v3/objects/companies`

Include your company data within a `properties` object. You can also add an `associations` object to associate the new company with existing records (e.g., contacts, deals) or activities (e.g., meetings, notes).

### Properties

Company details are stored in properties. HubSpot provides default properties, and you can also create custom properties.  When creating a company, include at least one of the following:

* `name`
* `domain` (recommended as the primary unique identifier to avoid duplicates)

If a company has multiple domains, use the `hs_additional_domains` field, separating domains with semicolons (e.g., `"hs_additional_domains" : "domain.com; domain2.com; domain3.com"`).

To view available properties, make a `GET` request to:

`/crm/v3/properties/companies`

Learn more about the [properties API](link_to_properties_api).

**Note:** If including `lifecyclestage`, use the internal name (not the label).  Internal names for default stages are text values (e.g., `subscriber`, `marketingqualifiedlead`), while custom stage internal names are numeric. Find the internal ID in your lifecycle stage settings or via the API.


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

* **`to.id`:**  The unique ID of the record or activity.
* **`types`:**  The association type.  Use the default association type IDs ([link to default association types](link_to_default_association_types)) or retrieve custom type IDs via the [associations API](link_to_associations_api).


## Retrieve Companies

Retrieve companies individually or in batches.

### Individual Company

Use a `GET` request to:

`/crm/v3/objects/companies/{companyId}`

### List of Companies

Use a `GET` request to:

`/crm/v3/objects/companies`

**Query Parameters:**

* **`properties`:** Comma-separated list of properties to return.
* **`propertiesWithHistory`:** Comma-separated list of properties to return, including historical values.
* **`associations`:** Comma-separated list of associated objects to retrieve IDs for.  See [associations API](link_to_associations_api).

### Batch Retrieval

Use a `POST` request to:

`/crm/v3/objects/companies/batch/read`

This endpoint *cannot* retrieve associations. Use the [associations API](link_to_associations_api) for batch association retrieval.  You can retrieve by record ID (`hs_object_id`) or a custom unique identifier property using the `idProperty` parameter.

**Example Request Body (JSON) - Record ID:**

```json
{
  "properties": ["name", "domain"],
  "inputs": [
    {
      "id": "56789"
    },
    {
      "id": "23456"
    }
  ]
}
```

**Example Request Body (JSON) - Unique Property:**

```json
{
  "properties": ["name", "domain"],
  "idProperty": "uniquepropertyexample",
  "inputs": [
    {
      "id": "abc"
    },
    {
      "id": "def"
    }
  ]
}
```

**Example Request Body (JSON) - Historical Values:**

```json
{
  "propertiesWithHistory": ["name"],
  "inputs": [
    {
      "id": "56789"
    },
    {
      "id": "23456"
    }
  ]
}
```


## Update Companies

Update companies individually or in batches. Use the company's record ID for updates.

### Individual Company

Use a `PATCH` request to:

`/crm/v3/objects/companies/{companyId}`

**Note on `lifecyclestage`:**  You can only update `lifecyclestage` forward in the stage order. To move backward, clear the existing value manually or via a workflow/integration.


## Associate Existing Companies

Associate a company with other CRM records or activities using a `PUT` request:

`/crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

Retrieve `associationTypeId` from the list of default values or via a `GET` request to `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`. See the [associations API](link_to_associations_api).


## Remove an Association

Remove an association using a `DELETE` request:

`/crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


## Pin an Activity

Pin an activity to a company record using the `hs_pinned_engagement_id` field (containing the activity ID from the [engagements APIs](link_to_engagements_api)). Only one activity can be pinned per record, and the activity must already be associated.

**Example Request Body (JSON) - PATCH request:**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```

You can also pin during company creation:

**Example Request Body (JSON) - POST request:**

```json
{
  "properties": {
    "domain": "example.com",
    "name": "Example Company",
    "hs_pinned_engagement_id": 123456789
  },
  "associations": [
    {
      "to": {
        "id": 123456789
      },
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

Delete companies individually or in batches (moving them to the recycling bin).  See the [reference documentation](link_to_reference_documentation) for batch deletion.

To delete individually, use a `DELETE` request:

`/crm/v3/objects/companies/{companyId}`

Remember to replace placeholder links (`link_to...`) with the actual URLs.
