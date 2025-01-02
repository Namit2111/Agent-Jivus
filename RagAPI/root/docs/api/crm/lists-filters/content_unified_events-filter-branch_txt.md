# HubSpot Lists API: Filter Documentation

This document details the HubSpot Lists API v3 filtering capabilities.  It explains how to construct filter definitions using JSON to create lists based on various criteria.  The legacy v1 API is also briefly addressed, but its use is discouraged due to its impending sunset.

## List Filter Overview

List filters define which records belong to a HubSpot list.  They utilize conditional logic expressed through *filter branches* with `AND` or `OR` operations (`filterBranchType` parameter) and individual *filters* (`filterType` parameter) within those branches.  Nested branches are allowed, creating complex filtering structures.  HubSpot uses a PASS/FAIL logic; a record must pass *all* filters to be included.


## Filter Evaluation Steps

1. **Record Selection:** Relevant records are selected or fetched based on the filter (e.g., all records for a `property` filter).
2. **Pruning Refinement (Optional):**  The `pruningRefineBy` parameter refines the data to a specific time range (see "Refine By Operation" section).
3. **Filter Application:** Filtering rules are applied to the refined data to determine PASS or FAIL.
4. **Coalescing Refinement (Optional):** The `coalescingRefineBy` parameter further refines the data based on the number of times a record satisfies the filter.
5. **Final PASS/FAIL:** If `coalescingRefineBy` is used, the record passes if it meets the specified occurrence count. Otherwise, it passes or fails based on step 3.


## Filter Branches

Filter branches structure the conditional logic.  They have a type (`filterBranchType`), an operator (`AND` or `OR`), a list of filters, and a list of sub-branches.

* **`OR` Branch:** Accepts a record if it passes *any* of its filters or sub-branches.  Must have at least one `AND` sub-branch and cannot have any direct filters.

* **`AND` Branch:** Accepts a record if it passes *all* of its filters and sub-branches.  Can have zero or more filters and zero or more nested `UNIFIED_EVENTS` and/or `ASSOCIATION` branches.

* **`UNIFIED_EVENTS` Branch:** Filters based on events.  Must be nested within an `AND` branch. Requires `eventTypeId` and `operator` (e.g., `HAS_COMPLETED`, `HAS_NOT_COMPLETED`).  Can only have `PROPERTY` type filters.

* **`ASSOCIATION` Branch:** Filters based on associated records.  Must be nested within an `AND` branch. Requires `objectTypeId`, `operator` (e.g., `IN_LIST`), `associationTypeId`, and `associationCategory`. Can only have `PROPERTY` type filters, with additional nested branches allowed only for `CONTACT` to `LINE_ITEM` associations.

**Structure:**  All filter definitions must begin with a root-level `OR` branch, containing one or more `AND` sub-branches.


## Filter Structure Example (JSON)

This example creates a list of contacts with the first name "John" OR those who do not have the last name "Smith":

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

## Filter Types

The `filterType` parameter specifies the type of filter.  Some key types include:

* `PROPERTY`: Filters based on a record's property values.  (See "Property Filter Operations")
* `UNIFIED_EVENTS`: Filters based on whether a contact has completed specific events.
* `ASSOCIATION`: Filters based on associated records.
* `FORM_SUBMISSION`: Filters based on form submissions.
* `EMAIL_EVENT`: Filters based on email events (opt-ins, etc.).
* `PAGE_VIEW`: Filters based on page views.
* and many more...


## Property Filter Operations

`PROPERTY`, `INTEGRATION_EVENT`, and `SURVEY_MONKEY_VALUE` filters use an `operation` object:

* `operationType`: The type of operation (e.g., `NUMBER`, `STRING`, `MULTISTRING`, `TIME_POINT`, `TIME_RANGED`).
* `operator`: The operator to apply (e.g., `IS_EQUAL_TO`, `CONTAINS`, `IS_BETWEEN`).
* `value` / `values`: The value(s) to filter by.
* `includeObjectsWithNoValueSet`:  Whether to include records with no value for the property (true/false).


## Time-Based Filter Examples

The following examples demonstrate the use of `TIME_POINT` and `TIME_RANGED` operations for property filters.  These utilize various ways to specify time ranges: absolute dates, relative to today/now, or compared against other properties.  (Note:  These are simplified; refer to the original document for complete JSON examples.)

* **Is equal to date:**  Filters records where a property's value matches a specific date.
* **In Last X Number of Days:**  Filters records where a property's value falls within the last X days.
* **In Next X Number of Days:** Filters records where a property's value falls within the next X days.
* **Updated or Not Updated in the Last X Days:** Filters based on when a property was last updated.
* **Is After Date:** Filters records where a property's value is after a specific date.
* **Is Relative to Today:** Filters records based on an offset from today's date.
* **Is Before or After another property:** Compares a property's value to another property's value or last update timestamp.


## Refine By Operations

* **`pruningRefineBy`:** Refines the dataset to a specific time range (absolute or relative).
* **`coalescingRefineBy`:** Determines if the record passed the filter criteria a minimum and/or maximum number of times.


## Legacy v1 List Filters

The v1 API (deprecated) offers similar filtering capabilities but with a slightly different syntax and fewer options. The only supported `filterType` is `PROPERTY`.  **Migration to v3 is strongly recommended.**


## Conclusion

HubSpot's Lists API v3 provides powerful filtering capabilities through a structured JSON format.  Understanding filter branches, filter types, and available operators is crucial for building effective and complex list definitions.  Remember to always start with an `OR` branch and use appropriate nesting for `AND` branches, `UNIFIED_EVENTS`, and `ASSOCIATION` branches as needed.  The original document provides a detailed reference for all available filter types, operators, and parameter values.
