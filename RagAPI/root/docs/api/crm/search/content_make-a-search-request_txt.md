# HubSpot CRM API Search Documentation

This document details the HubSpot CRM API's search functionality, allowing you to filter, sort, and search across various CRM objects and engagements.  A CRM scope is required to use these endpoints from an application. Refer to the [HubSpot API scope documentation](link_to_scopes_doc_here) for details.


## API Endpoints

CRM search endpoints follow this format:

`/crm/v3/objects/{object}/search`

Where `{object}` is the specific CRM object type (e.g., `contacts`, `companies`, `deals`).


## Making a Search Request

Use a `POST` request to the appropriate search endpoint. The request body contains filters, sorting rules, paging parameters, and property selection.


### Request Body Parameters

* **`filterGroups` (array):**  Groups filters using logical AND/OR operations.  Each `filterGroup` is an object containing an array of `filters`.

    * **`filters` (array):** An array of filter objects. Each filter object specifies a property, operator, and value.

        * **`propertyName` (string):** The name of the CRM property to filter on.
        * **`operator` (string):** The comparison operator.  See the "Filter Operators" section below.
        * **`value` (string/number):** The value to compare against. For `IN` and `NOT_IN` operators, this is an array of values (`values`). For `BETWEEN`, this is a lower bound value, and a `highValue` is also required.

* **`properties` (array, optional):**  Specifies which properties to return in the response. If omitted, default properties are returned.

* **`sorts` (array, optional):** Specifies the sorting rule. Only one sorting rule is allowed.

    * **`propertyName` (string):** The property to sort by.
    * **`direction` (string):**  `ASCENDING` or `DESCENDING`.

* **`limit` (integer, optional):** Specifies the number of results per page (max 200, default 10).

* **`after` (integer, optional):** Used for pagination.  Specify the `paging.next.after` value from the previous response to retrieve the next page.
* **`query` (string, optional):** Searches all default text properties for records containing this string.

### Filter Operators

| Operator       | Description                                      | Example                               |
|-----------------|--------------------------------------------------|---------------------------------------|
| `LT`           | Less than                                        | `"value": 10`                         |
| `LTE`          | Less than or equal to                             | `"value": 10`                         |
| `GT`           | Greater than                                       | `"value": 10`                         |
| `GTE`          | Greater than or equal to                           | `"value": 10`                         |
| `EQ`           | Equal to                                          | `"value": "Alice"`                    |
| `NEQ`          | Not equal to                                       | `"value": "Smith"`                    |
| `BETWEEN`      | Between a range (requires `highValue`)           | `"value": 1000, "highValue": 2000`     |
| `IN`           | In a list (values in `values` array)              | `"values": ["value1", "value2"]`     |
| `NOT_IN`       | Not in a list (values in `values` array)         | `"values": ["value1", "value2"]`     |
| `HAS_PROPERTY` | Has a value for the specified property           | (No value needed)                     |
| `NOT_HAS_PROPERTY` | Doesn't have a value for the specified property | (No value needed)                     |
| `CONTAINS_TOKEN` | Contains a token (wildcards * supported)        | `"value": "*@example.com"`           |
| `NOT_CONTAINS_TOKEN` | Does not contain a token (wildcards * supported) | `"value": "*@example.com"`           |


### Example Request (Contacts with email containing "@hubspot.com")

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

### Example Response

```json
{
  "total": 2,
  "results": [
    {
      "id": "100451",
      "properties": {
        "createdate": "2024-01-17T19:55:04.281Z",
        "email": "testperson@hubspot.com",
        // ... other properties
      },
      "createdAt": "2024-01-17T19:55:04.281Z",
      "updatedAt": "2024-09-11T13:27:39.356Z",
      "archived": false
    },
    // ... more results
  ],
  "paging": {
    "next": {
      "after": 10
    }
  }
}
```


## Searchable Objects and Engagements

The following tables list searchable objects, their default returned properties, and default searchable properties.  Note that default searchable properties for custom objects are limited to 20 selected properties.

### Objects

| Search Endpoint                      | Object       | Default Returned Properties                                                              |
|--------------------------------------|---------------|------------------------------------------------------------------------------------------|
| `/crm/v3/objects/carts/search`       | Carts         | `createdate`, `hs_lastmodifieddate`, `hs_object_id`                                      |
| `/crm/v3/objects/companies/search`   | Companies     | `name`, `domain`, `createdate`, `hs_lastmodifieddate`, `hs_object_id`                     |
| `/crm/v3/objects/contacts/search`    | Contacts      | `firstname`, `lastname`, `email`, `lastmodifieddate`, `hs_object_id`, `createdate`         |
| `/crm/v3/objects/deals/search`       | Deals         | `dealname`, `amount`, `closedate`, `pipeline`, `dealstage`, `createdate`, `hs_lastmodifieddate`, `hs_object_id` |
| `/crm/v3/objects/deal_split/search` | Deal splits   | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`                                  |
| ... (other objects) ...             | ...           | ...                                                                                    |


### Engagements

| Search Endpoint                    | Engagement  | Default Returned Properties                                         |
|------------------------------------|-------------|---------------------------------------------------------------------|
| `/crm/v3/objects/calls/search`     | Calls       | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`              |
| `/crm/v3/objects/emails/search`    | Emails      | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`              |
| `/crm/v3/objects/meetings/search`  | Meetings    | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`              |
| `/crm/v3/objects/notes/search`     | Notes       | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`              |
| `/crm/v3/objects/tasks/search`     | Tasks       | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`              |


## Searching Through Associations

Search for records associated with other records using the pseudo-property `associations.{objectType}`. For example, to find tickets associated with contact ID 123:

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

## Rate Limits and Limitations

* 5 requests per second.
* Maximum 200 objects per page.
* Maximum 3,000 characters in the query.
* Maximum 10,000 total results per query.
* Maximum 5 `filterGroups`, each with up to 6 `filters` (18 total filters).


This documentation provides a comprehensive overview of HubSpot's CRM API search functionality. Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
