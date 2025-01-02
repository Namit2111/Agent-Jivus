# HubSpot Lists API v3: List Filters Overview

This document provides a comprehensive overview of HubSpot's Lists API v3 filter functionality.  It explains how to construct filters to define the criteria for including records in a HubSpot list.

## List Filtering Basics

When creating a HubSpot list with `SNAPSHOT` or `DYNAMIC` processing type, filters determine which records are included.  Filters utilize conditional logic defined by *filter branches* with `AND` or `OR` operations (specified by the `filterBranchType` parameter).  Within each branch are individual filters (`filterType` parameter) that assess records. Filter branches can be nested.  HubSpot employs PASS/FAIL logic; a record must pass all filters to be included.

## Filter Evaluation Steps

1. **Record Selection:** Relevant records are selected based on the filter (e.g., fetching all records for a `property` filter).
2. **Pruning Refinement (Optional):**  The `pruningRefineBy` parameter refines data to a specific time range.
3. **Filter Application:** Filtering rules are applied to the refined data to determine PASS or FAIL.
4. **Coalescing Refinement (Optional):** The `coalescingRefineBy` parameter further refines data based on the number of occurrences (e.g., "contact has filled out a form at least 2 times").
5. **Final PASS/FAIL:** Records pass if they meet the coalescing criteria (if present) or the criteria from step 3.

## Filter Branches

A filter branch defines the conditional logic:

* **`filterBranchType`:** Specifies `AND` or `OR` operation.
* **`filters`:**  A list of individual filters within the branch.
* **`filterBranches`:** A list of nested filter branches.

* **`AND` Branch:** A record is accepted if it passes *all* filters and sub-branches.
* **`OR` Branch:** A record is accepted if it passes *any* filter or sub-branch.

**Structure:** All filter definitions begin with a root-level `OR` filter branch containing one or more nested `AND` sub-branches.

**Example JSON (OR with two AND branches):**

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

This creates a list of contacts with the first name "John" OR those who don't have the last name "Smith".


## Special Filter Branch Types

* **`UNIFIED_EVENTS`:** Filters based on events.  Must be nested within an `AND` branch. Requires at least one `PROPERTY` filter.
* **`ASSOCIATION`:** Filters based on associated records (e.g., contacts associated with deals).  Must be nested within an `AND` branch. Requires at least one filter.  Additional `filterBranches` are allowed only for `CONTACT` to `LINE_ITEM` associations.


## Filter Types

The `filterType` parameter specifies the type of filter.  Examples include: `PROPERTY`, `ADS_TIME`, `CTA`, `EMAIL_EVENT`, `EVENT`, `FORM_SUBMISSION`, `IN_LIST`, `PAGE_VIEW`, `PRIVACY`, `SURVEY_MONKEY`, `SURVEY_MONKEY_VALUE`, `WEBINAR`, `INTEGRATION_EVENT`.  See the HubSpot documentation for details on each type.


## Property Filter Operations

Used with `PROPERTY`, `INTEGRATION_EVENT`, and `SURVEY_MONKEY_VALUE` filters.  The `operation` object contains:

* **`operationType`:**  Type of operator (e.g., `NUMBER`, `MULTISTRING`).
* **`operator`:**  Specific operator (e.g., `IS_EQUAL_TO`, `CONTAINS`).
* **`value` / `values`:** Value(s) to filter by.
* **`includeObjectsWithNoValueSet`:** Boolean; whether to include records with no value for the property.  Defaults to `false`.

## Time-Based Filters (`TIME_POINT`, `TIME_RANGED`)

These operation types provide flexible date and time filtering.  Examples include:

* **`Is equal to date`:** Filters for records updated on a specific date.
* **`In Last X Number of Days`:** Records updated within the last X days.
* **`In Next X Number of Days`:** Records to be updated within the next X days.
* **`Updated or Not Updated in the Last X Days`:** Records updated or not updated in the last X days.
* **`Is After Date`:** Records updated after a specific date.
* **`Is Relative to Today`:** Records updated a certain number of days before or after today.
* **`Is Before or After another property`:**  Compares the update time to another property's value or last updated time.


## Refine By Operations

* **`pruningRefineBy`:** Refines the dataset to a specific timeframe (absolute or relative).
* **`coalescingRefineBy`:**  Specifies the minimum and maximum number of times a record must pass the filter.

Only one refine-by operation is allowed per filter.

## Legacy v1 Lists API (Deprecated)

The v1 API is deprecated.  While similar to v3, it has differences in syntax and available options.  Migrate to v3 as soon as possible.  The only supported `filterType` is `PROPERTY`.


##  All Property Types, String, Multi-string, Number, Boolean, Enumeration, and Datetime Operations

Detailed examples and supported operators for each property type are provided in the original HubSpot documentation.  Refer to the linked documentation within the original text for complete details.


This Markdown documentation provides a structured overview of HubSpot's List API v3 filtering.  Always consult the official HubSpot API documentation for the most up-to-date information and detailed specifications.
