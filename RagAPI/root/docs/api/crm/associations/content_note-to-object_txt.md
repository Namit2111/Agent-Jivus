# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 Associations endpoints, allowing you to manage relationships between records in the HubSpot CRM.  This API supports both default (unlabeled) and custom labeled associations.

**Note:** The v4 Associations API requires HubSpot NodeJS Client Version 9.0.0 or later.  Association limits depend on your HubSpot object and subscription.


## I. Core Concepts

* **Objects:**  Represent different data types in HubSpot (e.g., Contacts, Companies, Deals).
* **Records:** Individual entries within an object (e.g., a specific Contact record).
* **Associations:** Relationships between records, potentially across different objects.
* **Association Types (Definitions):** Define the types of relationships between objects (e.g., "Primary Company," "Billing Contact").  These can be HubSpot-defined or custom-created.
* **Labels:** User-defined names for association types, adding context to relationships.
* **`associationTypeId`:** A numerical ID uniquely identifying an association type.
* **`associationCategory`:**  Indicates whether an association type is `HUBSPOT_DEFINED` (predefined by HubSpot) or `USER_DEFINED` (custom).


## II. API Endpoints

The v4 Associations API offers two main categories of endpoints:

**A. Association Endpoints:**  Manage the creation, modification, and deletion of associations between records.

**B. Association Schema Endpoints:** Manage association definitions (types), custom labels, and association limits.

### II.A. Association Endpoints

#### 1. Associate Records

* **Without a Label (Default):**
    * **Method:** `PUT`
    * **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
    * **Example:**  `/crm/v4/objects/contact/12345/associations/default/company/67891` (Associates contact 12345 with company 67891)
    * **Bulk Association:**
        * **Method:** `POST`
        * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
        * **Request Body:** Array of `objectId` values.


* **With a Label:**
    * **Method:** `PUT`
    * **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
    * **Request Body:** Array of objects, each containing `associationCategory` and `associationTypeId`.
    * **Bulk Creation:**
        * **Method:** `POST`
        * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`
        * **Request Body:** Array of objects specifying record IDs and labels.

#### 2. Retrieve Associated Records

* **Individual Record:**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`
* **Batch Retrieval:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
    * **Request Body:** Array of `id` values for records.


#### 3. Update Record Association Labels

* Use the bulk create endpoints (`POST /crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`) to replace or append labels to existing associations.


#### 4. Remove Record Associations

* **All Associations:**
    * **Method:** `DELETE`
    * **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
    * **Bulk Deletion:**
        * **Method:** `POST`
        * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`
* **Specific Association Labels:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
    * **Request Body:** Array of objects specifying record IDs and `associationTypeId`, `category` to remove.



### II.B. Association Schema Endpoints

#### 1. Create and Manage Association Types

* **Create Association Labels:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
    * **Request Body:**  `name`, `label`, `inverseLabel` (for paired labels).
* **Retrieve Association Labels:**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Update Association Labels:**
    * **Method:** `PUT`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
    * **Request Body:** `associationTypeId`, `label`, `inverseLabel` (optional).
* **Delete Association Labels:**
    * **Method:** `DELETE`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`

#### 2. Set and Manage Association Limits

* **Create/Update Limits:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (create) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (update)
    * **Request Body:** Array of objects, each with `category`, `typeId`, `maxToObjectIds`.
* **Retrieve Limits:**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/all` (all limits) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (specific objects)
* **Delete Limits:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
    * **Request Body:** Array of objects specifying `category` and `typeId` to delete.

#### 3. High Association Usage Report

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/usage/high-usage-report/{userID}`
* This endpoint generates a report (sent via email) of records nearing or exceeding their association limits.


## III.  Example Responses (Detailed in the original text)

The original text provides numerous examples of request bodies and responses for various endpoints.  Refer to the original text for those detailed examples.


## IV.  Limitations

* **Daily Limits:** Vary based on your HubSpot subscription (Professional/Enterprise: 500,000; with API limit increase: 1,000,000).
* **Burst Limits:** Vary based on your HubSpot subscription (Free/Starter: 100 requests/10 seconds; Professional/Enterprise: 150 requests/10 seconds; with API limit increase: 200 requests/10 seconds).


## V.  `associationTypeId` Values

The original text provides extensive tables listing `associationTypeId` values for various HubSpot-defined associations between different object types.  Consult the original document for this detailed reference.


## VI.  v1 Associations (Legacy)

The original document also includes a table of `associationTypeId` values for the legacy v1 Associations API.  This is provided for reference only, as the v4 API is recommended.
