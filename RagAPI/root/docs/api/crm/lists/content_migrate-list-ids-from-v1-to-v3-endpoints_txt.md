# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, allowing for creation, manipulation, and retrieval of lists.  The legacy v1 API will be sunset on May 30th, 2025.  This guide facilitates migration from v1 to v3.

## List Processing Types

HubSpot Lists offer three processing types:

* **MANUAL:** Records are added or removed only via manual user actions or API calls. No background processing. Ideal for static lists.
* **DYNAMIC:**  Uses list filters to automatically match and include records. HubSpot's system manages memberships based on filter criteria, adding or removing records as they meet or fail those criteria. Ideal for evolving lists.
* **SNAPSHOT:** Filters are applied at creation; after initial processing, only manual updates are allowed. Useful for creating a list based on specific criteria at a point in time without automatic future updates.

## API Endpoints

All endpoints begin with `/crm/v3/lists/`.  Replace `{listId}` with the ILS (HubSpot internal) list ID.  You can find this ID in the HubSpot UI by hovering over a list and clicking "Details".


### 1. Create a List

**Method:** `POST`

**Endpoint:** `/crm/v3/lists/`

**Request Body:**

```json
{
  "name": "My static list",
  "objectTypeId": "0-1",  //e.g., 0-1 for contacts. See full list of object type IDs in HubSpot documentation.
  "processingType": "MANUAL" // or "DYNAMIC", "SNAPSHOT"
  // "filterBranch": { ... } // Optional for DYNAMIC and SNAPSHOT lists. See "Configuring List Filters and Branches" in HubSpot documentation.
}
```

**Response:**  A JSON object containing the created list's details, including the `listId`.

### 2. Retrieve Lists

Several methods exist for retrieving lists:

* **By List ID:**

    **Method:** `GET`

    **Endpoint:** `/crm/v3/lists/{listId}`

    **Query Parameter:** `includeFilters=true` (optional) to include filter definitions.

    **Response:**  JSON object containing the list's details.

* **By Name and Object Type:**

    **Method:** `GET`

    **Endpoint:** `/crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}`

    **Response:** JSON object containing the list's details.

* **Multiple Lists by ID:**

    **Method:** `GET`

    **Endpoint:** `/crm/v3/lists`

    **Query Parameter:** `listIds={listId1}&listIds={listId2}&...`

    **Response:** JSON array containing details for multiple lists.

    **Example:** `/crm/v3/lists?listIds=123&listIds=456`

* **Batch of Lists by ID (POST):**
    **Method:** `POST`
    **Endpoint:** `/crm/v3/lists/search`
    **Request Body:**
    ```json
    {
      "listIds": ["123", "456"],
      "additionalProperties": ["hs_is_public", "hs_is_read_only", ...] //Optional properties
    }
    ```
    **Response:** JSON array containing details for the specified lists. Filters are not included. To include filters use the GET method above with `includeFilters=true`.

### 3. Search for a List

**Method:** `POST`

**Endpoint:** `/crm/v3/lists/search`

**Request Body:**

```json
{
  "query": "HubSpot", // Optional search term in list name
  "processingTypes": ["MANUAL"], // Optional array of processing types to filter by
  "listIds": ["1","2"] //Optional - Search by List IDs
  //Other filtering parameters as detailed in HubSpot documentation
}
```

**Response:**  JSON array containing details of matching lists.


### 4. Update a List Name

**Method:** `PUT`

**Endpoint:** `/crm/v3/lists/{listId}/update-list-name`

**Query Parameter:** `listName={newListName}`

**Query Parameter:** `includeFilters=true` (optional) to include filter definitions.

**Response:** JSON object containing updated list details.

### 5. Update List Filter Branch (DYNAMIC lists only)

**Method:** `PUT`

**Endpoint:** `/crm/v3/lists/{listId}/update-list-filters`

**Request Body:**  The new filter branch definition (refer to HubSpot documentation for details on filter branch structure).

**Response:** JSON object containing updated list details.


### 6. Delete and Restore a List

* **Delete:**

    **Method:** `DELETE`

    **Endpoint:** `/crm/v3/lists/{listId}`

* **Restore:** (Within 90 days of deletion)

    **Method:** `PUT`

    **Endpoint:** `/crm/v3/lists/{listId}/restore`


### 7. Manage List Membership (MANUAL and SNAPSHOT lists only)

* **Add Records:**

    **Method:** `PUT`

    **Endpoint:** `/crm/v3/lists/{listId}/memberships/add`

    **Request Body:** Array of `recordId`s to add.

* **Add Records from Another List:**

    **Method:** `PUT`

    **Endpoint:** `/crm/v3/lists/{listId}/memberships/add-from/{sourceListId}`

    **Limit:** 100,000 records at a time.

* **View Records:**

    **Method:** `GET`

    **Endpoint:** `/crm/v3/lists/{listId}/memberships`

    **Response:**  Array of `recordId`s.

* **Delete Records:**

    **Method:** `PUT`

    **Endpoint:** `/crm/v3/lists/{listId}/memberships/remove`

    **Request Body:** Array of `recordId`s to remove.

* **Delete All Records:**

    **Method:** `DELETE`

    **Endpoint:** `/crm/v3/lists/{listId}/memberships` (This does *not* delete the list itself.)


### 8. Migration from v1 to v3

* **Get v3 `listId` from v1 `legacyListId` (single):**

    **Method:** `GET`

    **Endpoint:** `/crm/v3/lists/idmapping?legacyListId={legacyListId}`

    **Response:**  JSON object `{ "listId": "...", "legacyListId": "..." }`

* **Get v3 `listId` from v1 `legacyListId` (batch):**

    **Method:** `POST`

    **Endpoint:** `/crm/v3/lists/idmapping`

    **Request Body:** Array of `legacyListId`s.

    **Response:** JSON object with `legacyListIdsToIdsMapping` (successful mappings) and `missingLegacyListIds` (failed mappings).  Maximum 10,000 entries.

### 9. Get Recent List Members with Properties

1. **Get Record IDs:**
   `GET /crm/v3/lists/{listId}/memberships/join-order`

2. **Get Records with Properties:**
   `POST /crm/v3/objects/{object}/search` with `hs_object_id` IN the record IDs obtained in step 1.

   **Request Body (example):**

   ```json
   {
     "properties": ["firstname", "lastname", "email", ...],
     "filterGroups": [
       {
         "filters": [
           {
             "propertyName": "hs_object_id",
             "operator": "IN",
             "values": ["recordId1", "recordId2", ...]
           }
         ]
       }
     ]
   }
   ```

### 10. Get All/Recently Modified Records with Properties

Use the CRM search endpoint: `/crm/v3/objects/{object}/search`

* **All Records:**  Specify the object type (`contacts`, `deals`, etc.) and properties to retrieve.

* **Recently Modified Records:**  Add a filter on `lastmodifieddate` (e.g., `lastmodifieddate > 2024-03-08`)


##  Error Handling

The API returns standard HTTP status codes to indicate success or failure. Error responses will typically include a JSON object with details about the error. Refer to the HubSpot API documentation for specific error codes and their meanings.


This documentation provides a concise overview.  Always refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications.
