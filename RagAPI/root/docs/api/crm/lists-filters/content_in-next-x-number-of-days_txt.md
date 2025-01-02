# HubSpot Lists API v3: Filter Documentation

This document details the structure and usage of filters within the HubSpot Lists API v3.  It outlines the process of creating lists based on specific criteria, including examples and JSON structures.  The legacy v1 API is also briefly addressed.

## Overview

HubSpot Lists allow you to segment your contacts and other objects based on various criteria.  When creating a list with `SNAPSHOT` or `DYNAMIC` processing type, filters define which records belong to the list.  Filters use conditional logic defined by filter branches with `AND` or `OR` operations (`filterBranchType` parameter).  Each branch contains individual filters (`filterType` parameter) assessing records for inclusion.  Nested branches are also supported.

HubSpot uses PASS/FAIL logic: a record must pass all filters to be included.

## Filter Evaluation Steps

1. **Record Selection:** Relevant records are selected based on the chosen filter (e.g., fetching all records for a `property` filter).
2. **Pruning Refinement (Optional):**  The `pruningRefineBy` parameter refines the data to a specific time range (see "Refine By Operation" section).
3. **Filtering:** Filtering rules are applied to the refined data to determine PASS or FAIL.
4. **Coalescing Refinement (Optional):** The `coalescingRefineBy` parameter further refines the data based on the number of occurrences (e.g., "contact has filled out a form at least 2 times").  If present, records PASS if they meet the specified number of occurrences.  Otherwise, PASS/FAIL is determined by step 3.

## Filter Branches

Filter branches define the conditional logic.  They consist of a type (`filterBranchType`), an operator (`AND` or `OR`), a list of filters, and a list of sub-branches.

* **`AND` operator:** The record is accepted if it passes *all* filters and sub-branches within the branch.
* **`OR` operator:** The record is accepted if it passes *any* filter or sub-branch within the branch.

A record is a list member if it's accepted by the root filter branch.

**Structure:** All filter definitions must start with a root-level `OR` `filterBranchType` containing one or more nested `AND` sub-branches.

**Example JSON (OR with two nested AND branches):**

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

This creates a list of contacts with a first name of "John" OR those without a last name of "Smith".


**Example JSON (OR with one nested AND branch):**

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

This creates a list of contacts with a first name of "John" AND a last name of "Smith".


## Filtering on Events and Associated Objects

Special `AND` filter branch types:

* **`UNIFIED_EVENTS`:** Filters based on events.  Requires one or more `PROPERTY` filters.
* **`ASSOCIATION`:** Filters based on associated records.  Requires one or more filters.  Can have nested `ASSOCIATION` branches only for `CONTACT` to `LINE_ITEM` associations.

**Example JSON (using UNIFIED_EVENTS and ASSOCIATION):**

```json
{
  "filterBranches": [
    {
      "filterBranches": [
        {
          "filterBranchType": "UNIFIED_EVENTS",
          "filterBranchOperator": "AND",
          "filters": [ /* ...filters... */ ],
          "eventTypeId": "0-1",  // Example event type ID
          "operator": "HAS_COMPLETED" // Or HAS_NOT_COMPLETED
        },
        {
          "filterBranchType": "ASSOCIATION",
          "filterBranchOperator": "AND",
          "filters": [ /* ...filters... */ ],
          "objectTypeId": "0-1", // Example object type ID
          "operator": "IN_LIST",
          "associationTypeId": 280,
          "associationCategory": "HUBSPOT_DEFINED"
        }
      ],
      "filterBranchOperator": "AND",
      "filterBranchType": "AND",
      "filters": [ /* ...filters... */ ]
    }
  ],
  "filterBranchOperator": "OR",
  "filterBranchType": "OR",
  "filters": []
}
```


## Filter Branch Types

* **`OR`:**  Must have one or more nested `AND` branches. Cannot have filters directly within the OR branch. Accepts a record if *any* nested branch accepts it.
* **`AND`:** Can have zero or more filters and zero or more nested `UNIFIED_EVENTS` and/or `ASSOCIATION` branches. Accepts a record if it passes *all* filters and nested branches.
* **`UNIFIED_EVENTS`:** Only nested within `AND` branches.  Filters on unified events.
* **`ASSOCIATION`:** Only nested within `AND` branches. Filters on associated records.

## Filter Types

The `filterType` parameter defines the filter within the `filterBranch`.  Examples include: `PROPERTY`, `ADS_TIME`, `ADS_SEARCH`, `CTA`, `EMAIL_EVENT`, `EVENT`, `FORM_SUBMISSION`, `FORM_SUBMISSION_ON_PAGE`, `IN_LIST`, `PAGE_VIEW`, `PRIVACY`, `SURVEY_MONKEY`, `SURVEY_MONKEY_VALUE`, `WEBINAR`, `INTEGRATION_EVENT`.

## Property Filter Operations

