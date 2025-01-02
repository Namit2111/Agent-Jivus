# HubSpot Lists API v3: List Filters Overview

This document details the structure and usage of filters within the HubSpot Lists API v3.  It's crucial for defining which records belong to a list, whether it's a `SNAPSHOT` or `DYNAMIC` list.

## List Filter Structure

List filters employ conditional logic through *filter branches* using `AND` or `OR` operations (specified by `filterBranchType`). Each branch contains individual filters (`filterType`) evaluating records for inclusion.  Branches can be nested.

The fundamental structure requires a root-level `OR` filter branch containing one or more nested `AND` sub-branches.

**Example JSON:**

```json
{
  "filterBranch": {
    "filterBranches": [
      {
        "filterBranches": [],
        "filterBranchType": "AND",
        "filters": [ /* Filters for this AND branch */ ]
      }
    ],
    "filterBranchType": "OR",
    "filters": []
  }
}
```

This structure ensures proper rendering in the HubSpot UI.

## Filter Evaluation Steps

1. **Record Selection:** Relevant records are selected based on the filter.
2. **Pruning Refinement (Optional):**  The `pruningRefineBy` parameter refines the data to a specific time range.
3. **Filtering:** Filtering rules are applied to the refined data, resulting in `PASS` or `FAIL`.
4. **Coalescing Refinement (Optional):** The `coalescingRefineBy` parameter further refines based on the number of occurrences (e.g., "contact has filled out a form at least 2 times").
5. **Final Result:** Records passing all filters become list members.

## Filter Branch Types

* **`OR` Filter Branch:**
    * Must have one or more nested `AND` branches.
    * Cannot have filters directly within it.
    * Accepts a record if *any* nested branch accepts it.

    ```json
    {
      "filterBranchType": "OR",
      "filterBranches": [ /* One or more nested AND branches */ ],
      "filters": []
    }
    ```

* **`AND` Filter Branch:**
    * Can have zero or more filters.
    * Can have zero or more nested `UNIFIED_EVENTS` and/or `ASSOCIATION` branches.
    * Accepts a record only if it passes *all* filters and nested branches.

    ```json
    {
      "filterBranchType": "AND",
      "filterBranches": [ /* Nested UNIFIED_EVENTS or ASSOCIATION branches */ ],
      "filters": [ /* Filters for this AND branch */ ]
    }
    ```

* **`UNIFIED_EVENTS` Filter Branch:**
    * Only nested within `AND` branches.
    * Filters based on whether unified events have or haven't been completed.
    * Requires `eventTypeId` and `operator` (e.g., `"HAS_COMPLETED"` or `"HAS_NOT_COMPLETED"`).

    ```json
    {
      "filterBranchType": "UNIFIED_EVENTS",
      "filterBranches": [],
      "filters": [ /* One or more PROPERTY filters */ ],
      "eventTypeId": "event-id",
      "operator": "HAS_COMPLETED"
    }
    ```

* **`ASSOCIATION` Filter Branch:**
    * Only nested within `AND` branches.
    * Filters based on associated records.
    * Requires `objectTypeId`, `operator` (e.g., `"IN_LIST"`), `associationTypeId`, and `associationCategory`.

    ```json
    {
      "filterBranchType": "ASSOCIATION",
      "filterBranches": [],
      "filters": [ /* Filters for associated records */ ],
      "objectTypeId": "object-type-id",
      "operator": "IN_LIST",
      "associationTypeId": 123,
      "associationCategory": "HUBSPOT_DEFINED"
    }
    ```

## Filter Types (`filterType`)

Several filter types exist, allowing for complex list definitions:  `ADS_TIME`, `ADS_SEARCH`, `CTA`, `EMAIL_EVENT`, `EVENT`, `FORM_SUBMISSION`, `FORM_SUBMISSION_ON_PAGE`, `IN_LIST`, `PAGE_VIEW`, `PRIVACY`, `PROPERTY`, `SURVEY_MONKEY`, `SURVEY_MONKEY_VALUE`, `WEBINAR`, `INTEGRATION_EVENT`.  The `PROPERTY` type is the most versatile and is discussed in detail below.


## `PROPERTY` Filter Operations

The `PROPERTY` filter type uses an `operation` object to define its parameters:

* **`operationType`:** Specifies the operator type (e.g., `NUMBER`, `STRING`, `MULTISTRING`, `TIME_POINT`, `TIME_RANGED`).
* **`operator`:** The specific operator (e.g., `IS_EQUAL_TO`, `CONTAINS`, `IS_BEFORE`, `IS_BETWEEN`).
* **`value` / `values`:** The value(s) to filter against.
* **`includeObjectsWithNoValueSet`:**  (Boolean) Determines how records with no value for the property are handled.  Defaults to `false` (rejected).

**Example (`firstname` is "John"):**

```json
{
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
  ]
}
```

See the detailed table in the original text for a complete list of `operationType` values and supported operators.

## Time-Based Filters (`TIME_POINT`, `TIME_RANGED`)

These operations provide powerful time-based filtering.  Examples include:

* **`Is equal to date`:**  Filters for records with a property value matching a specific date.
* **`In Last X Number of Days`:**  Filters for records updated within the last X days.
* **`In Next X Number of Days`:** Filters for records to be updated within the next X days.
* **`Updated or Not Updated in the Last X Days`:** Filters based on whether a property was updated in the last X days.
* **`Is After Date`:** Filters for records updated after a specific date.
* **`Is Relative to Today`:** Filters relative to today's date (e.g., X days ago/from now).
* **`Is Before or After another property`:** Compares a property's value/last updated time to another property.


Refer to the provided JSON examples in the original text for detailed syntax on these time-based filters.


## Refine By Operations

* **`pruningRefineBy`:** Refines the dataset to a specific timeframe (absolute or relative).
* **`coalescingRefineBy`:** Determines if a record passes the filter a minimum/maximum number of times.

Only one refine-by operation is allowed per filter.


## Legacy v1 Lists API

While similar to v3, the v1 API has differences in syntax and available options.  **Note:** The v1 API is sunsetted.  Migrate to v3.  The v1 API only supports the `PROPERTY` filter type.


This comprehensive guide provides a solid understanding of HubSpot Lists API v3 filtering capabilities, enabling the creation of sophisticated list definitions. Remember to consult the official HubSpot documentation for the most up-to-date information and detailed API specifications.
