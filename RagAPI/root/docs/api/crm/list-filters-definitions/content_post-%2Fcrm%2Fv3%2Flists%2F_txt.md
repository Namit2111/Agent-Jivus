# HubSpot Lists API v3 Documentation

This document provides a comprehensive overview of the HubSpot Lists API v3, enabling you to manage list memberships for object lists.

## Introduction

The Lists API allows you to perform various operations on HubSpot lists, including fetching lists, creating new lists, updating list information, managing memberships, and working with list folders.  This API is crucial for bulk operations related to adding or removing contacts or companies from lists.

**Use Cases:**

* Bulk adding contacts to a list.
* Removing company records from a company list.
* Managing list memberships efficiently.


**Supported Products:**  Marketing Hub Starter and Content Hub Starter (or higher).

## API Endpoints

All endpoints use the base URL: `https://api.hubapi.com/crm/v3/`

**Authentication:** Requires an access token.  Use `Bearer YOUR_ACCESS_TOKEN` in the `Authorization` header.


### Lists

#### 1. Fetch List by ID

* **Method:** `GET`
* **Endpoint:** `/crm/v3/lists/{listId}`
* **Description:** Fetches a single list by its ILS list ID.
* **Parameters:**
    * `listId`: (required) The ID of the list to retrieve.
    * `includeFilters`: (optional, boolean) Whether to include filter definitions in the response. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/listId?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response:**  (Structure will vary, see HubSpot API documentation for detailed schema)
```json
{
  "listId": 123,
  "name": "My List",
  "objectTypeId": "contacts",
  // ... other properties
}
```

#### 2. Fetch List by Name

* **Method:** `GET`
* **Endpoint:** `/crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}`
* **Description:** Fetches a single list by its name and object type.
* **Parameters:**
    * `objectTypeId`: (required) The type of object the list contains (e.g., `contacts`, `companies`).
    * `listName`: (required) The name of the list.
    * `includeFilters`: (optional, boolean) Whether to include filter definitions in the response. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/object-type-id/contacts/name/MyList?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```


#### 3. Fetch Multiple Lists

* **Method:** `GET`
* **Endpoint:** `/crm/v3/lists/`
* **Description:** Fetches multiple lists based on provided `listIds`.
* **Parameters:**
    * `listId`: (required) Comma-separated list of list IDs to retrieve.
    * `includeFilters`: (optional, boolean) Whether to include filter definitions in the response. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/?listId=123,456&includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

#### 4. Create List

* **Method:** `POST`
* **Endpoint:** `/crm/v3/lists/`
* **Description:** Creates a new list.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`
* **Request Body (JSON):**
```json
{
  "objectTypeId": "contacts",
  "processingType": "MANUAL", // or SNAPSHOT
  "customProperties": {
    "additionalProp1": "value1",
    // ...
  },
  "listFolderId": 0,
  "name": "New List",
  "filterBranch": {
    "filterBranchType": "OR",
    "filterBranchOperator": "AND" // or OR
  }
}
```
* **Example Request (cURL):**  (Use the above JSON body as --data)

#### 5. Search Lists

* **Method:** `POST`
* **Endpoint:** `/crm/v3/lists/search`
* **Description:** Searches lists by name or pages through all lists.
* **Request Body (JSON):**
```json
{
  "listIds": ["123", "456"],
  "offset": 0,
  "query": "My List",
  "count": 25,
  "processingTypes": ["MANUAL", "SNAPSHOT"],
  "additionalProperties": ["prop1", "prop2"],
  "sort": "name" // e.g., "name ASC", "name DESC"
}
```
* **Example Request (cURL):** (Use the above JSON body as --data)


#### 6. Restore a List

* **Method:** `PUT`
* **Endpoint:** `/crm/v3/lists/{listId}/restore`
* **Description:** Restores a previously deleted list (within 90 days).
* **Parameters:**
    * `listId`: (required) The ID of the list to restore.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**


#### 7. Update List Filter Definition

* **Method:** `PUT`
* **Endpoint:** `/crm/v3/lists/{listId}/update-list-filters`
* **Description:** Updates the filter definition of a dynamic list.
* **Parameters:**
    * `listId`: (required) The ID of the list to update.
    * `enrollObjectsInWorkflows`: (optional, boolean)  Whether to enroll objects in workflows. Defaults to `false`.
