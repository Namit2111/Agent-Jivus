# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, which allows you to create, manage, and retrieve lists of HubSpot records (contacts, companies, deals, etc.).  The legacy v1 API will be sunsetted on May 30th, 2025.

## Overview

HubSpot lists are collections of records of the same object type, useful for segmentation, filtering, and grouping.  A list comprises two parts:

* **List Definition:** Stores metadata about the list (name, object type, processing type, filters).
* **List Memberships:** Mappings between the list and the associated records.

Three list processing types exist:

* **`MANUAL`:** Records are added or removed only via manual actions or API calls.  No background processing occurs.
* **`DYNAMIC`:**  List filters automatically determine membership.  Records are added/removed based on filter criteria. Background processing maintains the list.
* **`SNAPSHOT`:** Filters are specified at creation; subsequent membership changes require manual intervention.

## API Endpoints

All endpoints are under the `/crm/v3/lists` base path.  Replace `{listId}` with the list's ILS ID (Internal List ID), and `{objectTypeId}` with the ID of the object type (e.g., `0-1` for contacts).  You can find the ILS list ID in the HubSpot UI by hovering over the list and clicking "Details".


### 1. Create a List

**Method:** `POST /crm/v3/lists/`

**Request Body:**

```json
{
  "name": "My static list",
  "objectTypeId": "0-1",
  "processingType": "MANUAL" 
  // "filterBranch": { ... }  // Optional for DYNAMIC and SNAPSHOT lists
}
```

**Response:**  A JSON object containing the newly created list's details, including the `listId`.

### 2. Retrieve Lists

Several methods exist for retrieving lists:

* **By Name and Object Type:** `GET /crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}`
* **By ILS List ID:** `GET /crm/v3/lists/{listId}` (single list)
* **By Multiple ILS List IDs:** `GET /crm/v3/lists?listIds={listId1}&listIds={listId2}&...`

**Query Parameter:** `includeFilters=true` (returns list filter definitions)


### 3. Search for a List

**Method:** `POST /crm/v3/lists/search`

**Request Body:**

```json
{
  "query": "HubSpot", // Search term in list names
  "processingTypes": ["MANUAL"] // List processing types to search for
}
```

**Response:** A JSON object containing a list of matching lists.

### 4. Update a List

* **Update List Name:** `PUT /crm/v3/lists/{listId}/update-list-name?listName={newListName}`

* **Update List Filter Branch (DYNAMIC lists only):** `PUT /crm/v3/lists/{listId}/update-list-filters`

   **Request Body:**  The new filter branch definition.

### 5. Delete and Restore a List

* **Delete:** `DELETE /crm/v3/lists/{listId}`
* **Restore:** `PUT /crm/v3/lists/{listId}/restore` (within 90 days of deletion)

### 6. Manage List Membership (MANUAL or SNAPSHOT lists only)

* **Add Records:** `PUT /crm/v3/lists/{listId}/memberships/add` (Request body: array of `recordId`s)
* **Add Records from Another List:** `PUT /crm/v3/lists/{listId}/memberships/add-from/{sourceListId}` (Max 100,000 records)
* **View Records:** `GET /crm/v3/lists/{listId}/memberships`
* **Remove Records:** `PUT /crm/v3/lists/{listId}/memberships/remove` (Request body: array of `recordId`s)
* **Remove All Records:** `DELETE /crm/v3/lists/{listId}/memberships` (Removes members, not the list)


### 7. Migration from v1 to v3

* **Get v3 List ID from v1 List ID (single):** `GET /crm/v3/lists/idmapping?legacyListId={legacyListId}`
* **Get v3 List IDs from v1 List IDs (batch):** `POST /crm/v3/lists/idmapping` (Request body: array of `legacyListId`s - max 10,000)


### 8. Get Static/Dynamic Lists (using search)

Use `/crm/v3/lists/search` with `processingTypes` parameter:

* **Static:** `processingTypes":["MANUAL","SNAPSHOT"]`
* **Dynamic:** `processingTypes":["DYNAMIC"]`


### 9. Get a Batch of Lists by ID (using search or GET)

* **Using Search:** `POST /crm/v3/lists/search`  (Request body includes `listIds` array)
* **Using GET:** `GET /crm/v3/lists?includeFilters=true&listIds={listId1}&listIds={listId2}&...`

### 10. Get Recent List Members with Properties

1. Get record IDs: `GET /crm/v3/lists/{listId}/memberships/join-order`
2. Search for records using IDs: `POST /crm/v3/objects/{object}/search` (Request body specifies `properties` and filters using `hs_object_id` and `IN` operator)

### 11. Get All/Recently Modified Records with Properties

Use the CRM search endpoint: `POST /crm/v3/objects/{object}/search`

* **All Records:** Specify desired `properties`.
* **Recently Modified:** Filter by `lastmodifieddate` property (e.g., using `GT` operator).



## Error Handling

The API uses standard HTTP status codes to indicate success or failure.  Error responses include detailed JSON objects explaining the issue.


## Rate Limits

Be mindful of HubSpot's API rate limits to avoid throttling.


This documentation provides a comprehensive overview of the HubSpot Lists API v3.  Refer to the official HubSpot developer documentation for the most up-to-date information and detailed specifications.
