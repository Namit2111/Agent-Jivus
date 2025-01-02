# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, allowing for creation, management, and retrieval of lists within HubSpot.  The legacy v1 API is sunsetting on May 30th, 2025.  This document guides migration from v1 to v3.

## Overview

HubSpot lists organize records (contacts, companies, deals, etc.) for segmentation and filtering.  A list comprises a definition (essential information) and memberships (record mappings).  Three processing types exist:

* **MANUAL:** Records are added/removed manually via API or UI. No background processing.
* **DYNAMIC:**  List filters automatically add/remove records based on criteria. HubSpot manages memberships dynamically.
* **SNAPSHOT:** Filters are applied at creation; subsequent changes are manual only.

## API Endpoints

All endpoints below use the base URL `/crm/v3/lists/`.  Replace `{listId}` with the ILS list ID, `{objectTypeId}` with the object type ID (e.g., `0-1` for contacts), and `{listName}` with the list name.

### List Management

| Method | Endpoint                     | Description                                                                        | Request Body (Example)                                                     | Response (Example)                                                              |
|--------|------------------------------|------------------------------------------------------------------------------------|-----------------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| POST    | `/`                          | Create a list. Requires `name`, `objectTypeId`, `processingType`. `filterBranch` is optional. | `{"name": "My static list", "objectTypeId": "0-1", "processingType": "MANUAL"}` | `{ "listId": 123, ... }` (Includes newly created list ID)                      |
| GET     | `/object-type-id/{objectTypeId}/name/{listName}` | Retrieve a list by name and object type.                                       | None                                                                         | `{ "listId": 123, ... }`                                                        |
| GET     | `/{listId}`                  | Retrieve a list by ILS list ID.                                                 | None                                                                         | `{ "listId": 123, ... }`                                                        |
| GET     | `/` (with `listIds` query parameter) | Retrieve multiple lists by ILS list IDs (e.g., `?listIds=123&listIds=456`).     | None                                                                         | `[{ "listId": 123, ... }, { "listId": 456, ... }]`                              |
| POST    | `/search`                    | Search for lists by criteria (e.g., name, processing type).                     | `{"query": "HubSpot", "processingTypes": ["MANUAL"]}`                       | `[{ "listId": 123, ... }, ...]` (Array of matching lists)                     |
| PUT     | `/{listId}/update-list-name` | Update a list's name (requires `listName` query parameter).                   | None                                                                         | `{ "listId": 123, ... }`                                                        |
| PUT     | `/{listId}/update-list-filters` | Update a DYNAMIC list's filter branches.                                      | `{ "filterBranch": { ... } }`                                               | `{ "listId": 123, ... }`                                                        |
| DELETE  | `/{listId}`                  | Delete a list.                                                                   | None                                                                         | Success/Error response                                                        |
| PUT     | `/{listId}/restore`          | Restore a deleted list (within 90 days).                                        | None                                                                         | Success/Error response                                                        |


### List Membership Management (MANUAL & SNAPSHOT lists only)

| Method | Endpoint                        | Description                                                                    | Request Body (Example)             | Response (Example)                        |
|--------|---------------------------------|-------------------------------------------------------------------------------|--------------------------------------|---------------------------------------------|
| PUT     | `/{listId}/memberships/add`     | Add records to a list. Requires an array of `recordId`s.                    | `["recordId1", "recordId2"]`         | Success/Error response                      |
| PUT     | `/{listId}/memberships/add-from/{sourceListId}` | Add records from one list to another.                                      | None                                  | Success/Error response                      |
| GET     | `/{listId}/memberships`        | Retrieve all records in a list.                                              | None                                  | `[{ "recordId": "recordId1", ... }, ...]` |
| DELETE  | `/{listId}/memberships`        | Remove all records from a list (doesn't delete the list itself).            | None                                  | Success/Error response                      |
| PUT     | `/{listId}/memberships/remove`  | Remove specific records from a list. Requires an array of `recordId`s.       | `["recordId1", "recordId2"]`         | Success/Error response                      |


### Migration from v1 to v3

* **ID Mapping:**  Use `/crm/v3/lists/idmapping` (GET for single ID, POST for batch) to get v3 `listId` from v1 `legacyListId`.  Note: This endpoint will sunset May 30th, 2025.

* **Get Static Lists:** Use `/crm/v3/lists/search` with `processingTypes: ["MANUAL", "SNAPSHOT"]`.

* **Get Dynamic Lists:** Use `/crm/v3/lists/search` with `processingTypes: ["DYNAMIC"]`.

* **Get a batch of lists by list ID:** Use `/crm/v3/lists/search` with the `listIds` parameter. For a response that includes filters, use the `/crm/v3/lists` endpoint with the `includeListFilters=true` query parameter and the `listIds` parameter.

* **Get Recent List Members with Properties:** First, get record IDs via `/crm/v3/lists/{listId}/memberships/join-order`, then use `/crm/v3/objects/{object}/search` to fetch properties.

* **Get all/recently modified records with properties:** Use `/crm/v3/objects/{object}/search` with appropriate filters for `lastmodifieddate`.


## Examples (Expanded)

Many examples are provided throughout the document above.  These examples showcase request bodies and potential response structures.  Remember to replace placeholders like `{listId}`, `{objectTypeId}`, and specific record IDs with your actual values.  Always refer to the HubSpot API documentation for the most up-to-date details on parameters and response fields.  Error handling and authentication (using API keys) are essential aspects not explicitly detailed here but crucial for successful API interaction.
