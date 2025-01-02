# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, outlining its functionality, endpoints, and usage examples.  The legacy v1 API will be sunset on May 30th, 2025.  This documentation focuses on the v3 API.

## Overview

The HubSpot Lists API v3 allows you to manage lists within your HubSpot account. Lists are collections of records (contacts, companies, deals, or custom objects) used for segmentation, filtering, and grouping.  A list comprises a definition (essential information) and memberships (mappings between the list and records).

There are three list processing types:

* **MANUAL:** Records are added or removed manually via API calls or the HubSpot UI. No background processing.
* **DYNAMIC:**  Records are added or removed automatically based on specified filters.  HubSpot continuously evaluates records against these filters.
* **SNAPSHOT:** Filters are applied at creation.  After initial processing, records are only added or removed manually.


## API Endpoints

All endpoints are under the base URL: `/crm/v3/lists/`

Unless otherwise specified, requests should include your HubSpot API key in the header.

### 1. Create a List

* **Method:** `POST`
* **Endpoint:** `/crm/v3/lists/`
* **Request Body:**
    * `name` (string, required): The name of the list.
    * `objectTypeId` (string, required): The ID of the object type (e.g., `0-1` for contacts).  See the [full list of object type IDs](link_to_object_type_ids_if_available).
    * `processingType` (string, required):  One of `MANUAL`, `DYNAMIC`, or `SNAPSHOT`.
    * `filterBranch` (object, optional):  Filter definition for `DYNAMIC` and `SNAPSHOT` lists. (See configuring list filters and branches documentation)

* **Example Request Body (Manual List):**

```json
{
  "name": "My static list",
  "objectTypeId": "0-1",
  "processingType": "MANUAL"
}
```

* **Response:**  The created list object, including the `listId` (ILS list ID).


### 2. Retrieve Lists

Several methods exist to retrieve lists:

* **By Name and Object Type:**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}`
    * **Parameters:**
        * `{objectTypeId}`:  The object type ID.
        * `{listName}`: The list name.
* **By List ID:**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v3/lists/{listId}`
    * **Parameters:**
        * `{listId}`: The ILS list ID.
* **Multiple Lists by ID:**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v3/lists`
    * **Query Parameters:**
        * `listIds`: Comma-separated list of ILS list IDs (e.g., `?listIds=123,456`).
    * **Query parameter:** `includeFilters=true` to include filter definitions.

* **Example Request (By ID):** `GET /crm/v3/lists/123?includeFilters=true`


### 3. Search for a List

* **Method:** `POST`
* **Endpoint:** `/crm/v3/lists/search`
* **Request Body:**  Criteria for searching.  Examples:
    * `query` (string, optional): Search terms within the list name.
    * `processingTypes` (array of strings, optional):  Filter by processing type (e.g., `["MANUAL", "DYNAMIC"]`).
* **Example Request Body:**

```json
{
  "query": "HubSpot",
  "processingTypes": ["MANUAL"]
}
```

### 4. Update a List

* **Update List Name:**
    * **Method:** `PUT`
    * **Endpoint:** `/crm/v3/lists/{listId}/update-list-name`
    * **Query Parameters:**
        * `listName`: The new list name.  Must be unique.
    * **Query parameter:** `includeFilters=true` to include filter definitions.
* **Update List Filter Branch (DYNAMIC lists only):**
    * **Method:** `PUT`
    * **Endpoint:** `/crm/v3/lists/{listId}/update-list-filters`
    * **Request Body:** The updated filter branch definition.


### 5. Delete and Restore a List

* **Delete:**
    * **Method:** `DELETE`
    * **Endpoint:** `/crm/v3/lists/{listId}`
* **Restore:**
    * **Method:** `PUT`
    * **Endpoint:** `/crm/v3/lists/{listId}/restore`  (within 90 days of deletion)


### 6. Manage List Membership (MANUAL & SNAPSHOT lists only)

* **Add Records:**
    * **Method:** `PUT`
    * **Endpoint:** `/crm/v3/lists/{listId}/memberships/add`
    * **Request Body:** Array of `recordId`s to add.
* **Add Records from Another List:**
    * **Method:** `PUT`
    * **Endpoint:** `/crm/v3/lists/{listId}/memberships/add-from/{sourceListId}`
    * **Parameters:**
        * `{sourceListId}`: The ID of the source list.  (Limit of 100,000 records)
* **View Records:**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v3/lists/{listId}/memberships`
* **Delete Records:**
    * **Method:** `PUT`
    * **Endpoint:** `/crm/v3/lists/{listId}/memberships/remove`
    * **Request Body:** Array of `recordId`s to remove.
* **Delete All Records:**
    * **Method:** `DELETE`
    * **Endpoint:** `/crm/v3/lists/{listId}/memberships` (does not delete the list)


### 7. Migration from v1 to v3

* **Get Static Lists:** Use `/crm/v3/lists/search` with `processingTypes: ["MANUAL", "SNAPSHOT"]`.
* **Get Dynamic Lists:** Use `/crm/v3/lists/search` with `processingTypes: ["DYNAMIC"]`.
* **Get List IDs Mapping (v1 to v3):**
    * **Single Mapping:** `GET /crm/v3/lists/idmapping?legacyListId=<legacyListId>`
    * **Batch Mapping:** `POST /crm/v3/lists/idmapping` (request body: array of `legacyListId`s).


### 8. Get Recent List Members with Properties

1.  `GET /crm/v3/lists/{listId}/memberships/join-order` (get record IDs)
2.  `POST /crm/v3/objects/{object}/search` (search for records using the IDs obtained in step 1).


### 9. Get All/Recently Modified Records with Properties

Use `/crm/v3/objects/{object}/search`. Filter by `lastmodifieddate` for recently modified records.


## Error Handling

The API will return standard HTTP status codes to indicate success or failure.  Error responses will include detailed information about the error.


## Rate Limits

Refer to HubSpot's API documentation for rate limit information.


This documentation provides a comprehensive overview of the HubSpot Lists API v3. For detailed information on specific parameters, error codes, and advanced usage, refer to the official HubSpot API documentation.
