# HubSpot Lists API v3: List Filters Overview

This document provides a comprehensive overview of HubSpot's Lists API v3 filter functionality.  It explains how to construct filter definitions to select specific records for your lists.  The API uses a hierarchical structure based on `OR` and `AND` logic to define complex filtering conditions.

## List Filter Basics

When creating a HubSpot list with `SNAPSHOT` or `DYNAMIC` processing type, filters determine which records are included.  Filters utilize conditional logic structured through filter branches with `AND` or `OR` operation types (`filterBranchType` parameter).  These branches contain individual filters (`filterType` parameter) that evaluate records.  Nested filter branches are also possible.

HubSpot uses `PASS`/`FAIL` logic. A record becomes a list member only if it passes *all* filters.

## Filter Evaluation Steps

1. **Record Selection:** Relevant records are selected based on the filter.  For example, a `property` filter selects records based on their property values.
2. **Pruning Refinement (Optional):** The `pruningRefineBy` parameter refines the dataset to a specific time range.
3. **Filtering:** Filtering rules are applied to the refined dataset to determine `PASS` or `FAIL`.
4. **Coalescing Refinement (Optional):** The `coalescingRefineBy` parameter further refines the data based on the number of occurrences (e.g., "contact has filled out a form at least 2 times").  If present, records only pass if they meet the specified occurrence count.  Otherwise, the result from step 3 is used.


## Filter Branches

A filter branch defines conditional logic.  It's specified by its type (`filterBranchType`), operator (`OR` or `AND`), a list of filters, and a list of sub-branches.

* **`AND` Operator:** A record is accepted if it passes *all* filters and sub-branches within the branch.
* **`OR` Operator:** A record is accepted if it passes *any* filter or sub-branch within the branch.

A list's root filter branch dictates membership.

## Filter Branch Structure

All filter definitions must begin with a root-level `OR` filter branch. This `OR` branch must contain one or more `AND` sub-branches.  This structure is mandatory for proper UI rendering in HubSpot.

**Example JSON (OR with two AND sub-branches):**

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

This example creates a list of contacts with the first name "John" OR those who do not have the last name "Smith".


## Special Filter Branch Types

* **`UNIFIED_EVENTS`:** Filters based on events.  Must be nested within an `AND` branch. Requires at least one filter.
* **`ASSOCIATION`:** Filters based on associated records. Must be nested within an `AND` branch. Requires at least one filter.  Additional `filterBranches` are allowed only for `CONTACT` to `LINE_ITEM` associations.

## Filter Types

The `filterType` parameter specifies the type of filter.  Some examples include:

| `filterType`          | Description                                                                        |
|-----------------------|------------------------------------------------------------------------------------|
| `PROPERTY`            | Filters based on a record's property value.  See "Property Filter Operations" below. |
| `ADS_TIME`            | Filters based on ad views within a timeframe.                                      |
| `FORM_SUBMISSION`     | Filters based on form submissions.                                                  |
| `IN_LIST`             | Filters based on membership in another list, import, or workflow.                   |
| `INTEGRATION_EVENT`   | Filters based on integration events.                                               |
|  ...                  | ...                                                                                |


## Property Filter Operations

`PROPERTY`, `INTEGRATION_EVENT`, and `SURVEY_MONKEY_VALUE` filters use an `operation` object with these fields:

* `operationType`:  The type of operator (e.g., `NUMBER`, `MULTISTRING`).
* `operator`: The specific operator (e.g., `IS_EQUAL_TO`, `CONTAINS`).
* `value` / `values`: The value(s) to filter by.
* `includeObjectsWithNoValueSet`: `true` to include records with no value for the property; `false` (default) to exclude them.

**Example:**

```json
{
  "filterType": "PROPERTY",
  "property": "firstname",
  "operation": {
    "operationType": "MULTISTRING",
    "operator": "IS_EQUAL_TO",
    "values": ["John"]
  }
}
```

## Time-Based Filter Operations (`TIME_POINT`, `TIME_RANGED`)

These operations allow filtering based on timestamps, either absolute dates or relative to the current date.  Examples provided in the original text illustrate how to use these parameters for various scenarios such as "In Last X Number of Days," "Is After Date," etc.  The examples show detailed JSON structures for these date and time filters.


## Refine By Operations

* **`pruningRefineBy`:** Refines the dataset to a specific time range (absolute or relative).  Supports `ABSOLUTE_COMPARATIVE`, `ABSOLUTE_RANGED`, `RELATIVE_COMPARATIVE`, `RELATIVE_RANGED`.
* **`coalescingRefineBy`:**  Filters based on the number of times a record meets the filter criteria. Supports `NUM_OCCURRENCES`.

Only one refine-by operation is allowed per filter.

## Legacy v1 Lists API

The v1 API is deprecated and will be sunsetted.  While similar to v3, it has differences in syntax and available options.  Migration to v3 is recommended.  The provided text illustrates the v1 filter structure, showcasing its use of `PROPERTY` filter type with different operators.


##  Property Type Specific Operations (v1 API)

The v1 API documentation provides detailed information on operators supported for each property type:  `alltypes`, `string`, `multistring`, `number`, `boolean`, and `enumeration`.  Examples for each are provided showing how to build filters for each data type using various operators.  The datetime property type offers several sub-types (`datetime`, `datetime-comparative`, `datetime-ranged`, `datetime-rolling`, `rolling-property-updated`) each with their own set of supported operators.  Examples are shown for each of these sub-types to illustrate how to filter for different date and time scenarios.

This Markdown provides a structured and concise overview of HubSpot's List API v3 filtering capabilities. Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
