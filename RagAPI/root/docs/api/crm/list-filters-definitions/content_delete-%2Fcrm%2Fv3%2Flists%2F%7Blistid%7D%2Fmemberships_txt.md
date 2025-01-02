# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, allowing management of list memberships for object lists.  It requires either Marketing Hub Starter or Content Hub Starter.

## Use Cases

* Bulk adding contacts to a list.
* Removing company records from a company list.


## API Endpoints

All endpoints are under the base URL: `https://api.hubapi.com/crm/v3/lists/` and require authentication via `Bearer YOUR_ACCESS_TOKEN` in the Authorization header.  Standard API rate limits apply to all endpoints.


### Lists Management

| Method | Endpoint                  | Description                                                                   | Scopes                                      | Response Code |
|--------|---------------------------|-------------------------------------------------------------------------------|-----------------------------------------------|-----------------|
| GET    | `/crm/v3/lists/{listId}`     | Fetch a single list by ILS list ID.                                          | `crm.lists.read`                             | 200             |
| GET    | `/crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}` | Fetch a single list by list name and object type.                             | `crm.lists.read`                             | 200             |
| GET    | `/crm/v3/lists/`           | Fetch multiple lists by ILS list IDs.                                        | `crm.lists.read`                             | 200             |
| POST   | `/crm/v3/lists/`           | Create a new list.                                                             | `cms.membership.access_groups.write` or `crm.lists.write` | 200             |
| POST   | `/crm/v3/lists/search`     | Search lists by name or page through all lists (empty query).              | `crm.lists.read`                             | 200             |
| PUT    | `/crm/v3/lists/{listId}/restore` | Restore a previously deleted list.                                          | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 204             |
| PUT    | `/crm/v3/lists/{listId}/update-list-filters` | Update a DYNAMIC list's filter branch definition.                          | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200             |
| PUT    | `/crm/v3/lists/{listId}/update-list-name` | Update the name of a list.                                                  | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200             |
| DELETE | `/crm/v3/lists/{listId}`     | Delete a list (restorable for 90 days).                                     | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 204             |


### List Memberships Management

| Method | Endpoint                                         | Description                                                                                                   | Scopes                                      | Response Code |
|--------|-------------------------------------------------|---------------------------------------------------------------------------------------------------------------|-----------------------------------------------|-----------------|
| GET    | `/crm/v3/lists/{listId}/memberships/join-order` | Fetch list memberships ordered by added-to-list date.                                                        | `crm.lists.read`                             | 200             |
| GET    | `/crm/v3/lists/{listId}/memberships`             | Fetch list memberships ordered by record ID.                                                                 | `crm.lists.read`                             | 200             |
| GET    | `/crm/v3/lists/records/{objectTypeId}/{recordId}/memberships` | Get lists a record is a member of.                                                                        | `crm.lists.read`                             | 200             |
| PUT    | `/crm/v3/lists/{listId}/memberships/add-from/{sourceListId}` | Add all records from a source list to a destination list.                                                    | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 204             |
| PUT    | `/crm/v3/lists/{listId}/memberships/add-and-remove` | Add and/or remove records from a list.                                                                      | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200             |
| PUT    | `/crm/v3/lists/{listId}/memberships/add`         | Add records to a list.                                                                                      | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200             |
| PUT    | `/crm/v3/lists/{listId}/memberships/remove`      | Remove records from a list.                                                                                   | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200             |
| DELETE | `/crm/v3/lists/{listId}/memberships`             | Remove all records from a list (list itself remains).                                                        | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 204             |


### List Folders Management

| Method | Endpoint                                  | Description                                                             | Scopes                                      | Response Code |
|--------|-------------------------------------------|-------------------------------------------------------------------------|-----------------------------------------------|-----------------|
| GET    | `/crm/v3/lists/folders`                   | Retrieves a folder and its children.                                   | `crm.lists.read`                             | 200             |
| POST   | `/crm/v3/lists/folders`                   | Creates a new folder.                                                   | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200             |
| PUT    | `/crm/v3/lists/folders/{folderId}/move/{newParentFolderId}` | Moves a folder to a new parent folder.                               | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200             |
| PUT    | `/crm/v3/lists/folders/move-list`          | Moves a list to a given folder.                                        | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 204             |
| PUT    | `/crm/v3/lists/folders/{folderId}/rename`   | Renames a folder.                                                       | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200             |
| DELETE | `/crm/v3/lists/folders/{folderId}`         | Deletes a folder.                                                       | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 204             |


### Legacy List ID Mapping (Expires May 30, 2025)

| Method | Endpoint                  | Description                                                                 | Scopes             | Response Code |
|--------|---------------------------|-----------------------------------------------------------------------------|---------------------|-----------------|
| GET    | `/crm/v3/lists/idmapping` | Translate a legacy list ID to a modern list ID.                           | `crm.lists.read`     | 200             |
| POST   | `/crm/v3/lists/idmapping` | Translate multiple legacy list IDs to modern list IDs (max 10,000).       | `crm.lists.read`     | 200             |


## Example (Fetch List by ID using Python)

```python
import requests

access_token = "YOUR_ACCESS_TOKEN"
list_id = "YOUR_LIST_ID"
url = f"https://api.hubapi.com/crm/v3/lists/{list_id}?includeFilters=false"
headers = {
    "Authorization": f"Bearer {access_token}"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code} - {response.text}")
```

Remember to replace `"YOUR_ACCESS_TOKEN"` and `"YOUR_LIST_ID"` with your actual access token and list ID.  Error handling is crucial in production code.  Similar requests can be made for other endpoints using the appropriate HTTP method and parameters.  Refer to the HubSpot API documentation for detailed schema information for each endpoint's request and response.
