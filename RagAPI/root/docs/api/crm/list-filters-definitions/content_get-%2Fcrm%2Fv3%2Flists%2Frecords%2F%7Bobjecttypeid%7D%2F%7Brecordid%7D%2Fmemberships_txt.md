# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, allowing management of list memberships for object lists.  Requires either Marketing Hub Starter or Content Hub Starter or higher.

## Use Cases

* Bulk adding contacts to a list.
* Removing company records from a company list.

## Related Guide

[HubSpot Lists Guide](<Insert Link Here>)


## API Endpoints

All endpoints use the base URL: `https://api.hubapi.com/crm/v3/lists/` and require authentication via `Bearer YOUR_ACCESS_TOKEN`.  Replace `YOUR_ACCESS_TOKEN` with your actual access token.  Standard API rate limits apply to all endpoints.

**Authentication Methods:** Private apps, OAuth

**Error Handling:**  (Information missing from provided text, needs to be added)  Assume standard HTTP status codes are used (e.g., 200 for success, 400 for bad request, etc.)


### Lists Management

| Method | Endpoint                     | Description                                                              | Scopes                                      | Request Body (example)                                                                 | Response (example) | HTTP Status |
|--------|------------------------------|--------------------------------------------------------------------------|----------------------------------------------|-----------------------------------------------------------------------------------------|--------------------|--------------|
| GET    | `/crm/v3/lists/{listId}`       | Fetch a single list by ILS list ID.                                      | `crm.lists.read`                             | None                                                                                   | `{listId:123, name:"My List"}` | 200          |
| GET    | `/crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}` | Fetch a single list by list name and object type.                     | `crm.lists.read`                             | None                                                                                   | `{listId:123, name:"My List"}` | 200          |
| GET    | `/crm/v3/lists/`              | Fetch multiple lists by ILS list IDs.                                   | `crm.lists.read`                             | None                                                                                   | `[{listId:123, name:"My List"}, ...]` | 200          |
| POST   | `/crm/v3/lists/`              | Create a new list.                                                       | `cms.membership.access_groups.write` or `crm.lists.write` | `{"objectTypeId": "contacts", "processingType": "MANUAL", "name": "New List", ...}` | `{listId: 456, ...}`     | 200          |
| POST   | `/crm/v3/lists/search`        | Search lists by name or page through all lists.                       | `crm.lists.read`                             | `{"query": "my list", "count": 10, ...}`                                               | `[{listId:123, name:"My List"}, ...]` | 200          |
| PUT    | `/crm/v3/lists/{listId}/restore` | Restore a previously deleted list.                                     | `cms.membership.access_groups.write` or `crm.lists.write`, `crm.lists.read` | None                                                                                   | None                 | 204          |
| PUT    | `/crm/v3/lists/{listId}/update-list-filters` | Update the filter branch definition of a DYNAMIC list.                 | `cms.membership.access_groups.write` or `crm.lists.write`, `crm.lists.read` | `{"filterBranch": { "filterBranchType": "OR", ...}}`                               | `{listId:123, ...}` | 200          |
| PUT    | `/crm/v3/lists/{listId}/update-list-name` | Update the name of a list.                                             | `cms.membership.access_groups.write` or `crm.lists.write`, `crm.lists.read` | None                                                                                   | `{listId:123, ...}` | 200          |
| DELETE | `/crm/v3/lists/{listId}`       | Delete a list.                                                            | `cms.membership.access_groups.write` or `crm.lists.write`, `crm.lists.read` | None                                                                                   | None                 | 204          |


### List Memberships

