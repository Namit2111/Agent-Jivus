# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, allowing management of list memberships for object lists.  The API requires either Marketing Hub Starter or Content Hub Starter or higher.

## Use Cases

* Bulk adding contacts to a list.
* Removing company records from a company list.

## Authentication

All API calls require authentication using either private apps or OAuth.  Replace `YOUR_ACCESS_TOKEN` with your actual access token in the examples below.


## API Endpoints

### Lists

**1. Fetch List by ID (GET)**

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** `GET`
* **Description:** Fetches a single list by its ILS list ID.
* **Parameters:**
    * `listId`: (required) The ID of the list to retrieve.
    * `includeFilters`: (optional, boolean) Whether to include filter definitions. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
  ```bash
  curl --request GET \
       --url 'https://api.hubapi.com/crm/v3/lists/listId?includeFilters=false' \
       --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
  ```
* **Example Response:** (JSON -  structure will vary based on list data)
  ```json
  {
    "id": "123",
    "name": "My List",
    "objectTypeId": "contacts",
    // ... other list properties
  }
  ```

**2. Fetch List by Name (GET)**

* **Endpoint:** `/crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}`
* **Method:** `GET`
* **Description:** Fetches a single list by list name and object type.
* **Parameters:**
    * `objectTypeId`: (required) The type of object the list contains (e.g., "contacts", "companies").
    * `listName`: (required) The name of the list.
    * `includeFilters`: (optional, boolean) Whether to include filter definitions. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
  ```bash
  curl --request GET \
       --url 'https://api.hubapi.com/crm/v3/lists/object-type-id/contacts/name/MyList?includeFilters=false' \
       --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
  ```


**3. Fetch Multiple Lists (GET)**

* **Endpoint:** `/crm/v3/lists/`
* **Method:** `GET`
* **Description:** Fetches multiple lists by providing a comma-separated list of ILS list IDs.
* **Parameters:**
    * `listId`: (required) Comma-separated list of list IDs to retrieve.
    * `includeFilters`: (optional, boolean) Whether to include filter definitions. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
  ```bash
  curl --request GET \
       --url 'https://api.hubapi.com/crm/v3/lists/?listId=123,456&includeFilters=false' \
       --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
  ```

**4. Create List (POST)**

* **Endpoint:** `/crm/v3/lists/`
* **Method:** `POST`
* **Description:** Creates a new list.
* **Parameters:** (sent in JSON body)
    * `objectTypeId`: (required) Type of object (e.g., "contacts").
    * `processingType`: (required) Processing type ("MANUAL" or "SNAPSHOT").
    * `customProperties`: (optional) Custom properties.
    * `listFolderId`: (optional, integer) ID of the folder to place the list in.
    * `name`: (required) Name of the list.
    * `filterBranch`: (optional, for dynamic lists) Filter definition.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`
* **Example Request (cURL):**
  ```bash
  curl --request POST \
       --url https://api.hubapi.com/crm/v3/lists/ \
       --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
       --header 'content-type: application/json' \
       --data '{ "objectTypeId": "contacts", "processingType": "MANUAL", "name": "New List" }'
  ```

**5. Search Lists (POST)**

* **Endpoint:** `/crm/v3/lists/search`
* **Method:** `POST`
* **Description:** Searches lists by name or pages through all lists.
* **Parameters:** (sent in JSON body)
    * `listIds`: (optional) Array of list IDs to filter by.
    * `offset`: (optional, integer) Offset for pagination.
    * `query`: (optional) Search query.
    * `count`: (optional, integer) Number of results per page.
    * `processingTypes`: (optional) Array of processing types to filter by.
    * `additionalProperties`: (optional) Array of additional properties to filter by.
    * `sort`: (optional) Sorting criteria.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
  ```bash
  curl --request POST \
       --url https://api.hubapi.com/crm/v3/lists/search \
       --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
       --header 'content-type: application/json' \
       --data '{ "query": "My List" }'
  ```

**6. Restore a List (PUT)**

* **Endpoint:** `/crm/v3/lists/{listId}/restore`
* **Method:** `PUT`
* **Description:** Restores a previously deleted list.
* **Parameters:**
    * `listId`: (required) The ID of the list to restore.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`
* **Example Request (cURL):**
  ```bash
  curl --request PUT \
       --url https://api.hubapi.com/crm/v3/lists/listId/restore \
       --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
  ```

