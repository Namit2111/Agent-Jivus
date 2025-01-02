# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, allowing management of list memberships for object lists.  It requires either Marketing Hub Starter or Content Hub Starter or higher.

## API Version: v3

## Use Cases

* Bulk adding contacts to a list.
* Removing company records from a company list.

## Related Guide

[Lists Guide](<insert_link_here>)


## Lists Endpoints

### 1. Fetch List by ID (GET)

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** `GET`
* **Description:** Fetches a single list by its ILS list ID.
* **Parameters:**
    * `listId`: (required) The ID of the list to retrieve.
    * `includeFilters`: (optional, boolean)  Whether to include filter definitions in the response. Defaults to `false`.
* **Headers:**
    * `Authorization: Bearer YOUR_ACCESS_TOKEN`
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/listId?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):**  *(Schema details omitted for brevity, refer to HubSpot documentation)*
    ```json
    {
      "listId": 123,
      "name": "My List",
      // ... other properties
    }
    ```

### 2. Fetch List by Name (GET)

* **Endpoint:** `/crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}`
* **Method:** `GET`
* **Description:** Fetches a single list by list name and object type.
* **Parameters:**
    * `objectTypeId`: (required) The object type ID.
    * `listName`: (required) The name of the list.
    * `includeFilters`: (optional, boolean) Whether to include filter definitions. Defaults to `false`.
* **Headers:** `Authorization: Bearer YOUR_ACCESS_TOKEN`
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/object-type-id/objectTypeId/name/listName?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):** *(Schema details omitted)*


### 3. Fetch Multiple Lists (GET)

* **Endpoint:** `/crm/v3/lists/`
* **Method:** `GET`
* **Description:** Fetches multiple lists by their ILS list IDs.
* **Parameters:**
    * `listId`: (required) Comma-separated list of list IDs to retrieve.
    * `includeFilters`: (optional, boolean) Whether to include filter definitions. Defaults to `false`.
* **Headers:** `Authorization: Bearer YOUR_ACCESS_TOKEN`
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):** *(Schema details omitted)*


### 4. Create List (POST)

* **Endpoint:** `/crm/v3/lists/`
* **Method:** `POST`
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
* **Headers:**
    * `Authorization: Bearer YOUR_ACCESS_TOKEN`
    * `Content-Type: application/json`
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`
* **Example Request (cURL):** *(See provided cURL example)*
* **Example Response (HTTP 200):** *(Schema details omitted)*


### 5. Search Lists (POST)

* **Endpoint:** `/crm/v3/lists/search`
* **Method:** `POST`
* **Description:** Searches lists by name or pages through all lists.
* **Request Body (JSON):** *(See provided cURL example for parameter details)*
* **Headers:**
    * `Authorization: Bearer YOUR_ACCESS_TOKEN`
    * `Content-Type: application/json`
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):** *(See provided cURL example)*
* **Example Response (HTTP 200):** *(Schema details omitted)*


### 6. Restore a List (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/restore`
* **Method:** `PUT`
* **Description:** Restores a previously deleted list.
* **Parameters:** `listId`: (required) The ID of the list to restore.
* **Headers:** `Authorization: Bearer YOUR_ACCESS_TOKEN`
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`
* **Example Request (cURL):** *(See provided cURL example)*
* **Example Response (HTTP 204):** No content


### 7. Update List Filter Definition (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/update-list-filters`
* **Method:** `PUT`
* **Description:** Updates the filter definition of a DYNAMIC list.
* **Parameters:**
    * `listId`: (required) The ID of the list to update.
    * `enrollObjectsInWorkflows`: (optional, boolean) Whether to enroll objects in workflows. Defaults to `false`.
* **Request Body (JSON):** *(See provided cURL example)*
* **Headers:**
    * `Authorization: Bearer YOUR_ACCESS_TOKEN`
    * `Content-Type: application/json`
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`
* **Example Request (cURL):** *(See provided cURL example)*
* **Example Response (HTTP 200):** *(Schema details omitted)*


### 8. Update List Name (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/update-list-name`
* **Method:** `PUT`
* **Description:** Updates the name of a list.
* **Parameters:**
    * `listId`: (required) The ID of the list to update.
    * `includeFilters`: (optional, boolean) Whether to include filters. Defaults to `false`.
* **Headers:** `Authorization: Bearer YOUR_ACCESS_TOKEN`
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`
* **Example Request (cURL):** *(See provided cURL example)*
* **Example Response (HTTP 200):** *(Schema details omitted)*


### 9. Delete a List (DELETE)

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** `DELETE`
* **Description:** Deletes a list.
* **Parameters:** `listId`: (required) The ID of the list to delete.
* **Headers:** `Authorization: Bearer YOUR_ACCESS_TOKEN`
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`
* **Example Request (cURL):** *(See provided cURL example)*
* **Example Response (HTTP 204):** No content


## Memberships Endpoints

*(Detailed descriptions and examples are omitted for brevity, but follow a similar structure to the Lists endpoints above.  Refer to the provided text for specifics.)*

* **Fetch List Memberships Ordered by Added to List Date (GET):** `/crm/v3/lists/{listId}/memberships/join-order`
* **Fetch List Memberships Ordered by ID (GET):** `/crm/v3/lists/{listId}/memberships`
* **Get lists record is member of (GET):** `/crm/v3/lists/records/{objectTypeId}/{recordId}/memberships`
* **Add All Records from a Source List to a Destination List (PUT):** `/crm/v3/lists/{listId}/memberships/add-from/{sourceListId}`
* **Add and/or Remove Records from a List (PUT):** `/crm/v3/lists/{listId}/memberships/add-and-remove`
* **Add Records to a List (PUT):** `/crm/v3/lists/{listId}/memberships/add`
* **Remove Records from a List (PUT):** `/crm/v3/lists/{listId}/memberships/remove`
* **Delete All Records from a List (DELETE):** `/crm/v3/lists/{listId}/memberships`


## Folders Endpoints

*(Detailed descriptions and examples are omitted for brevity, but follow a similar structure to the Lists endpoints above.  Refer to the provided text for specifics.)*

* **Retrieves a folder (GET):** `/crm/v3/lists/folders`
* **Creates a folder (POST):** `/crm/v3/lists/folders`
* **Moves a folder (PUT):** `/crm/v3/lists/folders/{folderId}/move/{newParentFolderId}`
* **Moves a list to a given folder (PUT):** `/crm/v3/lists/folders/move-list`
* **Rename a folder (PUT):** `/crm/v3/lists/folders/{folderId}/rename`
* **Deletes a folder (DELETE):** `/crm/v3/lists/folders/{folderId}`


## Mapping Endpoints

*(Detailed descriptions and examples are omitted for brevity, but follow a similar structure to the Lists endpoints above.  Refer to the provided text for specifics.)*

* **Translate Legacy List Id to Modern List Id (GET):** `/crm/v3/lists/idmapping`
* **Translate Legacy List Id to Modern List Id in Batch (POST):** `/crm/v3/lists/idmapping`


## Authentication

All endpoints require authentication using either Private Apps or OAuth 2.0 with the appropriate scopes.  The `Authorization: Bearer YOUR_ACCESS_TOKEN` header must be included in all requests.  Replace `YOUR_ACCESS_TOKEN` with your actual access token.

## Rate Limits

All endpoints are subject to standard HubSpot API rate limits.


This documentation provides a concise overview. For complete details, including detailed schema definitions and error handling, please refer to the official HubSpot API documentation.
