# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 for managing record associations.  Associations represent relationships between different CRM objects (e.g., Contact to Company) or within the same object (e.g., Company to Company).  This API comprises two main endpoint types: *Association endpoints* for creating, updating, and deleting associations, and *Association schema endpoints* for managing association definitions, labels, and limits.

## I. Association Endpoints

These endpoints manage the associations themselves.

### A. Associate Records

**1. Without a Label:**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Parameters:**
    * `fromObjectType`: ID of the source object (e.g., `contact`, `company`).  See [Object Type IDs](#object-type-ids) for a complete list.
    * `fromObjectId`: ID of the source record.
    * `toObjectType`: ID of the target object.
    * `toObjectId`: ID of the target record.
* **Example:** Associate contact (ID 12345) with company (ID 67891):
    `PUT /crm/v4/objects/contact/12345/associations/default/company/67891`

* **Bulk Association (Without Label):**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
    * **Request Body:**  Array of `objectId` values to associate.


**2. With a Label:**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body:** Array of objects, each with:
    * `associationCategory`: `"HUBSPOT_DEFINED"` or `"USER_DEFINED"`
    * `associationTypeId`: Numeric ID of the label.  See [Association Type IDs](#object-type-ids) and [Retrieve Association Labels](#retrieve-association-labels).
* **Example:** Associate contact (ID 12345) with deal (ID 67891) using custom label (ID 36):
    `PUT /crm/v4/objects/contact/12345/associations/deal/67891`
    ```json
    [
      {
        "associationCategory": "USER_DEFINED",
        "associationTypeId": 36
      }
    ]
    ```
* **Bulk Labeled Association:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`
    * **Request Body:** Array of association objects, including `id` values of records and label parameters (`associationCategory`, `associationTypeId`).


### B. Retrieve Associated Records

**1. Individual Record:**

* **Method:** `GET`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`
* **Parameters:**
    * `fromObjectType`: ID of the source object.
    * `objectId`: ID of the source record.
    * `toObjectType`: ID of the target object.

**2. Batch Retrieval:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Request Body:** Array of `id` values of records to retrieve associations for.
* **Example:** Retrieve all company associations for contacts with IDs "33451" and "29851":
    ```json
    {
      "inputs": [
        {"id": "33451"},
        {"id": "29851"}
      ]
    }
    ```


### C. Update Record Association Labels

Use the same endpoints as for creating associations (`PUT` or `POST` batch endpoints) but include the updated labels in the request body.  To replace existing labels, only include the new labels.  To append labels, include both old and new.


### D. Remove Record Associations

**1. Remove All Associations:**

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`

* **Bulk Removal (All Associations):**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`
    * **Request Body:** Array of objects, each with `from` (containing `id`) and `to` (array of `id` objects).

**2. Remove Specific Association Labels:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
* **Request Body:** Array of objects, each with `from`, `to`, and `types` (array of objects with `associationCategory` and `associationTypeId`).


## II. Association Schema Endpoints

These endpoints manage the definitions, labels, and limits of associations.

### A. Understand Association Definitions, Configurations, and Labels

This section covers the management of association types, labels, and limits.  HubSpot provides predefined association types (e.g., "Primary" company association).  Admins can create custom association labels to add further context.

### B. Create and Manage Association Types

* **Create Association Labels:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
    * **Request Body:**
        * `name`: Internal name (no hyphens, doesn't start with a number).
        * `label`: Display name.
        * `inverseLabel` (optional, for paired labels):  Name of the inverse label.

### C. Retrieve Association Labels

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`

### D. Update Association Labels

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:**  `associationTypeId` and updated `label` (and optionally `inverseLabel`).


### E. Delete Association Labels

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`


### F. Set and Manage Association Limits

* **Create/Update Limits:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (create) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (update)
    * **Request Body:** Array of `inputs`, each with `category`, `typeId`, and `maxToObjectIds`.

* **Retrieve Limits:**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/all` (all limits) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (specific objects).

* **Delete Limits:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
    * **Request Body:** Array of `inputs`, each with `category` and `typeId`.



## III.  High Association Usage Report

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/usage/high-usage-report/{userID}`
* **Parameters:** `userID`: ID of the user to receive the report.


## IV.  Limitations

* **Daily Limits:** 500,000 requests (Professional and Enterprise, potentially higher with API limit increase).
* **Burst Limits:** 100 requests per 10 seconds (Free/Starter), 150 (Professional/Enterprise), potentially higher with API limit increase.


## V. Association Type ID Values

[See the extensive table in the original text for a complete list of `associationTypeId` values for various object combinations.]  This table shows predefined `typeId` values.  Custom object and label types will have unique `typeId` values which must be retrieved from the API or HubSpot settings.


## VI.  v1 Associations (Legacy)

[See the table in the original text for legacy v1 association type IDs.]


This markdown provides a comprehensive overview and examples for using the HubSpot CRM v4 Associations API. Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
