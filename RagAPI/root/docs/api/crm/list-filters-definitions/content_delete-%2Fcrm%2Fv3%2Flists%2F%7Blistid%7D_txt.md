# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, allowing management of list memberships for object lists.  Requires either Marketing Hub Starter or Content Hub Starter or higher.

## Use Cases

* Bulk adding contacts to a list.
* Removing company records from a company list.

## Related Guide

[HubSpot Lists Guide](LINK_TO_GUIDE_HERE -  Replace with actual link)


## API Endpoints

All endpoints are under the base URL: `https://api.hubapi.com/crm/v3/lists/`  and require authentication using either Private Apps or OAuth.  Remember to replace `YOUR_ACCESS_TOKEN` with your actual access token.  Standard API rate limits apply to all endpoints.

All examples use cURL, but the API is accessible from various languages (Node, PHP, Ruby, Python, C#).


### Lists

**1. Fetch List by ID (GET)**

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** `GET`
* **Description:** Fetches a single list by its ILS list ID.
* **Parameters:**
    * `listId` (string, required): The ID of the list.
    * `includeFilters` (boolean, optional): Whether to include filter definitions. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/listId?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):**  *(Schema varies depending on `includeFilters`)* (Example response omitted for brevity, refer to HubSpot documentation for details)

**2. Fetch List by Name (GET)**

* **Endpoint:** `/crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}`
* **Method:** `GET`
* **Description:** Fetches a single list by list name and object type.
* **Parameters:**
    * `objectTypeId` (string, required): The object type ID.
    * `listName` (string, required): The name of the list.
    * `includeFilters` (boolean, optional): Whether to include filter definitions. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/object-type-id/objectTypeId/name/listName?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):** (Example response omitted for brevity)

**3. Fetch Multiple Lists (GET)**

* **Endpoint:** `/crm/v3/lists/`
* **Method:** `GET`
* **Description:** Fetches multiple lists by their ILS list IDs.
* **Parameters:**
    * `listId` (array of strings, required): An array of list IDs.
    * `includeFilters` (boolean, optional): Whether to include filter definitions. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/?includeFilters=false&listId=list1Id,list2Id' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):** (Example response omitted for brevity)

**4. Create List (POST)**

* **Endpoint:** `/crm/v3/lists/`
* **Method:** `POST`
* **Description:** Creates a new list.
* **Parameters:** (Request body as JSON)
    * `objectTypeId` (string, required): The object type ID.
    * `processingType` (string, required):  `MANUAL` or `SNAPSHOT`.
    * `customProperties` (object, optional): Custom properties.
    * `listFolderId` (integer, optional): ID of the folder to place the list in.
    * `name` (string, required): The name of the list.
    * `filterBranch` (object, optional for `DYNAMIC` lists): Filter definition.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`
* **Example Request (cURL):**
```bash
curl --request POST \
     --url https://api.hubapi.com/crm/v3/lists/ \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{ "objectTypeId": "contacts", "processingType": "MANUAL", "name": "My New List" }'
```
* **Example Response (HTTP 200):** (Example response omitted for brevity)

**5. Search Lists (POST)**

* **Endpoint:** `/crm/v3/lists/search`
* **Method:** `POST`
* **Description:** Searches lists by name or pages through all lists.
* **Parameters:** (Request body as JSON)
    * `listIds` (array of strings, optional): Filter by list IDs.
    * `offset` (integer, optional): Pagination offset.
    * `query` (string, optional): Search query.
    * `count` (integer, optional): Number of results per page.
    * `processingTypes` (array of strings, optional): Filter by processing type.
    * `additionalProperties` (array of strings, optional): Filter by additional properties.
    * `sort` (string, optional): Sort order.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):** (Example omitted for brevity)
* **Example Response (HTTP 200):** (Example response omitted for brevity)

**6. Restore a List (PUT)**

* **Endpoint:** `/crm/v3/lists/{listId}/restore`
* **Method:** `PUT`
* **Description:** Restores a previously deleted list (up to 90 days).
* **Parameters:** `listId` (string, required): The ID of the list to restore.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):** (Example omitted for brevity)
* **Example Response (HTTP 204):** No content


**7. Update List Filter Definition (PUT)**

* **Endpoint:** `/crm/v3/lists/{listId}/update-list-filters`
* **Method:** `PUT`
* **Description:** Updates the filter branch definition of a DYNAMIC list.
* **Parameters:**
    * `listId` (string, required): The ID of the list.
    * `enrollObjectsInWorkflows` (boolean, optional): Whether to enroll objects in workflows. Defaults to false.
    * `filterBranch` (object, required): Updated filter definition.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):** (Example omitted for brevity)
* **Example Response (HTTP 200):** (Example response omitted for brevity)

**8. Update List Name (PUT)**

* **Endpoint:** `/crm/v3/lists/{listId}/update-list-name`
* **Method:** `PUT`
* **Description:** Updates the name of a list.  Name must be globally unique.
* **Parameters:**
    * `listId` (string, required): The ID of the list.
    * `name` (string, required): The new name of the list.
    * `includeFilters` (boolean, optional): Whether to include filter definitions. Defaults to `false`.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):** (Example omitted for brevity)
* **Example Response (HTTP 200):** (Example response omitted for brevity)

**9. Delete a List (DELETE)**

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** `DELETE`
* **Description:** Deletes a list. Restorable for 90 days.
* **Parameters:** `listId` (string, required): The ID of the list to delete.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):** (Example omitted for brevity)
* **Example Response (HTTP 204):** No content


### Memberships

*(Detailed descriptions and examples for membership endpoints are omitted for brevity. Refer to the original text for complete information.)*

**1. Fetch List Memberships Ordered by Added to List Date (GET)**
**2. Fetch List Memberships Ordered by ID (GET)**
**3. Get lists record is member of (GET)**
**4. Add All Records from a Source List to a Destination List (PUT)**
**5. Add and/or Remove Records from a List (PUT)**
**6. Add Records to a List (PUT)**
**7. Remove Records from a List (PUT)**
**8. Delete All Records from a List (DELETE)**

### Folders

**1. Retrieves a folder (GET)**
**2. Creates a folder (POST)**
**3. Moves a folder (PUT)**
**4. Moves a list to a given folder (PUT)**
**5. Rename a folder (PUT)**
**6. Deletes a folder (DELETE)**


### Mapping

**1. Translate Legacy List Id to Modern List Id (GET)**
**2. Translate Legacy List Id to Modern List Id in Batch (POST)**


This documentation provides a concise overview.  Always refer to the official HubSpot API documentation for the most up-to-date and complete information, including detailed schema definitions and error handling.
