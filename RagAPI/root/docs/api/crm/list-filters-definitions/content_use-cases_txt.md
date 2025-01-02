# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, allowing management of list memberships for object lists.  The API requires either Marketing Hub Starter or Content Hub Starter or higher.

## API Endpoints

All endpoints are under the base URL: `https://api.hubapi.com/crm/v3/lists/` and require an access token for authentication via the `Authorization: Bearer YOUR_ACCESS_TOKEN` header.  Responses are generally in JSON format.  Standard API rate limits apply to all endpoints.

**Authentication:**  Private apps and OAuth are supported.

### Lists Management

#### 1. Fetch List by ID (GET)

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** GET
* **Description:** Fetches a single list by its ILS list ID.
* **Parameters:**
    * `listId` (required): The ID of the list to retrieve.
    * `includeFilters` (optional, boolean):  If true, includes filter details in the response. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
  ```bash
  curl --request GET \
       --url 'https://api.hubapi.com/crm/v3/lists/listId?includeFilters=false' \
       --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
  ```
* **Example Response (HTTP 200):**  *(Schema varies depending on `includeFilters`)*  A JSON object representing the list details.


#### 2. Fetch List by Name (GET)

* **Endpoint:** `/crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}`
* **Method:** GET
* **Description:** Fetches a single list by its name and object type.
* **Parameters:**
    * `objectTypeId` (required): The type of objects in the list (e.g., contacts, companies).
    * `listName` (required): The name of the list.
    * `includeFilters` (optional, boolean): If true, includes filter details in the response. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
  ```bash
  curl --request GET \
       --url 'https://api.hubapi.com/crm/v3/lists/object-type-id/objectTypeId/name/listName?includeFilters=false' \
       --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
  ```
* **Example Response (HTTP 200):** A JSON object representing the list details.


#### 3. Fetch Multiple Lists (GET)

* **Endpoint:** `/crm/v3/lists/`
* **Method:** GET
* **Description:** Fetches multiple lists by providing a comma-separated list of `listIds`.
* **Parameters:**
    * `listId` (required): Comma separated list of IDs.
    * `includeFilters` (optional, boolean): If true, includes filter details in the response. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
  ```bash
  curl --request GET \
       --url 'https://api.hubapi.com/crm/v3/lists/?includeFilters=false&listId=123,456' \
       --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
  ```
* **Example Response (HTTP 200):** A JSON array containing details for each requested list.


#### 4. Create List (POST)

* **Endpoint:** `/crm/v3/lists/`
* **Method:** POST
* **Description:** Creates a new list.
* **Request Body (JSON):**
  ```json
  {
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
  }
  ```
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`
* **Example Request (cURL):**  *(See example in provided text)*
* **Example Response (HTTP 200):** A JSON object representing the newly created list.


#### 5. Search Lists (POST)

* **Endpoint:** `/crm/v3/lists/search`
* **Method:** POST
* **Description:** Searches lists by name or pages through all lists.
* **Request Body (JSON):**
  ```json
  {
    "listIds": ["string"],
    "offset": 0,
    "query": "string",
    "count": 0,
    "processingTypes": ["string"],
    "additionalProperties": ["string"],
    "sort": "string"
  }
  ```
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):** *(See example in provided text)*
* **Example Response (HTTP 200):** A JSON object containing the search results.


#### 6. Restore a List (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/restore`
* **Method:** PUT
* **Description:** Restores a previously deleted list (up to 90 days after deletion).
* **Parameters:**
    * `listId` (required): The ID of the list to restore.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):** *(See example in provided text)*
* **Example Response (HTTP 204):** No content.


#### 7. Update List Filter Definition (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/update-list-filters`
* **Method:** PUT
* **Description:** Updates the filter definition of a DYNAMIC list.
* **Parameters:**
    * `listId` (required): The ID of the list to update.
    * `enrollObjectsInWorkflows` (optional, boolean): If true, enrolls objects in workflows. Defaults to `false`.
* **Request Body (JSON):**  *(Similar structure to create)*
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):** *(See example in provided text)*
* **Example Response (HTTP 200):** A JSON object representing the updated list.


