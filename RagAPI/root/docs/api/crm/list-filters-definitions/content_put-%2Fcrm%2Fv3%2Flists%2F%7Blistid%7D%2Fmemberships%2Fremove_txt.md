# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, allowing management of list memberships for object lists.  It requires either Marketing Hub Starter or Content Hub Starter or higher.

## Use Cases

* Bulk adding contacts to a list.
* Removing company records from a company list.

## Authentication

All API calls require authentication using either Private Apps or OAuth 2.0.  The `authorization: Bearer YOUR_ACCESS_TOKEN` header must be included in all requests, replacing `YOUR_ACCESS_TOKEN` with your actual access token.

## Rate Limits

Standard HubSpot API rate limits apply.


## API Endpoints

### Lists

#### 1. Fetch List by ID (GET)

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** `GET`
* **Description:** Fetches a single list by its ILS list ID.
* **Parameters:**
    * `listId`: (required) The ID of the list to retrieve.
    * `includeFilters`: (optional, boolean)  If `true`, includes filter definitions in the response. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**

```bash
curl --request GET \
--url 'https://api.hubapi.com/crm/v3/lists/listId?includeFilters=false' \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

* **Example Response (HTTP 200):**  *(Schema varies; see HubSpot documentation for details)*


#### 2. Fetch List by Name (GET)

* **Endpoint:** `/crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}`
* **Method:** `GET`
* **Description:** Fetches a single list by its list name and object type.
* **Parameters:**
    * `objectTypeId`: (required) The type of object the list contains (e.g., contacts, companies).
    * `listName`: (required) The name of the list.
    * `includeFilters`: (optional, boolean) If `true`, includes filter definitions in the response. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**

```bash
curl --request GET \
--url 'https://api.hubapi.com/crm/v3/lists/object-type-id/objectTypeId/name/listName?includeFilters=false' \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

* **Example Response (HTTP 200):** *(Schema varies; see HubSpot documentation for details)*


#### 3. Fetch Multiple Lists (GET)

* **Endpoint:** `/crm/v3/lists/`
* **Method:** `GET`
* **Description:** Fetches multiple lists by their ILS list IDs.
* **Parameters:**
    * `listId`: (required) Comma-separated list of list IDs.
    * `includeFilters`: (optional, boolean) If `true`, includes filter definitions in the response. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**

```bash
curl --request GET \
--url 'https://api.hubapi.com/crm/v3/lists/?includeFilters=false' \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

* **Example Response (HTTP 200):** *(Schema varies; see HubSpot documentation for details)*


#### 4. Create List (POST)

* **Endpoint:** `/crm/v3/lists/`
* **Method:** `POST`
* **Description:** Creates a new list.
* **Parameters:**  *(See request body example below)*
    * `objectTypeId`: (required) Type of object the list contains.
    * `processingType`: (required)  `MANUAL` or `SNAPSHOT`.
    * `customProperties`: (optional) Custom properties for the list.
    * `listFolderId`: (optional) ID of the folder to place the list in.
    * `name`: (required) Name of the list.
    * `filterBranch`: (optional, for dynamic lists) Filter definition.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`
* **Example Request (cURL):**

```bash
curl --request POST \
--url https://api.hubapi.com/crm/v3/lists/ \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
--header 'content-type: application/json' \
--data '{
"objectTypeId": "string",
"processingType": "string",
"customProperties": {
"additionalProp1": "string",
"additionalProp2": "string",
"additionalProp3": "string"
},
"listFolderId": 0,
"name": "string",
"filterBranch": {
"filterBranchType": "OR",
"filterBranchOperator": "string"
}
}'
```

* **Example Response (HTTP 200):** *(Schema varies; see HubSpot documentation for details)*


#### 5. Search Lists (POST)

* **Endpoint:** `/crm/v3/lists/search`
* **Method:** `POST`
* **Description:** Searches lists by name or pages through all lists.
* **Parameters:** *(See request body example below)*
    * `listIds`: (optional) Array of list IDs to filter by.
    * `offset`: (optional) Offset for pagination.
    * `query`: (optional) Search query.
    * `count`: (optional) Number of results to return.
    * `processingTypes`: (optional) Array of processing types to filter by.
    * `additionalProperties`: (optional) Array of additional properties to filter by.
    * `sort`: (optional) Sort field.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**

