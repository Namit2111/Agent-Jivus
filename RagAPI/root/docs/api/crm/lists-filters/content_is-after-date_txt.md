# HubSpot Lists API: Filter Documentation

This document details the filter structure and options available when creating lists in the HubSpot CRM using the Lists API (v3).  The legacy v1 API is deprecated.

## List Filter Overview

When creating a HubSpot list with `SNAPSHOT` or `DYNAMIC` processing type, filters define which records are included.  Filters utilize conditional logic via filter branches with `AND` or `OR` operations (`filterBranchType` parameter).  Each branch contains individual filters (`filterType` parameter) evaluating records for inclusion.  Nested branches are supported.

HubSpot employs PASS/FAIL logic.  A record is a list member only if it passes all filters.

### Filter Evaluation Steps:

1. **Record Selection:** Relevant records are selected based on the filter (e.g., all records for a property filter).
2. **Pruning Refinement (optional):**  `pruningRefineBy` parameter refines data to a specific time range (see "Refine By Operation" section).
3. **Filter Application:** Filtering rules are applied to determine PASS or FAIL.
4. **Coalescing Refinement (optional):** `coalescingRefineBy` further refines data based on the number of occurrences (e.g., "contact has filled out a form at least 2 times").  If present, records PASS if they meet the occurrence criteria; otherwise, PASS/FAIL is determined by step 3.


## Filter Branch Structure

Filter branches define conditional logic.  They comprise:

* **`filterBranchType`:**  (`OR`, `AND`, `UNIFIED_EVENTS`, `ASSOCIATION`)
* **`filterBranchOperator`:** (`AND` or `OR`)
* **`filters`:** An array of individual filters.
* **`filterBranches`:** An array of nested filter branches.

**Structure Requirements:**

* All filter definitions must begin with a root-level `OR` filter branch.
* This root `OR` branch must contain one or more `AND` sub-branches.