* **Request Body (JSON):**  (Similar structure to create list's `filterBranch`)
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**


#### 8. Update List Name

* **Method:** `PUT`
* **Endpoint:** `/crm/v3/lists/{listId}/update-list-name`
* **Description:** Updates the name of a list.
* **Parameters:**
    * `listId`: (required) The ID of the list to update.
    * `includeFilters`: (optional, boolean) Whether to include filters in the response. Defaults to `false`.
* **Request Body (JSON):**  `{ "name": "New List Name" }`
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**


#### 9. Delete a List

* **Method:** `DELETE`
* **Endpoint:** `/crm/v3/lists/{listId}`
* **Description:** Deletes a list.  Can be restored within 90 days.
* **Parameters:**
    * `listId`: (required) The ID of the list to delete.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**



### Memberships  (All endpoints under `/crm/v3/lists/{listId}/memberships/` unless otherwise specified)

**(Note:  Many Membership endpoints have restrictions on `processingType` (MANUAL or SNAPSHOT) and maximum memberships (often < 100,000).  Refer to the HubSpot API documentation for detailed limits.)**

#### 10. Fetch List Memberships Ordered by Added to List Date

* **Method:** `GET`
* **Endpoint:** `/crm/v3/lists/{listId}/memberships/join-order`
* **Description:** Fetches list memberships ordered by join date.  Supports pagination (`after`, `before`, `limit`).
* **Parameters:**
    * `listId`: (required) The ID of the list.
    * `after`: (optional)  Pagination offset.
    * `before`: (optional) Pagination offset.
    * `limit`: (optional)  Number of records to return.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**


#### 11. Fetch List Memberships Ordered by ID

* **Method:** `GET`
* **Endpoint:** `/crm/v3/lists/{listId}/memberships`
* **Description:** Fetches list memberships ordered by `recordId`.  Supports pagination.
* **Parameters:** (Similar to above, replace `/join-order` with `/memberships`)
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**


#### 12. Get lists record is member of

* **Method:** `GET`
* **Endpoint:** `/crm/v3/lists/records/{objectTypeId}/{recordId}/memberships`
* **Description:** Retrieves the lists a specific record belongs to.
* **Parameters:**
    * `objectTypeId`: (required) Object type of the record.
    * `recordId`: (required) ID of the record.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**


#### 13. Add All Records from a Source List to a Destination List

* **Method:** `PUT`
* **Endpoint:** `/crm/v3/lists/{listId}/memberships/add-from/{sourceListId}`
* **Description:** Adds all records from one list to another.
* **Parameters:**
    * `listId`: (required) Destination list ID.
    * `sourceListId`: (required) Source list ID.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**


#### 14. Add and/or Remove Records from a List

* **Method:** `PUT`
* **Endpoint:** `/crm/v3/lists/{listId}/memberships/add-and-remove`
* **Description:** Adds and/or removes records from a list.
* **Request Body (JSON):**
```json
{
  "recordIdsToRemove": [654],
  "recordIdsToAdd": [123, 456, 789]
}
```
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**


#### 15. Add Records to a List

* **Method:** `PUT`
* **Endpoint:** `/crm/v3/lists/{listId}/memberships/add`
* **Description:** Adds records to a list.  Ignores existing members.
* **Request Body (JSON):** `["recordId1", "recordId2", ...]`
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**


#### 16. Remove Records from a List

* **Method:** `PUT`
* **Endpoint:** `/crm/v3/lists/{listId}/memberships/remove`
* **Description:** Removes records from a list.  Ignores non-members.
* **Request Body (JSON):** `["recordId1", "recordId2", ...]`
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**


#### 17. Delete All Records from a List

* **Method:** `DELETE`
* **Endpoint:** `/crm/v3/lists/{listId}/memberships`
* **Description:** Removes all records from a list (list itself remains).
* **Parameters:**
    * `listId`: (required) The ID of the list.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**


### Folders (All endpoints under `/crm/v3/lists/folders/`)

#### 18. Retrieves a folder

* **Method:** `GET`
* **Endpoint:** `/crm/v3/lists/folders`
* **Description:** Retrieves a folder and its child folders and lists (only lists in the retrieved folder itself).
* **Parameters:** `folderId`: (required)  The ID of the folder to retrieve.  Defaults to 0 (root).
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**


#### 19. Creates a folder

* **Method:** `POST`
* **Endpoint:** `/crm/v3/lists/folders`
* **Description:** Creates a new folder.
* **Request Body (JSON):** `{ "parentFolderId": 0, "name": "My Folder" }`
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**


#### 20. Moves a folder

* **Method:** `PUT`
* **Endpoint:** `/crm/v3/lists/folders/{folderId}/move/{newParentFolderId}`
* **Description:** Moves a folder to a new parent folder.
* **Parameters:**
    * `folderId`: (required) ID of the folder to move.
    * `newParentFolderId`: (required) ID of the new parent folder.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**


#### 21. Moves a list to a given folder

* **Method:** `PUT`
* **Endpoint:** `/crm/v3/lists/folders/move-list`
* **Description:** Moves a list to a specified folder.
* **Request Body (JSON):** `{ "listId": "listId", "newFolderId": "folderId" }`
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**


#### 22. Rename a folder

* **Method:** `PUT`
* **Endpoint:** `/crm/v3/lists/folders/{folderId}/rename`
* **Description:** Renames a folder.
* **Parameters:**
    * `folderId`: (required) ID of the folder to rename.
* **Request Body (JSON):** `{ "name": "New Folder Name" }`
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**


#### 23. Deletes a folder

* **Method:** `DELETE`
* **Endpoint:** `/crm/v3/lists/folders/{folderId}`
* **Description:** Deletes a folder.
* **Parameters:**
    * `folderId`: (required) ID of the folder to delete.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**


### Mapping (Temporary - Expires May 30, 2025)

#### 24. Translate Legacy List Id to Modern List Id

* **Method:** `GET`
* **Endpoint:** `/crm/v3/lists/idmapping`
* **Description:** Translates a single legacy list ID to a modern ID.
* **Parameters:** `legacyListId`: (required) The legacy list ID.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**


#### 25. Translate Legacy List Id to Modern List Id in Batch

* **Method:** `POST`
* **Endpoint:** `/crm/v3/lists/idmapping`
* **Description:** Translates multiple legacy list IDs to modern IDs (max 10,000).
* **Request Body (JSON):** `["legacyListId1", "legacyListId2", ...]`
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**


**Note:**  Replace placeholders like `{listId}`, `{objectTypeId}`, etc., with actual values.  Refer to the official HubSpot API documentation for detailed schema information and error handling.  Remember to replace `"YOUR_ACCESS_TOKEN"` with your actual HubSpot access token.
