# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, allowing management of list memberships for object lists.  Requires either Marketing Hub Starter or Content Hub Starter or higher.

## Use Cases

* Bulk adding contacts to a list.
* Removing company records from a company list.

## Related Guide

[HubSpot Lists Guide](<Insert_Link_Here>)


## API Endpoints

All endpoints use `https://api.hubapi.com/crm/v3/lists/` as a base URL.  Requires authentication via `Bearer YOUR_ACCESS_TOKEN` in the `Authorization` header.  Standard API rate limits apply.

**Authentication:** Private apps and OAuth are supported.

### Lists

#### 1. Fetch List by ID (GET)

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** `GET`
* **Description:** Fetches a single list by its ILS list ID.
* **Parameters:**
    * `listId` (required): The ILS list ID.
    * `includeFilters`: (optional, boolean)  Whether to include filter definitions in the response. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
--url 'https://api.hubapi.com/crm/v3/lists/listId?includeFilters=false' \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):**  *(JSON response showing list details)*


#### 2. Fetch List by Name (GET)

* **Endpoint:** `/crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}`
* **Method:** `GET`
* **Description:** Fetches a single list by its name and object type.
* **Parameters:**
    * `objectTypeId` (required): The object type ID.
    * `listName` (required): The list name.
    * `includeFilters`: (optional, boolean) Whether to include filter definitions in the response. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
--url 'https://api.hubapi.com/crm/v3/lists/object-type-id/objectTypeId/name/listName?includeFilters=false' \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):** *(JSON response showing list details)*


#### 3. Fetch Multiple Lists (GET)

* **Endpoint:** `/crm/v3/lists/`
* **Method:** `GET`
* **Description:** Fetches multiple lists by their ILS list IDs.
* **Parameters:**
    * `listId` (required): Comma-separated list of ILS list IDs.
    * `includeFilters`: (optional, boolean) Whether to include filter definitions in the response. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
--url 'https://api.hubapi.com/crm/v3/lists/?includeFilters=false' \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):** *(JSON response showing list details for each provided ID)*


#### 4. Create List (POST)

* **Endpoint:** `/crm/v3/lists/`
* **Method:** `POST`
* **Description:** Creates a new list.
* **Parameters:** (Request Body - JSON)
    * `objectTypeId`: (required) string, e.g., "contacts"
    * `processingType`: (required) string, e.g., "DYNAMIC", "MANUAL", "SNAPSHOT"
    * `customProperties`: (optional) Object of custom properties.
    * `listFolderId`: (optional, integer)  ID of the folder to place the list in. Defaults to 0 (root).
    * `name`: (required) string
    * `filterBranch`: (required for DYNAMIC lists) Object defining the filter branch.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`
* **Example Request (cURL):**
```bash
curl --request POST \
--url https://api.hubapi.com/crm/v3/lists/ \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
--header 'content-type: application/json' \
--data '{
"objectTypeId": "contacts",
"processingType": "DYNAMIC",
"customProperties": { "prop1": "value1" },
"listFolderId": 0,
"name": "My New List",
"filterBranch": { "filterBranchType": "OR", "filterBranchOperator": "AND" }
}'
```
* **Example Response (HTTP 200):** *(JSON response showing the created list details)*


#### 5. Search Lists (POST)

* **Endpoint:** `/crm/v3/lists/search`
* **Method:** `POST`
* **Description:** Searches lists by name or pages through all lists.
* **Parameters:** (Request Body - JSON)
    * `listIds`: (optional) Array of ILS list IDs.
    * `offset`: (optional, integer)  Offset for pagination.
    * `query`: (optional, string) Search query.
    * `count`: (optional, integer) Number of results to return.
    * `processingTypes`: (optional) Array of processing types to filter by.
    * `additionalProperties`: (optional) Array of additional properties to filter by.
    * `sort`: (optional, string) Sort order.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request POST \
--url https://api.hubapi.com/crm/v3/lists/search \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
--header 'content-type: application/json' \
--data '{ "query": "my list", "count": 10 }'
```
* **Example Response (HTTP 200):** *(JSON response showing the search results)*



#### 6. Restore a List (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/restore`
* **Method:** `PUT`
* **Description:** Restores a previously deleted list.  (Up to 90 days after deletion).
* **Parameters:**
    * `listId` (required): The ILS list ID.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request PUT \
