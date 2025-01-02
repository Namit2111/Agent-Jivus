# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 for managing record associations.  Associations represent relationships between objects and activities within the HubSpot CRM.  This version offers both association endpoints (for creating, editing, and removing associations) and association schema endpoints (for managing association definitions, labels, and limits).

**Note:** The v4 Associations API is supported in Version 9.0.0 or later of the NodeJS HubSpot Client.


## I. Association Endpoints

These endpoints handle the creation, modification, and deletion of associations between records.

### A. Associate Records

#### 1. Associate Records Without a Label

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Parameters:**
    * `fromObjectType`: ID of the object being associated (e.g., `contact`, `company`). See [Object Type IDs](#object-type-ids).
    * `fromObjectId`: ID of the record being associated.
    * `toObjectType`: ID of the object the record is being associated with. See [Object Type IDs](#object-type-ids).
    * `toObjectId`: ID of the record being associated with.
* **Example:** Associate contact (ID 12345) with company (ID 67891):
    `PUT /crm/v4/objects/contact/12345/associations/default/company/67891`

#### 2. Bulk Associate Records Without a Label

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
* **Request Body:** Array of `objectId` values for records to associate.
* **Example:** (See example request body in original text)


#### 3. Associate Records With a Label

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body:** Array of objects, each with:
    * `associationCategory`: `"HUBSPOT_DEFINED"` or `"USER_DEFINED"`.
    * `associationTypeId`: Numerical ID of the label.  Retrieve using `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`.
* **Example:** (See example request body and response in original text)

#### 4. Bulk Create Labeled Associations

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`
* **Request Body:** Array of objects specifying `objectId`s and labels.  Requires `associationCategory` and `associationTypeId`.
* **Example:** (See example request body in original text)


### B. Retrieve Associated Records

#### 1. Retrieve Individual Record's Associations

* **Method:** `GET`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`
* **Parameters:**
    * `fromObjectType`: Object type of the record.
    * `objectId`: ID of the record.
    * `toObjectType`: Object type of associated records.
* **Example:** Get all company associations for contact with ID 12345:
    `GET /crm/v4/objects/contact/12345/associations/company`

#### 2. Bulk Retrieve Associated Records

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Request Body:** Array of `id` values for records.
* **Example:** (See example request and response in original text)

### C. Update Record Association Labels

* Use the bulk create endpoints (`POST /crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`) to update existing labels.  Include all desired labels; existing labels will be replaced.

### D. Remove Record Associations

#### 1. Remove All Associations Between Two Records

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`

#### 2. Bulk Remove All Associations

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`
* **Request Body:** Array of objects, each specifying `from` and `to` object IDs.
* **Example:** (See example request body in original text)


#### 3. Remove Specific Association Labels

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
* **Request Body:** Array of objects, each specifying `from`, `to` object IDs, and `associationTypeId` and `category` of labels to remove.
* **Example:** (See example request body in original text)


### E. Report on High Association Usage

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/usage/high-usage-report/{userId}`
* **Parameter:** `userId`: ID of the user to receive the report.  Use the HubSpot Users API to retrieve user IDs.
* **Response:** A report (sent via email) of records nearing or exceeding association limits.


## II. Association Schema Endpoints

These endpoints manage association definitions, labels, and limits.

### A. Understand Association Definitions, Configurations, and Labels

This section covers managing association types, labels, and limits.

### B. HubSpot Defined Associations

* **Primary:** The main association (used in lists and workflows).
* **Unlabeled:** A default association with `label: null`.


### C. Custom Association Labels

Create custom labels to add context to record relationships.

#### 1. Create and Manage Association Types

* Use the definition endpoints to create and manage custom association types.

#### 2. Create Association Labels

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:**
    * `name`: Internal name (no hyphens, doesn't start with a number).
    * `label`: Display name of the label.
    * `inverseLabel` (optional, for paired labels): Second label in the pair.
* **Example:** (See example request bodies and response in original text)

#### 3. Retrieve Association Labels

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Response:** Array of objects, each with `category`, `typeId`, and `label`.
* **Example:** (See example response in original text)

#### 4. Update Association Labels

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:** `associationTypeId` and updated `label` (and `inverseLabel` if paired).
* **Example:** (See example request in original text)

#### 5. Delete Association Labels

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`


### D. Set and Manage Association Limits

#### 1. Create or Update Association Limits

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/{create|update}`
* **Request Body:**  Array of objects, each with `category`, `typeId`, and `maxToObjectIds`.
* **Example:** (See example request in original text)

#### 2. Retrieve Association Limits

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (or `/crm/v4/associations/definitions/configurations/all` for all limits).
* **Response:** Array of objects, each with `category`, `typeId`, `maxToObjectIds`, and `label`.
* **Example:** (See example response in original text)

#### 3. Delete Association Limits

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
* **Request Body:** Array of objects, each with `category` and `typeId` of limits to delete.
* **Example:** (See example request in original text)


## III. Limitations

* **Daily Limits:** 500,000 requests (Professional and Enterprise accounts).  API limit increase may raise this to 1,000,000, but this maximum won't further increase for association API requests.
* **Burst Limits:** 100 requests per 10 seconds (Free and Starter accounts), 150 requests per 10 seconds (Professional and Enterprise accounts). API limit increase raises this to 200 requests per 10 seconds, but this maximum won't further increase for association API requests.


## IV. Association Type ID Values

[See tables in original text for a comprehensive list of HubSpot-defined `associationTypeId` values for various object pairings.]


## V.  v1 Associations (Legacy)

[See table in original text for legacy v1 association type IDs.]


This markdown provides a structured and more readable version of the original documentation, enhancing clarity and ease of understanding.  Remember to always consult the official HubSpot API documentation for the most up-to-date information.
