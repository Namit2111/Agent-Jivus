# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 for managing associations between records.  Associations represent relationships between different CRM objects (e.g., Contact to Company) or within the same object (e.g., Company to Company).  This API provides endpoints for creating, managing, and retrieving these associations, including the ability to add custom labels.

**Note:** The v4 Associations API requires HubSpot NodeJS Client Version 9.0.0 or later.  Association limits depend on your HubSpot object and subscription.

## API Endpoints

The v4 Associations API is divided into two categories of endpoints:

* **Association Endpoints:** Create, edit, and remove associations between records.
* **Association Schema Endpoints:** Manage association definitions (types), custom labels, and association limits.


### I. Association Endpoints

#### A. Associate Records

**1. Associate Records Without a Label:**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Parameters:**
    * `fromObjectType`: ID of the source object (e.g., `contact`, `company`). See [Object Type IDs](#object-type-ids).
    * `fromObjectId`: ID of the source record.
    * `toObjectType`: ID of the target object.
    * `toObjectId`: ID of the target record.
* **Example:** Associate contact (ID 12345) with company (ID 67891):
    ```
    PUT /crm/v4/objects/contact/12345/associations/default/company/67891
    ```

**2. Bulk Associate Records Without a Label:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
* **Request Body:** Array of `objectId` values to associate.
* **Example:** Associate multiple contacts with a company.  Request Body:
    ```json
    [12345, 67890, 13579]
    ```

**3. Associate Records With a Label:**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body:** Array of objects, each with:
    * `associationCategory`: `"HUBSPOT_DEFINED"` or `"USER_DEFINED"`.
    * `associationTypeId`: Numeric ID of the label.  Obtain this via the `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels` endpoint.
* **Example:** Associate contact (ID 12345) with deal (ID 98765) using custom label (ID 36):
    ```json
    [{"associationCategory": "USER_DEFINED", "associationTypeId": 36}]
    ```
    ```
    PUT /crm/v4/objects/contact/12345/associations/deal/98765
    ```

**4. Bulk Create Labeled Associations:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`
* **Request Body:** Array of objects, each specifying `fromObjectId`, `toObjectId`, `associationCategory`, and `associationTypeId`.


#### B. Retrieve Associated Records

**1. Retrieve Individual Record Associations:**

* **Method:** `GET`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`
* **Parameters:**
    * `fromObjectType`: Source object ID.
    * `objectId`: Source record ID.
    * `toObjectType`: Target object ID.

**2. Bulk Retrieve Associated Records:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Request Body:** Array of `id` values for records to retrieve associations for.


#### C. Update Record Association Labels

Use the same endpoints as associating records (`PUT` and `POST` batch endpoints) but include the new label(s) in the request body. Existing labels are replaced if only new ones are provided; otherwise, labels are appended.

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
* **Request Body:** Array of objects, each specifying `from`, `to` record IDs and `associationTypeId`, `category` of the label to remove.


#### E. Report on High Association Usage

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/usage/high-usage-report/{userId}`
* **Parameters:** `userId`: The ID of the user to receive the report.

### II. Association Schema Endpoints

#### A. Create and Manage Association Types

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:**
    * `name`: Internal name (no hyphens, cannot start with a number).
    * `label`: Display name.
    * `inverseLabel` (optional, for paired labels): Inverse label name.

#### B. Retrieve Association Labels

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`

#### C. Update Association Labels

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:**  `associationTypeId` and updated `label` (and optionally `inverseLabel`).

#### D. Delete Association Labels

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`


#### E. Set and Manage Association Limits

**1. Create or Update Association Limits:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (create) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (update)
* **Request Body:** Array of objects, each with `category`, `typeId`, and `maxToObjectIds`.

**2. Retrieve Association Limits:**

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/all` (all limits) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (specific objects).

**3. Delete Association Limits:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
* **Request Body:** Array of objects, each with `category` and `typeId`.


## Object Type IDs

A comprehensive list of `objectTypeId` values is provided in the original document (too extensive to reproduce here).  This list includes IDs for contacts, companies, deals, tickets, and other objects, as well as HubSpot-defined association types (Primary, Unlabeled) and their corresponding IDs.  Remember that custom objects and labels will have unique `typeId` values.



## Response Codes and Examples

The original document provides extensive examples of request bodies and response structures for each endpoint.  These examples illustrate how to format requests and interpret the returned data, including details like `category`, `typeId`, and `label` fields.  Refer to the original document for specific code snippets.


## Limitations

* **Daily Limits:**  Vary by HubSpot subscription (Professional/Enterprise: 500,000; API limit increase: 1,000,000).
* **Burst Limits:** Vary by HubSpot subscription (Free/Starter: 100 requests/10 seconds; Professional/Enterprise: 150 requests/10 seconds; API limit increase: 200 requests/10 seconds).
* **Association Limits:**  The maximum number of associations per record depends on the object and your HubSpot subscription.

Remember to consult the HubSpot developer documentation for the most up-to-date information and details on error handling.
