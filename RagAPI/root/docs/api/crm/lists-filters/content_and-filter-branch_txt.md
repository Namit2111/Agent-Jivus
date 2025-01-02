# HubSpot Lists API v3: List Filters Overview

This document provides a comprehensive overview of the HubSpot Lists API v3 filter functionality, including structure, filter types, operations, and examples.  The legacy v1 API is also briefly addressed.

## List Filters

List filters define the criteria for including records in a HubSpot list.  They use conditional logic based on filter branches with `AND` or `OR` operation types, defined by the `filterBranchType` parameter.  Individual filters within branches assess records using `filterType` parameters.  Nested filter branches are also supported.  HubSpot uses PASS/FAIL logic; a record must pass all filters to be included.

### Filter Evaluation Steps

1. **Record Selection:** Relevant records are selected based on the chosen filter (e.g., all records for a property filter).
2. **Pruning Refinement (Optional):** The `pruningRefineBy` parameter refines the data to a specific time range.
3. **Filtering:** Filtering rules are applied to the refined data, determining PASS or FAIL.
4. **Coalescing Refinement (Optional):** The `coalescingRefineBy` parameter further refines the data based on the number of occurrences (e.g., "contact has filled out a form at least 2 times").
5. **Final Result:**  Records pass if they meet the criteria from steps 3 and 4 (or step 3 if no coalescing is used).

### Filter Branches

Filter branches structure the conditional logic. They have a type (`filterBranchType`), an operator (`AND` or `OR`), a list of filters, and a list of sub-branches.

* **`AND` Operator:** The record is accepted if it passes *all* filters and sub-branches.
* **`OR` Operator:** The record is accepted if it passes *any* filter or sub-branch.

**Structure:** All filter definitions must begin with a root-level `OR` filter branch containing one or more nested `AND` sub-branches.

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

This example creates a list of contacts with firstname "John" OR lastname not "Smith".


### Filtering on Events and Associated Objects

* **`UNIFIED_EVENTS`:** Filters on events.  Must be nested within an `AND` branch and have one or more `PROPERTY` filters.
* **`ASSOCIATION`:** Filters on associated records.  Must be nested within an `AND` branch and have one or more filters.  Additional `filterBranches` are allowed only for `CONTACT` to `LINE_ITEM` associations.


### Filter Types

The `filterType` parameter specifies the filter type.  Some examples are:

| `filterType`           | Description                                                                     |
|------------------------|---------------------------------------------------------------------------------|
| `PROPERTY`             | Evaluates a record's property value against an operation.                       |
| `UNIFIED_EVENTS`       | Evaluates if a contact completed a unified event.                               |
| `ASSOCIATION`          | Evaluates records associated with the primary record.                            |
| `FORM_SUBMISSION`      | Evaluates form submissions.                                                       |
| `PAGE_VIEW`            | Evaluates page views.                                                            |
| `EMAIL_EVENT`          | Evaluates email opt-in status.                                                  |
| ...                     | Many more types are available; see the HubSpot documentation for a complete list. |


### Property Filter Operations

The `operation` object within a `PROPERTY` filter defines the operation parameters:

* `operationType`: The type of operator (e.g., `NUMBER`, `STRING`, `TIME_POINT`, `TIME_RANGED`).
* `operator`: The specific operator (e.g., `IS_EQUAL_TO`, `IS_GREATER_THAN`, `CONTAINS`).
* `value`/`values`: The value(s) to filter by.
* `includeObjectsWithNoValueSet`:  Whether to include records with no value set for the property (default: `false`).

### Time-Based Filter Examples (`TIME_POINT` and `TIME_RANGED`)

The following examples illustrate `TIME_POINT` and `TIME_RANGED` operations:

* **`Is equal to date`:**  Filters for records where a property's value is within a specific date range.
* **`In Last X Number of Days`:**  Filters for records updated within the last X days.
* **`In Next X Number of Days`:** Filters for records that will be updated within the next X days.
* **`Updated or Not Updated in the Last X Days`:** Filters based on whether a property was updated within the last X days.
* **`Is After Date`:** Filters for records where a property's value is after a specific date.
* **`Is Relative to Today`:** Filters based on an offset from today's date.
* **`Is Before or After another property (value or last updated)`:** Compares a property's value to another property's value or last updated time.

(Detailed JSON examples for each of these are present in the original text and are too lengthy to reproduce here.)

### Refine By Operations

* `pruningRefineBy`: Refines the dataset to a specific timeframe (absolute or relative).
* `coalescingRefineBy`: Determines if a record passed the filter a certain number of times.

Only one refine by operation is allowed per filter.


### Legacy v1 List Filters

The v1 API (deprecated) offers similar filtering but with minor syntax differences and fewer options.  Only `PROPERTY` is supported as a `filterType`.


## API Call Examples

(Numerous API call examples in JSON format are provided in the original text, detailing different filter scenarios and their associated JSON payloads. Due to their length, they are omitted from this summary but are highly recommended to be referenced directly from the original text.)


This documentation provides a structured overview. For detailed information on all filter types, operators, and parameters, refer to the complete HubSpot API documentation.
