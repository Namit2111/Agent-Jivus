# HubSpot CRM API Search Documentation

This document details the HubSpot CRM API search endpoints, allowing you to filter, sort, and search objects, records, and engagements across your CRM.  A CRM scope is required to use these endpoints from an app. Refer to the [list of available scopes](<insert_link_here>) for details.

## API Endpoints

CRM search endpoints follow this format:

`/crm/v3/objects/{object}/search`

Where `{object}` represents the CRM object type (e.g., `contacts`, `companies`, `deals`).

## Making a Search Request

Use a `POST` request to the object's search endpoint.  The request body contains filters to narrow your search.

**Example (Contacts): Find contacts with email at hubspot.com**

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

The response includes the total number of results and an array of results. Each result contains an `id`, `properties`, `createdAt`, `updatedAt`, and `archived` status.


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

**Specifying Returned Properties:**

Include a `properties` array in the request body to specify which properties to return.

**Example (Companies): Find companies with annual revenue > $10,000,000 and return only `annualrevenue` and `name`**

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

| Search Endpoint                     | Object       | Default Returned Properties                                                                 |
|--------------------------------------|---------------|---------------------------------------------------------------------------------------------|
| `/crm/v3/objects/carts/search`      | Carts         | `createdate`, `hs_lastmodifieddate`, `hs_object_id`                                         |
| `/crm/v3/objects/companies/search`   | Companies     | `name`, `domain`, `createdate`, `hs_lastmodifieddate`, `hs_object_id`                       |
| `/crm/v3/objects/contacts/search`    | Contacts      | `firstname`, `lastname`, `email`, `lastmodifieddate`, `hs_object_id`, `createdate`            |
| `/crm/v3/objects/deals/search`       | Deals         | `dealname`, `amount`, `closedate`, `pipeline`, `dealstage`, `createdate`, `hs_lastmodifieddate`, `hs_object_id` |
| `/crm/v3/objects/deal_split/search` | Deal splits   | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`                                     |
| ...                                  | ...           | ...                                                                                       |


### Engagements

| Search Endpoint                  | Engagement  | Default Returned Properties                                               |
|----------------------------------|--------------|---------------------------------------------------------------------------|
| `/crm/v3/objects/calls/search`   | Calls        | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`                     |
| `/crm/v3/objects/emails/search`  | Emails       | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`                     |
| `/crm/v3/objects/meetings/search` | Meetings     | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`                     |
| `/crm/v3/objects/notes/search`   | Notes        | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`                     |
| `/crm/v3/objects/tasks/search`   | Tasks        | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`                     |


## Default Searchable Properties

A full list of default searchable properties for each object type is provided in the original text.  These properties are searched when using the `query` parameter.

## Filtering Search Results

Use `filterGroups` and `filters` in the request body to filter results.  Each `filterGroup` can contain multiple filters which are combined with AND logic.  Multiple `filterGroups` are combined with OR logic.


**Operators:**

| Operator         | Description                                     |
|-----------------|-------------------------------------------------|
| LT               | Less than                                      |
| LTE              | Less than or equal to                           |
| GT               | Greater than                                     |
| GTE              | Greater than or equal to                        |
| EQ               | Equal to                                        |
| NEQ              | Not equal to                                     |
| BETWEEN          | Within a specified range (requires `highValue` and `value`) |
| IN               | Included in a list (values in a `values` array) |
| NOT_IN           | Not included in a list (values in a `values` array) |
| HAS_PROPERTY     | Has a value for the property                   |
| NOT_HAS_PROPERTY | Does not have a value for the property          |
| CONTAINS_TOKEN   | Contains a token (wildcards * supported)       |
| NOT_CONTAINS_TOKEN | Does not contain a token                        |


## Searching Through Associations

Use the pseudo-property `associations.{objectType}` to search for records associated with other records.  (e.g., `associations.contact`).


## Sorting Search Results

Use the `sorts` array in the request body to sort results.  Only one sort rule is allowed.

## Paging Through Results

The default page size is 10.  Use the `limit` parameter (max 200) to change this. Use the `after` parameter (from `paging.next.after` in the previous response) to get subsequent pages.


## Limitations

* Newly created/updated objects may take time to appear in search results.
* Archived objects are not included.
* Rate limit: 5 requests per second.
* Maximum objects per page: 200.
* Maximum query length: 3000 characters.
* Maximum total results: 10,000.
* Maximum filterGroups: 5, maximum filters per group: 6, maximum total filters: 18.
* Phone number search uses standardized properties (`hs_searchable_calculated_*`), ignoring country codes.


This markdown documentation provides a comprehensive overview of the HubSpot CRM API search functionality.  Remember to replace placeholders like `<insert_link_here>` with actual links where applicable.
