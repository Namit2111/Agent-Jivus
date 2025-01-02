# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, allowing management of list memberships for object lists.  Requires either Marketing Hub Starter or Content Hub Starter or higher.

## Use Cases

* Bulk adding contacts to a list.
* Removing company records from a company list.


## API Endpoints

All endpoints are located under the base URL: `https://api.hubapi.com/crm/v3/lists/`

Unless otherwise specified, all endpoints require authentication via `Bearer YOUR_ACCESS_TOKEN` in the `Authorization` header.  Standard API rate limits apply.


### Lists Management

| Method | Endpoint                     | Description                                                                     | Scopes                                   | HTTP Status |
|--------|------------------------------|---------------------------------------------------------------------------------|--------------------------------------------|-------------|
| GET    | `/crm/v3/lists/{listId}`      | Fetch a single list by ILS list ID.                                            | `crm.lists.read`                           | 200         |
| GET    | `/crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}` | Fetch a single list by list name and object type.                               | `crm.lists.read`                           | 200         |
| GET    | `/crm/v3/lists/`             | Fetch multiple lists by ILS list IDs.                                          | `crm.lists.read`                           | 200         |
| POST   | `/crm/v3/lists/`             | Create a new list.                                                              | `cms.membership.access_groups.write` or `crm.lists.write` | 200         |
| POST   | `/crm/v3/lists/search`       | Search lists by name or page through all lists (empty query).                 | `crm.lists.read`                           | 200         |
| PUT    | `/crm/v3/lists/{listId}/restore` | Restore a previously deleted list.                                             | `cms.membership.access_groups.write` or `crm.lists.write` | 204         |
| PUT    | `/crm/v3/lists/{listId}/update-list-filters` | Update the filter branch definition of a DYNAMIC list.                         | `cms.membership.access_groups.write` or `crm.lists.write` | 200         |
| PUT    | `/crm/v3/lists/{listId}/update-list-name` | Update the name of a list.                                                    | `cms.membership.access_groups.write` or `crm.lists.write` | 200         |
| DELETE | `/crm/v3/lists/{listId}`      | Delete a list.                                                                  | `cms.membership.access_groups.write` or `crm.lists.write` | 204         |


#### Example: Fetch List by ID (GET)

**Request:**

```bash
curl --request GET \
--url 'https://api.hubapi.com/crm/v3/lists/listId?includeFilters=false' \
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

| Method | Endpoint                                           | Description                                                                                          | Scopes                                   | HTTP Status |
|--------|----------------------------------------------------|------------------------------------------------------------------------------------------------------|--------------------------------------------|-------------|
| GET    | `/crm/v3/lists/{listId}/memberships/join-order`   | Fetch list memberships ordered by added-to-list date.                                             | `crm.lists.read`                           | 200         |
| GET    | `/crm/v3/lists/{listId}/memberships`               | Fetch list memberships ordered by record ID.                                                          | `crm.lists.read`                           | 200         |
| GET    | `/crm/v3/lists/records/{objectTypeId}/{recordId}/memberships` | Get lists a record is a member of.                                                              | `crm.lists.read`                           | 200         |
| PUT    | `/crm/v3/lists/{listId}/memberships/add-from/{sourceListId}` | Add all records from a source list to a destination list.                                         | `cms.membership.access_groups.write` or `crm.lists.write` | 204         |
| PUT    | `/crm/v3/lists/{listId}/memberships/add-and-remove` | Add and/or remove records from a list.                                                             | `cms.membership.access_groups.write` or `crm.lists.write` | 200         |
| PUT    | `/crm/v3/lists/{listId}/memberships/add`           | Add records to a list.                                                                            | `cms.membership.access_groups.write` or `crm.lists.write` | 200         |
| PUT    | `/crm/v3/lists/{listId}/memberships/remove`        | Remove records from a list.                                                                         | `cms.membership.access_groups.write` or `crm.lists.write` | 200         |
| DELETE | `/crm/v3/lists/{listId}/memberships`               | Remove all records from a list (list itself remains).                                             | `cms.membership.access_groups.write` or `crm.lists.write` | 204         |


### List Folders Management

| Method | Endpoint                                         | Description                                                              | Scopes                                   | HTTP Status |
|--------|-------------------------------------------------|--------------------------------------------------------------------------|--------------------------------------------|-------------|
| GET    | `/crm/v3/lists/folders`                         | Retrieves a folder and its children.                                    | `crm.lists.read`                           | 200         |
| POST   | `/crm/v3/lists/folders`                         | Creates a folder.                                                        | `cms.membership.access_groups.write` or `crm.lists.write` | 200         |
| PUT    | `/crm/v3/lists/folders/{folderId}/move/{newParentFolderId}` | Moves a folder.                                                          | `cms.membership.access_groups.write` or `crm.lists.write` | 200         |
| PUT    | `/crm/v3/lists/folders/move-list`                | Moves a list to a given folder.                                           | `cms.membership.access_groups.write` or `crm.lists.write` | 204         |
| PUT    | `/crm/v3/lists/folders/{folderId}/rename`        | Renames a folder.                                                        | `cms.membership.access_groups.write` or `crm.lists.write` | 200         |
| DELETE | `/crm/v3/lists/folders/{folderId}`                | Deletes a folder.                                                        | `cms.membership.access_groups.write` or `crm.lists.write` | 204         |


### Legacy List ID Mapping (Temporary - Expires May 30, 2025)

| Method | Endpoint                     | Description                                                                             | Scopes            | HTTP Status |
|--------|------------------------------|-----------------------------------------------------------------------------------------|--------------------|-------------|
| GET    | `/crm/v3/lists/idmapping`    | Translate a legacy list ID to a modern list ID.                                      | `crm.lists.read` | 200         |
| POST   | `/crm/v3/lists/idmapping`    | Translate multiple legacy list IDs to modern list IDs (max 10,000).                    | `crm.lists.read` | 200         |


**Note:**  Replace placeholders like `{listId}`, `{objectTypeId}`, `{listName}`, `{folderId}`, `{sourceListId}`, and `{recordId}` with actual values.  The examples provided use `curl`, but the API can be accessed using any HTTP client library in various programming languages.  Refer to the HubSpot API documentation for detailed schema definitions and further information.