```bash
curl --request POST \
--url https://api.hubapi.com/crm/v3/lists/search \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
--header 'content-type: application/json' \
--data '{
"listIds": ["string"],
"offset": 0,
"query": "string",
"count": 0,
"processingTypes": ["string"],
"additionalProperties": ["string"],
"sort": "string"
}'
```

* **Example Response (HTTP 200):** *(Schema varies; see HubSpot documentation for details)*


#### 6. Restore a List (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/restore`
* **Method:** `PUT`
* **Description:** Restores a previously deleted list.  Lists can be restored up to 90 days after deletion.
* **Parameters:**
    * `listId`: (required) ID of the list to restore.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**

```bash
curl --request PUT \
--url https://api.hubapi.com/crm/v3/lists/listId/restore \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

* **Example Response (HTTP 204):** No content


#### 7. Update List Filter Definition (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/update-list-filters`
* **Method:** `PUT`
* **Description:** Updates the filter definition of a dynamic list.
* **Parameters:**
    * `listId`: (required) ID of the list to update.
    * `filterBranch`: (required) The new filter definition.
    * `enrollObjectsInWorkflows`: (optional, boolean) Whether to enroll objects in workflows. Defaults to `false`.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**

```bash
curl --request PUT \
--url 'https://api.hubapi.com/crm/v3/lists/listId/update-list-filters?enrollObjectsInWorkflows=false' \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
--header 'content-type: application/json' \
--data '{
"filterBranch": {
"filterBranchType": "OR",
"filterBranchOperator": "string"
}
}'
```

* **Example Response (HTTP 200):** *(Schema varies; see HubSpot documentation for details)*


#### 8. Update List Name (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/update-list-name`
* **Method:** `PUT`
* **Description:** Updates the name of a list.  The name must be globally unique.
* **Parameters:**
    * `listId`: (required) ID of the list to update.
    * `name`: (required) The new name of the list.
    * `includeFilters`: (optional, boolean) If `true`, includes filter definitions in the response. Defaults to `false`.

* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**

```bash
curl --request PUT \
--url 'https://api.hubapi.com/crm/v3/lists/listId/update-list-name?includeFilters=false' \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
--header 'content-type: application/json' \
--data '{"name": "New List Name"}'
```

* **Example Response (HTTP 200):** *(Schema varies; see HubSpot documentation for details)*


#### 9. Delete a List (DELETE)

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** `DELETE`
* **Description:** Deletes a list.  Lists can be restored within 90 days.
* **Parameters:**
    * `listId`: (required) ID of the list to delete.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**

```bash
curl --request DELETE \
--url https://api.hubapi.com/crm/v3/lists/listId \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

* **Example Response (HTTP 204):** No content



### Memberships

#### 10. Fetch List Memberships Ordered by Added to List Date (GET)

* **Endpoint:** `/crm/v3/lists/{listId}/memberships/join-order`
* **Method:** `GET`
* **Description:** Fetches list memberships ordered by join date.
* **Parameters:**
    * `listId`: (required) ID of the list.
    * `limit`: (optional) The maximum number of memberships to return.
    * `after`: (optional)  Cursor for pagination (after this record ID).
    * `before`: (optional) Cursor for pagination (before this record ID).
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**

```bash
curl --request GET \
--url 'https://api.hubapi.com/crm/v3/lists/listId/memberships/join-order?limit=100' \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

* **Example Response (HTTP 200):** *(Schema varies; see HubSpot documentation for details)*


#### 11. Fetch List Memberships Ordered by ID (GET)

* **Endpoint:** `/crm/v3/lists/{listId}/memberships`
* **Method:** `GET`
* **Description:** Fetches list memberships ordered by record ID.
* **Parameters:**
    * `listId`: (required) ID of the list.
    * `limit`: (optional) The maximum number of memberships to return.
    * `after`: (optional) Cursor for pagination (after this record ID).
    * `before`: (optional) Cursor for pagination (before this record ID).
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**

```bash
curl --request GET \
--url 'https://api.hubapi.com/crm/v3/lists/listId/memberships?limit=100' \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

* **Example Response (HTTP 200):** *(Schema varies; see HubSpot documentation for details)*


#### 12. Get Lists Record is Member Of (GET)

* **Endpoint:** `/crm/v3/lists/records/{objectTypeId}/{recordId}/memberships`
* **Method:** `GET`
* **Description:** Retrieves the lists a record is a member of.
* **Parameters:**
    * `objectTypeId`: (required) Type of object (e.g., contacts, companies).
    * `recordId`: (required) ID of the record.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**

```bash
curl --request GET \
--url https://api.hubapi.com/crm/v3/lists/records/objectTypeId/recordId/memberships \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

