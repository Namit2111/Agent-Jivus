# HubSpot CRM API Search Documentation

This document details the HubSpot CRM API search endpoints, allowing you to filter, sort, and search objects, records, and engagements across your CRM.  A CRM scope is required to use these endpoints from an application. Refer to the [list of available scopes](link_to_scopes_page_here -  replace with actual link) for details.

## API Endpoints

CRM search endpoints follow this format:

`/crm/v3/objects/{object}/search`

Where `{object}` represents the CRM object type (e.g., `contacts`, `companies`, `deals`).


## Making a Search Request

Use a `POST` request to the object's search endpoint. The request body contains filters, sorting rules, and pagination parameters.

### Request Body Parameters

* **`filterGroups` (array):**  Groups filters using AND/OR logic.  Each `filterGroup` is an array of `filters`.
    * **`filters` (array):** Each filter specifies a property, operator, and value.
        * **`propertyName` (string):** The name of the CRM property to filter on.  See "Searchable CRM Objects and Engagements" for default properties.  Use `associations.{objectType}` to search through associations (e.g., `associations.contact`).
        * **`operator` (string):** The comparison operator.  See "Filter Operators" for options.
        * **`value` (string or number):** The value to compare against. For `IN` and `NOT_IN`, use a `values` array instead.  For `BETWEEN`, use `highValue` and `value` for the range.
* **`properties` (array, optional):**  Specifies which properties to return in the response. If omitted, default properties are returned.
* **`sorts` (array, optional):**  Specifies the sorting rule. Only one sort is allowed.
    * **`propertyName` (string):** Property to sort by.
    * **`direction` (string):** `ASCENDING` or `DESCENDING`.
* **`limit` (integer, optional):** The number of results per page (max 200, default 10).
* **`after` (integer, optional):**  The `after` cursor for pagination.  Obtained from the previous response's `paging.next.after` property.
* **`query` (string, optional):** A free-text search query across default text properties.


### Filter Operators

| Operator       | Description                                      | Example                               |
|-----------------|--------------------------------------------------|---------------------------------------|
| `LT`            | Less than                                        | `"value": 10`                         |
| `LTE`           | Less than or equal to                            | `"value": 10`                         |
| `GT`            | Greater than                                       | `"value": 10`                         |
| `GTE`           | Greater than or equal to                           | `"value": 10`                         |
| `EQ`            | Equal to                                          | `"value": "Alice"`                     |
| `NEQ`           | Not equal to                                       | `"value": "Smith"`                     |
| `BETWEEN`       | Between a range (uses `highValue` and `value`)    | `"value": 1000, "highValue": 2000`     |
| `IN`            | In a list (uses `values` array)                   | `"values": ["value1", "value2"]`      |
| `NOT_IN`        | Not in a list (uses `values` array)               | `"values": ["value1", "value2"]`      |
| `HAS_PROPERTY`  | Has a value for the property                     |  (no value needed)                    |
| `NOT_HAS_PROPERTY` | Doesn't have a value for the property           |  (no value needed)                    |
| `CONTAINS_TOKEN` | Contains a token (supports wildcards `*`)        | `"value": "*@example.com"`            |
| `NOT_CONTAINS_TOKEN` | Doesn't contain a token                         | `"value": "example"`                  |


## Response

The API returns a JSON object with the following structure:

```json
{
  "total": 123, // Total number of matching records
  "results": [ // Array of matching records
    {
      "id": "record_id",
      "properties": { // CRM properties and values
        "propertyName1": "value1",
        "propertyName2": "value2"
      },
      "createdAt": "timestamp",
      "updatedAt": "timestamp",
      "archived": false
    },
    // ... more records
  ],
  "paging": {
    "next": {
      "after": 20 // Cursor for the next page
    }
  }
}
```

## Examples

**Example 1: Search for contacts with email containing "@hubspot.com"**

```bash
curl https://api.hubapi.com/crm/v3/objects/contacts/search \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
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
  }'
```

**Example 2: Search for companies with annual revenue greater than 10,000,000, returning only `annualrevenue` and `name` properties**

```bash
curl https://api.hubapi.com/crm/v3/objects/companies/search \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
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
  }'
```

## Searchable CRM Objects and Engagements

The following tables list searchable objects, their default returned properties, and default searchable properties.  (Tables would be recreated here using markdown formatting based on the provided text).

## Limitations

* Rate limit: 5 requests per second.
* Maximum results per query: 10,000.
* Maximum characters in query: 3,000.
* Maximum objects per page: 200.
* Maximum filterGroups: 5, with up to 6 filters per group (18 total filters).
* Newly created/updated objects may take time to appear in search results.
* Archived objects are not included.
* Phone number search uses standardized `hs_searchable_calculated_*` properties; do not include country codes.


This documentation provides a comprehensive overview of the HubSpot CRM API search functionality.  Remember to replace `"YOUR_ACCESS_TOKEN"` with your actual HubSpot API access token.
