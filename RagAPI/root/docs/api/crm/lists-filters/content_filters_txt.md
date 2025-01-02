# HubSpot Lists API: Filter Documentation

This document details the structure and usage of filters within the HubSpot Lists API (v3).  The legacy v1 API is deprecated and should not be used for new integrations.

## List Filters Overview

List filters define the criteria for including records in a HubSpot list.  They use conditional logic implemented through filter branches with `AND` or `OR` operations, determined by the `filterBranchType` parameter.  Each branch contains individual filters (`filterType` parameter) that evaluate records.  Filters use pass/fail logic; a record must pass all filters to be included.


## Filter Evaluation Steps

1. **Record Selection:** Relevant records are selected based on the filter.  For example, a `property` filter selects all records for evaluation.

2. **Pruning Refinement (Optional):**  The `pruningRefineBy` parameter refines the data to a specific time range.

3. **Filtering:** Filtering rules are applied to the refined data, resulting in pass/fail determinations.

4. **Coalescing Refinement (Optional):** The `coalescingRefineBy` parameter further refines the data based on the number of occurrences meeting the criteria.

5. **Final Determination:** Records pass or fail based on steps 3 and 4.


## Filter Branches

Filter branches structure the conditional logic.  They're defined by type (`filterBranchType`), operator (`AND` or `OR`), filters, and sub-branches.

* **`AND` Branch:** A record is accepted only if it passes *all* filters and sub-branches.
* **`OR` Branch:** A record is accepted if it passes *any* filter or sub-branch.

All filter definitions must begin with a root-level `OR` branch, containing one or more `AND` sub-branches.


### Example JSON Structure:

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

### Example: "First Name is John OR Last Name is not Smith"

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

### Example: "First Name is John AND Last Name is Smith"

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

## Filtering on Events and Associated Objects

* `UNIFIED_EVENTS`: Filters on events. Requires one or more `PROPERTY` filters.  No nested branches allowed.
* `ASSOCIATION`: Filters on associated records. Requires one or more filters.  Nested branches allowed only for `CONTACT` to `LINE_ITEM` associations.

These branches should be nested within an `AND` branch.


## Filter Branch Types

* **`OR`:** Root-level branch. Must have one or more `AND` sub-branches and zero filters.

* **`AND`:** Nested within `OR` branch. Can have zero or more filters and zero or more `UNIFIED_EVENTS` and/or `ASSOCIATION` sub-branches.

* **`UNIFIED_EVENTS`:** Nested within `AND` branch. Can have one or more `PROPERTY` filters. No nested branches.

* **`ASSOCIATION`:** Nested within `AND` branch. Must have one or more filters. Nested branches allowed only in specific cases.


## Filter Types

The `filterType` parameter specifies the type of filter.  Examples include: `PROPERTY`, `ADS_TIME`, `CTA`, `EMAIL_EVENT`, `EVENT`, `FORM_SUBMISSION`, `IN_LIST`, `PAGE_VIEW`, `PRIVACY`, `SURVEY_MONKEY`, `SURVEY_MONKEY_VALUE`, `WEBINAR`, `INTEGRATION_EVENT`.  See the HubSpot documentation for details on each type.


## Property Filter Operations

`PROPERTY`, `INTEGRATION_EVENT`, and `SURVEY_MONKEY_VALUE` filters use an `operation` object with:

* `operationType`: The operator type (e.g., `NUMBER`, `STRING`, `MULTISTRING`).
* `operator`: The specific operator (e.g., `IS_EQUAL_TO`, `CONTAINS`).
* `value`/`values`: The value(s) to filter by.
* `includeObjectsWithNoValueSet`:  (Boolean) Whether to include records without a value for the property.


## Time-Based Operations (`TIME_POINT`, `TIME_RANGED`)

These operations allow filtering based on dates and times, both absolute and relative to the current date.  See the examples in the original text for detailed JSON structures.


## Refine By Operations

* `pruningRefineBy`: Refines the dataset to a specific time range (absolute or relative).
* `coalescingRefineBy`: Specifies the minimum and maximum number of times a record must pass the filter.

Only one refine-by operation is allowed per filter.


## Legacy v1 List Filters

The v1 API is deprecated.  The only supported `filterType` was `PROPERTY`, with slightly different syntax than v3.


## All Property Types, String, Multi-string, Number, Boolean, Enumeration, and Datetime Operations

The original text provides detailed information on supported operators and usage for different property types in both v1 and v3 APIs.  Refer to that section for examples and specifics.  Note that the v1 API is deprecated.
