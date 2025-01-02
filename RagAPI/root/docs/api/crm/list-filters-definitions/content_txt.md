# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, allowing management of list memberships for object lists.  Requires either Marketing Hub Starter or Content Hub Starter or higher.

## Use Cases

* Bulk adding contacts to a list.
* Removing company records from a company list.

## Related Guide

[HubSpot Lists Guide](LINK_TO_GUIDE_HERE)  *(Replace LINK_TO_GUIDE_HERE with actual link)*

## API Endpoints

All endpoints are under the base URL: `https://api.hubapi.com/crm/v3/lists/` and require authentication via `Bearer YOUR_ACCESS_TOKEN` in the header.  Standard API rate limits apply to all endpoints.

**Authentication Methods:** Private apps and OAuth.

**Note:**  `listId` refers to the HubSpot Internal List ID.  `objectTypeId` represents the type of object (e.g., contacts, companies).  `listName` is the name of the list.  `sourceListId` and `destinationListId` are used in list membership transfer operations.  `folderId` and `newParentFolderId` refer to list folder IDs.


### Lists Management

| Method | Endpoint                  | Description                                                                 | Scopes                                          | HTTP Status | Notes                                                                          |
|--------|---------------------------|-----------------------------------------------------------------------------|---------------------------------------------------|-------------|---------------------------------------------------------------------------------|
| GET    | `/crm/v3/lists/{listId}`   | Fetch a single list by ILS list ID.                                        | `crm.lists.read`                                   | 200        | Includes filters if `includeFilters=true` in query parameters.                  |
| GET    | `/crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}` | Fetch a single list by list name and object type.                            | `crm.lists.read`                                   | 200        | Includes filters if `includeFilters=true` in query parameters.                  |
| GET    | `/crm/v3/lists/`          | Fetch multiple lists by ILS list IDs.                                      | `crm.lists.read`                                   | 200        | Includes filters if `includeFilters=true` in query parameters.                  |
| POST   | `/crm/v3/lists/`          | Create a new list.                                                          | `cms.membership.access_groups.write` or `crm.lists.write` | 200        | Requires a JSON body with list details (see example below).                   |
| POST   | `/crm/v3/lists/search`    | Search lists by name or page through all lists (empty query).              | `crm.lists.read`                                   | 200        |  See example for request body structure.                                     |
| PUT    | `/crm/v3/lists/{listId}/restore` | Restore a previously deleted list.                                         | `cms.membership.access_groups.write` or `crm.lists.write` | 204        |  List must be deleted within 90 days.                                         |
| PUT    | `/crm/v3/lists/{listId}/update-list-filters` | Update a dynamic list's filter definition.                                 | `cms.membership.access_groups.write` or `crm.lists.write` | 200        | Re-evaluates and updates memberships.                                      |
| PUT    | `/crm/v3/lists/{listId}/update-list-name` | Update the name of a list.                                                   | `cms.membership.access_groups.write` or `crm.lists.write` | 200        | Name must be globally unique.                                              |
| DELETE | `/crm/v3/lists/{listId}`   | Delete a list.                                                             | `cms.membership.access_groups.write` or `crm.lists.write` | 204        | List can be restored within 90 days.                                         |


### List Memberships

