# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, providing comprehensive information on creating, managing, and retrieving lists.  The legacy v1 API will be sunset on May 30th, 2025.  This guide facilitates migration to the v3 API.

## Overview

HubSpot Lists allow for record segmentation, filtering, and grouping based on object type (contacts, companies, deals, or custom objects).  A list comprises a definition (essential information) and memberships (mappings between the list and object records).  This API allows for creating, editing, and fetching lists.

There are three list processing types:

* **MANUAL:** Records are added or removed only through manual actions or API calls. No background processing.
* **DYNAMIC:**  List filters automatically manage memberships. Records are added or removed based on filter criteria.
* **SNAPSHOT:** Filters are set at creation; subsequent changes require manual intervention.


## API Endpoints

All endpoints are under the base URL `/crm/v3/lists/`.

### 1. Create a List

**Endpoint:** `/crm/v3/lists/`

**Method:** `POST`

**Request Body:**

```json
{
  "name": "My static list",
  "objectTypeId": "0-1",  // e.g., 0-1 for contacts
  "processingType": "MANUAL" // or "DYNAMIC", "SNAPSHOT"
  "filterBranch": { /* Optional; for DYNAMIC and SNAPSHOT lists. See 'Configuring List Filters and Branches' */ }
}
```

**Response:**  A JSON object containing the newly created list's data, including the `listId` (ILS list ID).

**Example:**  Successful creation returns a JSON object containing the new list's details, including the `listId`.


### 2. Retrieve Lists

Several methods exist to retrieve lists:

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
  "query": "HubSpot", // Optional search term in list name
  "processingTypes": ["MANUAL"] // Optional; array of processing types to filter by
}
```

**Response:** A JSON array containing lists matching the search criteria.

### 4. Update a List

* **Update List Name:**

    **Endpoint:** `/crm/v3/lists/{listId}/update-list-name`
    **Method:** `PUT`
    **Query Parameter:** `listName={newListName}`
    **Query Parameter:** `includeFilters=true` (optional)

* **Update List Filter Branch (DYNAMIC lists only):**

    **Endpoint:** `/crm/v3/lists/{listId}/update-list-filters`
    **Method:** `PUT`
    **Request Body:**  The updated filter branch definition.

### 5. Delete and Restore a List

* **Delete:**

    **Endpoint:** `/crm/v3/lists/{listId}`
    **Method:** `DELETE`

* **Restore (within 90 days of deletion):**

    **Endpoint:** `/crm/v3/lists/{listId}/restore`
    **Method:** `PUT`


### 6. Manage List Membership (MANUAL & SNAPSHOT lists only)

* **Add Records:**

    **Endpoint:** `/crm/v3/lists/{listId}/memberships/add`
    **Method:** `PUT`
    **Request Body:** An array of `recordId`s.

    **Endpoint (add from another list):** `/crm/v3/lists/{listId}/memberships/add-from/{sourceListId}`
    **Method:** `PUT`
    **(Limit: 100,000 records)**

* **View Records:**

    **Endpoint:** `/crm/v3/lists/{listId}/memberships`
    **Method:** `GET`

* **Remove Records:**

    **Endpoint:** `/crm/v3/lists/{listId}/memberships/remove`
    **Method:** `PUT`
    **Request Body:** An array of `recordId`s.

* **Remove All Records:**

    **Endpoint:** `/crm/v3/lists/{listId}/memberships`
    **Method:** `DELETE` (Removes members, not the list itself)


### 7.  Migration from v1 to v3

* **Get List IDs Mapping (One at a time):**

    **Endpoint:** `/crm/v3/lists/idmapping`
    **Method:** `GET`
    **Query Parameter:** `legacyListId={legacyListId}`

* **Get List IDs Mapping (Batch):**

    **Endpoint:** `/crm/v3/lists/idmapping`
    **Method:** `POST`
    **Request Body:** An array of `legacyListId`s (limit: 10,000).

**Note:**  The v1 API and ID mapping endpoints will be sunset on May 30th, 2025.


### 8. Getting Records Associated with a List (Requires additional steps)

This involves fetching `recordId`s via `/crm/v3/lists/{listId}/memberships/join-order` and then using the CRM search endpoint `/crm/v3/objects/{object}/search` with the retrieved IDs.  See the provided examples in the original text for details.


## Error Handling

The API returns standard HTTP status codes to indicate success or failure.  Detailed error messages are included in the response body for troubleshooting.


##  Rate Limiting

The API has rate limits.  Refer to HubSpot's documentation for details on rate limits and how to handle them.


This documentation provides a comprehensive overview of the HubSpot Lists API v3. Remember to consult the official HubSpot API documentation for the most up-to-date information and detailed specifications.
