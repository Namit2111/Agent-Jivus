# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, providing comprehensive information on creating, managing, and querying lists within HubSpot.  The legacy v1 API will be sunset on May 30th, 2025.  This guide focuses on the v3 API and includes migration information from v1.

## Overview

HubSpot lists are collections of records (contacts, companies, deals, or custom objects) used for segmentation, filtering, and grouping.  The v3 API allows for creating, editing, and retrieving these lists.  A list consists of a list definition (essential information) and list memberships (mappings between the list and object records).

There are three list processing types:

* **MANUAL:** Records are added or removed only via manual actions or API calls.  No background processing.
* **DYNAMIC:**  List filters determine membership. HubSpot automatically updates the list based on filter matches.
* **SNAPSHOT:** Filters are applied at creation. After initial processing, only manual updates are allowed.


## API Endpoints

All endpoints are under the base URL `/crm/v3/lists/`.  Replace `{listId}` with the ILS list ID and `{objectTypeId}` with the appropriate object type ID (see [Object Type IDs](<link_to_object_type_ids_documentation>)).  HTTP methods are specified for each operation.

### List Management

* **Create a List (POST /crm/v3/lists/)**
    * **Request Body:**
        * `name` (string, required): List name.
        * `objectTypeId` (string, required):  ID of the object type (e.g., "0-1" for contacts).
        * `processingType` (string, required):  "MANUAL", "DYNAMIC", or "SNAPSHOT".
        * `filterBranch` (object, optional): Filter definition for DYNAMIC and SNAPSHOT lists.  See [Configuring List Filters and Branches](<link_to_filter_branch_documentation>).
    * **Example Request Body (MANUAL):**
    ```json
    {
      "name": "My static list",
      "objectTypeId": "0-1",
      "processingType": "MANUAL"
    }
    ```
    * **Response:**  The created list object, including the `listId`.

* **Retrieve Lists (GET)**
    * **By Name (GET /crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}):** Retrieves a list by name and object type.
    * **By List ID (GET /crm/v3/lists/{listId}):** Retrieves a list by its `listId`.
    * **Multiple Lists by ID (GET /crm/v3/lists?listIds={listId1}&listIds={listId2}...):** Retrieves multiple lists using `listIds` query parameter.
    * `includeFilters=true` (query parameter, optional): Include filter definitions in the response.

* **Search for a List (POST /crm/v3/lists/search)**
    * **Request Body:**
        * `query` (string, optional): Search term (in list name).
        * `processingTypes` (array of strings, optional): Filter by processing type (e.g., `["MANUAL"]`).
    * **Example Request Body:**
    ```json
    {
      "query": "HubSpot",
      "processingTypes": ["MANUAL"]
    }
    ```
    * **Response:** Array of matching lists.

* **Update List Name (PUT /crm/v3/lists/{listId}/update-list-name?listName={newListName})**
    * Updates the list name.  `listName` must be unique.
    * `includeFilters=true` (query parameter, optional): Include filter definitions in the response.

* **Update List Filter Branch (PUT /crm/v3/lists/{listId}/update-list-filters)**
    * Updates the filter branch of a DYNAMIC list.
    * **Request Body:** The new filter branch definition.

* **Delete a List (DELETE /crm/v3/lists/{listId})**
    * Deletes a list.  Restorable within 90 days.

* **Restore a List (PUT /crm/v3/lists/{listId}/restore)**
    * Restores a deleted list (within 90 days).


### List Memberships (MANUAL and SNAPSHOT only)

* **Add Records (PUT /crm/v3/lists/{listId}/memberships/add)**
    * **Request Body:** Array of `recordId`s to add.

* **Add Records from Another List (PUT /crm/v3/lists/{listId}/memberships/add-from/{sourceListId})**
    * Adds records from `sourceListId` to `listId`.  100,000 record limit per request.

* **View Records (GET /crm/v3/lists/{listId}/memberships)**
    * Retrieves all list members, ordered by `recordId`.

* **Remove Records (PUT /crm/v3/lists/{listId}/memberships/remove)**
    * **Request Body:** Array of `recordId`s to remove.

* **Remove All Records (DELETE /crm/v3/lists/{listId}/memberships)**
    * Removes all records from the list (but not the list itself).


### Migration from v1 to v3

* **Get List ID Mapping (GET /crm/v3/lists/idmapping?legacyListId={legacyListId})**
    * Gets the v3 `listId` from a v1 `legacyListId`.

* **Get Multiple List ID Mappings (POST /crm/v3/lists/idmapping)**
    * **Request Body:** Array of `legacyListId`s.
    * **Response:**  Mapping of `legacyListId`s to `listId`s.  Includes `missingLegacyListIds` if any IDs are not found.  10,000 entry limit.


###  Retrieving Lists with Properties (requires additional API calls)

* **Get Recent List Members with Properties:**
    1. Use `/crm/v3/lists/{listId}/memberships/join-order` (GET) to get record IDs.
    2. Use `/crm/v3/objects/{object}/search` (POST) with the record IDs to retrieve properties.  Example request body shown below.

* **Get All/Recently Modified Records with Properties:** Use `/crm/v3/objects/{object}/search` (POST). Filter by `lastmodifieddate` for recently modified records.  Example request bodies below.

**Example Request Body for `/crm/v3/objects/{object}/search` (Retrieving Properties):**

```json
{
  "properties": [
    "firstname",
    "lastname",
    "email",
    "hs_object_id",
    "createdate",
    "lastmodifieddate",
    "hs_all_accessible_team_ids"
  ],
  "filterGroups": [
    {
      "filters": [
        {
          "propertyName": "hs_object_id",
          "operator": "IN",
          "values": ["808431983", "802539655", "101"]
        }
      ]
    }
  ]
}
```

**Example Request Body for `/crm/v3/objects/{object}/search` (Recently Modified Contacts):**

```json
{
  "properties": [
    "firstname",
    "lastname",
    "email",
    "hs_object_id",
    "createdate",
    "lastmodifieddate"
  ],
  "filterGroups": [
    {
      "filters": [
        {
          "propertyName": "lastmodifieddate",
          "operator": "GT",
          "value": "2024-02-22"
        }
      ]
    }
  ]
}
```


This documentation provides a comprehensive overview of the HubSpot Lists API v3. Remember to consult the official HubSpot API documentation for the most up-to-date information and details.  Replace placeholder links like `<link_to_object_type_ids_documentation>` with actual links when available.
