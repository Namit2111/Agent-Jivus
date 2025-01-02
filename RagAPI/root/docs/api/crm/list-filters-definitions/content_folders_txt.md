# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, allowing management of list memberships for object lists.  Requires either Marketing Hub Starter or Content Hub Starter or higher.

## Use Cases

* Bulk adding contacts to a list.
* Removing company records from a company list.

## Related Guide

[HubSpot Lists Guide](LINK_TO_GUIDE_HERE)  *(Replace LINK_TO_GUIDE_HERE with the actual link)*


## API Endpoints

All endpoints use `/crm/v3/lists/` as a base path and require authentication via `Bearer YOUR_ACCESS_TOKEN` in the authorization header.  Standard API rate limits apply to all endpoints.

### Lists Management

| Method | Endpoint                     | Description                                                                     | Scopes                                     | Response Code | Notes                                                                          |
|--------|------------------------------|---------------------------------------------------------------------------------|---------------------------------------------|----------------|---------------------------------------------------------------------------------|
| GET    | `/crm/v3/lists/{listId}`     | Fetch a single list by ILS list ID.                                           | `crm.lists.read`                            | 200            | `{listId}` is the Internal List ID.                                          |
| GET    | `/crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}` | Fetch a single list by list name and object type.                             | `crm.lists.read`                            | 200            |                                                                                 |
| GET    | `/crm/v3/lists/`             | Fetch multiple lists by providing a comma-separated list of `listIds`.          | `crm.lists.read`                            | 200            | Returns definitions of all lists for the provided IDs.                         |
| POST   | `/crm/v3/lists/`             | Create a new list.                                                              | `cms.membership.access_groups.write` or `crm.lists.write` | 200            | Requires a JSON payload with list details (see example below).                 |
| POST   | `/crm/v3/lists/search`       | Search lists by name or page through all lists (empty query).                  | `crm.lists.read`                            | 200            | Requires a JSON payload with search parameters (see example below).            |
| PUT    | `/crm/v3/lists/{listId}/restore` | Restore a previously deleted list.                                              | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 204            | Restores lists up to 90 days after deletion.                               |
| PUT    | `/crm/v3/lists/{listId}/update-list-filters` | Update the filter branch definition of a DYNAMIC list.                         | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200            | Re-evaluates and updates list memberships.                                   |
| PUT    | `/crm/v3/lists/{listId}/update-list-name` | Update the name of a list.                                                      | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200            | Name must be globally unique.                                                |
| DELETE | `/crm/v3/lists/{listId}`     | Delete a list.                                                                  | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 204            | Lists can be restored up to 90 days after deletion.                          |


### List Memberships Management

| Method | Endpoint                                         | Description                                                                              | Scopes                                     | Response Code | Notes                                                                                                   |
|--------|-------------------------------------------------|------------------------------------------------------------------------------------------|---------------------------------------------|----------------|----------------------------------------------------------------------------------------------------------|
| GET    | `/crm/v3/lists/{listId}/memberships/join-order`  | Fetch list memberships ordered by added-to-list date.                                    | `crm.lists.read`                            | 200            |                                                                                                          |
| GET    | `/crm/v3/lists/{listId}/memberships`             | Fetch list memberships ordered by record ID.                                             | `crm.lists.read`                            | 200            |                                                                                                          |
| GET    | `/crm/v3/lists/records/{objectTypeId}/{recordId}/memberships` | Get lists a record is a member of.                                                       | `crm.lists.read`                            | 200            |                                                                                                          |
| PUT    | `/crm/v3/lists/{listId}/memberships/add-from/{sourceListId}` | Add all records from a source list to a destination list.                               | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 204            | Destination list must have `processingType` of `MANUAL` or `SNAPSHOT`. Source list can have any type. |
| PUT    | `/crm/v3/lists/{listId}/memberships/add-and-remove` | Add and/or remove records from a list.                                                   | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200            | Requires JSON payload with `recordIdsToAdd` and `recordIdsToRemove` arrays.                |
| PUT    | `/crm/v3/lists/{listId}/memberships/add`        | Add records to a list.                                                                 | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200            | Requires JSON payload with an array of record IDs.                                                   |
| PUT    | `/crm/v3/lists/{listId}/memberships/remove`     | Remove records from a list.                                                             | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200            | Requires JSON payload with an array of record IDs.                                                   |
| DELETE | `/crm/v3/lists/{listId}/memberships`             | Remove all records from a list (list itself remains).                                 | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 204            | Only works for lists with `processingType` of `MANUAL` or `SNAPSHOT`.                             |


### List Folders Management

| Method | Endpoint                                   | Description                                                                | Scopes                                     | Response Code | Notes                                                                      |
|--------|-------------------------------------------|----------------------------------------------------------------------------|---------------------------------------------|----------------|------------------------------------------------------------------------------|
| GET    | `/crm/v3/lists/folders`                    | Retrieves a folder and its child folders.                               | `crm.lists.read`                            | 200            |                                                                              |
| POST   | `/crm/v3/lists/folders`                    | Creates a new folder.                                                     | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200            | Requires JSON payload with `parentFolderId` and `name`.                      |
| PUT    | `/crm/v3/lists/folders/{folderId}/move/{newParentFolderId}` | Moves a folder to a new parent folder.                                    | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200            |                                                                              |
| PUT    | `/crm/v3/lists/folders/move-list`           | Moves a list to a given folder.                                          | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 204            | Requires JSON payload with `listId` and `newFolderId`.                      |
| PUT    | `/crm/v3/lists/folders/{folderId}/rename`   | Renames a folder.                                                         | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200            |                                                                              |
| DELETE | `/crm/v3/lists/folders/{folderId}`          | Deletes a folder.                                                          | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 204            |                                                                              |


### Legacy List ID Mapping (Expires May 30, 2025)

| Method | Endpoint                | Description                                                                          | Scopes             | Response Code | Notes                                                                                     |
|--------|-------------------------|--------------------------------------------------------------------------------------|---------------------|----------------|---------------------------------------------------------------------------------------------|
| GET    | `/crm/v3/lists/idmapping` | Translate a legacy list ID to a modern list ID.                                      | `crm.lists.read` | 200            |                                                                                             |
| POST   | `/crm/v3/lists/idmapping` | Translate multiple legacy list IDs to modern list IDs (max 10,000).                   | `crm.lists.read` | 200            | Requires JSON payload with an array of legacy IDs.                                            |


## Examples

**Create List (POST /crm/v3/lists/)**

```json
{
  "objectTypeId": "contacts",
  "processingType": "MANUAL",
  "customProperties": {
    "additionalProp1": "value1",
    "additionalProp2": "value2"
  },
  "listFolderId": 0,
  "name": "My New List",
  "filterBranch": {
    "filterBranchType": "OR",
    "filterGroups": [ /* filter group definitions */ ]
  }
}
```

**Add Records to a List (PUT /crm/v3/lists/{listId}/memberships/add)**

```json
[
  "recordId1",
  "recordId2"
]
```


**Search Lists (POST /crm/v3/lists/search)**

```json
{
  "query": "My List",
  "count": 10,
  "offset": 0
}
```


**Note:**  Replace placeholders like `{listId}`, `objectTypeId`, `recordId`, `sourceListId`, `folderId`, and `newParentFolderId` with actual values.  The `filterGroups` section in the create list example requires further definition based on the desired filtering criteria.  Refer to the HubSpot API documentation for details on filter group structure.  Response examples and schemas are omitted here due to space constraints, but are available in the linked HubSpot documentation.  Also, error handling and more detailed response structures are not fully covered for brevity.  Always refer to official HubSpot API documentation for the most up-to-date information.
