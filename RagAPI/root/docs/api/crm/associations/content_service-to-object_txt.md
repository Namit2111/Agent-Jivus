# HubSpot CRM API: Associations v4

This document details the HubSpot CRM API v4 for managing associations between records.  Associations represent relationships between different objects (e.g., Contact to Company) or within the same object (e.g., Company to Company).  This API provides endpoints for creating, updating, retrieving, and deleting associations, along with managing association schemas (types and labels).

**Note:** This API is supported in HubSpot NodeJS Client Version 9.0.0 or later.  The number of associations a record can have depends on the object type and your HubSpot subscription.

## I. Association Endpoints

These endpoints manage the associations themselves.

### A. Associate Records

**1. Associate records without a label:**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Parameters:**
    * `fromObjectType`: ID of the object being associated (e.g., `contact`, `company`). See [Object Type IDs](#object-type-ids).
    * `fromObjectId`: ID of the record being associated.
    * `toObjectType`: ID of the object the record is being associated *to*. See [Object Type IDs](#object-type-ids).
    * `toObjectId`: ID of the record being associated *to*.
* **Example:** Associate contact (ID 12345) with company (ID 67891):
    `PUT /crm/v4/objects/contact/12345/associations/default/company/67891`

**2. Bulk associate records without a label:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
* **Request Body:** Array of `objectId` values for records to associate.
* **Example:** (See example request body in original document)

**3. Associate records with a label:**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body:** Array of objects, each with:
    * `associationCategory`: `"HUBSPOT_DEFINED"` or `"USER_DEFINED"`.
    * `associationTypeId`: Numeric ID of the label.  Retrieve using `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`.
* **Example:** (See example request body and response in original document)

**4. Bulk create labeled associations:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`
* **Request Body:**  Array of association objects, including `objectId` values and label information (`associationCategory`, `associationTypeId`).
* **Example:** (See example in original document)


### B. Retrieve Associated Records

**1. Retrieve individual record's associations:**

* **Method:** `GET`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`
* **Parameters:**
    * `fromObjectType`: Object type of the record.
    * `objectId`: ID of the record.
    * `toObjectType`: Object type to retrieve associations for.

**2. Retrieve associated records in bulk:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Request Body:** Array of `{id: objectId}` for records to retrieve associations for.
* **Example:** (See example request and response in original document)

### C. Update Record Association Labels

* Use the bulk create endpoints (`/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`) to update existing labels.  Include all labels, both existing and new.

### D. Remove Record Associations

**1. Remove all associations between two records:**

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`

**2. Bulk remove all associations:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`
* **Request Body:** Array of `{from: {id: objectId}, to: [{id: objectId}]}`.
* **Example:** (See example request body in original document)


**3. Remove specific association labels:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
* **Request Body:** Array of objects, each with `types` (array of `{associationCategory, associationTypeId}`), `from: {id}`, and `to: {id}`.
* **Example:** (See example request body and response in original document)

## II. Association Schema Endpoints

These endpoints manage the definitions and configurations of association types and labels.

### A. Understand Association Definitions, Configurations, and Labels

This section covers creating, managing, and retrieving association types and their configurations.

### B. HubSpot Defined Associations

HubSpot provides predefined association types, including "Primary" and "Unlabeled."

### C. Custom Association Labels

Create custom labels to add context to associations.

### D. Create and Manage Association Types

* **Create association labels:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
    * **Request Body:**
        * `name`: Internal name (no hyphens, doesn't start with a number).
        * `label`: Display name.
        * `inverseLabel` (optional, for paired labels): Second label in the pair.
    * **Example:** (See example request bodies and response in original document)

### E. Retrieve Association Labels

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Example:** (See example response in original document)

### F. Update Association Labels

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:** `{associationTypeId, label, inverseLabel (optional)}`
* **Example:** (See example request in original document)

### G. Delete Association Labels

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`


### H. Set and Manage Association Limits

* **Create or update association limits:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (create) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (update)
    * **Request Body:** Array of `{category, typeId, maxToObjectIds}`.
    * **Example:** (See example request in original document)

* **Retrieve association limits:**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/all` (all limits) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (limits between two objects)
    * **Example:** (See example response in original document)

* **Delete association limits:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
    * **Request Body:** Array of `{category, typeId}`.
    * **Example:** (See example request in original document)


## III.  Limitations

* **Daily Limits:** 500,000 requests (Professional/Enterprise).  API limit increase to 1,000,000 (Association API requests will not exceed 1,000,000 even with an increase).
* **Burst Limits:** 100 requests per 10 seconds (Free/Starter), 150 requests per 10 seconds (Professional/Enterprise). API limit increase to 200 requests per 10 seconds (Association API requests will not exceed 200 even with an increase).

## IV. Association Type ID Values

[See the extensive tables in the original document for a complete list of `associationTypeId` values for various object pairings and association types.]

## V. Legacy v1 Associations

[See the table in the original document for legacy v1 association type IDs.]


This markdown documentation provides a comprehensive overview of the HubSpot CRM API v4 for Associations. Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
