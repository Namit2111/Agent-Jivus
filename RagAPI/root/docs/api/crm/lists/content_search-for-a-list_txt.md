# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, providing comprehensive information on creating, managing, and retrieving lists.  The legacy v1 API will be sunset on May 30th, 2025.  This documentation focuses on the v3 API.

## Overview

HubSpot lists are collections of records (contacts, companies, deals, or custom objects) used for segmentation, filtering, and grouping.  The v3 API allows for creating, editing, and fetching these lists.  A list comprises a list definition (essential information) and list memberships (mappings between the list and object records).

Three list processing types exist:

* **MANUAL:** Records are added or removed only via manual user actions or API calls.  No background processing occurs.
* **DYNAMIC:**  List filters define membership. HubSpot automatically updates the list based on filter matches.  Records are re-evaluated whenever they change.
* **SNAPSHOT:** Filters are defined at creation.  After initial processing, only manual updates modify membership.


## API Endpoints

All endpoints are under the base URL `/crm/v3/lists/`.  Replace `{listId}` with the actual ILS list ID (obtainable via the HubSpot UI or search API).  `{objectTypeId}` represents the ID of the object type (e.g., contacts, companies).  See the full list of object type IDs in the HubSpot documentation.


### 1. Create a List

**Method:** `POST /crm/v3/lists/`

**Request Body:**

```json
{
  "name": "My static list",
  "objectTypeId": "0-1",  // Example: Contacts
  "processingType": "MANUAL" 
  //Optional: "filterBranch": {...} for DYNAMIC and SNAPSHOT lists
}
```

**Response:**  Returns the created list, including the `listId`.


### 2. Retrieve Lists

Several methods exist to retrieve lists:

* **By List ID:** `GET /crm/v3/lists/{listId}` (Individual list) or `GET /crm/v3/lists?listIds={listId1}&listIds={listId2}&...` (Multiple lists)  Add `includeFilters=true` to include filter definitions.

* **By Name and Object Type:** `GET /crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}`


### 3. Search for a List

**Method:** `POST /crm/v3/lists/search`

**Request Body:**

```json
{
  "query": "HubSpot",       // Search term in list name
  "processingTypes": ["MANUAL"] // Filter by processing type
}
```

**Response:** Returns a list of matching lists.


### 4. Update a List

* **Update List Name:** `PUT /crm/v3/lists/{listId}/update-list-name?listName={newListName}`

* **Update Filter Branch (DYNAMIC lists only):** `PUT /crm/v3/lists/{listId}/update-list-filters`  (Request body contains the new filter branch definition).


### 5. Delete and Restore a List

* **Delete:** `DELETE /crm/v3/lists/{listId}`
* **Restore (within 90 days):** `PUT /crm/v3/lists/{listId}/restore`


### 6. Manage List Membership (MANUAL and SNAPSHOT lists only)

* **Add Records:** `PUT /crm/v3/lists/{listId}/memberships/add` (Request body: array of `recordIds`) or `PUT /crm/v3/lists/{listId}/memberships/add-from/{sourceListId}` (add from another list, max 100,000 records)

* **View Records:** `GET /crm/v3/lists/{listId}/memberships`

* **Remove Records:** `PUT /crm/v3/lists/{listId}/memberships/remove` (Request body: array of `recordIds`) or `DELETE /crm/v3/lists/{listId}/memberships` (remove all records)


### 7. Migration from v1 to v3

* **Get v3 `listId` from v1 `legacyListId` (one at a time):** `GET /crm/v3/lists/idmapping?legacyListId={legacyListId}`

* **Get v3 `listId` from v1 `legacyListId` (batch):** `POST /crm/v3/lists/idmapping` (Request body: array of `legacyListIds`, max 10,000)


### 8. Get Lists by Type

* **Get Static Lists (MANUAL & SNAPSHOT):** `POST /crm/v3/lists/search` (Request body includes `"processingTypes": ["MANUAL", "SNAPSHOT"]`)

* **Get Dynamic Lists:** `POST /crm/v3/lists/search` (Request body includes `"processingTypes": ["DYNAMIC"]`)

* **Get a Batch of Lists by ID:** `POST /crm/v3/lists/search` (Request body includes `listIds` array)  or `GET /crm/v3/lists?includeFilters=true&listIds={listId1}&listIds={listId2}&...`


### 9. Get Recent List Members with Properties

1.  `GET /crm/v3/lists/{listId}/memberships/join-order` (Get member `recordIds`)
2.  `POST /crm/v3/objects/{object}/search` (Search for objects with the obtained `recordIds`)


### 10. Get All/Recently Modified Records

`POST /crm/v3/objects/{object}/search`  (Specify properties and filters as needed for recently modified records using `lastmodifieddate`).


## Error Handling

The API will return standard HTTP status codes to indicate success or failure.  Error responses will include details in the response body.  Refer to the HubSpot API documentation for a complete list of error codes and their meanings.


##  Rate Limits

Be aware of HubSpot's API rate limits to avoid exceeding allowed requests per time period.  Consult the HubSpot API documentation for current limits.


This documentation provides a high-level overview.  Consult the official HubSpot API documentation for detailed specifications, examples, and complete error handling information.
