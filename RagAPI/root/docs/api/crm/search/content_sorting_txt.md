# HubSpot CRM API Search Documentation

This document details the HubSpot CRM API's search functionality, allowing you to filter, sort, and search objects, records, and engagements across your CRM.  A CRM scope is required to use these endpoints from an app.  Refer to the [list of available scopes](<Insert Link to Scopes Here>) for details.


## API Endpoints

CRM search endpoints follow this format:

`/crm/v3/objects/{object}/search`

Where `{object}` is the specific CRM object type (e.g., `contacts`, `companies`, `deals`).


## Making a Search Request

To perform a search, send a `POST` request to the appropriate endpoint with the search criteria in the request body.

### Request Body

The request body can include the following parameters:

* **`filterGroups` (array):**  Allows for complex filtering using `AND` and `OR` logic.  Each `filterGroup` can contain multiple `filters`.
    * **`filters` (array):** Defines individual filter criteria. Each filter requires:
        * **`propertyName` (string):** The name of the CRM property to filter on.
        * **`operator` (string):** The comparison operator.  See the [Operator Table](#operator-table) below.
        * **`value` (string or number):** The value to compare against.  For `IN` and `NOT_IN` operators, use a `values` array instead.
        * **`highValue` (number, optional):** Used with the `BETWEEN` operator to specify the upper bound of the range.


* **`properties` (array, optional):** Specifies which properties to return in the response. If omitted, default properties are returned (see object-specific tables below).

* **`query` (string, optional):**  Searches all default text properties for records containing the specified string.

* **`sorts` (array, optional):** Specifies sorting criteria.  Only one sort rule is allowed. Each sort requires:
    * **`propertyName` (string):** The property to sort by.
    * **`direction` (string):**  `ASCENDING` or `DESCENDING`.

* **`limit` (number, optional):** Specifies the number of results per page (max 200, default 10).

* **`after` (number, optional):**  Used for pagination.  Specify the `paging.next.after` value from the previous response to retrieve the next page.


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

### Example Request (Query Search for Contacts with 'x'):

```bash
curl https://api.hubapi.com/crm/v3/objects/contacts/search \
--request POST \
--header "Content-Type: application/json" \
--header "authorization: Bearer YOUR_ACCESS_TOKEN" \
--data '{ "query": "x" }'
```


## Response

The API returns a JSON object with the following structure:

* **`total` (number):** The total number of records matching the search criteria.
* **`results` (array):** An array of matching records. Each record contains:
    * **`id` (string):** The ID of the record.
    * **`properties` (object):**  An object containing the requested properties and their values.
    * **`createdAt` (string):**  Creation timestamp.
    * **`updatedAt` (string):** Last update timestamp.
    * **`archived` (boolean):** Indicates if the record is archived.
* **`paging` (object, optional):** Contains pagination information, including `next.after` for retrieving subsequent pages.


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


## Searchable CRM Objects

The following tables list searchable objects, their default returned properties, and default searchable properties for query searches.

### Objects

| Search Endpoint                     | Object       | Default Returned Properties                                                                  |
|--------------------------------------|---------------|----------------------------------------------------------------------------------------------|
| `/crm/v3/objects/carts/search`       | Carts         | `createdate`, `hs_lastmodifieddate`, `hs_object_id`                                         |
| `/crm/v3/objects/companies/search`   | Companies     | `name`, `domain`, `createdate`, `hs_lastmodifieddate`, `hs_object_id`                         |
| `/crm/v3/objects/contacts/search`    | Contacts      | `firstname`, `lastname`, `email`, `lastmodifieddate`, `hs_object_id`, `createdate`            |
| `/crm/v3/objects/deals/search`       | Deals         | `dealname`, `amount`, `closedate`, `pipeline`, `dealstage`, `createdate`, `hs_lastmodifieddate`, `hs_object_id` |
| `/crm/v3/objects/deal_split/search` | Deal splits   | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`                                     |
| `/crm/v3/objects/discounts/search`   | Discounts     | `createdate`, `hs_lastmodifieddate`, `hs_object_id`                                         |
| `/crm/v3/objects/feedback_submissions/search` | Feedback Submissions | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`                                     |
| `/crm/v3/objects/fees/search`        | Fees          | `createdate`, `hs_lastmodifieddate`, `hs_object_id`                                         |
| `/crm/v3/objects/invoices/search`    | Invoices      | `createdate`, `hs_lastmodifieddate`, `hs_object_id`                                         |
| `/crm/v3/objects/leads/search`       | Leads         | `createdate`, `hs_lastmodifieddate`, `hs_object_id`                                         |
| `/crm/v3/objects/line_items/search`  | Line items    | `quantity`, `amount`, `price`, `createdate`, `hs_lastmodifieddate`, `hs_object_id`           |
| `/crm/v3/objects/orders/search`      | Orders        | `createdate`, `hs_lastmodifieddate`, `hs_object_id`                                         |
| `/crm/v3/objects/commerce_payments/search` | Payments      | `createdate`, `hs_lastmodifieddate`, `hs_object_id`                                         |
| `/crm/v3/objects/products/search`    | Products      | `name`, `description`, `price`, `createdate`, `hs_lastmodifieddate`, `hs_object_id`          |
| `/crm/v3/objects/quotes/search`      | Quotes        | `hs_expiration_date`, `hs_public_url_key`, `hs_status`, `hs_title`, `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id` |
| `/crm/v3/objects/subscriptions/search` | Subscriptions (Commerce) | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`                                     |
| `/crm/v3/objects/taxes/search`       | Taxes         | `createdate`, `hs_lastmodifieddate`, `hs_object_id`                                         |
| `/crm/v3/objects/tickets/search`     | Tickets       | `content`, `hs_pipeline`, `hs_pipeline_stage`, `hs_ticket_category`, `hs_ticket_priority`, `subject`, `createdate`, `hs_lastmodifieddate`, `hs_object_id` |


### Engagements

| Search Endpoint                | Engagement  | Default Returned Properties                                         |
|---------------------------------|--------------|---------------------------------------------------------------------|
| `/crm/v3/objects/calls/search`  | Calls        | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`             |
| `/crm/v3/objects/emails/search` | Emails       | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`             |
| `/crm/v3/objects/meetings/search`| Meetings     | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`             |
| `/crm/v3/objects/notes/search`  | Notes        | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`             |
| `/crm/v3/objects/tasks/search`  | Tasks        | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`             |


### Default Searchable Properties (for `query` parameter)

| Search Endpoint                     | Object       | Default Searchable Properties                                                                                                |
|--------------------------------------|---------------|----------------------------------------------------------------------------------------------------------------------------|
| `/crm/v3/objects/calls/search`       | Calls         | `hs_call_title`, `hs_body_preview`                                                                                       |
| `/crm/v3/objects/companies/search`   | Companies     | `website`, `phone`, `name`, `domain`                                                                                      |
| `/crm/v3/objects/contacts/search`    | Contacts      | `firstname`, `lastname`, `email`, `phone`, `hs_additional_emails`, `fax`, `mobilephone`, `company`, `hs_marketable_until_renewal` |
| `/crm/v3/objects/{objectType}/search` | Custom objects | Up to 20 selected properties.                                                                                             |
| `/crm/v3/objects/deals/search`       | Deals         | `dealname`, `pipeline`, `dealstage`, `description`, `dealtype`                                                              |
| `/crm/v3/objects/emails/search`     | Emails       | `hs_email_subject`                                                                                                       |
| `/crm/v3/objects/feedback_submissions/search` | Feedback Submissions | `hs_submission_name`, `hs_content`                                                                                       |
| `/crm/v3/objects/meetings/search`   | Meetings     | `hs_meeting_title`, `hs_meeting_body`                                                                                    |
| `/crm/v3/objects/notes/search`      | Notes        | `hs_note_body`                                                                                                         |
| `/crm/v3/objects/products/search`   | Products      | `name`, `description`, `price`, `hs_sku`                                                                                  |
| `/crm/v3/objects/quotes/search`     | Quotes        | `hs_sender_firstname`, `hs_sender_lastname`, `hs_proposal_slug`, `hs_title`, `hs_sender_company_name`, `hs_sender_email`, `hs_quote_number`, `hs_public_url_key` |
| `/crm/v3/objects/tasks/search`      | Tasks        | `hs_task_body`, `hs_task_subject`                                                                                       |
| `/crm/v3/objects/tickets/search`    | Tickets       | `subject`, `content`, `hs_pipeline_stage`, `hs_ticket_category`, `hs_ticket_id`                                             |


## Filtering Search Results

Use `filterGroups` and `filters` to refine results.  `AND` logic is applied within a `filterGroup`, while `OR` logic is applied between `filterGroups`.  Maximum limits apply (5 `filterGroups`, 6 `filters` per group, 18 total filters).


## Search Through Associations

Search for records associated with other records using the `associations.{objectType}` pseudo-property (e.g., `associations.contact`).  Note that custom object associations are not currently supported.


## Sorting Search Results

Use the `sorts` parameter to sort results in ascending or descending order. Only one sort rule is allowed per request.


## Paging Through Results

Results are paginated; use the `limit` parameter to control the page size (max 200) and the `after` parameter to retrieve subsequent pages.


## Operators Table

| Operator          | Description                                      |
|----------------------|--------------------------------------------------|
| `LT`              | Less than                                        |
| `LTE`             | Less than or equal to                             |
| `GT`              | Greater than                                       |
| `GTE`             | Greater than or equal to                           |
| `EQ`              | Equal to                                          |
| `NEQ`             | Not equal to                                       |
| `BETWEEN`         | Within a specified range (uses `value` and `highValue`) |
| `IN`              | Included in a list (uses `values` array)           |
| `NOT_IN`          | Not included in a list (uses `values` array)        |
| `HAS_PROPERTY`    | Has a value for the property                     |
| `NOT_HAS_PROPERTY` | Does not have a value for the property             |
| `CONTAINS_TOKEN`  | Contains a token (supports wildcards)              |
| `NOT_CONTAINS_TOKEN` | Does not contain a token                         |


## Limitations

* Newly created/updated objects may have a delay before appearing in search results.
* Archived objects will not appear in search results.
* Rate limit: 5 requests per second.
* Maximum objects per page: 200.
* Maximum query length: 3,000 characters.
* Maximum total results: 10,000.
* Phone number search uses standardized `hs_searchable_calculated_*` properties (area code and local number only; omit country code).


This documentation provides a comprehensive overview of the HubSpot CRM API search functionality.  Remember to replace `YOUR_ACCESS_TOKEN` with your actual HubSpot access token.
