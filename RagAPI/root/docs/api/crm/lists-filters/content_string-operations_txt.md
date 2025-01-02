# HubSpot Lists API: Filter Documentation

This document details the structure and usage of filters within the HubSpot Lists API (v3).  It covers filter types, branches, operations, and provides examples for common use cases.  The legacy v1 API is also briefly discussed.

## Overview

List filters define which records are included in a HubSpot list.  They utilize conditional logic based on `filterBranchType` (AND/OR) and individual `filterType` conditions.  A `PASS`/`FAIL` logic determines record membership.

### Filter Evaluation Steps:

1. **Record Selection:** Relevant records are selected based on the filter (e.g., all records for a property filter).
2. **Pruning Refinement (Optional):**  The `pruningRefineBy` parameter refines the data to a specific time range.
3. **Filtering:** Filtering rules are applied to the refined data to determine `PASS` or `FAIL`.
4. **Coalescing Refinement (Optional):** The `coalescingRefineBy` parameter further refines based on the number of occurrences (e.g., "contact has filled out a form at least 2 times").
5. **Final Evaluation:** Records pass if they meet all criteria, considering both pruning and coalescing refinements.


## Filter Branches

Filter branches structure the conditional logic.

* **Root Branch:** Always an `OR` filter branch (`filterBranchType: "OR"`).
* **Sub-branches:** Nested within the root branch, typically `AND` branches (`filterBranchType: "AND"`).  `AND` branches can contain other `AND` branches (e.g. for `UNIFIED_EVENTS` and `ASSOCIATION` filters).

**JSON Structure:**

```json
{
  "filterBranch": {
    "filterBranches": [
      {
        "filterBranches": [],
        "filterBranchType": "AND",
        "filters": [ /* Filters */ ]
      },
      {
        "filterBranches": [],
        "filterBranchType": "AND",
        "filters": [ /* Filters */ ]
      }
    ],
    "filterBranchType": "OR",
    "filters": []
  }
}
```

* **`OR` Branch:** Accepts a record if *any* of its sub-branches or filters pass.
* **`AND` Branch:** Accepts a record only if *all* its sub-branches and filters pass.


## Filter Types

The `filterType` parameter specifies the type of filter.  Examples include:

| `filterType`        | Description                                                                      |
|----------------------|----------------------------------------------------------------------------------|
| `PROPERTY`          | Filters based on a record's property value.                                      |
| `ADS_TIME`           | Evaluates ad views within a timeframe.                                          |
| `ADS_SEARCH`         | Evaluates ad interactions.                                                       |
| `CTA`               | Evaluates call-to-action interactions.                                           |
| `EMAIL_EVENT`        | Evaluates email subscription opt-in status.                                      |
| `EVENT`             | Evaluates specific events.                                                        |
| `FORM_SUBMISSION`   | Evaluates form submissions.                                                      |
| `FORM_SUBMISSION_ON_PAGE` | Evaluates form submissions on a specific page.                                 |
| `IN_LIST`           | Evaluates membership in other lists/imports/workflows.                            |
| `PAGE_VIEW`         | Evaluates page views.                                                            |
| `PRIVACY`           | Evaluates privacy consent.                                                       |
| `SURVEY_MONKEY`     | Evaluates SurveyMonkey survey responses.                                         |
| `SURVEY_MONKEY_VALUE` | Evaluates specific SurveyMonkey survey question responses with a specified value. |
| `WEBINAR`           | Evaluates webinar registrations/attendances.                                    |
| `INTEGRATION_EVENT` | Filters based on interactions with integration events.                           |


## Property Filter Operations

`PROPERTY` filters use an `operation` object with:

* `operationType`:  The type of operator (e.g., `NUMBER`, `STRING`, `MULTISTRING`, `TIME_POINT`, `TIME_RANGED`).
* `operator`: The specific operator (e.g., `IS_EQUAL_TO`, `CONTAINS`, `IS_BETWEEN`).
* `value` or `values`: The value(s) to compare against.
* `includeObjectsWithNoValueSet`:  Whether to include records with no value set for the property (true/false).

**Example (First Name is "John"):**

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

See the detailed table in the original text for supported `operationType` and operators for various property types.


## Time-Based Filters (`TIME_POINT`, `TIME_RANGED`)

These filter types are crucial for date-based filtering.  Examples from the original text include:

* **`IS_EQUAL_TO` date:**  Uses `TIME_RANGED` to specify a precise date range.
* **`In Last X Number of Days`:** Uses `TIME_RANGED` with `INDEXED` time points referencing `TODAY` and `NOW`.
* **`In Next X Number of Days`:** Similar to above, but with future offsets.
* **`Updated or Not Updated in the Last X Days`:** Uses `TIME_RANGED` with `UPDATED_AT` property parser.
* **`Is After Date`:** Uses `TIME_POINT` with a specified date.
* **`Is Relative to Today`:** Uses `TIME_POINT` with `INDEXED` time points.
* **`Is Before or After another property`:** Uses `TIME_POINT` with `PROPERTY_REFERENCED` time points.

(See detailed JSON examples in the original text)


## Refine By Operations

* **`pruningRefineBy`:** Refines the dataset to a specific time range (absolute or relative).
* **`coalescingRefineBy`:**  Determines if a record passed the filter a minimum/maximum number of times.

Only one refine-by operation is allowed per filter.

(See detailed JSON examples of `ABSOLUTE_COMPARATIVE`, `ABSOLUTE_RANGED`, `RELATIVE_COMPARATIVE`, `RELATIVE_RANGED`, and `NUM_OCCURRENCES` in the original text)


## Special Filter Branch Types

* **`UNIFIED_EVENTS`:**  Filters based on unified events.  Must be nested within an `AND` branch.
* **`ASSOCIATION`:**  Filters based on associated records. Must be nested within an `AND` branch.


## Legacy v1 Lists API

The v1 API is deprecated.  Its filter structure is similar but less feature-rich than v3.  Only `PROPERTY` filters are supported.  (See a v1 example in the original text)


##  Conclusion

This markdown document provides a comprehensive overview of HubSpot Lists API v3 filtering capabilities. The detailed examples and descriptions should enable developers to effectively create complex filter logic for their lists. Remember to consult the HubSpot documentation for the most up-to-date information and further details.
