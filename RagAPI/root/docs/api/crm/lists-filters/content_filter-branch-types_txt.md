# HubSpot Lists API: Filter Documentation

This document details the usage of filters within the HubSpot Lists API (v3).  It covers the structure, types, and operations of filters, providing examples for common use cases.  The legacy v1 API is also briefly discussed.

## Overview

List filters allow you to define the criteria for including records in a HubSpot list.  They utilize a conditional logic system based on filter branches with `AND` or `OR` operations.  Each branch can contain individual filters and nested branches.  The system uses a `PASS`/`FAIL` logic; a record must pass all filters to be included.

**Filter Evaluation Steps:**

1. **Record Selection:** Relevant records are selected based on the filter criteria (e.g., all records for a property filter).
2. **Pruning (Optional):** `pruningRefineBy` refines the data to a specific time range.
3. **Filtering:** Filtering rules are applied to the refined data. Records pass or fail based on these rules.
4. **Coalescing (Optional):** `coalescingRefineBy` further refines the data based on the number of occurrences (e.g., "contact filled out a form at least 2 times").
5. **Final Evaluation:** Records that pass all steps are included in the list.

## Filter Structure

Filters are defined using a JSON structure, always starting with a root-level `OR` filter branch.  This root branch contains one or more nested `AND` sub-branches.

**Example (Root OR with two nested AND branches):**

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

This example creates a list of contacts with a first name of "John" OR a last name that is not "Smith".  Note the nested `AND` branches ensure proper UI rendering.

## Filter Branch Types

* **`OR`:**  The root-level branch. Accepts a record if *any* of its nested `AND` branches accept it.  Cannot have filters directly within it.

* **`AND`:** Nested within `OR` branches. Accepts a record only if *all* of its filters and nested branches accept it.  Can contain `UNIFIED_EVENTS` and/or `ASSOCIATION` branches.

* **`UNIFIED_EVENTS`:**  Nested only within `AND` branches. Filters based on HubSpot unified events. Requires one or more `PROPERTY` filters.

* **`ASSOCIATION`:** Nested only within `AND` branches. Filters based on associated records. Requires one or more filters. Can have additional nested `ASSOCIATION` branches for `CONTACT` to `LINE_ITEM` associations.


## Filter Types

The `filterType` parameter specifies the type of filter.  Examples include:

| `filterType`         | Description                                                                        |
|----------------------|------------------------------------------------------------------------------------|
| `PROPERTY`           | Filters based on a record's property value.                                          |
| `ADS_TIME`           | Filters based on ad interactions within a timeframe.                               |
| `ADS_SEARCH`         | Filters based on ad search interactions.                                           |
| `CTA`                | Filters based on call-to-action interactions.                                        |
| `EMAIL_EVENT`        | Filters based on email subscription opt-in status.                                  |
| `EVENT`              | Filters based on events.                                                             |
| `FORM_SUBMISSION`    | Filters based on form submissions.                                                 |
| `FORM_SUBMISSION_ON_PAGE` | Filters based on form submissions on a specific page.                              |
| `IN_LIST`            | Filters based on membership in another list, import, or workflow.                    |
| `PAGE_VIEW`          | Filters based on page views.                                                         |
| `PRIVACY`            | Filters based on privacy consent.                                                   |
| `SURVEY_MONKEY`      | Filters based on Survey Monkey survey responses.                                    |
| `SURVEY_MONKEY_VALUE` | Filters based on specific Survey Monkey survey question responses with a value.      |
| `WEBINAR`            | Filters based on webinar registrations and attendance.                             |
| `INTEGRATION_EVENT` | Filters based on interactions with integration events.                             |


## Property Filter Operations

The `PROPERTY` filter type uses an `operation` object to define the filtering logic:

* **`operationType`:**  The type of property (e.g., `NUMBER`, `STRING`, `MULTISTRING`, `TIME_POINT`, `TIME_RANGED`).

* **`operator`:** The comparison operator (e.g., `IS_EQUAL_TO`, `IS_GREATER_THAN`, `CONTAINS`).

* **`value` / `values`:** The value(s) to compare against.

* **`includeObjectsWithNoValueSet`:** (Boolean)  Determines how records without a value for the property are handled. `true` includes them, `false` excludes them (default).

## Time-Based Filter Examples

The `TIME_POINT` and `TIME_RANGED` `operationType`s are used for time-based filters.  Here are several examples:

* **`Is equal to date`:**

```json
// ... (filterBranch structure) ...
"operation": {
  "operator": "IS_BETWEEN",
  "lowerBoundTimePoint": { "timeType": "DATE", "year": 2024, "month": 3, "day": 11, ... },
  "upperBoundTimePoint": { "timeType": "DATE", "year": 2024, "month": 3, "day": 11, ... },
  "operationType": "TIME_RANGED"
}
// ...
```

* **`In Last X Number of Days`:**

```json
// ... (filterBranch structure) ...
"lowerBoundTimePoint": { "timeType": "INDEXED", "indexReference": { "referenceType": "TODAY" }, "offset": { "days": -3 } },
// ...
```

* **`In Next X Number of Days`:**  Similar to "In Last X" but with positive `offset`.

* **`Updated or Not Updated in the Last X Days`:** Uses `propertyParser: "UPDATED_AT"` to check update timestamps.


## Refine By Operations

* **`pruningRefineBy`:** Refines the dataset to a specific time range (absolute or relative).

* **`coalescingRefineBy`:** Determines whether a record passed the filter a minimum/maximum number of times.  Only `NUM_OCCURRENCES` is supported.

## Legacy v1 Lists API

The v1 API is deprecated.  It shares similarities with v3 but has differences in syntax and available options.  The primary filter type is `PROPERTY`.

## Conclusion

This document provides a comprehensive overview of the HubSpot Lists API v3 filtering capabilities.  Refer to the full HubSpot documentation for detailed information on all supported properties, operators, and edge cases. Remember that the v1 API is deprecated, and migrating to v3 is recommended.
