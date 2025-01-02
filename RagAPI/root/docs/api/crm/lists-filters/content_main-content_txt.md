# HubSpot Lists API v3: List Filters Overview

This document provides a comprehensive overview of the HubSpot Lists API v3 filter functionality, enabling developers to create dynamic and complex list definitions.  The API uses a hierarchical structure of filter branches (AND/OR logic) containing individual filters to determine list membership.

## API Call

The core API call involves a POST request to create or update a list's filter definition. The specific endpoint will depend on the context of your HubSpot integration, but generally follows the pattern:

`/lists/{listId}/filters`

The request body is a JSON object detailing the filter structure.

## Data Structure: Filter Branches

List filters are built using nested filter branches, creating a tree-like structure.  Two primary branch types exist:

* **`OR` (`filterBranchType: "OR"`):**  A record is accepted if it passes *any* of its child branches.  It *must* contain at least one `AND` branch as a child; it cannot contain any filters directly.

* **`AND` (`filterBranchType: "AND"`):** A record is accepted if it passes *all* of its filters and *all* of its child branches. It can contain zero or more filters and zero or more nested `UNIFIED_EVENTS` and/or `ASSOCIATION` branches.


```json
{
  "filterBranch": {
    "filterBranches": [
      {
        "filterBranches": [],
        "filterBranchType": "AND",
        "filters": [ /* Filters here */ ]
      },
      {
        "filterBranches": [],
        "filterBranchType": "AND",
        "filters": [ /* More filters here */ ]
      }
    ],
    "filterBranchType": "OR",
    "filters": []
  }
}
```

This example shows an `OR` branch with two `AND` branches.  A record will be added to the list if it satisfies the conditions in *either* of the `AND` branches.


## Filter Types (`filterType`)

Several filter types are available, each evaluating specific criteria:

| `filterType`          | Description                                                                                                         |
|-----------------------|---------------------------------------------------------------------------------------------------------------------|
| `ADS_TIME`            | Evaluates ad viewership within a timeframe defined by `pruningRefineBy`.                                           |
| `ADS_SEARCH`          | Evaluates ad interactions.                                                                                            |
| `CTA`                 | Evaluates call-to-action interaction.                                                                                 |
| `EMAIL_EVENT`         | Evaluates email subscription opt-in status.                                                                           |
| `EVENT`               | Evaluates event participation.                                                                                       |
| `FORM_SUBMISSION`     | Evaluates form submission status.                                                                                   |
| `FORM_SUBMISSION_ON_PAGE` | Evaluates form submissions on a specific page.                                                                        |
| `IN_LIST`             | Evaluates membership in another list, import, or workflow.                                                          |
| `PAGE_VIEW`           | Evaluates page view history.                                                                                        |
| `PRIVACY`             | Evaluates privacy consent status.                                                                                   |
| `PROPERTY`            | Evaluates a record's property value (see "Property Filter Operations").                                                |
| `SURVEY_MONKEY`       | Evaluates SurveyMonkey survey response status.                                                                       |
| `SURVEY_MONKEY_VALUE` | Evaluates SurveyMonkey survey responses for specific question values.                                                   |
| `WEBINAR`             | Evaluates webinar registration and attendance.                                                                        |
| `INTEGRATION_EVENT`   | Filters contacts based on interactions with integration events and their properties.                                |


## Property Filter Operations (`filterType: "PROPERTY"`)

Property filters examine a record's property values.  They consist of:

* **`operationType`:**  The type of property (e.g., `NUMBER`, `STRING`, `MULTISTRING`, `TIME_POINT`, `TIME_RANGED`, `BOOL`, `ENUMERATION`, `ALL_PROPERTY`).

* **`operator`:**  The comparison operator (e.g., `IS_EQUAL_TO`, `CONTAINS`, `IS_BETWEEN`, `IS_AFTER`, `IS_BEFORE`).

* **`values` (or `value`):** The value(s) to compare against.

* **`includeObjectsWithNoValueSet` (boolean):** Determines whether records lacking a value for the property are included (`true`) or excluded (`false`).

**Example:** Filtering for contacts with "John" as their first name:

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

These operation types allow for filtering based on dates and times:

* **`TIME_POINT`:** Compares a property's value or last update time to a specific point in time (date, relative to today, or another property).  Operators include `IS_AFTER`, `IS_BEFORE`.

* **`TIME_RANGED`:** Checks if a property's value or last update time falls within a specified range. Operators include `IS_BETWEEN`, `IS_NOT_BETWEEN`.

**Examples:**  See the original text for several detailed examples of  `TIME_POINT` and `TIME_RANGED` filter usage, including "In Last X Number of Days," "Is After Date," and comparisons to other properties.


## `UNIFIED_EVENTS` and `ASSOCIATION` Filter Branches

These specialized `AND` branches filter based on events or associated objects:

* **`UNIFIED_EVENTS`:** Filters based on whether a record has completed (or not completed) a specific unified event. Requires `eventTypeId` and `operator` (e.g., `"HAS_COMPLETED"` or `"HAS_NOT_COMPLETED"`).

* **`ASSOCIATION`:** Filters based on associations between records (e.g., contacts and deals). Requires `objectTypeId`, `operator` (e.g., `"IN_LIST"`), `associationTypeId`, and `associationCategory`.


## Refine By Operations

These operations refine the dataset *before* filter evaluation:

* **`pruningRefineBy`:** Limits the dataset to a specific timeframe (absolute or relative).  Types include `ABSOLUTE_COMPARATIVE`, `ABSOLUTE_RANGED`, `RELATIVE_COMPARATIVE`, `RELATIVE_RANGED`.

* **`coalescingRefineBy`:**  Determines if a record meets filter criteria a minimum (`minOccurrences`) and maximum (`maxOccurrences`) number of times. Type: `NUM_OCCURRENCES`.


## Legacy v1 List Filters

The v1 API (deprecated) has a similar structure but with fewer features and a slightly different syntax.  It is strongly recommended to migrate to v3.

## Response

A successful API call will return a status code of 200 OK and likely contain information confirming the update or creation of the list filters.  Error responses will provide detailed information about the cause of failure.  Refer to HubSpot's API documentation for specific error codes and handling.
