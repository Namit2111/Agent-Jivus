# HubSpot CRM API Search Documentation

This document details the HubSpot CRM API's search functionality, allowing you to filter, sort, and search across various CRM objects and engagements.  A CRM scope is required to use these endpoints from an app.  Refer to the [list of available scopes](link_to_scopes_documentation_here -  replace with actual link) for details.


## I. Making a Search Request

To initiate a search, send a `POST` request to the object's search endpoint, formatted as:

`/crm/v3/objects/{object}/search`

where `{object}` represents the CRM object type (e.g., `contacts`, `companies`, `deals`).

The request body utilizes `filterGroups` to specify search criteria.


### A. Example: Searching Contacts by Email

This example retrieves contacts with emails containing "*@hubspot.com":

**Request:**

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

**Response:** (Example)

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
    {
      "id": "57156923994",
      "properties": {
        "createdate": "2024-09-11T18:21:50.012Z",
        "email": "emailmaria@hubspot.com",
        "firstname": "Maria",
        "hs_object_id": "57156923994",
        "lastmodifieddate": "2024-10-21T21:36:02.961Z",
        "lastname": "Johnson (Sample Contact)"
      },
      "createdAt": "2024-09-11T18:21:50.012Z",
      "updatedAt": "2024-10-21T21:36:02.961Z",
      "archived": false
    }
  ]
}
```


### B. Specifying Returned Properties

Include a `properties` array in the request body to specify which properties to retrieve.  If omitted, default properties are returned.

**Example (Companies):**

**Request:**

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


## II. Searchable Objects and Engagements

### A. Objects

| Search Endpoint                 | Object       | Default Returned Properties                                           |
|---------------------------------|---------------|-----------------------------------------------------------------------|
| `/crm/v3/objects/carts/search`  | Carts         | `createdate`, `hs_lastmodifieddate`, `hs_object_id`                  |
| `/crm/v3/objects/companies/search` | Companies     | `name`, `domain`, `createdate`, `hs_lastmodifieddate`, `hs_object_id` |
| `/crm/v3/objects/contacts/search` | Contacts      | `firstname`, `lastname`, `email`, `lastmodifieddate`, `hs_object_id`, `createdate` |
| `/crm/v3/objects/deals/search`   | Deals         | `dealname`, `amount`, `closedate`, `pipeline`, `dealstage`, `createdate`, `hs_lastmodifieddate`, `hs_object_id` |
| ... (other objects) ...         | ...           | ...                                                                   |


### B. Engagements

| Search Endpoint                | Engagement   | Default Returned Properties                                      |
|--------------------------------|---------------|-----------------------------------------------------------------|
| `/crm/v3/objects/calls/search` | Calls         | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`           |
| `/crm/v3/objects/emails/search` | Emails        | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`           |
| ... (other engagements) ...    | ...           | ...                                                             |



## III.  Advanced Search Options

### A. Default Searchable Properties

A simple `query` string can search across default text properties.

**Example (Contacts):**

```bash
curl https://api.hubapi.com/crm/v3/objects/contacts/search \
--request POST \
--header "Content-Type: application/json" \
--header "authorization: Bearer YOUR_ACCESS_TOKEN" \
--data '{ "query": "x" }'
```


### B. Filtering

Use `filterGroups` and `filters` to refine results based on property values.  Operators control the comparison (e.g., `EQ`, `GT`, `CONTAINS_TOKEN`).


### C.  Operators

| Operator         | Description                                          |
|-----------------|------------------------------------------------------|
| `LT`             | Less than                                           |
| `LTE`            | Less than or equal to                                |
| `GT`             | Greater than                                          |
| `GTE`            | Greater than or equal to                              |
| `EQ`             | Equal to                                             |
| `NEQ`            | Not equal to                                          |
| `BETWEEN`        | Within a range (uses `highValue` and `value`)         |
| `IN`             | Included in a list (values in `values` array)        |
| `NOT_IN`         | Not included in a list (values in `values` array)     |
| `HAS_PROPERTY`   | Has a value for the property                         |
| `NOT_HAS_PROPERTY` | Does not have a value for the property               |
| `CONTAINS_TOKEN` | Contains a token (wildcards * supported)              |
| `NOT_CONTAINS_TOKEN` | Does not contain a token                             |


### D. Searching Through Associations

Use `associations.{objectType}` to search for records associated with others.

**Example (Tickets associated with Contact ID 123):**

```bash
curl https://api.hubapi.com/crm/v3/objects/tickets/search \
--request POST \
--header "Content-Type: application/json" \
--header "authorization: Bearer YOUR_ACCESS_TOKEN" \
--data '{
  "filters": [
    {
      "propertyName": "associations.contact",
      "operator": "EQ",
      "value": "123"
    }
  ]
}'
```

### E. Sorting

Use the `sorts` array to specify sorting by property and direction (`ASCENDING` or `DESCENDING`).  Only one sort rule is allowed per request.


### F. Paging

The default page size is 10. Use the `limit` parameter to adjust (max 200).  Use the `after` parameter (from `paging.next.after` in the previous response) to retrieve subsequent pages.


## IV. Limitations

* Newly created/updated objects may take time to appear in search results.
* Archived objects are not included.
* Rate limit: 5 requests per second.
* Maximum objects per page: 200.
* Maximum query length: 3000 characters.
* Maximum total results: 10,000.
* Maximum filterGroups: 5, filters per group: 6, total filters: 18.
* Phone number search uses standardized properties (starting with `hs_searchable_calculated_*`), and country codes are ignored.


This documentation provides a comprehensive overview of the HubSpot CRM API search functionality.  Remember to replace `"Bearer YOUR_ACCESS_TOKEN"` with your actual access token.  Refer to the HubSpot Developer documentation for the most up-to-date information and details.
