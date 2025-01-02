# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, allowing management of list memberships for object lists.  Requires either Marketing Hub Starter or Content Hub Starter or higher.

## Use Cases

* Bulk adding contacts to a list.
* Removing company records from a company list.

## Related Guide

[Lists Guide](link_to_lists_guide_here)  *(Replace `link_to_lists_guide_here` with the actual link)*


## API Endpoints

All endpoints are under the base URL: `https://api.hubapi.com/crm/v3/lists/` and require authentication via `Bearer YOUR_ACCESS_TOKEN` in the header.  Standard API rate limits apply to all endpoints.


### Lists Management

#### 1. Fetch List by ID (GET)

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** `GET`
* **Parameters:**
    * `listId`: (string, required) The ID of the list to fetch.
    * `includeFilters`: (boolean, optional, default: `false`) Whether to include filter definitions in the response.
* **Scopes:** `crm.lists.read`
* **Response:**  A JSON object representing the list details.  (Example and Schema are missing from the provided text,  should be included in the actual API documentation).
* **Example (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/listId?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

#### 2. Fetch List by Name (GET)

* **Endpoint:** `/crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}`
* **Method:** `GET`
* **Parameters:**
    * `objectTypeId`: (string, required) The object type ID.
    * `listName`: (string, required) The name of the list to fetch.
    * `includeFilters`: (boolean, optional, default: `false`) Whether to include filter definitions in the response.
* **Scopes:** `crm.lists.read`
* **Response:** A JSON object representing the list details. (Example and Schema are missing from the provided text, should be included in the actual API documentation).
* **Example (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/object-type-id/objectTypeId/name/listName?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

#### 3. Fetch Multiple Lists (GET)

* **Endpoint:** `/crm/v3/lists/`
* **Method:** `GET`
* **Parameters:**
    * `listId`: (string, required) Comma-separated list of list IDs to fetch.
    * `includeFilters`: (boolean, optional, default: `false`) Whether to include filter definitions in the response.
* **Scopes:** `crm.lists.read`
* **Response:** A JSON array of list objects.  (Example and Schema are missing from the provided text, should be included in the actual API documentation).
* **Example (cURL):**
```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

#### 4. Create List (POST)

* **Endpoint:** `/crm/v3/lists/`
* **Method:** `POST`
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
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`
* **Response:** A JSON object representing the newly created list. (Example and Schema are missing from the provided text, should be included in the actual API documentation).
* **Example (cURL):**  *(Request body shown above)*

```bash
curl --request POST \
     --url https://api.hubapi.com/crm/v3/lists/ \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{...request body...}'
```


#### 5. Search Lists (POST)

* **Endpoint:** `/crm/v3/lists/search`
* **Method:** `POST`
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
* **Scopes:** `crm.lists.read`
* **Response:** A JSON object containing search results. (Example and Schema are missing from the provided text, should be included in the actual API documentation).
* **Example (cURL):** *(Request body shown above)*

```bash
curl --request POST \
     --url https://api.hubapi.com/crm/v3/lists/search \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{...request body...}'
```

#### 6. Restore a List (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/restore`
* **Method:** `PUT`
* **Parameters:**
    * `listId`: (string, required) The ID of the list to restore.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Response:** HTTP 204 (No Content)
* **Example (cURL):**
```bash
curl --request PUT \
     --url https://api.hubapi.com/crm/v3/lists/listId/restore \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

#### 7. Update List Filter Definition (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/update-list-filters`
* **Method:** `PUT`
* **Parameters:**
    * `listId`: (string, required) The ID of the list to update.
    * `enrollObjectsInWorkflows`: (boolean, optional, default: `false`) Whether to enroll objects in workflows.
* **Request Body (JSON):**
```json
{
  "filterBranch": {
    "filterBranchType": "OR",
    "filterBranchOperator": "string"
  }
}
```
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Response:** A JSON object representing the updated list. (Example and Schema are missing from the provided text, should be included in the actual API documentation).
* **Example (cURL):** *(Request body shown above)*

```bash
curl --request PUT \
     --url 'https://api.hubapi.com/crm/v3/lists/listId/update-list-filters?enrollObjectsInWorkflows=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{...request body...}'
```

#### 8. Update List Name (PUT)

* **Endpoint:** `/crm/v3/lists/{listId}/update-list-name`
* **Method:** `PUT`
* **Parameters:**
    * `listId`: (string, required) The ID of the list to update.
    * `includeFilters`: (boolean, optional, default: `false`) Whether to include filter definitions in the response.

* **Request Body (JSON):**  *(Missing from provided text,  needs name field)*
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Response:** A JSON object representing the updated list. (Example and Schema are missing from the provided text, should be included in the actual API documentation).
* **Example (cURL):**

```bash
curl --request PUT \
     --url 'https://api.hubapi.com/crm/v3/lists/listId/update-list-name?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

#### 9. Delete a List (DELETE)

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** `DELETE`
* **Parameters:**
    * `listId`: (string, required) The ID of the list to delete.
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Response:** HTTP 204 (No Content)
* **Example (cURL):**
```bash
curl --request DELETE \
     --url https://api.hubapi.com/crm/v3/lists/listId \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```


### List Memberships Management

*(Similar detailed descriptions for each membership endpoint are needed, including request bodies, responses, examples, and schemas.  The provided text only gives the basic information.  Follow the structure provided above for each endpoint.)*

#### 10. Fetch List Memberships Ordered by Added to List Date (GET)
#### 11. Fetch List Memberships Ordered by ID (GET)
#### 12. Get lists record is member of (GET)
#### 13. Add All Records from a Source List to a Destination List (PUT)
#### 14. Add and/or Remove Records from a List (PUT)
#### 15. Add Records to a List (PUT)
#### 16. Remove Records from a List (PUT)
#### 17. Delete All Records from a List (DELETE)


### List Folders Management

#### 18. Retrieves a folder (GET)
#### 19. Creates a folder (POST)
#### 20. Moves a folder (PUT)
#### 21. Moves a list to a given folder (PUT)
#### 22. Rename a folder (PUT)
#### 23. Deletes a folder (DELETE)


### Legacy List ID Mapping

#### 24. Translate Legacy List Id to Modern List Id (GET)
#### 25. Translate Legacy List Id to Modern List Id in Batch (POST)


**Note:**  This documentation is a template.  You must replace placeholders like  `listId`, `objectTypeId`,  `listName`,  and add missing response examples and schemas from the original API documentation.  Also, the  `processingType` values (MANUAL, SNAPSHOT, etc.) need to be defined.  Finally, provide the complete request body for the `Update List Name` endpoint.
