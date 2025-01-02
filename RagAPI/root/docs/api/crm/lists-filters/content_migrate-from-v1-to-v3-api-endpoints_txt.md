# HubSpot Lists API v3: List Filters Overview

This document provides a comprehensive overview of HubSpot's List API v3 filter functionality, enabling you to define criteria for selecting records in your lists.  HubSpot uses a nested structure of `AND` and `OR` filter branches to achieve complex filtering logic.

## List Filter Structure

List filters utilize a hierarchical structure:

* **Root Level:**  Always an `OR` filter branch. This means at least one of the nested `AND` branches must be satisfied for a record to be included.
* **Nested `AND` Branches:** One or more `AND` branches are nested within the root `OR` branch. A record must satisfy *all* filters within an `AND` branch to be accepted by that branch.
* **Filters:** Individual filter conditions are defined within each `AND` branch.  These filters specify criteria based on property values, events, or associations.

**Example JSON Structure:**

```json
{
  "filterBranch": {
    "filterBranches": [
      {
        "filterBranches": [],
        "filterBranchType": "AND",
        "filters": [ /* Filters for branch 1 */ ]
      },
      {
        "filterBranches": [],
        "filterBranchType": "AND",
        "filters": [ /* Filters for branch 2 */ ]
      }
    ],
    "filterBranchType": "OR",
    "filters": []
  }
}
```

This example shows an `OR` branch containing two `AND` branches. A record will be included in the list if it satisfies *all* the filters in *either* branch 1 *or* branch 2.


## Filter Branch Types

* **`OR` Filter Branch:**
    * Must contain one or more nested `AND` branches.
    * Cannot contain any individual filters (`filters`: `[]`).
    * A record is accepted if it satisfies the conditions in *at least one* nested `AND` branch.

* **`AND` Filter Branch:**
    * Can contain zero or more individual filters.
    * Can contain zero or more nested `UNIFIED_EVENTS` or `ASSOCIATION` branches.
    * A record is accepted only if it satisfies the conditions of *all* individual filters and *all* nested branches within the `AND` branch.

* **`UNIFIED_EVENTS` Filter Branch:**
    * Only allowed as a nested branch within an `AND` branch.
    * Used to filter based on events (e.g., form submissions, email opens).
    * Requires `eventTypeId` and `operator` (e.g., `HAS_COMPLETED`, `HAS_NOT_COMPLETED`).

* **`ASSOCIATION` Filter Branch:**
    * Only allowed as a nested branch within an `AND` branch.
    * Used to filter based on associated objects (e.g., deals associated with a contact).
    * Requires `objectTypeId`, `operator` (e.g., `IN_LIST`), `associationTypeId`, and `associationCategory`.


## Filter Types

The `filterType` parameter specifies the type of filter condition.  Key types include:

* `PROPERTY`: Filters based on the value of a contact or company property.
* `ADS_TIME`, `ADS_SEARCH`, `CTA`, `EMAIL_EVENT`, `EVENT`, `FORM_SUBMISSION`, `FORM_SUBMISSION_ON_PAGE`, `IN_LIST`, `PAGE_VIEW`, `PRIVACY`, `SURVEY_MONKEY`, `SURVEY_MONKEY_VALUE`, `WEBINAR`, `INTEGRATION_EVENT`:  Filters based on specific HubSpot or integration events.


## Property Filter Operations

`PROPERTY` filters utilize the `operation` object to define the comparison logic.  This object includes:

* `operationType`: The data type of the property (e.g., `NUMBER`, `STRING`, `MULTISTRING`, `BOOL`, `ENUMERATION`, `TIME_POINT`, `TIME_RANGED`).
* `operator`: The comparison operator (e.g., `IS_EQUAL_TO`, `IS_GREATER_THAN`, `CONTAINS`, `IS_BETWEEN`).
* `value` or `values`: The value(s) to compare against.
* `includeObjectsWithNoValueSet`:  (Boolean) Determines how records with no value for the specified property are handled.


## Time-Based Filters (`TIME_POINT` and `TIME_RANGED`)

These filter types allow for comparisons against dates and times.  They support various options, including:

* Specific dates.
* Relative dates (e.g., "in the last 7 days").
* Comparisons against other properties (e.g., "before another property's value").

## Refine By Operations

* `pruningRefineBy`: Refines the dataset to a specific time range before applying filters.  Supports absolute and relative time ranges (comparative and ranged).
* `coalescingRefineBy`: Specifies the minimum and maximum number of times a record must pass the filter criteria.


## API Call Example

To create a list of contacts with "John" as their first name OR those without "Smith" as their last name:

```json
POST /crm/v3/objects/lists

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

## Legacy v1 Lists API (Deprecated)

The v1 API is deprecated.  Migrate to the v3 API for continued support.  The v1 API has a similar structure but with fewer filter types and options.


This documentation provides a comprehensive guide to HubSpot's List API v3 filter capabilities. Refer to the official HubSpot API documentation for the most up-to-date details and additional filter types and operators.
