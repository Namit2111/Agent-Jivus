# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 Associations endpoints.  This version supersedes v3.  For v3 documentation, see the provided link in the original text.

## Overview

The Associations API v4 allows you to manage relationships between records in the HubSpot CRM.  These relationships can be between different object types (e.g., Contact to Company) or within the same object type (e.g., Company to Company).  The API comprises two main sections:

* **Association Endpoints:** Create, update, and delete associations between records.
* **Association Schema Endpoints:** Manage association definitions (types), custom labels, and association limits.

**Note:** The v4 API requires HubSpot NodeJS Client version 9.0.0 or later.  Association limits depend on your HubSpot object and subscription.


## I. Association Endpoints

These endpoints handle the creation, modification, and deletion of record associations.

### A. Associate Records

#### 1. Associate Records Without a Label

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Parameters:**
    * `fromObjectType`: ID of the source object.  Use object name (e.g., `contact`, `company`) for contacts, companies, deals, tickets, and notes; otherwise, use the object type ID.
    * `fromObjectId`: ID of the source record.
    * `toObjectType`: ID of the target object.  Use object name (e.g., `contact`, `company`) for contacts, companies, deals, tickets, and notes; otherwise, use the object type ID.
    * `toObjectId`: ID of the target record.
* **Example:** Associate contact (ID 12345) with company (ID 67891):
    `PUT /crm/v4/objects/contact/12345/associations/default/company/67891`

#### 2. Bulk Associate Records Without a Label

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
* **Request Body:** Array of `objectId` values to associate.
* **Example:**  Associate multiple contacts with companies (see example in original text).


#### 3. Associate Records With a Label

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body:** Array of objects, each with:
    * `associationCategory`: `"HUBSPOT_DEFINED"` or `"USER_DEFINED"`
    * `associationTypeId`: Numeric ID of the label (obtain via `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`).
* **Example:** Associate a contact with a deal using a custom label (see example in original text, steps 1-3).


#### 4. Bulk Create Labeled Associations

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`
* **Request Body:**  Array of associations with `id` values, `associationCategory`, and `associationTypeId` for each.

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
* **Request Body:** Array of `id` values of records to retrieve associations for.
* **Example:** Retrieve all company associations for two contacts (see example request and response in original text).


### C. Update Record Association Labels

Use the same `PUT` and `POST` endpoints as for association creation (sections I.A.3 and I.A.4), including both old and new labels to append, or just new labels to replace.


### D. Remove Record Associations

#### 1. Remove All Associations Between Two Records

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`

#### 2. Bulk Remove All Associations

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`
* **Request Body:** Array of objects, each specifying `from` and `to` record IDs.
* **Example:** Remove all associations between sets of contacts and companies (see example in original text).

#### 3. Remove Specific Association Labels

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
* **Request Body:** Array of objects, each specifying `from`, `to` record IDs, and `associationTypeId` and `category` of labels to remove.
* **Example:** Remove a custom label from an association (see example in original text).


## II. Association Schema Endpoints

These endpoints manage association definitions, labels, and limits.

### A. Understand Association Definitions, Configurations, and Labels

This section covers HubSpot-defined and custom association labels,  including how to manage association types and limits.


### B. Create and Manage Association Types

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:**
    * `name`: Internal name (no hyphens, no leading number).
    * `label`: Label displayed in HubSpot.
    * `inverseLabel` (optional, for paired labels): Second label in the pair.
* **Example:** Create single and paired labels (see examples in original text).

### C. Retrieve Association Labels

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Example:** Retrieve all association types from contacts to companies (see example response in original text).


### D. Update Association Labels

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:** `associationTypeId` and new `label` (and optionally `inverseLabel`).
* **Example:** Update a label (see example in original text).


### E. Delete Association Labels

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`


### F. Set and Manage Association Limits

#### 1. Create or Update Association Limits

* **Method:** `POST`
* **Endpoint:**
    * Create: `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create`
    * Update: `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update`
* **Request Body:** Array of `inputs`, each with `category`, `typeId`, and `maxToObjectIds`.
* **Example:** Set limits for deal-contact associations (see example in original text).

#### 2. Retrieve Association Limits

* **Method:** `GET`
* **Endpoint:**
    * All limits: `/crm/v4/associations/definitions/configurations/all`
    * Specific objects: `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}`
* **Example:** Retrieve limits between deals and contacts (see example response in original text).

#### 3. Delete Association Limits

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
* **Request Body:** Array of `inputs`, each with `category` and `typeId`.
* **Example:** Remove a limit (see example in original text).


## III.  Limitations

* **Daily Limits:**  Vary by HubSpot subscription (see original text).
* **Burst Limits:** Vary by HubSpot subscription (see original text).


## IV. Association Type ID Values

See the extensive tables in the original text for HubSpot-defined `associationTypeId` values for various object pairings and association directions.  Custom object and label type IDs must be retrieved from HubSpot settings.


## V.  Legacy v1 Associations API

A table of legacy v1 association type IDs is also provided in the original text.  Use v4 API when possible.


This markdown documentation provides a comprehensive overview of the HubSpot CRM API v4 Associations, including detailed explanations of endpoints, parameters, request and response examples, and important limitations.  Always refer to the official HubSpot API documentation for the most up-to-date information.