| Method | Endpoint                                            | Description                                                                                                   | Scopes             | Request Body (example)                                                       | Response (example)                    | HTTP Status |
|--------|----------------------------------------------------|---------------------------------------------------------------------------------------------------------------|----------------------|---------------------------------------------------------------------------------|---------------------------------------|--------------|
| GET    | `/crm/v3/lists/{listId}/memberships/join-order`      | Fetch list memberships ordered by added-to-list date.                                                     | `crm.lists.read`     | None                                                                               | `[{recordId:1, addedAt: ...}, ...]`    | 200          |
| GET    | `/crm/v3/lists/{listId}/memberships`                | Fetch list memberships ordered by record ID.                                                               | `crm.lists.read`     | None                                                                               | `[{recordId:1, addedAt: ...}, ...]`    | 200          |
| GET    | `/crm/v3/lists/records/{objectTypeId}/{recordId}/memberships` | Get lists a record is a member of.                                                                       | `crm.lists.read`     | None                                                                               | `[{listId:123, name:"My List"}, ...]` | 200          |
| PUT    | `/crm/v3/lists/{listId}/memberships/add-from/{sourceListId}` | Add all records from a source list to a destination list.                                                  | `cms.membership.access_groups.write` or `crm.lists.write`, `crm.lists.read` | None                                                                               | None                                 | 204          |
| PUT    | `/crm/v3/lists/{listId}/memberships/add-and-remove` | Add and/or remove records from a list.                                                                     | `cms.membership.access_groups.write` or `crm.lists.write`, `crm.lists.read` | `{"recordIdsToAdd":[1,2,3],"recordIdsToRemove":[4]}`                       | `{}`                                  | 200          |
| PUT    | `/crm/v3/lists/{listId}/memberships/add`            | Add records to a list.                                                                                       | `cms.membership.access_groups.write` or `crm.lists.write`, `crm.lists.read` | `["1","2","3"]`                                                               | `{}`                                  | 200          |
| PUT    | `/crm/v3/lists/{listId}/memberships/remove`         | Remove records from a list.                                                                                  | `cms.membership.access_groups.write` or `crm.lists.write`, `crm.lists.read` | `["1","2","3"]`                                                               | `{}`                                  | 200          |
| DELETE | `/crm/v3/lists/{listId}/memberships`                | Remove all records from a list (list itself is not deleted).                                              | `cms.membership.access_groups.write` or `crm.lists.write`, `crm.lists.read` | None                                                                               | None                                 | 204          |


### List Folders

| Method | Endpoint                                   | Description                                                                   | Scopes                                      | Request Body (example)                     | Response (example)                    | HTTP Status |
|--------|--------------------------------------------|-------------------------------------------------------------------------------|----------------------------------------------|---------------------------------------------|---------------------------------------|--------------|
| GET    | `/crm/v3/lists/folders`                     | Retrieves a folder and its children.                                           | `crm.lists.read`                             | None                                             | `{folderId: 1, name: "My Folder", ...}` | 200          |
| POST   | `/crm/v3/lists/folders`                     | Creates a new folder.                                                        | `cms.membership.access_groups.write` or `crm.lists.write`, `crm.lists.read` | `{"parentFolderId": 0, "name": "New Folder"}` | `{folderId: 456, ...}`                 | 200          |
| PUT    | `/crm/v3/lists/folders/{folderId}/move/{newParentFolderId}` | Moves a folder to a new parent folder.                                       | `cms.membership.access_groups.write` or `crm.lists.write`, `crm.lists.read` | None                                             | `{folderId: 1, ...}`                    | 200          |
| PUT    | `/crm/v3/lists/folders/move-list`           | Moves a list to a given folder.                                              | `cms.membership.access_groups.write` or `crm.lists.write`, `crm.lists.read` | `{"listId": "123", "newFolderId": "456"}` | None                                 | 204          |
| PUT    | `/crm/v3/lists/folders/{folderId}/rename`    | Renames a folder.                                                             | `cms.membership.access_groups.write` or `crm.lists.write`, `crm.lists.read` | None                                             | `{folderId: 1, ...}`                    | 200          |
| DELETE | `/crm/v3/lists/folders/{folderId}`           | Deletes a folder.                                                             | `cms.membership.access_groups.write` or `crm.lists.write`, `crm.lists.read` | None                                             | None                                 | 204          |


### Legacy List ID Mapping (Expires May 30, 2025)

| Method | Endpoint                     | Description                                                                          | Scopes             | Request Body (example)                     | Response (example)                    | HTTP Status |
|--------|------------------------------|--------------------------------------------------------------------------------------|----------------------|---------------------------------------------|---------------------------------------|--------------|
| GET    | `/crm/v3/lists/idmapping`      | Translate a legacy list ID to a modern list ID.                                  | `crm.lists.read`     | None                                             | `{legacyId: 1, id: 123}`                | 200          |
| POST   | `/crm/v3/lists/idmapping`      | Translate multiple legacy list IDs to modern list IDs (max 10,000).             | `crm.lists.read`     | `["1", "2", "3"]`                           | `[{legacyId: 1, id: 123}, ...]`          | 200          |


**Note:**  Response examples are simplified.  The actual responses will contain more detailed information.  Schema details are missing from the provided text and should be included in a complete documentation.  Remember to replace placeholders like `{listId}`, `{objectTypeId}`, etc. with actual values.  Consider adding sections on rate limits, error handling, and request examples in other programming languages (Node.js, PHP, Ruby, Python, C#) beyond the cURL examples given.
