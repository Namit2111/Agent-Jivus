# HubSpot CRM API: Companies

This document details the HubSpot CRM API endpoints for managing companies.  Companies in HubSpot store information about organizations that interact with your business.  These endpoints allow you to create, manage, and sync company data between HubSpot and other systems.

For broader context on objects, records, properties, and associations APIs, refer to the [Understanding the CRM guide](link-to-understanding-crm-guide).  For general CRM database management, see [how to manage your CRM database](link-to-crm-database-management).


## Create Companies

Use a `POST` request to `/crm/v3/objects/companies` to create new companies.  Include company data within a `properties` object and optionally an `associations` object to link the new company to existing records or activities.

**Properties:**

Company details are stored in properties.  HubSpot provides [default company properties](link-to-default-properties), and you can also [create custom properties](link-to-create-custom-properties).

When creating a company, include at least one of the following properties:

* `name`
* `domain` (Recommended:  `domain` is the primary unique identifier to prevent duplicates.  Use `hs_additional_domains` (semicolon-separated) for multiple domains, e.g., `"hs_additional_domains" : "domain.com; domain2.com; domain3.com"`)

Retrieve a list of your account's company properties using a `GET` request to `/crm/v3/properties/companies`. Learn more about the [properties API](link-to-properties-api).


**Important Note on `lifecyclestage`:** If included, use the internal name (not the label) of the lifecycle stage.  Default stages have text internal names (e.g., `"subscriber"`, `"marketingqualifiedlead"`), while custom stages have numeric IDs. Find the internal ID in your [lifecycle stage settings](link-to-lifecycle-stage-settings) or via the API.


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

**Associations:**

The `associations` object lets you link the new company with existing records or activities.

**Example Request Body (JSON) with Associations:**

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

* **`to.id`:**  The ID of the record or activity.
* **`types`:**  The association type.  Use the [list of default association type IDs](link-to-default-association-types) or retrieve custom types via the [associations API](link-to-associations-api).


## Retrieve Companies

Retrieve companies individually or in batches.

**Individual Company:**  Use a `GET` request to `/crm/v3/objects/companies/{companyId}`.

**List of Companies:** Use a `GET` request to `/crm/v3/objects/companies`.

**Query Parameters (for individual and list requests):**

* **`properties`:** Comma-separated list of properties to return.  Missing properties are omitted from the response.
* **`propertiesWithHistory`:** Comma-separated list of properties to return, including historical values.
* **`associations`:** Comma-separated list of associated objects to retrieve IDs for.


**Batch Retrieval (POST to `/crm/v3/objects/companies/batch/read`):**

Retrieves a batch of companies by record ID (default, using `hs_object_id`) or a custom unique identifier property (using `idProperty`).  This endpoint does *not* retrieve associations.  Use the [associations API](link-to-associations-api) for batch association retrieval.


**Example Request Body (JSON) - Batch Retrieval by Record ID:**

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

**Example Request Body (JSON) - Batch Retrieval by Custom Unique Property:**

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

**Example Request Body (JSON) - Batch Retrieval with History:**

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

**Individual Company:** Use a `PATCH` request to `/crm/v3/objects/companies/{companyId}`.

**Important Note on `lifecyclestage` Updates:** You can only move the `lifecyclestage` forward in the stage order. To move it backward, first clear the existing value manually or via a workflow/integration.

## Associate Existing Companies

Associate a company with other CRM records or activities using a `PUT` request to `/crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`.

Retrieve the `associationTypeId` from the [list of default values](link-to-default-association-types) or via a `GET` request to `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`.


## Remove an Association

Remove an association using a `DELETE` request to `/crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`.


## Pin an Activity

Pin an activity to a company record using the `hs_pinned_engagement_id` property (containing the activity ID, obtained via the [engagements APIs](link-to-engagements-api)).  Only one activity can be pinned per record, and the activity must already be associated with the company.


**Example Request Body (JSON) - Pinning via PATCH:**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```

**Example Request Body (JSON) - Create, Associate, and Pin in Single Request:**

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

Delete companies individually or in batches (sending them to the recycling bin; you can restore them later).

**Individual Company:** Use a `DELETE` request to `/crm/v3/objects/companies/{companyId}`.

See the [reference documentation](link-to-batch-delete-docs) for batch deletion.


**(Remember to replace placeholder links like `link-to-understanding-crm-guide` with actual URLs.)**
