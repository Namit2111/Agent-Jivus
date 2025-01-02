# HubSpot Lists API v3: List Filters Overview

This document details the structure and usage of filters within HubSpot's Lists API v3.  These filters determine which records are included in a `SNAPSHOT` or `DYNAMIC` list.

## API Endpoint

The primary endpoint for list creation and manipulation (including filter definitions) is a POST request to the HubSpot Lists API. The exact endpoint URL will vary depending on your HubSpot account and API key.  Refer to the HubSpot API documentation for the specific URL.

## Filter Structure

List filters utilize a hierarchical structure composed of:

* **Filter Branches:**  These define the conditional logic (AND/OR) governing filter evaluation.  A root `OR` branch is mandatory, containing one or more nested `AND` branches.

* **Filters:** These are individual conditions applied to records.  Multiple filter types exist, each assessing a specific record aspect (e.g., property values, events, associations).

The `PASS`/`FAIL` logic determines record inclusion: a record must pass all filters within its accepted branch to become a list member.

### JSON Structure Example

The basic JSON structure of a filter definition follows this pattern:

```json
{
  "filterBranch": {
    "filterBranchType": "OR", // Root branch MUST be OR
    "filters": [],             // Filters directly under OR (optional, but usually empty)
    "filterBranches": [        // Nested AND branches
      {
        "filterBranchType": "AND",
        "filters": [           // Filters within the AND branch
          {
            "filterType": "PROPERTY", // Example filter type
            "property": "firstname",
            "operation": {
              "operationType": "MULTISTRING",
              "operator": "IS_EQUAL_TO",
              "values": ["John"]
            }
          }
        ],
        "filterBranches": []     // Potentially nested branches (UNIFIED_EVENTS, ASSOCIATION)
      },
      // ... more AND branches ...
    ]
  }
}
```

## Filter Branch Types

* **`OR` Filter Branch:** The root-level branch.  A record is accepted if it passes *any* of its nested `AND` branches.  It cannot contain any direct filters (`filters` array must be empty).

* **`AND` Filter Branch:** Nested within the `OR` branch.  A record is accepted only if it passes *all* its filters and *all* its nested branches (including `UNIFIED_EVENTS` and `ASSOCIATION`).

* **`UNIFIED_EVENTS` Filter Branch:**  Only allowed within an `AND` branch. Filters records based on their interaction with HubSpot unified events. Requires at least one `PROPERTY` filter.

* **`ASSOCIATION` Filter Branch:** Only allowed within an `AND` branch. Filters records based on their association with other objects. Requires at least one filter.  Nested `filterBranches` are possible only for `CONTACT` to `LINE_ITEM` associations.


## Filter Types

Several filter types are available, each serving a different purpose:

| `filterType`           | Description                                                                        |
|------------------------|------------------------------------------------------------------------------------|
| `ADS_TIME`             | Evaluates ad exposure within a timeframe.                                             |
| `ADS_SEARCH`           | Evaluates ad interactions.                                                            |
| `CTA`                  | Evaluates call-to-action interaction.                                                 |
| `EMAIL_EVENT`          | Evaluates email subscription status.                                                |
| `EVENT`                | Evaluates event participation.                                                      |
| `FORM_SUBMISSION`      | Evaluates form submission status.                                                   |
| `FORM_SUBMISSION_ON_PAGE` | Evaluates form submissions on a specific page.                                       |
| `IN_LIST`              | Evaluates membership in other lists, imports, or workflows.                           |
| `PAGE_VIEW`            | Evaluates page view history.                                                        |
| `PRIVACY`              | Evaluates privacy consent status.                                                   |
| `PROPERTY`             | Evaluates a record's property values (most common type; see Property Filter Operations). |
| `SURVEY_MONKEY`        | Evaluates SurveyMonkey survey responses.                                             |
| `SURVEY_MONKEY_VALUE`  | Evaluates specific SurveyMonkey question responses.                                  |
| `WEBINAR`              | Evaluates webinar registration/attendance.                                           |
| `INTEGRATION_EVENT`    | Evaluates interactions with integration events.                                    |


## Property Filter Operations

The `PROPERTY` filter type uses an `operation` object to specify the filtering logic:

* **`operationType`:** Specifies the data type (e.g., `NUMBER`, `STRING`, `MULTISTRING`, `TIME_POINT`, `TIME_RANGED`).

* **`operator`:**  The comparison operator (e.g., `IS_EQUAL_TO`, `IS_GREATER_THAN`, `CONTAINS`).

* **`value` or `values`:** The value(s) to compare against.

* **`includeObjectsWithNoValueSet`:** (Boolean)  Determines whether records with no value for the specified property are included. Defaults to `false`.


Detailed operator options per `operationType` are provided in the original document.


## Time-Based Filters (`TIME_POINT`, `TIME_RANGED`)

These filter types allow for flexible date and time comparisons. Examples provided include:

* **`Is equal to date`**
* **`In Last X Number of Days`**
* **`In Next X Number of Days`**
* **`Updated or Not Updated in the Last X Days`**
* **`Is After Date`**
* **`Is Relative to Today`**
* **`Is Before or After another property (value or last updated)`**

The JSON examples demonstrating these are extensive in the original document.


## Refine By Operations

* **`pruningRefineBy`:** Narrows the dataset to a specific time range (absolute or relative).
* **`coalescingRefineBy`:**  Determines if a record meets filter criteria a certain number of times.

Only one refine by operation can be used per filter.


## Legacy v1 Lists API

The original document mentions the legacy v1 API, which is deprecated.  Migration to the v3 API is advised.  The v1 API had a simpler structure with only the `PROPERTY` filter type supported.


This Markdown documentation provides a comprehensive overview of HubSpot's Lists API v3 filter system.  Always refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications.
