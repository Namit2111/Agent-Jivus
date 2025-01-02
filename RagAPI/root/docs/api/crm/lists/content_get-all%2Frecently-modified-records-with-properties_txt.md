# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, outlining its functionality, endpoints, and usage examples.  The legacy v1 API will be sunset on May 30th, 2025.  This document focuses on the v3 API.


## Overview

The HubSpot Lists API v3 allows you to create, manage, and retrieve lists of records (contacts, companies, deals, or custom objects) within your HubSpot account. Lists are used for segmentation, filtering, and grouping records based on specific criteria.  A list consists of two parts:

* **List Definition:** Stores metadata about the list (name, object type, processing type, filters).
* **List Memberships:**  Mappings between the list and the individual records it contains.

There are three list processing types:

* **MANUAL:** Records are added or removed only through manual actions or API calls.  No background processing.
* **DYNAMIC:**  List filters are used to automatically add or remove records based on matching criteria.  HubSpot automatically updates memberships as records change.
* **SNAPSHOT:** List filters are applied at creation. After the initial snapshot, records are added or removed only manually.


## API Endpoints

All endpoints begin with `/crm/v3/lists/`.  Replace `{listId}` with the actual ILS list ID and `{objectTypeId}` with the appropriate object type ID (e.g., `0-1` for contacts).  See the [HubSpot Object Type IDs](<link to object type IDs if available>) for a complete list.

### 1. Create a List

**Method:** `POST`

**Endpoint:** `/crm/v3/lists/`

**Request Body:**

```json
{
  "name": "My static list",
  "objectTypeId": "0-1",
  "processingType": "MANUAL" 
  //Optional: "filterBranch": {...} for DYNAMIC and SNAPSHOT lists
}
```

**Response:**  The newly created list object, including the `listId`.


### 2. Retrieve Lists

**A. By List ID:**

**Method:** `GET`

**Endpoint:** `/crm/v3/lists/{listId}` (single list) or `/crm/v3/lists?listIds={listId1}&listIds={listId2}&...` (multiple lists)

**Query Parameters:** `includeFilters=true` (optional, to include filter definitions)

**Response:** List object(s).


**B. By Name and Object Type:**

**Method:** `GET`

**Endpoint:** `/crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}`

**Response:** The list object.


### 3. Search for a List

**Method:** `POST`

**Endpoint:** `/crm/v3/lists/search`

**Request Body:**

```json
{
  "query": "HubSpot", // Search term in list name
  "processingTypes": ["MANUAL"] // Optional: filter by processing type(s)
  // other search parameters as needed.
}
```

**Response:** Array of matching list objects.


### 4. Update a List

**A. Update List Name:**

**Method:** `PUT`

**Endpoint:** `/crm/v3/lists/{listId}/update-list-name`

**Query Parameters:** `listName=<newListName>`, `includeFilters=true` (optional)

**Response:** Updated list object.


**B. Update List Filter Branch (DYNAMIC lists only):**

**Method:** `PUT`

**Endpoint:** `/crm/v3/lists/{listId}/update-list-filters`

**Request Body:** The new filter branch definition.

**Response:** Updated list object.


### 5. Delete and Restore a List

**Delete:**

**Method:** `DELETE`

**Endpoint:** `/crm/v3/lists/{listId}`

**Response:** Success/failure message.


**Restore:**

**Method:** `PUT`

**Endpoint:** `/crm/v3/lists/{listId}/restore` (within 90 days of deletion)

**Response:** Success/failure message.


### 6. Manage List Membership (MANUAL and SNAPSHOT lists only)

**A. Add Records:**

**Method:** `PUT`

**Endpoint:** `/crm/v3/lists/{listId}/memberships/add`

**Request Body:** Array of `recordId`s to add.


**B. Add Records from Another List:**

**Method:** `PUT`

**Endpoint:** `/crm/v3/lists/{listId}/memberships/add-from/{sourceListId}`

**Request Body:**  None (the sourceListId specifies the source list)


**C. View Records:**

**Method:** `GET`

**Endpoint:** `/crm/v3/lists/{listId}/memberships`

**Response:** Array of `recordId`s.


**D. Remove Records:**

**Method:** `PUT`

**Endpoint:** `/crm/v3/lists/{listId}/memberships/remove`

**Request Body:** Array of `recordId`s to remove.


**E. Remove All Records:**

**Method:** `DELETE`

**Endpoint:** `/crm/v3/lists/{listId}/memberships`


### 7. Migration from v1 to v3

**A. Get Single List ID Mapping:**

**Method:** `GET`

**Endpoint:** `/crm/v3/lists/idmapping?legacyListId={legacyListId}`

**Response:** `{listId, legacyListId}`


**B. Get Multiple List ID Mappings:**

**Method:** `POST`

**Endpoint:** `/crm/v3/lists/idmapping`

**Request Body:** Array of `legacyListId`s.

**Response:** `{legacyListIdsToIdsMapping, missingLegacyListIds}`


### 8. Get Recent List Members with Properties

1. **GET `/crm/v3/lists/{listId}/memberships/join-order`**: Retrieve `recordId`s.
2. **POST `/crm/v3/objects/{object}/search`**: Search for objects using the `recordId`s obtained in step 1.


### 9. Get All/Recently Modified Records with Properties

Use the CRM object search endpoint (`/crm/v3/objects/{object}/search`). Filter by `lastmodifieddate` for recently modified records.


## Error Handling

The API will return standard HTTP status codes (e.g., 400 Bad Request, 404 Not Found, 500 Internal Server Error) along with a JSON error response providing details.


## Rate Limits

Refer to the HubSpot API documentation for details on rate limits and best practices.


This documentation provides a comprehensive overview of the HubSpot Lists API v3. Remember to consult the official HubSpot API documentation for the most up-to-date information and detailed specifications.
