# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 Associations endpoints.  This version supersedes the v3 Associations API.  It allows for managing relationships between records in the HubSpot CRM.

**Key Concepts:**

* **Objects:**  Represent different data types in HubSpot (e.g., Contacts, Companies, Deals).
* **Records:** Individual entries within an object (e.g., a specific contact).
* **Associations:** Relationships between records, potentially across different objects.
* **Association Types/Definitions:** Define the nature of the relationship (e.g., "Primary Company," "Billing Contact").  These can be HubSpot-defined or custom-created.
* **Association Labels:** User-defined labels that further describe an association (e.g., "Manager," "Employee").  Labels are supported for Contacts, Companies, Deals, Tickets, and Custom Objects.  Labels can be "single" (one label for both records) or "paired" (separate labels for each record in the association).


## API Endpoints

The v4 Associations API includes two categories of endpoints:

* **Association Endpoints:**  Create, update, and delete associations between records.
* **Association Schema Endpoints:** Manage association definitions (types) and labels, and set association limits.

**Note:** The v4 Associations API is supported in HubSpot NodeJS Client version 9.0.0 or later.  Association limits depend on your HubSpot subscription and the object type.


### I. Association Endpoints

#### A. Associate Records

**1. Associate Records Without a Label:**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Parameters:**
    * `fromObjectType`: ID of the source object (e.g., `contact`, `company`).  See "Association Type ID Values" section for a list.
    * `fromObjectId`: ID of the source record.
    * `toObjectType`: ID of the target object.
    * `toObjectId`: ID of the target record.
* **Example:** Associate contact (ID 12345) with company (ID 67891):
    `PUT /crm/v4/objects/contact/12345/associations/default/company/67891`

**2. Bulk Associate Records Without a Label:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
* **Request Body:** Array of `objectId` values for records to associate.


**3. Associate Records With a Label:**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body:** Array of objects, each with:
    * `associationCategory`: `"HUBSPOT_DEFINED"` or `"USER_DEFINED"`.
    * `associationTypeId`: Numerical ID of the label (obtained via `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`).

* **Example:**  Associate a contact with a deal using a custom label (typeId 36):

    `PUT /crm/v4/objects/contact/{objectId}/associations/deal/{toObjectId}`
    ```json
    [
      {
        "associationCategory": "USER_DEFINED",
        "associationTypeId": 36
      }
    ]
    ```

**4. Bulk Create Labeled Associations:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`
* **Request Body:**  Array of objects, each specifying record IDs and association details (`associationCategory`, `associationTypeId`).


#### B. Retrieve Associated Records

**1. Retrieve Individual Record's Associations:**

* **Method:** `GET`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`

**2. Bulk Retrieve Associated Records:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Request Body:** Array of `id` values for records.


#### C. Update Record Association Labels

* Use the bulk create endpoints (`/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`) to update existing labels.  Including only the new label replaces the existing label; including multiple labels appends them.


#### D. Remove Record Associations

**1. Remove All Associations Between Two Records:**

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`

**2. Bulk Remove All Associations:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`
* **Request Body:** Array of objects, each specifying `from` and `to` record IDs.

**3. Remove Specific Association Labels:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
* **Request Body:** Array of objects, each specifying record IDs and the `associationTypeId` and `category` of the label(s) to remove.



### II. Association Schema Endpoints

#### A.  Report on High Association Usage

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/usage/high-usage-report/{userId}`
* **Description:** Sends a report of records nearing or exceeding association limits to the specified user's email.


#### B. Understand Association Definitions, Configurations, and Labels

These endpoints manage association types and their configurations (limits).


#### C. Create and Manage Association Types

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:**
    * `name`: Internal name (no hyphens, doesn't start with a number).
    * `label`: Display name.
    * `inverseLabel` (optional, for paired labels): Second label in the pair.


#### D. Retrieve Association Labels

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`


#### E. Update Association Labels

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:** `associationTypeId` and new `label` (and `inverseLabel` if applicable).


#### F. Delete Association Labels

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`


#### G. Set and Manage Association Limits

**1. Create or Update Association Limits:**

* **Method:** `POST`
* **Endpoint:**
    * Create: `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create`
    * Update: `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update`
* **Request Body:** Array of objects, each with `category`, `typeId`, and `maxToObjectIds`.

**2. Retrieve Association Limits:**

* **Method:** `GET`
* **Endpoint:**
    * All limits: `/crm/v4/associations/definitions/configurations/all`
    * Limits between two objects: `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}`

**3. Delete Association Limits:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
* **Request Body:** Array of objects, each with `category` and `typeId` of limits to delete.


## Association Type ID Values

Detailed tables of HubSpot-defined `associationTypeId` values are provided in the original text.  These IDs specify the type of association between different objects.  Custom objects and custom labels will have unique `typeId` values.


## Limitations

* **Daily Limits:**  Vary by HubSpot subscription (500,000 for Professional and Enterprise; potentially 1,000,000 with an API limit increase).
* **Burst Limits:** Vary by HubSpot subscription (100 requests per 10 seconds for Free/Starter; 150 for Professional/Enterprise; potentially 200 with an API limit increase).


This comprehensive documentation provides a clear understanding of the HubSpot CRM API v4 Associations endpoints and their usage.  Remember to consult the HubSpot documentation for the most up-to-date information and any changes.
