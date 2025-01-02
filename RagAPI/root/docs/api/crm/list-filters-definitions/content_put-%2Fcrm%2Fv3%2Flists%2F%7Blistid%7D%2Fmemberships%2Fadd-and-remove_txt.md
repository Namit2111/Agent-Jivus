# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, allowing management of list memberships for object lists.  It requires either Marketing Hub Starter or Content Hub Starter or higher.

## API Overview

The API uses standard RESTful principles.  Authentication is via Private Apps or OAuth, requiring the appropriate scopes (detailed in each endpoint).  All endpoints are prefixed with `https://api.hubapi.com/crm/v3/lists/`.  Standard API rate limits apply.


## Endpoints

### Lists

| Method | Endpoint                     | Description                                                                       | Scopes                                    | Response Code |
|--------|------------------------------|-----------------------------------------------------------------------------------|---------------------------------------------|----------------|
| GET    | `/lists/{listId}`             | Fetch a single list by ILS list ID.                                               | `crm.lists.read`                            | 200            |
| GET    | `/lists/object-type-id/{objectTypeId}/name/{listName}` | Fetch a single list by list name and object type.                               | `crm.lists.read`                            | 200            |
| GET    | `/lists/`                     | Fetch multiple lists by ILS list IDs.                                              | `crm.lists.read`                            | 200            |
| POST   | `/lists/`                     | Create a new list.                                                                 | `cms.membership.access_groups.write` or `crm.lists.write` | 200            |
| POST   | `/lists/search`               | Search lists by name or page through all lists (empty query).                     | `crm.lists.read`                            | 200            |
| PUT    | `/lists/{listId}/restore`     | Restore a previously deleted list (up to 90 days after deletion).                 | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 204            |
| PUT    | `/lists/{listId}/update-list-filters` | Update the filter branch definition of a DYNAMIC list.                           | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200            |
| PUT    | `/lists/{listId}/update-list-name` | Update the name of a list.                                                        | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200            |
| DELETE | `/lists/{listId}`             | Delete a list (restorable for 90 days).                                          | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 204            |


#### Example: Fetching a List by ID (Python)

```python
import requests

access_token = "YOUR_ACCESS_TOKEN"
list_id = "your_list_id"
url = f"https://api.hubapi.com/crm/v3/lists/{list_id}?includeFilters=false"
headers = {"Authorization": f"Bearer {access_token}"}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code} - {response.text}")
```


### Memberships

| Method | Endpoint                                         | Description                                                                                             | Scopes                                    | Response Code |
|--------|-------------------------------------------------|---------------------------------------------------------------------------------------------------------|---------------------------------------------|----------------|
| GET    | `/lists/{listId}/memberships/join-order`         | Fetch list memberships ordered by added-to-list date.                                                | `crm.lists.read`                            | 200            |
| GET    | `/lists/{listId}/memberships`                    | Fetch list memberships ordered by record ID.                                                            | `crm.lists.read`                            | 200            |
| GET    | `/lists/records/{objectTypeId}/{recordId}/memberships` | Get lists a record is a member of.                                                                 | `crm.lists.read`                            | 200            |
| PUT    | `/lists/{listId}/memberships/add-from/{sourceListId}` | Add all records from a source list to a destination list (MANUAL or SNAPSHOT processingType).       | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 204            |
| PUT    | `/lists/{listId}/memberships/add-and-remove`      | Add and/or remove records from a list (MANUAL or SNAPSHOT processingType).                           | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200            |
| PUT    | `/lists/{listId}/memberships/add`                | Add records to a list (MANUAL or SNAPSHOT processingType).                                          | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200            |
| PUT    | `/lists/{listId}/memberships/remove`              | Remove records from a list (MANUAL or SNAPSHOT processingType).                                       | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200            |
| DELETE | `/lists/{listId}/memberships`                    | Remove all records from a list (MANUAL or SNAPSHOT processingType; <100,000 memberships).           | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 204            |


### Folders

| Method | Endpoint                               | Description                                                                   | Scopes                                    | Response Code |
|--------|---------------------------------------|-------------------------------------------------------------------------------|---------------------------------------------|----------------|
| GET    | `/lists/folders`                       | Retrieves a folder and its children.                                          | `crm.lists.read`                            | 200            |
| POST   | `/lists/folders`                       | Creates a new folder.                                                         | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200            |
| PUT    | `/lists/folders/{folderId}/move/{newParentFolderId}` | Moves a folder to a new parent folder.                                        | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200            |
| PUT    | `/lists/folders/move-list`             | Moves a list to a given folder.                                               | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 204            |
| PUT    | `/lists/folders/{folderId}/rename`     | Renames a folder.                                                              | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 200            |
| DELETE | `/lists/folders/{folderId}`           | Deletes a folder.                                                              | `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read` | 204            |


### Mapping (Legacy IDs - Expiring May 30, 2025)

| Method | Endpoint                  | Description                                                                  | Scopes             | Response Code |
|--------|---------------------------|------------------------------------------------------------------------------|---------------------|----------------|
| GET    | `/lists/idmapping`        | Translate a legacy list ID to a modern list ID.                              | `crm.lists.read`    | 200            |
| POST   | `/lists/idmapping`        | Translate a batch of legacy list IDs to modern list IDs (max 10,000 IDs).    | `crm.lists.read`    | 200            |


**Note:**  Replace placeholders like `{listId}`, `{objectTypeId}`, `{listName}`, `{sourceListId}`, `{folderId}`, and  `{newParentFolderId}` with actual values.  Remember to replace `"YOUR_ACCESS_TOKEN"` with your actual HubSpot access token.  Error handling and more robust code structure should be added for production use.  The examples provided are simplified for clarity.
