# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, allowing management of list memberships for object lists.  Requires either Marketing Hub Starter or Content Hub Starter or higher.

## API Overview

The Lists API provides endpoints for creating, retrieving, updating, and deleting lists, as well as managing their memberships.  It supports various operations, including bulk adding and removing records, searching for lists, and restoring deleted lists.  The API uses standard RESTful principles with JSON payloads.  Authentication is via Private apps or OAuth.


## Authentication

All requests require an access token.  This token is obtained through either Private app or OAuth 2.0 authentication methods.  Include the token in the `Authorization` header as `Bearer YOUR_ACCESS_TOKEN`.


## Rate Limits

Standard HubSpot API rate limits apply.  Refer to HubSpot's API documentation for details.


## Scopes

The required scopes vary by endpoint.  Common scopes include:

* `crm.lists.read`:  For reading list data.
* `crm.lists.write`: For creating, updating, and deleting lists.
* `cms.membership.access_groups.write`: Required for certain list modification operations.


## Endpoints

The following sections detail individual API endpoints.  Each section includes the HTTP method, endpoint URL, request parameters, example requests (cURL), and expected responses.


### Lists Management

#### 1. Fetch List by ID

* **Method:** `GET`
* **URL:** `/crm/v3/lists/{listId}`
* **Parameters:** `includeFilters=false` (optional, defaults to `false`)
* **Scopes:** `crm.lists.read`
* **Description:** Retrieves a single list by its ILS list ID.

```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/listId?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

#### 2. Fetch List by Name

* **Method:** `GET`
* **URL:** `/crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}`
* **Parameters:** `includeFilters=false` (optional, defaults to `false`)
* **Scopes:** `crm.lists.read`
* **Description:** Retrieves a single list by its name and object type.

```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/object-type-id/objectTypeId/name/listName?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

#### 3. Fetch Multiple Lists

* **Method:** `GET`
* **URL:** `/crm/v3/lists/`
* **Parameters:** `listId` (comma-separated list of IDs) `includeFilters=false` (optional, defaults to `false`)
* **Scopes:** `crm.lists.read`
* **Description:** Retrieves multiple lists based on provided `listId`s.

```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

#### 4. Create List

* **Method:** `POST`
* **URL:** `/crm/v3/lists/`
* **Parameters:** (in JSON body)
    * `objectTypeId`:  (string)
    * `processingType`: (string, e.g., "MANUAL", "DYNAMIC", "SNAPSHOT")
    * `customProperties`: (object)
    * `listFolderId`: (integer)
    * `name`: (string)
    * `filterBranch`: (object, for dynamic lists)
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`
* **Description:** Creates a new list.

```bash
curl --request POST \
     --url https://api.hubapi.com/crm/v3/lists/ \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{
         "objectTypeId": "string",
         "processingType": "string",
         "customProperties": { ... },
         "listFolderId": 0,
         "name": "string",
         "filterBranch": { ... }
     }'
```

#### 5. Search Lists

* **Method:** `POST`
* **URL:** `/crm/v3/lists/search`
* **Parameters:** (in JSON body)
    * `listIds`: (array of strings)
    * `offset`: (integer)
    * `query`: (string)
    * `count`: (integer)
    * `processingTypes`: (array of strings)
    * `additionalProperties`: (array of strings)
    * `sort`: (string)
* **Scopes:** `crm.lists.read`
* **Description:** Searches lists by name or paginates through all lists.

```bash
curl --request POST \
     --url https://api.hubapi.com/crm/v3/lists/search \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{ ... }'
```

#### 6. Restore a List

* **Method:** `PUT`
* **URL:** `/crm/v3/lists/{listId}/restore`
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Description:** Restores a previously deleted list.

