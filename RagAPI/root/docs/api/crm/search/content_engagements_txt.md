# HubSpot CRM API Search Documentation

This document details the HubSpot CRM API's search functionality, allowing you to filter, sort, and search across CRM objects and engagements.  A CRM scope is required for app usage. Refer to the [HubSpot scope list](<Insert Link to HubSpot Scope List Here>) for details.


## API Endpoints

CRM search endpoints follow this format:

`/crm/v3/objects/{object}/search`

where `{object}` represents the CRM object type (e.g., `contacts`, `companies`, `deals`).


## Making a Search Request

Use a `POST` request to the object's search endpoint. The request body contains filters to refine the search.

**Example (Search Contacts with HubSpot Email):**

```json
{
  "filterGroups": [
    {
      "filters": [
        {
          "propertyName": "email",
          "operator": "CONTAINS_TOKEN",
          "value": "*@hubspot.com"
        }
      ]
    }
  ]
}
```

**Response:**

The response includes `total` results and an array of `results`. Each result contains an `id`, `properties` (object properties), `createdAt`, `updatedAt`, and `archived` status.

```json
{
  "total": 2,
  "results": [
    {
      "id": "100451",
      "properties": {
        "createdate": "2024-01-17T19:55:04.281Z",
        "email": "testperson@hubspot.com",
        "firstname": "Test",
        "hs_object_id": "100451",
        "lastmodifieddate": "2024-09-11T13:27:39.356Z",
        "lastname": "Person"
      },
      "createdAt": "2024-01-17T19:55:04.281Z",
      "updatedAt": "2024-09-11T13:27:39.356Z",
      "archived": false
    },
    // ... more results
  ]
}
```

To specify returned properties, include a `properties` array in the request body:

**Example (Search Companies, return only `annualrevenue` and `name`):**

```json
{
  "filterGroups": [
    {
      "filters": [
        {
          "propertyName": "annualrevenue",
          "operator": "GT",
          "value": "10000000"
        }
      ]
    }
  ],
  "properties": ["annualrevenue", "name"]
}
```


## Searchable Objects and Engagements

### Objects

| Search Endpoint                     | Object       | Default Returned Properties                                                              |
|--------------------------------------|---------------|------------------------------------------------------------------------------------------|
| `/crm/v3/objects/carts/search`      | Carts         | `createdate`, `hs_lastmodifieddate`, `hs_object_id`                                     |
| `/crm/v3/objects/companies/search`   | Companies     | `name`, `domain`, `createdate`, `hs_lastmodifieddate`, `hs_object_id`                     |
| `/crm/v3/objects/contacts/search`    | Contacts      | `firstname`, `lastname`, `email`, `lastmodifieddate`, `hs_object_id`, `createdate`       |
| `/crm/v3/objects/deals/search`       | Deals         | `dealname`, `amount`, `closedate`, `pipeline`, `dealstage`, `createdate`, `hs_lastmodifieddate`, `hs_object_id` |
| `/crm/v3/objects/deal_split/search` | Deal splits   | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`                                 |
| ...                                  | ...           | ...                                                                                      |


### Engagements

| Search Endpoint                 | Engagement | Default Returned Properties                                                        |
|---------------------------------|-------------|------------------------------------------------------------------------------------|
| `/crm/v3/objects/calls/search`   | Calls       | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`                             |
| `/crm/v3/objects/emails/search`  | Emails      | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`                             |
| ...                             | ...         | ...                                                                                |


## Default Searchable Properties

A full list of default searchable properties for each object is provided in the original text, but is too extensive to fully reproduce here.  The text indicates that custom objects support up to 20 selected properties.


## Filtering Search Results

Use `filterGroups` and `filters` within the request body.

* **AND logic:** Comma-separated conditions within one `filters` array.
* **OR logic:** Multiple `filters` arrays within a `filterGroup`.

**Maximums:** 5 `filterGroups`, 6 `filters` per group (18 total filters).

**Operators:**

| Operator          | Description                                      |
|----------------------|--------------------------------------------------|
| `LT`               | Less than                                        |
| `LTE`              | Less than or equal to                             |
| `GT`               | Greater than                                       |
| `GTE`              | Greater than or equal to                           |
| `EQ`               | Equal to                                          |
| `NEQ`              | Not equal to                                       |
| `BETWEEN`          | Within a range (use `highValue` and `value`)       |
| `IN`               | In a list (use `values` array; lowercase strings) |
| `NOT_IN`           | Not in a list (use `values` array; lowercase strings) |
| `HAS_PROPERTY`     | Has a value for the property                      |
| `NOT_HAS_PROPERTY` | Does not have a value for the property             |
| `CONTAINS_TOKEN`   | Contains a token (wildcards * supported)          |
| `NOT_CONTAINS_TOKEN` | Does not contain a token                         |


## Searching Through Associations

Use the pseudo-property `associations.{objectType}` (e.g., `associations.contact`).  Custom object associations are not currently supported.


## Sorting Search Results

Use the `sorts` array.  Only one sort rule is allowed.


## Paging Through Results

Default page size is 10. Use `limit` (max 200) to change. Use `after` (integer) from `paging.next.after` in the previous response to get subsequent pages.


## Limitations

* Delay in reflecting newly created/updated objects.
* Archived objects are not included.
* Rate limit: 5 requests per second.
* Maximum 200 objects per page.
* Query length limit: 3000 characters.
* Maximum 10,000 total results per query.
* Phone number search uses standardized properties (`hs_searchable_calculated_*`), area code and local number only.


This documentation provides a comprehensive overview of the HubSpot CRM API search functionality.  Remember to replace `"YOUR_ACCESS_TOKEN"` with your actual access token in the cURL examples.
