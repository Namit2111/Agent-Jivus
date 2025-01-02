# HubSpot Lists API: Filter Overview

This document provides a comprehensive overview of the HubSpot Lists API filters, focusing on the v3 API.  The v1 API is deprecated and will be sunsetted.  Refer to the HubSpot documentation for migration instructions.

## List Filters

List filters define the criteria for including records in a HubSpot list. They use conditional logic based on filter branches and individual filter types.  HubSpot uses PASS/FAIL logic; a record must pass all filters to be included.

### Filter Evaluation Steps

1. **Record Selection:** Relevant records are selected based on the filter criteria (e.g., fetching all records for a property filter).
2. **Pruning (Optional):** `pruningRefineBy` refines the data to a specific time range.
3. **Filtering:** Filtering rules are applied to the refined data to determine PASS or FAIL.
4. **Coalescing (Optional):** `coalescingRefineBy` further refines the data based on the number of occurrences (e.g., "contact has filled out a form at least 2 times").
5. **Final Result:** Records pass or fail based on steps 3 and 4.

### Filter Branches

Filter branches structure the conditional logic:

* **`filterBranchType`:** Defines the branch's operation type (`AND` or `OR`).
* **`filters`:** A list of individual filters within the branch.
* **`filterBranches`:** A list of nested filter branches.

**Structure:**

All filter definitions begin with a root-level `OR` filter branch, containing one or more nested `AND` filter branches.  This structure is required by the HubSpot API.

**Example (JSON):**

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

**OR Branch:**

* Must contain one or more nested `AND` branches.
* Cannot contain any filters directly.
* A record passes if it passes *any* nested `AND` branch.

**AND Branch:**

* Can contain zero or more filters.
* Can contain zero or more nested `UNIFIED_EVENTS` and/or `ASSOCIATION` branches.
* A record passes if it passes *all* filters and nested branches.


### Filtering on Events and Associated Objects

* **`UNIFIED_EVENTS`:** Filters based on HubSpot events.  Requires at least one property filter.
* **`ASSOCIATION`:** Filters based on associated records (e.g., contacts associated with deals).  Requires at least one filter.  Can have nested `ASSOCIATION` branches for certain object types (e.g., `CONTACT` to `LINE_ITEM`).


### Filter Types

The `filterType` parameter specifies the type of filter:

| `filterType`           | Description                                                                    |
|------------------------|--------------------------------------------------------------------------------|
| `ADS_TIME`             | Contact's ad interactions within a timeframe.                                   |
| `ADS_SEARCH`           | Contact's ad interactions based on specific criteria.                         |
| `CTA`                  | Contact's interaction with a specific call-to-action.                           |
| `EMAIL_EVENT`          | Contact's email opt-in status.                                               |
| `EVENT`                | Contact's interaction with a specific event.                                   |
| `FORM_SUBMISSION`      | Contact's form submissions (specific or any).                                 |
| `FORM_SUBMISSION_ON_PAGE` | Contact's form submissions on a specific page.                               |
| `IN_LIST`              | Whether a record is in a specific list, import, or workflow.                 |
| `PAGE_VIEW`            | Contact's page view history.                                                   |
| `PRIVACY`              | Contact's privacy consent status.                                              |
| `PROPERTY`             | Record's property value satisfies specified conditions (see below).             |
| `SURVEY_MONKEY`        | Contact's SurveyMonkey survey responses.                                       |
| `SURVEY_MONKEY_VALUE`  | Specific SurveyMonkey survey question responses.                               |
| `WEBINAR`              | Contact's webinar registration/attendance.                                      |
| `INTEGRATION_EVENT`    | Contact's interaction with integration events.                                |


### Property Filter Operations

The `PROPERTY` filter type uses an `operation` object:

* **`operationType`:** Type of operator (e.g., `NUMBER`, `MULTISTRING`).
* **`operator`:** Specific operator (e.g., `IS_EQUAL_TO`, `CONTAINS`).
* **`value`/`values`:** Value(s) to filter by.
* **`includeObjectsWithNoValueSet`:**  Handles records with no value set for the property (true = accept, false = reject).


| `operationType`       | Supported Operators                                             | Description                                                                  |
|-----------------------|-----------------------------------------------------------------|------------------------------------------------------------------------------|
| `ALL_PROPERTY`       | `IS_KNOWN`, `IS_NOT_KNOWN`                                      | Property value known or unknown.                                              |
| `BOOL`                | `IS_EQUAL_TO`, `IS_NOT_EQUAL_TO`, `HAS_EVER_BEEN_EQUAL_TO`, `HAS_NEVER_BEEN_EQUAL_TO` | Boolean property value.                                                       |
| `ENUMERATION`         | Various operators for multi-select properties                   | Enumeration/multi-select property value.                                      |
| `MULTISTRING`         | `IS_EQUAL_TO`, `IS_NOT_EQUAL_TO`, `CONTAINS`, `DOES_NOT_CONTAIN`, `STARTS_WITH`, `ENDS_WITH` | Multiple string values.                                                       |
| `NUMBER`              | `IS_EQUAL_TO`, `IS_NOT_EQUAL_TO`, `IS_BETWEEN`, `IS_NOT_BETWEEN`, etc. | Number property value.                                                        |
| `STRING`              | Similar to `MULTISTRING`, also includes historical operators       | Single string value.                                                          |
| `TIME_POINT`          | `IS_EQUAL_TO`, `IS_BEFORE`, `IS_AFTER`                           | Property updated before/after a specific time or relative to today.           |
| `TIME_RANGED`         | `IS_BETWEEN`, `IS_NOT_BETWEEN`                                  | Property updated within/outside a specific time range or relative to today.   |


**Time-based examples (TIME_POINT and TIME_RANGED):**  See the original text for detailed JSON examples of filtering by date, last X days, next X days, etc.  These examples show how to use `timeType`, `timezoneSource`, `zoneId`, `offset`, `indexReference` (e.g., `TODAY`, `NOW`), etc., to construct date-based filters.


### Refine By Operations

* **`pruningRefineBy`:**  Refines the dataset to a specific timeframe (absolute or relative).
* **`coalescingRefineBy`:** Determines whether a record passed the filter a specified number of times. Only one refine-by operation is allowed per filter.

**Pruning:**

* **`ABSOLUTE_COMPARATIVE`:** Before or after a specific timestamp.
* **`ABSOLUTE_RANGED`:** Between or outside a timestamp range.
* **`RELATIVE_COMPARATIVE`:** Before or after a relative time offset (days, weeks).
* **`RELATIVE_RANGED`:** Between or outside a relative time offset range.

**Coalescing:**

* **`NUM_OCCURRENCES`:** Minimum and maximum number of times a record must pass the filter.

### v1 List Filters (Legacy - Deprecated)

The v1 API is structurally similar but has a simpler syntax and fewer options.  It only supports `PROPERTY` filters.  The original text gives an example.

### All Property Types Operations

The original text details the operators for each property type (`string`, `multistring`, `number`, `boolean`, `enumeration`, `datetime`, etc.).  It showcases specific JSON examples for each property type and operator.  Consult the original text for detailed examples.


This markdown documentation summarizes the key aspects of HubSpot Lists API v3 filters. For detailed information and the most up-to-date specifications, always refer to the official HubSpot API documentation.