| Method | Endpoint                                          | Description                                                                                             | Scopes                                          | HTTP Status | Notes                                                                                                |
|--------|---------------------------------------------------|---------------------------------------------------------------------------------------------------------|---------------------------------------------------|-------------|-----------------------------------------------------------------------------------------------------|
| GET    | `/crm/v3/lists/{listId}/memberships/join-order`   | Fetch list memberships ordered by added date.                                                           | `crm.lists.read`                                   | 200        |  Supports pagination using `after` and `before` parameters.                                       |
| GET    | `/crm/v3/lists/{listId}/memberships`              | Fetch list memberships ordered by record ID.                                                            | `crm.lists.read`                                   | 200        | Supports pagination using `after` and `before` parameters.                                       |
| GET    | `/crm/v3/lists/records/{objectTypeId}/{recordId}/memberships` | Get lists a record is a member of.                                                                   | `crm.lists.read`                                   | 200        |                                                                                                     |
| PUT    | `/crm/v3/lists/{listId}/memberships/add-from/{sourceListId}` | Add all records from a source list to a destination list.                                           | `cms.membership.access_groups.write` or `crm.lists.write` | 204        |  Destination list must be MANUAL or SNAPSHOT processing type. Source list can have any type.       |
| PUT    | `/crm/v3/lists/{listId}/memberships/add-and-remove` | Add and/or remove records from a list.                                                              | `cms.membership.access_groups.write` or `crm.lists.write` | 200        | List must be MANUAL or SNAPSHOT processing type. Requires JSON body with record IDs.                |
| PUT    | `/crm/v3/lists/{listId}/memberships/add`           | Add records to a list.                                                                                 | `cms.membership.access_groups.write` or `crm.lists.write` | 200        | List must be MANUAL or SNAPSHOT processing type. Requires JSON body with record IDs.                |
| PUT    | `/crm/v3/lists/{listId}/memberships/remove`        | Remove records from a list.                                                                            | `cms.membership.access_groups.write` or `crm.lists.write` | 200        | List must be MANUAL or SNAPSHOT processing type. Requires JSON body with record IDs.                |
| DELETE | `/crm/v3/lists/{listId}/memberships`              | Remove all records from a list (list itself is not deleted).                                       | `cms.membership.access_groups.write` or `crm.lists.write` | 204        | List must be MANUAL or SNAPSHOT processing type.                                                   |


### List Folders

| Method | Endpoint                                    | Description                                                                  | Scopes                                          | HTTP Status | Notes                                                                      |
|--------|---------------------------------------------|------------------------------------------------------------------------------|---------------------------------------------------|-------------|------------------------------------------------------------------------------|
| GET    | `/crm/v3/lists/folders`                     | Retrieves a folder and its child folders.                                   | `crm.lists.read`                                   | 200        |  Use `folderId` query parameter to specify a starting folder.                 |
| POST   | `/crm/v3/lists/folders`                     | Creates a folder.                                                            | `cms.membership.access_groups.write` or `crm.lists.write` | 200        | Requires JSON body with parent folder ID and name.                             |
| PUT    | `/crm/v3/lists/folders/{folderId}/move/{newParentFolderId}` | Moves a folder to a new parent folder.                                      | `cms.membership.access_groups.write` or `crm.lists.write` | 200        |                                                                              |
| PUT    | `/crm/v3/lists/folders/move-list`            | Moves a list to a given folder.                                           | `cms.membership.access_groups.write` or `crm.lists.write` | 204        | Requires JSON body with list ID and new folder ID.                            |
| PUT    | `/crm/v3/lists/folders/{folderId}/rename`    | Renames a folder.                                                            | `cms.membership.access_groups.write` or `crm.lists.write` | 200        |                                                                              |
| DELETE | `/crm/v3/lists/folders/{folderId}`           | Deletes a folder.                                                             | `cms.membership.access_groups.write` or `crm.lists.write` | 204        |                                                                              |


### Legacy List ID Mapping (Expires May 30, 2025)

| Method | Endpoint                | Description                                                                        | Scopes                                   | HTTP Status |
|--------|-------------------------|------------------------------------------------------------------------------------|-------------------------------------------|-------------|
| GET    | `/crm/v3/lists/idmapping` | Translate a legacy list ID to a modern list ID.                               | `crm.lists.read`                           | 200        |
| POST   | `/crm/v3/lists/idmapping` | Translate multiple legacy list IDs to modern list IDs (max 10,000).            | `crm.lists.read`                           | 200        |


### Example: Create List Request

```json
{
  "objectTypeId": "contacts",
  "processingType": "DYNAMIC",
  "customProperties": {},
  "listFolderId": 0,
  "name": "My New List",
  "filterBranch": {
    "filterBranchType": "OR",
    "filterGroups": [
      {
        "filters": [
          {
            "propertyName": "email",
            "operator": "EQ",
            "value": "test@example.com"
          }
        ]
      }
    ]
  }
}
```

This is a simplified example; the `filterBranch` can be more complex depending on your filtering needs.  Consult the HubSpot API documentation for details on filter structures.  Remember to replace `"contacts"` with the appropriate `objectTypeId`.


**Note:**  Error handling and detailed response schemas are omitted for brevity but are crucial for robust integration.  Refer to the official HubSpot API documentation for complete details, including error codes and response structures for each endpoint.
