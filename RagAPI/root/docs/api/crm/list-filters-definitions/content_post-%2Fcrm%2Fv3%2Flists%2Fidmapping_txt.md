# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, allowing management of list memberships for object lists.  It requires either Marketing Hub Starter or Content Hub Starter.

## API Endpoints

All endpoints use `/crm/v3/lists/` as a base path and require authentication via `Bearer YOUR_ACCESS_TOKEN` in the `Authorization` header.  Standard API rate limits apply to all endpoints.


**I. Lists Management**

* **Fetch List by ID (GET):**

    * **Endpoint:** `/crm/v3/lists/{listId}`
    * **Description:** Retrieves a single list by its ILS list ID.
    * **Parameters:**
        * `listId`: (string, required) The ID of the list.
        * `includeFilters`: (boolean, optional) Include filter definitions. Defaults to `false`.
    * **Scopes:** `crm.lists.read`
    * **Example cURL Request:**
        ```bash
        curl --request GET \
             --url 'https://api.hubapi.com/crm/v3/lists/listId?includeFilters=false' \
             --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
        ```
    * **Example Response (HTTP 200):**  *(Schema omitted for brevity, refer to HubSpot documentation for details)*
        ```json
        {
          "id": 123,
          "name": "My List",
          // ... other properties
        }
        ```

* **Fetch List by Name (GET):**

    * **Endpoint:** `/crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}`
    * **Description:** Retrieves a single list by its name and object type.
    * **Parameters:**
        * `objectTypeId`: (string, required) The object type ID (e.g., "contacts").
        * `listName`: (string, required) The name of the list.
        * `includeFilters`: (boolean, optional) Include filter definitions. Defaults to `false`.
    * **Scopes:** `crm.lists.read`
    * **Example cURL Request:** (Replace placeholders)
        ```bash
        curl --request GET \
             --url 'https://api.hubapi.com/crm/v3/lists/object-type-id/contacts/name/MyList?includeFilters=false' \
             --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
        ```

* **Fetch Multiple Lists (GET):**

    * **Endpoint:** `/crm/v3/lists/`
    * **Description:** Retrieves multiple lists by their IDs.
    * **Parameters:**
        * `listId`: (string, optional) Comma-separated list of list IDs.
        * `includeFilters`: (boolean, optional) Include filter definitions. Defaults to `false`.
    * **Scopes:** `crm.lists.read`
    * **Example cURL Request:**
        ```bash
        curl --request GET \
             --url 'https://api.hubapi.com/crm/v3/lists/?includeFilters=false' \
             --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
        ```

* **Create List (POST):**

    * **Endpoint:** `/crm/v3/lists/`
    * **Description:** Creates a new list.
    * **Request Body (JSON):**
        ```json
        {
          "objectTypeId": "string",
          "processingType": "string", //MANUAL, SNAPSHOT, DYNAMIC
          "customProperties": {},
          "listFolderId": 0,
          "name": "string",
          "filterBranch": {} // For DYNAMIC lists only
        }
        ```
    * **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`
    * **Example cURL Request:** (Replace placeholders)
        ```bash
        curl --request POST \
             --url https://api.hubapi.com/crm/v3/lists/ \
             --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
             --header 'content-type: application/json' \
             --data '{ "objectTypeId": "contacts", "processingType": "MANUAL", "name": "New List" }'
        ```

* **Search Lists (POST):**

    * **Endpoint:** `/crm/v3/lists/search`
    * **Description:** Searches lists by name or pages through all lists.
    * **Request Body (JSON):**
        ```json
        {
          "listIds": [],
          "offset": 0,
          "query": "string",
          "count": 0,
          "processingTypes": [],
          "additionalProperties": [],
          "sort": "string"
        }
        ```
    * **Scopes:** `crm.lists.read`
    * **Example cURL Request:**
        ```bash
        curl --request POST \
             --url https://api.hubapi.com/crm/v3/lists/search \
             --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
             --header 'content-type: application/json' \
             --data '{ "query": "My List" }'
        ```

* **Restore a List (PUT):**

    * **Endpoint:** `/crm/v3/lists/{listId}/restore`
    * **Description:** Restores a deleted list (up to 90 days after deletion).
    * **Parameters:**
        * `listId`: (string, required) The ID of the deleted list.
    * **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
    * **Example cURL Request:**
        ```bash
        curl --request PUT \
             --url https://api.hubapi.com/crm/v3/lists/listId/restore \
             --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
        ```

* **Update List Filter Definition (PUT):**

    * **Endpoint:** `/crm/v3/lists/{listId}/update-list-filters`
    * **Description:** Updates the filter definition of a DYNAMIC list.
    * **Parameters:**
        * `listId`: (string, required) The ID of the list.
        * `enrollObjectsInWorkflows`: (boolean, optional)  Enroll objects in workflows. Defaults to `false`.
    * **Request Body (JSON):**  `(filterBranch)`  Similar structure as in Create List.
    * **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
    * **Example cURL Request:** (Replace placeholders)
        ```bash
        curl --request PUT \
             --url 'https://api.hubapi.com/crm/v3/lists/listId/update-list-filters?enrollObjectsInWorkflows=false' \
             --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
             --header 'content-type: application/json' \
             --data '{ "filterBranch": { "filterBranchType": "OR", "filterBranchOperator": "string" } }'
        ```

* **Update List Name (PUT):**

    * **Endpoint:** `/crm/v3/lists/{listId}/update-list-name`
    * **Description:** Updates the name of a list.
    * **Parameters:**
        * `listId`: (string, required) The ID of the list.
        * `includeFilters`: (boolean, optional) Include filter definitions. Defaults to `false`.
    * **Request Body (JSON):** `"name": "New List Name"`
    * **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
    * **Example cURL Request:** (Replace placeholders)
        ```bash
        curl --request PUT \
             --url 'https://api.hubapi.com/crm/v3/lists/listId/update-list-name?includeFilters=false' \
             --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
             --header 'content-type: application/json' \
             --data '{ "name": "New List Name" }'
        ```

* **Delete a List (DELETE):**

    * **Endpoint:** `/crm/v3/lists/{listId}`
    * **Description:** Deletes a list.  Can be restored within 90 days.
    * **Parameters:**
        * `listId`: (string, required) The ID of the list.
    * **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
    * **Example cURL Request:**
        ```bash
        curl --request DELETE \
             --url https://api.hubapi.com/crm/v3/lists/listId \
             --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
        ```


**(II. List Memberships Management - continues in the next section due to length limitations.)**
