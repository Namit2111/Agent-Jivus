# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, providing comprehensive information on managing lists within HubSpot.  The legacy v1 API will be sunsetted on May 30th, 2025.  This document focuses on the v3 API and migration from v1.


## List Processing Types

HubSpot Lists support three processing types:

* **MANUAL:** Records are added or removed only through manual user actions or API calls.  No background processing occurs.  Ideal for static lists.
* **DYNAMIC:**  List filters define membership. HubSpot automatically adds or removes records based on filter matches.  Ideal for lists expected to change over time.
* **SNAPSHOT:** Filters are specified at creation; after initial processing, the list is static (only manual updates allowed).  Good for lists based on specific criteria at a point in time.


## API Endpoints

All endpoints below are under the base URL `/crm/v3/lists/`.  Replace `{listId}` and `{objectTypeId}` with the appropriate IDs.  `{object}` in some examples refers to the object type (e.g., `contacts`, `companies`).  `ILS list ID` refers to the HubSpot internal list ID.

**1. Create a List:**

* **Method:** `POST`
* **Endpoint:** `/`
* **Request Body:**
    * `name` (string, required): List name.
    * `objectTypeId` (string, required): ID of the object type (e.g., `0-1` for contacts). See [object type IDs](link_to_object_type_ids_page_if_available)
    * `processingType` (string, required): `MANUAL`, `DYNAMIC`, or `SNAPSHOT`.
    * `filterBranch` (object, optional):  Filter definition for `DYNAMIC` and `SNAPSHOT` lists.  See [configuring list filters and branches](link_to_filter_config_page_if_available)
* **Example Request:**

```json
{
  "name": "My static list",
  "objectTypeId": "0-1",
  "processingType": "MANUAL"
}
```

* **Response:**  Includes the newly created list's `listId`.


**2. Retrieve Lists:**

* **By Name:**
    * **Method:** `GET`
    * **Endpoint:** `/object-type-id/{objectTypeId}/name/{listName}`
* **By `listId` (single):**
    * **Method:** `GET`
    * **Endpoint:** `/{listId}`
* **By `listId` (multiple):**
    * **Method:** `GET`
    * **Endpoint:** `/`
    * **Query Parameters:** `listIds={listId1}&listIds={listId2}&...`  (e.g., `listIds=940&listIds=938`)
    * **Optional Query Parameter:** `includeFilters=true` (includes filter definitions in response)
* **Example Response (single list):**

```json
{
  "listId": 123,
  "name": "My List",
  "objectTypeId": "0-1",
  "processingType": "MANUAL",
  // ... other properties
}
```

**3. Search for a List:**

* **Method:** `POST`
* **Endpoint:** `/search`
* **Request Body:**
    * `query` (string, optional): Search term (within list name).
    * `processingTypes` (array of strings, optional):  Filter by processing type (e.g., `["MANUAL"]`).
* **Example Request:**

```json
{
  "query": "HubSpot",
  "processingTypes": ["MANUAL"]
}
```

* **Response:**  Array of matching lists.


**4. Update a List Name:**

* **Method:** `PUT`
* **Endpoint:** `/{listId}/update-list-name`
* **Query Parameters:** `listName={newListName}`
* **Optional Query Parameter:** `includeFilters=true`

**5. Update a List Filter Branch (DYNAMIC lists only):**

* **Method:** `PUT`
* **Endpoint:** `/{listId}/update-list-filters`
* **Request Body:** New filter branch definition.


**6. Delete and Restore a List:**

* **Delete:**
    * **Method:** `DELETE`
    * **Endpoint:** `/{listId}`
* **Restore:**
    * **Method:** `PUT`
    * **Endpoint:** `/{listId}/restore`  (Only within 90 days of deletion)


**7. Manage List Memberships (MANUAL & SNAPSHOT lists only):**

* **Add Records:**
    * **Method:** `PUT`
    * **Endpoint:** `/{listId}/memberships/add`
    * **Request Body:** Array of `recordId`s.
* **Add Records from Another List:**
    * **Method:** `PUT`
    * **Endpoint:** `/{listId}/memberships/add-from/{sourceListId}`
* **View Records:**
    * **Method:** `GET`
    * **Endpoint:** `/{listId}/memberships`
* **Remove Records:**
    * **Method:** `PUT`
    * **Endpoint:** `/{listId}/memberships/remove`
    * **Request Body:** Array of `recordId`s.
* **Remove All Records:**
    * **Method:** `DELETE`
    * **Endpoint:** `/{listId}/memberships`


**8. Migration from v1 to v3:**

* **Get `listId` from `legacyListId` (single):**
    * **Method:** `GET`
    * **Endpoint:** `/idmapping`
    * **Query Parameter:** `legacyListId={legacyListId}`
* **Get `listId` from `legacyListId` (multiple):**
    * **Method:** `POST`
    * **Endpoint:** `/idmapping`
    * **Request Body:** Array of `legacyListId`s (limit 10,000).


**9. Get Static Lists:**

* **Method:** `POST`
* **Endpoint:** `/search`
* **Request Body:**  Similar to list search, but specifying `processingTypes`: `["MANUAL", "SNAPSHOT"]`.


**10. Get Dynamic Lists:**

* **Method:** `POST`
* **Endpoint:** `/search`
* **Request Body:** Similar to list search, but specifying `processingTypes`: `["DYNAMIC"]`.


**11. Get a Batch of Lists by `listId`:**

* **Method:** `POST`
* **Endpoint:** `/search`
* **Request Body:** Include `listIds` array.  Use GET `/crm/v3/lists` with `includeFilters=true` and `listIds` for filter information.


**12. Get Recent List Members with Properties:**

1. Get record IDs via `GET /crm/v3/lists/{listId}/memberships/join-order`.
2. Use `POST /crm/v3/objects/{object}/search` with obtained `recordId`s in the `values` parameter of a filter.


**13. Get All/Recently Modified Records with Properties:**

* Use `POST /crm/v3/objects/{object}/search`. Filter by `lastmodifieddate` for recently modified records.


## Error Handling

The API returns standard HTTP status codes to indicate success or failure.  Detailed error messages will be included in the response body.


This documentation provides a comprehensive overview. Refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications. Remember to replace placeholder values with your actual data.
