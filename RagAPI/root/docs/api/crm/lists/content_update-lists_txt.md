# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, outlining its functionality, endpoints, and usage examples.  The legacy v1 API will be sunsetted on May 30th, 2025.  This guide focuses on the v3 replacement.

## Overview

The HubSpot Lists API v3 allows you to create, manage, and retrieve lists of HubSpot records (contacts, companies, deals, or custom objects).  A list consists of two parts:

* **List Definition:** Stores metadata about the list (name, object type, processing type, filters).
* **List Memberships:**  A mapping between the list and the records it contains.

Three processing types exist:

* **`MANUAL`:** Records are added or removed only through manual actions or API calls.  No background processing occurs.
* **`DYNAMIC`:**  List filters automatically manage membership. Records are added or removed based on filter criteria.  HubSpot handles background processing.
* **`SNAPSHOT`:** Filters are applied at creation. After initial processing, changes are only via manual actions or API calls.


## API Endpoints

All endpoints begin with `/crm/v3/lists/`.  Replace `{listId}` with the actual ILS list ID and `{objectTypeId}` with the appropriate object type ID (e.g., `0-1` for contacts).


### 1. Create a List

**Endpoint:** `/crm/v3/lists/`

**Method:** `POST`

**Request Body:**

```json
{
  "name": "My static list",
  "objectTypeId": "0-1",
  "processingType": "MANUAL" 
  //Optional: "filterBranch": {...} for DYNAMIC and SNAPSHOT lists
}
```

**Response:**  A JSON object containing the newly created list's details, including the `listId`.


### 2. Retrieve Lists

Several methods exist for retrieving lists:

* **By List ID:**

  **Endpoint:** `/crm/v3/lists/{listId}`
  **Method:** `GET`
  **Query Parameter:** `includeFilters=true` (optional, includes filter definitions)

* **By Name and Object Type:**

  **Endpoint:** `/crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}`
  **Method:** `GET`

* **Multiple Lists by ID:**

  **Endpoint:** `/crm/v3/lists`
  **Method:** `GET`
  **Query Parameter:** `listIds={listId1}&listIds={listId2}&...`

### 3. Search for a List

**Endpoint:** `/crm/v3/lists/search`

**Method:** `POST`

**Request Body:**

```json
{
  "query": "HubSpot", // Search term (optional)
  "processingTypes": ["MANUAL"] // Array of processing types (optional)
  // other search criteria
}
```

**Response:** A JSON array of matching lists.


### 4. Update a List

* **Update List Name:**

  **Endpoint:** `/crm/v3/lists/{listId}/update-list-name`
  **Method:** `PUT`
  **Query Parameter:** `listName={newListName}`
  **Query Parameter:** `includeFilters=true` (optional)

* **Update List Filter Branch (DYNAMIC lists only):**

  **Endpoint:** `/crm/v3/lists/{listId}/update-list-filters`
  **Method:** `PUT`
  **Request Body:** The new filter branch definition.


### 5. Delete and Restore a List

* **Delete:**

  **Endpoint:** `/crm/v3/lists/{listId}`
  **Method:** `DELETE`

* **Restore:**

  **Endpoint:** `/crm/v3/lists/{listId}/restore`
  **Method:** `PUT` (Only within 90 days of deletion)


### 6. Manage List Membership (MANUAL and SNAPSHOT lists only)

* **Add Records:**

  **Endpoint:** `/crm/v3/lists/{listId}/memberships/add`
  **Method:** `PUT`
  **Request Body:** An array of `recordId`s.

  **Endpoint (add from another list):** `/crm/v3/lists/{listId}/memberships/add-from/{sourceListId}`
  **Method:** `PUT`  (limit 100,000 records)

* **View Records:**

  **Endpoint:** `/crm/v3/lists/{listId}/memberships`
  **Method:** `GET`

* **Remove Records:**

  **Endpoint:** `/crm/v3/lists/{listId}/memberships/remove`
  **Method:** `PUT`
  **Request Body:** An array of `recordId`s.

* **Remove All Records:**

  **Endpoint:** `/crm/v3/lists/{listId}/memberships`
  **Method:** `DELETE` (removes members, not the list)


### 7. Migrate from v1 to v3

* **Get v3 ID from v1 ID (single):**

   **Endpoint:** `/crm/v3/lists/idmapping?legacyListId={legacyListId}`
   **Method:** `GET`

* **Get v3 IDs from v1 IDs (batch):**

   **Endpoint:** `/crm/v3/lists/idmapping`
   **Method:** `POST`
   **Request Body:** An array of `legacyListId`s (limit 10,000)


### 8. Get Lists by Type (using search)

* **Get Static Lists:**  Use `/crm/v3/lists/search` with `processingTypes: ["MANUAL", "SNAPSHOT"]` in the request body.
* **Get Dynamic Lists:** Use `/crm/v3/lists/search` with `processingTypes: ["DYNAMIC"]` in the request body.
* **Get Batch of Lists by ID:** Use `/crm/v3/lists/search` with `listIds` array in the request body (filters not included).  To include filters, use `/crm/v3/lists` with `includeFilters=true` and `listIds` query parameters.


### 9. Get Recent List Members with Properties

1.  Use `/crm/v3/lists/{listId}/memberships/join-order` (GET) to get `recordId`s.
2.  Use `/crm/v3/objects/{object}/search` (POST) with the `recordId`s in the `values` parameter of a filter.


### 10. Get All/Recently Modified Records with Properties

Use `/crm/v3/objects/{object}/search` (POST).  Filter by `lastmodifieddate` for recently modified records.


## Error Handling

The API will return standard HTTP status codes to indicate success or failure. Error responses will include a JSON payload with details about the error.


## Rate Limits

Refer to HubSpot's API documentation for current rate limits.


This documentation provides a comprehensive overview.  Consult the official HubSpot API documentation for the most up-to-date information and detailed specifications.
