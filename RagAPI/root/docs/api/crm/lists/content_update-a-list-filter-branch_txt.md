# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, providing comprehensive information on creating, managing, and interacting with lists within your HubSpot account.  The legacy v1 API will be sunsetted on May 30th, 2025.  This document focuses on the v3 API.

## Overview

HubSpot lists are collections of records (contacts, companies, deals, or custom objects) used for segmentation, filtering, and grouping.  A list comprises a definition (essential list information) and memberships (mappings between the list and its records).  The v3 API allows for creation, editing, and retrieval of lists.

Three list processing types exist:

* **MANUAL:** Records are added or removed manually via API calls or user actions.  No background processing occurs.
* **DYNAMIC:**  List filters define membership. HubSpot automatically updates the list based on filter criteria.
* **SNAPSHOT:** Filters are applied at creation; after initial processing, updates are manual only.


## API Endpoints & Usage

All endpoints below are prefixed with `/crm/v3/lists/`.  Replace `{listId}` with the actual list ID (ILS list ID).  Object type IDs can be found in the [HubSpot Object Type ID documentation](<insert_link_here_if_available>).

### 1. Create a List

**Endpoint:** `/` (POST)

**Request Body:**

```json
{
  "name": "My static list",
  "objectTypeId": "0-1", // e.g., 0-1 for contacts
  "processingType": "MANUAL"  // or "DYNAMIC", "SNAPSHOT"
  //Optional: "filterBranch": { ... }  // for DYNAMIC and SNAPSHOT lists. See "Configuring List Filters and Branches" documentation.
}
```

**Response:**  A JSON object containing the newly created list's details, including the `listId`.

**Example:**

```bash
curl -X POST \
  'https://api.hubapi.com/crm/v3/lists/' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
        "name": "My static list",
        "objectTypeId": "0-1",
        "processingType": "MANUAL"
      }'
```


### 2. Retrieve Lists

* **By List ID:**

    **Endpoint:** `/{listId}` (GET)

    **Query Parameter:** `includeFilters=true` (optional) to include filter definitions.

    **Response:** JSON object representing the list.

* **By Name and Object Type:**

    **Endpoint:** `/object-type-id/{objectTypeId}/name/{listName}` (GET)

    **Response:** JSON object representing the list.


* **Multiple Lists by ID:**

    **Endpoint:** `/` (GET)

    **Query Parameter:** `listIds={listId1}&listIds={listId2}&...`

    **Response:** JSON array of lists.


* **Search Lists:** (For more complex searches)

    **Endpoint:** `/search` (POST)

    **Request Body:**

    ```json
    {
      "query": "HubSpot", // Search term in list name
      "processingTypes": ["MANUAL"], // Array of processing types
      // other search parameters
    }
    ```
    **Response:** JSON array of lists matching criteria.


### 3. Update a List

* **Update List Name:**

    **Endpoint:** `/{listId}/update-list-name` (PUT)

    **Query Parameter:** `listName=NewListName`

    **Query Parameter:** `includeFilters=true` (optional)

* **Update List Filters (DYNAMIC lists only):**

    **Endpoint:** `/{listId}/update-list-filters` (PUT)

    **Request Body:** New filter branch definition.


### 4. Delete and Restore a List

* **Delete:**

    **Endpoint:** `/{listId}` (DELETE)

* **Restore:**

    **Endpoint:** `/{listId}/restore` (PUT)  (Only within 90 days of deletion)


### 5. Manage List Memberships (MANUAL and SNAPSHOT lists only)

* **Add Records:**

    **Endpoint:** `/{listId}/memberships/add` (PUT)

    **Request Body:** Array of `recordId`s.

* **Add Records from Another List:**

    **Endpoint:** `/{listId}/memberships/add-from/{sourceListId}` (PUT)  (Limit 100,000 records)

* **View Records:**

    **Endpoint:** `/{listId}/memberships` (GET)

* **Remove Records:**

    **Endpoint:** `/{listId}/memberships/remove` (PUT)

    **Request Body:** Array of `recordId`s.

* **Remove All Records:**

    **Endpoint:** `/{listId}/memberships` (DELETE)  (Does not delete the list itself.)



### 6. Migration from v1 to v3

* **Get List ID Mapping (Single):**

    **Endpoint:** `/idmapping` (GET)

    **Query Parameter:** `legacyListId={legacyListId}`

* **Get List ID Mapping (Batch):**

    **Endpoint:** `/idmapping` (POST)

    **Request Body:** Array of `legacyListId`s (Max 10,000).


### 7. Get Recent List Members with Properties (Requires two API calls)


1. **Get Member IDs:**  `/crm/v3/lists/{listId}/memberships/join-order` (GET)
2. **Get Member Data:** `/crm/v3/objects/{objectTypeId}/search` (POST)  Use the `hs_object_id` property and the `IN` operator with the IDs obtained in step 1.


### 8. Get All/Recently Modified Records

Use the CRM search endpoint:  `/crm/v3/objects/{objectTypeId}/search` (POST)

* **All Records:** Provide the object type.
* **Recently Modified:** Filter by `lastmodifieddate` using the appropriate operator (e.g., `GT` for greater than).


##  Error Handling

The API returns standard HTTP status codes and JSON error responses for various issues (e.g., 400 Bad Request, 404 Not Found).  Refer to HubSpot's API documentation for specific error codes and messages.


## Rate Limits

Be mindful of HubSpot's API rate limits to avoid throttling.


This documentation provides a comprehensive overview.  Consult the official HubSpot API documentation for the most up-to-date information, including detailed specifications and examples for each endpoint.  Remember to replace placeholder values like `{listId}` and `YOUR_API_KEY` with your actual values.
