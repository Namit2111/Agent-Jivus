# HubSpot CRM API: Companies

This document details the HubSpot CRM API endpoints for managing companies.  Companies in HubSpot store information about organizations interacting with your business.  These endpoints allow you to create, manage, and synchronize company data between HubSpot and other systems.

For a broader understanding of objects, records, properties, and associations within the HubSpot CRM API, refer to the [Understanding the CRM](link-to-understanding-crm-guide) guide.  For general CRM database management, see [how to manage your CRM database](link-to-crm-management-guide).


## Create Companies

To create new companies, send a `POST` request to `/crm/v3/objects/companies`.

Include your company data within a `properties` object. You can also add an `associations` object to associate the new company with existing records (e.g., contacts, deals) or activities (e.g., meetings, notes).

### Properties

Company details are stored in properties.  HubSpot provides [default company properties](link-to-default-properties), but you can also [create custom properties](link-to-custom-properties).

When creating a company, include at least one of the following properties:

* `name`
* `domain`

It's strongly recommended to always include `domain`, as it's the primary unique identifier to prevent duplicates. For companies with multiple domains, use the `hs_additional_domains` field, separating domains with semicolons (e.g., `"hs_additional_domains": "domain.com;domain2.com;domain3.com"`).

Retrieve a list of your account's company properties using a `GET` request to `/crm/v3/properties/companies`. Learn more about the [properties API](link-to-properties-api).

**Note:** If including `lifecyclestage`, use the internal name.  Default stage internal names are text values (e.g., `subscriber`, `marketingqualifiedlead`) that don't change even if the label is edited. Custom stage internal names are numeric values. Find a stage's internal ID in your [lifecycle stage settings](link-to-lifecycle-stage-settings) or by retrieving the lifecycle stage property via the API.


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

* **`to.id`:** The ID of the record or activity to associate.
* **`types`:** The association type.  Use `associationCategory` and `associationTypeId`.  See [this list](link-to-association-type-list) of default IDs or retrieve custom association type values via the [associations API](link-to-associations-api).


## Retrieve Companies

Retrieve companies individually or in batches.

* **Individual Company:** `GET /crm/v3/objects/companies/{companyId}`
* **All Companies:** `GET /crm/v3/objects/companies`
* **Batch Read:** `POST /crm/v3/objects/companies/batch/read` (cannot retrieve associations)

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of current and historical properties.
* `associations`: Comma-separated list of associated objects to retrieve IDs for.  See [associations API](link-to-associations-api).

For batch read, use `idProperty` to retrieve by a custom unique identifier property (default is `hs_object_id`).


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

**Example Request Body (Batch Read with current and historical values):**

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

Update companies individually or in batches.  Use the company's record ID to update via API.

* **Individual Company:** `PATCH /crm/v3/objects/companies/{companyId}`

**Note:** When updating `lifecyclestage`, you can only move forward in the stage order. To move backward, clear the existing value manually or via a workflow/integration.


## Associate Existing Companies

Associate a company with other CRM records or activities: `PUT /crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`.

Retrieve `associationTypeId` from [this list](link-to-association-type-list) or via `GET /crm/v4/associations/{fromObjectType}/{toObjectType}/labels`. See the [associations API](link-to-associations-api).


## Remove an Association

Remove an association: `DELETE /crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`.


## Pin an Activity

Pin an activity to a company record using `hs_pinned_engagement_id` (the activity's ID from the [engagements APIs](link-to-engagements-api)). Only one activity can be pinned per record; it must already be associated with the company.

**Example Request Body (PATCH):**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```

You can also create, associate, and pin in a single request:

**Example Request Body (POST):**

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

Delete companies individually or in batches (moves to the recycling bin; you can [restore them](link-to-restore-companies) later).

* **Individual Company:** `DELETE /crm/v3/objects/companies/{companyId}`
* **Batch Delete:** See [reference documentation](link-to-batch-delete-docs)


Remember to replace placeholder links (`link-to-xyz`) with the actual URLs.