* **Example Response (HTTP 200):** *(Schema varies; see HubSpot documentation for details)*


#### 13. Add All Records from a Source List to a Destination List (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/memberships/add-from/{sourceListId}`
* **Method:** `PUT`
* **Description:** Adds all records from a source list to a destination list.  Existing members are ignored.
* **Parameters:**
    * `listId`: (required) ID of the destination list (must be MANUAL or SNAPSHOT processingType).
    * `sourceListId`: (required) ID of the source list (under 100,000 memberships).  Both lists must contain the same object type.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**

```bash
curl --request PUT \
--url https://api.hubapi.com/crm/v3/lists/listId/memberships/add-from/sourceListId \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

* **Example Response (HTTP 204):** No content


#### 14. Add and/or Remove Records from a List (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/memberships/add-and-remove`
* **Method:** `PUT`
* **Description:** Adds and/or removes records from a list.
* **Parameters:**
    * `listId`: (required) ID of the list (must be MANUAL or SNAPSHOT processingType).
    * `recordIdsToRemove`: (required) Array of record IDs to remove.
    * `recordIdsToAdd`: (required) Array of record IDs to add.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**

```bash
curl --request PUT \
--url https://api.hubapi.com/crm/v3/lists/listId/memberships/add-and-remove \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
--header 'content-type: application/json' \
--data '{
"recordIdsToRemove": [654],
"recordIdsToAdd": [123, 456, 789]
}'
```

* **Example Response (HTTP 200):** *(Schema varies; see HubSpot documentation for details)*


#### 15. Add Records to a List (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/memberships/add`
* **Method:** `PUT`
* **Description:** Adds records to a list.  Existing members and non-existent records are ignored.
* **Parameters:**
    * `listId`: (required) ID of the list (must be MANUAL or SNAPSHOT processingType).
    * `recordIdsToAdd`: (required) Array of record IDs to add.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**

```bash
curl --request PUT \
--url https://api.hubapi.com/crm/v3/lists/listId/memberships/add \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
--header 'content-type: application/json' \
--data '[ "string" ]'
```

* **Example Response (HTTP 200):** *(Schema varies; see HubSpot documentation for details)*


#### 16. Remove Records from a List (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/memberships/remove`
* **Method:** `PUT`
* **Description:** Removes records from a list.  Non-existent and non-member records are ignored.
* **Parameters:**
    * `listId`: (required) ID of the list (must be MANUAL or SNAPSHOT processingType).
    * `recordIdsToRemove`: (required) Array of record IDs to remove.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**

```bash
curl --request PUT \
--url https://api.hubapi.com/crm/v3/lists/listId/memberships/remove \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
--header 'content-type: application/json' \
--data '[ "string" ]'
```

* **Example Response (HTTP 200):** *(Schema varies; see HubSpot documentation for details)*


#### 17. Delete All Records from a List (DELETE)

* **Endpoint:** `/crm/v3/lists/{listId}/memberships`
* **Method:** `DELETE`
* **Description:** Removes all records from a list (but not the list itself).
* **Parameters:**
    * `listId`: (required) ID of the list (must be MANUAL or SNAPSHOT processingType, and have under 100,000 memberships).
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**

```bash
curl --request DELETE \
--url https://api.hubapi.com/crm/v3/lists/listId/memberships \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

* **Example Response (HTTP 204):** No content



### Folders

#### 18. Retrieves a folder (GET)

* **Endpoint:** `/crm/v3/lists/folders`
* **Method:** `GET`
* **Description:** Retrieves a folder and its child folders recursively. Only the retrieved folder will include child lists.
* **Parameters:**
    * `folderId`: (optional) ID of the folder to retrieve. Defaults to 0 (root folder).
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**

```bash
curl --request GET \
--url 'https://api.hubapi.com/crm/v3/lists/folders?folderId=0' \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

* **Example Response (HTTP 200):** *(Schema varies; see HubSpot documentation for details)*


#### 19. Creates a folder (POST)