**Example JSON (OR with nested AND):**

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
        "filterBranchType": "AND",
        "filters": [ /* filters here */ ],
        "filterBranches": []
      }
    ],
    "filterBranchType": "OR",
    "filters": []
  }
}
```

This structure ensures correct rendering in the HubSpot UI.

**Example:  First name "John" OR last name NOT "Smith"**

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

**Example: First name "John" AND last name "Smith"**

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

* **`OR`:** Requires one or more nested `AND` branches.  No filters are allowed directly within an `OR` branch. A record is accepted if it passes any nested `AND` branch.

* **`AND`:** Can have zero or more filters and zero or more nested `UNIFIED_EVENTS` and/or `ASSOCIATION` branches.  A record is accepted only if it passes all filters and all nested branches.

* **`UNIFIED_EVENTS`:**  Only nested within `AND` branches. Filters on events.  Requires at least one `PROPERTY` filter. No nested branches allowed.

* **`ASSOCIATION`:** Only nested within `AND` branches. Filters on associated records. Requires at least one filter.  Only allows nested `ASSOCIATION` branches for `CONTACT` to `LINE_ITEM` associations.


## Filter Types

The `filterType` parameter defines the type of filter. Examples include: `PROPERTY`, `ADS_TIME`, `ADS_SEARCH`, `CTA`, `EMAIL_EVENT`, `EVENT`, `FORM_SUBMISSION`, `FORM_SUBMISSION_ON_PAGE`, `IN_LIST`, `PAGE_VIEW`, `PRIVACY`, `SURVEY_MONKEY`, `SURVEY_MONKEY_VALUE`, `WEBINAR`, `INTEGRATION_EVENT`.  See the HubSpot documentation for detailed descriptions of each.


## Property Filter Operations

The `operation` object within a `PROPERTY`, `INTEGRATION_EVENT`, or `SURVEY_MONKEY_VALUE` filter defines the operation details:

* **`operationType`:** (`ALL_PROPERTY`, `BOOL`, `ENUMERATION`, `MULTISTRING`, `NUMBER`, `STRING`, `TIME_POINT`, `TIME_RANGED`)  Specifies the operator type.
* **`operator`:** The specific operator (e.g., `IS_EQUAL_TO`, `IS_NOT_EQUAL_TO`, `CONTAINS`, etc.).  Operators vary based on `operationType` and property type.
* **`value` / `values`:** The value(s) to filter by.
* **`includeObjectsWithNoValueSet`:** (boolean)  Determines if records without a value for the property are accepted (`true`) or rejected (`false`, default).

## Time-Based Filters (`TIME_POINT` and `TIME_RANGED`)

These filter types allow filtering based on timestamps, either absolute dates or relative to the current time. See the provided examples in the original text for detailed JSON structures.

**Examples:**

* **`Is equal to date`:** Filters records where a property's value matches a specific date.
* **`In Last X Number of Days`:** Filters records updated within the last X days.
* **`In Next X Number of Days`:** Filters records to be updated within the next X days.
* **`Updated or Not Updated in the Last X Days`:** Filters records based on whether they were updated within the last X days.
* **`Is After Date`:** Filters records where a property's value is after a specified date.
* **`Is Relative to Today`:** Filters based on an offset from today's date.
* **`Is Before or After another property (value or last updated)`:** Compares a property's value or last updated time to another property.

## Refine By Operations

* **`pruningRefineBy`:** Refines the dataset to a time range (absolute or relative).
* **`coalescingRefineBy`:** Determines if a record passes the filter a minimum number of times.  Only one refine-by operation is allowed per filter.

### Pruning Refine By Types:

* **`ABSOLUTE_COMPARATIVE`:** Compares a timestamp to a specific timestamp (BEFORE or AFTER).
* **`ABSOLUTE_RANGED`:** Checks if a timestamp is within (BETWEEN) or outside (NOT_BETWEEN) a range.
* **`RELATIVE_COMPARATIVE`:** Compares a timestamp to an offset (PAST or FUTURE) from the current time (BEFORE or AFTER).
* **`RELATIVE_RANGED`:** Checks if a timestamp falls within a range defined by time offsets.

### Coalescing Refine By Types:

* **`NUM_OCCURRENCES`:** Specifies a minimum and/or maximum number of times a record must pass the filter.


## Legacy v1 List Filters (Deprecated)

The v1 API is deprecated; use v3.  The v1 API only supports `PROPERTY` filters with a slightly different structure.

## All Property Types Operations

Filters for whether a property value is known or unknown using `IS_KNOWN` and `IS_NOT_KNOWN`.

## Specific Property Type Operations (v1)

The v1 API offers different operators depending on the property type (`propertyType` parameter):

* **`string`:** (`IS_EQUAL_TO`, `IS_NOT_EQUAL_TO`, `CONTAINS`, `DOES_NOT_CONTAIN`, `STARTS_WITH`, `ENDS_WITH`, `HAS_EVER_BEEN_EQUAL_TO`, `HAS_NEVER_BEEN_EQUAL_TO`, `HAS_EVER_CONTAINED`, `HAS_NEVER_CONTAINED`)
* **`multistring`:** (`IS_EQUAL_TO`, `IS_NOT_EQUAL_TO`, `CONTAINS`, `DOES_NOT_CONTAIN`, `STARTS_WITH`, `ENDS_WITH`)
* **`number`:** (`IS_EQUAL_TO`, `IS_NOT_EQUAL_TO`, `IS_BETWEEN`, `IS_NOT_BETWEEN`, `HAS_EVER_BEEN_EQUAL_TO`, `HAS_NEVER_BEEN_EQUAL_TO`)
* **`bool`:** (`IS_EQUAL_TO`, `IS_NOT_EQUAL_TO`, `HAS_EVER_BEEN_EQUAL_TO`, `HAS_NEVER_BEEN_EQUAL_TO`)
* **`enumeration`:** (`IS_EQUAL_TO`, `IS_NOT_EQUAL_TO`, `HAS_EVER_BEEN_ANY_OF`, `HAS_NEVER_BEEN_ANY_OF`)
* **`datetime`:** (`IS_EQUAL_TO`, `IS_BEFORE_DATE`, `IS_AFTER_DATE`)
* **`datetime-comparative`:** (`IS_BEFORE`, `IS_AFTER`)
* **`datetime-ranged`:** (`IS_BETWEEN`, `IS_NOT_BETWEEN`)
* **`datetime-rolling`:** (`IS_LESS_THAN_X_DAYS_AGO`, `IS_MORE_THAN_X_DAYS_AGO`, `IS_LESS_THAN_X_DAYS_FROM_NOW`, `IS_MORE_THAN_X_DAYS_FROM_NOW`)
* **`rolling-property-updated`:** (`UPDATED_IN_LAST_X_DAYS`, `NOT_UPDATED_IN_LAST_X_DAYS`)


Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
