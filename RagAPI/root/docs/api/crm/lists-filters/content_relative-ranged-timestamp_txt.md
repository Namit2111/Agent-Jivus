# HubSpot Lists API v3: List Filters Overview

This document details the structure and usage of filters within the HubSpot Lists API v3.  Filters determine which records are included in a HubSpot list, supporting both `SNAPSHOT` and `DYNAMIC` list processing types.

## API Call and Response Structure

The HubSpot Lists API uses a POST request to create or update lists. The filter definition is part of the request body in JSON format.  The response will typically include a status code (e.g., 200 OK for success) and potentially a list ID.  Error responses will include details about the failure.


## Filter Structure

HubSpot list filters use a hierarchical structure based on `filterBranchType` (OR or AND) and individual filters (`filterType`).

**Base Structure:**

All filter definitions begin with a root-level `OR` filter branch. This `OR` branch must contain one or more nested `AND` sub-branches.  Each `AND` branch can contain multiple individual filters or further nested branches (including `UNIFIED_EVENTS` and `ASSOCIATION` types).

```json
{
  "filterBranch": {
    "filterBranches": [
      {
        "filterBranches": [],
        "filterBranchType": "AND",
        "filters": [ /* Filters for this AND branch */ ]
      },
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

**Example: Contacts with First Name "John" OR Last Name not "Smith"**

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

**Example: Contacts with First Name "John" AND Last Name "Smith"**

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

## Filter Evaluation Steps

1. **Record Selection:** Relevant records are selected based on the filter criteria.
2. **Pruning (Optional):** `pruningRefineBy` refines the data to a specific time range.
3. **Filtering:** Filtering rules are applied to determine if records `PASS` or `FAIL`.
4. **Coalescing (Optional):** `coalescingRefineBy` further refines the data based on the number of occurrences.
5. **Result:** Records that `PASS` all filters are members of the list.

## Filter Branch Types

* **OR:** Accepts a record if it passes *any* of its nested `AND` branches.  Must have at least one nested `AND` branch and no direct filters.

* **AND:** Accepts a record if it passes *all* of its filters and nested branches. Can have zero or more filters and nested `UNIFIED_EVENTS` or `ASSOCIATION` branches.

* **UNIFIED_EVENTS:** Filters based on completed or uncompleted unified events.  Must be nested within an `AND` branch and contain one or more `PROPERTY` type filters.

* **ASSOCIATION:** Filters based on associated records.  Must be nested within an `AND` branch and have one or more filters.  Additional nested `ASSOCIATION` branches are only permitted for `CONTACT` to `LINE_ITEM` associations.

## Filter Types

The `filterType` parameter specifies the type of filter condition (e.g., `PROPERTY`, `FORM_SUBMISSION`, `PAGE_VIEW`).  Refer to the HubSpot documentation for a complete list and details on each filter type.


## Property Filter Operations

When using `PROPERTY`, `INTEGRATION_EVENT`, or `SURVEY_MONKEY_VALUE` filter types, the `operation` object defines the filter's specifics:

* `operationType`: Type of operator (e.g., `NUMBER`, `STRING`, `MULTISTRING`, `TIME_POINT`, `TIME_RANGED`).
* `operator`: Specific operator (e.g., `IS_EQUAL_TO`, `IS_GREATER_THAN`, `CONTAINS`).
* `value` / `values`: Value(s) to filter by.
* `includeObjectsWithNoValueSet`: Whether to include records with no value for the property (true/false).

See the detailed tables in the original text for specific `operationType` and supported operators for each property type.

## Time-Based Filters (`TIME_POINT`, `TIME_RANGED`)

The `TIME_POINT` and `TIME_RANGED` operations allow for various time-based comparisons, including:

* Specific dates
* Relative to today (e.g., "in last X days")
* Comparisons between properties or their last updated times.

Refer to the examples in the original text for detailed JSON structures for these filters.

## Refine By Operations

* `pruningRefineBy`: Refines the dataset to a specific timeframe (absolute or relative).
* `coalescingRefineBy`: Determines if a record passed the filter a minimum/maximum number of times.

Only one refine-by operation is allowed per filter.


## Legacy v1 List Filters

The v1 API (deprecated) is similar but has differences in syntax and available options.  The transition guide should be consulted for migrating from v1 to v3.


This markdown documentation provides a concise overview of HubSpot's List API v3 filter functionality.  Always refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications.
