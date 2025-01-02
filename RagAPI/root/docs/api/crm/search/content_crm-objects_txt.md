# HubSpot CRM API Search Documentation

This document details the HubSpot CRM API search endpoints, allowing you to filter, sort, and search across CRM objects, records, and engagements.  A CRM scope is required to use these endpoints from an app. Refer to the [list of available scopes](<insert_link_here>) for details.

## API Endpoints

CRM search endpoints follow this format:

`/crm/v3/objects/{object}/search`

Where `{object}` represents the CRM object type (e.g., `contacts`, `companies`, `deals`).


## Making a Search Request

Use a `POST` request to the object's search endpoint. The request body uses JSON to specify filters, properties to return, sorting, pagination, and more.

### Request Body Parameters

* **`filterGroups` (array):**  Groups filters using AND/OR logic.  Each `filterGroup` contains an array of `filters`.  Maximum 5 `filterGroups`, each with up to 6 `filters` (18 total filters max).

    * **`filters` (array, within `filterGroups`):**  Each filter specifies a property, operator, and value.
        * **`propertyName` (string):** The name of the CRM property to filter on.  `associations.{objectType}` can be used to filter by associated objects.
        * **`operator` (string):** The comparison operator.  See the "Filter Operators" section below.
        * **`value` (string or number):** The value to compare against.  For `IN` and `NOT_IN`, use a `values` array instead.  For `BETWEEN`, use `highValue` and `value`.
        * **`values` (array, optional):** Used with `IN` and `NOT_IN` operators.


* **`properties` (array, optional):** Specifies which properties to return in the response.  If omitted, default properties are returned.

* **`query` (string, optional):** Searches all default text properties for records containing the specified string (case-insensitive).

* **`sorts` (array, optional):** Specifies sorting. Only one sort rule allowed.
    * **`propertyName` (string):** Property to sort by.
    * **`direction` (string):** `ASCENDING` or `DESCENDING`.

* **`limit` (integer, optional):**  Specifies the number of results per page (max 200, default 10).

* **`after` (integer, optional):**  Used for pagination.  Specifies the starting point for the next page of results.  Obtained from the `paging.next.after` field in the previous response.


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

### Example Request (Companies with annual revenue > $10,000,000 and returning only `annualrevenue` and `name`)

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

The response is a JSON object with the following fields:

* **`total` (integer):** The total number of matching records.

* **`results` (array):** An array of matching records.  Each record contains:
    * **`id` (string):** The ID of the record.
    * **`properties` (object):**  An object containing the requested properties and their values.
    * **`createdAt` (string):**  The creation timestamp of the record.
    * **`updatedAt` (string):** The last modification timestamp of the record.
    * **`archived` (boolean):** Indicates whether the record is archived.

* **`paging` (object, optional):** Contains pagination information, including `next.after` for accessing the next page.


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

The following tables list searchable objects, their default returned properties, and default searchable properties for text-based searches using the `query` parameter.


### Objects

| Search Endpoint                      | Object      | Default Returned Properties                                                                  |
|--------------------------------------|-------------|----------------------------------------------------------------------------------------------|
| `/crm/v3/objects/carts/search`       | Carts        | `createdate`, `hs_lastmodifieddate`, `hs_object_id`                                         |
| `/crm/v3/objects/companies/search`    | Companies    | `name`, `domain`, `createdate`, `hs_lastmodifieddate`, `hs_object_id`                         |
| `/crm/v3/objects/contacts/search`     | Contacts     | `firstname`, `lastname`, `email`, `lastmodifieddate`, `hs_object_id`, `createdate`             |
| `/crm/v3/objects/deals/search`       | Deals        | `dealname`, `amount`, `closedate`, `pipeline`, `dealstage`, `createdate`, `hs_lastmodifieddate`, `hs_object_id` |
| `/crm/v3/objects/deal_split/search` | Deal splits  | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`                                     |
| ... (other objects) ...             | ...          | ...                                                                                        |


### Engagements

| Search Endpoint                 | Engagement | Default Returned Properties                                         |
|---------------------------------|-------------|--------------------------------------------------------------------|
| `/crm/v3/objects/calls/search`   | Calls       | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`             |
| `/crm/v3/objects/emails/search`  | Emails      | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`             |
| `/crm/v3/objects/meetings/search` | Meetings    | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`             |
| `/crm/v3/objects/notes/search`   | Notes       | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`             |
| `/crm/v3/objects/tasks/search`   | Tasks       | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`             |


### Default Searchable Properties (for `query` parameter)

| Search Endpoint                      | Object      | Default Searchable Properties                                                                     |
|--------------------------------------|-------------|-------------------------------------------------------------------------------------------------|
| `/crm/v3/objects/calls/search`       | Calls        | `hs_call_title`, `hs_body_preview`                                                             |
| `/crm/v3/objects/companies/search`    | Companies    | `website`, `phone`, `name`, `domain`                                                            |
| `/crm/v3/objects/contacts/search`     | Contacts     | `firstname`, `lastname`, `email`, `phone`, `hs_additional_emails`, `fax`, `mobilephone`, `company`, `hs_marketable_until_renewal` |
| `/crm/v3/objects/{objectType}/search` | Custom Objects | Up to 20 selected properties.                                                                  |
| ... (other objects) ...             | ...          | ...                                                                                         |


## Filter Operators

| Operator          | Description                                      |
|----------------------|--------------------------------------------------|
| `LT`              | Less than                                         |
| `LTE`             | Less than or equal to                              |
| `GT`              | Greater than                                        |
| `GTE`             | Greater than or equal to                           |
| `EQ`              | Equal to                                           |
| `NEQ`             | Not equal to                                        |
| `BETWEEN`         | Within a specified range (use `highValue` and `value`) |
| `IN`              | Included in a list (use `values` array)             |
| `NOT_IN`          | Not included in a list (use `values` array)         |
| `HAS_PROPERTY`    | Has a value for the property                       |
| `NOT_HAS_PROPERTY` | Doesn't have a value for the property              |
| `CONTAINS_TOKEN`  | Contains a token (wildcards * supported)           |
| `NOT_CONTAINS_TOKEN` | Does not contain a token                          |


##  Searching Through Associations

Use the `associations.{objectType}` pseudo-property to search for records associated with other records.  For example: `associations.contact`


##  Rate Limits and Limitations

* 5 requests per second.
* Maximum 200 objects per page.
* Maximum 3,000 characters in the query body.
* Maximum 10,000 total results per query.
* Maximum 5 `filterGroups` with up to 6 `filters` each (18 total filters).

Newly created or updated objects may take time to appear in search results. Archived objects are not included.  When searching phone numbers, only the area code and local number are used.  Country codes should be omitted.
