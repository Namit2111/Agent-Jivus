# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, allowing management of list memberships for object lists.  The API requires either Marketing Hub Starter or Content Hub Starter or higher.

## Authentication

All API requests require authentication.  Use either Private Apps or OAuth 2.0 with the necessary scopes.  Replace `YOUR_ACCESS_TOKEN` with your actual access token in the examples below.


## Lists Endpoints

### 1. Fetch List by ID (GET)

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** GET
* **Description:** Retrieves a single list by its ILS list ID.
* **Parameters:**
    * `listId`: (string, required) The ID of the list to retrieve.
    * `includeFilters`: (boolean, optional)  Include filter definitions in the response. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**

```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/listId?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

* **Example Response (HTTP 200):**  *(Schema omitted for brevity; refer to HubSpot documentation for details)*
  ```json
  {
    "listId": 123,
    "name": "My List",
    // ... other properties
  }
  ```


### 2. Fetch List by Name (GET)

* **Endpoint:** `/crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}`
* **Method:** GET
* **Description:** Retrieves a single list by its name and object type.
* **Parameters:**
    * `objectTypeId`: (string, required) The type of object in the list (e.g., "contacts").
    * `listName`: (string, required) The name of the list.
    * `includeFilters`: (boolean, optional) Include filter definitions. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**

```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/object-type-id/objectTypeId/name/listName?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

* **Example Response (HTTP 200):**  *(Schema omitted)*


### 3. Fetch Multiple Lists (GET)

* **Endpoint:** `/crm/v3/lists/`
* **Method:** GET
* **Description:** Retrieves multiple lists by their ILS list IDs.
* **Parameters:**
    * `listId`: (string, optional, repeatable)  List of list IDs to retrieve.  If omitted, retrieves all lists.
    * `includeFilters`: (boolean, optional) Include filter definitions. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**

```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

* **Example Response (HTTP 200):** *(Schema omitted)*


### 4. Create List (POST)

* **Endpoint:** `/crm/v3/lists/`
* **Method:** POST
* **Description:** Creates a new list.
* **Parameters:** (Request body - application/json)
    * `objectTypeId`: (string, required)  The object type of the list (e.g., "contacts").
    * `processingType`: (string, required) The processing type ("MANUAL" or "SNAPSHOT").
    * `customProperties`: (object, optional) Custom properties for the list.
    * `listFolderId`: (integer, optional) The ID of the folder to place the list in.
    * `name`: (string, required) The name of the list.
    * `filterBranch`: (object, required for DYNAMIC lists) Filter criteria.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`
* **Example Request (cURL):**

```bash
curl --request POST \
     --url https://api.hubapi.com/crm/v3/lists/ \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{ "objectTypeId": "contacts", "processingType": "MANUAL", "name": "New List", "listFolderId": 0 }'
```

* **Example Response (HTTP 200):** *(Schema omitted)*


### 5. Search Lists (POST)

* **Endpoint:** `/crm/v3/lists/search`
* **Method:** POST
* **Description:** Searches lists by name or retrieves all lists.
* **Parameters:** (Request body - application/json)
    * `listIds`: (array of strings, optional) List of IDs to filter by.
    * `offset`: (integer, optional) Pagination offset.
    * `query`: (string, optional) Search query (list name).
    * `count`: (integer, optional) Number of results to return.
    * `processingTypes`: (array of strings, optional) Processing types to filter by.
    * `additionalProperties`: (array of strings, optional) Custom properties to filter by.
    * `sort`: (string, optional) Sorting criteria.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**

```bash
curl --request POST \
     --url https://api.hubapi.com/crm/v3/lists/search \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{ "query": "my list", "count": 10 }'
```

* **Example Response (HTTP 200):** *(Schema omitted)*


### 6. Restore a List (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/restore`
* **Method:** PUT
* **Description:** Restores a deleted list (within 90 days of deletion).
* **Parameters:**
    * `listId`: (string, required) The ID of the list to restore.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**

