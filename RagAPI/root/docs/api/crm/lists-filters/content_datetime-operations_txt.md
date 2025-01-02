# HubSpot Lists API v3: List Filters Overview

This document provides a comprehensive overview of HubSpot's Lists API v3 filter functionality.  It explains how to construct filter definitions to specify which records belong to a list.  The API uses a hierarchical structure based on `AND` and `OR` logic.

## List Filter Fundamentals

When creating a HubSpot list with `SNAPSHOT` or `DYNAMIC` processing type, filters determine list membership.  Filters utilize conditional logic defined by filter branches, which employ `AND` or `OR` operations (specified via the `filterBranchType` parameter).

Within each branch, individual filters (`filterType` parameter) assess records for inclusion.  Nested filter branches are also supported, creating complex filtering logic.

HubSpot uses a `PASS`/`FAIL` system. A record becomes a list member only if it passes all filters.

## Filter Evaluation Steps

1. **Record Selection:** Relevant records are selected based on the filter's criteria. For example, a `property` filter retrieves all records for evaluation.

2. **Pruning Refinement (Optional):** The `pruningRefineBy` parameter refines the dataset to a specific time range.

3. **Filter Application:** Filtering rules are applied to the refined data to determine `PASS` or `FAIL`.

4. **Coalescing Refinement (Optional):** The `coalescingRefineBy` parameter further refines the data based on the number of occurrences.  If present, records `PASS` only if they meet the specified occurrence count. Otherwise, `PASS`/`FAIL` is determined by step 3.


## Filter Branch Structure

A filter branch is a data structure defining conditional logic. It comprises a `filterBranchType` (`OR` or `AND`), a list of filters, and a list of sub-branches.

* **`OR` Branch:** A record is accepted if it passes *any* filter or sub-branch within the `OR` branch.  `OR` branches must contain at least one `AND` sub-branch and cannot have any direct filters.

* **`AND` Branch:** A record is accepted only if it passes *all* filters and sub-branches within the `AND` branch.

The root filter branch must always be `OR`. This `OR` branch must contain one or more `AND` sub-branches.

**Example JSON Structure:**

```json
{
  "filterBranch": {
    "filterBranches": [
      {
        "filterBranches": [],
        "filterBranchType": "AND",
        "filters": [ /* filters here */ ]
      }
    ],
    "filterBranchType": "OR",
    "filters": []
  }
}
```


## Example API Calls

**Example 1:  First Name "John" OR Last Name NOT "Smith"**

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

**Example 2: First Name "John" AND Last Name "Smith"**

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

## Special Filter Branch Types

* **`UNIFIED_EVENTS`:** Filters on events.  Must be nested within an `AND` branch. Requires `eventTypeId` and `operator` (e.g., `HAS_COMPLETED`, `HAS_NOT_COMPLETED`).

* **`ASSOCIATION`:** Filters on associated records. Must be nested within an `AND` branch. Requires `objectTypeId`, `operator` (e.g., `IN_LIST`), `associationTypeId`, and `associationCategory`.


## Filter Types

The `filterType` parameter determines the type of filter.  Common types include: `PROPERTY`, `ADS_TIME`, `ADS_SEARCH`, `CTA`, `EMAIL_EVENT`, `EVENT`, `FORM_SUBMISSION`, `FORM_SUBMISSION_ON_PAGE`, `IN_LIST`, `PAGE_VIEW`, `PRIVACY`, `SURVEY_MONKEY`, `SURVEY_MONKEY_VALUE`, `WEBINAR`, `INTEGRATION_EVENT`.


## Property Filter Operations

`PROPERTY`, `INTEGRATION_EVENT`, and `SURVEY_MONKEY_VALUE` filters use an `operation` object:

* `operationType`:  (e.g., `NUMBER`, `STRING`, `MULTISTRING`, `TIME_POINT`, `TIME_RANGED`).

* `operator`: (e.g., `IS_EQUAL_TO`, `IS_NOT_EQUAL_TO`, `CONTAINS`, `IS_BETWEEN`).

* `value`/`values`: The value(s) to filter against.

* `includeObjectsWithNoValueSet`: Boolean; determines handling of records without a value for the property.


## Time-Based Filter Operations (`TIME_POINT` and `TIME_RANGED`)

These offer flexible date and time filtering using absolute or relative timestamps.  Examples include:

* **`Is equal to date`:** Filters for records with a property value equal to a specific date.

* **`In Last X Number of Days`:** Filters for records updated within the last X days.

* **`In Next X Number of Days`:** Filters for records to be updated in the next X days.

* **`Updated or Not Updated in the Last X Days`:** Filters based on whether a property was updated within a time frame.

* **`Is After Date`:** Filters for records with a property value after a specified date.

* **`Is Relative to Today`:** Filters based on a time offset relative to today.

* **`Is Before or After another property`:** Compares a property value to another property's value or last update time.


## Refine By Operations

* **`pruningRefineBy`:** Refines the dataset to a specific time range (absolute or relative).

* **`coalescingRefineBy`:** Filters based on the number of times a record passes the filter criteria.


## Legacy v1 Lists API

The legacy v1 API is deprecated and will be sunsetted.  While similar to v3, it has differences in syntax and available options.  Migration to v3 is recommended.


This documentation provides a high-level overview.  Refer to the official HubSpot API documentation for complete details and specific parameter descriptions.
