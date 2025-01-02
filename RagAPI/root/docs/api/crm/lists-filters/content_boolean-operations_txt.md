# HubSpot Lists API: Filter Documentation

This document details the structure and usage of filters within the HubSpot Lists API (v3).  The legacy v1 API is deprecated and should not be used for new integrations.

## Overview

List filters define the criteria for including records in a HubSpot list.  They use a hierarchical structure of branches with `AND` and `OR` logic.  The core components are:

* **`filterBranch`:** The root-level structure containing the overall filter logic.
* **`filterBranchType`:** Defines the logical operation (`OR` or `AND`) of a branch.
* **`filterType`:** Specifies the type of filter condition applied (e.g., `PROPERTY`, `EVENT`, `FORM_SUBMISSION`).
* **`filters`:** An array of individual filter conditions within a branch.
* **`filterBranches`:** An array of nested filter branches, allowing for complex conditional logic.


## Filter Structure

All filter definitions must begin with a root `OR` filter branch. This branch must contain one or more nested `AND` filter branches.

**Example (JSON):**

```json
{
  "filterBranch": {
    "filterBranches": [
      {
        "filterBranches": [],
        "filterBranchType": "AND",
        "filters": [ /* filters here */ ]
      },
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

This structure ensures proper rendering in the HubSpot UI.  The root `OR` acts as a parent, with `AND` branches representing child filter groups.

**Example:  Contacts with first name "John" OR those without last name "Smith"**

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

**Example: Contacts with first name "John" AND last name "Smith"**

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

* **`OR`:** Accepts a record if *any* of its nested `AND` branches are met.  It cannot contain direct filters; only nested branches.

* **`AND`:** Accepts a record only if *all* of its filters and nested branches are met.  It can contain filters and nested `UNIFIED_EVENTS` or `ASSOCIATION` branches.

* **`UNIFIED_EVENTS`:** Filters based on HubSpot unified events.  Must be nested within an `AND` branch.  Requires `eventTypeId` and `operator` (e.g., `HAS_COMPLETED`, `HAS_NOT_COMPLETED`).

* **`ASSOCIATION`:** Filters based on associated objects (e.g., contacts associated with deals). Must be nested within an `AND` branch.  Requires `objectTypeId`, `operator` (e.g., `IN_LIST`), `associationTypeId`, and `associationCategory`.


## Filter Types

The `filterType` parameter determines the type of condition.  Common types include:

* `PROPERTY`: Filters based on a property's value.  Requires an `operation` object (see below).
* `EVENT`: Filters based on whether a contact has a specific event.
* `FORM_SUBMISSION`: Filters based on form submissions.
* `IN_LIST`: Filters based on membership in other lists.
* and many others...


## Property Filter Operations

The `operation` object within a `PROPERTY` filter specifies the comparison.  Key fields:

* `operationType`:  The type of operation (e.g., `NUMBER`, `STRING`, `MULTISTRING`, `TIME_POINT`, `TIME_RANGED`).
* `operator`: The comparison operator (e.g., `IS_EQUAL_TO`, `CONTAINS`, `IS_BETWEEN`).
* `value` or `values`: The value(s) to compare against.
* `includeObjectsWithNoValueSet`:  Whether to include records with no value for the property (true/false).


## Time-Based Filters (`TIME_POINT` and `TIME_RANGED`)

These filter types are powerful for date-related comparisons.  Examples:

* **`Is equal to date`:** Uses `TIME_RANGED` with inclusive bounds set to a specific date.
* **`In Last X Number of Days`:** Uses `TIME_RANGED` with `lowerBoundTimePoint` set to a relative offset from today and `upperBoundTimePoint` set to the current time.
* **`In Next X Number of Days`:** Similar to "In Last X Days," but the offset is positive.
* **`Updated or Not Updated in the Last X Days`:** Uses `TIME_RANGED` with `propertyParser` set to `UPDATED_AT`.
* **`Is After Date`:** Uses `TIME_POINT` to check if a property is after a specific date.
* **`Is Relative to Today`:** Uses `TIME_POINT` with a relative offset from today.
* **`Is Before or After another property`:** Uses `TIME_POINT` to compare against another property's value or last updated time.


## Refine By Operations

These operations further refine the dataset before filter evaluation:

* **`pruningRefineBy`:** Limits the dataset to a specific time range (absolute or relative).
* **`coalescingRefineBy`:**  Specifies the minimum/maximum number of times a record must meet the filter criteria.


## API Call Example (using `curl`)

The exact API call will depend on your specific HubSpot API key and the endpoint for creating or updating lists.  However, the request body would contain the JSON filter structure defined above.  Remember to replace placeholders like `<YOUR_API_KEY>` and the list ID.


```bash
curl -X POST \
  https://api.hubapi.com/crm/v3/objects/lists/<listId>/filters \
  -H 'Authorization: Bearer <YOUR_API_KEY>' \
  -H 'Content-Type: application/json' \
  -d '{
    "filterBranch": {
      "filterBranchType": "OR",
      // ... your filter structure ...
    }
  }'
```


##  Legacy v1 API (Deprecated)

The v1 API is significantly simpler but lacks the features and flexibility of v3. Its use is strongly discouraged.


This documentation provides a comprehensive overview. For detailed information on specific filter types, operators, and parameters, refer to the official HubSpot API documentation.
