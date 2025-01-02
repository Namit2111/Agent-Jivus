# HubSpot CRM API Search Documentation

This document details the HubSpot CRM API's search functionality, allowing you to filter, sort, and search across various CRM objects and engagements.  A CRM scope is required to use these endpoints from an application.  Refer to the [list of available scopes](<insert link here>) for details.


## API Endpoints

CRM search endpoints follow this format:

`/crm/v3/objects/{object}/search`

where `{object}` is the type of CRM object you're searching (e.g., `contacts`, `companies`, `deals`).


## Making a Search Request

Use a `POST` request to the appropriate search endpoint. The request body contains the search criteria.


### Request Body Parameters

* **`filterGroups` (array):**  Groups filters using AND/OR logic.  Maximum 5 groups, 6 filters per group (18 total).
    * **`filters` (array, within each `filterGroup`):**  Individual filter conditions.
        * **`propertyName` (string):** The name of the CRM property to filter on.  See Searchable Properties sections below for details.  For associations, use `associations.{objectType}` (e.g., `associations.contact`).
        * **`operator` (string):** The comparison operator. See Operator Table below.
        * **`value` (string/number/array):** The value to compare against.  For `IN` and `NOT_IN` operators, provide an array of values. For `BETWEEN`, use `value` for the lower bound and `highValue` for the upper bound.  For `CONTAINS_TOKEN` and `NOT_CONTAINS_TOKEN`, wildcards (`*`) are supported.
* **`properties` (array, optional):** Specifies the properties to return in the response. If omitted, default properties are returned.
* **`query` (string, optional):**  A simple text search across default searchable properties for the object type.
* **`sorts` (array, optional):** Sorts results. Only one sort rule is allowed.
    * **`propertyName` (string):** Property to sort by.
    * **`direction` (string):**  `ASCENDING` or `DESCENDING`.
