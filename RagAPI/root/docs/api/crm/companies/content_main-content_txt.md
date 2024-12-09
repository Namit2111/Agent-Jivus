# HubSpot CRM API: Companies

This document details the HubSpot CRM API endpoints for managing companies.  Companies in HubSpot store information about organizations that interact with your business.  These endpoints allow you to create, manage, and synchronize company data between HubSpot and other systems.

## Understanding the Basics

Before using these APIs, familiarize yourself with:

* [Understanding the CRM](link_to_understanding_crm_guide): Learn about objects, records, properties, and associations in the HubSpot CRM.
* [Managing your CRM database](link_to_managing_crm_database): General information on managing your CRM database.


## API Endpoints

All endpoints are under the `/crm/v3/objects/companies` base path unless otherwise specified.


### Create Companies

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/companies`

**Request Body:**  JSON object containing:

* **`properties` (required):** An object containing company property data.  At least one of `name` or `domain` is required.  `domain` is strongly recommended as it's the primary unique identifier.  Multiple domains can be added using the `hs_additional_domains` property (e.g., `"hs_additional_domains" : "domain.com; domain2.com; domain3.com"`).  See [Properties](#properties) for details.
* **`associations` (optional):** An array of objects associating the new company with existing records or activities. See [Associations](#associations) for details.


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
    "lifecyclestage": "51439524"
  }
}
```

**Note on `lifecyclestage`:** If included, use the internal name (not the label).  Internal names for default stages are text values; for custom stages, they are numeric.


### Properties

Company details are stored as properties.  HubSpot provides default properties, but you can also create custom properties.  To view available properties:

**Method:** `GET`

**Endpoint:** `/crm/v3/properties/companies`


Learn more about the [properties API](link_to_properties_api).


### Associations

When creating or updating companies, you can associate them with existing records (contacts, deals, etc.) or activities (meetings, notes, etc.).

**In the `associations` object:**

| Parameter       | Description                                                                                                     |
|-----------------|-----------------------------------------------------------------------------------------------------------------|
| `to.id`         | The ID of the record or activity to associate.                                                                 |
| `types`         | An array of association types. Each object should contain `associationCategory` ("HUBSPOT_DEFINED") and `associationTypeId`. |


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
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 280 }]
    }
  ]
}
```

See the [associations API](link_to_associations_api) for details on association types.


### Retrieve Companies

**Retrieve Individual Company:**

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/companies/{companyId}`

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `associations`: Comma-separated list of associated objects to retrieve.


**Retrieve Multiple Companies (Batch):**

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/companies/batch/read`

**Request Body:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `inputs`: An array of objects, each containing an `id` (record ID or custom unique identifier).
* `idProperty` (optional):  The name of a custom unique identifier property if not using record IDs.


**Examples:**

(Record ID based retrieval):

```json
{
  "properties": ["name", "domain"],
  "inputs": [{"id": "56789"}, {"id": "23456"}]
}
```

(Custom unique identifier property retrieval):

```json
{
  "properties": ["name", "domain"],
  "idProperty": "uniquepropertyexample",
  "inputs": [{"id": "abc"}, {"id": "def"}]
}
```

Note: Batch retrieval cannot retrieve associations. Use the associations API for batch association retrieval.


### Update Companies

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/companies/{companyId}`

**Request Body:** JSON object containing properties to update.  Updating `lifecyclestage` only allows moving *forward* in the stage order.


### Associate Existing Companies

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

`associationTypeId` can be found in the list of default values or retrieved via `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`.


### Remove an Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


### Pin an Activity

To pin an activity to a company record, include the `hs_pinned_engagement_id` property (the ID of the activity) in your request.  Only one activity can be pinned per record.


**Example (in a PATCH request):**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```

You can also pin during company creation.


### Delete Companies

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/companies/{companyId}`

For batch deletion, refer to the [reference documentation](link_to_batch_delete_docs).



**(Remember to replace placeholder links like `link_to_understanding_crm_guide` with actual links from the HubSpot API documentation.)**
