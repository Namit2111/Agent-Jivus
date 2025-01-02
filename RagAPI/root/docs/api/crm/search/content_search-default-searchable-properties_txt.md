# HubSpot CRM API Search Documentation

This document details the HubSpot CRM API search endpoints, allowing you to filter, sort, and search objects, records, and engagements across your CRM.  A CRM scope is required to use these endpoints from an app.  Refer to the [list of available scopes](<insert_link_here>) for details.

## API Endpoints

CRM search endpoints follow this format:

`/crm/v3/objects/{object}/search`

Where `{object}` represents the CRM object type (e.g., `contacts`, `companies`, `deals`).

## Making a Search Request

Use a `POST` request to the object's search endpoint.  The request body includes filters to narrow the search.

### Request Body Parameters

* **`filterGroups` (array):**  Groups filters logically using AND/OR operations.  A maximum of five `filterGroups` are allowed, each containing up to six filters (18 total).

    * **`filters` (array):**  Individual filter criteria within a `filterGroup`.
        * **`propertyName` (string):** The CRM property to filter on.
        * **`operator` (string):** The comparison operator (see Operator section below).
        * **`value` (string/number):** The value to compare against.  For `IN` and `NOT_IN` operators, use a `values` array instead.
        * **`highValue` (number):** Used with the `BETWEEN` operator to specify the upper bound of the range.


* **`properties` (array, optional):**  Specifies the properties to return in the response. If omitted, default properties are returned (see Searchable Objects section).

* **`query` (string, optional):** Searches all default text properties for records containing the specified string.

* **`sorts` (array, optional):** Sorts the results. Only one sort rule is allowed.
    * **`propertyName` (string):** The property to sort by.
    * **`direction` (string):**  `ASCENDING` or `DESCENDING`.

* **`limit` (integer, optional):**  Specifies the number of results per page (max 200, default 10).
* **`after` (integer, optional):**  Used for pagination.  Specify the `paging.next.after` value from the previous response to retrieve the next page.


### Operators

| Operator        | Description                                      | Example                                  |
|-----------------|--------------------------------------------------|------------------------------------------|
| `LT`            | Less than                                         | `"value": 10`                            |
| `LTE`           | Less than or equal to                             | `"value": 10`                            |
| `GT`            | Greater than                                      | `"value": 10`                            |
| `GTE`           | Greater than or equal to                          | `"value": 10`                            |
| `EQ`            | Equal to                                          | `"value": "Alice"`                        |
| `NEQ`           | Not equal to                                       | `"value": "Smith"`                        |
| `BETWEEN`       | Within a range                                    | `"value": 1000, "highValue": 2000`       |
| `IN`            | Included in a list (string values must be lowercase)| `"values": ["value1", "value2"]`         |
| `NOT_IN`        | Not included in a list (string values must be lowercase) | `"values": ["value1", "value2"]`         |
| `HAS_PROPERTY`  | Has a value for the property                     |                                          |
| `NOT_HAS_PROPERTY` | Does not have a value for the property            |                                          |
| `CONTAINS_TOKEN`| Contains a token (wildcards * supported)         | `"value": "*@example.com"`              |
| `NOT_CONTAINS_TOKEN` | Does not contain a token                         | `"value": "example"`                     |


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

### Example Request (Companies with annual revenue > 10,000,000, returning only `annualrevenue` and `name`)

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


## Response

The response is a JSON object with the following structure:

```json
{
  "total": <total_number_of_results>,
  "results": [
    {
      "id": <object_id>,
      "properties": {
        // CRM properties and their values
      },
      "createdAt": <creation_timestamp>,
      "updatedAt": <last_update_timestamp>,
      "archived": <boolean>
    },
    // ... more results
  ],
  "paging": {
    "next": {
      "after": <next_page_token>
    }
  }
}
```

## Searchable CRM Objects and Engagements

The following tables list searchable objects, their default returned properties, and default searchable properties.

### Objects

| Search Endpoint                      | Object       | Default Returned Properties                                                                     |
|--------------------------------------|---------------|------------------------------------------------------------------------------------------------|
| `/crm/v3/objects/carts/search`       | Carts         | `createdate`, `hs_lastmodifieddate`, `hs_object_id`                                           |
| `/crm/v3/objects/companies/search`   | Companies     | `name`, `domain`, `createdate`, `hs_lastmodifieddate`, `hs_object_id`                             |
| `/crm/v3/objects/contacts/search`    | Contacts      | `firstname`, `lastname`, `email`, `lastmodifieddate`, `hs_object_id`, `createdate`                 |
| `/crm/v3/objects/deals/search`       | Deals         | `dealname`, `amount`, `closedate`, `pipeline`, `dealstage`, `createdate`, `hs_lastmodifieddate`, `hs_object_id` |
| `/crm/v3/objects/deal_split/search` | Deal splits   | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`                                         |
| ...  (more objects) ...             | ...           | ...                                                                                           |


### Engagements

| Search Endpoint                 | Engagement | Default Returned Properties                                                                 |
|---------------------------------|-------------|---------------------------------------------------------------------------------------------|
| `/crm/v3/objects/calls/search`   | Calls       | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`                                     |
| `/crm/v3/objects/emails/search`  | Emails      | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`                                     |
| ... (more engagements) ...      | ...         | ...                                                                                       |


### Default Searchable Properties (Examples)

| Search Endpoint                      | Object       | Default Searchable Properties                                                             |
|--------------------------------------|---------------|-----------------------------------------------------------------------------------------|
| `/crm/v3/objects/companies/search`   | Companies     | `website`, `phone`, `name`, `domain`                                                     |
| `/crm/v3/objects/contacts/search`    | Contacts      | `firstname`, `lastname`, `email`, `phone`, `hs_additional_emails`, `fax`, `mobilephone`, `company`, `hs_marketable_until_renewal` |
| `/crm/v3/objects/{objectType}/search` | Custom objects | Up to 20 selected properties.                                                           |


## Searching Through Associations

Search for records associated with other records using the pseudo-property `associations.{objectType}`.  For example, to find tickets associated with contact ID 123:

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

**Note:** Searching through custom object associations is not currently supported.


## Pagination

The API returns pages of results. Use the `limit` parameter to control the page size (max 200). Use the `after` parameter in subsequent requests to fetch the next page using the `paging.next.after` value from the previous response.


## Rate Limiting and Limitations

* 5 requests per second.
* Maximum 10,000 total results per query.
* Maximum query length: 3,000 characters.
* Newly created/updated objects might have a delay before appearing in search results.
* Archived objects are not included in search results.


This documentation provides a comprehensive overview of the HubSpot CRM API search functionality.  Remember to replace placeholders like `<insert_link_here>` and `YOUR_ACCESS_TOKEN` with actual values.  Consult the official HubSpot API documentation for the most up-to-date information.
