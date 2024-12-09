# HubSpot CRM API: Companies

This document details the HubSpot Companies API, allowing you to manage company records within HubSpot.  You can create, retrieve, update, and delete company records, as well as manage associations between companies and other HubSpot objects.

## Understanding Companies in HubSpot

In HubSpot, companies store information about organizations that interact with your business.  The Companies API allows for seamless management of company data and synchronization with external systems.  For a broader understanding of HubSpot's object, record, property, and association APIs, refer to the [Understanding the CRM](link-to-understanding-crm-guide) guide.  For general CRM database management, see [Managing your CRM database](link-to-crm-database-management).


## API Endpoints

All endpoints are under the `/crm/v3/objects/companies` base path unless otherwise specified.

### Create Companies

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/companies`

Creates a new company record.  The request body must include a `properties` object containing company data.  You can optionally include an `associations` object to associate the new company with existing records (contacts, deals, etc.) or activities (meetings, notes, etc.).

**Required Properties:** At least one of `name` or `domain` is required.  It's strongly recommended to always include `domain` as it's the primary unique identifier.  Multiple domains can be added using the `hs_additional_domains` field (e.g., `"hs_additional_domains": "domain.com;domain2.com"`).

**Example Request Body:**

```json
{
  "properties": {
    "name": "HubSpot",
    "domain": "hubspot.com",
    "city": "Cambridge",
    "industry": "Technology",
    "phone": "555-555-555",
    "state": "Massachusetts",
    "lifecyclestage": "51439524" // Note: Use internal lifecycle stage name or ID
  }
}
```

**Lifecycle Stage Note:** When including `lifecyclestage`, use the internal name (e.g., `"subscriber"`, `"marketingqualifiedlead"`) for default stages or the numeric ID for custom stages.  You can find the ID in your lifecycle stage settings or by retrieving the property via API.


### Properties

Company details are stored in properties.  HubSpot provides default properties, and you can also create custom properties.  To view all available properties, use a `GET` request to `/crm/v3/properties/companies`.  Learn more about the [Properties API](link-to-properties-api).


### Associations

When creating or updating a company, you can associate it with existing records or activities using the `associations` object.

**Example Request Body (with associations):**

```json
{
  "properties": {
    "name": "HubSpot",
    "domain": "hubspot.com"
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

* `to.id`: The ID of the record or activity to associate.
* `types`: An array of association types.  `associationCategory` and `associationTypeId` are required.  Default association type IDs are listed [here](link-to-association-type-ids), or you can retrieve custom association types via the [Associations API](link-to-associations-api).


### Retrieve Companies

**Individual Company:**

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/companies/{companyId}`

Retrieves a single company by its ID.

**All Companies:**

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/companies`

Retrieves a list of all companies.

**Query Parameters (for both individual and all companies):**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `associations`: Comma-separated list of associated objects to retrieve IDs for.

**Batch Retrieval:**

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/companies/batch/read`

Retrieves a batch of companies by record ID or a custom unique identifier property.  Associations cannot be retrieved using this endpoint.  Use the `idProperty` parameter to specify a custom unique identifier property; otherwise, it defaults to `hs_object_id`.

**Example Request Body (Batch, using record IDs):**

```json
{
  "properties": ["name", "domain"],
  "inputs": [ { "id": "56789" }, { "id": "23456" } ]
}
```

**Example Request Body (Batch, using custom unique identifier property):**

```json
{
  "properties": ["name", "domain"],
  "idProperty": "uniquepropertyexample",
  "inputs": [ { "id": "abc" }, { "id": "def" } ]
}
```


### Update Companies

**Individual Company:**

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/companies/{companyId}`

Updates an existing company.  Include only the properties you wish to modify.

**Lifecycle Stage Note (Update):**  When updating `lifecyclestage`, you can only move forward in the stage order. To move backward, clear the existing value first (manually, via workflow, or integration).


### Associate Existing Companies

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

Associates an existing company with other CRM records or activities.

### Remove Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

Removes an association between a company and another object.


### Pin an Activity

To pin an activity to a company record, include the `hs_pinned_engagement_id` property with the activity's ID in a `PATCH` request (or in a `POST` request when creating a new company).

**Example Request Body (PATCH):**

```json
{
  "properties": { "hs_pinned_engagement_id": 123456789 }
}
```

### Delete Companies

**Individual Company:**

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/companies/{companyId}`

Deletes a company (moves it to the recycling bin).  See the [reference documentation](link-to-batch-delete-docs) for batch deletion.


This markdown provides a comprehensive overview of the HubSpot Companies API. Remember to replace placeholder links (e.g., `link-to-understanding-crm-guide`) with the actual links to the relevant HubSpot documentation.
