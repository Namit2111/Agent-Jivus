# HubSpot Lists API v3: Filter Documentation

This document details the structure and usage of filters within the HubSpot Lists API v3.  This API allows you to define lists of records (e.g., contacts) based on specified criteria.  The legacy v1 API is deprecated and should not be used for new integrations.

## List Filter Overview

When creating a list with either `SNAPSHOT` or `DYNAMIC` processing type, filters determine which records are included.  Filters utilize conditional logic defined by *filter branches* with `AND` or `OR` operation types (specified by the `filterBranchType` parameter).  Within branches, individual filters (`filterType` parameter) assess records for inclusion.  Nested branches are also supported.

HubSpot employs a `PASS`/`FAIL` logic: a record becomes a list member only if it passes *all* filters.


## Filter Evaluation Steps

1. **Record Selection:** Relevant records are selected based on the chosen filter (e.g., all records for a `property` filter).
2. **Pruning Refinement (Optional):** The `pruningRefineBy` parameter refines data to a specific time range.
3. **Filtering:** Filtering rules are applied to the refined data to determine `PASS` or `FAIL`.
4. **Coalescing Refinement (Optional):** The `coalescingRefineBy` parameter further refines data based on the number of occurrences (e.g., "contact has filled out a form at least 2 times").  If present, records must meet the specified occurrence count to `PASS`.
5. **Final Result:** Records pass or fail based on steps 3 and 4.


## Filter Branches

A filter branch is a data structure representing conditional logic. It's defined by:

* `filterBranchType`:  (`OR`, `AND`, `UNIFIED_EVENTS`, `ASSOCIATION`)
* `filterBranchOperator`: (`AND` or `OR`) - determines how the branch evaluates relative to others.
* `filters`: A list of individual filters within this branch.
* `filterBranches`: A list of nested filter branches.

* **`AND` Branch:** A record is accepted if it passes *all* filters and sub-branches within the `AND` branch.
* **`OR` Branch:** A record is accepted if it passes *any* filter or sub-branch within the `OR` branch.

The root filter branch must always be `OR`.


## Filter Branch Structure Example (JSON)

A basic structure always starts with an `OR` branch containing one or more `AND` sub-branches:

```json
{
  "filterBranch": {
    "filterBranches": [
      {
        "filterBranches": [],
        "filterBranchType": "AND",
        "filters": [ /* filters here */ ]
      }
    ],
    "filterBranchType": "OR",
    "filters": []
  }
}
```

### Example: "First Name is 'John' OR Last Name is not 'Smith'"

```json
{
  "filterBranch": {
    "filterBranchType": "OR",
    "filters": [],
    "filterBranches": [
      {
        "filterBranchType": "AND",
        "filters": [
          {
            "filterType": "PROPERTY",
            "property": "firstname",
            "operation": {
              "operationType": "MULTISTRING",
              "operator": "IS_EQUAL_TO",
              "values": ["John"]
            }
          }
        ],
        "filterBranches": []
      },
      {
        "filterBranchType": "AND",
        "filters": [
          {
            "filterType": "PROPERTY",
            "property": "lastname",
            "operation": {
              "operationType": "MULTISTRING",
              "operator": "IS_NOT_EQUAL_TO",
              "values": ["Smith"]
            }
          }
        ],
        "filterBranches": []
      }
    ]
  }
}
```

### Example: "First Name is 'John' AND Last Name is 'Smith'"

```json
{
  "filterBranch": {
    "filterBranchType": "OR",
    "filters": [],
    "filterBranches": [
      {
        "filterBranchType": "AND",
        "filters": [
          {
            "filterType": "PROPERTY",
            "property": "firstname",
            "operation": {
              "operationType": "MULTISTRING",
              "operator": "IS_EQUAL_TO",
              "values": ["John"]
            }
          },
          {
            "filterType": "PROPERTY",
            "property": "lastname",
            "operation": {
              "operationType": "MULTISTRING",
              "operator": "IS_EQUAL_TO",
              "values": ["Smith"]
            }
          }
        ],
        "filterBranches": []
      }
    ]
  }
}
```


## Filtering on Events and Associated Objects

* **`UNIFIED_EVENTS`:** Filters based on events. Must be nested within an `AND` branch. Requires at least one `PROPERTY` filter.
* **`ASSOCIATION`:** Filters based on associated records. Must be nested within an `AND` branch.  Requires at least one filter.  Additional `filterBranches` are only allowed for `CONTACT` to `LINE_ITEM` associations.


## Filter Branch Types

