# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, providing comprehensive information on creating, managing, and retrieving lists.  The legacy v1 API is sunsetting on May 30th, 2025; this documentation focuses on the v3 replacement.

## Overview

Lists in HubSpot are collections of records (contacts, companies, deals, or custom objects) used for segmentation, filtering, and grouping.  The v3 API allows for creating, updating, and retrieving these lists. A list comprises a list definition (essential information) and list memberships (mappings between the list and records).

Three list processing types exist:

* **MANUAL:** Records are added or removed only via manual user actions or API calls. No background processing occurs.
* **DYNAMIC:**  List filters define membership. HubSpot automatically updates the list based on filter matches. Records are reevaluated upon changes.
* **SNAPSHOT:** Filters are applied upon creation; subsequent membership changes require manual intervention.


## API Endpoints

All endpoints below are prefixed with `/crm/v3/lists/`.  Replace `{listId}` and `{objectTypeId}` with the appropriate values.  `{object}` in some endpoints refers to the object type (e.g., `contacts`, `companies`). Object Type IDs can be found in the [full list of object type IDs](<Insert Link to Object Type IDs if available>).


### List Management

* **Create a List (POST /):**
    * **Request Body:**
        ```json
        {
          "name": "My static list",
          "objectTypeId": "0-1",  // Replace with your object type ID
          "processingType": "MANUAL"
        }
        ```
    * **Response:**  Returns the created list including its `listId`.

* **Retrieve Lists (GET):**
    * **By `listId` (GET /{listId}):** Retrieves a single list by its ID.  Add `includeFilters=true` to include filter definitions.
    * **By Name and Object Type (GET /object-type-id/{objectTypeId}/name/{listName}):** Retrieves a list by name and object type.
    * **Multiple Lists by `listId` (GET /?listIds={listId1}&listIds={listId2}...):** Retrieves multiple lists by their IDs. Add `includeFilters=true` to include filter definitions.

* **Search for a List (POST /search):**
    * **Request Body:**
        ```json
        {
          "query": "HubSpot",
          "processingTypes": ["MANUAL"]
        }
        ```
    * **Response:** Returns a list of lists matching the search criteria.

* **Update List Name (PUT /{listId}/update-list-name):**
    * **Query Parameters:** `listName` (new list name).
    * **Response:** The updated list. Add `includeFilters=true` to include filter definitions.

* **Update List Filter Branch (PUT /{listId}/update-list-filters):**
    * **Request Body:** The new filter branch definition.
    * **Response:** The updated list.

* **Delete a List (DELETE /{listId}):** Deletes a list. Restorable within 90 days.
* **Restore a List (PUT /{listId}/restore):** Restores a deleted list (within 90 days).


### List Membership Management

These endpoints apply only to `MANUAL` and `SNAPSHOT` lists.  `DYNAMIC` lists manage membership automatically.

* **Add Records (PUT /{listId}/memberships/add):**
    * **Request Body:** An array of `recordId`s to add.
* **Add Records from Another List (PUT /{listId}/memberships/add-from/{sourceListId}):**  Add records from one list to another (up to 100,000 at a time).
* **View Records (GET /{listId}/memberships):** Retrieves all list members, ordered by `recordId`.
* **Remove Records (PUT /{listId}/memberships/remove):**
    * **Request Body:** An array of `recordId`s to remove.
* **Remove All Records (DELETE /{listId}/memberships):** Removes all records from the list (but not the list itself).


### Migration from v1 to v3

* **Get List ID Mapping (GET /idmapping?legacyListId={legacyListId}):** Get a single v3 `listId` from a v1 `legacyListId`.
* **Get Multiple List ID Mappings (POST /idmapping):**  Get multiple v3 `listId`s from an array of v1 `legacyListId`s (limit 10,000).


### Retrieving Lists by Type

* **Get Static Lists (POST /search):** Search for lists with `processingTypes`: `["MANUAL", "SNAPSHOT"]`.
* **Get Dynamic Lists (POST /search):** Search for lists with `processingTypes`: `["DYNAMIC"]`.
* **Get a Batch of Lists by List ID (POST /search or GET /):** Use `listIds` parameter in the request body (POST) or query parameters (GET).  Use `includeListFilters=true` (GET only) for filter details.


### Retrieving List Members with Properties

* **Get Recent List Members with Properties:**
    1. Use `/crm/v3/lists/{listId}/memberships/join-order` (GET) to get member `recordId`s.
    2. Use `/crm/v3/objects/{object}/search` (POST) to fetch properties for those `recordId`s using the `values` parameter in the filter.

* **Get All/Recently Modified Records with Properties:** Use `/crm/v3/objects/{object}/search` (POST).  Filter by `lastmodifieddate` for recently modified records.


##  Error Handling

The API will return standard HTTP status codes to indicate success or failure.  Detailed error messages will be included in the response body.  Refer to the HubSpot API documentation for a complete list of error codes and their meanings.


## Rate Limits

The HubSpot API has rate limits. Be mindful of these limits to avoid exceeding them and causing your requests to fail.  Refer to the HubSpot API documentation for details on the rate limits and how to handle them.


This documentation provides a summary. Consult the official HubSpot API documentation for the most up-to-date and complete information.
