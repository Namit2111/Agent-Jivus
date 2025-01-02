# HubSpot Lists API v3 Documentation

This document provides a comprehensive overview of the HubSpot Lists API v3, allowing you to manage list memberships for object lists.  The API uses standard RESTful principles.

## API Version: v3

## Use Cases

* Bulk adding contacts to a list.
* Removing company records from a company list.

## Authentication

All API calls require authentication using either:

* **Private Apps:**  Requires a private app integration.
* **OAuth:**  Requires an OAuth 2.0 access token.  The token should be included in the `Authorization` header as `Bearer YOUR_ACCESS_TOKEN`.


## Rate Limits

Standard HubSpot API rate limits apply.


## Lists Endpoints

### 1. Fetch List by ID (GET)

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** `GET`
* **Description:** Retrieves a single list by its ILS list ID.
* **Parameters:**
    * `listId`: (required) The ID of the list to retrieve.
    * `includeFilters`: (optional, boolean)  Includes filter definitions in the response. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/listId?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):**  *(Schema varies; refer to HubSpot documentation for details)*


### 2. Fetch List by Name (GET)

* **Endpoint:** `/crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}`
* **Method:** `GET`
* **Description:** Retrieves a single list by its name and object type.
* **Parameters:**
    * `objectTypeId`: (required) The object type ID (e.g., contacts, companies).
    * `listName`: (required) The name of the list.
    * `includeFilters`: (optional, boolean) Includes filter definitions in the response. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/object-type-id/objectTypeId/name/listName?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):** *(Schema varies; refer to HubSpot documentation for details)*


### 3. Fetch Multiple Lists (GET)

* **Endpoint:** `/crm/v3/lists/`
* **Method:** `GET`
* **Description:** Retrieves multiple lists in a single request by providing a comma-separated list of `listId` values.
* **Parameters:**
    * `listId`: (optional) Comma separated list of list IDs to retrieve. If not provided, fetches all lists.
    * `includeFilters`: (optional, boolean) Includes filter definitions in the response. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):** *(Schema varies; refer to HubSpot documentation for details)*


### 4. Create List (POST)

* **Endpoint:** `/crm/v3/lists/`
* **Method:** `POST`
* **Description:** Creates a new list.
* **Parameters:**  *(Request body is JSON)*
    * `objectTypeId`: (required) The object type ID.
    * `processingType`: (required) The processing type ("MANUAL" or "DYNAMIC").
    * `customProperties`: (optional) Custom properties for the list.
    * `listFolderId`: (optional)  The ID of the folder to place the list in.
    * `name`: (required) The name of the list.
    * `filterBranch`: (required for `DYNAMIC` lists) The filter definition.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`
* **Example Request (cURL):**
```bash
curl --request POST \
     --url https://api.hubapi.com/crm/v3/lists/ \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{ "objectTypeId": "contacts", "processingType": "MANUAL", "name": "My New List" }'
```
* **Example Response (HTTP 200):** *(Schema varies; refer to HubSpot documentation for details)*


### 5. Search Lists (POST)

* **Endpoint:** `/crm/v3/lists/search`
* **Method:** `POST`
* **Description:** Searches lists by name or paginates through all lists.
* **Parameters:** *(Request body is JSON)*
    * `listIds`: (optional) List of list IDs to search.
    * `offset`: (optional) Offset for pagination.
    * `query`: (optional) Search query.
    * `count`: (optional) Number of results to return.
    * `processingTypes`: (optional) List of processing types to filter by.
    * `additionalProperties`: (optional) Additional properties to filter by.
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
* **Example Response (HTTP 200):** *(Schema varies; refer to HubSpot documentation for details)*


### 6. Restore a List (PUT)

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
* **Example Response (HTTP 204):** No content.


### 7. Update List Filter Definition (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/update-list-filters`
* **Method:** `PUT`
* **Description:** Updates the filter definition of a DYNAMIC list.
* **Parameters:**
    * `listId`: (required) The ID of the list to update.
    * `enrollObjectsInWorkflows`: (optional, boolean) Whether to enroll objects in workflows. Defaults to `false`.
    * `filterBranch`: (required) The updated filter definition.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`
* **Example Request (cURL):**
```bash
curl --request PUT \
     --url 'https://api.hubapi.com/crm/v3/lists/listId/update-list-filters?enrollObjectsInWorkflows=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{ "filterBranch": { "filterBranchType": "OR", "filterBranchOperator": "string" } }'
```
* **Example Response (HTTP 200):** *(Schema varies; refer to HubSpot documentation for details)*


### 8. Update List Name (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/update-list-name`
* **Method:** `PUT`
* **Description:** Updates the name of a list.
* **Parameters:**
    * `listId`: (required) The ID of the list to update.
    * `name`: (required) The new name of the list.
    * `includeFilters`: (optional, boolean) Includes filter definitions in the response. Defaults to `false`.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`
* **Example Request (cURL):**
```bash
curl --request PUT \
     --url 'https://api.hubapi.com/crm/v3/lists/listId/update-list-name?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{ "name": "New List Name" }'
```
* **Example Response (HTTP 200):** *(Schema varies; refer to HubSpot documentation for details)*


### 9. Delete a List (DELETE)

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** `DELETE`
* **Description:** Deletes a list.
* **Parameters:**
    * `listId`: (required) The ID of the list to delete.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`
* **Example Request (cURL):**
```bash
curl --request DELETE \
     --url https://api.hubapi.com/crm/v3/lists/listId \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 204):** No content.



## Lists Memberships Endpoints

*(Detailed descriptions for each membership endpoint are omitted for brevity, but the structure is similar to the Lists endpoints above.  Refer to the original text for specifics.)*

* **Fetch List Memberships Ordered by Added to List Date (GET)**
* **Fetch List Memberships Ordered by ID (GET)**
* **Get lists record is member of (GET)**
* **Add All Records from a Source List to a Destination List (PUT)**
* **Add and/or Remove Records from a List (PUT)**
* **Add Records to a List (PUT)**
* **Remove Records from a List (PUT)**
* **Delete All Records from a List (DELETE)**


## Lists Folders Endpoints

*(Detailed descriptions for each folder endpoint are omitted for brevity, but the structure is similar to the Lists endpoints above.  Refer to the original text for specifics.)*

* **Retrieves a folder (GET)**
* **Creates a folder (POST)**
* **Moves a folder (PUT)**
* **Moves a list to a given folder (PUT)**
* **Rename a folder (PUT)**
* **Deletes a folder (DELETE)**


## Lists Mapping Endpoints

*(Detailed descriptions for each mapping endpoint are omitted for brevity, but the structure is similar to the Lists endpoints above.  Refer to the original text for specifics.)*

* **Translate Legacy List Id to Modern List Id (GET)**
* **Translate Legacy List Id to Modern List Id in Batch (POST)**


**Note:**  This documentation is based on the provided text and may not be entirely comprehensive.  Always refer to the official HubSpot API documentation for the most up-to-date and accurate information, including detailed schema definitions for request and response bodies.
