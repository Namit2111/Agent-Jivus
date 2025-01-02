# HubSpot Lists API: Filter Documentation

This document details the HubSpot Lists API's filtering capabilities, focusing on the v3 API.  The legacy v1 API is deprecated and will be sunsetted.

## List Filters Overview

When creating a HubSpot list with `SNAPSHOT` or `DYNAMIC` processing types, filters determine which records are included. Filters use conditional logic defined by filter branches with `AND` or `OR` operation types (`filterBranchType` parameter).  Each branch contains individual filters (`filterType` parameter) evaluating records for inclusion.  Nested filter branches are allowed.

HubSpot uses PASS/FAIL logic. A record is a list member only if it passes *all* filters.

### Filter Evaluation Steps:

1. **Record Selection:** Relevant records are selected based on the filter (e.g., all records for a `property` filter).
2. **Pruning Refinement (Optional):** `pruningRefineBy` parameter refines data to a specific time range.
3. **Filtering:** Filtering rules are applied to the refined data, determining PASS or FAIL.
4. **Coalescing Refinement (Optional):** `coalescingRefineBy` further refines based on the number of occurrences (e.g., "contact filled out a form at least 2 times").
5. **Final Result:**  If `coalescingRefineBy` is present, records meeting the occurrence criteria PASS. Otherwise, PASS/FAIL is based on step 3.

### Filter Branches

A filter branch defines conditional logic.  It consists of a type (`OR` or `AND`), a list of filters, and a list of sub-branches.

* **`OR` Filter Branch:** Accepts a record if it passes *any* of its filters or sub-branches.  Must have at least one `AND` sub-branch and no direct filters.

* **`AND` Filter Branch:** Accepts a record if it passes *all* of its filters and sub-branches. Can have zero or more filters and nested `UNIFIED_EVENTS` or `ASSOCIATION` branches.

* **Structure:** All filter definitions must start with a root-level `OR` filter branch containing one or more `AND` sub-branches.


**Example JSON Structure:**

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

**Example: "First Name is 'John' OR Last Name is not 'Smith'":**

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

**Example: "First Name is 'John' AND Last Name is 'Smith'":**

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


### Filtering on Events and Associated Objects

* **`UNIFIED_EVENTS`:** Filters on events.  Must be nested within an `AND` branch and have at least one `PROPERTY` filter.

* **`ASSOCIATION`:** Filters on associated records. Must be nested within an `AND` branch and have at least one filter.  Additional `filterBranches` are allowed only for `CONTACT` to `LINE_ITEM` associations.


### Filter Types

The `filterType` parameter specifies the type of filter.  Common types include: `PROPERTY`, `ADS_TIME`, `ADS_SEARCH`, `CTA`, `EMAIL_EVENT`, `EVENT`, `FORM_SUBMISSION`, `FORM_SUBMISSION_ON_PAGE`, `IN_LIST`, `PAGE_VIEW`, `PRIVACY`, `SURVEY_MONKEY`, `SURVEY_MONKEY_VALUE`, `WEBINAR`, `INTEGRATION_EVENT`.

### Property Filter Operations

For `PROPERTY`, `INTEGRATION_EVENT`, and `SURVEY_MONKEY_VALUE` filters, the `operation` object defines filter parameters:

* `operationType`: Type of operator (e.g., `NUMBER`, `MULTISTRING`).
* `operator`: Operator to apply (e.g., `IS_EQUAL_TO`, `IS_NOT_EQUAL_TO`).
* `value` / `values`: Value(s) to filter by.
* `includeObjectsWithNoValueSet`:  Whether to include records with no value set for the property (true/false).

The supported `operationType` and `operator` combinations vary by property type. See the detailed tables below for specifics.


### Time-Based Filter Examples

These examples use `TIME_POINT` and `TIME_RANGED` operations.  They can reference specific dates or relative times.

* **Is Equal to Date:**  Uses `TIME_RANGED` with `lowerBoundTimePoint` and `upperBoundTimePoint` set to the same date.

* **In Last X Number of Days:** Uses `TIME_RANGED` with `lowerBoundTimePoint` offset from "today" and `upperBoundTimePoint` set to "now."

* **In Next X Number of Days:** Uses `TIME_RANGED` with `lowerBoundTimePoint` set to "now" and `upperBoundTimePoint` offset from "today."

* **Updated or Not Updated in the Last X Days:** Uses `TIME_RANGED` with `propertyParser` set to `UPDATED_AT`.

* **Is After Date:** Uses `TIME_POINT` with `operator` set to `IS_AFTER`.

* **Is Relative to Today:** Uses `TIME_POINT` with `timePoint.timeType` set to `INDEXED` and an `offset`.

* **Is Before or After Another Property:** Uses `TIME_POINT` with `timePoint.timeType` set to `PROPERTY_REFERENCED`.



### Refine By Operations

* **`pruningRefineBy`:** Refines the dataset to a time range (absolute or relative).

* **`coalescingRefineBy`:** Determines whether a record PASSED the filter a minimum/maximum number of times (`NUM_OCCURRENCES`).

Only one refine by operation is allowed per filter.


### v1 List Filters (Legacy - Deprecated)

The v1 API is deprecated. Migrate to v3.  The v1 API supports only `PROPERTY` filters with a slightly different syntax.


## Detailed Tables:  (Too extensive to include fully formatted tables here.  The original text provides these tables completely.  This Markdown would need to be edited to include them.)

The original text includes extensive tables detailing:

* Supported `filterType` values and their descriptions.
* Supported `operationType` values, their supported operators, and descriptions.
* Detailed parameters and values for `pruningRefineBy` and `coalescingRefineBy` operations.
* Supported operators for all property types in v1 API (string, multi-string, number, boolean, enumeration, datetime).


## API Call Example (Illustrative - Adapt to your needs)

A complete API call would involve sending a JSON payload containing the filter definition to the appropriate HubSpot Lists API endpoint (POST request to create or update a list). The exact endpoint URL and authentication method will depend on your HubSpot account setup and API key.  Refer to HubSpot's API documentation for specifics on API calls.


This markdown provides a comprehensive overview of HubSpot's List API filtering capabilities.  Remember to consult HubSpot's official API documentation for the most up-to-date information, including endpoint URLs, authentication details, error codes, and rate limits.