* **`limit` (integer, optional):**  Number of results per page (max 200, default 10).
* **`after` (integer, optional):**  Pagination token for retrieving subsequent pages.


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
  ]
}
```


### Example Request (Companies with Property Selection):

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

### Example Request (using 'BETWEEN' operator):

```json
{
"filterGroups":[{
"filters":[
{
"propertyName":"hs_lastmodifieddate",
"operator":"BETWEEN",
"highValue": "1642672800000",
"value":"1579514400000"
}
]
}]
}
```

### Example Request (using 'IN' operator):

```json
{
"filterGroups":[
{
"filters":[
{
"propertyName":"enumeration_property",
"operator":"IN",
"values": ["value_1", "value_2"]
}
]
}
],
"properties": ["annualrevenue", "enumeration_property", "name"]
}
```


### Example using `query` parameter:

```bash
curl https://api.hubapi.com/crm/v3/objects/contacts/search \
--request POST \
--header "Content-Type: application/json" \
--header "authorization: Bearer YOUR_ACCESS_TOKEN" \
--data '{
"query": "x"
}'
```

### Example using associations:

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


### Example using sorting:

```bash
curl https://api.hubapi.com/crm/v3/objects/contacts/search \
--request POST \
--header "Content-Type: application/json" \
--header "authorization: Bearer YOUR_ACCESS_TOKEN" \
--data '{
"sorts": [
{
"propertyName": "createdate",
"direction": "DESCENDING"
}
]
}'
```

### Example using pagination:

```bash
curl https://api.hubapi.com/crm/v3/objects/contacts/search \
--request POST \
--header "Content-Type: application/json" \
--header "authorization: Bearer YOUR_ACCESS_TOKEN" \
--data '{
"limit": 20
}'
```

To get the next page use the `after` value from the previous response's `paging.next.after` property.

```bash
curl https://api.hubapi.com/crm/v3/objects/contacts/search \
--request POST \
--header "Content-Type: application/json" \
--header "authorization: Bearer YOUR_ACCESS_TOKEN" \
--data '{
"after": "20"
}'
```


## Response

The response is a JSON object with the following structure:

* **`total` (integer):** Total number of matching records.
* **`results` (array):** Array of matching records. Each record contains:
    * **`id` (string):** The ID of the record.
    * **`properties` (object):**  Object containing the requested properties and their values.
    * **`createdAt` (string):** Creation timestamp.
    * **`updatedAt` (string):** Last modification timestamp.
    * **`archived` (boolean):**  Whether the record is archived.
* **`paging` (object, optional):** Pagination information (only present if there are more pages).
    * **`next` (object):** Information about the next page.
        * **`after` (string):**  The `after` value to use in the next request.


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

| Search Endpoint                     | Object      | Default Returned Properties                                                                 |
|--------------------------------------|--------------|---------------------------------------------------------------------------------------------|
| `/crm/v3/objects/carts/search`       | Carts        | `createdate`, `hs_lastmodifieddate`, `hs_object_id`                                      |
| `/crm/v3/objects/companies/search`   | Companies    | `name`, `domain`, `createdate`, `hs_lastmodifieddate`, `hs_object_id`                      |
| `/crm/v3/objects/contacts/search`    | Contacts     | `firstname`, `lastname`, `email`, `lastmodifieddate`, `hs_object_id`, `createdate`          |
| `/crm/v3/objects/deals/search`       | Deals        | `dealname`, `amount`, `closedate`, `pipeline`, `dealstage`, `createdate`, `hs_lastmodifieddate`, `hs_object_id` |
| `/crm/v3/objects/deal_split/search` | Deal splits  | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`                                   |
| `/crm/v3/objects/discounts/search`   | Discounts    | `createdate`, `hs_lastmodifieddate`, `hs_object_id`                                      |
| `/crm/v3/objects/feedback_submissions/search` | Feedback Submissions | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`                                   |
| `/crm/v3/objects/fees/search`        | Fees         | `createdate`, `hs_lastmodifieddate`, `hs_object_id`                                      |
| `/crm/v3/objects/invoices/search`    | Invoices     | `createdate`, `hs_lastmodifieddate`, `hs_object_id`                                      |
| `/crm/v3/objects/leads/search`       | Leads        | `createdate`, `hs_lastmodifieddate`, `hs_object_id`                                      |
| `/crm/v3/objects/line_items/search`  | Line items   | `quantity`, `amount`, `price`, `createdate`, `hs_lastmodifieddate`, `hs_object_id`         |
| `/crm/v3/objects/orders/search`      | Orders       | `createdate`, `hs_lastmodifieddate`, `hs_object_id`                                      |
| `/crm/v3/objects/commerce_payments/search` | Payments     | `createdate`, `hs_lastmodifieddate`, `hs_object_id`                                      |
| `/crm/v3/objects/products/search`    | Products     | `name`, `description`, `price`, `createdate`, `hs_lastmodifieddate`, `hs_object_id`         |
| `/crm/v3/objects/quotes/search`      | Quotes       | `hs_expiration_date`, `hs_public_url_key`, `hs_status`, `hs_title`, `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id` |
| `/crm/v3/objects/subscriptions/search` | Subscriptions | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`                                   |
| `/crm/v3/objects/taxes/search`       | Taxes        | `createdate`, `hs_lastmodifieddate`, `hs_object_id`                                      |
| `/crm/v3/objects/tickets/search`     | Tickets      | `content`, `hs_pipeline`, `hs_pipeline_stage`, `hs_ticket_category`, `hs_ticket_priority`, `subject`, `createdate`, `hs_lastmodifieddate`, `hs_object_id` |


### Engagements

