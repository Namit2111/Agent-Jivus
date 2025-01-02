# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, providing comprehensive information on creating, managing, and retrieving lists.  The legacy v1 API will be sunset on May 30th, 2025.  This document focuses on the v3 API.

## Overview

HubSpot lists are collections of records (contacts, companies, deals, or custom objects) used for segmentation, filtering, and grouping.  A list comprises a definition (essential information) and memberships (mappings between the list and records).  Three processing types exist:

* **MANUAL:** Records are added or removed manually via API or UI. No background processing.
* **DYNAMIC:**  Records are automatically added or removed based on specified filters. HubSpot manages memberships.
* **SNAPSHOT:** Filters are applied at creation; subsequent changes are manual.

## API Endpoints

All endpoints begin with `/crm/v3/lists/`.  Replace `{listId}` with the ILS list ID, `{objectTypeId}` with the object type ID (see [Object Type IDs](<link_to_object_type_ids_documentation>), and `{listName}` with the list name.

### 1. Create a List

* **Method:** `POST`
* **Endpoint:** `/`
* **Request Body:**
    * `name` (string, required): List name.
    * `objectTypeId` (string, required): Object type ID (e.g., "0-1" for contacts).
    * `processingType` (string, required):  `MANUAL`, `DYNAMIC`, or `SNAPSHOT`.
    * `filterBranch` (object, optional): Filter branch definition (for `DYNAMIC` and `SNAPSHOT` lists). See [Configuring List Filters and Branches](<link_to_filter_branch_documentation>).

* **Example Request Body (MANUAL):**

```json
{
  "name": "My static list",
  "objectTypeId": "0-1",
  "processingType": "MANUAL"
}
```

* **Response:**  Returns the created list, including the generated `listId`.


### 2. Retrieve Lists

Several methods exist to retrieve lists:

* **By Name:**
    * **Method:** `GET`
    * **Endpoint:** `/object-type-id/{objectTypeId}/name/{listName}`
* **By `listId` (single list):**
    * **Method:** `GET`
    * **Endpoint:** `{listId}`
* **By `listId` (multiple lists):**
    * **Method:** `GET`
    * **Endpoint:** `?listIds={listId1}&listIds={listId2}&...`
* **Include Filters:** Add `includeFilters=true` to any GET request to include filter definitions.


### 3. Search for a List

* **Method:** `POST`
* **Endpoint:** `/search`
* **Request Body:**
    * `query` (string, optional): Search term (in list name).
    * `processingTypes` (array of strings, optional):  Filter by processing type (e.g., `["MANUAL"]`).
    * `listIds` (array of strings, optional):  Filter by list IDs.
    * `offset` (integer, optional): Pagination offset.
    * `additionalProperties` (array of strings, optional):  Additional properties to retrieve (e.g., `["hs_is_public"]`).

* **Example Request Body:**

```json
{
  "query": "HubSpot",
  "processingTypes": ["MANUAL"]
}
```

* **Response:**  An array of matching lists.


### 4. Update a List

* **Update Name:**
    * **Method:** `PUT`
    * **Endpoint:** `{listId}/update-list-name`
    * **Query Parameters:** `listName` (string, required) - New list name. `includeFilters=true` (optional)
* **Update Filter Branch (DYNAMIC lists only):**
    * **Method:** `PUT`
    * **Endpoint:** `{listId}/update-list-filters`
    * **Request Body:**  The new filter branch definition.


### 5. Delete and Restore a List

* **Delete:**
    * **Method:** `DELETE`
    * **Endpoint:** `{listId}`
* **Restore:**
    * **Method:** `PUT`
    * **Endpoint:** `{listId}/restore` (within 90 days of deletion)


### 6. Manage List Membership (MANUAL and SNAPSHOT lists only)

* **Add Records:**
    * **Method:** `PUT`
    * **Endpoint:** `{listId}/memberships/add`
    * **Request Body:** Array of `recordId`s.
* **Add Records from Another List:**
    * **Method:** `PUT`
    * **Endpoint:** `{listId}/memberships/add-from/{sourceListId}`
    * **Limit:** 100,000 records at a time.
* **View Records:**
    * **Method:** `GET`
    * **Endpoint:** `{listId}/memberships`
* **Remove Records:**
    * **Method:** `PUT`
    * **Endpoint:** `{listId}/memberships/remove`
    * **Request Body:** Array of `recordId`s.
* **Remove All Records:**
    * **Method:** `DELETE`
    * **Endpoint:** `{listId}/memberships` (removes members, not the list itself).


### 7. Migrate from v1 to v3

* **Get v3 `listId` from v1 `legacyListId` (single):**
    * **Method:** `GET`
    * **Endpoint:** `/idmapping?legacyListId={legacyListId}`
* **Get v3 `listId` from v1 `legacyListId` (batch):**
    * **Method:** `POST`
    * **Endpoint:** `/idmapping`
    * **Request Body:** Array of `legacyListId`s (limit: 10,000).  *(Note: this endpoint will be sunset on May 30th, 2025)*


### 8. Get Lists by Processing Type (Search Endpoint)

Use the `/search` endpoint with the `processingTypes` parameter to retrieve lists based on type:

* **Static Lists (MANUAL & SNAPSHOT):**  `processingTypes`: `["MANUAL", "SNAPSHOT"]`
* **Dynamic Lists:** `processingTypes`: `["DYNAMIC"]`


### 9. Get Recent List Members with Properties

1. Get `recordId`s via `GET /crm/v3/lists/{listId}/memberships/join-order`.
2. Use a `POST /crm/v3/objects/{object}/search` request to fetch properties for those `recordId`s.


### 10. Get All/Recently Modified Records with Properties

Use `POST /crm/v3/objects/{object}/search`. For recently modified, filter by `lastmodifieddate`.


##  Error Handling

The API will return standard HTTP status codes to indicate success or failure. Error responses will contain details about the issue.


## Rate Limits

Consult HubSpot's API documentation for current rate limits.


This documentation provides a high-level overview.  Refer to the official HubSpot API documentation for detailed specifications and the most up-to-date information.  Remember to replace placeholder values like `{listId}` and `{objectTypeId}` with your actual values.