* **Endpoint:** `/crm/v3/lists/folders`
* **Method:** `POST`
* **Description:** Creates a new folder.
* **Parameters:**
    * `parentFolderId`: (required) ID of the parent folder.
    * `name`: (required) Name of the new folder.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**

```bash
curl --request POST \
--url https://api.hubapi.com/crm/v3/lists/folders \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
--header 'content-type: application/json' \
--data '{
"parentFolderId": "string",
"name": "string"
}'
```

* **Example Response (HTTP 200):** *(Schema varies; see HubSpot documentation for details)*


#### 20. Moves a folder (PUT)

* **Endpoint:** `/crm/v3/lists/folders/{folderId}/move/{newParentFolderId}`
* **Method:** `PUT`
* **Description:** Moves a folder to a new parent folder.
* **Parameters:**
    * `folderId`: (required) ID of the folder to move.
    * `newParentFolderId`: (required) ID of the new parent folder.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**

```bash
curl --request PUT \
--url https://api.hubapi.com/crm/v3/lists/folders/folderId/move/newParentFolderId \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

* **Example Response (HTTP 200):** *(Schema varies; see HubSpot documentation for details)*


#### 21. Moves a list to a given folder (PUT)

* **Endpoint:** `/crm/v3/lists/folders/move-list`
* **Method:** `PUT`
* **Description:** Moves a list to a specified folder.
* **Parameters:**
    * `listId`: (required) ID of the list to move.
    * `newFolderId`: (required) ID of the new folder.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**

```bash
curl --request PUT \
--url https://api.hubapi.com/crm/v3/lists/folders/move-list \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
--header 'content-type: application/json' \
--data '{
"listId": "string",
"newFolderId": "string"
}'
```

* **Example Response (HTTP 204):** No content


#### 22. Rename a folder (PUT)

* **Endpoint:** `/crm/v3/lists/folders/{folderId}/rename`
* **Method:** `PUT`
* **Description:** Renames a folder.
* **Parameters:**
    * `folderId`: (required) ID of the folder to rename.
    * `name`: (required) New name for the folder.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**

```bash
curl --request PUT \
--url https://api.hubapi.com/crm/v3/lists/folders/folderId/rename \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
--header 'content-type: application/json' \
--data '{"name": "New Folder Name"}'
```

* **Example Response (HTTP 200):** *(Schema varies; see HubSpot documentation for details)*


#### 23. Deletes a folder (DELETE)

* **Endpoint:** `/crm/v3/lists/folders/{folderId}`
* **Method:** `DELETE`
* **Description:** Deletes a folder.
* **Parameters:**
    * `folderId`: (required) ID of the folder to delete.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**

```bash
curl --request DELETE \
--url https://api.hubapi.com/crm/v3/lists/folders/folderId \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

* **Example Response (HTTP 204):** No content



### Mapping (Legacy ID Translation - Expiring May 30, 2025)

#### 24. Translate Legacy List Id to Modern List Id (GET)

* **Endpoint:** `/crm/v3/lists/idmapping`
* **Method:** `GET`
* **Description:** Translates a single legacy list ID to a modern list ID.
* **Parameters:**
    * `legacyListId`: (required) The legacy list ID.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**

```bash
curl --request GET \
--url https://api.hubapi.com/crm/v3/lists/idmapping \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
--header 'content-type: application/json' \
--data '{"legacyListId": "legacyId"}'
```

* **Example Response (HTTP 200):** *(Schema varies; see HubSpot documentation for details)*


#### 25. Translate Legacy List Id to Modern List Id in Batch (POST)

* **Endpoint:** `/crm/v3/lists/idmapping`
* **Method:** `POST`
* **Description:** Translates multiple legacy list IDs to modern list IDs (max 10,000).
* **Parameters:**
    * `legacyListIds`: (required) Array of legacy list IDs.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**

```bash
curl --request POST \
--url https://api.hubapi.com/crm/v3/lists/idmapping \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
--header 'content-type: application/json' \
--data '[ "string" ]'
```

* **Example Response (HTTP 200):** *(Schema varies; see HubSpot documentation for details)*


**Note:**  Remember to replace placeholders like `{listId}`, `objectTypeId`, `listName`,  `sourceListId`, `folderId`, `newParentFolderId`,  and `"string"` values with your actual data.  Always refer to the official HubSpot API documentation for the most up-to-date information on schemas and potential response codes.  The example responses are placeholders; the actual structure will depend on the specific API call.
