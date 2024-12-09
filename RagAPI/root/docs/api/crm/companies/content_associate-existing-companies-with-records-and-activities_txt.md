# HubSpot CRM API: Companies

This document details the HubSpot API endpoints for managing company records.  Companies in HubSpot store information about organizations interacting with your business.  These endpoints allow you to create, manage, and synchronize company data between HubSpot and other systems.

For a broader understanding of HubSpot objects, records, properties, and associations, refer to the [Understanding the CRM](<link_to_understanding_crm_guide>) guide.  For general CRM database management, see [how to manage your CRM database](<link_to_crm_database_management>).


## Create Companies

Use a `POST` request to `/crm/v3/objects/companies` to create new companies.  Include company data within a `properties` object. You can also add an `associations` object to link the new company with existing records (contacts, deals) or activities (meetings, notes).

**Properties:**

Company details are stored in properties.  HubSpot provides default properties, and you can create custom ones.  When creating a company, include at least one of the following:

* `name`
* `domain` (Recommended – primary unique identifier to prevent duplicates)

If a company has multiple domains, use the `hs_additional_domains` field, separating domains with semicolons (e.g., `"hs_additional_domains" : "domain.com; domain2.com; domain3.com"`).

To view available properties, use a `GET` request to `/crm/v3/properties/companies`.  See the [properties API](<link_to_properties_api>) for more details.

**Important Note on `lifecyclestage`:** If included, values must use the lifecycle stage's *internal name*, not the label.  Default stages have text internal names (e.g., `"subscriber"`, `"marketingqualifiedlead"`), while custom stages use numeric IDs. Find the internal ID in your lifecycle stage settings or via the API.


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

When creating a company, associate it with existing records or activities using the `associations` object.

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
      "to": { "id": 101 },
      "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 280 } ]
    },
    {
      "to": { "id": 556677 },
      "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 185 } ]
    }
  ]
}
```

**Parameters:**

* `to.id`:  The ID of the record or activity to associate.
* `types`:  The association type.  Includes `associationCategory` and `associationTypeId`.  See [default association type IDs](<link_to_default_association_types>) or use the [associations API](<link_to_associations_api>) for custom types.


## Retrieve Companies

Retrieve companies individually or in batches.

**Individual Company:**

Use a `GET` request to `/crm/v3/objects/companies/{companyId}`.

**List of All Companies:**

Use a `GET` request to `/crm/v3/objects/companies`.

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties (current and historical) to return.
* `associations`: Comma-separated list of associated objects to retrieve IDs for.  See the [associations API](<link_to_associations_api>).

**Batch Retrieval:**

Use a `POST` request to `/crm/v3/objects/companies/batch/read` to retrieve a batch of companies by record ID or a custom unique identifier property.  This endpoint *does not* retrieve associations. Use the [associations API](<link_to_associations_api>) for batch association retrieval.

* `idProperty`: (Optional)  Use a custom unique identifier property instead of the record ID (`hs_object_id`).


**Example Request Body (Batch, by record ID):**

```json
{
  "properties": ["name", "domain"],
  "inputs": [ { "id": "56789" }, { "id": "23456" } ]
}
```

**Example Request Body (Batch, by custom unique property):**

```json
{
  "properties": ["name", "domain"],
  "idProperty": "uniquepropertyexample",
  "inputs": [ { "id": "abc" }, { "id": "def" } ]
}
```


**Example Request Body (Batch, historical values):**

```json
{
  "propertiesWithHistory": ["name"],
  "inputs": [ { "id": "56789" }, { "id": "23456" } ]
}
```


## Update Companies

Update companies individually or in batches. Use the company's record ID for updates.

**Individual Company:**

Use a `PATCH` request to `/crm/v3/objects/companies/{companyId}`.

**Important Note on `lifecyclestage`:** You can only update `lifecyclestage` *forward* in the stage order. To move backward, first clear the existing value manually, via a workflow, or through an integration.

## Associate Existing Companies

Associate a company with other CRM records or activities using a `PUT` request to `/crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`.  Retrieve `associationTypeId` from the [default list](<link_to_default_association_types>) or via a `GET` request to `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`. See the [associations API](<link_to_associations_api>) for details.

## Remove an Association

Use a `DELETE` request to `/crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}` to remove an association.


## Pin an Activity

Pin an activity to a company record using the `hs_pinned_engagement_id` field (containing the activity ID, retrieved via the [engagements APIs](<link_to_engagements_api>)).  Only one activity can be pinned per record; the activity must already be associated.

**Example Request Body (PATCH):**

```json
{
  "properties": { "hs_pinned_engagement_id": 123456789 }
}
```

You can also create, associate, and pin in a single `POST` request:

**Example Request Body (POST):**

```json
{
  "properties": {
    "domain": "example.com",
    "name": "Example Company",
    "hs_pinned_engagement_id": 123456789
  },
  "associations": [
    // ... association details ...
  ]
}
```


## Delete Companies

Delete companies individually or in batches (moving them to the recycling bin). You can later restore them within HubSpot.

**Individual Company:**

Use a `DELETE` request to `/crm/v3/objects/companies/{companyId}`.

See the [reference documentation](<link_to_batch_delete_docs>) for batch deletion.


**Remember to replace placeholder links (`<link_to...>`) with the actual URLs.**
