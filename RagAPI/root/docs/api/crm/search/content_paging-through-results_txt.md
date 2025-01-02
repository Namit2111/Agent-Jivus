# HubSpot CRM API Search Documentation

This document details the HubSpot CRM API search endpoints, allowing you to filter, sort, and search objects, records, and engagements across your CRM.  A CRM scope is required to use these endpoints from an app. Refer to the [list of available scopes](<insert_link_here>) for details.


## API Endpoints

CRM search endpoints follow this format:

`/crm/v3/objects/{object}/search`

where `{object}` represents the CRM object type (e.g., `contacts`, `companies`, `deals`).


## Making a Search Request

To search, send a `POST` request to the object's search endpoint with the search criteria in the request body.


### Request Body Parameters

* **`query` (string, optional):**  A search string to match against default searchable properties. Results are returned in order of object creation (oldest first) unless overridden with sorting.

* **`filterGroups` (array of objects, optional):** An array of filter groups.  Each group can contain multiple filters using AND logic within a group and OR logic between groups.  Maximum 5 `filterGroups` with up to 6 filters each (18 total filters).

    * **`filters` (array of objects):**  An array of filter objects.

        * **`propertyName` (string):** The name of the CRM property to filter on.  Use `associations.{objectType}` to filter by associated objects.
        * **`operator` (string):** The comparison operator. See the "Filter Operators" section below.
        * **`value` (string):** The value to compare against.  For `IN` and `NOT_IN`, use a `values` array instead. For `BETWEEN`, use `highValue` and `value`.

* **`properties` (array of strings, optional):**  An array of property names to return in the response. If omitted, default properties are returned.

* **`sorts` (array of objects, optional):** An array containing a single sorting rule.

    * **`propertyName` (string):** The property to sort by.
    * **`direction` (string):** `ASCENDING` or `DESCENDING`.

* **`limit` (integer, optional):** The number of results per page (max 200, default 10).

* **`after` (integer, optional):**  Used for pagination.  Provide the `paging.next.after` value from the previous response to retrieve the next page.



### Example Request (Contacts):

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
  ],
  "properties": ["email", "firstname", "lastname"],
  "limit": 20,
  "sorts": [
    {
      "propertyName": "createdate",
      "direction": "DESCENDING"
    }
  ]
}
```

This example searches contacts whose email contains "@hubspot.com", returns only email, firstname, and lastname, limits results to 20 per page, and sorts by creation date (newest first).


### Example cURL Request (Contacts):

```bash
curl https://api.hubapi.com/crm/v3/objects/contacts/search \
  --request POST \
  --header "Content-Type: application/json" \
  --header "authorization: Bearer YOUR_ACCESS_TOKEN" \
  --data '{
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
Replace `YOUR_ACCESS_TOKEN` with your actual access token.


## Response

The response is a JSON object with the following structure:

```json
{
  "total": <integer>, // Total number of matching records
  "results": [
    {
      "id": <string>, // ID of the record
      "properties": {
        // CRM properties and their values
      },
      "createdAt": <string>, // ISO 8601 timestamp
      "updatedAt": <string>, // ISO 8601 timestamp
      "archived": <boolean> // True if archived, otherwise false
    },
    // ... more results
  ],
  "paging": {
    "next": {
      "after": <integer> //  Use this value in the 'after' parameter for pagination
    }
  }
}
```


## Searchable Objects and Engagements

The following tables list searchable objects and their default properties:

### Objects

