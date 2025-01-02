# HubSpot Lists API v3: List Filters Overview

This document details the structure and usage of filters within HubSpot's Lists API v3.  Filters define the criteria for including records in a list, supporting complex conditional logic.  The API uses a nested structure of `OR` and `AND` branches to build these conditions.

## API Call

List filters are defined as part of the list creation or update process.  The API endpoint typically uses a `POST` request to create a new list or a `PUT` request to update an existing one. The filter definition is included in the request body as a JSON object.

**Example Endpoint (POST):**

`/contacts/v3/lists`


## API Response

A successful API call will return a JSON response containing the newly created or updated list's details, including the filter definition if successful. An unsuccessful call will return an appropriate HTTP error code and an error message detailing the issue.


## Filter Structure

The core structure of a list filter is a nested JSON object.  The top-level element is `filterBranch`. This branch *must* be of type `"OR"` and contain one or more nested `AND` branches.  Each `AND` branch can contain multiple filters.

**Basic Structure:**

```json
{
  "filterBranch": {
    "filterBranchType": "OR",
    "filters": [],  // Empty for the top-level OR branch
    "filterBranches": [
      {
        "filterBranchType": "AND",
        "filters": [ /* Filter 1 */, /* Filter 2 */ ],
        "filterBranches": []
      },
      {
        "filterBranchType": "AND",
        "filters": [ /* Filter 3 */ ],
        "filterBranches": []
      }
    ]
  }
}
```

This structure represents the logical expression: `(Filter 1 AND Filter 2) OR (Filter 3)`

**Example 1:  First Name "John" OR Last Name NOT "Smith"**

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


## Filter Types

The `filterType` parameter specifies the type of filter.  Several types are supported, including `PROPERTY`, `UNIFIED_EVENTS`, `ASSOCIATION`, and others.  See the original text for a complete list.

## Property Filter Operations

The `PROPERTY` filter type uses an `operation` object to define the criteria. This object specifies `operationType` (e.g., `NUMBER`, `STRING`, `MULTISTRING`, `TIME_POINT`, `TIME_RANGED`), `operator` (e.g., `IS_EQUAL_TO`, `IS_GREATER_THAN`, `CONTAINS`), and `value` or `values` to compare against the property's value.  The `includeObjectsWithNoValueSet` parameter controls whether records with no value for the property are included.

## Time-Based Filters (`TIME_POINT` and `TIME_RANGED`)

These filter types allow for filtering based on timestamps.  They can use absolute dates, relative offsets (e.g., "in the last 7 days"), or comparisons to other properties. Refer to the original text for detailed examples.

## `UNIFIED_EVENTS` and `ASSOCIATION` Filter Branches

These specialized `AND` branches allow filtering based on events associated with a record or based on the properties of associated objects.  They have specific parameters (e.g., `eventTypeId`, `objectTypeId`).


## Legacy v1 Lists API

The original text mentions a legacy v1 API, but strongly advises migrating to the v3 API. The v1 API has limitations compared to v3.

## Conclusion

HubSpot's Lists API v3 provides a powerful and flexible way to define lists based on complex criteria.  Understanding the nested structure of `OR` and `AND` branches, the various filter types, and the property operation parameters is crucial for effectively using this API. Remember to always refer to the official HubSpot documentation for the most up-to-date information and API specifications.