```bash
curl --request PUT \
     --url https://api.hubapi.com/crm/v3/lists/listId/restore \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

#### 7. Update List Filter Definition

* **Method:** `PUT`
* **URL:** `/crm/v3/lists/{listId}/update-list-filters`
* **Parameters:** `enrollObjectsInWorkflows=false` (optional)  (JSON body contains `filterBranch`)
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Description:** Updates the filter definition of a dynamic list.

```bash
curl --request PUT \
     --url 'https://api.hubapi.com/crm/v3/lists/listId/update-list-filters?enrollObjectsInWorkflows=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{ "filterBranch": { ... } }'
```

#### 8. Update List Name

* **Method:** `PUT`
* **URL:** `/crm/v3/lists/{listId}/update-list-name`
* **Parameters:** `includeFilters=false` (optional, defaults to `false`)
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Description:** Updates the name of a list.

```bash
curl --request PUT \
     --url 'https://api.hubapi.com/crm/v3/lists/listId/update-list-name?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

#### 9. Delete a List

* **Method:** `DELETE`
* **URL:** `/crm/v3/lists/{listId}`
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Description:** Deletes a list.

```bash
curl --request DELETE \
     --url https://api.hubapi.com/crm/v3/lists/listId \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```



### List Memberships Management

**(Note:  Many of these endpoints only work for lists with `processingType` of MANUAL or SNAPSHOT and/or have membership limits.)**

#### 10. Fetch List Memberships Ordered by Added to List Date

* **Method:** `GET`
* **URL:** `/crm/v3/lists/{listId}/memberships/join-order`
* **Parameters:** `limit` (integer, optional) `after`, `before` (optional offset parameters for pagination)
* **Scopes:** `crm.lists.read`
* **Description:** Retrieves list memberships ordered by join date.

```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/listId/memberships/join-order?limit=100' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

#### 11. Fetch List Memberships Ordered by ID

* **Method:** `GET`
* **URL:** `/crm/v3/lists/{listId}/memberships`
* **Parameters:** `limit` (integer, optional) `after`, `before` (optional offset parameters for pagination)
* **Scopes:** `crm.lists.read`
* **Description:** Retrieves list memberships ordered by record ID.

```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/listId/memberships?limit=100' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

#### 12. Get Lists Record is Member Of

* **Method:** `GET`
* **URL:** `/crm/v3/lists/records/{objectTypeId}/{recordId}/memberships`
* **Scopes:** `crm.lists.read`
* **Description:** Retrieves lists a specific record is a member of.

```bash
curl --request GET \
     --url https://api.hubapi.com/crm/v3/lists/records/objectTypeId/recordId/memberships \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

#### 13. Add All Records from a Source List to a Destination List

* **Method:** `PUT`
* **URL:** `/crm/v3/lists/{listId}/memberships/add-from/{sourceListId}`
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Description:** Adds all records from a source list to a destination list.

```bash
curl --request PUT \
     --url https://api.hubapi.com/crm/v3/lists/listId/memberships/add-from/sourceListId \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

#### 14. Add and/or Remove Records from a List

* **Method:** `PUT`
* **URL:** `/crm/v3/lists/{listId}/memberships/add-and-remove`
* **Parameters:** (JSON body with `recordIdsToRemove` and `recordIdsToAdd` arrays)
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Description:** Adds and/or removes records from a list.

```bash
curl --request PUT \
     --url https://api.hubapi.com/crm/v3/lists/listId/memberships/add-and-remove \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{ "recordIdsToRemove": [...], "recordIdsToAdd": [...] }'
```

#### 15. Add Records to a List

* **Method:** `PUT`
* **URL:** `/crm/v3/lists/{listId}/memberships/add`
* **Parameters:** (JSON body with array of recordIds)
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Description:** Adds records to a list.

```bash
curl --request PUT \
     --url https://api.hubapi.com/crm/v3/lists/listId/memberships/add \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '[ ... ]'
```

#### 16. Remove Records from a List

