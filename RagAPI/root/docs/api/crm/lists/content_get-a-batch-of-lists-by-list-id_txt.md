# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, providing comprehensive information on creating, managing, and querying lists within HubSpot.  The legacy v1 API is sunsetting on May 30th, 2025; this document focuses on the v3 replacement.

## Overview

HubSpot lists allow for record segmentation, filtering, and grouping.  They can contain contacts, companies, deals, or custom objects.  The v3 API offers functionality to create, update, retrieve, and delete lists, along with managing their memberships. A list comprises a definition (essential information) and memberships (mappings between the list and object records).

Three list processing types exist:

* **MANUAL:** Records are added or removed only through manual user actions or API calls. No background processing by HubSpot.  Ideal for static lists.
* **DYNAMIC:**  List filters define which records are members. HubSpot automatically updates the list based on filter matches.  Suitable for lists expected to change over time.
* **SNAPSHOT:** Filters are set at creation; post-initial processing, records are only added/removed manually.  Useful for a one-time snapshot based on specific criteria.


## API Endpoints

All endpoints are under the base URL `/crm/v3/lists/`.  Replace `{listId}` with the actual ILS list ID.  Object type IDs can be found in the [HubSpot Object Type IDs documentation](<link_to_object_type_ids_documentation_if_available>).


### 1. Create a List

**Endpoint:** `/crm/v3/lists/`

**Method:** `POST`

**Request Body:**

```json
{
  "name": "My static list",
  "objectTypeId": "0-1", // e.g., 0-1 for contacts
  "processingType": "MANUAL"  // or "DYNAMIC", "SNAPSHOT"
  // Optional: "filterBranch": { ... }  (For DYNAMIC and SNAPSHOT lists)
}
```

**Response:**  A JSON object containing the newly created list's details, including its `listId`.


### 2. Retrieve Lists

Several methods exist to retrieve lists:

* **By Name and Object Type:**

    **Endpoint:** `/crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}`
    **Method:** `GET`

* **By `listId` (Individual List):**

    **Endpoint:** `/crm/v3/lists/{listId}`
    **Method:** `GET`
    **Query Parameter:** `includeFilters=true` (optional, includes filter definitions)

* **By `listId` (Multiple Lists):**

    **Endpoint:** `/crm/v3/lists`
    **Method:** `GET`
    **Query Parameter:** `listIds={listId1}&listIds={listId2}&...`


### 3. Search for a List

**Endpoint:** `/crm/v3/lists/search`

**Method:** `POST`

**Request Body:**

```json
{
  "query": "HubSpot", // Optional search term in list name
  "processingTypes": ["MANUAL"] // Optional array of processing types to filter by
  // other search criteria can be added as needed
}
```

**Response:** A JSON object containing a list of matching lists.


### 4. Update a List

* **Update List Name:**

    **Endpoint:** `/crm/v3/lists/{listId}/update-list-name`
    **Method:** `PUT`
    **Query Parameter:** `listName={newListName}`
    **Query Parameter:** `includeFilters=true` (optional)


* **Update List Filter Branch (DYNAMIC lists only):**

    **Endpoint:** `/crm/v3/lists/{listId}/update-list-filters`
    **Method:** `PUT`
    **Request Body:**  The new filter branch definition.


### 5. Delete and Restore a List

* **Delete:**

    **Endpoint:** `/crm/v3/lists/{listId}`
    **Method:** `DELETE`

* **Restore (within 90 days):**

    **Endpoint:** `/crm/v3/lists/{listId}/restore`
    **Method:** `PUT`


### 6. Manage List Membership (MANUAL and SNAPSHOT lists only)

* **Add Records:**

    **Endpoint:** `/crm/v3/lists/{listId}/memberships/add`
    **Method:** `PUT`
    **Request Body:** An array of `recordId`s.

    **Endpoint (Add from another list):** `/crm/v3/lists/{listId}/memberships/add-from/{sourceListId}`
    **Method:** `PUT`
    **(Limit 100,000 records)**

* **View Records:**

    **Endpoint:** `/crm/v3/lists/{listId}/memberships`
    **Method:** `GET`

* **Remove Records:**

    **Endpoint:** `/crm/v3/lists/{listId}/memberships/remove`
    **Method:** `PUT`
    **Request Body:** An array of `recordId`s.

* **Remove All Records:**

    **Endpoint:** `/crm/v3/lists/{listId}/memberships`
    **Method:** `DELETE`  (Does not delete the list itself.)


### 7. Migration from v1 to v3

* **Get Static Lists (MANUAL & SNAPSHOT):**  Use `/crm/v3/lists/search` with `processingTypes: ["MANUAL", "SNAPSHOT"]` in the request body.
* **Get Dynamic Lists:** Use `/crm/v3/lists/search` with `processingTypes: ["DYNAMIC"]` in the request body.
* **Get Batch of Lists by `listId`:** Use `/crm/v3/lists/search` with a `listIds` array, or `/crm/v3/lists` with `includeFilters=true` and `listIds`.
* **Get Recent List Members with Properties:** Requires a `GET` to `/crm/v3/lists/{listId}/memberships/join-order` followed by a `POST` to `/crm/v3/objects/{object}/search`.
* **Get All/Recently Modified Records:** Use `/crm/v3/objects/{object}/search`. Filter by `lastmodifieddate` for recently modified records.
* **Migrate List IDs:**
    * **Single ID Mapping:** `GET /crm/v3/lists/idmapping?legacyListId=<legacyListId>`
    * **Batch ID Mapping:** `POST /crm/v3/lists/idmapping` (Body: array of legacy `listId`s; limit 10,000)


## Error Handling

The API will return standard HTTP status codes (e.g., 400 Bad Request, 404 Not Found, 500 Internal Server Error) along with JSON error responses providing details on the error.  Refer to the HubSpot API documentation for specific error codes and their meanings.


This documentation provides a summary. For the most up-to-date information and detailed specifications, always refer to the official HubSpot API documentation.
