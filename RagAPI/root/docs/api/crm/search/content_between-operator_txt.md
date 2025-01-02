# HubSpot CRM API Search Documentation

This document details the HubSpot CRM API search endpoints, allowing you to filter, sort, and search objects, records, and engagements across your CRM.  A CRM scope is required to use these endpoints from an app. Refer to the [HubSpot API Scopes documentation](<Insert Link to HubSpot API Scopes Here>) for details.


## 1. Making a Search Request

To search your CRM, make a `POST` request to the object's search endpoint, formatted as follows:

`/crm/v3/objects/{object}/search`

where `{object}` represents the CRM object type (e.g., `contacts`, `companies`, `deals`).

The request body includes filters to refine your search.


### Example 1: Searching Contacts by Email

This example retrieves contacts with emails containing "*@hubspot.com":

**Request:**

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

**Response (Example):**

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
    {
      "id": "57156923994",
      "properties": {
        "createdate": "2024-09-11T18:21:50.012Z",
        "email": "emailmaria@hubspot.com",
        "firstname": "Maria",
        "hs_object_id": "57156923994",
        "lastmodifieddate": "2024-10-21T21:36:02.961Z",
        "lastname": "Johnson (Sample Contact)"
      },
      "createdAt": "2024-09-11T18:21:50.012Z",
      "updatedAt": "2024-10-21T21:36:02.961Z",
      "archived": false
    }
  ]
}
```


### Example 2: Specifying Returned Properties

This example searches companies with `annualrevenue` > 10,000,000 and returns only `annualrevenue` and `name`:

**Request:**

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

**Response (Example - partial):**

```json
{
  "total": 38,
  "results": [
    {
      "id": "2810868468",
      "properties": {
        "annualrevenue": "1000000000",
        "name": "Google"
      },
      // ... other fields
    },
    // ... more results
  ]
}
```


## 2. Searchable CRM Objects and Engagements

The following tables list searchable objects, their default returned properties, and default searchable properties.


### 2.1 Objects

| Search Endpoint                 | Object       | Default Returned Properties                                                                   |
|---------------------------------|---------------|-----------------------------------------------------------------------------------------------|
| `/crm/v3/objects/carts/search`  | Carts         | `createdate`, `hs_lastmodifieddate`, `hs_object_id`                                         |
| `/crm/v3/objects/companies/search` | Companies     | `name`, `domain`, `createdate`, `hs_lastmodifieddate`, `hs_object_id`                         |
| `/crm/v3/objects/contacts/search` | Contacts      | `firstname`, `lastname`, `email`, `lastmodifieddate`, `hs_object_id`, `createdate`            |
| `/crm/v3/objects/deals/search`   | Deals         | `dealname`, `amount`, `closedate`, `pipeline`, `dealstage`, `createdate`, `hs_lastmodifieddate`, `hs_object_id` |
| `/crm/v3/objects/deal_split/search` | Deal splits  | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`                                     |
| ... (other objects) ...         | ...           | ...                                                                                       |


### 2.2 Engagements

| Search Endpoint                 | Engagement   | Default Returned Properties                                                              |
|---------------------------------|---------------|------------------------------------------------------------------------------------------|
| `/crm/v3/objects/calls/search`  | Calls         | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`                                 |
| `/crm/v3/objects/emails/search` | Emails        | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`                                 |
| `/crm/v3/objects/meetings/search`| Meetings      | `hs_createdate`, `hs_lastmodifieddate`, `hs_object_id`                                 |
| ... (other engagements) ...     | ...           | ...                                                                                     |


### 2.3 Default Searchable Properties

These properties are searched by default when using the `query` parameter.

| Search Endpoint                 | Object       | Default Searchable Properties                                                              |
|---------------------------------|---------------|-------------------------------------------------------------------------------------------|
| `/crm/v3/objects/calls/search`  | Calls         | `hs_call_title`, `hs_body_preview`                                                      |
| `/crm/v3/objects/companies/search` | Companies     | `website`, `phone`, `name`, `domain`                                                    |
| `/crm/v3/objects/contacts/search` | Contacts      | `firstname`, `lastname`, `email`, `phone`, `hs_additional_emails`, `fax`, `mobilephone`, `company`, `hs_marketable_until_renewal` |
| ... (other objects) ...         | ...           | ...                                                                                     |


## 3.  Filtering Search Results

Use `filterGroups` in the request body to filter results.  `filterGroups` can contain multiple `filters`, applying `AND` logic within a group and `OR` logic between groups.  A maximum of 5 `filterGroups` with up to 6 `filters` each (18 total) is allowed.


### Filter Operators

| Operator          | Description                                      |
|----------------------|--------------------------------------------------|
| `LT`               | Less than                                       |
| `LTE`              | Less than or equal to                             |
| `GT`               | Greater than                                      |
| `GTE`              | Greater than or equal to                          |
| `EQ`               | Equal to                                        |
| `NEQ`              | Not equal to                                     |
| `BETWEEN`          | Within a range (uses `highValue` and `value`)      |
| `IN`               | Included in a list (uses `values` array)          |
| `NOT_IN`           | Not included in a list (uses `values` array)      |
| `HAS_PROPERTY`     | Has a value for the property                     |
| `NOT_HAS_PROPERTY` | Doesn't have a value for the property            |
| `CONTAINS_TOKEN`   | Contains a token (wildcards * allowed)           |
| `NOT_CONTAINS_TOKEN`| Does not contain a token                         |


## 4. Searching Through Associations

Search for records associated with other records using the pseudo-property `associations.{objectType}` (e.g., `associations.contact`).  Custom object associations are not currently supported.


## 5. Sorting Search Results

Use the `sorts` array to sort results. Only one sorting rule is allowed per search.


## 6. Paging Through Results

The default page size is 10.  Use the `limit` parameter (max 200) to change this.  Use the `after` parameter (from `paging.next.after` in the previous response) to access subsequent pages.


## 7. Limitations

* Newly created/updated objects may take time to appear in search results.
* Archived objects are not included.
* Rate limit: 5 requests per second.
* Maximum objects per page: 200.
* Maximum query length: 3,000 characters.
* Maximum total results: 10,000.
* Maximum filters: 18 (5 filterGroups, 6 filters per group).
* Phone number search uses standardized `hs_searchable_calculated_*` properties; omit country codes.


## 8.  cURL Examples (Summarized)

The provided text contains many cURL examples.  These are all similar in structure and demonstrate the use of different parameters and filters.  Refer to the sections above for details on each parameter's usage.  A typical cURL request would look like this (remember to replace placeholders):

```bash
curl https://api.hubapi.com/crm/v3/objects/{object}/search \
  --request POST \
  --header "Content-Type: application/json" \
  --header "authorization: Bearer YOUR_ACCESS_TOKEN" \
  --data '{your_json_data}'
```


This comprehensive documentation provides a detailed overview of the HubSpot CRM API search functionality.  Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
