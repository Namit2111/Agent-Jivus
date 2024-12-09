# HubSpot CRM API: Companies

This document details the HubSpot CRM API endpoints for managing companies.  Companies in HubSpot store information about organizations interacting with your business. These endpoints allow you to create, manage, and sync company data between HubSpot and other systems.

For a broader understanding of objects, records, properties, and associations APIs, refer to the [Understanding the CRM](link_to_understanding_crm_guide) guide. For general information on managing your CRM database, see [how to manage your CRM database](link_to_crm_database_management).


## Create Companies

To create new companies, send a `POST` request to `/crm/v3/objects/companies`.

Include your company data within a `properties` object.  You can also add an `associations` object to associate the new company with existing records (e.g., contacts, deals) or activities (e.g., meetings, notes).

**Properties:**

Company details are stored in properties.  HubSpot offers [default HubSpot company properties](link_to_default_properties), and you can also [create custom properties](link_to_creating_custom_properties).

When creating a company, include at least one of the following properties: `name` or `domain`.  Using `domain` is recommended, as domain names are the primary unique identifier to prevent duplicates.  For companies with multiple domains, use the `hs_additional_domains` field, separating domains with semicolons (e.g., `"hs_additional_domains": "domain.com;domain2.com;domain3.com"`).

To view all available properties, send a `GET` request to `/crm/v3/properties/companies`.  Learn more about the [properties API](link_to_properties_api).

**Important Note:** If including `lifecyclestage`, values must be the lifecycle stage's internal name.  Default stages use text values (e.g., `subscriber`, `marketingqualifiedlead`), while custom stages use numeric values. Find a stage's internal ID in your [lifecycle stage settings](link_to_lifecycle_stage_settings) or by retrieving the lifecycle stage property via the API.

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

## Associations

When creating a company, associate it with existing records or activities using an `associations` object.

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

**Parameters:**

*   `to`: The record or activity ID to associate.
*   `types`:  The association type. Include `associationCategory` and `associationTypeId`.  Default IDs are [listed here](link_to_default_association_type_ids); retrieve custom type values via the [associations API](link_to_associations_api).


## Retrieve Companies

Retrieve companies individually or in batches.

*   **Individual Company:**  `GET /crm/v3/objects/companies/{companyId}`
*   **List of Companies:** `GET /crm/v3/objects/companies`
*   **Batch Read:** `POST /crm/v3/objects/companies/batch/read` (supports retrieval by record ID or custom unique identifier property using the `idProperty` parameter).  Batch read *cannot* retrieve associations.  Use the [associations API](link_to_associations_api) for batch association reads.

**Query Parameters:**

*   `properties`: Comma-separated list of properties to return.
*   `propertiesWithHistory`: Comma-separated list of current and historical properties.
*   `associations`: Comma-separated list of associated objects to retrieve IDs for.
*   `idProperty`: (For batch read only)  The name of a custom unique identifier property.  Defaults to `hs_object_id` (record ID).


**Example Request Body (Batch Read with record ID):**

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

**Example Request Body (Batch Read with unique value property):**

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

**Example Request Body (Batch Read with historical values):**

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

Update companies individually or in batches.  Use the company's record ID for updates.

*   **Individual Company:** `PATCH /crm/v3/objects/companies/{companyId}`

**Important Note (Lifecycle Stage):** When updating `lifecyclestage`, you can only move *forward* in the stage order. To move backward, clear the existing lifecycle stage value manually, via a workflow, or through an integration.

## Associate Existing Companies

Associate a company with other CRM records or activities:

`PUT /crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

Retrieve `associationTypeId` from the [list of default values](link_to_default_association_type_ids) or via `GET /crm/v4/associations/{fromObjectType}/{toObjectType}/labels`.  Learn more in the [associations API](link_to_associations_api).


## Remove an Association

Remove an association:

`DELETE /crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


## Pin an Activity

Pin an activity to a company record using the `hs_pinned_engagement_id` field (containing the activity ID from the [engagements APIs](link_to_engagements_api)).  Only one activity can be pinned per record; the activity must already be associated with the company.

**Example Request Body (PATCH):**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```

**Example Request Body (POST - create and pin simultaneously):**

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

Delete companies individually or in batches (moves them to the recycling bin; they can be restored).

*   **Individual Company:** `DELETE /crm/v3/objects/companies/{companyId}`
*   **Batch Delete:** See the [reference documentation](link_to_batch_delete_docs)


**(Remember to replace placeholder links like `link_to_understanding_crm_guide` with actual URLs.)**
