# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, allowing management of list memberships for object lists.  It requires either Marketing Hub Starter or Content Hub Starter or higher.

## Use Cases

* Bulk adding contacts to a list.
* Removing company records from a company list.


## Authentication

All API calls require authentication using either Private Apps or OAuth 2.0.  The `authorization` header must include a Bearer token:  `Authorization: Bearer YOUR_ACCESS_TOKEN`.


## API Endpoints

The base URL for all endpoints is `https://api.hubapi.com/crm/v3/lists/`.


### Lists

#### 1. Fetch List by ID (GET)

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** GET
* **Description:** Fetches a single list by its ILS list ID.
* **Parameters:**
    * `listId` (required): The ID of the list.
    * `includeFilters` (optional): Boolean indicating whether to include filter definitions. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
--url 'https://api.hubapi.com/crm/v3/lists/listId?includeFilters=false' \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):**  *(Schema varies; see HubSpot documentation for details)*


#### 2. Fetch List by Name (GET)

* **Endpoint:** `/crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}`
* **Method:** GET
* **Description:** Fetches a single list by list name and object type.
* **Parameters:**
    * `objectTypeId` (required): The object type ID.
    * `listName` (required): The name of the list.
    * `includeFilters` (optional): Boolean indicating whether to include filter definitions. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
--url 'https://api.hubapi.com/crm/v3/lists/object-type-id/objectTypeId/name/listName?includeFilters=false' \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):** *(Schema varies; see HubSpot documentation for details)*


#### 3. Fetch Multiple Lists (GET)

* **Endpoint:** `/crm/v3/lists/`
* **Method:** GET
* **Description:** Fetches multiple lists by providing a comma separated list of `listIds`.
* **Parameters:**
    * `listId` (required): Comma-separated list of ILS list IDs.
    * `includeFilters` (optional): Boolean indicating whether to include filter definitions. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
--url 'https://api.hubapi.com/crm/v3/lists/?includeFilters=false&listId=123,456' \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):** *(Schema varies; see HubSpot documentation for details)*


#### 4. Create List (POST)

* **Endpoint:** `/crm/v3/lists/`
* **Method:** POST
* **Description:** Creates a new list.
* **Parameters:** (Body Parameters - JSON)
    * `objectTypeId`:  (string) The object type ID.
    * `processingType`: (string) The processing type ('MANUAL' or 'DYNAMIC').
    * `customProperties`: (object)  Custom properties for the list.
    * `listFolderId`: (integer) The ID of the folder to place the list in.
    * `name`: (string) The name of the list.
    * `filterBranch`: (object) The filter definition for dynamic lists.
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
"customProperties": {},
"listFolderId": 0,
"name": "My New List",
"filterBranch": {
"filterBranchType": "OR",
"filterBranchOperator": "AND"
}
}'
```
* **Example Response (HTTP 200):** *(Schema varies; see HubSpot documentation for details)*


#### 5. Search Lists (POST)

* **Endpoint:** `/crm/v3/lists/search`
* **Method:** POST
* **Description:** Searches lists by name or pages through all lists.
* **Parameters:** (Body Parameters - JSON)
    * `listIds`: (array of strings)  List of IDs to search.
    * `offset`: (integer) Offset for pagination.
    * `query`: (string) Search query.
    * `count`: (integer) Number of results per page.
    * `processingTypes`: (array of strings)  Processing types to filter by.
    * `additionalProperties`: (array of strings) Additional properties to filter by.
    * `sort`: (string) Sorting criteria.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):** (See documentation for full example)


#### 6. Restore a List (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/restore`
* **Method:** PUT
* **Description:** Restores a previously deleted list.
* **Parameters:**
    * `listId` (required): The ID of the deleted list.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):** (See documentation for full example)


#### 7. Update List Filter Definition (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/update-list-filters`
* **Method:** PUT
* **Description:** Updates the filter branch definition of a DYNAMIC list.
* **Parameters:**
    * `listId` (required): The ID of the list.
    * `enrollObjectsInWorkflows` (optional): Boolean, defaults to false.
    * `filterBranch` (required, body parameter): (object) The new filter branch definition.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):** (See documentation for full example)


#### 8. Update List Name (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/update-list-name`
* **Method:** PUT
* **Description:** Updates the name of a list.
* **Parameters:**
    * `listId` (required): The ID of the list.
    * `includeFilters` (optional): Boolean indicating whether to include filter definitions. Defaults to `false`.
    * `name` (required, body parameter): The new name of the list (must be unique).
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):** (See documentation for full example)


#### 9. Delete a List (DELETE)

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** DELETE
* **Description:** Deletes a list.  Lists can be restored for up to 90 days.
* **Parameters:**
    * `listId` (required): The ID of the list.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):** (See documentation for full example)


### Memberships

*(Endpoints for adding, removing, and fetching list memberships are detailed similarly to the List endpoints above. Refer to the original text for specifics.)*


### Folders

*(Endpoints for managing list folders are detailed similarly to the List endpoints above. Refer to the original text for specifics.)*


### Mapping

*(Endpoints for translating legacy list IDs to modern IDs are detailed similarly to the List endpoints above. Refer to the original text for specifics.)*


**Note:**  This documentation is a summary. Always refer to the official HubSpot API documentation for the most up-to-date information, including detailed schema definitions and error handling.  The example responses are placeholders; the actual responses will vary depending on the request.
