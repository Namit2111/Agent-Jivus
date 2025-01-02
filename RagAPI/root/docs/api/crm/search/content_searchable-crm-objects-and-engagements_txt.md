# HubSpot CRM API Search Documentation

This document details the HubSpot CRM API search endpoints, allowing you to filter, sort, and search objects, records, and engagements across your CRM.  A CRM scope is required to use these endpoints from an app. Refer to the [list of available scopes](<insert_link_here>) for details.


## API Endpoints

CRM search endpoints follow this format:

`/crm/v3/objects/{object}/search`

where `{object}` represents the CRM object type (e.g., `contacts`, `companies`, `deals`).


## Making a Search Request

To search, make a `POST` request to the appropriate endpoint. The request body uses JSON to specify filters, properties to return, sorting, and pagination.


### Request Body Parameters

* **`filterGroups` (array):**  Groups filters using AND/OR logic.  Each `filterGroup` contains an array of `filters`.
    * **`filters` (array):**  Each filter defines a search criterion.
        * **`propertyName` (string):** The CRM property to filter on.
        * **`operator` (string):** The comparison operator (see Operator table below).
        * **`value` (string/number):** The value to compare against.  For `IN` and `NOT_IN`, use a `values` array instead.
        * **`highValue` (number):** Used with the `BETWEEN` operator for the upper bound.

* **`properties` (array, optional):**  Specifies which properties to return in the response.  If omitted, default properties are returned (see tables below).

* **`sorts` (array, optional):**  Specifies sorting criteria. Only one sort is allowed.
    * **`propertyName` (string):** The property to sort by.
    * **`direction` (string):**  `"ASCENDING"` or `"DESCENDING"`.

* **`limit` (integer, optional):**  Specifies the number of results per page (max 200, default 10).

* **`after` (integer, optional):**  Used for pagination.  Provides the ID of the last record from the previous page.


### Example Request (Contacts)

Find contacts with email address containing "@hubspot.com":

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

### Example Request (Companies, specifying properties)

Find companies with annual revenue greater than 10,000,000 and return only `annualrevenue` and `name`:

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

### Example using Associations

Find all tickets associated with contact ID 123:

```json
{
  "filters": [
    {
      "propertyName": "associations.contact",
      "operator": "EQ",
      "value": "123"
    }
  ]
}
```


## Response

The response is a JSON object with the following structure:

* **`total` (integer):** The total number of matching records.
* **`results` (array):** An array of matching records. Each record contains:
    * **`id` (string):** The ID of the record.
    * **`properties` (object):**  An object containing the requested properties and their values.
    * **`createdAt` (string):**  The creation timestamp.
    * **`updatedAt` (string):** The last update timestamp.
    * **`archived` (boolean):** Indicates whether the record is archived.
* **`paging` (object, optional):** Pagination information. Contains `next` object with `after` property for the next page.


### Example Response (Contacts)

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


## Searchable Objects and Engagements

### Objects

| Search Endpoint                     | Object       | Default Returned Properties                                           |
|--------------------------------------|---------------|-----------------------------------------------------------------------|
| `/crm/v3/objects/carts/search`      | Carts         | `createdate`, `hs_lastmodifieddate`, `hs_object_id`                   |
| `/crm/v3/objects/companies/search`   | Companies     | `name`, `domain`, `createdate`, `hs_lastmodifieddate`, `hs_object_id` |
| `/crm/v3/objects/contacts/search`    | Contacts      | `firstname`, `lastname`, `email`, `lastmodifieddate`, `hs_object_id`, `createdate` |
| `/crm/v3/objects/deals/search`      | Deals         | `dealname`, `amount`, `closedate`, `pipeline`, `dealstage`, `createdate`, `hs_lastmodifieddate`, `hs_object_id` |
| `/crm/v3/objects/deal_split/search` | Deal splits   | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`                |
| ...  (more objects) ...             | ...           | ...                                                                   |


### Engagements

| Search Endpoint                   | Engagement | Default Returned Properties                                       |
|------------------------------------|------------|-------------------------------------------------------------------|
| `/crm/v3/objects/calls/search`    | Calls      | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`           |
| `/crm/v3/objects/emails/search`   | Emails     | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`           |
| ...  (more engagements) ...       | ...        | ...                                                              |



## Default Searchable Properties

A `query` parameter can search all default text properties.  Results are ordered by creation date (oldest first) unless sorting is specified.

| Search Endpoint                     | Object       | Default Searchable Properties                                      |
|--------------------------------------|---------------|-------------------------------------------------------------------|
| `/crm/v3/objects/calls/search`      | Calls         | `hs_call_title`, `hs_body_preview`                               |
| `/crm/v3/objects/companies/search`   | Companies     | `website`, `phone`, `name`, `domain`                             |
| `/crm/v3/objects/contacts/search`    | Contacts      | `firstname`, `lastname`, `email`, `phone`, `hs_additional_emails`, `fax`, `mobilephone`, `company`, `hs_marketable_until_renewal` |
| ...  (more objects) ...             | ...           | ...                                                              |


## Filter Operators

| Operator         | Description                                     |
|-----------------|-------------------------------------------------|
| `LT`             | Less than                                      |
| `LTE`            | Less than or equal to                           |
| `GT`             | Greater than                                     |
| `GTE`            | Greater than or equal to                        |
| `EQ`             | Equal to                                        |
| `NEQ`            | Not equal to                                     |
| `BETWEEN`        | Between a range (use `value` and `highValue`)    |
| `IN`             | In a list (use `values` array, lowercase strings)|
| `NOT_IN`         | Not in a list (use `values` array, lowercase strings)|
| `HAS_PROPERTY`   | Has a value for the specified property          |
| `NOT_HAS_PROPERTY` | Does not have a value for the specified property |
| `CONTAINS_TOKEN` | Contains a token (wildcards * supported)        |
| `NOT_CONTAINS_TOKEN` | Does not contain a token                       |


## Pagination

Results are returned in pages. Use `limit` to control page size and `after` to retrieve subsequent pages.


## Limitations

* Newly created/updated objects may take time to appear in search results.
* Archived objects are not included.
* Rate limit: 5 requests per second.
* Maximum objects per page: 200.
* Maximum query length: 3000 characters.
* Maximum total results: 10,000.
* Maximum filters: 18 (5 `filterGroups`, 6 filters per group).
* Phone number search uses standardized properties (`hs_searchable_calculated_*`), ignoring country codes.

