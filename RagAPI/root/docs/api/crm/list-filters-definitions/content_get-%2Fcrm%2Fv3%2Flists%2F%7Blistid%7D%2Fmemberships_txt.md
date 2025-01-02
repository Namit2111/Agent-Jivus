# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, allowing management of list memberships for object lists.  The API requires either Marketing Hub Starter or Content Hub Starter or higher.

## Use Cases

* Bulk adding contacts to a list.
* Removing company records from a company list.

## Authentication

The API uses either private apps or OAuth 2.0 for authentication.  Requests require an `authorization` header with a Bearer token:  `authorization: Bearer YOUR_ACCESS_TOKEN`.


## Lists Endpoints

### 1. Fetch List by ID (GET)

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** `GET`
* **Description:** Retrieves a single list by its ILS list ID.
* **Parameters:**
    * `listId` (required): The ID of the list to retrieve.
    * `includeFilters`: (optional, boolean) Whether to include filter definitions in the response. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/listId?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):**  *(Schema omitted for brevity, see HubSpot documentation for details)*


### 2. Fetch List by Name (GET)

* **Endpoint:** `/crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}`
* **Method:** `GET`
* **Description:** Retrieves a single list by its name and object type.
* **Parameters:**
    * `objectTypeId` (required): The ID of the object type.
    * `listName` (required): The name of the list.
    * `includeFilters`: (optional, boolean) Whether to include filter definitions in the response. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/object-type-id/objectTypeId/name/listName?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):** *(Schema omitted)*


### 3. Fetch Multiple Lists (GET)

* **Endpoint:** `/crm/v3/lists/`
* **Method:** `GET`
* **Description:** Retrieves multiple lists by their ILS list IDs.
* **Parameters:**
    * `listId` (required): Comma-separated list of list IDs.
    * `includeFilters`: (optional, boolean) Whether to include filter definitions in the response. Defaults to `false`.
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
* **Method:** `POST`
* **Description:** Creates a new list.
* **Parameters:** (Request body - JSON)
    * `objectTypeId`: (required) String, object type ID.
    * `processingType`: (required) String, processing type (e.g., "MANUAL", "DYNAMIC").
    * `customProperties`: (optional) Object, custom properties for the list.
    * `listFolderId`: (optional, integer)  ID of the folder to place the list in. 0 for the root folder.
    * `name`: (required) String, list name.
    * `filterBranch`: (optional, only for DYNAMIC lists) Object defining the list's filter.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`
* **Example Request (cURL):**
```bash
curl --request POST \
     --url https://api.hubapi.com/crm/v3/lists/ \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{ "objectTypeId": "string", "processingType": "string", "customProperties": { ... }, "listFolderId": 0, "name": "string", "filterBranch": { ... } }'
```
* **Example Response (HTTP 200):** *(Schema omitted)*


### 5. Search Lists (POST)

* **Endpoint:** `/crm/v3/lists/search`
* **Method:** `POST`
* **Description:** Searches lists by name or pages through all lists.
* **Parameters:** (Request body - JSON)
    * `listIds`: (optional) Array of list IDs to filter by.
    * `offset`: (optional, integer) Offset for pagination.
    * `query`: (optional) Search query string.
    * `count`: (optional, integer) Number of results to return.
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
     --data '{ "listIds": ["string"], "offset": 0, "query": "string", "count": 0, "processingTypes": ["string"], "additionalProperties": ["string"], "sort": "string" }'
```
* **Example Response (HTTP 200):** *(Schema omitted)*


### 6. Restore a List (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/restore`
* **Method:** `PUT`
* **Description:** Restores a previously deleted list.  Lists can be restored up to 90 days after deletion.
* **Parameters:**
    * `listId` (required): The ID of the list to restore.
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
* **Method:** `PUT`
* **Description:** Updates the filter definition of a DYNAMIC list.
* **Parameters:**
    * `listId` (required): The ID of the list to update.
    * `enrollObjectsInWorkflows`: (optional, boolean) Whether to enroll objects in workflows upon update. Defaults to `false`.
    * `filterBranch`: (required) Object, the new filter branch definition.
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
* **Method:** `PUT`
* **Description:** Updates the name of a list. The name must be globally unique.
* **Parameters:**
    * `listId` (required): The ID of the list to update.
    * `includeFilters`: (optional, boolean) Whether to include filter definitions in the response. Defaults to `false`.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request PUT \
     --url 'https://api.hubapi.com/crm/v3/lists/listId/update-list-name?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):** *(Schema omitted)*


### 9. Delete a List (DELETE)

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** `DELETE`
* **Description:** Deletes a list.  Lists can be restored within 90 days.
* **Parameters:**
    * `listId` (required): The ID of the list to delete.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request DELETE \
     --url https://api.hubapi.com/crm/v3/lists/listId \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 204):** No content


## Memberships Endpoints

*(Descriptions and examples omitted for brevity.  Refer to the original text for details on each endpoint.)*

* **Fetch List Memberships Ordered by Added to List Date (GET):** `/crm/v3/lists/{listId}/memberships/join-order`
* **Fetch List Memberships Ordered by ID (GET):** `/crm/v3/lists/{listId}/memberships`
* **Get lists record is member of (GET):** `/crm/v3/lists/records/{objectTypeId}/{recordId}/memberships`
* **Add All Records from a Source List to a Destination List (PUT):** `/crm/v3/lists/{listId}/memberships/add-from/{sourceListId}`
* **Add and/or Remove Records from a List (PUT):** `/crm/v3/lists/{listId}/memberships/add-and-remove`
* **Add Records to a List (PUT):** `/crm/v3/lists/{listId}/memberships/add`
* **Remove Records from a List (PUT):** `/crm/v3/lists/{listId}/memberships/remove`
* **Delete All Records from a List (DELETE):** `/crm/v3/lists/{listId}/memberships`


## Folders Endpoints

*(Descriptions and examples omitted for brevity.)*

* **Retrieves a folder (GET):** `/crm/v3/lists/folders`
* **Creates a folder (POST):** `/crm/v3/lists/folders`
* **Moves a folder (PUT):** `/crm/v3/lists/folders/{folderId}/move/{newParentFolderId}`
* **Moves a list to a given folder (PUT):** `/crm/v3/lists/folders/move-list`
* **Rename a folder (PUT):** `/crm/v3/lists/folders/{folderId}/rename`
* **Deletes a folder (DELETE):** `/crm/v3/lists/folders/{folderId}`


## Mapping Endpoints

*(Descriptions and examples omitted for brevity.)*

* **Translate Legacy List Id to Modern List Id (GET):** `/crm/v3/lists/idmapping`
* **Translate Legacy List Id to Modern List Id in Batch (POST):** `/crm/v3/lists/idmapping`


**Note:**  This documentation is a summary.  Refer to the official HubSpot API documentation for complete details, including schemas and error handling.  The provided cURL examples are illustrative and may require adjustments based on your specific needs. Remember to replace placeholders like `listId`, `objectTypeId`, `listName`, etc., with actual values.