**7. Update List Filter Definition (PUT)**

* **Endpoint:** `/crm/v3/lists/{listId}/update-list-filters`
* **Method:** `PUT`
* **Description:** Updates the filter definition of a DYNAMIC list.
* **Parameters:**
    * `listId`: (required) The ID of the list to update.
    * `enrollObjectsInWorkflows`: (optional, boolean) Whether to enroll objects in workflows. Defaults to `false`.
    * `filterBranch`: (required) The new filter definition (JSON).
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`
* **Example Request (cURL):**
  ```bash
  curl --request PUT \
       --url 'https://api.hubapi.com/crm/v3/lists/listId/update-list-filters?enrollObjectsInWorkflows=false' \
       --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
       --header 'content-type: application/json' \
       --data '{ "filterBranch": { "filterBranchType": "OR", "filterBranchOperator": "string" } }'
  ```

**8. Update List Name (PUT)**

* **Endpoint:** `/crm/v3/lists/{listId}/update-list-name`
* **Method:** `PUT`
* **Description:** Updates the name of a list.
* **Parameters:**
    * `listId`: (required) The ID of the list to update.
    * `name`: (required) The new name of the list.
    * `includeFilters`: (optional, boolean) Whether to include filter definitions. Defaults to `false`.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`
* **Example Request (cURL):**
  ```bash
  curl --request PUT \
       --url 'https://api.hubapi.com/crm/v3/lists/listId/update-list-name?includeFilters=false' \
       --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
       --header 'content-type: application/json' \
       --data '{ "name": "New List Name" }'
  ```


**9. Delete a List (DELETE)**

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** `DELETE`
* **Description:** Deletes a list.  Lists can be restored within 90 days.
* **Parameters:**
    * `listId`: (required) The ID of the list to delete.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`
* **Example Request (cURL):**
  ```bash
  curl --request DELETE \
       --url https://api.hubapi.com/crm/v3/lists/listId \
       --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
  ```



### Memberships

**(The following endpoints related to memberships operate on lists with `processingType` of `MANUAL` or `SNAPSHOT` and have limitations on the number of memberships.)**

**1. Fetch List Memberships Ordered by Added to List Date (GET)**

* **Endpoint:** `/crm/v3/lists/{listId}/memberships/join-order`
* **Method:** `GET`
* **Description:** Fetches list memberships ordered by join date.
* **Parameters:**
    * `listId`: (required) The ID of the list.
    * `limit`: (optional, integer) Number of results to return.
    * `after`: (optional) Cursor for pagination (after).
    * `before`: (optional) Cursor for pagination (before).
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
  ```bash
  curl --request GET \
       --url 'https://api.hubapi.com/crm/v3/lists/listId/memberships/join-order?limit=100' \
       --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
  ```


**2. Fetch List Memberships Ordered by ID (GET)**

* **Endpoint:** `/crm/v3/lists/{listId}/memberships`
* **Method:** `GET`
* **Description:** Fetches list memberships ordered by record ID.
* **Parameters:**  Similar to above, using `limit`, `after`, `before`.
* **Scopes:** `crm.lists.read`


**3. Get lists record is member of (GET)**

* **Endpoint:** `/crm/v3/lists/records/{objectTypeId}/{recordId}/memberships`
* **Method:** `GET`
* **Description:** Retrieves lists a record is a member of.
* **Parameters:**
    * `objectTypeId`: (required) Object type ID.
    * `recordId`: (required) Record ID.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
  ```bash
  curl --request GET \
       --url https://api.hubapi.com/crm/v3/lists/records/contacts/123/memberships \
       --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
  ```

**4. Add All Records from a Source List to a Destination List (PUT)**

* **Endpoint:** `/crm/v3/lists/{listId}/memberships/add-from/{sourceListId}`
* **Method:** `PUT`
* **Description:** Adds all records from a source list to a destination list.
* **Parameters:**
    * `listId`: (required) Destination list ID.
    * `sourceListId`: (required) Source list ID.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`


**5. Add and/or Remove Records from a List (PUT)**

