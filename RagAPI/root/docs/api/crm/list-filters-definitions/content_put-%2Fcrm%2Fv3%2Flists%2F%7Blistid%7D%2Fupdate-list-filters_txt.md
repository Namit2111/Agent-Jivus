# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, allowing management of list memberships for object lists.  Requires either Marketing Hub Starter or Content Hub Starter or higher.

## Use Cases

* Bulk adding contacts to a list.
* Removing company records from a company list.

## Related Guide

[HubSpot Lists Guide](<Insert Link Here>)


## API Endpoints

All endpoints use `https://api.hubapi.com/crm/v3/lists/` as the base URL and require authentication via `Bearer YOUR_ACCESS_TOKEN` in the header.  Standard API rate limits apply.

**Authentication:** Private apps and OAuth are supported.


### Lists

#### 1. Fetch List by ID (GET)

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** `GET`
* **Parameters:** `includeFilters=false` (optional, defaults to `false`)
* **Scopes:** `crm.lists.read`
* **Description:** Fetches a single list by its ILS list ID.
* **Example Request (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/listId?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):**  *(Schema omitted for brevity, refer to HubSpot's API documentation for detailed schema)*  A JSON object representing the list.


#### 2. Fetch List by Name (GET)

* **Endpoint:** `/crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}`
* **Method:** `GET`
* **Parameters:** `includeFilters=false` (optional, defaults to `false`)
* **Scopes:** `crm.lists.read`
* **Description:** Fetches a single list by list name and object type.
* **Example Request (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/object-type-id/objectTypeId/name/listName?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):** A JSON object representing the list.


#### 3. Fetch Multiple Lists (GET)

* **Endpoint:** `/crm/v3/lists/`
* **Method:** `GET`
* **Parameters:** `includeFilters=false` (optional, defaults to `false`),  `listId` (comma-separated list of IDs)
* **Scopes:** `crm.lists.read`
* **Description:** Fetches multiple lists by their ILS list IDs.
* **Example Request (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):** A JSON object containing an array of list objects.


#### 4. Create List (POST)

* **Endpoint:** `/crm/v3/lists/`
* **Method:** `POST`
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`
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
* **Example Request (cURL):**
```bash
curl --request POST \
     --url https://api.hubapi.com/crm/v3/lists/ \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{...}' //Insert JSON body above
```
* **Example Response (HTTP 200):** A JSON object representing the newly created list.


#### 5. Search Lists (POST)

* **Endpoint:** `/crm/v3/lists/search`
* **Method:** `POST`
* **Scopes:** `crm.lists.read`
* **Description:** Searches lists by name or pages through all lists.
* **Request Body (JSON):**
```json
{
  "listIds": ["string"],
  "offset": 0,
  "query": "string",
  "count": 0,
  "processingTypes": ["string"],
  "additionalProperties": ["string"],
  "sort": "string"
}
```
* **Example Request (cURL):**
```bash
curl --request POST \
     --url https://api.hubapi.com/crm/v3/lists/search \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{...}' //Insert JSON body above

```
* **Example Response (HTTP 200):** A JSON object with search results.


#### 6. Restore a List (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/restore`
* **Method:** `PUT`
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Description:** Restores a previously deleted list (up to 90 days).
* **Example Request (cURL):**
```bash
curl --request PUT \
     --url https://api.hubapi.com/crm/v3/lists/listId/restore \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 204):** No content.


#### 7. Update List Filter Definition (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/update-list-filters`
* **Method:** `PUT`
* **Parameters:** `enrollObjectsInWorkflows=false` (optional, defaults to `false`)
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Description:** Updates the filter definition of a DYNAMIC list.
* **Request Body (JSON):**
```json
{
  "filterBranch": {
    "filterBranchType": "OR",
    "filterBranchOperator": "string"
  }
}
```
* **Example Request (cURL):**
```bash
curl --request PUT \
     --url 'https://api.hubapi.com/crm/v3/lists/listId/update-list-filters?enrollObjectsInWorkflows=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{...}' //Insert JSON body above
```
* **Example Response (HTTP 200):** A JSON object representing the updated list.


#### 8. Update List Name (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/update-list-name`
* **Method:** `PUT`
* **Parameters:** `includeFilters=false` (optional, defaults to `false`)
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Description:** Updates the name of a list.
* **Example Request (cURL):**
```bash
curl --request PUT \
     --url 'https://api.hubapi.com/crm/v3/lists/listId/update-list-name?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 200):** A JSON object representing the updated list.


#### 9. Delete a List (DELETE)

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** `DELETE`
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Description:** Deletes a list.  Restorable for 90 days.
* **Example Request (cURL):**
```bash
curl --request DELETE \
     --url https://api.hubapi.com/crm/v3/lists/listId \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```
* **Example Response (HTTP 204):** No content.


### Memberships

*(Endpoints for adding, removing, and fetching list memberships follow a similar structure to the examples above.  Refer to the original text for specifics on each endpoint.)*  Note that many membership endpoints only work for lists with `processingType` of `MANUAL` or `SNAPSHOT` and may have limitations on the number of memberships.


### Folders

*(Endpoints for managing list folders also follow a similar structure. Refer to the original text for details.)*


### Mapping

*(Endpoints for translating legacy list IDs are temporary and will expire. Refer to the original text for details.)*


**Note:**  Replace placeholders like `{listId}`, `{objectTypeId}`, `{listName}`, `{sourceListId}`, `{folderId}`, etc., with actual values.  The examples provided are cURL commands; adapt them to your preferred language.  Refer to the HubSpot API documentation for detailed schema information and error handling.