#### 8. Update List Name (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/update-list-name`
* **Method:** PUT
* **Description:** Updates the name of a list.
* **Parameters:**
    * `listId` (required): The ID of the list to update.
    * `includeFilters` (optional, boolean): If true, includes filter details in the response. Defaults to `false`.
* **Request Body (JSON):**  `{"name": "new name"}`
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):** *(See example in provided text)*
* **Example Response (HTTP 200):** A JSON object representing the updated list.


#### 9. Delete a List (DELETE)

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** DELETE
* **Description:** Deletes a list.  Restorable for 90 days.
* **Parameters:**
    * `listId` (required): The ID of the list to delete.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):** *(See example in provided text)*
* **Example Response (HTTP 204):** No content.


### List Memberships Management

#### 10. Fetch List Memberships Ordered by Added to List Date (GET)

* **Endpoint:** `/crm/v3/lists/{listId}/memberships/join-order`
* **Method:** GET
* **Description:** Fetches list memberships ordered by join date.  Supports pagination using `after` and `before` offsets and `limit`.
* **Parameters:**
    * `listId` (required): The ID of the list.
    * `after` (optional): Pagination offset.
    * `before` (optional): Pagination offset.
    * `limit` (optional): Number of records to return.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):** *(See example in provided text)*
* **Example Response (HTTP 200):** A JSON object with list membership details.


#### 11. Fetch List Memberships Ordered by ID (GET)

* **Endpoint:** `/crm/v3/lists/{listId}/memberships`
* **Method:** GET
* **Description:** Fetches list memberships ordered by record ID. Supports pagination using `after` and `before` offsets and `limit`.
* **Parameters:**
    * `listId` (required): The ID of the list.
    * `after` (optional): Pagination offset.
    * `before` (optional): Pagination offset.
    * `limit` (optional): Number of records to return.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):** *(See example in provided text)*
* **Example Response (HTTP 200):** A JSON object with list membership details.


#### 12. Get Lists Record is Member Of (GET)

* **Endpoint:** `/crm/v3/lists/records/{objectTypeId}/{recordId}/memberships`
* **Method:** GET
* **Description:** Gets the lists a specific record is a member of.
* **Parameters:**
    * `objectTypeId` (required): The type of the record.
    * `recordId` (required): The ID of the record.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):** *(See example in provided text)*
* **Example Response (HTTP 200):** A JSON array of list IDs.


#### 13. Add All Records from a Source List to a Destination List (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/memberships/add-from/{sourceListId}`
* **Method:** PUT
* **Description:** Adds all records from a source list to a destination list.  Ignores existing members.  Destination list must be MANUAL or SNAPSHOT. Source list can have any processingType.
* **Parameters:**
    * `listId` (required): Destination list ID.
    * `sourceListId` (required): Source list ID (limited to <100,000 members).
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):** *(See example in provided text)*
* **Example Response (HTTP 204):** No content.


#### 14. Add and/or Remove Records from a List (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/memberships/add-and-remove`
* **Method:** PUT
* **Description:** Adds and/or removes records from a list. List must be MANUAL or SNAPSHOT.
* **Parameters:**
    * `listId` (required): The list ID.
* **Request Body (JSON):**
  ```json
  {
    "recordIdsToRemove": [654],
    "recordIdsToAdd": [123, 456, 789]
  }
  ```
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):** *(See example in provided text)*
* **Example Response (HTTP 200):**  A JSON object representing the updated list membership.


#### 15. Add Records to a List (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/memberships/add`
* **Method:** PUT
* **Description:** Adds records to a list. Ignores non-existent or already existing records. List must be MANUAL or SNAPSHOT.
* **Parameters:**
    * `listId` (required): The list ID.
* **Request Body (JSON):** `["recordId1", "recordId2", ...]`
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):** *(See example in provided text)*
* **Example Response (HTTP 200):** A JSON object representing the updated list membership.


#### 16. Remove Records from a List (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/memberships/remove`
* **Method:** PUT
* **Description:** Removes records from a list. Ignores non-existent or non-member records. List must be MANUAL or SNAPSHOT.
* **Parameters:**
    * `listId` (required): The list ID.
