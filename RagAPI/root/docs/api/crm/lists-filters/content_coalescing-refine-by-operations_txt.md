# HubSpot Lists API v3: Filter Documentation

This document details the structure and usage of filters within HubSpot's Lists API v3.  These filters determine which records are included in a list, using conditional logic based on properties and events.  The API uses a `PASS`/`FAIL` system; a record must pass all filters to be included.

## API Endpoint

While the specific endpoint isn't explicitly provided in the source text, the context implies a `POST` request to create or update a list, including its filter definition within the request body.  This would likely be something similar to:

`/crm/v3/objects/lists/{listId}/filters` (Hypothetical endpoint)


## Filter Structure

Filters are organized hierarchically into branches using `AND` and `OR` logic. The structure *must* start with a root-level `OR` branch containing one or more nested `AND` branches.  This structure is enforced by the API to ensure compatibility with the HubSpot UI.

**Basic Structure (JSON):**

```json
{
  "filterBranch": {
    "filterBranches": [
      {
        "filterBranches": [],
        "filterBranchType": "AND",
        "filters": [ /* Array of filters */ ]
      },
      {
        "filterBranches": [],
        "filterBranchType": "AND",
        "filters": [ /* Array of filters */ ]
      }
    ],
    "filterBranchType": "OR",
    "filters": []
  }
}
```

**Example 1: First name "John" OR last name not "Smith"**

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

**Example 2: First name "John" AND last name "Smith"**

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


## Filter Branch Types

* **`OR`:** Accepts a record if *any* of its nested `AND` branches accept it.  Must have at least one nested `AND` branch and cannot have any direct filters.

* **`AND`:** Accepts a record only if *all* of its filters and nested branches accept it. Can have zero or more filters and zero or more nested `UNIFIED_EVENTS` or `ASSOCIATION` branches.

* **`UNIFIED_EVENTS`:** Filters based on events.  Must be nested within an `AND` branch. Requires `eventTypeId` and `operator` (e.g., `HAS_COMPLETED`, `HAS_NOT_COMPLETED`).

* **`ASSOCIATION`:** Filters based on associated objects. Must be nested within an `AND` branch. Requires `objectTypeId`, `operator` (e.g., `IN_LIST`), `associationTypeId`, and `associationCategory`.


## Filter Types

The `filterType` parameter specifies the type of filter.  Common types include:

* `PROPERTY`: Filters based on a record's property value.  Requires an `operation` object defining the operator and value(s).
* `UNIFIED_EVENTS`
* `ASSOCIATION`
* `ADS_TIME`, `ADS_SEARCH`, `CTA`, `EMAIL_EVENT`, `EVENT`, `FORM_SUBMISSION`, `FORM_SUBMISSION_ON_PAGE`, `IN_LIST`, `PAGE_VIEW`, `PRIVACY`, `SURVEY_MONKEY`, `SURVEY_MONKEY_VALUE`, `WEBINAR`, `INTEGRATION_EVENT`  (Other filter types with specific parameters)


## Property Filter Operations

The `operation` object within a `PROPERTY` filter defines the filtering logic:

* `operationType`:  The type of operation (e.g., `NUMBER`, `STRING`, `MULTISTRING`, `TIME_POINT`, `TIME_RANGED`).
* `operator`: The specific operator (e.g., `IS_EQUAL_TO`, `IS_GREATER_THAN`, `CONTAINS`, `IS_BETWEEN`).
* `value` / `values`: The value(s) to compare against.
* `includeObjectsWithNoValueSet`:  Whether to include records without a value for the property (boolean, defaults to `false`).


## Time-Based Filters (`TIME_POINT`, `TIME_RANGED`)

These filter types allow for flexible date/time comparisons:

* **`TIME_POINT`:** Compares a single point in time.  Can use absolute dates, relative dates (e.g., "3 days ago"), or comparisons to other properties.

* **`TIME_RANGED`:**  Compares a time range.  Supports absolute and relative ranges.


## Refine By Operations

* **`pruningRefineBy`:** Refines the dataset to a specific timeframe *before* filter evaluation.  Supports absolute and relative comparisons and ranges.

* **`coalescingRefineBy`:**  Applies after filter evaluation, checking if a record passed the filter a certain number of times (`NUM_OCCURRENCES`).


## Legacy v1 Lists API

The v1 API is deprecated. It offers similar functionality but with a slightly different syntax and fewer options.  It's strongly recommended to migrate to the v3 API.


This documentation provides a comprehensive overview of HubSpot's Lists API v3 filtering capabilities.  Refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications for each parameter.
