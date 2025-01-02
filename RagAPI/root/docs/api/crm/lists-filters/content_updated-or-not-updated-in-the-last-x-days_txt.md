# HubSpot Lists API v3: Filter Documentation

This document details the structure and usage of filters within the HubSpot Lists API v3.  It explains how to construct filter definitions to select specific records for inclusion in a list.  The legacy v1 API is also briefly covered, but its use is discouraged due to its impending deprecation.


## List Filters Overview

When creating a HubSpot list with `SNAPSHOT` or `DYNAMIC` processing type, filters define which records are included.  Filters utilize conditional logic based on `filterBranchType` (AND or OR) and individual `filterType` parameters.  Nested filter branches are allowed.

HubSpot employs PASS/FAIL logic.  A record is a list member only if it passes *all* filters.

### Filter Evaluation Steps

1. **Record Selection:** Relevant records are selected based on the filter (e.g., all records for a `property` filter).
2. **Pruning Refinement (Optional):**  `pruningRefineBy` refines the data to a specific time range.
3. **Filter Application:** Filtering rules are applied to the refined data to determine PASS or FAIL.
4. **Coalescing Refinement (Optional):** `coalescingRefineBy` further refines data based on the number of occurrences (e.g., "contact has filled out a form at least 2 times").
5. **Final PASS/FAIL:**  Records pass if they meet the coalescing criteria (if applicable) or the criteria from step 3.


### Filter Branches

A filter branch is a data structure defining the conditional logic.  It's defined by its type (`filterBranchType`), operator (AND or OR), a list of filters, and a list of sub-branches.

* **AND:** A record is accepted if it passes *all* filters and sub-branches.
* **OR:** A record is accepted if it passes *any* filter or sub-branch.

The root filter branch must always be an OR branch containing one or more AND sub-branches.


### Structure

The basic structure follows this pattern:

```json
{
  "filterBranch": {
    "filterBranches": [
      {
        "filterBranches": [],
        "filterBranchType": "AND",
        "filters": [ /* Filters here */ ]
      },
      /* More AND branches here */
    ],
    "filterBranchType": "OR",
    "filters": []
  }
}
```

**Example 1: First Name "John" OR Last Name NOT "Smith"**

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


### Filtering on Events and Associated Objects

Special `AND` filter branch types:

* **`UNIFIED_EVENTS`:** Filters based on events.  Requires at least one filter.
* **`ASSOCIATION`:** Filters based on associated records.  Requires at least one filter.  Additional `filterBranches` are allowed only for `CONTACT` to `LINE_ITEM` associations.

Example using both:  (Simplified, omits some details for brevity)

```json
{
  "filterBranches": [
    {
      "filterBranches": [
        { "filterBranchType": "UNIFIED_EVENTS", ... },
        { "filterBranchType": "ASSOCIATION", ... }
      ],
      "filterBranchType": "AND", ...
    }
  ],
  "filterBranchType": "OR", ...
}
```


### Filter Branch Types

* **`OR`:** The root-level branch. Must contain one or more AND sub-branches and have no filters.
* **`AND`:** Nested within OR branches. Can contain filters and `UNIFIED_EVENTS`/`ASSOCIATION` branches.
* **`UNIFIED_EVENTS`:** Nested within AND branches. Filters on unified events.
* **`ASSOCIATION`:** Nested within AND branches. Filters on associated records.


### Filter Types

Various filter types exist, each with specific parameters.  (See original text for a complete list and descriptions).  Key types include: `PROPERTY`, `UNIFIED_EVENTS`, `ASSOCIATION`, `ADS_TIME`, `ADS_SEARCH`, `CTA`, `EMAIL_EVENT`, etc.


### Property Filter Operations

`PROPERTY`, `INTEGRATION_EVENT`, and `SURVEY_MONKEY_VALUE` filters utilize an `operation` object:

* `operationType`:  The type of operator (e.g., `NUMBER`, `MULTISTRING`).
* `operator`: The specific operator (e.g., `IS_EQUAL_TO`, `CONTAINS`).
* `value`/`values`: The value(s) to filter by.
* `includeObjectsWithNoValueSet`:  Whether to include records with no value set for the property (default: `false`).

(See original text for a table of `operationType`s and supported operators).


### Time-Based Filter Examples

The original text provides detailed examples for various time-based operations using `TIME_POINT` and `TIME_RANGED`.  These include:

* `Is equal to date`
* `In Last X Number of Days`
* `In Next X Number of Days`
* `Updated or Not Updated in the Last X Days`
* `Is After Date`
* `Is Relative to Today`
* `Is Before or After another property`


### Refine By Operations

* **`pruningRefineBy`:** Refines the dataset to a specific timeframe (absolute or relative).
* **`coalescingRefineBy`:** Determines if a record passed the filter a specified number of times.

Only one refine-by operation is allowed per filter.


### Legacy v1 List Filters

The v1 API (deprecated) has a similar structure, but with a simpler filter type (`PROPERTY`) and minor syntax differences.  **Migrate to v3.**


## API Call Examples (Illustrative)

The provided text gives numerous JSON examples for creating lists with different filter criteria.  These examples demonstrate the usage of filter branches, filters, and operators to achieve specific filtering goals.  The exact API call method (POST, PUT, etc.) will depend on the specific HubSpot API endpoint used to create or update a list.  You'll need to consult the HubSpot API documentation for precise endpoint details and request methods.


##  Response

A successful API call to create or update a list will return a response indicating the status (success or failure) and potentially details about the created or updated list.  The exact format of the response will depend on the specific API endpoint and HubSpot's API specifications.  Error responses will provide information about any issues encountered during the process.