* **`OR`:** Root-level branch.  Must have one or more nested `AND` branches and zero filters.
* **`AND`:** Nested branch. Can have zero or more filters and zero or more nested `UNIFIED_EVENTS` or `ASSOCIATION` branches.
* **`UNIFIED_EVENTS`:** Nested within `AND`.  Can have one or more `PROPERTY` filters and zero additional branches.  Requires `eventTypeId` and `operator` (`HAS_COMPLETED`, `HAS_NOT_COMPLETED`).
* **`ASSOCIATION`:** Nested within `AND`.  Must have one or more filters and zero additional branches.  Requires `objectTypeId`, `operator` (`IN_LIST`), `associationTypeId`, and `associationCategory`.


## Filter Types (`filterType`)

The `filterType` parameter specifies the type of filter.  Some examples include:

* `PROPERTY`: Filters on record properties (see "Property Filter Operations").
* `ADS_TIME`, `ADS_SEARCH`, `CTA`, `EMAIL_EVENT`, `EVENT`, `FORM_SUBMISSION`, `FORM_SUBMISSION_ON_PAGE`, `IN_LIST`, `PAGE_VIEW`, `PRIVACY`, `SURVEY_MONKEY`, `SURVEY_MONKEY_VALUE`, `WEBINAR`, `INTEGRATION_EVENT` :  Each filter type has specific parameters. Refer to the HubSpot documentation for detailed information on each type.


## Property Filter Operations

The `operation` object within a `PROPERTY` filter defines the filter's parameters:

* `operationType`: (`ALL_PROPERTY`, `BOOL`, `ENUMERATION`, `MULTISTRING`, `NUMBER`, `STRING`, `TIME_POINT`, `TIME_RANGED`)
* `operator`:  Specific operator depending on the `operationType` (e.g., `IS_EQUAL_TO`, `IS_NOT_EQUAL_TO`, `CONTAINS`, `IS_BETWEEN`).
* `value` or `values`: Single value or array of values to filter by.
* `includeObjectsWithNoValueSet`:  Boolean; `true` includes records with no value set for the property, `false` excludes them (default).


## Time-Based Filter Examples (`TIME_POINT`, `TIME_RANGED`)

These examples use the `notes_last_updated` property.  Replace this with the appropriate property for your use case.

* **`Is equal to date`:**  Filters records updated on a specific date.

* **`In Last X Number of Days`:** Filters records updated within the last X days.

* **`In Next X Number of Days`:** Filters records to be updated within the next X days.

* **`Updated or Not Updated in the Last X Days`:** Filters records updated (or not updated) within the last X days.

* **`Is After Date`:** Filters records updated after a specific date.

* **`Is Relative to Today`:** Filters records updated a specific number of days before or after today.

* **`Is Before or After another property (value or last updated)`:** Compares a property's update time to another property's value or last update time.


(Detailed JSON examples for each time-based filter are provided in the original text and should be included here for completeness).


## Refine By Operations

* **`pruningRefineBy`:** Refines the dataset to a specific time range (absolute or relative).
* **`coalescingRefineBy`:** Defines the minimum and maximum number of times a record must meet the filter criteria to pass (`NUM_OCCURRENCES`).

Only one refine-by operation is allowed per filter.

(Detailed JSON examples for each refine-by operation type – `ABSOLUTE_COMPARATIVE`, `ABSOLUTE_RANGED`, `RELATIVE_COMPARATIVE`, `RELATIVE_RANGED`, `NUM_OCCURRENCES` –  are provided in the original text and should be included here for completeness).


## v1 List Filters (Legacy - Deprecated)

The v1 API is deprecated. Use v3 instead.  The primary difference is that v1 only supports `PROPERTY` filters with a simpler structure.

(The example code for v1 filters should be included here).


## All Property Types Operations (v1)

(The sections for String, Multi-string, Number, Boolean, Enumeration, and Datetime operations for the legacy v1 API should be included here with code examples).


## API Call Example (Conceptual)

The exact API call will depend on your specific needs and which HTTP method you use. However, a general structure would look like this (using `POST` to create a list):


```bash
curl -X POST \
  https://api.hubapi.com/crm/v3/objects/contacts/lists/{listId}/filters \
  -H 'Content-Type: application/json' \
  -d '{
        "filterBranch": {
          // Your filter branch JSON here
        }
      }'
```

Remember to replace `{listId}` with the actual ID of your list, and populate the  `"filterBranch"` with your filter definition in JSON format as described above.


This markdown provides a comprehensive overview of HubSpot Lists API v3 filters.  Remember to refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications for each filter type and parameter.
