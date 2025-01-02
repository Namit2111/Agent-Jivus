# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, providing a concise overview and examples for each endpoint.  The legacy v1 API is sunsetting on May 30th, 2025; this documentation focuses on the v3 replacement.

## Overview

HubSpot Lists allow for record segmentation, filtering, and grouping based on object type (contacts, companies, deals, or custom objects). The v3 API enables creation, editing, and retrieval of lists.  A list comprises a definition (essential information) and memberships (mappings between the list and object records).

Three list processing types exist:

* **MANUAL:** Records are added or removed only via manual actions or API calls. No background processing.
* **DYNAMIC:**  List filters automatically manage memberships.  Records are added/removed based on filter matches; changes are reflected automatically.
* **SNAPSHOT:** Filters are defined at creation. After initial processing, only manual updates modify memberships.


## API Endpoints

All endpoints use the base URL: `/crm/v3/lists/`  Unless otherwise specified, requests should be made using JSON.

**Note:** `{listId}` refers to the HubSpot ILS (Internal List ID) and `{objectTypeId}` refers to the ID of the object type (e.g., "0-1" for contacts).  Refer to HubSpot's documentation for a full list of `objectTypeId` values.


### 1. Create a List

* **Method:** `POST`
* **Endpoint:** `/crm/v3/lists/`
* **Request Body:**
    * `name` (string, required): List name.
    * `objectTypeId` (string, required): Object type ID.
    * `processingType` (string, required):  `MANUAL`, `DYNAMIC`, or `SNAPSHOT`.
    * `filterBranch` (object, optional): Filter branch definition (for `DYNAMIC` and `SNAPSHOT` types).

* **Example Request:**

```json
{
  "name": "My static list",
  "objectTypeId": "0-1",
  "processingType": "MANUAL"
}
```

* **Response:**  The created list object, including the generated `listId`.


### 2. Retrieve Lists

Several methods exist for retrieving lists:

* **By Name:**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}`
* **By `listId` (Single List):**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v3/lists/{listId}`
    * **Query Parameter:** `includeFilters=true` (optional) to include filter definitions.
* **By `listId` (Multiple Lists):**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v3/lists`
    * **Query Parameter:** `listIds={listId1}&listIds={listId2}&...`  (e.g., `listIds=940&listIds=938`)
    * **Query Parameter:** `includeFilters=true` (optional) to include filter definitions.


### 3. Search for a List

* **Method:** `POST`
* **Endpoint:** `/crm/v3/lists/search`
* **Request Body:**
    * `query` (string, optional): Search term within list names.
    * `processingTypes` (array of strings, optional):  Filter by processing type (e.g., `["MANUAL", "DYNAMIC"]`).
    * `listIds` (array of strings, optional):  Filter by list IDs.
    * `offset` (integer, optional): Pagination offset.

* **Example Request:**

```json
{
  "query": "HubSpot",
  "processingTypes": ["MANUAL"]
}
```

* **Response:** Array of matching lists.


### 4. Update a List Name

* **Method:** `PUT`
* **Endpoint:** `/crm/v3/lists/{listId}/update-list-name`
* **Query Parameter:** `listName` (string, required): New list name.
* **Query Parameter:** `includeFilters=true` (optional) to include filter definitions.


### 5. Update List Filter Branch (Dynamic Lists Only)

* **Method:** `PUT`
* **Endpoint:** `/crm/v3/lists/{listId}/update-list-filters`
* **Request Body:**  New filter branch definition.


### 6. Delete and Restore a List

* **Delete:**
    * **Method:** `DELETE`
    * **Endpoint:** `/crm/v3/lists/{listId}`
* **Restore:**
    * **Method:** `PUT`
    * **Endpoint:** `/crm/v3/lists/{listId}/restore`  (Within 90 days of deletion)


### 7. Manage List Memberships (MANUAL & SNAPSHOT Lists Only)

* **Add Records:**
    * **Method:** `PUT`
    * **Endpoint:** `/crm/v3/lists/{listId}/memberships/add`
    * **Request Body:** Array of `recordId`s.
* **Add Records from Another List:**
    * **Method:** `PUT`
    * **Endpoint:** `/crm/v3/lists/{listId}/memberships/add-from/{sourceListId}` (limit 100,000 records)
* **View Records:**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v3/lists/{listId}/memberships`
* **Remove Records:**
    * **Method:** `PUT`
    * **Endpoint:** `/crm/v3/lists/{listId}/memberships/remove`
    * **Request Body:** Array of `recordId`s.
* **Remove All Records:**
    * **Method:** `DELETE`
    * **Endpoint:** `/crm/v3/lists/{listId}/memberships`


### 8. Migrate from v1 to v3 (Use before May 30th, 2025)

* **Single ID Mapping:**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v3/lists/idmapping?legacyListId={legacyListId}`
* **Batch ID Mapping:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v3/lists/idmapping`
    * **Request Body:** Array of `legacyListId`s (limit 10,000).


### 9.  Get Recent List Members with Properties

This involves a two-step process:

1. Get `recordId`s using `/crm/v3/lists/{listId}/memberships/join-order` (GET request)
2. Use the CRM search endpoint `/crm/v3/objects/{object}/search` (POST request) with the retrieved `recordId`s in the `values` parameter under `filterGroups`.  Specify the `properties` you want to retrieve.

### 10. Get All/Recently Modified Records with Properties

Use the CRM search endpoint `/crm/v3/objects/{object}/search` (POST request).  Specify desired `properties`. For recently modified, filter by `lastmodifieddate`.

## Error Handling

HubSpot's API returns standard HTTP status codes and JSON error responses. Consult the HubSpot API documentation for detailed error handling information.


This documentation provides a comprehensive yet concise overview of the HubSpot Lists API v3. Always refer to the official HubSpot API documentation for the most up-to-date information and details.
