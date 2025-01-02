# HubSpot Lists API v3 Documentation

This document provides a comprehensive guide to the HubSpot Lists API v3.  The legacy v1 API will be sunset on May 30th, 2025.  This documentation focuses on the v3 API and provides migration guidance.

## Overview

HubSpot Lists allow for the segmentation, filtering, and grouping of records (contacts, companies, deals, or custom objects) based on specific criteria. The v3 Lists API enables the creation, manipulation, and retrieval of these lists.  A list comprises two key components:

* **List Definition:** Stores metadata about the list (name, object type, processing type, etc.).
* **List Memberships:**  Mappings between the list and the actual records it contains.

Three processing types exist:

* **MANUAL:** Records are added or removed only through manual user actions or API calls.
* **DYNAMIC:**  List filters define membership; HubSpot automatically updates the list based on these filters.
* **SNAPSHOT:** Filters are applied at creation; subsequent changes require manual updates.

## API Endpoints and Usage

All endpoints below are prefixed with `/crm/v3/lists/`.  Replace placeholders like `{listId}` and `{objectTypeId}` with actual values.  Object type IDs can be found in the [HubSpot Object Type ID documentation](link_to_object_type_id_doc_here -  replace with actual link if available).


### 1. Create a List

* **Method:** `POST`
* **Endpoint:** `/`
* **Request Body:**
    ```json
    {
      "name": "My static list",
      "objectTypeId": "0-1",  //Example: Contacts
      "processingType": "MANUAL"
    }
    ```
* **Response:**  A JSON object containing the newly created list's details, including its `listId`.

### 2. Retrieve Lists

Several methods exist to retrieve lists:

* **By Name and Object Type:**
    * **Method:** `GET`
    * **Endpoint:** `/object-type-id/{objectTypeId}/name/{listName}`
* **By `listId` (Individual List):**
    * **Method:** `GET`
    * **Endpoint:** `/{listId}`
* **By `listId` (Multiple Lists):**
    * **Method:** `GET`
    * **Endpoint:** `/` (with query parameter `listIds=listId1&listIds=listId2...`)
    * Example: `/crm/v3/lists/?listIds=123&listIds=456`
* **Include Filters:** Add the query parameter `includeFilters=true` to any GET request to retrieve filter definitions.


### 3. Search for a List

* **Method:** `POST`
* **Endpoint:** `/search`
* **Request Body:**
    ```json
    {
      "query": "HubSpot",
      "processingTypes": ["MANUAL"]
    }
    ```
* **Response:** A JSON array of lists matching the search criteria.


### 4. Update a List

* **Update List Name:**
    * **Method:** `PUT`
    * **Endpoint:** `/{listId}/update-list-name`
    * **Query Parameter:** `listName={newListName}`

* **Update List Filters (DYNAMIC lists only):**
    * **Method:** `PUT`
    * **Endpoint:** `/{listId}/update-list-filters`
    * **Request Body:** The new filter branch definition.


### 5. Delete and Restore a List

* **Delete:**
    * **Method:** `DELETE`
    * **Endpoint:** `/{listId}`
* **Restore:** (within 90 days of deletion)
    * **Method:** `PUT`
    * **Endpoint:** `/{listId}/restore`


### 6. Manage List Membership (MANUAL & SNAPSHOT lists only)

* **Add Records:**
    * **Method:** `PUT`
    * **Endpoint:** `/{listId}/memberships/add`
    * **Request Body:** An array of `recordId`s.
* **Add Records from Another List:**
    * **Method:** `PUT`
    * **Endpoint:** `/{listId}/memberships/add-from/{sourceListId}`
    * **Limit:** 100,000 records per request.
* **View Records:**
    * **Method:** `GET`
    * **Endpoint:** `/{listId}/memberships`
* **Remove Records:**
    * **Method:** `PUT`
    * **Endpoint:** `/{listId}/memberships/remove`
    * **Request Body:** An array of `recordId`s.
* **Remove All Records:**
    * **Method:** `DELETE`
    * **Endpoint:** `/{listId}/memberships` (This does *not* delete the list itself.)


### 7. Migration from v1 to v3

HubSpot provides endpoints to migrate from the legacy v1 API.  These will be sunset May 30th, 2025.

* **Get Static Lists (MANUAL & SNAPSHOT):** Use the `/search` endpoint with `processingTypes=["MANUAL", "SNAPSHOT"]`.
* **Get Dynamic Lists:** Use the `/search` endpoint with `processingTypes=["DYNAMIC"]`.
* **Get a Batch of Lists by `listId`:** Use the `/search` endpoint with the `listIds` parameter.  To include filters, use the GET endpoint `/` with `includeFilters=true` and `listIds`.
* **Get Recent List Members with Properties:** First, get `recordId`s using `/memberships/join-order`, then use the CRM object search endpoint (`/crm/v3/objects/{object}/search`) with these IDs.
* **Get All/Recently Modified Records:** Use the CRM object search endpoint (`/crm/v3/objects/{object}/search`). Filter by `lastmodifieddate` for recently modified records.
* **Migrate List IDs:**
    * **Single ID:** `GET /crm/v3/lists/idmapping?legacyListId=<legacyListId>`
    * **Multiple IDs:** `POST /crm/v3/lists/idmapping` (body: array of `legacyListId`s, limit 10,000)


## Error Handling

The API returns standard HTTP status codes.  Error responses will contain JSON objects with details about the error.


## Rate Limits

Consult the HubSpot API documentation for current rate limits.


This documentation provides a concise overview. Refer to the official HubSpot API documentation for the most up-to-date information, detailed specifications, and complete examples.
