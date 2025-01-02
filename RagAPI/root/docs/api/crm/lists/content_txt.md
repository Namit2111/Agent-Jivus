# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, providing comprehensive information on creating, managing, and retrieving lists.  The legacy v1 API will be sunsetted on May 30th, 2025.  This document focuses on the v3 API.

## Overview

Lists in HubSpot are collections of records of the same object type (e.g., contacts, companies, deals). They facilitate record segmentation, filtering, and grouping.  A list comprises a list definition (essential information) and list memberships (mappings between the list and object records).

There are three list processing types:

* **MANUAL:** Records are added or removed only through manual user actions or API calls. No background processing by HubSpot.
* **DYNAMIC:**  List filters define membership criteria. HubSpot automatically updates membership based on filter matches.
* **SNAPSHOT:** List filters are set at creation.  After initial processing, only manual updates are allowed.


## API Endpoints

All endpoints below are prefixed with `/crm/v3/lists/`.  Replace `{listId}` with the actual ILS list ID and `{objectTypeId}` with the appropriate object type ID (see [Object Type IDs](<link_to_object_type_ids_documentation>)).

### 1. Create a List

**Method:** `POST`

**Endpoint:** `/`

**Request Body:**

```json
{
  "name": "My static list",
  "objectTypeId": "0-1",  // Example: Contacts
  "processingType": "MANUAL"
  //Optional: "filterBranch": {...}  for DYNAMIC and SNAPSHOT lists (see configuring list filters and branches)
}
```

**Response:**  A JSON object containing the newly created list's information, including the `listId`.

### 2. Retrieve Lists

Several methods exist to retrieve lists:

* **By List ID:**

  **Method:** `GET`
  **Endpoint:** `/{listId}`
  **Query Parameters:** `includeFilters=true` (optional, includes filter definitions)

* **By Name and Object Type:**

  **Method:** `GET`
  **Endpoint:** `/object-type-id/{objectTypeId}/name/{listName}`

* **Multiple Lists by ID:**

  **Method:** `GET`
  **Endpoint:** `/`
  **Query Parameters:** `listIds={listId1}&listIds={listId2}&...`  `includeFilters=true` (optional)


**Response:** A JSON array containing list information.


### 3. Search for a List

**Method:** `POST`

**Endpoint:** `/search`

**Request Body:**

```json
{
  "query": "HubSpot",  //Search term in list name
  "processingTypes": ["MANUAL"] //List processing type(s)
}
```

**Response:** A JSON array of lists matching the search criteria.


### 4. Update a List

* **Update List Name:**

  **Method:** `PUT`
  **Endpoint:** `/{listId}/update-list-name`
  **Query Parameters:** `listName={newListName}`, `includeFilters=true` (optional)


* **Update List Filter Branch (DYNAMIC lists only):**

  **Method:** `PUT`
  **Endpoint:** `/{listId}/update-list-filters`
  **Request Body:** The updated filter branch definition.

**Response:**  Updated list information.

### 5. Delete and Restore a List

* **Delete:**

  **Method:** `DELETE`
  **Endpoint:** `/{listId}`

* **Restore:**

  **Method:** `PUT`
  **Endpoint:** `/{listId}/restore`  (Within 90 days of deletion)

**Response:**  Success/failure indication.


### 6. Manage List Membership (MANUAL and SNAPSHOT lists only)


* **Add Records:**

  **Method:** `PUT`
  **Endpoint:** `/{listId}/memberships/add`
  **Request Body:** Array of `recordId`s

* **Add Records from another List:**

  **Method:** `PUT`
  **Endpoint:** `/{listId}/memberships/add-from/{sourceListId}` (Limit: 100,000 records)

* **View Records:**

  **Method:** `GET`
  **Endpoint:** `/{listId}/memberships`

* **Delete Records:**

  **Method:** `PUT`
  **Endpoint:** `/{listId}/memberships/remove`
  **Request Body:** Array of `recordId`s

* **Delete All Records (from List):**

  **Method:** `DELETE`
  **Endpoint:** `/{listId}/memberships` (List itself remains)

**Response:**  Success/failure indication or list of records.


### 7. Migrate from v1 to v3

* **Get v3 List ID from v1 List ID (single):**

  **Method:** `GET`
  **Endpoint:** `/idmapping`
  **Query Parameters:** `legacyListId={legacyListId}`

* **Get v3 List IDs from v1 List IDs (batch):**

  **Method:** `POST`
  **Endpoint:** `/idmapping`
  **Request Body:** Array of `legacyListId`s (Max 10,000)


**Response:**  JSON object mapping legacy and v3 IDs.  Note that the `/idmapping` endpoints will sunset May 30th, 2025.


### 8. Get Lists by Processing Type (search based)

* **Get Static Lists (MANUAL and SNAPSHOT):**
    * Method: `POST`
    * Endpoint: `/search`
    * Request Body: Include `"processingTypes": ["MANUAL", "SNAPSHOT"]`

* **Get Dynamic Lists:**
    * Method: `POST`
    * Endpoint: `/search`
    * Request Body: Include `"processingTypes": ["DYNAMIC"]`

* **Get Batch of Lists by List ID:**
    * Method: `POST`
    * Endpoint: `/search`
    * Request Body: Include `"listIds": ["listId1", "listId2", ...]`  You can optionally include `additionalProperties` for extra list data.  Filters are *not* included in the response.  To include filters use the GET method on `/` with `listIds` and `includeFilters=true`.



### 9. Get List Members with Properties

1. Get record IDs via `/crm/v3/lists/{listId}/memberships/join-order` (GET request).
2. Use `/crm/v3/objects/{object}/search` (POST request) with the obtained `recordId`s in the `values` parameter under `filterGroups`.  Specify the desired `properties` to retrieve.

### 10. Get All/Recently Modified Records with Properties

Use the CRM search endpoint `/crm/v3/objects/{object}/search` (POST).  To filter by `lastmodifieddate`, use the `filterGroups` parameter.

##  Error Handling

The API will return standard HTTP status codes to indicate success or failure. Error responses will include details in the JSON response body.


## Rate Limits

Refer to HubSpot's API documentation for current rate limits.


This documentation provides a comprehensive overview of the HubSpot Lists API v3.  Refer to HubSpot's official API documentation for the most up-to-date information and detailed specifications. Remember to replace placeholders like `{listId}` and `{objectTypeId}` with actual values.
