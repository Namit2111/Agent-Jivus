# HubSpot Lists API v3: List Filters Overview

This document provides a comprehensive overview of HubSpot's Lists API v3 filter functionality, enabling you to create dynamic and targeted lists based on various criteria.  It includes examples and explains the structure and logic behind list filters.


## List Filters: Defining Membership

List filters define which records are included in a HubSpot list.  When creating a list with `SNAPSHOT` or `DYNAMIC` processing type, you use filters to specify membership conditions.  These filters employ conditional logic using filter branches with `AND` or `OR` operations (defined by the `filterBranchType` parameter).  Each branch contains individual filters (`filterType` parameter) assessing records for inclusion.  Nested filter branches allow for complex logic.  HubSpot uses a `PASS`/`FAIL` system: records passing all filters become list members.


## Filter Evaluation Steps

1. **Record Selection:**  Relevant records are selected or fetched based on the chosen filter (e.g., all records for a `property` filter).

2. **Pruning Refinement (Optional):** The `pruningRefineBy` parameter refines the data to a specific time range (see "Refine By Operation" section).

3. **Filtering:** Filtering rules are applied to the (potentially refined) data to determine `PASS` or `FAIL`.

4. **Coalescing Refinement (Optional):** The `coalescingRefineBy` parameter further refines the data based on the number of times a record meets the criteria (e.g., "contact has filled out a form at least 2 times").

5. **Final Evaluation:**  Records are accepted based on step 3 (if no `coalescingRefineBy` is used) or step 4 (if `coalescingRefineBy` is present).


## Filter Branches

Filter branches structure the conditional logic.  They're defined by type (`filterBranchType`), operator (`AND` or `OR`), a list of filters, and a list of sub-branches.

* **`AND` Branch:** A record is accepted only if it passes *all* filters and sub-branches within the `AND` branch.

* **`OR` Branch:** A record is accepted if it passes *any* filter or sub-branch within the `OR` branch.

The root filter branch in a list definition must be an `OR` type.


## Structure of Filter Definitions

All list filter definitions must adhere to a specific structure:

* **Root Branch:** An `OR` filter branch.
* **Child Branches:** One or more nested `AND` filter branches within the root `OR` branch.

**Example JSON (OR with two AND branches):**

```json
{
  "filterBranch": {
    "filterBranchType": "OR",
    "filters": [],
    "filterBranches": [
      {
        "filterBranchType": "AND",
        "filters": [ /* Filters for first condition */ ],
        "filterBranches": []
      },
      {
        "filterBranchType": "AND",
        "filters": [ /* Filters for second condition */ ],
        "filterBranches": []
      }
    ]
  }
}
```

This structure is mandatory for proper rendering in the HubSpot UI.


## Filtering on Events and Associated Objects

Special `AND` filter branch types:

* **`UNIFIED_EVENTS`:** Filters on events.  Requires at least one filter.
* **`ASSOCIATION`:** Filters on associated records. Requires at least one filter.  Additional `filterBranches` are allowed only for `CONTACT` to `LINE_ITEM` associations.

**Example JSON (using UNIFIED_EVENTS and ASSOCIATION):**

```json
{
  "filterBranches": [
    {
      "filterBranchType": "AND",
      "filters": [ /* Main filters */ ],
      "filterBranches": [
        {
          "filterBranchType": "UNIFIED_EVENTS",
          "filters": [ /* Event filters */ ],
          "filterBranches": []
        },
        {
          "filterBranchType": "ASSOCIATION",
          "filters": [ /* Association filters */ ],
          "filterBranches": []
        }
      ]
    }
  ],
  "filterBranchType": "OR",
  "filters": []
}
```


## Filter Branch Types Detailed

* **`OR`:**  Must contain one or more nested `AND` branches.  Cannot have any direct filters. Accepts records passing any of its nested branches.

* **`AND`:** Can contain zero or more filters and zero or more nested `UNIFIED_EVENTS` and/or `ASSOCIATION` branches. Accepts records passing all filters and sub-branches.

* **`UNIFIED_EVENTS`:**  Only nested within `AND` branches. Contains one or more `PROPERTY` filters. Cannot have nested branches.

* **`ASSOCIATION`:** Only nested within `AND` branches. Must contain at least one filter. Cannot have nested branches except for `CONTACT` to `LINE_ITEM` associations.


## Filter Types

Numerous `filterType` options exist, including `PROPERTY`, `ADS_TIME`, `ADS_SEARCH`, `CTA`, `EMAIL_EVENT`, `EVENT`, `FORM_SUBMISSION`, `FORM_SUBMISSION_ON_PAGE`, `IN_LIST`, `PAGE_VIEW`, `PRIVACY`, `SURVEY_MONKEY`, `SURVEY_MONKEY_VALUE`, `WEBINAR`, and `INTEGRATION_EVENT`.  See HubSpot's documentation for detailed descriptions of each type.


## Property Filter Operations

When using `PROPERTY`, `INTEGRATION_EVENT`, or `SURVEY_MONKEY_VALUE` filters, an `operation` object is required:


* **`operationType`:**  Specifies the operator type (e.g., `NUMBER`, `STRING`).

* **`operator`:** The specific operator (e.g., `IS_EQUAL_TO`, `CONTAINS`).

* **`value` / `values`:** The value(s) to filter by.

* **`includeObjectsWithNoValueSet`:** (Boolean) Determines how records with no value for the property are handled (default: `false`).


## Time-Based Operations (`TIME_POINT`, `TIME_RANGED`)

These operations are used extensively for date and time-based filtering and offer various options such as comparing to specific dates, relative timeframes (e.g., "in the last X days"), or other properties' values.

**(See examples in original text for `TIME_POINT` and `TIME_RANGED` usage)**

## Refine By Operations

* **`pruningRefineBy`:** Refines the dataset to a specific time frame (absolute or relative).

* **`coalescingRefineBy`:** Determines if a record meets filter criteria a certain number of times.  Only one refine by operation is supported per filter.


## Legacy v1 List Filters

The v1 API (deprecated as of May 30, 2025) provides similar filtering but with differences in syntax and available options.  Migrate to v3 for continued support.  The only supported `filterType` in v1 is `PROPERTY`.


## All Property Types Operations

For all property types, you can filter based on whether a property value is known or unknown, using `IS_KNOWN` and `IS_NOT_KNOWN` operators.


## Specific Property Type Operations

The original text details available operations for string, multi-string, number, boolean, and datetime property types.  (See the original text for detailed operator lists and examples for each property type).


This markdown document provides a structured and detailed overview of the HubSpot Lists API v3 filter capabilities.  Refer to the original text and HubSpot's official documentation for the most up-to-date information and comprehensive examples.