```bash
curl --request PUT \
     --url https://api.hubapi.com/crm/v3/lists/listId/restore \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

* **Example Response (HTTP 204):** No content


### 7. Update List Filter Definition (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/update-list-filters`
* **Method:** PUT
* **Description:** Updates the filter definition of a DYNAMIC list.
* **Parameters:**
    * `listId`: (string, required) The ID of the list to update.
    * `enrollObjectsInWorkflows`: (boolean, optional) Enroll objects in workflows. Defaults to `false`.
    * `filterBranch`: (object, required) The updated filter branch definition.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**

```bash
curl --request PUT \
     --url 'https://api.hubapi.com/crm/v3/lists/listId/update-list-filters?enrollObjectsInWorkflows=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{ "filterBranch": { "filterBranchType": "OR", "filterBranchOperator": "string" } }'
```

* **Example Response (HTTP 200):** *(Schema omitted)*


### 8. Update List Name (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/update-list-name`
* **Method:** PUT
* **Description:** Updates the name of a list.
* **Parameters:**
    * `listId`: (string, required) The ID of the list to update.
    * `name`: (string, required) The new name for the list.
    * `includeFilters`: (boolean, optional) Include filter definitions. Defaults to `false`.

* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**

```bash
curl --request PUT \
     --url 'https://api.hubapi.com/crm/v3/lists/listId/update-list-name?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{ "name": "Updated List Name" }'
```

* **Example Response (HTTP 200):** *(Schema omitted)*


### 9. Delete a List (DELETE)

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** DELETE
* **Description:** Deletes a list.  Restorable for 90 days.
* **Parameters:**
    * `listId`: (string, required) The ID of the list to delete.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**

```bash
curl --request DELETE \
     --url https://api.hubapi.com/crm/v3/lists/listId \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

* **Example Response (HTTP 204):** No content


## List Memberships Endpoints

*(These endpoints are similar in structure to the list endpoints above.  Omitting detailed descriptions for brevity.  Refer to the original text for specifics.)*


### 10. Fetch List Memberships Ordered by Added to List Date (GET)
`/crm/v3/lists/{listId}/memberships/join-order`

### 11. Fetch List Memberships Ordered by ID (GET)
`/crm/v3/lists/{listId}/memberships`

### 12. Get lists record is member of (GET)
`/crm/v3/lists/records/{objectTypeId}/{recordId}/memberships`

### 13. Add All Records from a Source List to a Destination List (PUT)
`/crm/v3/lists/{listId}/memberships/add-from/{sourceListId}`

### 14. Add and/or Remove Records from a List (PUT)
`/crm/v3/lists/{listId}/memberships/add-and-remove`

### 15. Add Records to a List (PUT)
`/crm/v3/lists/{listId}/memberships/add`

### 16. Remove Records from a List (PUT)
`/crm/v3/lists/{listId}/memberships/remove`

### 17. Delete All Records from a List (DELETE)
`/crm/v3/lists/{listId}/memberships`


## List Folders Endpoints

*(Similar structure to previous endpoints; descriptions omitted for brevity. Refer to original text.)*

### 18. Retrieves a folder (GET)
`/crm/v3/lists/folders`

### 19. Creates a folder (POST)
`/crm/v3/lists/folders`

### 20. Moves a folder (PUT)
`/crm/v3/lists/folders/{folderId}/move/{newParentFolderId}`

### 21. Moves a list to a given folder (PUT)
`/crm/v3/lists/folders/move-list`

### 22. Rename a folder (PUT)
`/crm/v3/lists/folders/{folderId}/rename`

### 23. Deletes a folder (DELETE)
`/crm/v3/lists/folders/{folderId}`


## List ID Mapping Endpoints

*(Temporary APIs; expiring May 30th, 2025)*

### 24. Translate Legacy List Id to Modern List Id (GET)
`/crm/v3/lists/idmapping`

### 25. Translate Legacy List Id to Modern List Id in Batch (POST)
`/crm/v3/lists/idmapping`


**Note:**  Replace placeholders like `{listId}`, `{objectTypeId}`, `{listName}`, etc., with actual values.  The complete schema for request and response bodies can be found in the official HubSpot API documentation.  Error handling and rate limits are also detailed in the official documentation.
