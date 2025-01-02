# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, allowing management of list memberships for object lists.  Requires either Marketing Hub Starter or Content Hub Starter or higher.

## Use Cases

* Bulk adding contacts to a list.
* Removing company records from a company list.


## API Endpoints

The API uses standard HTTP methods (GET, POST, PUT, DELETE) and requires authentication via Private Apps or OAuth.  All endpoints are located under the base URL `https://api.hubapi.com/crm/v3/lists/`.  Replace `YOUR_ACCESS_TOKEN` with your actual access token.  Standard API rate limits apply to all endpoints.

**Authentication:**  All examples below assume you've already obtained an access token.  You'll need to include the `Authorization: Bearer YOUR_ACCESS_TOKEN` header in your requests.

### Lists

#### 1. Fetch List by ID (GET)

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** GET
* **Description:** Fetches a single list by its ILS list ID.
* **Parameters:**
    * `listId` (required): The ID of the list to fetch.
    * `includeFilters` (optional, boolean, default: `true`): Whether to include filter information in the response.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/listId?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):**  *(Schema varies depending on `includeFilters`)*  Response will contain list details including name, ID, object type, etc.


#### 2. Fetch List by Name (GET)

* **Endpoint:** `/crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}`
* **Method:** GET
* **Description:** Fetches a single list by list name and object type.
* **Parameters:**
    * `objectTypeId` (required): The ID of the object type.
    * `listName` (required): The name of the list.
    * `includeFilters` (optional, boolean, default: `true`): Whether to include filter information in the response.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/object-type-id/objectTypeId/name/listName?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):** *(Schema varies depending on `includeFilters`)* Response will contain list details.


#### 3. Fetch Multiple Lists (GET)

* **Endpoint:** `/crm/v3/lists/`
* **Method:** GET
* **Description:** Fetches multiple lists by their ILS list IDs.
* **Parameters:**
    * `listId` (required, array): An array of list IDs to fetch.
    * `includeFilters` (optional, boolean, default: `true`): Whether to include filter information in the response.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/?includeFilters=false&listId=123,456' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):** An array of list details.


#### 4. Create List (POST)

* **Endpoint:** `/crm/v3/lists/`
* **Method:** POST
* **Description:** Creates a new list.
* **Parameters:**  *(Body parameters in JSON)*
    * `objectTypeId`: (required, string)  The type of objects in the list (e.g., "contacts").
    * `processingType`: (required, string)  The processing type of the list (e.g., "DYNAMIC", "MANUAL", "SNAPSHOT").
    * `customProperties`: (optional, object) Custom properties for the list.
    * `listFolderId`: (optional, integer) ID of the folder to place the list in.
    * `name`: (required, string) The name of the list.
    * `filterBranch`: (required if `processingType` is "DYNAMIC", object) Filter definition for dynamic lists.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`
* **Example Request (cURL):**
```bash
curl --request POST \
     --url https://api.hubapi.com/crm/v3/lists/ \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{
               "objectTypeId": "contacts",
               "processingType": "MANUAL",
               "name": "My New List"
             }'
```
* **Example Response (HTTP 200):**  The created list object.


#### 5. Search Lists (POST)

* **Endpoint:** `/crm/v3/lists/search`
* **Method:** POST
* **Description:** Searches lists by name or paginates through all lists.
* **Parameters:** *(Body parameters in JSON)*
    * `listIds`: (optional, array) Array of list IDs to filter by.
    * `offset`: (optional, integer) Pagination offset.
    * `query`: (optional, string) Search query.
    * `count`: (optional, integer) Number of results to return.
    * `processingTypes`: (optional, array) Array of processing types to filter by.
    * `additionalProperties`: (optional, array) Array of additional properties to filter by.
    * `sort`: (optional, string) Sorting criteria.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request POST \
     --url https://api.hubapi.com/crm/v3/lists/search \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{"query": "My List"}'
```
* **Example Response (HTTP 200):**  An array of matching lists.


#### 6. Restore a List (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/restore`
* **Method:** PUT
* **Description:** Restores a previously deleted list.  Only works within 90 days of deletion.
* **Parameters:**
    * `listId` (required): The ID of the list to restore.
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
* **Method:** PUT
* **Description:** Updates the filter definition of a DYNAMIC list.
* **Parameters:**
    * `listId` (required): The ID of the list to update.
    * `enrollObjectsInWorkflows` (optional, boolean, default: `true`): Whether to enroll objects in workflows.
    * `filterBranch`: (required, object) The updated filter branch definition.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request PUT \
     --url 'https://api.hubapi.com/crm/v3/lists/listId/update-list-filters?enrollObjectsInWorkflows=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{ "filterBranch": { "filterBranchType": "OR", "filterBranchOperator": "string" } }'
