# HubSpot CRM API Search Documentation

This document details the HubSpot CRM API search endpoints, allowing you to filter, sort, and search objects, records, and engagements across your CRM.  A CRM scope is required to use these endpoints from an app.  Refer to the [HubSpot API Scopes documentation](<insert_link_here>) for details.

## API Endpoints

CRM search endpoints follow this format:

`/crm/v3/objects/{object}/search`

Where `{object}` represents the CRM object type (e.g., `contacts`, `companies`, `deals`).  Separate endpoints exist for engagements (calls, emails, meetings, notes, tasks).


## Making a Search Request

Use a `POST` request to the object's search endpoint. The request body contains filters, sorting rules, and pagination parameters.

### Request Body Parameters

* **`filterGroups` (array):**  Groups filters using AND/OR logic.  Each `filterGroup` is an object containing an array of `filters`.
    * **`filters` (array):**  An array of filter objects. Each filter object requires:
        * **`propertyName` (string):** The name of the CRM property to filter on.  See "Searchable CRM Objects and Engagements" section for defaults.
        * **`operator` (string):** The comparison operator. See "Filter Operators" section for available operators.
        * **`value` (string/number/array):** The value to compare against.  The type depends on the property and operator.  For `IN` and `NOT_IN` operators on string properties, values must be lowercase.  For `BETWEEN`, use `highValue` and `value` for the range.
* **`properties` (array, optional):** Specifies which properties to return in the response. If omitted, default properties are returned.
* **`sorts` (array, optional):**  An array of sorting rules. Only one sorting rule is allowed. Each sort object requires:
    * **`propertyName` (string):** The property to sort by.
    * **`direction` (string):** `"ASCENDING"` or `"DESCENDING"`.
* **`limit` (integer, optional):** The number of results per page (maximum 200, default 10).
* **`after` (integer, optional):**  Used for pagination.  Specify the `paging.next.after` value from the previous response to get the next page.
* **`query` (string, optional):** Search all default text properties for records containing the specified string.


### Example Request (Contacts with email containing "@hubspot.com"):

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

### Example Request (Companies with annual revenue > $10,000,000, returning only `annualrevenue` and `name`):

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

The API returns a JSON object with:

* **`total` (integer):** The total number of matching records.
* **`results` (array):** An array of matching records. Each record is an object with:
    * **`id` (string):** The ID of the record.
    * **`properties` (object):** An object containing the requested properties and their values.
    * **`createdAt` (string):** The creation timestamp.
    * **`updatedAt` (string):** The last update timestamp.
    * **`archived` (boolean):** Whether the record is archived.
* **`paging` (object, optional):**  Contains pagination information, including `next.after` for retrieving subsequent pages.


### Example Response:

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

## Searchable CRM Objects and Engagements

### Objects

| Search Endpoint                     | Object      | Default Returned Properties                                                                |
|--------------------------------------|-------------|-------------------------------------------------------------------------------------------|
| `/crm/v3/objects/carts/search`      | Carts       | `createdate`, `hs_lastmodifieddate`, `hs_object_id`                                     |
| `/crm/v3/objects/companies/search`   | Companies   | `name`, `domain`, `createdate`, `hs_lastmodifieddate`, `hs_object_id`                    |
| `/crm/v3/objects/contacts/search`    | Contacts    | `firstname`, `lastname`, `email`, `lastmodifieddate`, `hs_object_id`, `createdate`        |
| `/crm/v3/objects/deals/search`      | Deals       | `dealname`, `amount`, `closedate`, `pipeline`, `dealstage`, `createdate`, `hs_lastmodifieddate`, `hs_object_id` |
| `/crm/v3/objects/deal_split/search` | Deal splits | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`                                   |
| ... (more objects) ...              | ...         | ...                                                                                     |


### Engagements

| Search Endpoint                 | Engagement | Default Returned Properties                                                        |
|---------------------------------|-------------|------------------------------------------------------------------------------------|
| `/crm/v3/objects/calls/search`  | Calls       | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`                             |
| `/crm/v3/objects/emails/search` | Emails      | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`                             |
| ... (more engagements) ...      | ...         | ...                                                                              |


## Default Searchable Properties

These properties are searched by default when using the `query` parameter.

| Search Endpoint                     | Object      | Default Searchable Properties                                                            |
|--------------------------------------|-------------|----------------------------------------------------------------------------------------|
| `/crm/v3/objects/calls/search`      | Calls       | `hs_call_title`, `hs_body_preview`                                                    |
| `/crm/v3/objects/companies/search`   | Companies   | `website`, `phone`, `name`, `domain`                                                  |
| `/crm/v3/objects/contacts/search`    | Contacts    | `firstname`, `lastname`, `email`, `phone`, `hs_additional_emails`, `fax`, `mobilephone`, `company`, `hs_marketable_until_renewal` |
| `/crm/v3/objects/{objectType}/search` | Custom Objects | Up to 20 selected properties.                                                        |
| ... (more objects) ...              | ...         | ...                                                                                  |


## Filter Operators

| Operator          | Description                                      |
|-------------------|--------------------------------------------------|
| `LT`              | Less than                                        |
| `LTE`             | Less than or equal to                             |
| `GT`              | Greater than                                     |
| `GTE`             | Greater than or equal to                          |
| `EQ`              | Equal to                                         |
| `NEQ`             | Not equal to                                      |
| `BETWEEN`         | Within a specified range (`highValue`, `value`) |
| `IN`              | Included in a list (`values` array)              |
| `NOT_IN`          | Not included in a list (`values` array)           |
| `HAS_PROPERTY`    | Has a value for the property                     |
| `NOT_HAS_PROPERTY` | Does not have a value for the property            |
| `CONTAINS_TOKEN`  | Contains a token (wildcards allowed)              |
| `NOT_CONTAINS_TOKEN` | Does not contain a token                         |


## Search Through Associations

Use the pseudo-property `associations.{objectType}` to search for records associated with other records.  Example: `associations.contact`

**Note:** Searching through custom object associations is not currently supported.


## Pagination

The API returns pages of results. Use the `limit` parameter to control the page size (max 200) and the `after` parameter to retrieve subsequent pages.


## Limitations

* Newly created/updated objects may take time to appear in search results.
* Archived objects are not included in search results.
* Rate limit: 5 requests per second.
* Maximum 200 objects per page.
* Maximum query length: 3000 characters.
* Maximum total results: 10,000.
* Maximum filters: 18 (5 `filterGroups`, up to 6 `filters` per group).
* Phone number search uses standardized calculated properties (starting with `hs_searchable_calculated_*`).  Do not include country codes.

This documentation provides a comprehensive overview of the HubSpot CRM API search functionality.  Refer to the official HubSpot API documentation for the most up-to-date information and detailed examples.