The `operation` object defines parameters for `PROPERTY`, `INTEGRATION_EVENT`, and `SURVEY_MONKEY_VALUE` filter types.

* **`operationType`:** Type of operator (e.g., `NUMBER`, `MULTISTRING`).
* **`operator`:** Operator applied to `operationType` (e.g., `IS_EQUAL_TO`, `IS_NOT_EQUAL_TO`).
* **`value`/`values`:** Value(s) to filter by.
* **`includeObjectsWithNoValueSet`:** (Boolean)  Whether to include records with no value for the property (true) or exclude them (false, default).

**Example (firstname = "John"):**

```json
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
]
```

See the table below for a summary of operation types and supported operators.  Detailed information and examples are in the full HubSpot documentation.


| `operationType` | Supported Operators                                                                              | Description                                                                                                 |
|-----------------|--------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| `ALL_PROPERTY`  | `IS_KNOWN`, `IS_NOT_KNOWN`                                                                       | Whether a property value is known or unknown.                                                              |
| `BOOL`          | `IS_EQUAL_TO`, `IS_NOT_EQUAL_TO`, `HAS_EVER_BEEN_EQUAL_TO`, `HAS_NEVER_BEEN_EQUAL_TO`            | Boolean property value equality.                                                                            |
| `ENUMERATION`   | `IS_ANY_OF`, `IS_NONE_OF`, `IS_EXACTLY`, `IS_NOT_EXACTLY`, `CONTAINS_ALL_OF`, `DOES_NOT_CONTAIN_ALL_OF`, `HAS_EVER_BEEN_ANY_OF`, `HAS_NEVER_BEEN_ANY_OF`, `HAS_EVER_BEEN_EXACTLY`, `HAS_NEVER_BEEN_EXACTLY`, `HAS_EVER_CONTAINED_ALL`, `HAS_NEVER_CONTAINED_ALL` | Enumeration/multi-select property value comparisons.                                                       |
| `MULTISTRING`   | `IS_EQUAL_TO`, `IS_NOT_EQUAL_TO`, `CONTAINS`, `DOES_NOT_CONTAIN`, `STARTS_WITH`, `ENDS_WITH`         | String property value comparisons.                                                                          |
| `NUMBER`        | `IS_EQUAL_TO`, `IS_NOT_EQUAL_TO`, `IS_BETWEEN`, `IS_NOT_BETWEEN`, `HAS_EVER_BEEN_EQUAL_TO`, `HAS_NEVER_BEEN_EQUAL_TO` | Number property value comparisons.                                                                         |
| `STRING`        | `IS_EQUAL_TO`, `IS_NOT_EQUAL_TO`, `CONTAINS`, `DOES_NOT_CONTAIN`, `STARTS_WITH`, `ENDS_WITH`, `HAS_EVER_BEEN_EQUAL_TO`, `HAS_NEVER_BEEN_EQUAL_TO`, `HAS_EVER_CONTAINED`, `HAS_NEVER_CONTAINED` | String property value comparisons.                                                                          |
| `TIME_POINT`    | `IS_EQUAL_TO`, `IS_BEFORE`, `IS_AFTER`                                                          | Compares a property to a specific time or another property's value/last updated time.                       |
| `TIME_RANGED`   | `IS_BETWEEN`, `IS_NOT_BETWEEN`                                                                   | Compares a property to a specific time range.                                                              |



## TIME_POINT and TIME_RANGED Examples

Numerous examples for `TIME_POINT` and `TIME_RANGED` are provided in the original text, showcasing date comparisons, relative time offsets (e.g., "In Last X Number of Days"), and property comparisons.  Refer to the original text for these detailed JSON examples.


## Refine By Operation

* **`pruningRefineBy`:** Refines the dataset to a specific timeframe (relative or absolute).
* **`coalescingRefineBy`:** Determines if the record PASSES the filter a minimum/maximum number of times.

Only one refine by operation is allowed per filter.


## Pruning Refine By Operations

* **Absolute Comparative:** Compares a timestamp to a given timestamp.
* **Absolute Ranged:** Checks if a timestamp falls between two given timestamps.
* **Relative Comparative:** Compares a timestamp to a relative offset (days/weeks past/future).
* **Relative Ranged:** Checks if a timestamp falls within a relative time range.


## Coalescing Refine By Operations

Only `NUM_OCCURRENCES` is supported. Specifies minimum and maximum occurrences for a record to PASS the filter.


## v1 List Filters (Legacy)

The legacy v1 API is deprecated.  The primary difference is the limited `filterType` support (only `PROPERTY`).


## All Property Types, String, Multi-String, Number, Boolean, Enumeration, and Datetime Operations

The original text provides detailed information on operators supported by various property types in the v1 API.  Refer to the original for specific operator lists and examples.  These are similar to but not identical to the v3 API.


This markdown documentation summarizes the core aspects of HubSpot Lists API v3 filtering.  Always refer to the official HubSpot API documentation for the most up-to-date and comprehensive information.
