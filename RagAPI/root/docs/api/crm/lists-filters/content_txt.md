# HubSpot Lists API v3: List Filters Overview

This document provides a comprehensive overview of HubSpot's Lists API v3 filter capabilities, enabling you to define complex conditional logic for selecting records in your lists.  The API uses a hierarchical structure based on `OR` and `AND` filter branches to achieve this.

## List Filter Fundamentals

When creating a HubSpot list with `SNAPSHOT` or `DYNAMIC` processing type, filters define which records belong.  Filters use conditional logic structured with `AND` and `OR` operations, controlled by the `filterBranchType` parameter.  Each branch contains individual filters (`filterType` parameter) evaluating records for inclusion.  Branches can be nested for complex logic.

HubSpot uses a `PASS`/`FAIL` system.  A record is a list member only if it passes *all* filters.

### Filter Evaluation Steps

1. **Record Selection:** Relevant records are selected based on the filter.  For example, a `property` filter selects records with the specified property.
2. **Pruning (`pruningRefineBy`):** (Optional) Refines the dataset to a specific time range.
3. **Filtering:** Filtering rules are applied to the refined dataset.  Records `PASS` or `FAIL` based on these rules.
4. **Coalescing (`coalescingRefineBy`):** (Optional) Further refines based on the number of occurrences (e.g., "contact filled out a form at least 2 times").  Records `PASS` if they meet the occurrence criteria.
5. **Final Result:** If `coalescingRefineBy` is absent, the result from step 3 determines inclusion.


## Filter Branch Structure

Filter branches define conditional logic.  They consist of:

* **`filterBranchType`:**  `OR` or `AND`.
* **`filterBranches`:**  An array of nested filter branches.
* **`filters`:** An array of individual filters.

**Mandatory Structure:** All filter definitions must start with a root-level `OR` filter branch, containing one or more nested `AND` filter branches.

**Example JSON (OR with two nested AND branches):**

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

This example creates a list of contacts with "John" as the first name OR those who do *not* have "Smith" as the last name.


## Filter Branch Types

* **`OR`:** Accepts a record if *any* of its nested `AND` branches (it must have at least one) accept it.  Cannot have any direct filters.

* **`AND`:** Accepts a record only if *all* its nested branches and filters accept it. Can contain nested `UNIFIED_EVENTS` and/or `ASSOCIATION` branches.

* **`UNIFIED_EVENTS`:**  Filters based on event completion status.  Can only be nested within an `AND` branch.  Requires `eventTypeId` and `operator` ( `HAS_COMPLETED` or `HAS_NOT_COMPLETED`).

* **`ASSOCIATION`:** Filters based on associated records.  Can only be nested within an `AND` branch. Requires `objectTypeId`, `operator` (`IN_LIST`), `associationTypeId`, and `associationCategory`.


## Filter Types

The `filterType` parameter specifies the type of filter.  Some key types include:

* `PROPERTY`: Filters based on property values.
* `ADS_TIME`, `ADS_SEARCH`, `CTA`, `EMAIL_EVENT`, `EVENT`, `FORM_SUBMISSION`, `FORM_SUBMISSION_ON_PAGE`, `IN_LIST`, `PAGE_VIEW`, `PRIVACY`, `SURVEY_MONKEY`, `SURVEY_MONKEY_VALUE`, `WEBINAR`, `INTEGRATION_EVENT`:  Each filters based on specific interaction or data.

(See full table in the original text for a complete list and descriptions)


## Property Filter Operations

`PROPERTY`, `INTEGRATION_EVENT`, and `SURVEY_MONKEY_VALUE` filters use an `operation` object:

* **`operationType`:**  Data type of the property (e.g., `NUMBER`, `STRING`, `MULTISTRING`, `TIME_POINT`, `TIME_RANGED`).
* **`operator`:**  The comparison operator (e.g., `IS_EQUAL_TO`, `CONTAINS`, `IS_BETWEEN`).
* **`value` / `values`:** The value(s) to compare against.
* **`includeObjectsWithNoValueSet`:** (Boolean) Whether to include records with no value for the property.

(See table in the original text for a complete list of `operationType` and supported operators)


## Time-Based Filters (`TIME_POINT`, `TIME_RANGED`)

Examples of constructing time-based filters are shown in the original text, demonstrating how to filter by:

* Specific dates
* Last X days
* Next X days
* Updated/Not updated in last X days
* Relative to today
* Compared to another property's value or last updated time


## Refine By Operations

* **`pruningRefineBy`:** Refines the dataset to a timeframe using absolute or relative timestamps.  Examples include:
    * **Absolute Comparative:**  `BEFORE` or `AFTER` a specific timestamp.
    * **Absolute Ranged:** `BETWEEN` or `NOT_BETWEEN` two timestamps.
    * **Relative Comparative:** `BEFORE` or `AFTER` a time offset (days/weeks).
    * **Relative Ranged:** `BETWEEN` or `NOT_BETWEEN` two time offsets.

* **`coalescingRefineBy`:**  Filters based on the number of times a record passes the filter criteria using `NUM_OCCURRENCES` (with optional `minOccurrences` and `maxOccurrences`).


## Legacy v1 Lists API

The v1 API (deprecated) is similar but has minor syntax and options differences.  It will be sunsetted.  The original text offers a brief comparison and guidance for migrating to v3.


## API Call Example (POST)

The examples in the original text demonstrate how to construct API calls using JSON to create lists based on various filtering criteria.  Remember that the endpoint would be the specific HubSpot API endpoint for creating or updating lists.  You will need appropriate authentication tokens.

This comprehensive markdown documentation summarizes the key aspects of the HubSpot Lists API v3 filter system. Refer to the original text for detailed examples and tables.
