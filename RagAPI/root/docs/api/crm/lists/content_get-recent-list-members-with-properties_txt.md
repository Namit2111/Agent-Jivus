# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, providing information on creating, managing, and retrieving lists of contacts, companies, deals, or custom objects.  The legacy v1 API is sunsetting on May 30th, 2025;  migration guidance is included.

## Overview

HubSpot lists are collections of records of the same object type, useful for segmentation, filtering, and grouping.  The v3 API offers functionality to create, edit, and fetch these lists.  A list comprises a *list definition* (essential information) and *list memberships* (mappings between the list and object records).

There are three list processing types:

* **MANUAL:** Records are added or removed only via manual actions or API calls. No background processing by HubSpot.
* **DYNAMIC:**  List filters define membership. HubSpot automatically updates the list based on filter matches. Records are reevaluated whenever they change.
* **SNAPSHOT:** List filters are set at creation.  After initial processing, updates are manual only.


## API Endpoints

All endpoints begin with `/crm/v3/lists/`.  Replace `{listId}` with the ILS (HubSpot Internal List ID) and `{objectTypeId}` with the ID corresponding to the object type (e.g., "0-1" for contacts).  See the [HubSpot Object Type IDs documentation](<Insert Link Here -  replace with actual link if available>) for a full list of object type IDs.


### 1. Create a List

**Method:** `POST`

**Endpoint:** `/crm/v3/lists/`

**Request Body:**

```json
{
  "name": "My static list",
  "objectTypeId": "0-1",
  "processingType": "MANUAL" 
  //Optional: "filterBranch": { ... } for DYNAMIC and SNAPSHOT lists
}
```

**Response:**  A JSON object containing the created list's details, including `listId`.


### 2. Retrieve Lists

Several methods exist to retrieve lists:

* **By Name and Object Type:**

  **Method:** `GET`
  **Endpoint:** `/crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}`

* **By `listId` (Single List):**

  **Method:** `GET`
  **Endpoint:** `/crm/v3/lists/{listId}`

* **By `listId` (Multiple Lists):**

  **Method:** `GET`
  **Endpoint:** `/crm/v3/lists?listIds={listId1}&listIds={listId2}&...`

* **Search:** (See section 4)


**Query Parameter:** `includeFilters=true` (returns list filter definitions)


### 3. Search for a List

**Method:** `POST`

**Endpoint:** `/crm/v3/lists/search`

**Request Body:**

```json
{
  "query": "HubSpot", // Search term in list name
  "processingTypes": ["MANUAL"] //Filter by processing type(s)
  // other search parameters as needed.
}
```

**Response:** JSON array of matching lists.


### 4. Update a List

* **Update List Name:**

  **Method:** `PUT`
  **Endpoint:** `/crm/v3/lists/{listId}/update-list-name`
  **Query Parameter:** `listName={newName}`
  **Query Parameter:** `includeFilters=true` (optional, returns list filter definitions)

* **Update Filter Branch (DYNAMIC lists only):**

  **Method:** `PUT`
  **Endpoint:** `/crm/v3/lists/{listId}/update-list-filters`
  **Request Body:** The updated filter branch definition.


### 5. Delete and Restore a List

* **Delete:**

  **Method:** `DELETE`
  **Endpoint:** `/crm/v3/lists/{listId}`

* **Restore (within 90 days of deletion):**

  **Method:** `PUT`
  **Endpoint:** `/crm/v3/lists/{listId}/restore`


### 6. Manage List Membership (MANUAL or SNAPSHOT lists only)

* **Add Records:**

  **Method:** `PUT`
  **Endpoint:** `/crm/v3/lists/{listId}/memberships/add`
  **Request Body:** Array of `recordId`s.

* **Add Records from another List:**

    **Method:** `PUT`
    **Endpoint:** `/crm/v3/lists/{listId}/memberships/add-from/{sourceListId}`
    (Limit 100,000 records)

* **View Records:**

  **Method:** `GET`
  **Endpoint:** `/crm/v3/lists/{listId}/memberships`

* **Remove Records:**

  **Method:** `PUT`
  **Endpoint:** `/crm/v3/lists/{listId}/memberships/remove`
  **Request Body:** Array of `recordId`s.

* **Remove All Records:**

  **Method:** `DELETE`
  **Endpoint:** `/crm/v3/lists/{listId}/memberships` (Does not delete the list itself)


### 7. Migration from v1 to v3

* **Get v3 `listId` from v1 `legacyListId` (Single):**

  **Method:** `GET`
  **Endpoint:** `/crm/v3/lists/idmapping?legacyListId={legacyListId}`

* **Get v3 `listId` from v1 `legacyListId` (Multiple):**

  **Method:** `POST`
  **Endpoint:** `/crm/v3/lists/idmapping`
  **Request Body:** Array of `legacyListId`s (limit 10,000)


### 8. Getting Lists by Type

* **Get Static Lists (MANUAL & SNAPSHOT):**  Use `/crm/v3/lists/search` with `processingTypes: ["MANUAL", "SNAPSHOT"]` in the request body.

* **Get Dynamic Lists:** Use `/crm/v3/lists/search` with `processingTypes: ["DYNAMIC"]` in the request body.

* **Get a Batch of Lists by `listId`:** Use `/crm/v3/lists/search` with the `listIds` parameter.  To include filters, use `/crm/v3/lists` with `includeFilters=true` and `listIds`.

### 9. Getting List Members with Properties

1. Use `/crm/v3/lists/{listId}/memberships/join-order` (GET) to get member `recordId`s.
2. Use `/crm/v3/objects/{object}/search` (POST) with the `recordId`s in the `values` parameter of the filter to retrieve properties for those records.

### 10. Get All/Recently Modified Records with Properties

Use `/crm/v3/objects/{object}/search` (POST).  For recently modified, filter by `lastmodifieddate`.


## Error Handling

(Add a section detailing how errors are returned by the API, including status codes and error messages.)


## Rate Limits

(Add a section on API rate limits.)


## Authentication

(Add a section detailing the authentication method used by the API, typically API keys or OAuth 2.0.)


This documentation provides a comprehensive overview of the HubSpot Lists API v3.  Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
