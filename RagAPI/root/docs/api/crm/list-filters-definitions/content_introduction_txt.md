# HubSpot Lists API v3 Documentation

This document details the HubSpot Lists API v3, allowing management of list memberships for object lists.  The API requires either Marketing Hub Starter or Content Hub Starter or higher.

## Use Cases

* Bulk adding contacts to a list.
* Removing company records from a company list.

## Authentication

All API calls require authentication using either Private Apps or OAuth.  You will need to replace `YOUR_ACCESS_TOKEN` with your actual access token in the examples below.


## API Endpoints

The following sections detail each API endpoint, including HTTP method, URL, required scopes, parameters, request examples (using cURL), and expected responses.  Note that response examples and schemas are omitted for brevity, as they are readily available on the HubSpot developer portal.


### Lists

**1. Fetch List by ID (GET)**

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** `GET`
* **Scopes:** `crm.lists.read`
* **Parameters:** `includeFilters=false` (optional, defaults to `false`)
* **Request (cURL):**
  ```bash
  curl --request GET \
  --url 'https://api.hubapi.com/crm/v3/lists/listId?includeFilters=false' \
  --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
  ```
* **Response:** HTTP 200 (Success)


**2. Fetch List by Name (GET)**

* **Endpoint:** `/crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}`
* **Method:** `GET`
* **Scopes:** `crm.lists.read`
* **Parameters:** `includeFilters=false` (optional, defaults to `false`)
* **Request (cURL):**
  ```bash
  curl --request GET \
  --url 'https://api.hubapi.com/crm/v3/lists/object-type-id/objectTypeId/name/listName?includeFilters=false' \
  --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
  ```
* **Response:** HTTP 200 (Success)


**3. Fetch Multiple Lists (GET)**

* **Endpoint:** `/crm/v3/lists/`
* **Method:** `GET`
* **Scopes:** `crm.lists.read`
* **Parameters:** `includeFilters=false` (optional, defaults to `false`),  `listId` (comma separated list of IDs)
* **Request (cURL):**
  ```bash
  curl --request GET \
  --url 'https://api.hubapi.com/crm/v3/lists/?includeFilters=false&listId=123,456' \
  --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
  ```
* **Response:** HTTP 200 (Success)


**4. Create List (POST)**

* **Endpoint:** `/crm/v3/lists/`
* **Method:** `POST`
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write`
* **Request Body (JSON):**
  ```json
  {
    "objectTypeId": "string",
    "processingType": "string",
    "customProperties": {
      "additionalProp1": "string",
      "additionalProp2": "string",
      "additionalProp3": "string"
    },
    "listFolderId": 0,
    "name": "string",
    "filterBranch": {
      "filterBranchType": "OR",
      "filterBranchOperator": "string"
    }
  }
  ```
* **Request (cURL):**
  ```bash
  curl --request POST \
  --url https://api.hubapi.com/crm/v3/lists/ \
  --header 'authorization: Bearer YOUR_ACCESS_TOKEN' \
  --header 'content-type: application/json' \
  --data '{...}' // Replace with the JSON above
  ```
* **Response:** HTTP 200 (Success)


**5. Search Lists (POST)**

* **Endpoint:** `/crm/v3/lists/search`
* **Method:** `POST`
* **Scopes:** `crm.lists.read`
* **Request Body (JSON):**  (Example, parameters are optional)
  ```json
  {
    "listIds": ["string"],
    "offset": 0,
    "query": "string",
    "count": 0,
    "processingTypes": ["string"],
    "additionalProperties": ["string"],
    "sort": "string"
  }
  ```
* **Request (cURL):**  (Similar to Create List, using the JSON above)
* **Response:** HTTP 200 (Success)


**6. Restore a List (PUT)**

* **Endpoint:** `/crm/v3/lists/{listId}/restore`
* **Method:** `PUT`
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Request (cURL):**
  ```bash
  curl --request PUT \
  --url https://api.hubapi.com/crm/v3/lists/listId/restore \
  --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
  ```
* **Response:** HTTP 204 (No Content)


**7. Update List Filter Definition (PUT)**

* **Endpoint:** `/crm/v3/lists/{listId}/update-list-filters`
* **Method:** `PUT`
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Request Body (JSON):**
  ```json
  {
    "filterBranch": {
      "filterBranchType": "OR",
      "filterBranchOperator": "string"
    }
  }
  ```
* **Request (cURL):** (Similar to Create List, using the JSON above)
* **Response:** HTTP 200 (Success)


**8. Update List Name (PUT)**

* **Endpoint:** `/crm/v3/lists/{listId}/update-list-name`
* **Method:** `PUT`
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Request (cURL):**  (Similar to Restore a List)
* **Response:** HTTP 200 (Success)



**9. Delete a List (DELETE)**

* **Endpoint:** `/crm/v3/lists/{listId}`
* **Method:** `DELETE`
* **Scopes:** `cms.membership.access_groups.write` or `crm.lists.write` and `crm.lists.read`
* **Request (cURL):** (Similar to Restore a List)
* **Response:** HTTP 204 (No Content)



### Memberships

(Similar detailed explanations as above for each Memberships endpoint would follow here,  including  `Fetch List Memberships Ordered by Added to List Date`, `Fetch List Memberships Ordered by ID`, `Get lists record is member of`, `Add All Records from a Source List to a Destination List`, `Add and/or Remove Records from a List`, `Add Records to a List`, `Remove Records from a List`, and `Delete All Records from a List`.)



### Folders

(Similar detailed explanations as above would follow here for each Folders endpoint, including `Retrieves a folder`, `Creates a folder`, `Moves a folder`, `Moves a list to a given folder`, `Rename a folder`, and `Deletes a folder`.)


### Mapping

(Similar detailed explanations as above would follow here for each Mapping endpoint, including `Translate Legacy List Id to Modern List Id` and `Translate Legacy List Id to Modern List Id in Batch`.)


**Note:**  This documentation provides a concise overview.  For complete details, including detailed schema information and error handling, refer to the official HubSpot API documentation.  The examples provided are using cURL but similar requests can be made using other libraries like Python's `requests` library.