* **Endpoint:** `/crm/v3/lists/{listId}/memberships/add-and-remove`
* **Method:** `PUT`
* **Description:** Add and/or remove records from a list.
* **Parameters:** (sent in JSON body)
    * `recordIdsToRemove`: (required) Array of record IDs to remove.
    * `recordIdsToAdd`: (required) Array of record IDs to add.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`
* **Example Request (cURL):**
  ```bash
  curl --request PUT \
       --url https://api.hubapi.com/crm/v3/lists/listId/memberships/add-and-remove \
       --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
       --header 'content-type: application/json' \
       --data '{ "recordIdsToRemove": [654], "recordIdsToAdd": [123, 456, 789] }'
  ```

**6. Add Records to a List (PUT)**

* **Endpoint:** `/crm/v3/lists/{listId}/memberships/add`
* **Method:** `PUT`
* **Description:** Adds records to a list.
* **Parameters:** (sent in JSON body)  Array of record IDs.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`

**7. Remove Records from a List (PUT)**

* **Endpoint:** `/crm/v3/lists/{listId}/memberships/remove`
* **Method:** `PUT`
* **Description:** Removes records from a list.
* **Parameters:** (sent in JSON body) Array of record IDs.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`

**8. Delete All Records from a List (DELETE)**

* **Endpoint:** `/crm/v3/lists/{listId}/memberships`
* **Method:** `DELETE`
* **Description:** Removes all records from a list (list itself remains).
* **Parameters:**
    * `listId`: (required) The ID of the list.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`



### Folders

**1. Retrieves a folder (GET)**

* **Endpoint:** `/crm/v3/lists/folders`
* **Method:** `GET`
* **Description:** Retrieves a folder and its child folders.
* **Parameters:**
    * `folderId`: (optional, integer) The ID of the folder to retrieve. Defaults to 0 (root folder).
* **Scopes:** `crm.lists.read`

**2. Creates a folder (POST)**

* **Endpoint:** `/crm/v3/lists/folders`
* **Method:** `POST`
* **Description:** Creates a new folder.
* **Parameters:** (sent in JSON body)
    * `parentFolderId`: (required) The ID of the parent folder.
    * `name`: (required) The name of the new folder.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`

**3. Moves a folder (PUT)**

* **Endpoint:** `/crm/v3/lists/folders/{folderId}/move/{newParentFolderId}`
* **Method:** `PUT`
* **Description:** Moves a folder to a new parent folder.
* **Parameters:**
    * `folderId`: (required) The ID of the folder to move.
    * `newParentFolderId`: (required) The ID of the new parent folder.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`

**4. Moves a list to a given folder (PUT)**

* **Endpoint:** `/crm/v3/lists/folders/move-list`
* **Method:** `PUT`
* **Description:** Moves a list to a specified folder.
* **Parameters:** (sent in JSON body)
    * `listId`: (required) The ID of the list to move.
    * `newFolderId`: (required) The ID of the new folder.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`

**5. Rename a folder (PUT)**

* **Endpoint:** `/crm/v3/lists/folders/{folderId}/rename`
* **Method:** `PUT`
* **Description:** Renames a folder.
* **Parameters:**
    * `folderId`: (required) The ID of the folder to rename.
    * `name`: (required) The new name of the folder.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`

**6. Deletes a folder (DELETE)**

* **Endpoint:** `/crm/v3/lists/folders/{folderId}`
* **Method:** `DELETE`
* **Description:** Deletes a folder.
* **Parameters:**
    * `folderId`: (required) The ID of the folder to delete.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`


### Mapping (Temporary - expires May 30, 2025)

**1. Translate Legacy List Id to Modern List Id (GET)**

* **Endpoint:** `/crm/v3/lists/idmapping`
* **Method:** `GET`
* **Description:** Translates a legacy list ID to a modern list ID.
* **Parameters:**
    * `legacyListId`: (required) The legacy list ID.
* **Scopes:** `crm.lists.read`

**2. Translate Legacy List Id to Modern List Id in Batch (POST)**

* **Endpoint:** `/crm/v3/lists/idmapping`
* **Method:** `POST`
* **Description:** Translates multiple legacy list IDs to modern list IDs (max 10,000).
* **Parameters:** (sent in JSON body) Array of legacy list IDs.
* **Scopes:** `crm.lists.read`


**Note:**  Response examples and schemas are omitted for brevity but are available in the original documentation.  Error handling and detailed response codes are also not included here but should be considered in a production implementation.  Always refer to the official HubSpot API documentation for the most up-to-date information.
