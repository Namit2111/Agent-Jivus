# HubSpot CRM API Search Documentation

This document details the HubSpot CRM API's search functionality, allowing you to filter, sort, and search across various objects and engagements within your CRM.  A CRM scope is required to utilize these endpoints from an application. Refer to the [list of available scopes](link-to-scopes-documentation-here) for details.


## API Endpoints

CRM search endpoints follow this format:

`/crm/v3/objects/{object}/search`

where `{object}` represents the CRM object type (e.g., `contacts`, `companies`, `deals`).


## Making a Search Request

To perform a search, send a `POST` request to the appropriate endpoint with the search criteria in the request body.


### Request Body Parameters

The request body accepts several parameters to refine your search:

* **`filterGroups` (array):**  Groups filters using AND/OR logic.  Each `filterGroup` can contain multiple `filters`.  A maximum of five `filterGroups` with up to six `filters` each (18 total filters) is allowed.

    * **`filters` (array):**  Each filter specifies a property, operator, and value.
        * **`propertyName` (string):** The name of the CRM property to filter on.  For associations, use `associations.{objectType}` (e.g., `associations.contact`).  Custom object associations are not currently supported.
        * **`operator` (string):** The comparison operator.  See the "Filter Operators" section below.
        * **`value` (string or number):** The value to compare against. For `IN` and `NOT_IN` operators, use a `values` array instead. For `BETWEEN`, use `highValue` and `value` for the range.
        * **`values` (array, optional):**  Used with `IN` and `NOT_IN` operators. Contains a list of values. String values for `IN` and `NOT_IN` must be lowercase.

* **`properties` (array, optional):** Specifies the properties to include in the response. If omitted, default properties are returned.

* **`query` (string, optional):** A search string that searches across default text properties for records containing the specified string.

* **`sorts` (array, optional):**  Specifies how to sort the results. Only one sorting rule is allowed.
    * **`propertyName` (string):** The property to sort by.
    * **`direction` (string):**  `ASCENDING` or `DESCENDING`.

* **`limit` (integer, optional):** The number of results per page (max 200, default 10).

* **`after` (integer, optional):**  Used for pagination.  Specifies the starting record for the next page.  Obtained from the `paging.next.after` property in the previous response.


### Example Request (Contacts):

```json
{
  "filterGroups": [
    {
      "filters": [
        {
          "propertyName": "email",
          "operator": "CONTAINS_TOKEN",
          "value": "*@example.com"
        }
      ]
    }
  ],
  "properties": ["email", "firstname", "lastname"],
  "sorts": [
    {
      "propertyName": "createdate",
      "direction": "DESCENDING"
    }
  ],
  "limit": 20
}
```

This example searches for contacts with emails containing "@example.com", returns only email, firstname and lastname properties, sorts by creation date (newest first), and returns 20 results per page.


### Example using cURL:

```bash
curl https://api.hubapi.com/crm/v3/objects/contacts/search \
  --request POST \
  --header "Content-Type: application/json" \
  --header "authorization: Bearer YOUR_ACCESS_TOKEN" \
  --data '{
    "filterGroups": [ ... ]
  }'
```
Replace `YOUR_ACCESS_TOKEN` with your actual HubSpot access token.


## Response

The API returns a JSON object with the following structure:

```json
{
  "total": <number_of_total_results>,
  "results": [
    {
      "id": <record_id>,
      "properties": {
        // CRM properties and their values
      },
      "createdAt": <creation_timestamp>,
      "updatedAt": <update_timestamp>,
      "archived": <boolean>
    },
    // ... more results
  ],
  "paging": {
    "next": {
      "after": <next_page_start_integer>
    }
  }
}
```

* **`total`:** The total number of matching records.
* **`results`:** An array of matching records.  Each record includes its ID, properties, creation timestamp, update timestamp, and archived status.
* **`paging`:**  Pagination information.  `paging.next.after` provides the `after` value for fetching the next page.



## Searchable Objects and Engagements

The following tables list the searchable objects and engagements, along with their default returned and searchable properties:

**Objects:**

| Search Endpoint                     | Object       | Default Returned Properties                                                              |
|--------------------------------------|---------------|---------------------------------------------------------------------------------------------|
| `/crm/v3/objects/carts/search`      | Carts         | `createdate`, `hs_lastmodifieddate`, `hs_object_id`                                         |
| `/crm/v3/objects/companies/search`   | Companies     | `name`, `domain`, `createdate`, `hs_lastmodifieddate`, `hs_object_id`                       |
| `/crm/v3/objects/contacts/search`    | Contacts      | `firstname`, `lastname`, `email`, `lastmodifieddate`, `hs_object_id`, `createdate`           |
| `/crm/v3/objects/deals/search`       | Deals         | `dealname`, `amount`, `closedate`, `pipeline`, `dealstage`, `createdate`, `hs_lastmodifieddate`, `hs_object_id` |
| `/crm/v3/objects/deal_split/search` | Deal splits   | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`                                   |
| ... (other objects) ...             | ...           | ...                                                                                       |


**Engagements:**

| Search Endpoint                    | Engagement   | Default Returned Properties                                                              |
|------------------------------------|---------------|---------------------------------------------------------------------------------------------|
| `/crm/v3/objects/calls/search`     | Calls         | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`                                   |
| `/crm/v3/objects/emails/search`    | Emails        | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`                                   |
| `/crm/v3/objects/meetings/search`  | Meetings      | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`                                   |
| ... (other engagements) ...       | ...           | ...                                                                                       |


*(Note:  The full list of objects and engagements with their respective properties is included in the original text.)*


## Filter Operators

| Operator          | Description                                                                     |
|----------------------|---------------------------------------------------------------------------------|
| `LT`              | Less than                                                                       |
| `LTE`             | Less than or equal to                                                            |
| `GT`              | Greater than                                                                      |
| `GTE`             | Greater than or equal to                                                        |
| `EQ`              | Equal to                                                                        |
| `NEQ`             | Not equal to                                                                     |
| `BETWEEN`         | Within a specified range (requires `highValue` and `value`)                     |
| `IN`              | Included in a list (requires `values` array; string values must be lowercase)  |
| `NOT_IN`          | Not included in a list (requires `values` array; string values must be lowercase)|
| `HAS_PROPERTY`    | Has a value for the specified property                                          |
| `NOT_HAS_PROPERTY` | Does not have a value for the specified property                               |
| `CONTAINS_TOKEN`  | Contains a token (wildcards (*) are supported)                                |
| `NOT_CONTAINS_TOKEN` | Does not contain a token                                                      |


## Limitations

* Newly created or updated objects may take time to appear in search results.
* Archived objects are not included in search results.
* Rate limit: 5 requests per second.
* Maximum objects per page: 200.
* Maximum query length: 3,000 characters.
* Maximum total results: 10,000.
* Maximum filterGroups: 5, with a maximum of 6 filters per group (18 total filters).
* Phone number search uses standardized properties (`hs_searchable_calculated_*`) and ignores country codes.


This documentation provides a comprehensive overview of the HubSpot CRM API search functionality. Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
