# HubSpot Lists API v3: List Filters Overview

This document provides a comprehensive overview of HubSpot's Lists API v3 filter functionalities, including structure, filter types, operations, and examples.  The legacy v1 API is also briefly discussed.

## List Filters

List filters allow you to define criteria to determine which records belong to a list.  When creating a list with `SNAPSHOT` or `DYNAMIC` processing type, filters are essential for membership determination.

Filters use conditional logic defined by *filter branches* with `AND` or `OR` operation types (`filterBranchType` parameter).  Each branch contains individual filters (`filterType` parameter) assessing records for inclusion.  Nested branches are supported.

HubSpot uses PASS/FAIL logic. A record becomes a list member only if it passes *all* filters.


## Filter Evaluation Steps

1. **Record Selection:** Relevant records are selected based on the filter (e.g., all records for a `property` filter).
2. **Pruning Refinement (Optional):** `pruningRefineBy` parameter refines the data to a specific time range.
3. **Filtering:** Filtering rules are applied to the refined data to determine PASS/FAIL.
4. **Coalescing Refinement (Optional):** `coalescingRefineBy` further refines data based on the number of occurrences (e.g., "contact filled out a form at least 2 times").  Records passing the required number of occurrences are marked PASS.
5. **Final PASS/FAIL:** If no `coalescingRefineBy` is present, step 3 determines PASS/FAIL.


## Filter Branches

A filter branch is a data structure defining conditional logic.  It includes:

*   **`filterBranchType`:** `OR` or `AND`.
*   **Operator:** `OR` (any condition passes) or `AND` (all conditions pass).
*   **Filters:** A list of individual filters.
*   **Sub-branches:** Nested filter branches.

**Structure:** All filter definitions begin with a root-level `OR` branch, followed by one or more `AND` sub-branches.

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

This creates a list of contacts with firstname "John" OR lastname not "Smith".


## Filter Branch Types

*   **`OR`:**  Must have one or more `AND` sub-branches; no filters allowed.  Passes if *any* nested branch passes.
*   **`AND`:** Can have zero or more filters and zero or more nested `UNIFIED_EVENTS` and/or `ASSOCIATION` branches. Passes only if *all* filters and nested branches pass.
*   **`UNIFIED_EVENTS`:** Nested within `AND`; filters on events; requires one or more `PROPERTY` filters; no nested branches.
*   **`ASSOCIATION`:** Nested within `AND`; filters on associated records; requires one or more filters; allows nested branches only for `CONTACT` to `LINE_ITEM` associations.


## Filter Types

The `filterType` parameter defines the filter's logic.  Some key types include:

*   `PROPERTY`: Evaluates a record's property value.  See "Property Filter Operations" below.
*   `ADS_TIME`, `ADS_SEARCH`, `CTA`, `EMAIL_EVENT`, `EVENT`, `FORM_SUBMISSION`, `FORM_SUBMISSION_ON_PAGE`, `IN_LIST`, `PAGE_VIEW`, `PRIVACY`, `SURVEY_MONKEY`, `SURVEY_MONKEY_VALUE`, `WEBINAR`, `INTEGRATION_EVENT`: Evaluate interactions with specific HubSpot features or integrations.


## Property Filter Operations

The `operation` object defines the parameters for `PROPERTY`, `INTEGRATION_EVENT`, and `SURVEY_MONKEY_VALUE` filters:

*   **`operationType`:**  The type of operator (e.g., `NUMBER`, `MULTISTRING`).
*   **`operator`:** The specific operator (e.g., `IS_EQUAL_TO`, `CONTAINS`).
*   **`value`/`values`:** The value(s) to filter by.
*   **`includeObjectsWithNoValueSet`:** (boolean)  Whether to include records with no value for the property. Defaults to `false`.


## Time-Based Filters (`TIME_POINT`, `TIME_RANGED`)

These operations allow filtering based on timestamps:

*   **`TIME_POINT`:**  Compares a property's value or last update time to a single point in time (specific date or relative to today).
*   **`TIME_RANGED`:** Compares a property's value or last update time to a time range.

Examples are provided in the original text for various scenarios (e.g., "Is equal to date", "In Last X Number of Days", etc.).


## Refine By Operations

*   **`pruningRefineBy`:** Refines the dataset to a timeframe (absolute or relative).
*   **`coalescingRefineBy`:** Determines if a record passes the filter a minimum/maximum number of times.

Only one refine by operation is allowed per filter.


## Legacy v1 Lists API

The v1 API is deprecated and will be sunsetted.  It is similar to v3 but has differences in syntax and available options.  The only supported `filterType` is `PROPERTY`.


## Conclusion

HubSpot's Lists API v3 offers a flexible and powerful filtering system.  Understanding the structure of filter branches and the various filter types and operations is crucial for effectively managing and segmenting your lists.  Remember to consult the official HubSpot documentation for the most up-to-date information and detailed specifications.
