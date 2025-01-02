# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, allowing management of list memberships for object lists.  Requires either Marketing Hub Starter or Content Hub Starter or higher.

## Use Cases

* Bulk adding contacts to a list.
* Removing company records from a company list.


## API Endpoints

The API uses standard HTTP methods (GET, POST, PUT, DELETE).  All endpoints are located under `/crm/v3/lists/`.  Authentication requires a `Bearer` token in the `Authorization` header.  Standard API rate limits apply.


### Lists

#### 1. Fetch List by ID (GET)

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** GET
* **Description:** Retrieves a single list by its ILS list ID.
* **Parameters:**
    * `listId`: (required) The ID of the list.
    * `includeFilters`: (optional, boolean)  If true, includes filter details. Defaults to false.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
--url 'https://api.hubapi.com/crm/v3/lists/listId?includeFilters=false' \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):**  *(Schema omitted for brevity, see HubSpot documentation for details)*  A JSON object representing the list.


#### 2. Fetch List by Name (GET)

* **Endpoint:** `/crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}`
* **Method:** GET
* **Description:** Retrieves a single list by its name and object type.
* **Parameters:**
    * `objectTypeId`: (required) The object type ID (e.g., contacts, companies).
    * `listName`: (required) The name of the list.
    * `includeFilters`: (optional, boolean) If true, includes filter details. Defaults to false.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
--url 'https://api.hubapi.com/crm/v3/lists/object-type-id/objectTypeId/name/listName?includeFilters=false' \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):**  *(Schema omitted for brevity)* A JSON object representing the list.


#### 3. Fetch Multiple Lists (GET)

* **Endpoint:** `/crm/v3/lists/`
* **Method:** GET
* **Description:** Retrieves multiple lists by their ILS list IDs.
* **Parameters:**
    * `listId`: (required) Comma-separated list of list IDs.
    * `includeFilters`: (optional, boolean) If true, includes filter details. Defaults to false.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request GET \
--url 'https://api.hubapi.com/crm/v3/lists/?includeFilters=false' \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):** *(Schema omitted for brevity)* A JSON object containing an array of lists.


#### 4. Create List (POST)

* **Endpoint:** `/crm/v3/lists/`
* **Method:** POST
* **Description:** Creates a new list.
* **Parameters:** (Body, JSON)
    * `objectTypeId`: (required) The object type ID.
    * `processingType`: (required) The processing type (e.g., `MANUAL`, `DYNAMIC`, `SNAPSHOT`).
    * `customProperties`: (optional) Custom properties for the list.
    * `listFolderId`: (optional) The ID of the folder to place the list in.
    * `name`: (required) The name of the list.
    * `filterBranch`: (required for `DYNAMIC` lists)  Filter definition.
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
"name": "My New List"
}'
```
* **Example Response (HTTP 200):** *(Schema omitted for brevity)* A JSON object representing the newly created list.


#### 5. Search Lists (POST)

* **Endpoint:** `/crm/v3/lists/search`
* **Method:** POST
* **Description:** Searches lists by name or page through all lists.
* **Parameters:** (Body, JSON)
    * `listIds`: (optional) Array of list IDs to filter by.
    * `offset`: (optional) Offset for pagination.
    * `query`: (optional) Search query string.
    * `count`: (optional) Number of results per page.
    * `processingTypes`: (optional) Array of processing types to filter by.
    * `additionalProperties`: (optional) Array of additional properties to filter by.
    * `sort`: (optional) Sort field.
* **Scopes:** `crm.lists.read`
* **Example Request (cURL):** *(See documentation for full example)*
* **Example Response (HTTP 200):** *(Schema omitted for brevity)* A JSON object containing paginated search results.


#### 6. Restore a List (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/restore`
* **Method:** PUT
* **Description:** Restores a deleted list (within 90 days of deletion).
* **Parameters:**
    * `listId`: (required) The ID of the list to restore.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request PUT \
--url https://api.hubapi.com/crm/v3/lists/listId/restore \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 204):** No content.


#### 7. Update List Filter Definition (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/update-list-filters`
* **Method:** PUT
* **Description:** Updates the filter definition of a DYNAMIC list.
* **Parameters:**
    * `listId`: (required) The ID of the list.
    * `filterBranch`: (required) The updated filter branch definition.
    * `enrollObjectsInWorkflows`: (optional, boolean) Whether to enroll objects in workflows. Defaults to `false`.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):** *(See documentation for full example)*
* **Example Response (HTTP 200):** *(Schema omitted for brevity)*


#### 8. Update List Name (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/update-list-name`
* **Method:** PUT
* **Description:** Updates the name of a list.  Name must be globally unique.
* **Parameters:**
    * `listId`: (required) The ID of the list.
    * `name`: (required) The new name of the list.  (Usually sent in the request body)
    * `includeFilters`: (optional, boolean) If true, includes filter details. Defaults to false.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):** *(See documentation for full example)*
* **Example Response (HTTP 200):** *(Schema omitted for brevity)*


#### 9. Delete a List (DELETE)

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** DELETE
* **Description:** Deletes a list.  Restorable for 90 days.
* **Parameters:**
    * `listId`: (required) The ID of the list to delete.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Example Request (cURL):**
```bash
curl --request DELETE \
--url https://api.hubapi.com/crm/v3/lists/listId \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 204):** No content.


### Memberships

*(Endpoints for adding, removing, and fetching list memberships are similarly documented with cURL examples, scopes, and HTTP response codes.  Refer to the original documentation for detailed specifics on each endpoint.)*

### Folders

*(Endpoints for managing list folders are similarly documented.  Refer to the original documentation for detailed specifics.)*

### Mapping

*(Endpoints for translating legacy list IDs are similarly documented.  Refer to the original documentation for detailed specifics.)*


**Note:**  This markdown provides a concise summary.  Refer to the original HubSpot API documentation for comprehensive details, including schema definitions, detailed parameter descriptions, error handling, and rate limits.  Always replace placeholders like `{listId}`, `objectTypeId`, etc., with actual values.
