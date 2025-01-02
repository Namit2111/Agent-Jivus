# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 for managing record associations.  Associations represent relationships between records in the HubSpot CRM, allowing connections between different object types (e.g., Contact to Company) and within the same object type (e.g., Company to Company).

This API consists of two main endpoint categories:

* **Association Endpoints:** Create, update, and delete associations between records.
* **Association Schema Endpoints:** Manage association definitions (types), custom labels, and association limits.

**Note:** The v4 Associations API requires HubSpot NodeJS Client version 9.0.0 or later.  Association limits depend on the object and your HubSpot subscription.


## I. Association Endpoints

These endpoints handle the creation, modification, and deletion of associations between records.

### A. Associate Records

#### 1. Associate Records Without a Label

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Parameters:**
    * `fromObjectType`: ID of the source object (e.g., `contact`, `company`).  See [Object Type IDs](#object-type-ids) for a list.
    * `fromObjectId`: ID of the source record.
    * `toObjectType`: ID of the target object.
    * `toObjectId`: ID of the target record.
* **Example:** Associate contact (ID 12345) with company (ID 67891):
    `PUT /crm/v4/objects/contact/12345/associations/default/company/67891`

#### 2. Bulk Associate Records Without a Label

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
* **Request Body:** Array of `objectId` values for records to associate.
* **Example:**  (See example request body in original document)

#### 3. Associate Records With a Label

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body:** Array of objects, each with:
    * `associationCategory`: `"HUBSPOT_DEFINED"` or `"USER_DEFINED"`.
    * `associationTypeId`: Numeric ID of the label.  See [Association Type IDs](#object-type-ids) or retrieve labels via `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`.
* **Example:** Associate contact (objectId) with deal (toObjectId) using custom label (typeId 36):
    `PUT /crm/v4/objects/contact/{objectId}/associations/deal/{toObjectId}`
    (Request Body: `[{"associationCategory": "USER_DEFINED", "associationTypeId": 36}]`)

#### 4. Bulk Create Labeled Associations

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`
* **Request Body:** Array of associations, each with `objectId` values and label information (`associationCategory`, `associationTypeId`).


### B. Retrieve Associated Records

#### 1. Retrieve Individual Record's Associations

* **Method:** `GET`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`
* **Parameters:**
    * `fromObjectType`: Source object ID.
    * `objectId`: Source record ID.
    * `toObjectType`: Target object ID.

#### 2. Bulk Retrieve Associated Records

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Request Body:** Array of `id` values for records.

### C. Update Record Association Labels

Use the bulk create endpoints (`/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`) to update labels.  To replace existing labels, only include the new label in the request. To append labels, include both old and new labels.

### D. Remove Record Associations

#### 1. Remove All Associations Between Two Records

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`

#### 2. Bulk Remove All Associations

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`
* **Request Body:** Array of associations to remove (from and to object IDs).

#### 3. Remove Specific Association Labels

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
* **Request Body:**  Array of objects, each specifying record IDs and `associationTypeId` and `category` of the label to remove.


## II. Association Schema Endpoints

These endpoints manage association definitions, labels, and limits.

### A. Understand Association Definitions, Configurations, and Labels

This section explains how to manage association types, labels, and limits using the schema endpoints.

### B. HubSpot Defined Associations

HubSpot provides predefined association types (`Primary` and `Unlabeled`).


### C. Custom Association Labels

Create custom labels to add context to record relationships.

#### 1. Create Association Labels

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:**
    * `name`: Internal name (no hyphens, no leading numbers).
    * `label`: Display name.
    * `inverseLabel` (optional, for paired labels): Name of the inverse label.

#### 2. Retrieve Association Labels

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`

#### 3. Update Association Labels

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:** `associationTypeId` and updated `label` (and optionally `inverseLabel`).

#### 4. Delete Association Labels

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`

### D. Set and Manage Association Limits

#### 1. Create or Update Association Limits

* **Method:** `POST`
* **Endpoint:**
    * Create: `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create`
    * Update: `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update`
* **Request Body:** Array of objects, each with `category`, `typeId`, and `maxToObjectIds`.

#### 2. Retrieve Association Limits

* **Method:** `GET`
* **Endpoint:**
    * All limits: `/crm/v4/associations/definitions/configurations/all`
    * Limits between two objects: `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}`

#### 3. Delete Association Limits

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
* **Request Body:** Array of objects to delete, each specifying `category` and `typeId`.


## III.  Limitations

* **Daily Limits:**  Vary by subscription (Professional/Enterprise: 500,000; with API limit increase: 1,000,000).
* **Burst Limits:** Vary by subscription (Free/Starter: 100 requests/10 seconds; Professional/Enterprise: 150 requests/10 seconds; with API limit increase: 200 requests/10 seconds).

## IV. Association Type ID Values

[See detailed tables of `associationTypeId` values in the original document]


## V.  v1 Associations (Legacy)

[See legacy v1 association IDs in the original document]

This comprehensive markdown documentation provides a clear and concise overview of the HubSpot CRM API v4 for associations, including detailed endpoint descriptions, request/response examples, and crucial considerations regarding limits and IDs.  Remember to replace placeholder values (e.g., `{objectId}`, `{fromObjectType}`) with actual values in your API calls.
