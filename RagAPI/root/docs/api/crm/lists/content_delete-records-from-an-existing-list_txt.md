# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, providing a comprehensive guide to managing lists within your HubSpot account.  The legacy v1 API will be sunsetted on May 30th, 2025.  This documentation focuses on the v3 API.


## Overview

HubSpot lists are collections of records (contacts, companies, deals, or custom objects) used for segmentation, filtering, and grouping. The v3 Lists API allows for creation, modification, and retrieval of lists.  A list comprises a list definition (essential information) and list memberships (mappings between the list and object records).


## List Processing Types

Three processing types exist:

* **MANUAL:** Records are added or removed only through manual user actions or API calls.  No background processing by HubSpot.  Ideal for static lists.
* **DYNAMIC:**  List filters define membership criteria. HubSpot automatically maintains the list, adding/removing records based on filter matches. Ideal for lists expected to change over time.
* **SNAPSHOT:** List filters are specified at creation; after initial processing, only manual updates are possible. Useful for creating a list based on criteria at a specific point in time.


## API Endpoints

All endpoints are prefixed with `/crm/v3/lists/`.  Replace `{listId}` with the actual ILS list ID and `{objectTypeId}` with the ID of the object type (e.g., "0-1" for contacts).  See the HubSpot documentation for a complete list of `objectTypeId` values.


### 1. Create a List

**Method:** `POST`

**Endpoint:** `/`

**Request Body:**

```json
{
  "name": "My static list",
  "objectTypeId": "0-1",
  "processingType": "MANUAL" 
  // "filterBranch": { ... }  //Optional for DYNAMIC and SNAPSHOT lists
}
```

**Response:**  The created list's details, including the `listId`.


### 2. Retrieve Lists

Several methods exist:

* **By ILS List ID:**
    * **Method:** `GET`
    * **Endpoint:** `/{listId}`
    * **Query Parameter:** `includeFilters=true` (optional, to include filter definitions)

* **By Name and Object Type:**
    * **Method:** `GET`
    * **Endpoint:** `/object-type-id/{objectTypeId}/name/{listName}`

* **Multiple Lists by ID:**
    * **Method:** `GET`
    * **Endpoint:** `/`
    * **Query Parameter:** `listIds={listId1}&listIds={listId2}&...`
    * **Query Parameter:** `includeFilters=true` (optional)

* **Search Lists (POST):** More flexible search. See section below.


### 3. Search for a List

**Method:** `POST`

**Endpoint:** `/search`

**Request Body:**

```json
{
  "query": "HubSpot", // Search term in list name
  "processingTypes": ["MANUAL"] //Filter by processing type(s)
  // other parameters available
}
```

**Response:** An array of lists matching the search criteria.


### 4. Update a List

* **Update List Name:**
    * **Method:** `PUT`
    * **Endpoint:** `/{listId}/update-list-name`
    * **Query Parameter:** `listName={newListName}`
    * **Query Parameter:** `includeFilters=true` (optional)

* **Update Filter Branch (DYNAMIC lists only):**
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


### 6. Manage List Membership (MANUAL and SNAPSHOT lists only)

* **Add Records:**
    * **Method:** `PUT`
    * **Endpoint:** `/{listId}/memberships/add`
    * **Request Body:** An array of `recordId`s.

* **Add Records from another List:**
    * **Method:** `PUT`
    * **Endpoint:** `/{listId}/memberships/add-from/{sourceListId}`

* **View Records:**
    * **Method:** `GET`
    * **Endpoint:** `/{listId}/memberships`

* **Remove Records:**
    * **Method:** `PUT`
    * **Endpoint:** `/{listId}/memberships/remove`
    * **Request Body:** An array of `recordId`s.

* **Remove All Records:**
    * **Method:** `DELETE`
    * **Endpoint:** `/{listId}/memberships`


### 7. Migrate from v1 to v3 (Use before May 30th, 2025)

* **Single ID Mapping:**
    * **Method:** `GET`
    * **Endpoint:** `/idmapping`
    * **Query Parameter:** `legacyListId={legacyListId}`

* **Batch ID Mapping:**
    * **Method:** `POST`
    * **Endpoint:** `/idmapping`
    * **Request Body:** An array of `legacyListId`s (max 10,000).


### 8. Get Recent List Members with Properties

1. Get record IDs using: `GET /crm/v3/lists/{listId}/memberships/join-order`
2. Use CRM object search (`POST /crm/v3/objects/{object}/search`) with the retrieved IDs in the `values` parameter.


### 9. Get All/Recently Modified Records with Properties

Use the CRM object search endpoint (`POST /crm/v3/objects/{object}/search`).  Filter by `lastmodifieddate` for recently modified records.



##  Error Handling

The API will return standard HTTP status codes to indicate success or failure.  Refer to the HubSpot API documentation for specific error codes and their meanings.


## Rate Limits

Be aware of HubSpot's API rate limits to avoid exceeding allowed request counts.


## Authentication

You will need a HubSpot API key for authentication.  Refer to the HubSpot API documentation for details on authentication methods.


This documentation provides a summary.  Always refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications.
