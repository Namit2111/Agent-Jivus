# HubSpot Lists API v3 Documentation

This document provides a comprehensive overview of the HubSpot Lists API v3, enabling you to manage list memberships for object lists.

## Introduction

The Lists API allows for bulk operations on lists, such as adding or removing contacts or companies.  It supports various actions including fetching lists, creating lists, updating list information, and managing list memberships.  This API requires either Marketing Hub Starter or Content Hub Starter or higher.

## Use Cases

* Bulk adding contacts to a list.
* Removing company records from a company list.
* Managing list memberships efficiently.

## Authentication

All API calls require authentication.  Use either Private Apps or OAuth 2.0.  Replace `YOUR_ACCESS_TOKEN` with your actual access token in the examples below.

## API Endpoints

The following sections detail the available API endpoints, including their HTTP methods, required scopes, parameters, and examples.  All endpoints are under the base URL: `https://api.hubapi.com/crm/v3/lists/`

### Lists Management

#### 1. Fetch List by ID (GET)

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** GET
* **Description:** Retrieves a single list by its ILS list ID.
* **Scopes:** `crm.lists.read`
* **Parameters:**
    * `listId`: (required) The ID of the list to retrieve.
    * `includeFilters`: (optional, boolean) Whether to include filter definitions in the response. Defaults to `false`.
* **Example Request (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/listId?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):**  *(Response structure will vary based on included filters)*
```json
{
  "listId": 123,
  "name": "My List",
  "objectTypeId": "contacts",
  // ... other properties
}
```


#### 2. Fetch List by Name (GET)

* **Endpoint:** `/crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}`
* **Method:** GET
* **Description:** Retrieves a single list by its name and object type.
* **Scopes:** `crm.lists.read`
* **Parameters:**
    * `objectTypeId`: (required) The type of objects in the list (e.g., "contacts", "companies").
    * `listName`: (required) The name of the list.
    * `includeFilters`: (optional, boolean) Whether to include filter definitions in the response. Defaults to `false`.
* **Example Request (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/object-type-id/contacts/name/MyList?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```


#### 3. Fetch Multiple Lists (GET)

* **Endpoint:** `/crm/v3/lists/`
* **Method:** GET
* **Description:** Retrieves multiple lists by providing a comma-separated list of `listId`s.
* **Scopes:** `crm.lists.read`
* **Parameters:**
    * `listId`: (optional, comma-separated) A list of list IDs to retrieve.  If omitted, retrieves all lists.
    * `includeFilters`: (optional, boolean) Whether to include filter definitions in the response. Defaults to `false`.
* **Example Request (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/?listId=123,456&includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```


#### 4. Create List (POST)

* **Endpoint:** `/crm/v3/lists/`
* **Method:** POST
* **Description:** Creates a new list.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`
* **Parameters:** (sent as JSON in the request body)
    * `objectTypeId`: (required) The type of objects in the list (e.g., "contacts", "companies").
    * `processingType`: (required) The processing type of the list ("MANUAL" or "SNAPSHOT").
    * `customProperties`: (optional) Custom properties for the list.
    * `listFolderId`: (optional) The ID of the folder to place the list in.
    * `name`: (required) The name of the list.
    * `filterBranch`: (optional, for DYNAMIC lists) The filter definition.
* **Example Request (cURL):**
```bash
curl --request POST \
     --url https://api.hubapi.com/crm/v3/lists/ \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{
               "objectTypeId": "contacts",
               "processingType": "MANUAL",
               "name": "My New List",
               "listFolderId": 0
             }'
```


#### 5. Search Lists (POST)

* **Endpoint:** `/crm/v3/lists/search`
* **Method:** POST
* **Description:** Searches lists by name or pages through all lists.
* **Scopes:** `crm.lists.read`
* **Parameters:** (sent as JSON in the request body)
    * `listIds`: (optional) A list of list IDs to filter by.
    * `offset`: (optional) The offset for pagination.
    * `query`: (optional) The search query.
    * `count`: (optional) The number of results to return.
    * `processingTypes`: (optional) A list of processing types to filter by.
    * `additionalProperties`: (optional) A list of additional properties to filter by.
    * `sort`: (optional) The sorting criteria.
* **Example Request (cURL):** (similar to Create List, replace with appropriate parameters)


#### 6. Restore a List (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/restore`
* **Method:** PUT
* **Description:** Restores a previously deleted list (within 90 days).
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Parameters:**
    * `listId`: (required) The ID of the list to restore.
* **Example Request (cURL):**
```bash
curl --request PUT \
     --url https://api.hubapi.com/crm/v3/lists/listId/restore \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```


#### 7. Update List Filter Definition (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/update-list-filters`
* **Method:** PUT
* **Description:** Updates the filter definition of a DYNAMIC list.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Parameters:**
    * `listId`: (required) The ID of the list to update.
    * `filterBranch`: (required) The new filter definition (JSON).
    * `enrollObjectsInWorkflows`: (optional, boolean) Whether to enroll objects in workflows. Defaults to `false`.
* **Example Request (cURL):** (similar to Create List, replace with appropriate parameters)


#### 8. Update List Name (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/update-list-name`
* **Method:** PUT
* **Description:** Updates the name of a list.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Parameters:**
    * `listId`: (required) The ID of the list to update.
    * `name`: (required) The new name of the list.
    * `includeFilters`: (optional, boolean) Whether to include filter definitions in the response. Defaults to `false`.
* **Example Request (cURL):**


#### 9. Delete a List (DELETE)

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** DELETE
* **Description:** Deletes a list.  The list can be restored within 90 days.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Parameters:**
    * `listId`: (required) The ID of the list to delete.
* **Example Request (cURL):**



### List Memberships Management

**(Endpoints similar to List Management, refer to original text for details.  Replace `{listId}` and other placeholders as needed.)**


#### 10.  Fetch List Memberships Ordered by Added to List Date (GET)
#### 11.  Fetch List Memberships Ordered by ID (GET)
#### 12.  Get lists record is member of (GET)
#### 13.  Add All Records from a Source List to a Destination List (PUT)
#### 14.  Add and/or Remove Records from a List (PUT)
#### 15.  Add Records to a List (PUT)
#### 16.  Remove Records from a List (PUT)
#### 17.  Delete All Records from a List (DELETE)


### List Folders Management

**(Endpoints similar to List Management, refer to original text for details.  Replace `{folderId}` and other placeholders as needed.)**

#### 18. Retrieves a folder. (GET)
#### 19. Creates a folder (POST)
#### 20. Moves a folder (PUT)
#### 21. Moves a list to a given folder (PUT)
#### 22. Rename a folder (PUT)
#### 23. Deletes a folder (DELETE)


### Legacy List ID Mapping

#### 24. Translate Legacy List Id to Modern List Id (GET)
#### 25. Translate Legacy List Id to Modern List Id in Batch (POST)


**Note:**  This documentation provides a concise summary.  Refer to the original HubSpot API documentation for complete details, including schema definitions for request and response bodies.  Error handling and detailed response codes are not included here but are crucial for robust integration.  Remember to handle potential errors appropriately in your code.
