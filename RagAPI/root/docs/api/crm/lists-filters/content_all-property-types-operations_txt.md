# HubSpot Lists API v3 Filter Documentation

This document details the structure and usage of filters within HubSpot's Lists API v3.  It describes how to construct filter definitions to select specific records for inclusion in a list.  The API uses a hierarchical structure of `OR` and `AND` branches, combined with various filter types to define complex logic.

## Overview

When creating a HubSpot list with `SNAPSHOT` or `DYNAMIC` processing type, filters determine which records are included.  Filters utilize conditional logic defined by filter branches with `AND` or `OR` operation types (`filterBranchType` parameter).  These branches contain individual filters (`filterType` parameter) assessing records for inclusion.  Nested filter branches are also supported.

HubSpot uses PASS/FAIL logic. A record is a list member only if it passes *all* filters.

## Filter Evaluation Steps

1. **Record Selection:** Relevant records are selected based on the chosen filter (e.g., all records for a property filter).
2. **Pruning (Optional):** The `pruningRefineBy` parameter refines the data to a specific time range.
3. **Filtering:** Filtering rules are applied to the refined data to determine PASS or FAIL.
4. **Coalescing (Optional):** The `coalescingRefineBy` parameter further refines data based on the number of occurrences (e.g., "contact has filled out a form at least 2 times").  If present, records pass if they meet the specified occurrence count. Otherwise, PASS/FAIL is determined by step 3.

## Filter Branches

Filter branches structure the conditional logic.  They are defined by type (`filterBranchType`), operator (`OR` or `AND`), a list of filters, and a list of sub-branches.

* **`OR` Branch:** Accepts a record if it passes *any* of its filters or sub-branches.  Must contain one or more `AND` sub-branches and cannot have any direct filters.

* **`AND` Branch:** Accepts a record only if it passes *all* its filters and sub-branches. Can have zero or more filters and zero or more nested `UNIFIED_EVENTS` and/or `ASSOCIATION` branches.

**Structure:** All filter definitions must start with a root-level `OR` branch, containing one or more `AND` sub-branches.

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

This creates a list of contacts with a first name "John" OR those without a last name "Smith".

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

This creates a list of contacts with a first name "John" AND a last name "Smith".


## Special Filter Branch Types

* **`UNIFIED_EVENTS`:** Filters on events.  Must be nested within an `AND` branch and requires at least one `PROPERTY` filter.

* **`ASSOCIATION`:** Filters on associated records. Must be nested within an `AND` branch and requires at least one filter.  Additional `filterBranches` are allowed only for `CONTACT` to `LINE_ITEM` associations.


## Filter Types

The `filterType` parameter specifies the filter's logic.  Common types include:

* `PROPERTY`: Evaluates a record's property value against specified criteria (see "Property Filter Operations").
* `ADS_TIME`, `ADS_SEARCH`, `CTA`, `EMAIL_EVENT`, `EVENT`, `FORM_SUBMISSION`, `FORM_SUBMISSION_ON_PAGE`, `IN_LIST`, `PAGE_VIEW`, `PRIVACY`, `SURVEY_MONKEY`, `SURVEY_MONKEY_VALUE`, `WEBINAR`, `INTEGRATION_EVENT`:  Each evaluates interactions with specific HubSpot features or integrations.


## Property Filter Operations

The `operation` object within a `PROPERTY` filter defines the criteria.  Key fields include:

* `operationType`:  Specifies the data type (e.g., `NUMBER`, `STRING`, `MULTISTRING`, `TIME_POINT`, `TIME_RANGED`).
* `operator`:  The comparison operator (e.g., `IS_EQUAL_TO`, `CONTAINS`, `IS_BETWEEN`).
* `value` / `values`: The value(s) to compare against.
* `includeObjectsWithNoValueSet`:  Whether to include records with no value set for the property (default is `false`).


## Time-Based Filters (`TIME_POINT` and `TIME_RANGED`)

These operations provide flexible time-based filtering:

* **`TIME_POINT`:** Compares a property's value or last updated time to a single point in time (specific date, relative to today, or another property).  Examples: `IS_EQUAL_TO`, `IS_AFTER`, `IS_BEFORE`.

* **`TIME_RANGED`:** Compares a property's value or last updated time to a range. Examples: `IS_BETWEEN`, `IS_NOT_BETWEEN`.


## Refine By Operations

* **`pruningRefineBy`:** Refines the dataset to a specific time range (absolute or relative).
* **`coalescingRefineBy`:**  Determines if a record passes the filter a minimum/maximum number of times (`NUM_OCCURRENCES`).

Only one refine by operation is allowed per filter.


## Legacy v1 Lists API

While similar to v3, the v1 API has minor differences in syntax and options.  **Note:** The v1 API is deprecated.


This documentation provides a comprehensive overview of HubSpot's Lists API v3 filtering capabilities. For detailed information on specific filter types and operators, consult the HubSpot API reference documentation.
