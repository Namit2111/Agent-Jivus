# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 for managing associations between records.  Associations represent relationships between different objects (e.g., Contact to Company) or within the same object (e.g., Company to Company).  This API includes endpoints for managing associations and their schema (definitions and labels).  Requires HubSpot NodeJS Client Version 9.0.0 or later.

## I.  Association Endpoints (CRUD Operations)

These endpoints allow creating, editing, and deleting associations between records.  The number of associations a record can have depends on the object type and your HubSpot subscription.

### A. Associate Records

**1. Without a Label (Default Association):**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Parameters:**
    * `{fromObjectType}`: ID of the object being associated (e.g., `contact`, `company`). See [Object Type IDs](#object-type-ids)
    * `{fromObjectId}`: ID of the record being associated.
    * `{toObjectType}`: ID of the object the record is being associated *to*.  See [Object Type IDs](#object-type-ids).
    * `{toObjectId}`: ID of the record being associated *to*.
* **Example:** Associate contact (ID 12345) with company (ID 67891):
  `PUT /crm/v4/objects/contact/12345/associations/default/company/67891`

* **Bulk Association:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
    * **Request Body:** Array of `{objectId}` values to associate.


**2. With a Label:**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body:** Array of objects, each with:
    * `"associationCategory"`: `"HUBSPOT_DEFINED"` or `"USER_DEFINED"`.
    * `"associationTypeId"`: Numeric ID of the label.  See [Association Type IDs](#object-type-ids) and [Retrieve Association Labels](#retrieve-association-labels).
* **Example:** Associate a contact with a deal using a custom label (typeId 36):
  `PUT /crm/v4/objects/contact/{objectId}/associations/deal/{toObjectId}` with body: `[{"associationCategory": "USER_DEFINED", "associationTypeId": 36}]`
  *(Requires prior retrieval of `typeId` via `/crm/v4/associations/contact/deal/labels`)*

* **Bulk Labeled Association:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`
    * **Request Body:**  Array of associations, each with `objectId` values and the `associationCategory` and `associationTypeId`.


### B. Retrieve Associated Records

**1. Individual Record:**

* **Method:** `GET`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`
* **Parameters:**
    * `{fromObjectType}`: Object type of the record.
    * `{objectId}`: ID of the record.
    * `{toObjectType}`: Object type of associated records.

**2. Batch Retrieval:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Request Body:** Array of `{id}` values for records whose associations need to be retrieved.
* **Example:** Retrieve companies associated with two contacts:
  `POST /crm/v4/associations/contacts/companies/batch/read` with body: `{"inputs": [{"id": "33451"}, {"id": "29851"}]}`

### C. Update Record Association Labels

Use the same `PUT` and `POST` endpoints as associating records with labels. To replace a label, only include the new label. To append, include all labels (old and new).

### D. Remove Record Associations

**1. Remove All Associations:**

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}/{toObjectId}`

* **Bulk Removal:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`
    * **Request Body:** Array of `{from}` and `{to}` objects specifying records to disassociate.


**2. Remove Specific Association Labels:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
* **Request Body:** Array of objects, each with:
    * `"types"`: Array of objects specifying the `associationCategory` and `associationTypeId` to remove.
    * `"from"`: `{id}` of the `from` object.
    * `"to"`: `{id}` of the `to` object.


## II. Association Schema Endpoints

These endpoints manage association definitions (types) and their labels.

### A. Create and Manage Association Types

* **Method:** `POST` (Create), `PUT` (Update), `DELETE` (Delete)
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`  (Create/Update), `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}` (Delete)
* **Request Body (Create):**
    * `"name"`: Internal name (no hyphens, cannot start with a number).
    * `"label"`: Display name.
    * `"inverseLabel"` (optional, for paired labels):  Second label in the pair.
* **Request Body (Update):**
    * `"associationTypeId"`: ID of the label to update.
    * `"label"`: New label name.
    * `"inverseLabel"` (optional): New inverse label.

### B. Retrieve Association Labels

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Response:** Array of objects, each with `category`, `typeId`, and `label`.

### C. Update Association Labels

* See [Update Association Labels](#update-record-association-labels).


### D. Delete Association Labels

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`


### E. Set and Manage Association Limits

* **Create/Update Limits:** `POST` to `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (create) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (update).
* **Request Body:**  Array of `inputs`, each with `category`, `typeId`, and `maxToObjectIds`.
* **Retrieve Limits:** `GET` to `/crm/v4/associations/definitions/configurations/all` (all limits) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (limits between specific objects).
* **Delete Limits:** `POST` to `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`. Request body includes `category` and `typeId` of limits to remove.


## III.  High Association Usage Report

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/usage/high-usage-report/{userId}`
* **Parameters:** `{userId}`: ID of the user who will receive the report via email.


## IV.  HubSpot Defined Associations

HubSpot provides default association types:

* **Primary:** The main association.
* **Unlabeled:** A default association without a label.


## V.  Object Type IDs

[See the table in the original text for a complete list of object type IDs for various associations].


## VI. Limitations

* **Daily Limits:** Vary by subscription (Professional/Enterprise: 500,000; API limit increase: 1,000,000).
* **Burst Limits:** Vary by subscription (Free/Starter: 100 requests/10 seconds; Professional/Enterprise: 150 requests/10 seconds; API limit increase: 200 requests/10 seconds).


This documentation provides a comprehensive overview of the HubSpot CRM API v4 Associations.  Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
