# HubSpot Lists API: Filter Documentation

This document details the filter structure and options available when creating lists within the HubSpot CRM using the Lists API (v3).  It also briefly covers the legacy v1 API.

## List Filter Overview

List filters allow you to define the criteria for including records in a HubSpot list.  You construct filters using a hierarchical structure of filter branches with `AND` or `OR` logic.  The overall structure is always an `OR` branch containing one or more `AND` sub-branches.

### Filter Evaluation Steps

1. **Record Selection:** The API selects or fetches the relevant records based on the filter's initial criteria (e.g., property values for a `PROPERTY` filter).

2. **Pruning Refinement (Optional):** If a `pruningRefineBy` parameter is included, it refines the dataset to a specific time range.

3. **Filter Application:** Filtering rules are applied to the (potentially refined) data. Records either `PASS` or `FAIL` based on these rules.

4. **Coalescing Refinement (Optional):** If a `coalescingRefineBy` parameter is present, the results are further refined based on the number of times a record meets the filter criteria (e.g., "filled out a form at least 2 times").

5. **Final Result:** Records that `PASS` all filters become members of the list.


### Filter Branches

Filter branches structure the conditional logic. Each branch has a `filterBranchType` (`OR` or `AND`) and may contain filters and nested branches.

* **`OR` Branch:** A record is accepted if it passes *any* of its child branches or filters.  Must contain at least one `AND` sub-branch. Cannot contain any direct filters.

* **`AND` Branch:** A record is accepted if it passes *all* of its child branches and filters. Can have zero or more filters and nested `UNIFIED_EVENTS` or `ASSOCIATION` branches.


### Basic Filter Structure (JSON)

The fundamental structure starts with an `OR` branch containing one or more `AND` branches:

```json
{
  "filterBranch": {
    "filterBranches": [
      {
        "filterBranches": [],
        "filterBranchType": "AND",
        "filters": [ /* filters here */ ]
      },
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

### Example: "First Name is John OR Last Name is not Smith"

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

### Example: "First Name is John AND Last Name is Smith"

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

## Special Filter Branch Types

* **`UNIFIED_EVENTS`:** Filters on events. Must be nested within an `AND` branch. Requires at least one filter.

* **`ASSOCIATION`:** Filters on records associated with the primary record. Must be nested within an `AND` branch. Requires at least one filter.  May contain nested `ASSOCIATION` branches for certain object types (e.g., `CONTACT` to `LINE_ITEM`).


## Filter Types

The `filterType` parameter specifies the type of filter.  Common types include:

* `PROPERTY`: Filters based on object properties (see Property Filter Operations).
* `ADS_TIME`, `ADS_SEARCH`, `CTA`, `EMAIL_EVENT`, `EVENT`, `FORM_SUBMISSION`, `FORM_SUBMISSION_ON_PAGE`, `IN_LIST`, `PAGE_VIEW`, `PRIVACY`, `SURVEY_MONKEY`, `SURVEY_MONKEY_VALUE`, `WEBINAR`, `INTEGRATION_EVENT`:  Filters based on specific HubSpot interactions or events.


## Property Filter Operations

The `operation` object within a `PROPERTY` filter defines the comparison:

* `operationType`:  The type of property (e.g., `NUMBER`, `STRING`, `MULTISTRING`, `TIME_POINT`, `TIME_RANGED`, `ENUMERATION`, `BOOL`, `ALL_PROPERTY`).
* `operator`: The comparison operator (e.g., `IS_EQUAL_TO`, `IS_GREATER_THAN`, `CONTAINS`, `IS_BETWEEN`).
* `value` / `values`: The value(s) to compare against.
* `includeObjectsWithNoValueSet`:  Whether to include records with no value for the specified property (true/false, defaults to false).


## Time-Based Filter Operations (`TIME_POINT` and `TIME_RANGED`)

These operations allow filtering based on timestamps, either absolute dates or relative to "today" or "now".  Refer to the provided examples in the original text for specific JSON structures for various scenarios (e.g., "Is equal to date," "In Last X Number of Days," etc.).


## Refine By Operations

* **`pruningRefineBy`:** Refines the dataset to a specific time range (absolute or relative).
* **`coalescingRefineBy`:** Refines the results based on the minimum and maximum number of times a record meets the filter criteria.


## Legacy v1 Lists API

The v1 API is deprecated.  Its filtering is similar but less flexible than v3.  Only `PROPERTY` filters are supported.


## Conclusion

HubSpot's List API offers a robust filtering mechanism with flexible `AND`/`OR` logic and a wide range of filter types and operators.  Understanding the hierarchical structure of filter branches is crucial for building effective list definitions.  Always refer to the official HubSpot API documentation for the most up-to-date information on supported parameters and their options.
