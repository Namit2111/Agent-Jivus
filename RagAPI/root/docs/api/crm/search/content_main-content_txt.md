# HubSpot CRM API Search Documentation

This document details the HubSpot CRM API search endpoints, allowing you to filter, sort, and search objects, records, and engagements across your CRM.  A CRM scope is required to use these endpoints from an app.  Refer to the [HubSpot API Scopes documentation](<Insert Link to HubSpot API Scopes Here>) for details.

## API Endpoints

CRM search endpoints follow this format:

`/crm/v3/objects/{object}/search`

Where `{object}` represents the CRM object type (e.g., `contacts`, `companies`, `deals`).

## Making a Search Request

Search requests are made using a `POST` request to the object's search endpoint. The request body contains filters and other parameters to refine the search.

**Example:** Retrieve contacts with email addresses containing "@hubspot.com":

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

**Response:**  A successful response will be a JSON object with the following structure:

```json
{
  "total": 2, // Total number of matching records
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

| Search Endpoint                     | Object      | Default Returned Properties                                                              |
|--------------------------------------|-------------|------------------------------------------------------------------------------------------|
| `/crm/v3/objects/carts/search`       | Carts       | `createdate`, `hs_lastmodifieddate`, `hs_object_id`                                     |
| `/crm/v3/objects/companies/search`   | Companies   | `name`, `domain`, `createdate`, `hs_lastmodifieddate`, `hs_object_id`                     |
| `/crm/v3/objects/contacts/search`    | Contacts    | `firstname`, `lastname`, `email`, `lastmodifieddate`, `hs_object_id`, `createdate`       |
| `/crm/v3/objects/deals/search`       | Deals       | `dealname`, `amount`, `closedate`, `pipeline`, `dealstage`, `createdate`, `hs_lastmodifieddate`, `hs_object_id` |
| `/crm/v3/objects/deal_split/search` | Deal splits | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`                                 |
| `/crm/v3/objects/discounts/search`   | Discounts   | `createdate`, `hs_lastmodifieddate`, `hs_object_id`                                     |
| `/crm/v3/objects/feedback_submissions/search` | Feedback Submissions | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id` |
| `/crm/v3/objects/fees/search`        | Fees        | `createdate`, `hs_lastmodifieddate`, `hs_object_id`                                     |
| `/crm/v3/objects/invoices/search`    | Invoices    | `createdate`, `hs_lastmodifieddate`, `hs_object_id`                                     |
| `/crm/v3/objects/leads/search`       | Leads       | `createdate`, `hs_lastmodifieddate`, `hs_object_id`                                     |
| `/crm/v3/objects/line_items/search`  | Line items  | `quantity`, `amount`, `price`, `createdate`, `hs_lastmodifieddate`, `hs_object_id`       |
| `/crm/v3/objects/orders/search`      | Orders      | `createdate`, `hs_lastmodifieddate`, `hs_object_id`                                     |
| `/crm/v3/objects/commerce_payments/search` | Payments | `createdate`, `hs_lastmodifieddate`, `hs_object_id` |
| `/crm/v3/objects/products/search`    | Products    | `name`, `description`, `price`, `createdate`, `hs_lastmodifieddate`, `hs_object_id`       |
| `/crm/v3/objects/quotes/search`      | Quotes      | `hs_expiration_date`, `hs_public_url_key`, `hs_status`, `hs_title`, `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id` |
| `/crm/v3/objects/subscriptions/search` | Subscriptions (Commerce) | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id` |
| `/crm/v3/objects/taxes/search`      | Taxes       | `createdate`, `hs_lastmodifieddate`, `hs_object_id`                                     |
| `/crm/v3/objects/tickets/search`     | Tickets     | `content`, `hs_pipeline`, `hs_pipeline_stage`, `hs_ticket_category`, `hs_ticket_priority`, `subject`, `createdate`, `hs_lastmodifieddate`, `hs_object_id` |


### Engagements

| Search Endpoint                 | Engagement | Default Returned Properties                                         |
|---------------------------------|-------------|---------------------------------------------------------------------|
| `/crm/v3/objects/calls/search`   | Calls       | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`             |
| `/crm/v3/objects/emails/search`  | Emails      | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`             |
| `/crm/v3/objects/meetings/search`| Meetings    | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`             |
| `/crm/v3/objects/notes/search`   | Notes       | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`             |
| `/crm/v3/objects/tasks/search`   | Tasks       | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`             |


## Default Searchable Properties

A full list of default searchable properties for each object is available in the original text.  This varies greatly by object type.


## Filtering Search Results

Use `filterGroups` and `filters` within the request body to specify criteria.

* **AND** logic: Comma-separated conditions within one `filters` array.
* **OR** logic: Multiple `filters` arrays within a `filterGroup`.

Maximums: 5 `filterGroups`, 6 `filters` per group (18 total filters).

**Example:** Contacts with firstname "Alice" AND lastname not "Smith" OR no email:

```json
{
  "filterGroups": [
    {
      "filters": [
        {"propertyName": "firstname", "operator": "EQ", "value": "Alice"},
        {"propertyName": "lastname", "operator": "NEQ", "value": "Smith"}
      ]
    },
    {
      "filters": [
        {"propertyName": "email", "operator": "NOT_HAS_PROPERTY"}
      ]
    }
  ]
}
```

### Filter Operators

| Operator         | Description                                          |
|-----------------|------------------------------------------------------|
| `LT`            | Less than                                            |
| `LTE`           | Less than or equal to                                 |
| `GT`            | Greater than                                           |
| `GTE`           | Greater than or equal to                              |
| `EQ`            | Equal to                                             |
| `NEQ`           | Not equal to                                          |
| `BETWEEN`       | Within a range (uses `highValue` and `value`)        |
| `IN`            | Included in a list (values in `values` array)         |
| `NOT_IN`        | Not included in a list (values in `values` array)      |
| `HAS_PROPERTY`  | Has a value for the property                         |
| `NOT_HAS_PROPERTY` | Doesn't have a value for the property                   |
| `CONTAINS_TOKEN` | Contains a token (wildcards * supported)             |
| `NOT_CONTAINS_TOKEN` | Doesn't contain a token                             |


## Searching Through Associations

Use the pseudo-property `associations.{objectType}` to search for records associated with other records.

**Example:** Tickets associated with contact ID 123:

```json
{
  "filters": [
    {"propertyName": "associations.contact", "operator": "EQ", "value": "123"}
  ]
}
```

**(Note: Custom object associations are not currently supported.)**

## Sorting Search Results

Use the `sorts` array to specify sorting criteria. Only one sorting rule is allowed.

**Example:** Sort contacts by `createdate` descending:

```json
{
  "sorts": [
    {"propertyName": "createdate", "direction": "DESCENDING"}
  ]
}
```

## Paging Through Results

Default page size: 10 records.  Use the `limit` parameter (max 200) to change this.  Use the `after` parameter (integer value from `paging.next.after` in the previous response) to retrieve subsequent pages.


## Limitations

* Delay in indexing new/updated objects.
* Archived objects are not included.
* Rate limit: 5 requests per second.
* Maximum objects per page: 200.
* Maximum query length: 3,000 characters.
* Maximum total results: 10,000.
* Phone number search uses standardized properties (`hs_searchable_calculated_*`), only area code and local number are used.  Do not include country codes.

This enhanced documentation provides a clearer and more organized overview of the HubSpot CRM API search functionality.  Remember to replace `"Bearer YOUR_ACCESS_TOKEN"` with your actual access token in the curl examples.
