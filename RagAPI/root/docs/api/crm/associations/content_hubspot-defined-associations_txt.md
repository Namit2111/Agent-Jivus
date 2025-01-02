# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 for managing record associations.  Associations represent relationships between different CRM objects (e.g., Contact to Company) or within the same object (e.g., Company to Company).  This API includes endpoints for managing associations and their schemas (definitions and labels).  Note that this API requires HubSpot Client NodeJS version 9.0.0 or later.

## I. Association Endpoints

These endpoints create, edit, and delete associations between records. The number of associations a record can have depends on the object type and your HubSpot subscription.

### A. Associate Records

#### 1. Without a Label (Default Association)

* **Individual Association:**
    * **Method:** `PUT`
    * **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
    * **Parameters:**
        * `fromObjectType`: ID of the object being associated (e.g., `contact`, `company`). See [Object Type IDs](#object-type-ids) for a list.
        * `fromObjectId`: ID of the record being associated.
        * `toObjectType`: ID of the object the record is being associated with.
        * `toObjectId`: ID of the record being associated with.
    * **Example:** Associate contact (ID 12345) with company (ID 67891):
        `PUT /crm/v4/objects/contact/12345/associations/default/company/67891`

* **Bulk Association:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
    * **Request Body:** Array of `objectId` values for records to associate.
    * **Example:** (Request Body) `[{ "objectId": "123" }, { "objectId": "456" }]`


#### 2. With a Label

* **Individual Association:**
    * **Method:** `PUT`
    * **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/{toObjectType}/{toObjectId}`
    * **Request Body:** Array of objects, each with:
        * `associationCategory`: `"HUBSPOT_DEFINED"` or `"USER_DEFINED"`.
        * `associationTypeId`: Numerical ID of the label.  See [Association Type IDs](#object-type-ids) and [Retrieve Association Labels](#retrieve-association-labels) for details.
    * **Example:** (Request Body, using custom label with `associationTypeId` 36):
       ```json
       [
         {
           "associationCategory": "USER_DEFINED",
           "associationTypeId": 36
         }
       ]
       ```
    * **Response:**  (Example)
       ```json
       {
         "fromObjectTypeId": "0-1",
         "fromObjectId": 29851,
         "toObjectTypeId": "0-3",
         "toObjectId": 21678228008,
         "labels": ["Point of contact"]
       }
       ```

* **Bulk Association:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`
    * **Request Body:**  Similar to individual association, but for multiple record pairs.  Includes `objectId` values for each record.


### B. Retrieve Associated Records

#### 1. Individual Record

* **Method:** `GET`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`
* **Parameters:**
    * `fromObjectType`: Object type of the record.
    * `objectId`: ID of the record.
    * `toObjectType`: Object type to retrieve associations for.


#### 2. Batch Retrieval

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Request Body:** Array of `id` values for records to retrieve associations for.
    * **Example:** (Request Body) `{"inputs": [{"id": "33451"}, {"id": "29851"}]}`
* **Response:** (Example)  Returns `toObjectId`, `associationTypes` (including `category`, `typeId`, `label`).  See full example in original document.


### C. Update Record Association Labels

Use the same endpoints as associating records (`PUT` for individual, `POST` for bulk) to update labels. To replace existing labels, only include the new labels in the request. To append, include both new and old.

### D. Remove Record Associations

#### 1. Remove All Associations

* **Individual:**
    * **Method:** `DELETE`
    * **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`

* **Bulk:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`
    * **Request Body:** Array of objects, each specifying `from` and `to` object IDs.


#### 2. Remove Specific Association Labels

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
* **Request Body:** Array of objects, each specifying `from`, `to` object IDs and the `associationTypeId` and `category` of the label to remove.


## II. Association Schema Endpoints

These endpoints manage association definitions (types) and labels.

### A. Create and Manage Association Types

* **Create Association Labels:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
    * **Request Body:**
        * `name`: Internal name (no hyphens, cannot start with a number).
        * `label`: Display name in HubSpot.
        * `inverseLabel` (optional, for paired labels): Second label in the pair.
    * **Example (single label):** `{"label": "Partner", "name": "partner"}`
    * **Example (paired labels):** `{"label": "Manager", "inverseLabel": "Employee", "name": "manager_employee"}`
    * **Response:** Returns `category` and `typeId` for the new label(s).

### B. Retrieve Association Labels

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Response:** Array of objects, each with `category`, `typeId`, and `label`.

### C. Update Association Labels

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:** `associationTypeId` and new `label` (and optionally `inverseLabel`).

### D. Delete Association Labels

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`


### E. Set and Manage Association Limits

#### 1. Create or Update Limits

* **Create:** `POST /crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create`
* **Update:** `POST /crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update`
* **Request Body:** Array of objects, each with `category`, `typeId`, and `maxToObjectIds`.

#### 2. Retrieve Limits

* **All Limits:** `GET /crm/v4/associations/definitions/configurations/all`
* **Specific Objects:** `GET /crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}`

#### 3. Delete Limits

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
* **Request Body:** Array of objects specifying `category` and `typeId` of limits to delete.


## III.  High Association Usage Report

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/usage/high-usage-report/{userId}`
* **Parameters:** `userId`:  ID of the user to receive the report.
* **Description:** Sends a report of records nearing or exceeding association limits to the specified user's email.


## IV.  Object Type IDs

A comprehensive list of `objectType` IDs is provided in the original document.  This is crucial for using the API correctly.

## V.  Limitations

* **Daily Limits:**  Vary by subscription (500,000 for Professional and Enterprise, potentially 1,000,000 with an API limit increase, but this increase doesn't apply to the association API).
* **Burst Limits:**  Vary by subscription (100 requests/10 seconds for Free/Starter, 150 for Professional/Enterprise, potentially 200 with an API limit increase, but this increase doesn't apply to the association API).


This markdown provides a structured and concise overview of the HubSpot CRM API v4 for associations. Remember to consult the original document for the complete details and any updates.
