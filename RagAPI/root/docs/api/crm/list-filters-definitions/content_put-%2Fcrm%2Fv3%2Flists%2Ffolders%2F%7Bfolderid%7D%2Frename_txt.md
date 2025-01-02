# HubSpot Lists API v3 Documentation

This document outlines the HubSpot Lists API v3, providing details on managing list memberships for object lists.  The API requires either Marketing Hub Starter or Content Hub Starter or higher.


## Use Cases

* Bulk adding contacts to a list.
* Removing company records from a company list.


## API Endpoints

The API offers various endpoints for managing lists, memberships, and folders.  All endpoints require authentication via Private Apps or OAuth, and use `https://api.hubapi.com/crm/v3/` as the base URL.  Replace `YOUR_ACCESS_TOKEN` with your actual access token.  Standard API rate limits apply to all endpoints.

**Authentication:**  Use `Bearer YOUR_ACCESS_TOKEN` in the `Authorization` header.


### Lists Management

| Method | Endpoint                     | Description                                                                         | Scopes                                        | HTTP Status |
|--------|------------------------------|-------------------------------------------------------------------------------------|-------------------------------------------------|-------------|
| GET    | `/lists/{listId}`              | Fetch a single list by ILS list ID.                                                | `crm.lists.read`                               | 200         |
| GET    | `/lists/object-type-id/{objectTypeId}/name/{listName}` | Fetch a single list by list name and object type.                               | `crm.lists.read`                               | 200         |
| GET    | `/lists/`                      | Fetch multiple lists by ILS list ID.                                               | `crm.lists.read`                               | 200         |
| POST   | `/lists/`                      | Create a new list.                                                                  | `cms.membership.access_groups.write` or `crm.lists.write` | 200         |
| POST   | `/lists/search`               | Search lists by name or page through all lists (empty query).                     | `crm.lists.read`                               | 200         |
| PUT    | `/lists/{listId}/restore`      | Restore a previously deleted list (up to 90 days after deletion).                 | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 204         |
| PUT    | `/lists/{listId}/update-list-filters` | Update the filter branch definition of a DYNAMIC list.                            | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200         |
| PUT    | `/lists/{listId}/update-list-name` | Update the name of a list.                                                        | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200         |
| DELETE | `/lists/{listId}`              | Delete a list (restorable for 90 days).                                          | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 204         |


#### Example: Fetch List by ID (GET)

**Request:**

```bash
curl --request GET \
     --url 'https://api.hubapi.com/crm/v3/lists/123?includeFilters=false' \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

**Response (Example):**

```json
{
  "listId": 123,
  "name": "My List",
  "objectTypeId": "contacts",
  // ... other properties
}
```


### List Memberships Management

| Method | Endpoint                                      | Description                                                                                                | Scopes                                        | HTTP Status |
|--------|-----------------------------------------------|------------------------------------------------------------------------------------------------------------|-------------------------------------------------|-------------|
| GET    | `/lists/{listId}/memberships/join-order`      | Fetch list memberships ordered by added date.                                                              | `crm.lists.read`                               | 200         |
| GET    | `/lists/{listId}/memberships`                 | Fetch list memberships ordered by record ID.                                                              | `crm.lists.read`                               | 200         |
| GET    | `/lists/records/{objectTypeId}/{recordId}/memberships` | Get lists a record is a member of.                                                                     | `crm.lists.read`                               | 200         |
| PUT    | `/lists/{listId}/memberships/add-from/{sourceListId}` | Add all records from a source list to a destination list.                                              | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 204         |
| PUT    | `/lists/{listId}/memberships/add-and-remove`   | Add and/or remove records from a list.                                                                   | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200         |
| PUT    | `/lists/{listId}/memberships/add`             | Add records to a list.                                                                                   | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200         |
| PUT    | `/lists/{listId}/memberships/remove`           | Remove records from a list.                                                                                 | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200         |
| DELETE | `/lists/{listId}/memberships`                 | Remove all records from a list (list itself is not deleted).                                            | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 204         |



#### Example: Add Records to a List (PUT)

**Request:**

```bash
curl --request PUT \
     --url https://api.hubapi.com/crm/v3/lists/123/memberships/add \
     --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
     --header 'content-type: application/json' \
     --data '[1, 2, 3]'
```

**Response (Example -  HTTP 200):**  An empty response body usually indicates success.



### List Folders Management

| Method | Endpoint                                   | Description                                                                           | Scopes                                        | HTTP Status |
|--------|--------------------------------------------|---------------------------------------------------------------------------------------|-------------------------------------------------|-------------|
| GET    | `/lists/folders`                           | Retrieves a folder and its children.                                                  | `crm.lists.read`                               | 200         |
| POST   | `/lists/folders`                           | Creates a new folder.                                                                 | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200         |
| PUT    | `/lists/folders/{folderId}/move/{newParentFolderId}` | Moves a folder to a new parent folder.                                                 | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200         |
| PUT    | `/lists/folders/move-list`                  | Moves a list to a given folder.                                                       | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 204         |
| PUT    | `/lists/folders/{folderId}/rename`          | Renames a folder.                                                                    | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200         |
| DELETE | `/lists/folders/{folderId}`                 | Deletes a folder.                                                                     | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 204         |


### Legacy List ID Mapping (Expires May 30, 2025)

| Method | Endpoint                 | Description                                                                             | Scopes               | HTTP Status |
|--------|--------------------------|-----------------------------------------------------------------------------------------|-----------------------|-------------|
| GET    | `/lists/idmapping`       | Translate a legacy list ID to a modern list ID.                                        | `crm.lists.read`      | 200         |
| POST   | `/lists/idmapping`       | Translate a batch of legacy list IDs to modern list IDs (max 10,000).                 | `crm.lists.read`      | 200         |


**Note:**  Always refer to the official HubSpot API documentation for the most up-to-date information on available endpoints, parameters, schemas, and potential changes.  The examples provided here are simplified and might require adjustments based on your specific needs.