--url https://api.hubapi.com/crm/v3/lists/listId/restore \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 204):** No content.


#### 7. Update List Filter Definition (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/update-list-filters`
* **Method:** `PUT`
* **Description:** Updates the filter definition of a DYNAMIC list.
* **Parameters:**
    * `listId` (required): The ILS list ID.
    * `enrollObjectsInWorkflows`: (optional, boolean) Whether to enroll objects in workflows. Defaults to `false`.
    * (Request Body - JSON): `filterBranch`: Object defining the new filter branch.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request PUT \
--url 'https://api.hubapi.com/crm/v3/lists/listId/update-list-filters?enrollObjectsInWorkflows=false' \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
--header 'content-type: application/json' \
--data '{ "filterBranch": { "filterBranchType": "OR", "filterBranchOperator": "AND" } }'
```
* **Example Response (HTTP 200):** *(JSON response, potentially showing updated list details)*


#### 8. Update List Name (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/update-list-name`
* **Method:** `PUT`
* **Description:** Updates the name of a list.  Name must be globally unique.
* **Parameters:**
    * `listId` (required): The ILS list ID.
    * `includeFilters`: (optional, boolean) Whether to include filter definitions in the response. Defaults to `false`.
    * (Request Body - JSON): `name`: The new list name (string).
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request PUT \
--url 'https://api.hubapi.com/crm/v3/lists/listId/update-list-name?includeFilters=false' \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
--header 'content-type: application/json' \
--data '{ "name": "My Updated List" }'
```
* **Example Response (HTTP 200):** *(JSON response, potentially showing updated list details)*



#### 9. Delete a List (DELETE)

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** `DELETE`
* **Description:** Deletes a list.  Restorable for 90 days.
* **Parameters:**
    * `listId` (required): The ILS list ID.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request DELETE \
--url https://api.hubapi.com/crm/v3/lists/listId \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 204):** No content.


### Memberships

#### 10. Fetch List Memberships Ordered by Added to List Date (GET)

* **Endpoint:** `/crm/v3/lists/{listId}/memberships/join-order`
* **Method:** `GET`
* **Description:** Fetches list memberships ordered by join date.
* **Parameters:**
    * `listId` (required): The ILS list ID.
    * `limit`: (optional, integer) Number of results to return (max 1000). Defaults to 100.
    * `after`: (optional, string)  Cursor for pagination (ascending order).
    * `before`: (optional, string) Cursor for pagination (descending order).
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
--url 'https://api.hubapi.com/crm/v3/lists/listId/memberships/join-order?limit=100' \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):** *(JSON response showing list memberships)*



#### 11. Fetch List Memberships Ordered by ID (GET)

* **Endpoint:** `/crm/v3/lists/{listId}/memberships`
* **Method:** `GET`
* **Description:** Fetches list memberships ordered by record ID.
* **Parameters:**  Similar to above, replacing `/join-order` with `/memberships`.
* **Scopes:** `crm.lists.read`


#### 12. Get Lists Record is Member Of (GET)

* **Endpoint:** `/crm/v3/lists/records/{objectTypeId}/{recordId}/memberships`
* **Method:** `GET`
* **Description:** Retrieves the lists a specific record is a member of.
* **Parameters:**
    * `objectTypeId` (required): The object type ID (e.g., "contacts").
    * `recordId` (required): The record ID.
* **Scopes:** `crm.lists.read`


#### 13. Add All Records from a Source List to a Destination List (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/memberships/add-from/{sourceListId}`
* **Method:** `PUT`
* **Description:** Adds all records from a source list to a destination list.  Ignores existing members.  Destination list must be MANUAL or SNAPSHOT. Source list can have any processing type.  Limited to source lists with under 100,000 memberships.
* **Parameters:**
    * `listId` (required): The ILS ID of the destination list.
    * `sourceListId` (required): The ILS ID of the source list.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`


#### 14. Add and/or Remove Records from a List (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/memberships/add-and-remove`
* **Method:** `PUT`
* **Description:** Adds and/or removes records from a list.  List must be MANUAL or SNAPSHOT.
* **Parameters:**
    * `listId` (required): The ILS list ID.
    * (Request Body - JSON):
        * `recordIdsToRemove`: Array of record IDs to remove.
        * `recordIdsToAdd`: Array of record IDs to add.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`


#### 15. Add Records to a List (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/memberships/add`
* **Method:** `PUT`
* **Description:** Adds records to a list. Ignores existing members and non-existent records. List must be MANUAL or SNAPSHOT.
* **Parameters:**
    * `listId` (required): The ILS list ID.
    * (Request Body - JSON): Array of record IDs to add.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`


#### 16. Remove Records from a List (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/memberships/remove`
* **Method:** `PUT`
* **Description:** Removes records from a list. Ignores non-existent records and records not in the list. List must be MANUAL or SNAPSHOT.
* **Parameters:** Similar to Add Records, replacing `/add` with `/remove`.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`


#### 17. Delete All Records from a List (DELETE)

* **Endpoint:** `/crm/v3/lists/{listId}/memberships`
* **Method:** `DELETE`
* **Description:** Removes all records from a list (but does not delete the list).  List must be MANUAL or SNAPSHOT, and have less than 100,000 memberships.
* **Parameters:**
    * `listId` (required): The ILS list ID.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`


