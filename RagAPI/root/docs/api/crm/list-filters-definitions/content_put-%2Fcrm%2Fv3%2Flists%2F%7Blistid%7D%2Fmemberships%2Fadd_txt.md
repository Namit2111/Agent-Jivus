# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, allowing management of list memberships for object lists.  Requires either Marketing Hub Starter or Content Hub Starter or higher.

## API Overview

The Lists API v3 provides endpoints for various list operations, including fetching, creating, updating, deleting lists, and managing memberships.  It also includes functionality for working with list folders and mapping legacy list IDs to modern IDs.  Authentication is handled via Private Apps or OAuth, requiring specific scopes depending on the operation.

## Authentication

All API calls require authentication.  Use either:

* **Private Apps:** Generate an API key within your HubSpot account.
* **OAuth:**  Follow HubSpot's OAuth 2.0 flow to obtain an access token.

The `Bearer` token is passed in the `Authorization` header as `Authorization: Bearer YOUR_ACCESS_TOKEN`.


## API Endpoints

All endpoints are located under the base URL: `https://api.hubapi.com/crm/v3/lists/`

Unless otherwise specified, all endpoints adhere to standard HubSpot API rate limits.


### Lists Management

| Method | Endpoint                      | Description                                                                        | Scopes                                         | Response Code |
|--------|-------------------------------|------------------------------------------------------------------------------------|-------------------------------------------------|----------------|
| GET    | `/crm/v3/lists/{listId}`        | Fetch a single list by ILS list ID.                                              | `crm.lists.read`                               | 200            |
| GET    | `/crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}` | Fetch a single list by list name and object type.                               | `crm.lists.read`                               | 200            |
| GET    | `/crm/v3/lists/`               | Fetch multiple lists by ILS list IDs.                                             | `crm.lists.read`                               | 200            |
| POST   | `/crm/v3/lists/`               | Create a new list.                                                                 | `cms.membership.access_groups.write` or `crm.lists.write` | 200            |
| POST   | `/crm/v3/lists/search`         | Search lists by name or page through all lists.                                   | `crm.lists.read`                               | 200            |
| PUT    | `/crm/v3/lists/{listId}/restore` | Restore a previously deleted list.                                                | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 204            |
| PUT    | `/crm/v3/lists/{listId}/update-list-filters` | Update a dynamic list's filter definition.                                      | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200            |
| PUT    | `/crm/v3/lists/{listId}/update-list-name` | Update the name of a list.                                                        | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200            |
| DELETE | `/crm/v3/lists/{listId}`        | Delete a list.                                                                   | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 204            |


### List Memberships

| Method | Endpoint                                         | Description                                                                                                | Scopes                                         | Response Code |
|--------|-------------------------------------------------|------------------------------------------------------------------------------------------------------------|-------------------------------------------------|----------------|
| GET    | `/crm/v3/lists/{listId}/memberships/join-order` | Fetch list memberships ordered by added-to-list date.                                                    | `crm.lists.read`                               | 200            |
| GET    | `/crm/v3/lists/{listId}/memberships`             | Fetch list memberships ordered by record ID.                                                              | `crm.lists.read`                               | 200            |
| GET    | `/crm/v3/lists/records/{objectTypeId}/{recordId}/memberships` | Get lists a record is a member of.                                                                     | `crm.lists.read`                               | 200            |
| PUT    | `/crm/v3/lists/{listId}/memberships/add-from/{sourceListId}` | Add all records from a source list to a destination list.                                                | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 204            |
| PUT    | `/crm/v3/lists/{listId}/memberships/add-and-remove` | Add and/or remove records from a list.                                                                   | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200            |
| PUT    | `/crm/v3/lists/{listId}/memberships/add`         | Add records to a list.                                                                                   | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200            |
| PUT    | `/crm/v3/lists/{listId}/memberships/remove`      | Remove records from a list.                                                                                | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200            |
| DELETE | `/crm/v3/lists/{listId}/memberships`             | Remove all records from a list (list itself remains).                                                     | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 204            |


### List Folders

| Method | Endpoint                               | Description                                                              | Scopes                                         | Response Code |
|--------|---------------------------------------|--------------------------------------------------------------------------|-------------------------------------------------|----------------|
| GET    | `/crm/v3/lists/folders`                | Retrieves a folder and its child folders.                               | `crm.lists.read`                               | 200            |
| POST   | `/crm/v3/lists/folders`                | Creates a new folder.                                                    | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200            |
| PUT    | `/crm/v3/lists/folders/{folderId}/move/{newParentFolderId}` | Moves a folder to a new parent folder.                                    | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200            |
| PUT    | `/crm/v3/lists/folders/move-list`      | Moves a list to a given folder.                                         | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 204            |
| PUT    | `/crm/v3/lists/folders/{folderId}/rename` | Renames a folder.                                                        | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200            |
| DELETE | `/crm/v3/lists/folders/{folderId}`      | Deletes a folder.                                                        | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 204            |


### Legacy List ID Mapping (Expires May 30, 2025)

| Method | Endpoint                  | Description                                                                  | Scopes                | Response Code |
|--------|---------------------------|------------------------------------------------------------------------------|------------------------|----------------|
| GET    | `/crm/v3/lists/idmapping` | Translate a legacy list ID to a modern list ID.                           | `crm.lists.read`       | 200            |
| POST   | `/crm/v3/lists/idmapping` | Translate a batch of legacy list IDs to modern list IDs (max 10,000).       | `crm.lists.read`       | 200            |


## Examples

**Fetch List by ID (cURL):**

```bash
curl --request GET \
--url 'https://api.hubapi.com/crm/v3/lists/123?includeFilters=false' \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

**Create a List (cURL):**

```bash
curl --request POST \
--url https://api.hubapi.com/crm/v3/lists/ \
--header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
--header 'content-type: application/json' \
--data '{
"objectTypeId": "contacts",
"processingType": "MANUAL",
"name": "My New List",
"listFolderId": 0
}'
```

**(Note:  Replace placeholders like `listId`, `objectTypeId`, `listName`, `YOUR_ACCESS_TOKEN`,  etc. with actual values.)**  Refer to the HubSpot API documentation for detailed schema information for request and response bodies.  Remember to handle potential error responses appropriately in your code.
