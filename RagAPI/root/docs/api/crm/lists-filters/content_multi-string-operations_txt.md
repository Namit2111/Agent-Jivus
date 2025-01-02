# HubSpot Lists API: Filter Documentation

This document details the structure and usage of filters within the HubSpot Lists API (v3).  The legacy v1 API is deprecated and should not be used for new integrations.

## Overview

List filters define the criteria for including records in a HubSpot list.  They utilize conditional logic based on filter branches (`filterBranchType`) with `AND` or `OR` operations.  These branches contain individual filters (`filterType`) that evaluate record properties.

**Key Concepts:**

* **`filterBranchType`:**  Defines the logical operation (`OR` or `AND`) between nested branches and filters.
* **`filterType`:** Specifies the type of filter (e.g., `PROPERTY`, `UNIFIED_EVENTS`, `ASSOCIATION`).
* **`operation`:** (Used with `PROPERTY` and other filter types)  Defines the operator and values for comparing property values.
* **`PASS`/`FAIL` Logic:** A record is included in the list only if it passes *all* filters and branches.


## Filter Structure

All filter definitions must begin with a root-level `OR` `filterBranchType`. This root `OR` branch must contain one or more nested `AND` sub-branches.  This structure ensures proper rendering in the HubSpot UI.

**Example JSON (OR branch with two AND sub-branches):**

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

This example creates a list of contacts where the `firstname` is "John" **OR** the `lastname` is not "Smith".


**Example JSON (OR branch with one AND sub-branch):**

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

This example creates a list of contacts where the `firstname` is "John" **AND** the `lastname` is "Smith".


## Filter Branch Types

* **`OR`:** Accepts a record if *any* of its nested `AND` branches pass.  Must have at least one nested `AND` branch. Cannot have any direct filters.

* **`AND`:** Accepts a record only if *all* of its filters and nested branches pass. Can have zero or more filters and nested branches (including `UNIFIED_EVENTS` and `ASSOCIATION`).

* **`UNIFIED_EVENTS`:**  Filters based on completed or uncompleted unified events.  Can only be nested within an `AND` branch.  Requires `eventTypeId` and `operator` (e.g., `HAS_COMPLETED`, `HAS_NOT_COMPLETED`).

* **`ASSOCIATION`:** Filters based on associations with other objects. Can only be nested within an `AND` branch. Requires `objectTypeId`, `operator` (e.g., `IN_LIST`), `associationTypeId`, and `associationCategory`.


## Filter Types

The `filterType` parameter specifies the kind of filter:

* **`PROPERTY`:**  Filters based on property values.  Uses the `operation` object to define the comparison.  See "Property Filter Operations" section.
* **`ADS_TIME`, `ADS_SEARCH`, `CTA`, `EMAIL_EVENT`, `EVENT`, `FORM_SUBMISSION`, `FORM_SUBMISSION_ON_PAGE`, `IN_LIST`, `PAGE_VIEW`, `PRIVACY`, `SURVEY_MONKEY`, `SURVEY_MONKEY_VALUE`, `WEBINAR`, `INTEGRATION_EVENT`:**  Specific filter types for various HubSpot interactions and events.  Refer to the HubSpot documentation for details on each filter type.


## Property Filter Operations

The `operation` object within a `PROPERTY` filter allows for various comparisons. Key parameters include:

* **`operationType`:**  Specifies the data type (e.g., `NUMBER`, `STRING`, `MULTISTRING`, `TIME_POINT`, `TIME_RANGED`).
* **`operator`:** The comparison operator (e.g., `IS_EQUAL_TO`, `IS_GREATER_THAN`, `CONTAINS`, `IS_BETWEEN`).
* **`value` / `values`:** The value(s) to compare against.
* **`includeObjectsWithNoValueSet`:**  (Boolean) Indicates whether to include records with no value set for the specified property (defaults to `false`).


## Time-Based Filters (`TIME_POINT` and `TIME_RANGED`)

These filter types are particularly useful for date-based criteria.  They utilize various `timeType` options like `DATE`, `INDEXED` (relative to today or now), and `PROPERTY_REFERENCED` (comparison to another property's value).

**Examples:**

* **`IS_EQUAL_TO` date:**  Compares a property's date to a specific date.
* **`In Last X Number of Days`:** Compares a property's date to a range within the last *x* days.
* **`In Next X Number of Days`:** Compares a property's date to a range within the next *x* days.
* **`Updated or Not Updated in the Last X Days`:** Checks whether a property was updated (or not) within the last *x* days.
* **`Is After Date`:** Compares a property's date to whether it is after a specified date.
* **`Is Relative to Today`:** Compares a property's date relative to today's date (using positive or negative offsets).
* **`Is Before or After another property`:** Compares a property's date to the value or last updated date of another property.


## Refine By Operations

Refine by operations further refine the dataset before filter evaluation:

* **`pruningRefineBy`:** Limits the dataset to a specific time range (absolute or relative).
* **`coalescingRefineBy`:**  Specifies a minimum and/or maximum number of occurrences for a record to pass the filter. Only one refine by operation is allowed per filter.


##  Legacy v1 Lists API (Deprecated)

The v1 API is significantly less flexible than v3 and is scheduled for sunsetting. It only supports `PROPERTY` filters with a limited set of operators for each property type.  Migrate to v3 as soon as possible.


## API Call Example (POST)

A `POST` request would be used to create or update a list's filter definition.  The body would contain the JSON structure as shown in the examples above.  The specific endpoint would depend on the HubSpot API version and authentication method.  Refer to the HubSpot API documentation for details.


This documentation provides a comprehensive overview of HubSpot List filters.  For detailed information on specific filter types, operators, and API endpoints, consult the official HubSpot API documentation.