* **Request Body (JSON):** `["recordId1", "recordId2", ...]`
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):** *(See example in provided text)*
* **Example Response (HTTP 200):** A JSON object representing the updated list membership.


#### 17. Delete All Records from a List (DELETE)

* **Endpoint:** `/crm/v3/lists/{listId}/memberships`
* **Method:** DELETE
* **Description:** Removes all records from a list (list itself remains). List must be MANUAL or SNAPSHOT and have <100,000 members.
* **Parameters:**
    * `listId` (required): The list ID.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):** *(See example in provided text)*
* **Example Response (HTTP 204):** No content.


### List Folders Management

#### 18. Retrieves a folder (GET)

* **Endpoint:** `/crm/v3/lists/folders`
* **Method:** GET
* **Description:** Retrieves a folder and its child folders recursively.
* **Parameters:**
    * `folderId` (optional):  The ID of the folder to retrieve. Defaults to 0 (root).
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):** *(See example in provided text)*
* **Example Response (HTTP 200):** A JSON object representing the folder and its contents.

#### 19. Creates a folder (POST)

* **Endpoint:** `/crm/v3/lists/folders`
* **Method:** POST
* **Description:** Creates a new folder.
* **Request Body (JSON):**
    ```json
    {
        "parentFolderId": "string",
        "name": "string"
    }
    ```
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):** *(See example in provided text)*
* **Example Response (HTTP 200):** A JSON object representing the newly created folder.


#### 20. Moves a folder (PUT)

* **Endpoint:** `/crm/v3/lists/folders/{folderId}/move/{newParentFolderId}`
* **Method:** PUT
* **Description:** Moves a folder to a new parent folder.
* **Parameters:**
    * `folderId` (required): The ID of the folder to move.
    * `newParentFolderId` (required): The ID of the new parent folder.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):** *(See example in provided text)*
* **Example Response (HTTP 200):** A JSON object representing the moved folder.


#### 21. Moves a list to a given folder (PUT)

* **Endpoint:** `/crm/v3/lists/folders/move-list`
* **Method:** PUT
* **Description:** Moves a list to a specific folder.
* **Request Body (JSON):**
    ```json
    {
        "listId": "string",
        "newFolderId": "string"
    }
    ```
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):** *(See example in provided text)*
* **Example Response (HTTP 204):** No content.


#### 22. Rename a folder (PUT)

* **Endpoint:** `/crm/v3/lists/folders/{folderId}/rename`
* **Method:** PUT
* **Description:** Renames a folder.
* **Parameters:**
    * `folderId` (required): The ID of the folder to rename.
* **Request Body (JSON):** `{"name": "new name"}`
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):** *(See example in provided text)*
* **Example Response (HTTP 200):** A JSON object representing the renamed folder.


#### 23. Deletes a folder (DELETE)

* **Endpoint:** `/crm/v3/lists/folders/{folderId}`
* **Method:** DELETE
* **Description:** Deletes a folder.
* **Parameters:**
    * `folderId` (required): The ID of the folder to delete.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):** *(See example in provided text)*
* **Example Response (HTTP 204):** No content.


### Legacy List ID Mapping (Temporary - Expires May 30, 2025)

#### 24. Translate Legacy List Id to Modern List Id (GET)

* **Endpoint:** `/crm/v3/lists/idmapping`
* **Method:** GET
* **Description:** Translates a single legacy list ID to a modern list ID.
* **Parameters:**
    * `legacyListId` (required): The legacy list ID.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):** *(See example in provided text)*
* **Example Response (HTTP 200):** A JSON object containing the mapping.


#### 25. Translate Legacy List Id to Modern List Id in Batch (POST)

* **Endpoint:** `/crm/v3/lists/idmapping`
* **Method:** POST
* **Description:** Translates multiple legacy list IDs to modern list IDs (max 10,000).
* **Request Body (JSON):** `["legacyListId1", "legacyListId2", ...]`
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):** *(See example in provided text)*
* **Example Response (HTTP 200):** A JSON array containing the mappings.


This documentation provides a comprehensive overview of the HubSpot Lists API v3.  Remember to replace placeholders like `{listId}`, `objectTypeId`, etc., with actual values.  Always refer to the official HubSpot API documentation for the most up-to-date information and schema details.