| Search Endpoint             | Object      | Default Returned Properties                                      |
|-----------------------------|-------------|-----------------------------------------------------------------|
| `/crm/v3/objects/carts/search` | Carts       | `createdate`, `hs_lastmodifieddate`, `hs_object_id`            |
| `/crm/v3/objects/companies/search` | Companies   | `name`, `domain`, `createdate`, `hs_lastmodifieddate`, `hs_object_id` |
| `/crm/v3/objects/contacts/search` | Contacts    | `firstname`, `lastname`, `email`, `lastmodifieddate`, `hs_object_id`, `createdate` |
| `/crm/v3/objects/deals/search` | Deals       | `dealname`, `amount`, `closedate`, `pipeline`, `dealstage`, `createdate`, `hs_lastmodifieddate`, `hs_object_id` |
| `/crm/v3/objects/deal_split/search` | Deal Splits | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`          |
| `/crm/v3/objects/discounts/search` | Discounts   | `createdate`, `hs_lastmodifieddate`, `hs_object_id`            |
| `/crm/v3/objects/feedback_submissions/search` | Feedback Submissions | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`          |
| `/crm/v3/objects/fees/search` | Fees        | `createdate`, `hs_lastmodifieddate`, `hs_object_id`            |
| `/crm/v3/objects/invoices/search` | Invoices    | `createdate`, `hs_lastmodifieddate`, `hs_object_id`            |
| `/crm/v3/objects/leads/search` | Leads       | `createdate`, `hs_lastmodifieddate`, `hs_object_id`            |
| `/crm/v3/objects/line_items/search` | Line Items  | `quantity`, `amount`, `price`, `createdate`, `hs_lastmodifieddate`, `hs_object_id` |
| `/crm/v3/objects/orders/search` | Orders      | `createdate`, `hs_lastmodifieddate`, `hs_object_id`            |
| `/crm/v3/objects/commerce_payments/search` | Payments    | `createdate`, `hs_lastmodifieddate`, `hs_object_id`            |
| `/crm/v3/objects/products/search` | Products    | `name`, `description`, `price`, `createdate`, `hs_lastmodifieddate`, `hs_object_id` |
| `/crm/v3/objects/quotes/search` | Quotes      | `hs_expiration_date`, `hs_public_url_key`, `hs_status`, `hs_title`, `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id` |
| `/crm/v3/objects/subscriptions/search` | Subscriptions (Commerce) | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`          |
| `/crm/v3/objects/taxes/search` | Taxes       | `createdate`, `hs_lastmodifieddate`, `hs_object_id`            |
| `/crm/v3/objects/tickets/search` | Tickets     | `content`, `hs_pipeline`, `hs_pipeline_stage`, `hs_ticket_category`, `hs_ticket_priority`, `subject`, `createdate`, `hs_lastmodifieddate`, `hs_object_id` |


### Engagements

| Search Endpoint             | Engagement  | Default Returned Properties                               |
|-----------------------------|-------------|-----------------------------------------------------------|
| `/crm/v3/objects/calls/search` | Calls       | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`     |
| `/crm/v3/objects/emails/search` | Emails      | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`     |
| `/crm/v3/objects/meetings/search` | Meetings    | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`     |
| `/crm/v3/objects/notes/search` | Notes       | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`     |
| `/crm/v3/objects/tasks/search` | Tasks       | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`     |


## Default Searchable Properties

These properties are searched by default when using the `query` parameter:  A full list is provided in the original text,  but it varies by object type.


## Filter Operators

| Operator          | Description                                      |
|----------------------|--------------------------------------------------|
| `LT`               | Less than                                         |
| `LTE`              | Less than or equal to                             |
| `GT`               | Greater than                                        |
| `GTE`              | Greater than or equal to                            |
| `EQ`               | Equal to                                          |
| `NEQ`              | Not equal to                                       |
| `BETWEEN`          | Within a specified range (uses `highValue` and `value`) |
| `IN`               | Included in a list (uses `values` array)           |
| `NOT_IN`           | Not included in a list (uses `values` array)        |
| `HAS_PROPERTY`     | Has a value for the specified property             |
| `NOT_HAS_PROPERTY` | Does not have a value for the specified property    |
| `CONTAINS_TOKEN`   | Contains a token (wildcards * supported)          |
| `NOT_CONTAINS_TOKEN` | Does not contain a token                          |


## Search Through Associations

Search for records associated with other records using the `associations.{objectType}` pseudo-property.  (Custom object associations are not currently supported).


## Pagination

Results are returned in pages. Use the `limit` parameter to control page size (max 200) and the `after` parameter for pagination.


## Limitations

* Newly created/updated objects may take time to appear in search results.
* Archived objects are not included in search results.
* Rate limit: 5 requests per second.
* Maximum 200 objects per page.
* Query maximum length: 3,000 characters.
* Maximum 10,000 total results per query.
* Maximum 18 filters (5 filterGroups, 6 filters per group).
* Phone number search uses standardized `hs_searchable_calculated_*` properties, ignoring country codes.

This documentation provides a comprehensive overview of the HubSpot CRM API search functionality.  Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
