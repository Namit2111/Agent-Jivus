# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 for managing record associations.  Associations represent relationships between objects and activities within the HubSpot CRM.  This version (v4) improves upon v3, offering enhanced functionality and efficiency.  For v3 documentation, refer to the provided link.

**Note:** The v4 Associations API is supported in HubSpot NodeJS Client version 9.0.0 or later.

## API Endpoints Categories

The v4 API is divided into two main endpoint categories:

* **Association Endpoints:** Create, update, and delete associations between records.
* **Association Schema Endpoints:** Manage association definitions (types), custom labels, and association limits.


## I. Association Endpoints

These endpoints handle the creation and manipulation of associations between records.  The number of associations a record can have depends on the object type and your HubSpot subscription.


### A. Associate Records

#### 1. Associate Records Without a Label

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Parameters:**
    * `fromObjectType`: ID of the object being associated (e.g., `contact`, `company`).  See [Object Type IDs](#association-type-id-values) for a list.
    * `fromObjectId`: ID of the record being associated.
    * `toObjectType`: ID of the object the record is being associated *to*.
    * `toObjectId`: ID of the record being associated *to*.
* **Example:** Associate contact (ID 12345) with company (ID 67891):
    `PUT /crm/v4/objects/contact/12345/associations/default/company/67891`

#### 2. Bulk Associate Records Without a Label

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
* **Request Body:** Array of `objectId` values for records to associate.
* **Example:**  (See example request in original text)


#### 3. Associate Records With a Label

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body:** Array of objects, each with:
    * `associationCategory`: `"HUBSPOT_DEFINED"` or `"USER_DEFINED"`.
    * `associationTypeId`: Numeric ID of the label.  Retrieve using `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`.
* **Example:** Associate a contact with a deal using a custom label (ID 36):
    1. `GET /crm/v4/associations/contact/deal/labels` (to get `typeId`)
    2. `PUT /crm/v4/objects/contact/{objectId}/associations/deal/{toObjectId}` with body: `[{"associationCategory": "USER_DEFINED", "associationTypeId": 36}]`
* **Example Response:** (See example response in original text)


#### 4. Bulk Create Labeled Associations

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`
* **Request Body:** Array of association objects, including `objectId` values and label information (`associationCategory`, `associationTypeId`).


### B. Retrieve Associated Records

#### 1. Retrieve Individual Record Associations

* **Method:** `GET`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`
* **Parameters:**
    * `fromObjectType`: Object type of the record.
    * `objectId`: ID of the record.
    * `toObjectType`: Object type of associated records.

#### 2. Bulk Retrieve Associated Records

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Request Body:** Array of `id` values for records.
* **Example Request and Response:** (See examples in original text)


### C. Update Record Association Labels

Use the bulk create endpoints (`PUT` or `POST`) to update existing labels.  Including only the new label replaces the existing one; including both old and new labels appends them.


### D. Remove Record Associations

#### 1. Remove All Associations

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`

#### 2. Bulk Remove All Associations

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`
* **Request Body:** Array of objects specifying `from` and `to` record IDs.
* **Example:** (See example in original text)

#### 3. Remove Specific Association Labels

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
* **Request Body:** Array of objects specifying `from`, `to` record IDs, and `associationTypeId` and `category` of the label to remove.
* **Example:** (See example in original text)


## II. Association Schema Endpoints

These endpoints manage association definitions (types), custom labels, and limits.


### A. Understand Association Definitions, Configurations, and Labels

This section describes HubSpot-defined and custom associations.


### B. HubSpot Defined Associations

HubSpot provides predefined association types (e.g., unlabeled Contact to Company) and two specific types:

* **Primary:** The main association; used in HubSpot tools.
* **Unlabeled:** A default association; always returned in responses with `label: null`.


### C. Custom Association Labels

You can create custom labels to further define associations.


### D. Create and Manage Association Types

Use these endpoints to create, manage, and delete custom association labels.


#### 1. Create Association Labels

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:**
    * `name`: Internal name (no hyphens, no leading numbers).
    * `label`: Display name.
    * `inverseLabel` (optional, for paired labels):  Second label in the pair.
* **Example Requests and Responses:** (See examples in original text)

#### 2. Retrieve Association Labels

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Example Response:** (See example in original text)

#### 3. Update Association Labels

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:** `associationTypeId` and updated `label` (and optionally `inverseLabel`).
* **Example:** (See example in original text)

#### 4. Delete Association Labels

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`


### E. Set and Manage Association Limits

#### 1. Create or Update Association Limits

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (create) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (update)
* **Request Body:** Array of `inputs`, each with `category`, `typeId`, and `maxToObjectIds`.
* **Example:** (See example in original text)


#### 2. Retrieve Association Limits

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/all` (all limits) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (specific objects)
* **Example Response:** (See example in original text)


#### 3. Delete Association Limits

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
* **Request Body:** Array of `inputs`, each with `category` and `typeId` of limits to delete.
* **Example:** (See example in original text)


## III. Report on High Association Usage

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/usage/high-usage-report/{userId}`
* **Parameters:** `userId`: ID of the user to receive the report.  Requires user ID retrieval via the HubSpot Users API.


## IV. Limitations

* **Daily Limits:**  Vary by HubSpot subscription (Professional/Enterprise: 500,000 requests; with API limit increase: 1,000,000).
* **Burst Limits:** Vary by subscription (Free/Starter: 100 requests/10 seconds; Professional/Enterprise: 150 requests/10 seconds; with API limit increase: 200 requests/10 seconds).


## V. Association Type ID Values

[See detailed tables in original text for `associationTypeId` values for various object pairings and association types.]


## VI. v1 Associations (Legacy)

[See the table in the original text for v1 association type IDs.]


This markdown documentation provides a comprehensive overview of the HubSpot CRM API v4 for Associations. Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
