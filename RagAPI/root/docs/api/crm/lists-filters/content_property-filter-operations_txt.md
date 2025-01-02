# HubSpot Lists API v3 Filter Documentation

This document details the structure and usage of filters within HubSpot's Lists API v3.  These filters determine which records are included in a list, based on conditional logic.  The API uses a JSON-based structure for defining filters.

## Overview

When creating a HubSpot list with `SNAPSHOT` or `DYNAMIC` processing type, filters define list membership. Filters employ conditional logic structured using filter branches with `AND` or `OR` operation types (`filterBranchType` parameter).  Within each branch are individual filters (`filterType` parameter) assessing records for inclusion.  Nested filter branches are also possible.  HubSpot uses PASS/FAIL logic; a record must pass all filters to be included.

## Filter Evaluation Steps

1. **Record Selection:** Relevant records are selected or fetched based on the filter.  For example, a `property` filter retrieves all records' property values.
2. **Pruning Refinement (Optional):**  The `pruningRefineBy` parameter refines the data to a specific time range.
3. **Filtering:** Filtering rules are applied to the (potentially refined) data, determining PASS or FAIL.
4. **Coalescing Refinement (Optional):** The `coalescingRefineBy` parameter further refines data based on the number of occurrences (e.g., "contact has filled out a form at least 2 times").
5. **Final Determination:**  If `coalescingRefineBy` is present, records passing the occurrence criteria are accepted. Otherwise, records are accepted or rejected based on step 3.

## Filter Branches

A filter branch is a data structure defining the conditional logic.  It consists of a type (`OR` or `AND`), an operator, filters, and sub-branches.

* **`OR` Filter Branch:** Accepts a record if it passes *any* of its filters or sub-branches.  It *must* have one or more nested `AND` branches and *cannot* have any direct filters.

  ```json
  {
    "filterBranchType": "OR",
    "filterBranches": [ /* One or more nested AND filter branches */ ],
    "filters": [] /* Zero filters */
  }
  ```

* **`AND` Filter Branch:** Accepts a record only if it passes *all* of its filters and sub-branches.  It can have zero or more filters and zero or more nested `UNIFIED_EVENTS` and/or `ASSOCIATION` branches.

  ```json
  {
    "filterBranchType": "AND",
    "filterBranches": [ /* Zero or more nested UNIFIED_EVENTS or ASSOCIATION filter branches */ ],
    "filters": [ /* Zero or more filters */ ]
  }
  ```

* **`UNIFIED_EVENTS` Filter Branch:**  Used to filter based on events.  Can only be nested within an `AND` branch. Must have one or more `PROPERTY` filters, and cannot have other filter branches.

  ```json
  {
    "filterBranchType": "UNIFIED_EVENTS",
    "filterBranches": [],
    "filters": [ /* One or more PROPERTY filters */ ],
    "eventTypeId": "0-1",
    "operator": "HAS_COMPLETED"
  }
  ```

* **`ASSOCIATION` Filter Branch:** Filters on records associated with the primary record.  Can only be nested within an `AND` branch.  Must have one or more filters and cannot have additional nested branches (except for `CONTACT` to `LINE_ITEM` associations).

  ```json
  {
    "filterBranchType": "ASSOCIATION",
    "filterBranches": [],
    "filters": [ /* Zero or more filters */ ],
    "objectTypeId": "0-1",
    "operator": "IN_LIST",
    "associationTypeId": 280,
    "associationCategory": "HUBSPOT_DEFINED"
  }
  ```

## Filter Structure

All filter definitions must start with a root-level `OR` branch, containing one or more nested `AND` branches.


## Filter Types

The `filterType` parameter specifies the type of filter.  Examples include: `PROPERTY`, `ADS_TIME`, `ADS_SEARCH`, `CTA`, `EMAIL_EVENT`, `EVENT`, `FORM_SUBMISSION`, `FORM_SUBMISSION_ON_PAGE`, `IN_LIST`, `PAGE_VIEW`, `PRIVACY`, `SURVEY_MONKEY`, `SURVEY_MONKEY_VALUE`, `WEBINAR`, `INTEGRATION_EVENT`.


## Property Filter Operations

The `PROPERTY`, `INTEGRATION_EVENT`, and `SURVEY_MONKEY_VALUE` filter types use an `operation` object:

* `operationType`:  The type of operator (e.g., `NUMBER`, `MULTISTRING`).
* `operator`: The specific operator (e.g., `IS_EQUAL_TO`, `CONTAINS`).
* `value`/`values`: The value(s) to filter by.
* `includeObjectsWithNoValueSet`:  Whether to include records with no value for the property (default: `false`).

Example:

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

See the detailed table in the original text for a complete list of `operationType` options and supported operators.


## Time-Based Filters (`TIME_POINT`, `TIME_RANGED`)

These filter types allow filtering based on timestamps.  Examples include "Is equal to date," "In Last X Number of Days," "In Next X Number of Days," "Updated or Not Updated in the Last X Days," "Is After Date," "Is Relative to Today," and "Is Before or After another property".  The original text provides detailed JSON examples for each case.


## Refine By Operations

* **`pruningRefineBy`:** Refines the dataset to a specific time range (absolute or relative).
* **`coalescingRefineBy`:**  Determines if a record passed the filter a minimum/maximum number of times.

Only one refine-by operation is allowed per filter.


## Legacy v1 Lists API

The v1 API is deprecated.  The original text provides details on its differences from v3 and instructions for migrating.  The main difference is that v1 only supports `PROPERTY` as `filterType`.


This markdown documentation summarizes the provided text, offering a structured and more easily navigable guide to HubSpot's Lists API v3 filtering capabilities.  Remember to consult the official HubSpot documentation for the most up-to-date information.
