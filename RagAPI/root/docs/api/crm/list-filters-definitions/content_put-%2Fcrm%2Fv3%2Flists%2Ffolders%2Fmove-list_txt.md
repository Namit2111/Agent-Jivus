# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, allowing management of list memberships for object lists.  Requires either Marketing Hub Starter or Content Hub Starter or higher.

## API Version: v3

## Use Cases

* Bulk adding contacts to a list.
* Removing company records from a company list.


## Lists Endpoints

### 1. Fetch List by ID (GET)

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** `GET`
* **Description:** Fetches a single list by its ILS list ID.
* **Parameters:**
    * `listId` (string, required): The ID of the list to fetch.
    * `includeFilters` (boolean, optional):  If true, includes filters in the response. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Rate Limits:** Standard API rate limits apply.
* **Authentication:** Private apps, OAuth
* **Example Request (cURL):**

```bash
curl --request GET \
--url 'https://api.hubapi.com/crm/v3/lists/listId?includeFilters=false' \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

* **Example Response (HTTP 200):**  *(Schema varies; refer to HubSpot documentation for details)*

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
    * `objectTypeId` (string, required): The object type ID.
    * `listName` (string, required): The name of the list.
    * `includeFilters` (boolean, optional): If true, includes filters in the response. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Rate Limits:** Standard API rate limits apply.
* **Authentication:** Private apps, OAuth
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
* **Description:** Fetches multiple lists by their ILS list IDs.
* **Parameters:**
    * `listId` (array of strings, optional): Array of list IDs to fetch. If omitted, fetches all lists.
    * `includeFilters` (boolean, optional): If true, includes filters in the response. Defaults to `false`.
* **Scopes:** `crm.lists.read`
* **Rate Limits:** Standard API rate limits apply.
* **Authentication:** Private apps, OAuth
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
* **Parameters:**  *(See request body below)*
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`
* **Rate Limits:** Standard API rate limits apply.
* **Authentication:** Private apps, OAuth
* **Example Request (cURL):**

```bash
curl --request POST \
--url https://api.hubapi.com/crm/v3/lists/ \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
--header 'content-type: application/json' \
--data '{
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
}'
```

* **Example Response (HTTP 200):** *(Schema varies; refer to HubSpot documentation for details)*


### 5. Search Lists (POST)

* **Endpoint:** `/crm/v3/lists/search`
* **Method:** `POST`
* **Description:** Searches lists by name or pages through all lists.
* **Parameters:** *(See request body below)*
* **Scopes:** `crm.lists.read`
* **Rate Limits:** Standard API rate limits apply.
* **Authentication:** Private apps, OAuth
* **Example Request (cURL):**

```bash
curl --request POST \
--url https://api.hubapi.com/crm/v3/lists/search \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
--header 'content-type: application/json' \
--data '{
"listIds": ["string"],
"offset": 0,
"query": "string",
"count": 0,
"processingTypes": ["string"],
"additionalProperties": ["string"],
"sort": "string"
}'
```

* **Example Response (HTTP 200):** *(Schema varies; refer to HubSpot documentation for details)*


### 6. Restore a List (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/restore`
* **Method:** `PUT`
* **Description:** Restores a previously deleted list.
* **Parameters:**
    * `listId` (string, required): The ID of the list to restore.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Rate Limits:** Standard API rate limits apply.
* **Authentication:** Private apps, OAuth
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
    * `listId` (string, required): The ID of the list to update.
    * `enrollObjectsInWorkflows` (boolean, optional): Whether to enroll objects in workflows. Defaults to `false`.
    * `filterBranch` (object, required): The updated filter branch definition.  *(See request body below)*
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Rate Limits:** Standard API rate limits apply.
* **Authentication:** Private apps, OAuth
* **Example Request (cURL):**

```bash
curl --request PUT \
--url 'https://api.hubapi.com/crm/v3/lists/listId/update-list-filters?enrollObjectsInWorkflows=false' \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
--header 'content-type: application/json' \
--data '{
"filterBranch": {
"filterBranchType": "OR",
"filterBranchOperator": "string"
}
}'
```

* **Example Response (HTTP 200):** *(Schema varies; refer to HubSpot documentation for details)*


### 8. Update List Name (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/update-list-name`
* **Method:** `PUT`
* **Description:** Updates the name of a list.
* **Parameters:**
    * `listId` (string, required): The ID of the list to update.
    * `includeFilters` (boolean, optional): If true, includes filters in the response. Defaults to `false`.
    * `name` (string, required): The new name of the list.  (Should be added in request body - see example below)
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Rate Limits:** Standard API rate limits apply.
* **Authentication:** Private apps, OAuth
* **Example Request (cURL):**

```bash
curl --request PUT \
--url 'https://api.hubapi.com/crm/v3/lists/listId/update-list-name?includeFilters=false' \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
--header 'content-type: application/json' \
--data '{"name": "New List Name"}'
```

* **Example Response (HTTP 200):** *(Schema varies; refer to HubSpot documentation for details)*


### 9. Delete a List (DELETE)

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** `DELETE`
* **Description:** Deletes a list.
* **Parameters:**
    * `listId` (string, required): The ID of the list to delete.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Rate Limits:** Standard API rate limits apply.
* **Authentication:** Private apps, OAuth
* **Example Request (cURL):**

```bash
curl --request DELETE \
--url https://api.hubapi.com/crm/v3/lists/listId \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

* **Example Response (HTTP 204):** No content


## Memberships Endpoints

*(Similar detailed descriptions are needed for all memberships endpoints, mirroring the structure above.  Include parameters, scopes, authentication, example requests, and example responses.)*


## Folders Endpoints

*(Similar detailed descriptions are needed for all folders endpoints, mirroring the structure above.  Include parameters, scopes, authentication, example requests, and example responses.)*


## Mapping Endpoints

*(Similar detailed descriptions are needed for all mapping endpoints, mirroring the structure above.  Include parameters, scopes, authentication, example requests, and example responses.)*


**Note:**  Replace placeholders like `{listId}`, `objectTypeId`, `listName`, `sourceListId`, `folderId`, `newParentFolderId`,  `"string"` and `YOUR_ACCESS_TOKEN` with actual values.  Refer to the official HubSpot API documentation for detailed schema information for request and response bodies.
