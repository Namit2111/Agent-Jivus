# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, allowing management of list memberships for object lists.  Requires either Marketing Hub Starter or Content Hub Starter or higher.

## Use Cases

* Bulk adding contacts to a list.
* Removing company records from a company list.

## Related Guide

[Lists Guide](<Insert Link Here>)  (Replace `<Insert Link Here>` with the actual link)


## API Endpoints

All endpoints are located under the base URL: `https://api.hubapi.com/crm/v3/lists/`  and require authentication via `Bearer YOUR_ACCESS_TOKEN` in the authorization header.


### Lists

**1. Fetch List by ID (GET)**

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** `GET`
* **Description:** Fetches a single list by its ILS list ID.
* **Parameters:**
    * `listId`: (Required) The ID of the list.
    * `includeFilters`: (Optional, Boolean) Whether to include filters in the response. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/listId?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):**  (Schema omitted for brevity, refer to HubSpot API documentation for details)
    ```json
    {
      "listId": 123,
      "name": "My List",
      // ... other properties
    }
    ```

**2. Fetch List by Name (GET)**

* **Endpoint:** `/crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}`
* **Method:** `GET`
* **Description:** Fetches a single list by list name and object type.
* **Parameters:**
    * `objectTypeId`: (Required) The object type ID.
    * `listName`: (Required) The name of the list.
    * `includeFilters`: (Optional, Boolean) Whether to include filters in the response. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/object-type-id/objectTypeId/name/listName?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):** (Schema omitted)


**3. Fetch Multiple Lists (GET)**

* **Endpoint:** `/crm/v3/lists/`
* **Method:** `GET`
* **Description:** Fetches multiple lists by their ILS list IDs.
* **Parameters:**
    * `listId`: (Required) Comma-separated list of list IDs.
    * `includeFilters`: (Optional, Boolean) Whether to include filters in the response. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/?includeFilters=false&listId=123,456' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):** (Schema omitted)


**4. Create List (POST)**

* **Endpoint:** `/crm/v3/lists/`
* **Method:** `POST`
* **Description:** Creates a new list.
* **Parameters:** (Body as application/json)
    * `objectTypeId`: (Required) The object type ID.
    * `processingType`: (Required) The processing type of the list (e.g., "MANUAL", "DYNAMIC").
    * `customProperties`: (Optional) Custom properties for the list.
    * `listFolderId`: (Optional) The ID of the folder to place the list in.
    * `name`: (Required) The name of the list.
    * `filterBranch`: (Required for DYNAMIC lists) The filter definition for the list.
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
       "customProperties": {},
       "listFolderId": 0,
       "name": "My New List",
       "filterBranch": { "filterBranchType": "OR", "filterBranchOperator": "AND"}
     }'
```
* **Example Response (HTTP 200):** (Schema omitted)


**5. Search Lists (POST)**

* **Endpoint:** `/crm/v3/lists/search`
* **Method:** `POST`
* **Description:** Searches lists by name or paginates through all lists.
* **Parameters:** (Body as application/json)
    * `listIds`: (Optional) Array of list IDs to filter by.
    * `offset`: (Optional) Offset for pagination.
    * `query`: (Optional) Search query string.
    * `count`: (Optional) Number of results to return.
    * `processingTypes`: (Optional) Array of processing types to filter by.
    * `additionalProperties`: (Optional) Array of additional properties to filter by.
    * `sort`: (Optional) Sort order.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request POST \
     --url https://api.hubapi.com/crm/v3/lists/search \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{
        "query": "My List",
        "count": 10
     }'
```
* **Example Response (HTTP 200):** (Schema omitted)


**6. Restore a List (PUT)**

* **Endpoint:** `/crm/v3/lists/{listId}/restore`
* **Method:** `PUT`
* **Description:** Restores a previously deleted list.
* **Parameters:**
    * `listId`: (Required) The ID of the deleted list.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request PUT \
     --url https://api.hubapi.com/crm/v3/lists/listId/restore \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 204):** No content


**7. Update List Filter Definition (PUT)**

* **Endpoint:** `/crm/v3/lists/{listId}/update-list-filters`
* **Method:** `PUT`
* **Description:** Updates the filter definition of a DYNAMIC list.
* **Parameters:**
    * `listId`: (Required) The ID of the list.
    * `enrollObjectsInWorkflows`: (Optional, Boolean) Whether to enroll objects in workflows. Defaults to `false`.
    * `filterBranch`: (Required) The updated filter branch definition. (Body as application/json)
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request PUT \
     --url 'https://api.hubapi.com/crm/v3/lists/listId/update-list-filters?enrollObjectsInWorkflows=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{ "filterBranch": { "filterBranchType": "OR", "filterBranchOperator": "AND" } }'
```
* **Example Response (HTTP 200):** (Schema omitted)


**8. Update List Name (PUT)**

* **Endpoint:** `/crm/v3/lists/{listId}/update-list-name`
* **Method:** `PUT`
* **Description:** Updates the name of a list.
* **Parameters:**
    * `listId`: (Required) The ID of the list.
    * `name`: (Required) The new name of the list. (Body as application/json)
    * `includeFilters`: (Optional, Boolean) Whether to include filters in the response. Defaults to `false`.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**  (Note: Body would contain the new name)
```bash
curl --request PUT \
     --url 'https://api.hubapi.com/crm/v3/lists/listId/update-list-name?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{ "name": "New List Name" }'
```
* **Example Response (HTTP 200):** (Schema omitted)


**9. Delete a List (DELETE)**

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** `DELETE`
* **Description:** Deletes a list.
* **Parameters:**
    * `listId`: (Required) The ID of the list.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request DELETE \
     --url https://api.hubapi.com/crm/v3/lists/listId \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 204):** No content



### Memberships

**(Endpoints for adding, removing, and fetching list memberships follow a similar structure to the above examples.  They are omitted here for brevity, but can be found in the provided text.)**  Refer to the original text for details on each endpoint, including parameters, scopes, and request/response examples.


### Folders

**(Endpoints for managing list folders are also omitted for brevity, but can be found in the provided text.  They follow a similar format as the above examples.)**


### Mapping

**(Endpoints for legacy list ID mapping are also omitted for brevity, but details can be found in the original text.)**


**Note:**  Replace placeholders like `{listId}`, `objectTypeId`, `listName`, `sourceListId`, `folderId`, `newParentFolderId` with actual values.  The schema for responses are not included here for brevity, refer to the official HubSpot API documentation for complete schema details.  Error handling and detailed response codes are also not included, and should be reviewed in the HubSpot API documentation.
