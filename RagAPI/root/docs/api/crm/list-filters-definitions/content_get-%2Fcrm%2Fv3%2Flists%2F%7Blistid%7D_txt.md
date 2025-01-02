# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, allowing management of list memberships for object lists.  Requires either Marketing Hub Starter or Content Hub Starter or higher.

## Use Cases

* Bulk adding contacts to a list.
* Removing company records from a company list.

## Related Guide

[Lists Guide](<Insert_Lists_Guide_Link_Here>)


## API Endpoints

All endpoints use `https://api.hubapi.com/crm/v3/lists/` as a base URL and require authentication via `Bearer YOUR_ACCESS_TOKEN` in the `Authorization` header.  Replace `YOUR_ACCESS_TOKEN` with your actual access token.  Standard API rate limits apply to all endpoints.

### Lists

#### 1. Fetch List by ID (GET)

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** `GET`
* **Description:** Fetches a single list by its ILS list ID.
* **Parameters:**
    * `listId` (required): The ID of the list.
    * `includeFilters` (optional, boolean):  Include filter details. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/listId?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):**  *(Schema details omitted for brevity - refer to HubSpot's API documentation for detailed schema)*
  ```json
  {
    "listId": 123,
    "name": "My List",
    // ... other properties
  }
  ```

#### 2. Fetch List by Name (GET)

* **Endpoint:** `/crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}`
* **Method:** `GET`
* **Description:** Fetches a single list by its name and object type.
* **Parameters:**
    * `objectTypeId` (required): The object type ID.
    * `listName` (required): The name of the list.
    * `includeFilters` (optional, boolean): Include filter details. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/object-type-id/objectTypeId/name/listName?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):** *(Schema details omitted)*


#### 3. Fetch Multiple Lists (GET)

* **Endpoint:** `/crm/v3/lists/`
* **Method:** `GET`
* **Description:** Fetches multiple lists by their ILS list IDs.
* **Parameters:**
    * `listId` (required, array): An array of list IDs.
    * `includeFilters` (optional, boolean): Include filter details. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/?includeFilters=false&listId=123&listId=456' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):** *(Schema details omitted)*


#### 4. Create List (POST)

* **Endpoint:** `/crm/v3/lists/`
* **Method:** `POST`
* **Description:** Creates a new list.
* **Parameters:** (Request body - application/json)
    * `objectTypeId` (required):  The object type ID (e.g., contacts).
    * `processingType` (required): The list processing type ("MANUAL" or "SNAPSHOT").
    * `customProperties` (optional): Custom properties for the list.
    * `listFolderId` (optional, integer): The ID of the folder to place the list in.
    * `name` (required): The name of the list.
    * `filterBranch` (optional): Filter definition for DYNAMIC lists.
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
         "name": "New List",
         "listFolderId": 0
       }'
```
* **Example Response (HTTP 200):** *(Schema details omitted)*


#### 5. Search Lists (POST)

* **Endpoint:** `/crm/v3/lists/search`
* **Method:** `POST`
* **Description:** Searches lists by name or pages through all lists.
* **Parameters:** (Request body - application/json)
    * `listIds` (optional, array): Array of list IDs to filter by.
    * `offset` (optional, integer):  Pagination offset.
    * `query` (optional, string): Search query.
    * `count` (optional, integer): Number of results to return.
    * `processingTypes` (optional, array): Array of processing types to filter by.
    * `additionalProperties` (optional, array): Array of additional properties to filter by.
    * `sort` (optional, string): Sorting criteria.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):** *(Simplified example)*
```bash
curl --request POST \
     --url https://api.hubapi.com/crm/v3/lists/search \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{"query": "My List"}'
```
* **Example Response (HTTP 200):** *(Schema details omitted)*


#### 6. Restore a List (PUT)

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


#### 7. Update List Filter Definition (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/update-list-filters`
* **Method:** `PUT`
* **Description:** Updates the filter branch definition of a DYNAMIC list.
* **Parameters:**
    * `listId` (required): The ID of the list.
    * `enrollObjectsInWorkflows` (optional, boolean): Enroll objects in workflows. Defaults to `false`.
    * `filterBranch` (required): The updated filter branch definition (JSON).
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request PUT \
     --url 'https://api.hubapi.com/crm/v3/lists/listId/update-list-filters?enrollObjectsInWorkflows=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{ "filterBranch": { "filterBranchType": "OR", "filterBranchOperator": "string" } }'
```
* **Example Response (HTTP 200):** *(Schema details omitted)*


#### 8. Update List Name (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/update-list-name`
* **Method:** `PUT`
* **Description:** Updates the name of a list. The name must be globally unique.
* **Parameters:**
    * `listId` (required): The ID of the list.
    * `name` (required): The new name of the list.
    * `includeFilters` (optional, boolean): Include filter details. Defaults to `false`.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request PUT \
     --url 'https://api.hubapi.com/crm/v3/lists/listId/update-list-name?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{"name": "New List Name"}'
```
* **Example Response (HTTP 200):** *(Schema details omitted)*


#### 9. Delete a List (DELETE)

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


### Memberships

*(Endpoints for managing list memberships are documented similarly to the above examples.  Refer to the original text for specifics on each endpoint.)*


### Folders

*(Endpoints for managing list folders are documented similarly to the above examples.  Refer to the original text for specifics on each endpoint.)*


### Mapping (Legacy ID Translation - Expiring May 30, 2025)

*(Endpoints for translating legacy list IDs are documented similarly to the above examples.  Refer to the original text for specifics on each endpoint.)*


**Note:**  This documentation provides a concise overview. For complete details including schemas, error handling, and detailed parameter descriptions, refer to the official HubSpot API documentation.  The examples provided are simplified for clarity and may require adjustments depending on your specific needs and data.
