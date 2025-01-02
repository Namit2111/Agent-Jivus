# HubSpot Lists API: Filter Documentation

This document details the structure and usage of filters within the HubSpot Lists API (v3).  It explains how to construct filter definitions using JSON to create lists based on various criteria.  The legacy v1 API is also briefly discussed.

## List Filters Overview

List filters allow you to define the membership criteria for both SNAPSHOT and DYNAMIC lists.  They use conditional logic implemented through *filter branches* and individual *filters*.

* **Filter Branches:** Define the logical structure (AND/OR) connecting individual filters.
* **Filters:** Specify conditions applied to individual record properties to determine list membership.  A record is a list member if it passes all filters within the root filter branch.

HubSpot uses PASS/FAIL logic. A record is added to the list only if it passes *all* conditions.

## Filter Evaluation Steps

1. **Record Selection:** Relevant records are selected based on the chosen filter (e.g., all records for a property filter).
2. **Pruning (Optional):** `pruningRefineBy` refines the data to a specific time range.
3. **Filtering:** Filtering rules are applied to determine PASS/FAIL.
4. **Coalescing (Optional):** `coalescingRefineBy` further refines based on the number of occurrences (e.g., "contact has filled out a form at least 2 times").
5. **Final Result:** Records pass or fail based on steps 3 and 4.

## Filter Branch Structure

All filter definitions must begin with a root-level `OR` filter branch, containing one or more nested `AND` sub-branches. This structure is required by the HubSpot API for proper UI rendering.

**Example JSON (OR with two AND branches):**

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

This example creates a list of contacts with a first name "John" OR those without a last name "Smith".  Each nested `AND` branch represents a distinct condition group.

**Example JSON (OR with one AND branch):**

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

This example creates a list of contacts with a first name "John" AND a last name "Smith".


## Filter Branch Types

* **`OR`:**  Requires one or more nested `AND` branches. Accepts a record if *any* nested branch accepts it.  Cannot have any direct filters.
* **`AND`:** Can have zero or more filters and zero or more nested `UNIFIED_EVENTS` or `ASSOCIATION` branches. Accepts a record only if *all* nested branches and filters accept it.
* **`UNIFIED_EVENTS`:**  Nested within `AND`. Filters on unified events (requires at least one `PROPERTY` filter).  Cannot have nested branches.
* **`ASSOCIATION`:** Nested within `AND`. Filters on associated records (requires at least one filter).  Can only have additional `filterBranches` for `CONTACT` to `LINE_ITEM` associations.

## Filter Types

The `filterType` parameter specifies the type of condition to apply.  Examples include: `PROPERTY`, `ADS_TIME`, `CTA`, `EMAIL_EVENT`, `EVENT`, `FORM_SUBMISSION`, `IN_LIST`, `PAGE_VIEW`, and more.  See the original document for a full list.


## Property Filter Operations

Used with `PROPERTY`, `INTEGRATION_EVENT`, and `SURVEY_MONKEY_VALUE` filter types.  Defines the filter's parameters:

* `operationType`:  The type of operation (e.g., `NUMBER`, `STRING`, `MULTISTRING`, `TIME_POINT`, `TIME_RANGED`).
* `operator`: The operator to apply (e.g., `IS_EQUAL_TO`, `CONTAINS`, `IS_BETWEEN`).
* `value`/`values`: The value(s) to compare against.
* `includeObjectsWithNoValueSet`:  Whether to include records with no value for the property (defaults to `false`).

## Time-Based Filter Examples

The original document provides numerous examples for `TIME_POINT` and `TIME_RANGED` operations, including:

* **Is equal to date:** Filtering based on exact dates.
* **In Last X Number of Days:** Filtering within a specific past timeframe.
* **In Next X Number of Days:** Filtering within a specific future timeframe.
* **Updated or Not Updated in the Last X Days:** Filtering based on property update timestamps.
* **Is After Date:** Filtering based on a date cutoff.
* **Is Relative to Today:** Filtering based on an offset from the current date.
* **Is Before or After another property:** Comparing property values or timestamps.


## Refine By Operations

* **`pruningRefineBy`:** Refines the dataset to a specific time range (absolute or relative).
* **`coalescingRefineBy`:**  Determines if a record meets the filter criteria a specified number of times.

Only one refine by operation can be used per filter.

## Legacy v1 List Filters

The v1 API (deprecated) is similar to v3 but with minor syntax differences and fewer options.  The `PROPERTY` filter type is the only one supported.  The v1 API is being sunsetted.


This markdown documentation provides a comprehensive overview of the HubSpot Lists API's filtering capabilities, including detailed JSON examples and explanations of each parameter. Remember to refer to the official HubSpot API documentation for the most up-to-date information and details.
