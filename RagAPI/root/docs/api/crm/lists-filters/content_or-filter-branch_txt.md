# HubSpot Lists API v3: List Filters Overview

This document provides a comprehensive overview of HubSpot's Lists API v3 filter functionality, enabling developers to define complex criteria for selecting records within lists.  The API uses a hierarchical structure based on `OR` and `AND` filter branches to create flexible and powerful filtering logic.

## List Filter Structure

List filters employ a hierarchical structure built upon filter branches.  The structure always begins with a root-level `OR` filter branch, containing one or more nested `AND` filter branches.  Each `AND` branch can contain individual filters and further nested branches (e.g., `UNIFIED_EVENTS` or `ASSOCIATION`).

**Basic Structure (JSON):**

```json
{
  "filterBranch": {
    "filterBranches": [
      {
        "filterBranches": [],
        "filterBranchType": "AND",
        "filters": [ /* Individual filters */ ]
      }
      /* More AND filter branches */
    ],
    "filterBranchType": "OR",
    "filters": []
  }
}
```

**Example: Contacts with First Name "John" OR without Last Name "Smith"**

This example demonstrates an `OR` branch with two `AND` sub-branches, each defining a specific criterion.

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

This example uses a single `AND` branch within the root `OR` branch.

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

* **`OR`:** Accepts a record if it satisfies *any* of its nested `AND` branches.  Must have at least one `AND` sub-branch and cannot have any individual filters.

* **`AND`:** Accepts a record only if it satisfies *all* of its filters and nested branches. Can have zero or more filters and zero or more nested `UNIFIED_EVENTS` or `ASSOCIATION` branches.

* **`UNIFIED_EVENTS`:**  Used to filter based on HubSpot's unified event framework.  Can only be nested within an `AND` branch. Requires at least one `PROPERTY` filter.

* **`ASSOCIATION`:** Used to filter on associated objects. Can only be nested within an `AND` branch. Requires at least one filter.  Allows nested `ASSOCIATION` branches only for `CONTACT` to `LINE_ITEM` associations.


## Filter Types

The `filterType` parameter specifies the type of filter condition.  Common types include: `PROPERTY`, `ADS_TIME`, `ADS_SEARCH`, `CTA`, `EMAIL_EVENT`, `EVENT`, `FORM_SUBMISSION`, `FORM_SUBMISSION_ON_PAGE`, `IN_LIST`, `PAGE_VIEW`, `PRIVACY`, `SURVEY_MONKEY`, `SURVEY_MONKEY_VALUE`, `WEBINAR`, and `INTEGRATION_EVENT`.

## Property Filter Operations

`PROPERTY` filters utilize an `operation` object to define filtering logic. Key parameters within the `operation` object include:

* **`operationType`:** Specifies the data type (e.g., `NUMBER`, `STRING`, `MULTISTRING`, `TIME_POINT`, `TIME_RANGED`).

* **`operator`:** Defines the comparison operator (e.g., `IS_EQUAL_TO`, `CONTAINS`, `IS_BETWEEN`, `IS_AFTER`).

* **`value` / `values`:** The value(s) to compare against.

* **`includeObjectsWithNoValueSet`:** Controls how records with no value for the property are handled (defaults to `false`).


## Time-Based Filters (`TIME_POINT` and `TIME_RANGED`)

These filter types provide powerful ways to filter based on timestamps.  They support both absolute dates and relative offsets from "today" or "now".

**Examples:**

* **`Is equal to date`:**  Filters records where a property's value matches a specific date.
* **`In Last X Number of Days`:** Filters records updated within the last X days.
* **`In Next X Number of Days`:** Filters records to be updated within the next X days.
* **`Updated or Not Updated in the Last X Days`:** Filters based on whether a property has been updated within the last X days.
* **`Is After Date`:** Filters records where a property's value is after a specified date.
* **`Is Relative to Today`:** Filters based on an offset (positive or negative) from today.
* **`Is Before or After another property`:** Compares a property's timestamp to another property's timestamp.


## Refine By Operations

Refine by operations further refine the dataset before filter evaluation:

* **`pruningRefineBy`:** Limits the dataset to a specific time range (absolute or relative).
* **`coalescingRefineBy`:** Filters records based on the number of times they meet the filter criteria (minimum and maximum occurrences).


## Legacy v1 Lists API

HubSpot's legacy v1 Lists API provides similar functionality but with minor differences in syntax and available options.  **Note:** The v1 API is sunsetting, and migration to v3 is recommended.


This documentation provides a high-level overview.  Refer to the official HubSpot API documentation for detailed specifications and examples for each filter type and operation.