```
* **Example Response (HTTP 200):**  The updated list object.


#### 8. Update List Name (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/update-list-name`
* **Method:** PUT
* **Description:** Updates the name of a list.  The name must be globally unique.
* **Parameters:**
    * `listId` (required): The ID of the list to update.
    * `name`: (required, string) The new name for the list.
    * `includeFilters` (optional, boolean, default: `true`): Whether to include filter information in the response.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request PUT \
     --url 'https://api.hubapi.com/crm/v3/lists/listId/update-list-name?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{ "name": "New List Name" }'
```
* **Example Response (HTTP 200):** The updated list object.


#### 9. Delete a List (DELETE)

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** DELETE
* **Description:** Deletes a list.  List can be restored within 90 days.
* **Parameters:**
    * `listId` (required): The ID of the list to delete.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request DELETE \
     --url https://api.hubapi.com/crm/v3/lists/listId \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 204):** No content.


### Memberships

**(Note:  The following endpoints only work for lists with `processingType` of MANUAL or SNAPSHOT and, in some cases,  membership limits may apply.)**

#### 10. Fetch List Memberships Ordered by Added to List Date (GET)

* **Endpoint:** `/crm/v3/lists/{listId}/memberships/join-order`
* **Method:** GET
* **Description:** Fetches list memberships ordered by join date.
* **Parameters:**
    * `listId` (required): The ID of the list.
    * `limit`: (optional, integer) Number of memberships to return.
    * `after`: (optional, string) Offset ID to start fetching after.
    * `before`: (optional, string) Offset ID to start fetching before.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/listId/memberships/join-order?limit=100' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):** Array of memberships, ordered by join date.


#### 11. Fetch List Memberships Ordered by ID (GET)

* **Endpoint:** `/crm/v3/lists/{listId}/memberships`
* **Method:** GET
* **Description:** Fetches list memberships ordered by record ID.
* **Parameters:**
    * `listId` (required): The ID of the list.
    * `limit`: (optional, integer) Number of memberships to return.
    * `after`: (optional, string) Offset ID to start fetching after.
    * `before`: (optional, string) Offset ID to start fetching before.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/listId/memberships?limit=100' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):** Array of memberships, ordered by record ID.


#### 12. Get lists record is member of (GET)

* **Endpoint:** `/crm/v3/lists/records/{objectTypeId}/{recordId}/memberships`
* **Method:** GET
* **Description:** Gets the lists a record is a member of.
* **Parameters:**
    * `objectTypeId`: (required) The type of object.
    * `recordId`: (required) The ID of the record.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
     --url https://api.hubapi.com/crm/v3/lists/records/objectTypeId/recordId/memberships \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):** Array of lists the record belongs to.


#### 13. Add All Records from a Source List to a Destination List (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/memberships/add-from/{sourceListId}`
* **Method:** PUT
* **Description:** Adds all records from a source list to a destination list.  Ignores existing members.
* **Parameters:**
    * `listId` (required): The ID of the destination list.
    * `sourceListId` (required): The ID of the source list.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request PUT \
     --url https://api.hubapi.com/crm/v3/lists/listId/memberships/add-from/sourceListId \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 204):** No content.


#### 14. Add and/or Remove Records from a List (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/memberships/add-and-remove`
* **Method:** PUT
* **Description:** Adds and/or removes records from a list.
* **Parameters:** *(Body parameters in JSON)*
    * `listId` (required): The ID of the list.
    * `recordIdsToAdd`: (required, array): Array of record IDs to add.
    * `recordIdsToRemove`: (required, array): Array of record IDs to remove.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request PUT \
     --url https://api.hubapi.com/crm/v3/lists/listId/memberships/add-and-remove \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{
               "recordIdsToAdd": [123, 456],
               "recordIdsToRemove": [654]
             }'
```
* **Example Response (HTTP 200):**  Result of the operation.


#### 15. Add Records to a List (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/memberships/add`
* **Method:** PUT
* **Description:** Adds records to a list. Ignores non-existent or existing records.
* **Parameters:** *(Body parameters in JSON)*
    * `listId` (required): The ID of the list.
    * `recordIdsToAdd`: (required, array): Array of record IDs to add.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request PUT \
     --url https://api.hubapi.com/crm/v3/lists/listId/memberships/add \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '[123, 456]'
```
* **Example Response (HTTP 200):** Result of the operation.


#### 16. Remove Records from a List (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/memberships/remove`
* **Method:** PUT
* **Description:** Removes records from a list. Ignores non-existent or non-member records.
* **Parameters:** *(Body parameters in JSON)*
    * `listId` (required): The ID of the list.
    * `recordIdsToRemove`: (required, array): Array of record IDs to remove.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request PUT \
     --url https://api.hubapi.com/crm/v3/lists/listId/memberships/remove \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '[654]'