### Folders

#### 18. Retrieves a Folder (GET)

* **Endpoint:** `/crm/v3/lists/folders`
* **Method:** `GET`
* **Description:** Retrieves a folder and its child folders recursively.  Only the top-level folder will have its child lists.
* **Parameters:**
    * `folderId`: (optional, integer)  The folder ID. Defaults to 0 (root).
* **Scopes:** `crm.lists.read`


#### 19. Creates a Folder (POST)

* **Endpoint:** `/crm/v3/lists/folders`
* **Method:** `POST`
* **Description:** Creates a new folder.
* **Parameters:** (Request Body - JSON)
    * `parentFolderId`: (required, string) ID of the parent folder.
    * `name`: (required, string) Name of the new folder.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`


#### 20. Moves a Folder (PUT)

* **Endpoint:** `/crm/v3/lists/folders/{folderId}/move/{newParentFolderId}`
* **Method:** `PUT`
* **Description:** Moves a folder to a new parent folder.
* **Parameters:**
    * `folderId`: (required, string) ID of the folder to move.
    * `newParentFolderId`: (required, string) ID of the new parent folder.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`


#### 21. Moves a List to a Given Folder (PUT)

* **Endpoint:** `/crm/v3/lists/folders/move-list`
* **Method:** `PUT`
* **Description:** Moves a list to a specified folder.
* **Parameters:** (Request Body - JSON)
    * `listId`: (required, string) ID of the list to move.
    * `newFolderId`: (required, string) ID of the new folder.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`


#### 22. Rename a Folder (PUT)

* **Endpoint:** `/crm/v3/lists/folders/{folderId}/rename`
* **Method:** `PUT`
* **Description:** Renames a folder.
* **Parameters:**
    * `folderId`: (required, string) ID of the folder to rename.
    * (Request Body - JSON): `name`: (required, string) New name of the folder.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`


#### 23. Deletes a Folder (DELETE)

* **Endpoint:** `/crm/v3/lists/folders/{folderId}`
* **Method:** `DELETE`
* **Description:** Deletes a folder.
* **Parameters:**
    * `folderId`: (required, string) ID of the folder to delete.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`


### Mapping (Temporary - Expires May 30, 2025)

#### 24. Translate Legacy List Id to Modern List Id (GET)

* **Endpoint:** `/crm/v3/lists/idmapping`
* **Method:** `GET`
* **Description:** Translates a legacy list ID to a modern list ID.
* **Parameters:**
    * `legacyListId`: (required, string) Legacy List ID.
* **Scopes:** `crm.lists.read`


#### 25. Translate Legacy List Id to Modern List Id in Batch (POST)

* **Endpoint:** `/crm/v3/lists/idmapping`
* **Method:** `POST`
* **Description:** Translates multiple legacy list IDs to modern list IDs (max 10,000).
* **Parameters:** (Request Body - JSON) Array of legacy List IDs.
* **Scopes:** `crm.lists.read`


**Note:**  Replace placeholders like `{listId}`, `{objectTypeId}`, `{listName}`, etc., with actual values.  Error handling and detailed response schemas are omitted for brevity but are crucial in a production implementation.  Remember to consult the official HubSpot API documentation for the most up-to-date information and complete schema details.
