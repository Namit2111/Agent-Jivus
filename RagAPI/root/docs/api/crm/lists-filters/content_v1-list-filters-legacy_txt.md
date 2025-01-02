# HubSpot Lists API: Filter Documentation

This document details the structure and usage of filters within the HubSpot Lists API (v3).  It explains how to create lists based on complex conditional logic using filter branches and individual filter types.  The legacy v1 API is also briefly covered.

## Overview

List filters allow you to define the criteria for including records in a HubSpot list.  Filters use conditional logic structured in filter branches with `AND` or `OR` operations, nested to create complex rules.  HubSpot uses a `PASS`/`FAIL` system; records must pass all filters to be included.


## Filter Structure

All filter definitions must start with a root-level `OR` `filterBranchType`. This root `OR` branch contains one or more nested `AND` sub-branches. Each `AND` branch contains one or more filters defining specific criteria.

**Example JSON Structure:**

```json
{
  "filterBranch": {
    "filterBranches": [
      {
        "filterBranches": [],
        "filterBranchType": "AND",
        "filters": [ /* Filters for the first AND branch */ ]
      },
      {
        "filterBranches": [],
        "filterBranchType": "AND",
        "filters": [ /* Filters for the second AND branch */ ]
      }
    ],
    "filterBranchType": "OR",
    "filters": []
  }
}
```

This structure ensures proper rendering in the HubSpot UI.  An `OR` branch means a record passes if it satisfies *any* of its child `AND` branches. An `AND` branch requires a record to satisfy *all* its filters.


## Filter Branch Types

* **`OR` filter branch:** The root branch.  Must contain one or more nested `AND` branches and cannot have any individual filters.  A record passes if it meets the criteria of *at least one* nested `AND` branch.

  ```json
  {
    "filterBranchType": "OR",
    "filterBranches": [ /* One or more nested AND branches */ ],
    "filters": []
  }
  ```

* **`AND` filter branch:** Nested within `OR` branches.  Can contain zero or more filters and zero or more nested `UNIFIED_EVENTS` and/or `ASSOCIATION` branches. A record passes only if it meets the criteria of *all* filters and nested branches.

  ```json
  {
    "filterBranchType": "AND",
    "filterBranches": [ /* Zero or more nested branches */ ],
    "filters": [ /* Zero or more filters */ ]
  }
  ```

* **`UNIFIED_EVENTS` filter branch:**  Nested only within `AND` branches. Filters records based on their interaction with specific unified events. Must have at least one `PROPERTY` type filter and cannot have nested branches.

  ```json
  {
    "filterBranchType": "UNIFIED_EVENTS",
    "filterBranches": [],
    "filters": [ /* One or more PROPERTY filters */ ],
    "eventTypeId": "0-1", // Event ID
    "operator": "HAS_COMPLETED" // or HAS_NOT_COMPLETED
  }
  ```

* **`ASSOCIATION` filter branch:** Nested only within `AND` branches. Filters based on associated records. Must have one or more filters and cannot have nested branches.  Additional nested `filterBranches` are only allowed for `CONTACT` to `LINE_ITEM` associations.

  ```json
  {
    "filterBranchType": "ASSOCIATION",
    "filterBranches": [],
    "filters": [ /* One or more filters */ ],
    "objectTypeId": "0-1", // Object type ID
    "operator": "IN_LIST", // or other operators
    "associationTypeId": 280, // Association type ID
    "associationCategory": "HUBSPOT_DEFINED" // etc.
  }
  ```


## Filter Types

The `filterType` parameter defines the type of filter within a branch. Some examples include:

* `PROPERTY`: Filters based on a record's property values.  See "Property Filter Operations" below.
* `ADS_TIME`, `ADS_SEARCH`, `CTA`, `EMAIL_EVENT`, `EVENT`, `FORM_SUBMISSION`, `FORM_SUBMISSION_ON_PAGE`, `IN_LIST`, `PAGE_VIEW`, `PRIVACY`, `SURVEY_MONKEY`, `SURVEY_MONKEY_VALUE`, `WEBINAR`, `INTEGRATION_EVENT` :  These filter types each have specific parameters to define the filtering criteria.  Refer to the HubSpot documentation for details on each type.


## Property Filter Operations

`PROPERTY` filters use the `operation` object to define criteria:

* `operationType`:  The type of operator (e.g., `NUMBER`, `STRING`, `MULTISTRING`, `TIME_POINT`, `TIME_RANGED`).
* `operator`: The specific operator (e.g., `IS_EQUAL_TO`, `CONTAINS`, `IS_BEFORE`, `IS_BETWEEN`).
* `value`/`values`: The value(s) to compare against.
* `includeObjectsWithNoValueSet`:  (boolean) Whether to include records without a value for the specified property.


**Examples:**

* **String:** `firstname` equals "John"

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

* **Number:** `amount` is greater than 100

  ```json
  {
    "filterType": "PROPERTY",
    "property": "amount",
    "operation": {
      "operationType": "NUMBER",
      "operator": "IS_GREATER_THAN",
      "value": 100
    }
  }
  ```