```
* **Example Response (HTTP 200):** Result of the operation.


#### 17. Delete All Records from a List (DELETE)

* **Endpoint:** `/crm/v3/lists/{listId}/memberships`
* **Method:** DELETE
* **Description:** Removes all records from a list (but does not delete the list itself).
* **Parameters:**
    * `listId` (required): The ID of the list.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request DELETE \
     --url https://api.hubapi.com/crm/v3/lists/listId/memberships \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 204):** No content.


### Folders

#### 18. Retrieves a folder (GET)

* **Endpoint:** `/crm/v3/lists/folders`
* **Method:** GET
* **Description:** Retrieves a folder and its child folders.
* **Parameters:**
    * `folderId`: (optional, integer, default: 0) The ID of the folder to retrieve. If omitted, returns the root folder.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/folders?folderId=0' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):** Folder details including name, ID, parent ID, and child folders.


#### 19. Creates a folder (POST)

* **Endpoint:** `/crm/v3/lists/folders`
* **Method:** POST
* **Description:** Creates a new folder.
* **Parameters:** *(Body parameters in JSON)*
    * `parentFolderId`: (required, string) The ID of the parent folder.
    * `name`: (required, string) The name of the folder.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request POST \
     --url https://api.hubapi.com/crm/v3/lists/folders \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{
               "parentFolderId": "0",
               "name": "My New Folder"
             }'
```
* **Example Response (HTTP 200):** The created folder object.


#### 20. Moves a folder (PUT)

* **Endpoint:** `/crm/v3/lists/folders/{folderId}/move/{newParentFolderId}`
* **Method:** PUT
* **Description:** Moves a folder to a new parent folder.
* **Parameters:**
    * `folderId`: (required) The ID of the folder to move.
    * `newParentFolderId`: (required) The ID of the new parent folder.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request PUT \
     --url https://api.hubapi.com/crm/v3/lists/folders/folderId/move/newParentFolderId \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):** The moved folder object.


#### 21. Moves a list to a given folder (PUT)

* **Endpoint:** `/crm/v3/lists/folders/move-list`
* **Method:** PUT
* **Description:** Moves a list to a specified folder.
* **Parameters:** *(Body parameters in JSON)*
    * `listId`: (required, string) The ID of the list to move.
    * `newFolderId`: (required, string) The ID of the new folder.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request PUT \
     --url https://api.hubapi.com/crm/v3/lists/folders/move-list \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{
               "listId": "listId",
               "newFolderId": "newFolderId"
             }'
```
* **Example Response (HTTP 204):** No content.


#### 22. Rename a folder (PUT)

* **Endpoint:** `/crm/v3/lists/folders/{folderId}/rename`
* **Method:** PUT
* **Description:** Renames a folder.
* **Parameters:**
    * `folderId`: (required) The ID of the folder to rename.
    * `name`: (required, string) The new name of the folder.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request PUT \
     --url https://api.hubapi.com/crm/v3/lists/folders/folderId/rename \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{ "name": "Renamed Folder" }'
```
* **Example Response (HTTP 200):** The renamed folder object.


#### 23. Deletes a folder (DELETE)

* **Endpoint:** `/crm/v3/lists/folders/{folderId}`
* **Method:** DELETE
* **Description:** Deletes a folder.
* **Parameters:**
    * `folderId`: (required) The ID of the folder to delete.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request DELETE \
     --url https://api.hubapi.com/crm/v3/lists/folders/folderId \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 204):** No content.


### Mapping (Legacy ID Translation - Expires May 30, 2025)

#### 24. Translate Legacy List Id to Modern List Id (GET)

* **Endpoint:** `/crm/v3/lists/idmapping`
* **Method:** GET
* **Description:** Translates a single legacy list ID to a modern list ID.
* **Parameters:**
    * `legacyId`: (required, string) The legacy list ID.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
     --url https://api.hubapi.com/crm/v3/lists/idmapping?legacyId=legacyId \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):** The modern list ID.


#### 25. Translate Legacy List Id to Modern List Id in Batch (POST)

* **Endpoint:** `/crm/v3/lists/idmapping`
* **Method:** POST
* **Description:** Translates multiple legacy list IDs to modern list IDs (max 10,000).
* **Parameters:** *(Body parameters in JSON)*
    * `legacyIds`: (required, array) Array of legacy list IDs.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request POST \
     --url https://api.hubapi.com/crm/v3/lists/idmapping \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '["legacyId1", "legacyId2"]'
```
* **Example Response (HTTP 200):** An array of modern list IDs, corresponding to the input legacy IDs.


**Note:**  Replace placeholders like `listId`, `objectTypeId`, `listName`, `sourceListId`, `folderId`, `newParentFolderId`, `legacyId`, etc. with your actual values.  The response schemas are not provided in the original text and would need to be obtained from the HubSpot API documentation or by making test calls.  Error handling and detailed response codes should also be checked in the official HubSpot API documentation.
