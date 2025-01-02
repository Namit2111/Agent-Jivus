# HubSpot Lists API v3 Filter Documentation

This document details the structure and usage of filters in the HubSpot Lists API v3.  It's designed for developers creating and managing lists using the API.  The legacy v1 API is also briefly covered, but its use is discouraged as it's slated for sunsetting.

## Overview

List filters define the criteria for including records in a HubSpot list.  They use conditional logic built from filter branches with `AND` or `OR` operations, and individual filters of various types.  Records are members of a list if they pass *all* filters within the list's definition.

**Key Concepts:**

* **`filterBranchType`:**  Defines the logical operation (`OR` or `AND`) within a filter branch.
* **`filterType`:**  Specifies the type of filter (e.g., `PROPERTY`, `UNIFIED_EVENTS`, `ASSOCIATION`).
* **`filters`:** An array of individual filter objects within a branch.
* **`filterBranches`:** An array of nested filter branches within a branch.
* **`PASS` / `FAIL` logic:**  A record must pass all filters to be included in the list.


## Filter Structure

All filter definitions must start with a root-level `OR` `filterBranchType`. This root `OR` branch must contain one or more nested `AND` sub-filter branches.

**Basic JSON Structure:**

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
        "filters": [ /* More filters for another AND branch */ ]
      }
    ],
    "filterBranchType": "OR",
    "filters": []
  }
}
```

**Example: First Name "John" OR Last Name NOT "Smith"**

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

**Example: First Name "John" AND Last Name "Smith"**

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

* **`OR`:** Accepts a record if it passes *any* of its nested `AND` branches.  Must have at least one nested `AND` branch. Cannot have any direct filters.

* **`AND`:** Accepts a record only if it passes *all* of its filters and all its nested branches. Can have zero or more filters and nested `UNIFIED_EVENTS` or `ASSOCIATION` branches.

* **`UNIFIED_EVENTS`:** Filters based on events.  Can only be nested within an `AND` branch. Must have at least one property filter.  Cannot have nested branches.

* **`ASSOCIATION`:** Filters based on associated objects. Can only be nested within an `AND` branch. Must have at least one filter.  Can have nested branches only for `CONTACT` to `LINE_ITEM` associations.


## Filter Types

The `filterType` parameter determines the type of filter.  Some common types are:

* `PROPERTY`: Filters based on property values.
* `UNIFIED_EVENTS`: Filters on events (requires `eventTypeId` and `operator`).
* `ASSOCIATION`: Filters on associated records (requires `objectTypeId`, `operator`, `associationTypeId`, `associationCategory`).
* `FORM_SUBMISSION`, `EMAIL_EVENT`, `PAGE_VIEW`, etc.:  Filters based on specific HubSpot events and interactions.


## Property Filter Operations

Property filters use an `operation` object with:

* **`operationType`:** The type of operation (e.g., `NUMBER`, `STRING`, `MULTISTRING`, `TIME_POINT`, `TIME_RANGED`).
* **`operator`:** The specific operator (e.g., `IS_EQUAL_TO`, `CONTAINS`, `IS_BETWEEN`).
* **`value` / `values`:** The value(s) to compare against.
* **`includeObjectsWithNoValueSet`:** (Boolean)  Whether to include records without a value for the property.


## Time-Based Filters (`TIME_POINT` and `TIME_RANGED`)

These filter types allow filtering based on timestamps, either absolute dates or relative to the current date.  Examples are provided in the original text for:

* `Is equal to date`
* `In Last X Number of Days`
* `In Next X Number of Days`
* `Updated or Not Updated in the Last X Days`
* `Is After Date`
* `Is Relative to Today`
* `Is Before or After another property (value or last updated)`

These examples showcase the various parameters (`timeType`, `timezoneSource`, `zoneId`, `indexReference`, `offset`, `propertyParser`, etc.) used for specifying time ranges and comparisons.

## Refine By Operations

* **`pruningRefineBy`:** Refines the dataset to a specific time range (absolute or relative).
* **`coalescingRefineBy`:** Determines if a record passed the filter a minimum/maximum number of times.  Only `NUM_OCCURRENCES` is supported.


## Legacy v1 Lists API

The v1 API is deprecated.  Its filtering is similar but less flexible than v3. Only the `PROPERTY` `filterType` is supported.

## Conclusion

This documentation provides a comprehensive overview of HubSpot Lists API v3 filtering.  By understanding the nested structure, logical operators, filter types, and available operations, developers can effectively use the API to create powerful and sophisticated list definitions. Remember to consult the official HubSpot API documentation for the most up-to-date information and detailed specifications.