* **Date:**  `last_updated` is within the last 7 days (using `TIME_RANGED`)

  ```json
  {
    "filterType": "PROPERTY",
    "property": "last_updated",
    "operation": {
      "operationType": "TIME_RANGED",
      "operator": "IS_BETWEEN",
      "lowerBoundTimePoint": {/* ... */}, // See Date Examples below
      "upperBoundTimePoint": {/* ... */} // See Date Examples below
    }
  }
  ```


## Time-Based Filter Examples

The following examples demonstrate various date and time filter options using `TIME_POINT` and `TIME_RANGED`:

* **Is equal to date:** (Requires `TIME_RANGED`)

  ```json
  // ... (Full filter object structure as in the original document, this is a snippet)
  "lowerBoundTimePoint": {
    "timeType": "DATE",
    "timezoneSource": "CUSTOM",
    "zoneId": "America/New_York",
    "year": 2024,
    "month": 3,
    "day": 11,
    "hour": 0,
    "minute": 0,
    "second": 0,
    "millisecond": 0
  },
  "upperBoundTimePoint": {
    "timeType": "DATE",
    "timezoneSource": "CUSTOM",
    "zoneId": "US/Eastern",
    "year": 2024,
    "month": 3,
    "day": 11,
    "hour": 23,
    "minute": 59,
    "second": 59,
    "millisecond": 999
  },
  // ...
  ```

* **In Last X Number of Days:** (Uses `TIME_RANGED` and `INDEXED` timeType)

  ```json
  // ... (Full filter object structure)
  "lowerBoundTimePoint": {
    "timeType": "INDEXED",
    "timezoneSource": "CUSTOM",
    "zoneId": "US/Eastern",
    "indexReference": { "referenceType": "TODAY" },
    "offset": { "days": -3 }
  },
  // ...
  ```

* **In Next X Number of Days:** (Uses `TIME_RANGED` and `INDEXED` timeType)

  ```json
  // ... (Full filter object structure)
  "upperBoundTimePoint": {
    "timeType": "INDEXED",
    "timezoneSource": "CUSTOM",
    "zoneId": "US/Eastern",
    "indexReference": { "referenceType": "TODAY" },
    "offset": { "days": 5 }
  },
  // ...
  ```

* **Updated or Not Updated in the Last X Days:** (Uses `TIME_RANGED` and `INDEXED` timeType, `propertyParser: "UPDATED_AT"`)

  ```json
   // ... (Full filter object structure)
   "propertyParser": "UPDATED_AT",
   "lowerBoundTimePoint": {
    "timeType": "INDEXED",
    "timezoneSource": "CUSTOM",
    "zoneId": "America/New_York",
    "indexReference": { "referenceType": "TODAY" },
    "offset": { "days": -7 }
  },
  // ...
  ```

* **Is After Date:** (Uses `TIME_POINT` and `DATE` timeType)

  ```json
  // ... (Full filter object structure)
  "timePoint": {
    "timeType": "DATE",
    "timezoneSource": "CUSTOM",
    "zoneId": "America/New_York",
    "year": 2024,
    "month": 3,
    "day": 4,
    "hour": 23,
    "minute": 59,
    "second": 59,
    "millisecond": 999
  },
  // ...
  ```

* **Is Relative to Today:** (Uses `TIME_POINT` and `INDEXED` timeType)

  ```json
  // ... (Full filter object structure)
  "timePoint": {
    "timeType": "INDEXED",
    "timezoneSource": "CUSTOM",
    "zoneId": "America/New_York",
    "indexReference": { "referenceType": "TODAY" },
    "offset": { "days": 2 }
  },
  // ...
  ```

* **Is Before or After another property (value or last updated):** (Uses `TIME_POINT` and `PROPERTY_REFERENCED` timeType)

   ```json
  // ... (Full filter object structure)
  "timePoint": {
    "timeType": "PROPERTY_REFERENCED",
    "timezoneSource": "CUSTOM",
    "zoneId": "US/Eastern",
    "property": "hs_latest_open_lead_date",
    "referenceType": "VALUE" // or UPDATED_AT
  },
  // ...
  ```


## Refine By Operations

Refine by operations further refine the dataset *after* initial filtering:

* **`pruningRefineBy`:** Limits the dataset to a specific time range (absolute or relative).
* **`coalescingRefineBy`:** Filters based on the number of times a record meets the filter criteria (number of occurrences).

Only one refine by operation is allowed per filter.


## Legacy v1 Lists API

The v1 API is deprecated.  The core functionality is similar, but with differences in syntax and available options.  The only supported `filterType` is `PROPERTY`.


## Conclusion

This documentation provides a comprehensive overview of HubSpot Lists API v3 filters.  For detailed information on specific filter types, operators, and error handling, refer to the official HubSpot API documentation.  Remember that the v1 API is deprecated and should be migrated to v3.
