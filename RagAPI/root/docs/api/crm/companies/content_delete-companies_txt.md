# HubSpot CRM API: Companies

This document details the HubSpot API endpoints for managing companies. Companies in HubSpot store information about organizations interacting with your business.  These endpoints allow you to create, manage, and sync company data between HubSpot and other systems.

For a broader understanding of objects, records, properties, and associations within the HubSpot API, refer to the [Understanding the CRM](<link_to_understanding_crm_guide>) guide.  For general CRM database management, see [How to manage your CRM database](<link_to_crm_database_management>).


## Create Companies

To create new companies, send a `POST` request to:

`/crm/v3/objects/companies`

Include your company data within a `properties` object. You can also add an `associations` object to link your new company with existing records (e.g., contacts, deals) or activities (e.g., meetings, notes).

### Properties

Company details are stored in properties.  HubSpot provides [default company properties](<link_to_default_properties>), but you can also [create custom properties](<link_to_create_custom_properties>).

When creating a company, include at least one of the following properties:

* `name`
* `domain`

It's strongly recommended to always include `domain` as it's the primary unique identifier, preventing duplicates.  For companies with multiple domains, use the `hs_additional_domains` field, separating domains with semicolons (e.g., `"hs_additional_domains" : "domain.com; domain2.com; domain3.com"`).

Retrieve a list of your account's company properties via a `GET` request to:

`/crm/v3/properties/companies`

Learn more about the [properties API](<link_to_properties_api>).

**Note:** If including `lifecyclestage`, use the internal name (not the label). Default stage internal names are text values; custom stage internal names are numeric. Find internal IDs in your lifecycle stage settings or via the API.


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

* **`to.id`**: The ID of the record or activity.
* **`types`**:  Association type. Use [default association type IDs](<link_to_default_association_types>) or retrieve custom type IDs via the [associations API](<link_to_associations_api>).


## Retrieve Companies

Retrieve companies individually or in batches.

### Individual Company

`GET` request to:

`/crm/v3/objects/companies/{companyId}`

### List of Companies

`GET` request to:

`/crm/v3/objects/companies`

**Query Parameters:**

* **`properties`**: Comma-separated list of properties to return.
* **`propertiesWithHistory`**: Comma-separated list of properties to return, including historical values.
* **`associations`**: Comma-separated list of associated objects to retrieve IDs for.  See [associations API](<link_to_associations_api>).

### Batch Retrieval

`POST` request to:

`/crm/v3/objects/companies/batch/read`

This endpoint does *not* retrieve associations. Use the [associations API](<link_to_associations_api>) for batch association retrieval.

* **`idProperty` (optional)**: Use a custom unique identifier property instead of the record ID (`hs_object_id`).  If omitted, `id` values refer to `hs_object_id`.

**Example Request Body (JSON - Record IDs):**

```json
{
  "properties": ["name", "domain"],
  "inputs": [
    { "id": "56789" },
    { "id": "23456" }
  ]
}
```

**Example Request Body (JSON - Unique Value Property):**

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

**Example Request Body (JSON - Current and Historical Values):**

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

Update companies individually or in batches. Use the company's record ID for updates.

### Individual Company

`PATCH` request to:

`/crm/v3/objects/companies/{companyId}`

**Note:** When updating `lifecyclestage`, you can only move *forward* in the stage order. To move backward, first clear the existing value manually or via a workflow/integration.

### Batch Update

[Link to batch update documentation]


## Associate Existing Companies

Associate a company with other CRM records or activities:

`PUT` request to:

`/crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


Retrieve `associationTypeId` from [default values](<link_to_default_association_types>) or via a `GET` request to:

`/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`

See the [associations API](<link_to_associations_api>) for details.


## Remove an Association

`DELETE` request to:

`/crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


## Pin an Activity

Pin an activity to a company record using the `hs_pinned_engagement_id` field (containing the activity ID from the [engagements APIs](<link_to_engagements_api>)).  Only one activity can be pinned per record; the activity must already be associated with the company.

**Example Request Body (JSON - PATCH):**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```

**Example Request Body (JSON - POST - Create and Pin):**

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

### Individual Company

`DELETE` request to:

`/crm/v3/objects/companies/{companyId}`

### Batch Delete

[Link to batch delete documentation]


**(Remember to replace placeholder links like `<link_to_understanding_crm_guide>` with actual links to the relevant HubSpot documentation.)**