| Search Endpoint                | Engagement | Default Returned Properties                                      |
|---------------------------------|-------------|-----------------------------------------------------------------|
| `/crm/v3/objects/calls/search`  | Calls       | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`           |
| `/crm/v3/objects/emails/search` | Emails      | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`           |
| `/crm/v3/objects/meetings/search`| Meetings    | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`           |
| `/crm/v3/objects/notes/search`  | Notes       | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`           |
| `/crm/v3/objects/tasks/search`  | Tasks       | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`           |


## Default Searchable Properties

A `query` parameter searches across these properties by default.

| Search Endpoint                     | Object      | Default Searchable Properties                                                              |
|--------------------------------------|--------------|-------------------------------------------------------------------------------------------|
| `/crm/v3/objects/calls/search`       | Calls        | `hs_call_title`, `hs_body_preview`                                                        |
| `/crm/v3/objects/companies/search`   | Companies    | `website`, `phone`, `name`, `domain`                                                    |
| `/crm/v3/objects/contacts/search`    | Contacts     | `firstname`, `lastname`, `email`, `phone`, `hs_additional_emails`, `fax`, `mobilephone`, `company`, `hs_marketable_until_renewal` |
| `/crm/v3/objects/{objectType}/search` | Custom Objects | Up to 20 selected properties.                                                          |
| `/crm/v3/objects/deals/search`       | Deals        | `dealname`, `pipeline`, `dealstage`, `description`, `dealtype`                             |
| `/crm/v3/objects/emails/search`     | Emails      | `hs_email_subject`                                                                     |
| `/crm/v3/objects/feedback_submissions/search` | Feedback Submissions | `hs_submission_name`, `hs_content`                                                   |
| `/crm/v3/objects/meetings/search`   | Meetings    | `hs_meeting_title`, `hs_meeting_body`                                                    |
| `/crm/v3/objects/notes/search`      | Notes       | `hs_note_body`                                                                         |
| `/crm/v3/objects/products/search`   | Products     | `name`, `description`, `price`, `hs_sku`                                                 |
| `/crm/v3/objects/quotes/search`     | Quotes       | `hs_sender_firstname`, `hs_sender_lastname`, `hs_proposal_slug`, `hs_title`, `hs_sender_company_name`, `hs_sender_email`, `hs_quote_number`, `hs_public_url_key` |
| `/crm/v3/objects/tasks/search`      | Tasks       | `hs_task_body`, `hs_task_subject`                                                        |
| `/crm/v3/objects/tickets/search`    | Tickets      | `subject`, `content`, `hs_pipeline_stage`, `hs_ticket_category`, `hs_ticket_id`           |


## Filter Operators

| Operator          | Description                                                              |
|----------------------|--------------------------------------------------------------------------|
| `LT`               | Less than the specified value.                                          |
| `LTE`              | Less than or equal to the specified value.                               |
| `GT`               | Greater than the specified value.                                         |
| `GTE`              | Greater than or equal to the specified value.                             |
| `EQ`               | Equal to the specified value.                                            |
| `NEQ`              | Not equal to the specified value.                                         |
| `BETWEEN`          | Within the specified range (use `value` and `highValue`).                 |
| `IN`               | Included within the specified list (use `values` array). Case-sensitive for enumeration properties, lowercase for string properties. |
| `NOT_IN`           | Not included within the specified list (use `values` array). Case-sensitive for enumeration properties, lowercase for string properties. |
| `HAS_PROPERTY`     | Has a value for the specified property.                                  |
| `NOT_HAS_PROPERTY` | Doesn't have a value for the specified property.                          |
| `CONTAINS_TOKEN`   | Contains a token (wildcards * supported).                               |
| `NOT_CONTAINS_TOKEN` | Doesn't contain a token.                                               |


## Limitations

* Newly created/updated objects may take time to appear in search results.
* Archived objects are not included.
* Rate limited to 5 requests per second.
* Maximum 200 objects per page.
* Query maximum 3000 characters.
* Maximum 10,000 total results per query.
* Maximum 5 `filterGroups` with up to 6 `filters` each (18 total filters).
* Phone number search uses standardized `hs_searchable_calculated_*` properties; omit country codes.


## Error Handling

The API will return standard HTTP status codes to indicate success or failure.  Pay particular attention to 400 errors, which may indicate exceeding request limits or invalid parameters.  Check the response body for detailed error messages.
