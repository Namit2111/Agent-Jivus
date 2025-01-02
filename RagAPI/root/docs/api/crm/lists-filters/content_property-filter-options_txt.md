# HubSpot Lists API: Filter Documentation

This document details the HubSpot Lists API's filtering capabilities, focusing on the v3 API.  The legacy v1 API is deprecated and will be sunsetted.

## List Filters Overview

When creating HubSpot lists with `SNAPSHOT` or `DYNAMIC` processing types, filters determine which records are included.  Filters utilize conditional logic defined by *filter branches* with `AND` or `OR` operation types (`filterBranchType` parameter).  Within branches are individual filters (`filterType` parameter) assessing records for inclusion.  Branches can be nested.

HubSpot employs PASS/FAIL logic. A record becomes a list member only if it passes all filters.

## Filter Evaluation Steps

1. **Record Selection:** Relevant records are selected/fetched based on the filter (e.g., all records for a property filter).
2. **Pruning Refinement (Optional):**  `pruningRefineBy` refines data to a specific time range (see "Refine By Operation" section).
3. **Filtering:** Filtering rules are applied to the refined data to determine PASS or FAIL.
4. **Coalescing Refinement (Optional):** `coalescingRefineBy` further refines data based on the number of occurrences (e.g., "contact filled out a form at least 2 times").  If present, records PASS if they meet the specified occurrence count; otherwise, PASS/FAIL is determined by step 3.


## Filter Branches

A filter branch defines conditional logic.  It consists of a type (`filterBranchType`), an operator (`OR` or `AND`), a list of filters, and a list of sub-branches.

* **`AND` operator:** A record is accepted if it passes *all* filters and sub-branches within the branch.
* **`OR` operator:** A record is accepted if it passes *any* filter or sub-branch.

List membership requires acceptance by the root filter branch.

**Structure:** All filter definitions begin with a root-level `OR` filter branch containing one or more nested `AND` sub-branches.


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

This creates a list of contacts with the first name "John" OR those without the last name "Smith".


## Filtering on Events and Associated Objects

Two special `AND` filter branch types exist:

* **`UNIFIED_EVENTS`:** Filters based on events.  Requires at least one filter.
* **`ASSOCIATION`:** Filters on records associated with the primary record. Requires at least one filter.  Additional `filterBranches` are allowed only for `CONTACT` to `LINE_ITEM` associations.

These branches should be nested within an `AND` branch.


## Filter Branch Types

* **`OR` filter branch:**  Must have one or more nested `AND` branches and zero filters.  Accepts a record if *any* nested branch accepts it.

* **`AND` filter branch:** Can have zero or more filters and zero or more nested `UNIFIED_EVENTS` and/or `ASSOCIATION` branches. Accepts a record if it passes *all* filters and nested branches.

* **`UNIFIED_EVENTS` filter branch:**  Can only be nested within an `AND` branch.  Must have one or more `PROPERTY` filters and no other branches.

* **`ASSOCIATION` filter branch:** Can only be nested within an `AND` branch.  Must have one or more filters and cannot have nested branches (except for `CONTACT` to `LINE_ITEM`).


## Filter Types

The `filterType` parameter defines the filter within a `filterBranch`.  Examples include `PROPERTY`, `ADS_TIME`, `CTA`, `EMAIL_EVENT`, `EVENT`, `FORM_SUBMISSION`, `IN_LIST`, `PAGE_VIEW`, `PRIVACY`, `SURVEY_MONKEY`, `WEBINAR`, and `INTEGRATION_EVENT`. See the HubSpot documentation for a complete list and details.


## Property Filter Operations

When using `PROPERTY`, `INTEGRATION_EVENT`, or `SURVEY_MONKEY_VALUE` filter types, an `operation` object defines filter parameters:

* `operationType`:  The operator type (e.g., `NUMBER`, `MULTISTRING`).
* `operator`: The operator (e.g., `IS_EQUAL_TO`, `IS_NOT_EQUAL_TO`).
* `value`/`values`: The value(s) to filter by.
* `includeObjectsWithNoValueSet`:  Whether to include records without a value for the property (true/false, defaults to false).

**Example:**

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

This filters for contacts with a `firstname` of "John".

See the HubSpot documentation for supported `operationType` and `operator` combinations for each property type.


## `TIME_POINT` and `TIME_RANGED` Examples

These operation types allow for various date/time comparisons.  Examples include:

* **`Is equal to date`:**  Uses `TIME_RANGED` with precise start and end times.
* **`In Last X Number of Days`:** Uses `TIME_RANGED` with `INDEXED` `timeType` and negative `offset`.
* **`In Next X Number of Days`:** Uses `TIME_RANGED` with `INDEXED` `timeType` and positive `offset`.
* **`Updated or Not Updated in the Last X Days`:** Uses `TIME_RANGED` with `UPDATED_AT` `propertyParser` and `INDEXED` `timeType`.
* **`Is After Date`:** Uses `TIME_POINT` with a specific `DATE` `timeType`.
* **`Is Relative to Today`:** Uses `TIME_POINT` with `INDEXED` `timeType` and `offset`.
* **`Is Before or After another property`:** Uses `TIME_POINT` with `PROPERTY_REFERENCED` `timeType`.


See the HubSpot documentation for complete JSON examples of each.


## Refine By Operation

* **`pruningRefineBy`:** Refines the dataset to a specific timeframe (absolute or relative).
* **`coalescingRefineBy`:** Determines if a record PASSED the filter a minimum/maximum number of times (`NUM_OCCURRENCES`).

Only one refine by operation is allowed per filter.


## v1 List Filters (Legacy)

The deprecated v1 API has a similar filtering mechanism but with minor syntax differences and fewer options. The only supported `filterType` is `PROPERTY`.  Migration to the v3 API is recommended.


## Appendix:  All Property Types and Operations (v1)

The v1 API supports detailed filtering across various property types: `alltypes`, `string`, `multistring`, `number`, `boolean`, and `enumeration`. It also features various `datetime` operation types (`datetime`, `datetime-comparative`, `datetime-ranged`, `datetime-rolling`, `rolling-property-updated`).  Refer to the HubSpot documentation for comprehensive operator details for each property type.
