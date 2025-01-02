# HubSpot Lists API: Filter Documentation

This document details the structure and usage of filters within the HubSpot Lists API (v3).  It explains how to construct filter definitions to target specific records for inclusion in lists.  Note that the legacy v1 API is deprecated.

## List Filter Overview

List filters control which records are included in a HubSpot list.  They use conditional logic defined by filter branches with `AND` or `OR` operation types (`filterBranchType` parameter).  Each branch contains individual filters (`filterType` parameter) that assess records.  Branches can be nested.

HubSpot uses PASS/FAIL logic.  A record is a list member if it passes all filters in the filter definition.


## Filter Evaluation Steps

1. **Record Selection:** Relevant records are selected based on the filter. For example, a `property` filter selects records based on their property values.
2. **Pruning Refinement (Optional):** The `pruningRefineBy` parameter refines the data to a specific time range.
3. **Filtering:** Filtering rules are applied to determine PASS or FAIL.
4. **Coalescing Refinement (Optional):** The `coalescingRefineBy` parameter refines the data based on the number of times a record satisfies a filter.
5. **Final Evaluation:** Records are included if they meet all criteria.


## Filter Branches

Filter branches define conditional logic.  They consist of:

* **`filterBranchType`:**  `OR` or `AND`.
* **`filters`:** A list of individual filters within the branch.
* **`filterBranches`:** A list of nested filter branches.


### `OR` Filter Branch

* Must contain one or more nested `AND` filter branches.
* Cannot have any individual filters (`filters` array must be empty).
* A record passes if it passes *any* nested `AND` branch.

```json
{
  "filterBranchType": "OR",
  "filterBranches": [ /* One or more AND branches */ ],
  "filters": []
}
```

### `AND` Filter Branch

* Can contain zero or more individual filters.
* Can contain zero or more nested `UNIFIED_EVENTS` and/or `ASSOCIATION` filter branches.
* A record passes if it passes *all* individual filters and *all* nested branches.

```json
{
  "filterBranchType": "AND",
  "filterBranches": [ /* Zero or more UNIFIED_EVENTS or ASSOCIATION branches */ ],
  "filters": [ /* Zero or more filters */ ]
}
```

### `UNIFIED_EVENTS` Filter Branch

* Only allowed as a nested branch within an `AND` branch.
* Filters on whether records have or haven't completed a specified unified event.
* Must have one or more `PROPERTY` filters.
* Cannot have nested filter branches.

```json
{
  "filterBranchType": "UNIFIED_EVENTS",
  "filterBranches": [],
  "filters": [ /* One or more PROPERTY filters */ ],
  "eventTypeId": "0-1",  //Event Type ID
  "operator": "HAS_COMPLETED" // or HAS_NOT_COMPLETED
}
```

### `ASSOCIATION` Filter Branch

* Only allowed as a nested branch within an `AND` branch.
* Filters records based on their association with the primary record.
* Must have one or more filters.
* Cannot have nested filter branches except for `CONTACT` to `LINE_ITEM` associations which may have additional nested `ASSOCIATION` branches.

```json
{
  "filterBranchType": "ASSOCIATION",
  "filterBranches": [],
  "filters": [ /* One or more filters */ ],
  "objectTypeId": "0-1", //Object Type ID
  "operator": "IN_LIST", //Can also be different operators
  "associationTypeId": 280,
  "associationCategory": "HUBSPOT_DEFINED" // or USER_DEFINED, INTEGRATOR_DEFINED
}
```

## Filter Structure Example

A list of contacts with first name "John" OR those without last name "Smith":

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

The `filterType` parameter specifies the type of filter.  Common types include:

* `PROPERTY`: Filters based on property values (see "Property Filter Operations").
* `ADS_TIME`, `ADS_SEARCH`, `CTA`, `EMAIL_EVENT`, `EVENT`, `FORM_SUBMISSION`, `FORM_SUBMISSION_ON_PAGE`, `IN_LIST`, `PAGE_VIEW`, `PRIVACY`, `SURVEY_MONKEY`, `SURVEY_MONKEY_VALUE`, `WEBINAR`, `INTEGRATION_EVENT`:  These filter types have their own specific parameters.


## Property Filter Operations

`PROPERTY` filters use an `operation` object:

* `operationType`: Data type (e.g., `NUMBER`, `STRING`, `MULTISTRING`, `TIME_POINT`, `TIME_RANGED`).
* `operator`: Comparison operator (e.g., `IS_EQUAL_TO`, `IS_GREATER_THAN`, `CONTAINS`).
* `value` or `values`: Value(s) to compare against.
* `includeObjectsWithNoValueSet`:  Whether to include records without a value for the property (default: `false`).


**Example:**

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

These filter types allow for filtering based on dates and times, including relative offsets from the current time.  Examples include:

* **`Is equal to date`:** Specifies an exact date and time.
* **`In Last X Number of Days`:**  Specifies a range from X days ago to the present.
* **`In Next X Number of Days`:** Specifies a range from the present to X days in the future.
* **`Updated or Not Updated in the Last X Days`:**  Filters based on the last update time of a property.
* **`Is After Date`:**  Specifies a date and time after which a record must have been updated.
* **`Is Relative to Today`:**  Specifies a number of days before or after today.
* **`Is Before or After another property (value or last updated)`:** Compares a property's value or last updated timestamp to another property.


Detailed JSON examples for each of these time-based filter types are provided in the original text.


## Refine By Operations

Refine by operations further refine the dataset:

* **`pruningRefineBy`:** Limits the dataset to a specific time range (absolute or relative).  Examples include `ABSOLUTE_COMPARATIVE`, `ABSOLUTE_RANGED`, `RELATIVE_COMPARATIVE`, `RELATIVE_RANGED`.
* **`coalescingRefineBy`:**  Specifies the minimum and maximum number of times a record must pass the filter (`NUM_OCCURRENCES`).


## Legacy v1 Lists API (Deprecated)

The v1 API is deprecated.  It offers a simpler filtering mechanism with only `PROPERTY` filters, but lacks the features and flexibility of v3.  Migration to v3 is recommended.


## Property Type Operations (v1 and v3 Differences Noted Where Applicable)

The original text provides extensive examples of filtering operations based on various property types:  `string`, `multistring`, `number`, `boolean`, `enumeration`, and `datetime` (v1 uses different propertyType names for `datetime` operations).  Refer to the original for detailed examples and supported operators for each type.  Note that v3 offers many more operators and functionalities compared to v1.


This markdown documentation provides a structured overview of HubSpot's Lists API filtering capabilities.  For complete details and the most up-to-date information, always refer to the official HubSpot API documentation.
