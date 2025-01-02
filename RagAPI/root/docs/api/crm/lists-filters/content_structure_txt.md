# HubSpot Lists API v3: List Filters Overview

This document provides a comprehensive overview of the HubSpot Lists API v3 filter functionality.  It details the structure, types, and usage of filters for creating both `SNAPSHOT` and `DYNAMIC` lists.  The legacy v1 API is also briefly discussed.

## List Filters: Defining List Membership

List filters use conditional logic to determine which records belong to a list.  This logic is built using:

* **Filter Branches:**  These define the overall structure of the filter logic using `AND` or `OR` operators (`filterBranchType`).
* **Filters:**  These are individual conditions applied within filter branches (`filterType`).  They check specific properties or events.

HubSpot uses PASS/FAIL logic. A record is a list member only if it passes *all* filters in its path.

## Filter Evaluation Steps

1. **Record Selection:** Relevant records are selected based on the chosen filter.
2. **Pruning Refinement (Optional):**  The `pruningRefineBy` parameter refines the data to a specific time range.
3. **Filter Application:** Filtering rules are applied to the refined data to determine PASS or FAIL status.
4. **Coalescing Refinement (Optional):** The `coalescingRefineBy` parameter further refines based on the number of times a record meets the criteria.
5. **Final PASS/FAIL:**  The record's final status is determined based on steps 3 and 4.

## Filter Branches

Filter branches are hierarchical.  The structure *must* begin with a root-level `OR` filter branch, followed by one or more nested `AND` filter branches.

**Structure (JSON):**

```json
{
  "filterBranch": {
    "filterBranches": [
      {
        "filterBranches": [],
        "filterBranchType": "AND",
        "filters": [ /* filters here */ ]
      },
      /* more AND branches */
    ],
    "filterBranchType": "OR",
    "filters": []
  }
}
```

**Example:  First Name "John" OR Last Name NOT "Smith"**

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

## Special Filter Branch Types

* **`UNIFIED_EVENTS`:** Filters based on HubSpot events.  Must be nested within an `AND` branch.
* **`ASSOCIATION`:** Filters based on associated records. Must be nested within an `AND` branch.  Allows for nested `ASSOCIATION` branches in `CONTACT` to `LINE_ITEM` associations.


## Filter Types (`filterType`)

The available filter types vary; some are property-based while others use specific HubSpot events or actions.  A full list is available in the HubSpot documentation.  Key examples include:

* `PROPERTY`: Filters based on property values (see below).
* `FORM_SUBMISSION`: Filters based on form submissions.
* `EVENT`: Filters based on HubSpot events.
* `PAGE_VIEW`: Filters based on page views.

## Property Filter Operations

`PROPERTY`, `INTEGRATION_EVENT`, and `SURVEY_MONKEY_VALUE` filter types use an `operation` object to define filtering criteria:

* `operationType`:  The type of operation (e.g., `NUMBER`, `STRING`, `MULTISTRING`, `TIME_POINT`, `TIME_RANGED`).
* `operator`: The operator used (e.g., `IS_EQUAL_TO`, `CONTAINS`, `IS_BETWEEN`).
* `value` / `values`: The value(s) to compare against.
* `includeObjectsWithNoValueSet`:  (boolean) Whether to include records without a value for the property.


## Time-Based Operations (`TIME_POINT`, `TIME_RANGED`)

These operations allow filtering based on time-based properties. Examples include:

* **`Is equal to date`:** Filters for records where a property's value matches a specific date.
* **`In Last X Number of Days`:** Filters for records updated within the last X days.
* **`In Next X Number of Days`:** Filters for records to be updated in the next X days.
* **`Updated or Not Updated in the Last X Days`:** Filters based on property update status.
* **`Is After Date`:** Filters for records with a property value after a specific date.
* **`Is Relative to Today`:** Filters based on an offset from the current date.
* **`Is Before or After another property (value or last updated)`:**  Compares a property's value or last updated time to another property.

## Refine By Operations

* **`pruningRefineBy`:** Refines the dataset to a specific time range (absolute or relative).
* **`coalescingRefineBy`:**  Specifies the minimum and maximum number of times a record must meet the filter criteria to pass.

Only one refine by operation can be used at a time.

## Legacy v1 Lists API

The v1 API has a similar structure but with some differences in syntax and available options.  **It is deprecated and will be sunsetted.**  Migrate to the v3 API.  The primary difference is that only `PROPERTY` filterType is supported.


## Conclusion

This document provides a high-level overview.  Refer to the official HubSpot documentation for exhaustive details and the most up-to-date information.  Remember to always consult the API reference for precise parameter definitions and supported values.
