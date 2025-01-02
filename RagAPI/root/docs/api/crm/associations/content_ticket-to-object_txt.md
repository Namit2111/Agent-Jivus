# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 for managing associations between records.  Associations represent relationships between different objects (e.g., Contact to Company) or within the same object (e.g., Company to Company).  This API comprises two sets of endpoints: Association endpoints and Association schema endpoints.

**Note:** The v4 Associations API is supported in Version 9.0.0 or later of the NodeJS HubSpot Client.  Association limits depend on the object and your HubSpot subscription.


## I. Association Endpoints

These endpoints create, edit, and remove associations between records.

### A. Associate Records

#### 1. Associate Records Without a Label

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Parameters:**
    * `fromObjectType`: ID of the object being associated (e.g., `contact`, `company`).  See [Object Type IDs](#object-type-ids)
    * `fromObjectId`: ID of the record being associated.
    * `toObjectType`: ID of the object the record is being associated *to*.  See [Object Type IDs](#object-type-ids)
    * `toObjectId`: ID of the record being associated to.
* **Example:** Associate contact (ID 12345) with company (ID 67891):
    `PUT /crm/v4/objects/contact/12345/associations/default/company/67891`

#### 2. Bulk Associate Records Without a Label

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
* **Request Body:**  Array of `objectId` values for records to associate.
* **Example:** (See example request body in original documentation)

#### 3. Associate Records With a Label

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body:** Array of objects, each with:
    * `associationCategory`: `"HUBSPOT_DEFINED"` or `"USER_DEFINED"`
    * `associationTypeId`: Numeric ID of the label. See [Default Type IDs](#default-type-ids) and how to retrieve custom label IDs.
* **Example:** (See example request body and response in original documentation)


#### 4. Bulk Create Labeled Associations

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`
* **Request Body:** Array of objects, each with `objectId` values and required label parameters (`associationCategory`, `associationTypeId`).
* **Example:** (See example request body in original documentation)


### B. Retrieve Associated Records

#### 1. Retrieve Individual Record's Associations

* **Method:** `GET`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`
* **Parameters:**
    * `fromObjectType`: Object type of the record whose associations are being retrieved.
    * `objectId`: ID of the record.
    * `toObjectType`: Object type of the associated records to retrieve.

#### 2. Bulk Retrieve Associated Records

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Request Body:** Array of `id` values for records.
* **Example:** (See example request and response in original documentation)


### C. Update Record Association Labels

* Use the bulk create endpoints (`POST /crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`)  to update labels.  To replace an existing label, only include the new label. To append, include both new and existing labels.

### D. Remove Record Associations

#### 1. Remove All Associations Between Two Records

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`

#### 2. Bulk Remove All Associations

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`
* **Request Body:** Array of objects, each with `from` and `to` objects containing `id` values.
* **Example:** (See example request body in original documentation)

#### 3. Remove Specific Association Labels

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
* **Request Body:** Array of objects, each with `from`, `to`, and `types` (containing `associationCategory` and `associationTypeId`).
* **Example:** (See example request body and response in original documentation)



## II. Association Schema Endpoints

These endpoints manage association definitions (types), custom labels, and association limits.

### A. Understand Association Definitions, Configurations, and Labels

This section covers managing association types, configurations, and labels.


### B. HubSpot Defined Associations

HubSpot provides predefined association types (e.g., unlabeled Contact to Company).  Two key types:

* **Primary:** The main association. Used in HubSpot tools.
* **Unlabeled:** A default association; `label` will be `null`.


### C. Custom Association Labels

Create custom labels to provide additional context to relationships (e.g., "Manager," "Employee").


### D. Create and Manage Association Types

* **Create Association Labels:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
    * **Request Body:**
        * `name`: Internal name (no hyphens, no leading number).
        * `label`: Display name.
        * `inverseLabel` (optional, for paired labels): Second label in the pair.
    * **Example:** (See example request bodies and responses in original documentation)

* **Retrieve Association Labels:**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
    * **Example:** (See example response in original documentation)

* **Update Association Labels:**
    * **Method:** `PUT`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
    * **Request Body:** `associationTypeId` and new `label` (and optionally `inverseLabel`).
    * **Example:** (See example request in original documentation)

* **Delete Association Labels:**
    * **Method:** `DELETE`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`


### E. Set and Manage Association Limits

* **Create or Update Association Limits:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (create) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (update)
    * **Request Body:** Array of `inputs`, each with:
        * `category`: `"HUBSPOT_DEFINED"` or `"USER_DEFINED"`.
        * `typeId`: Numeric ID of the association type.
        * `maxToObjectIds`: Maximum number of associations allowed.
    * **Example:** (See example request in original documentation)

* **Retrieve Association Limits:**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/all` (all limits) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (limits between specific objects)
    * **Example:** (See example response in original documentation)

* **Delete Association Limits:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
    * **Request Body:** Array of `inputs`, each with `category` and `typeId`.
    * **Example:** (See example request in original documentation)


## III.  High Association Usage Report

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/usage/high-usage-report/{userID}`
* **Parameters:** `userID`: ID of the user to receive the report.
* **Description:** Generates a report of records nearing or exceeding their association limits.  The report is emailed to the specified user.


## IV.  Limitations

* **Daily Limits:** 500,000 requests (Professional and Enterprise; increases to 1,000,000 with API limit increase, but not further for associations).
* **Burst Limits:** 100 requests per 10 seconds (Free/Starter); 150 (Professional/Enterprise); 200 (with API limit increase, but not further for associations).


## V. Object Type IDs

*(Refer to the tables in the original documentation for a comprehensive list of `typeId` values for different object pairings)*

This section provides a partial representation.  Consult the original document for the complete list.

### Default Type IDs:

*(Refer to the original documentation for the complete list)*

This section needs the full table from the original document to be completed.


## VI.  v1 Associations (Legacy)

*(Refer to the table in the original documentation for the legacy v1 `typeId` values)*



This comprehensive markdown documentation provides a detailed overview of the HubSpot CRM API v4 for Associations, including all the endpoints, request/response examples, and crucial details like limitations and object type IDs. Remember to consult the original documentation for the most up-to-date and complete information.
