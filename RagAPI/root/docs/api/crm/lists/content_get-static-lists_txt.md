# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, outlining its functionality, endpoints, and usage examples.  The legacy v1 API will be sunset on May 30th, 2025.  This document focuses on the v3 API.

## Overview

The HubSpot Lists API v3 allows you to create, manage, and retrieve lists of records within your HubSpot account. Lists are collections of records of the same object type (e.g., contacts, companies, deals) used for segmentation and filtering. A list comprises a definition (essential list information) and memberships (mappings between the list and records).

Three processing types exist:

* **MANUAL:** Records are added or removed only through manual actions or API calls.  No background processing occurs.
* **DYNAMIC:**  List filters are used to automatically include or exclude records based on criteria. HubSpot's system manages memberships dynamically.
* **SNAPSHOT:** Filters are applied at creation. After initial processing, records are added or removed manually.

## API Endpoints

All endpoints below are prefixed with `/crm/v3/lists/`.  Replace `{listId}` with the ILS list ID and `{objectTypeId}` with the appropriate object type ID (see HubSpot's documentation for a full list).

**1. Create a List:**

* **Method:** `POST`
* **Endpoint:** `/`
* **Request Body:**
    * `name` (string, required): List name.
    * `objectTypeId` (string, required): ID of the object type (e.g., "0-1" for contacts).
    * `processingType` (string, required):  "MANUAL", "DYNAMIC", or "SNAPSHOT".
    * `filterBranch` (object, optional): Filter definition for DYNAMIC and SNAPSHOT lists. (See "Configuring List Filters and Branches" in HubSpot's documentation).
* **Response:**  The created list's details, including the `listId`.

```json
// Example Request Body
{
  "name": "My Static List",
  "objectTypeId": "0-1",
  "processingType": "MANUAL"
}
```

**2. Retrieve Lists:**

* **By List ID:**
    * **Method:** `GET`
    * **Endpoint:** `/{listId}`
    * **Query Parameters:** `includeFilters=true` (optional) to include filter definitions.
* **By Name and Object Type:**
    * **Method:** `GET`
    * **Endpoint:** `object-type-id/{objectTypeId}/name/{listName}`
* **Multiple Lists by ID:**
    * **Method:** `GET`
    * **Endpoint:** `/`
    * **Query Parameters:** `listIds={listId1}&listIds={listId2}&...`  (e.g., `listIds=940&listIds=938`) and `includeFilters=true` (optional).

**3. Search for a List:**

* **Method:** `POST`
* **Endpoint:** `/search`
* **Request Body:**
    * `query` (string, optional): Search term for list names.
    * `processingTypes` (array of strings, optional): Filter by processing type (e.g., `["MANUAL", "DYNAMIC"]`).
    * `listIds` (array of strings, optional): Search by a list of list IDs.
    * `additionalProperties` (array of strings, optional): Include additional properties such as `hs_is_public`, `hs_is_read_only`, etc.

```json
// Example Request Body
{
  "query": "HubSpot",
  "processingTypes": ["MANUAL"]
}
```

**4. Update a List Name:**

* **Method:** `PUT`
* **Endpoint:** `/{listId}/update-list-name`
* **Query Parameters:** `listName={newListName}` and `includeFilters=true` (optional).


**5. Update List Filter Branch (DYNAMIC lists only):**

* **Method:** `PUT`
* **Endpoint:** `/{listId}/update-list-filters`
* **Request Body:** The new filter branch definition.

**6. Delete and Restore a List:**

* **Delete:**
    * **Method:** `DELETE`
    * **Endpoint:** `/{listId}`
* **Restore:**
    * **Method:** `PUT`
    * **Endpoint:** `/{listId}/restore`  (Only within 90 days of deletion).


**7. Manage List Memberships (MANUAL and SNAPSHOT lists only):**

* **Add Records:**
    * **Method:** `PUT`
    * **Endpoint:** `/{listId}/memberships/add`
    * **Request Body:** Array of `recordId`s.
* **Add Records from Another List:**
    * **Method:** `PUT`
    * **Endpoint:** `/{listId}/memberships/add-from/{sourceListId}`
* **View Records:**
    * **Method:** `GET`
    * **Endpoint:** `/{listId}/memberships`
* **Remove Records:**
    * **Method:** `PUT`
    * **Endpoint:** `/{listId}/memberships/remove`
    * **Request Body:** Array of `recordId`s.
* **Remove All Records:**
    * **Method:** `DELETE`
    * **Endpoint:** `/{listId}/memberships`


**8. Migration from v1 to v3:**

* **Get v3 List ID from v1 List ID (single):**
    * **Method:** `GET`
    * **Endpoint:** `/idmapping`
    * **Query Parameters:** `legacyListId={legacyListId}`
* **Get v3 List IDs from v1 List IDs (batch):**
    * **Method:** `POST`
    * **Endpoint:** `/idmapping`
    * **Request Body:** Array of `legacyListId`s (maximum 10,000).


**9. Get Recent List Members with Properties:**

1.  **GET `/crm/v3/lists/{listId}/memberships/join-order`** to get the record IDs.
2.  **POST `/crm/v3/objects/{object}/search`** using the obtained record IDs in the `values` parameter under `filterGroups`.  Specify properties to retrieve.


**10. Get All/Recently Modified Records with Properties:**

* Use the CRM search endpoint:  `POST /crm/v3/objects/{object}/search` . Filter by `lastmodifieddate` for recently modified records.


##  Error Handling

HubSpot's API returns standard HTTP status codes to indicate success or failure.  Refer to the HubSpot API documentation for details on specific error codes and their meanings.

## Rate Limits

Be mindful of HubSpot's API rate limits to avoid exceeding allowed requests per time period.  Check the HubSpot documentation for current rate limit information.


This documentation provides a concise overview.  Always consult the official HubSpot API documentation for the most up-to-date information, including detailed descriptions of request parameters, response structures, and error handling.
