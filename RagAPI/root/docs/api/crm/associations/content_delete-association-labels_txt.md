# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 for managing record associations.  Associations represent relationships between records in the HubSpot CRM, allowing connections between different object types (e.g., Contact to Company) and within the same object type (e.g., Company to Company).

This API comprises two main sections:

* **Association endpoints:** Create, update, and delete associations between records.
* **Association schema endpoints:** Manage association definitions (types), custom labels, and association limits.

## I. Association Endpoints

These endpoints handle the creation, modification, and deletion of associations between records.  The number of associations a record can have depends on the object type and your HubSpot subscription.

### A. Associate Records

#### 1. Associate Records Without a Label

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Parameters:**
    * `fromObjectType`: ID of the source object (e.g., `contact`, `company`). See [Object Type IDs](#object-type-ids).
    * `fromObjectId`: ID of the source record.
    * `toObjectType`: ID of the target object. See [Object Type IDs](#object-type-ids).
    * `toObjectId`: ID of the target record.
* **Example:** Associate contact with ID 12345 to company with ID 67891:
    ```
    PUT /crm/v4/objects/contact/12345/associations/default/company/67891
    ```

#### 2. Bulk Associate Records Without a Label

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
* **Request Body:** Array of `objectId` values for records to associate.
* **Example:** Associate multiple contacts to companies: (See example in original document)

#### 3. Associate Records With a Label

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body:** Array of objects, each with:
    * `associationCategory`: `"HUBSPOT_DEFINED"` or `"USER_DEFINED"`.
    * `associationTypeId`: Numeric ID of the association label.  See [Object Type IDs](#object-type-ids) and [Retrieve Association Labels](#retrieve-association-labels).
* **Example:** Associate a contact with a deal using a custom label (See example in original document).

#### 4. Bulk Create Labeled Associations

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`
* **Request Body:**  Array of association objects including `objectId` values and label information (`associationCategory`, `associationTypeId`).


### B. Retrieve Associated Records

#### 1. Retrieve Individual Record Associations

* **Method:** `GET`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`
* **Parameters:**
    * `fromObjectType`: ID of the source object.
    * `objectId`: ID of the source record.
    * `toObjectType`: ID of the target object.

#### 2. Bulk Retrieve Associated Records

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Request Body:** Array of `id` values for records whose associations are to be retrieved.
* **Example:** Retrieve all company associations for two contacts (See example in original document).


### C. Update Record Association Labels

Use the same endpoints as for creating labeled associations (`PUT` or `POST`).  To replace existing labels, only include the new label(s) in the request. To append labels, include both old and new.

### D. Remove Record Associations

#### 1. Remove All Associations

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`

#### 2. Bulk Remove All Associations

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`
* **Request Body:** Array of objects, each specifying `from` and `to` object IDs.

#### 3. Remove Specific Association Labels

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
* **Request Body:**  Array of objects specifying `from`, `to` object IDs and  `associationTypeId` and `category` of labels to remove.


## II. Association Schema Endpoints

These endpoints manage association definitions, custom labels, and limits.

### A. Understand Association Definitions, Configurations, and Labels

This section covers HubSpot-defined associations (e.g., "Primary") and custom labels.


### B. Create and Manage Association Types

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:**  `name`, `label`, `inverseLabel` (for paired labels).

### C. Retrieve Association Labels

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`


### D. Update Association Labels

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:** `associationTypeId` and updated `label` and optionally `inverseLabel`.


### E. Delete Association Labels

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`


### F. Set and Manage Association Limits

#### 1. Create or Update Association Limits

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (create) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (update)
* **Request Body:** Array of objects with `category`, `typeId`, and `maxToObjectIds`.

#### 2. Retrieve Association Limits

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/all` (all limits) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (specific objects).

#### 3. Delete Association Limits

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
* **Request Body:** Array of objects with `category` and `typeId` of limits to delete.


## III. Report on High Association Usage

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/usage/high-usage-report/{userId}`
* **Parameters:** `userId`: ID of the user to receive the report.


## IV. Limitations

* **Daily Limits:** Vary by subscription (500,000 for Professional and Enterprise, potentially 1,000,000 with API limit increase).
* **Burst Limits:** Vary by subscription (100 requests per 10 seconds for Free/Starter, 150 for Professional/Enterprise, potentially 200 with API limit increase).


## V. Object Type IDs

[Include the tables from the original document detailing `associationTypeId` values for different object types and association directions here.  This section should be formatted as a clear table for easy readability.]


## VI. Legacy v1 Associations API

[Include the table from the original document detailing the legacy v1 association IDs.]

This comprehensive documentation provides a clear understanding of the HubSpot CRM API v4 for associations, enabling developers to effectively manage record relationships within their HubSpot instances. Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
