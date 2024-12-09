# HubSpot CRM API: Companies

This document details the HubSpot API endpoints for managing company records.  Companies in HubSpot store information about organizations that interact with your business.  These endpoints allow you to create, manage, and synchronize company data between HubSpot and other systems.

## Understanding the CRM

For a comprehensive understanding of objects, records, properties, and associations within the HubSpot CRM API, refer to the [Understanding the CRM](link-to-understanding-crm-guide) guide.  For general information on managing your CRM database, see [Managing your CRM database](link-to-managing-crm-database).


## Create Companies

To create new companies, send a `POST` request to `/crm/v3/objects/companies`.

Include your company data within a `properties` object. You can also include an `associations` object to associate the new company with existing records (e.g., contacts, deals) or activities (e.g., meetings, notes).

### Properties

Company details are stored in properties.  HubSpot provides [default company properties](link-to-default-properties), but you can also [create custom properties](link-to-creating-custom-properties).

When creating a company, include at least one of the following properties:

* `name`
* `domain`

It's strongly recommended to always include `domain` as it's the primary unique identifier, preventing duplicate companies.  For companies with multiple domains, use the `hs_additional_domains` field, separating domains with semicolons (e.g., `"hs_additional_domains": "domain.com;domain2.com;domain3.com"`).

To view all available properties, send a `GET` request to `/crm/v3/properties/companies`.  Learn more about the [properties API](link-to-properties-api).

**Note:** If including `lifecyclestage`, use the internal name (not the label).  Internal names for default stages are text values (e.g., `"subscriber"`, `"marketingqualifiedlead"`); custom stage internal names are numeric values. Find a stage's internal ID in your [lifecycle stage settings](link-to-lifecycle-stage-settings) or by retrieving the lifecycle stage property via the API.


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

* **`to`:** The record or activity ID to associate.
* **`types`:** The association type. Includes `associationCategory` and `associationTypeId`.  See [default association type IDs](link-to-default-association-types) or use the [associations API](link-to-associations-api) for custom types.


## Retrieve Companies

Retrieve companies individually or in batches.

* **Individual Company:** `GET /crm/v3/objects/companies/{companyId}`
* **List of Companies:** `GET /crm/v3/objects/companies`
* **Batch Read:** `POST /crm/v3/objects/companies/batch/read` (cannot retrieve associations)


**Query Parameters:**

* **`properties`:** Comma-separated list of properties to return.
* **`propertiesWithHistory`:** Comma-separated list of properties to return, including historical values.
* **`associations`:** Comma-separated list of associated objects to retrieve IDs for.
* **`idProperty` (Batch Read Only):**  Use a custom unique identifier property instead of the record ID (`hs_object_id`).


**Example Batch Read Request Body (JSON - using record IDs):**

```json
{
  "properties": ["name", "domain"],
  "inputs": [
    { "id": "56789" },
    { "id": "23456" }
  ]
}
```

**Example Batch Read Request Body (JSON - using a custom unique property):**

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

**Example Batch Read Request Body (JSON - current and historical values):**

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

* **Individual Company:** `PATCH /crm/v3/objects/companies/{companyId}`

**Note:** When updating `lifecyclestage`, you can only move *forward* in the stage order. To move backward, clear the existing value manually, via a workflow, or through an integration.


## Associate Existing Companies

Associate a company with other CRM records or activities:

`PUT /crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

Retrieve `associationTypeId` from [default values](link-to-default-association-types) or via `GET /crm/v4/associations/{fromObjectType}/{toObjectType}/labels`.  Learn more in the [associations API](link-to-associations-api).


## Remove an Association

Remove an association:

`DELETE /crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


## Pin an Activity

Pin an activity to a company record using the `hs_pinned_engagement_id` property (requires the activity ID from the [engagements APIs](link-to-engagements-api)).  Only one activity can be pinned per record; the activity must already be associated with the company.

**Example Request Body (JSON - PATCH request to update):**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```

**Example Request Body (JSON - POST request to create and pin):**

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

Delete companies individually or in batches (moves them to the recycling bin).  You can later [restore the company](link-to-restoring-companies) within HubSpot.

* **Individual Company:** `DELETE /crm/v3/objects/companies/{companyId}`

See the [reference documentation](link-to-batch-delete-docs) for batch deletion.


**(Remember to replace placeholder links like `link-to-understanding-crm-guide` with the actual links.)**
