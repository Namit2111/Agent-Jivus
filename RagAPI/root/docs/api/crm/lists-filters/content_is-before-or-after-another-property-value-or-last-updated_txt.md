# HubSpot Lists API v3: Filter Documentation

This document details the structure and usage of filters within the HubSpot Lists API v3.  The API allows for creating dynamic and snapshot lists by defining complex filtering logic.  This logic is built using filter branches with `AND` and `OR` operations, and individual filter types to define criteria.


## List Filter Overview

Filters determine which records are included in a HubSpot list.  The filtering process uses a tree-like structure of filter branches and individual filters.

* **Processing Type:** Lists are created with either `SNAPSHOT` or `DYNAMIC` processing types. Filters are used in both.
* **Filter Branches:**  Organize filters using `AND` and `OR` logic.  The root branch is always `OR`.
* **Filter Types:** Define specific criteria for filtering (e.g., property values, events, associations).
* **Evaluation:** Records are evaluated sequentially against the filter structure.  A record is included in the list only if it passes all filters within the root filter branch.


## Filter Structure

All filter definitions begin with a root-level `OR` filter branch. This root `OR` branch contains one or more nested `AND` sub-branches.

**Basic JSON Structure:**

```json
{
  "filterBranch": {
    "filterBranches": [
      {
        "filterBranches": [],
        "filterBranchType": "AND",
        "filters": [ /* Individual filters */ ]
      },
      {
        "filterBranches": [],
        "filterBranchType": "AND",
        "filters": [ /* Individual filters */ ]
      }
    ],
    "filterBranchType": "OR",
    "filters": []
  }
}
```

**Example: "First Name is John" OR "Last Name is not Smith"**

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

**Example: "First Name is John" AND "Last Name is Smith"**

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

## Filter Branch Types

* **`OR`:** Accepts a record if *any* of its nested `AND` branches accept it.  Must have at least one nested `AND` branch.  Cannot have any filters directly within the `OR` branch.

* **`AND`:** Accepts a record only if *all* of its filters and nested branches accept it. Can have zero or more filters and nested branches (including `UNIFIED_EVENTS` and `ASSOCIATION`).

* **`UNIFIED_EVENTS`:** Filters based on HubSpot events.  Only nested within `AND` branches. Requires at least one filter.  Example:  `HAS_COMPLETED`, `HAS_NOT_COMPLETED`.

* **`ASSOCIATION`:** Filters based on associated objects.  Only nested within `AND` branches.  Requires at least one filter. Example: `IN_LIST`.


## Filter Types

The `filterType` parameter specifies the type of filter:

* `PROPERTY`: Filters based on property values. (See "Property Filter Operations" below).
* `ADS_TIME`, `ADS_SEARCH`, `CTA`, `EMAIL_EVENT`, `EVENT`, `FORM_SUBMISSION`, `FORM_SUBMISSION_ON_PAGE`, `IN_LIST`, `PAGE_VIEW`, `PRIVACY`, `SURVEY_MONKEY`, `SURVEY_MONKEY_VALUE`, `WEBINAR`, `INTEGRATION_EVENT`:  Each filters based on a specific HubSpot feature's interactions.


## Property Filter Operations

`PROPERTY` filters use an `operation` object to specify criteria:

* `operationType`:  The type of operation (e.g., `NUMBER`, `STRING`, `MULTISTRING`, `TIME_POINT`, `TIME_RANGED`, `BOOL`, `ENUMERATION`, `ALL_PROPERTY`).
* `operator`:  The comparison operator (e.g., `IS_EQUAL_TO`, `IS_NOT_EQUAL_TO`, `CONTAINS`, `IS_BETWEEN`, `IS_BEFORE`, `IS_AFTER`).
* `value` or `values`: The value(s) to compare against.
* `includeObjectsWithNoValueSet`:  A boolean indicating whether to include records without a value for the property.


## Time-Based Operations (`TIME_POINT` and `TIME_RANGED`)

These operation types are used for filtering based on timestamps:

* **`TIME_POINT`:**  Compares a single timestamp.  Operators: `IS_AFTER`, `IS_BEFORE`, `IS_EQUAL_TO`.
* **`TIME_RANGED`:** Compares a timestamp range. Operators: `IS_BETWEEN`, `IS_NOT_BETWEEN`.

Examples for these are detailed in the original text, showcasing different date representations (absolute, relative to "today" or "now", relative to another property).


## Refine By Operations

These operations further refine the dataset *after* initial filter evaluation.

* **`pruningRefineBy`:** Refines the dataset to a specific time range (absolute or relative).  Types: `ABSOLUTE_COMPARATIVE`, `ABSOLUTE_RANGED`, `RELATIVE_COMPARATIVE`, `RELATIVE_RANGED`.

* **`coalescingRefineBy`:**  Specifies the minimum and maximum number of times a record must satisfy the filter criteria to be included. Type: `NUM_OCCURRENCES`.


## Legacy v1 Lists API

The original text mentions a legacy v1 API, which is being sunset.  The core concepts remain similar, but the syntax and available options differ.  Details on the differences are present in the original text.


This markdown documentation provides a comprehensive overview of HubSpot's List API v3 filtering capabilities. Remember to refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications.