* **Method:** `PUT`
* **URL:** `/crm/v3/lists/{listId}/memberships/remove`
* **Parameters:** (JSON body with array of recordIds)
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Description:** Removes records from a list.

```bash
curl --request PUT \
     --url https://api.hubapi.com/crm/v3/lists/listId/memberships/remove \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '[ ... ]'
```

#### 17. Delete All Records from a List

* **Method:** `DELETE`
* **URL:** `/crm/v3/lists/{listId}/memberships`
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Description:** Removes all records from a list (list itself remains).

```bash
curl --request DELETE \
     --url https://api.hubapi.com/crm/v3/lists/listId/memberships \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```


### List Folders Management

#### 18. Retrieves a folder.

* **Method:** `GET`
* **URL:** `/crm/v3/lists/folders`
* **Parameters:** `folderId` (integer, optional)
* **Scopes:** `crm.lists.read`
* **Description:** Retrieves a folder and its child folders and lists.

```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/folders?folderId=0' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

#### 19. Creates a folder

* **Method:** `POST`
* **URL:** `/crm/v3/lists/folders`
* **Parameters:** (JSON body with `parentFolderId` and `name`)
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Description:** Creates a new list folder.

```bash
curl --request POST \
     --url https://api.hubapi.com/crm/v3/lists/folders \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{ "parentFolderId": "string", "name": "string" }'
```

#### 20. Moves a folder

* **Method:** `PUT`
* **URL:** `/crm/v3/lists/folders/{folderId}/move/{newParentFolderId}`
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Description:** Moves a folder to a new parent folder.

```bash
curl --request PUT \
     --url https://api.hubapi.com/crm/v3/lists/folders/folderId/move/newParentFolderId \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

#### 21. Moves a list to a given folder

* **Method:** `PUT`
* **URL:** `/crm/v3/lists/folders/move-list`
* **Parameters:** (JSON body with `listId` and `newFolderId`)
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Description:** Moves a list to a specified folder.

```bash
curl --request PUT \
     --url https://api.hubapi.com/crm/v3/lists/folders/move-list \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '{ "listId": "string", "newFolderId": "string" }'
```

#### 22. Rename a folder

* **Method:** `PUT`
* **URL:** `/crm/v3/lists/folders/{folderId}/rename`
* **Parameters:**  (JSON body with new name)
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Description:** Renames a folder.

```bash
curl --request PUT \
     --url https://api.hubapi.com/crm/v3/lists/folders/folderId/rename \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

#### 23. Deletes a folder

* **Method:** `DELETE`
* **URL:** `/crm/v3/lists/folders/{folderId}`
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Description:** Deletes a folder.

```bash
curl --request DELETE \
     --url https://api.hubapi.com/crm/v3/lists/folders/folderId \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```


### Legacy List ID Mapping (Expires May 30, 2025)

#### 24. Translate Legacy List Id to Modern List Id

* **Method:** `GET`
* **URL:** `/crm/v3/lists/idmapping`
* **Scopes:** `crm.lists.read`
* **Description:** Translates a single legacy list ID to a modern list ID.

```bash
curl --request GET \
     --url https://api.hubapi.com/crm/v3/lists/idmapping \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

#### 25. Translate Legacy List Id to Modern List Id in Batch

* **Method:** `POST`
* **URL:** `/crm/v3/lists/idmapping`
* **Parameters:** (JSON body with array of legacy list IDs)
* **Scopes:** `crm.lists.read`
* **Description:** Translates multiple legacy list IDs to modern list IDs (max 10,000).

```bash
curl --request POST \
     --url https://api.hubapi.com/crm/v3/lists/idmapping \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '[ ... ]'
```


**Note:**  Replace placeholders like `{listId}`, `{objectTypeId}`, `{listName}`, etc., with actual values.  The examples use cURL, but the API can be accessed using any HTTP client library in various programming languages.  Always refer to the official HubSpot API documentation for the most up-to-date information and schema details for request and response bodies.
