# HubSpot Lists API v3: Filter Documentation

This document details the filter structure and options available for creating dynamic and snapshot lists in the HubSpot Lists API v3.  The legacy v1 API is deprecated and should be migrated to v3.

## Overview

List filters use conditional logic to determine which records belong to a list.  The core structure consists of nested filter branches (`filterBranchType`: `OR` and `AND`) containing individual filters (`filterType`).  HubSpot uses PASS/FAIL logic; a record must pass all filters to be included.

## API Call Structure

List filters are defined within a JSON payload sent to the HubSpot API (typically via a POST request to create or update a list).  The primary structure is a `filterBranch` object:

```json
{
  "filterBranch": {
    "filterBranchType": "OR",  // Root branch MUST be OR
    "filters": [],              // Filters at this level (optional, root OR branch cannot have filters)
    "filterBranches": [         // Nested AND branches
      {
        "filterBranchType": "AND",
        "filters": [
          // Individual filters
        ],
        "filterBranches": [
          // Further nested branches (e.g., UNIFIED_EVENTS, ASSOCIATION)
        ]
      },
      // ... more AND branches ...
    ]
  }
}
```


## Filter Branch Types

* **`OR`**: The root-level filter branch.  A record passes if it passes *any* of its nested `AND` branches.  It cannot contain individual filters.

```json
{
  "filterBranchType": "OR",
  "filterBranches": [ /* One or more AND branches */ ],
  "filters": []
}
```

* **`AND`**: Nested within `OR` branches. A record passes if it passes *all* of its filters and nested branches.

```json
{
  "filterBranchType": "AND",
  "filters": [ /* Zero or more filters */ ],
  "filterBranches": [ /* Zero or more UNIFIED_EVENTS or ASSOCIATION branches */ ]
}
```

* **`UNIFIED_EVENTS`**: Used to filter based on events.  Only allowed as a nested branch within an `AND` branch. Requires at least one filter.

```json
{
  "filterBranchType": "UNIFIED_EVENTS",
  "filterBranches": [],
  "filters": [ /* One or more PROPERTY filters */ ],
  "eventTypeId": "0-1",  // Event type ID
  "operator": "HAS_COMPLETED" // or HAS_NOT_COMPLETED
}
```

* **`ASSOCIATION`**: Used to filter based on associated records. Only allowed as a nested branch within an `AND` branch. Requires at least one filter.

```json
{
  "filterBranchType": "ASSOCIATION",
  "filterBranches": [],
  "filters": [ /* Zero or more filters */ ],
  "objectTypeId": "0-1",      // Associated object type ID
  "operator": "IN_LIST",       // or other operators
  "associationTypeId": 280,    // Association type ID
  "associationCategory": "HUBSPOT_DEFINED" // or other categories
}
```


## Filter Types

The `filterType` parameter specifies the type of filter condition.  Examples include:

* `PROPERTY`: Filters based on contact properties (see "Property Filter Operations" below).
* `ADS_TIME`, `ADS_SEARCH`, `CTA`, `EMAIL_EVENT`, `EVENT`, `FORM_SUBMISSION`, `FORM_SUBMISSION_ON_PAGE`, `IN_LIST`, `PAGE_VIEW`, `PRIVACY`, `SURVEY_MONKEY`, `SURVEY_MONKEY_VALUE`, `WEBINAR`, `INTEGRATION_EVENT` : Filter based on various HubSpot interactions and events.

## Property Filter Operations

`PROPERTY` filters require an `operation` object defining the filter parameters:

* `operationType`:  The type of operator (e.g., `NUMBER`, `MULTISTRING`).
* `operator`: The specific operator (e.g., `IS_EQUAL_TO`, `IS_BETWEEN`).
* `value` / `values`: The value(s) to compare against.
* `includeObjectsWithNoValueSet`: (Boolean) Whether to include records without a value for the property. Defaults to `false`.


**Example: First Name equals "John"**

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

## Time-Based Filters (`TIME_POINT` and `TIME_RANGED`)

These operation types provide flexible time-based filtering:

* **`TIME_POINT`**: Compares a property's timestamp to a single point in time.
* **`TIME_RANGED`**: Compares a property's timestamp to a time range.

**Examples:**

* **Is equal to date:**
    ```json
    // ... (within a filter's operation) ...
    "operationType": "TIME_RANGED",
    "lowerBoundTimePoint": { "timeType": "DATE", "year": 2024, "month": 3, "day": 11, ... },
    "upperBoundTimePoint": { "timeType": "DATE", "year": 2024, "month": 3, "day": 11, ... },
    // ...
    ```

* **In Last X Number of Days:**
    ```json
    // ... (within a filter's operation) ...
    "operationType": "TIME_RANGED",
    "lowerBoundTimePoint": { "timeType": "INDEXED", "indexReference": { "referenceType": "TODAY" }, "offset": { "days": -3 } },
    // ...
    ```

* **Is Relative to Today:**
    ```json
    // ... (within a filter's operation) ...
    "operationType": "TIME_POINT",
    "timePoint": { "timeType": "INDEXED", "indexReference": { "referenceType": "TODAY" }, "offset": { "days": 2 } },
    // ...
    ```



## Refine By Operations

* **`pruningRefineBy`**: Refines the dataset to a specific time range before filter evaluation (absolute or relative).
* **`coalescingRefineBy`**:  Determines if a record passes the filter a minimum/maximum number of times.  Only `NUM_OCCURRENCES` is supported.

## Legacy v1 API (Deprecated)

The v1 API is deprecated.  While similar to v3, it has fewer features and a slightly different structure.  Migrate to v3 as soon as possible.


This documentation provides a comprehensive overview of HubSpot's Lists API v3 filtering capabilities.  Refer to the official HubSpot API documentation for the most up-to-date information and complete details on all available filter types and operators.
