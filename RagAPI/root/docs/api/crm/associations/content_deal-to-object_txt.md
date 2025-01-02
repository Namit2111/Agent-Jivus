# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 for managing record associations.  Associations represent relationships between records in HubSpot, allowing you to link records of different or the same object types (e.g., Contact to Company, Company to Company).  This API provides endpoints for creating, managing, and querying these associations.

## API Endpoints Categories

The v4 Associations API is divided into two main categories:

* **Association Endpoints:** Create, update, and delete associations between records.
* **Association Schema Endpoints:** Manage association definitions (types), custom labels, and association limits.


##  I. Association Endpoints

These endpoints handle the creation and manipulation of associations between records.

### A. Associate Records

**1. Associate Records Without a Label:**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Parameters:**
    * `fromObjectType`: ID of the source object (e.g., `contact`, `company`).  See [Object Type IDs](#object-type-ids)
    * `fromObjectId`: ID of the source record.
    * `toObjectType`: ID of the target object. See [Object Type IDs](#object-type-ids)
    * `toObjectId`: ID of the target record.
* **Example:** Associate contact (ID 12345) with company (ID 67891):
    `PUT /crm/v4/objects/contact/12345/associations/default/company/67891`
* **Bulk Association (POST):** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`  Request body contains an array of `objectId` values.


**2. Associate Records With a Label:**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body:**  Array of objects, each containing:
    * `associationCategory`: `"HUBSPOT_DEFINED"` or `"USER_DEFINED"`.
    * `associationTypeId`: Numerical ID of the label (see [Retrieve Association Labels](#retrieve-association-labels)).
* **Example:** Associate contact with deal using custom label (ID 36):
    1. `GET /crm/v4/associations/contact/deal/labels` (Retrieve label ID)
    2. `PUT /crm/v4/objects/contact/{objectId}/associations/deal/{toObjectId}`
       ```json
       [
         {
           "associationCategory": "USER_DEFINED",
           "associationTypeId": 36
         }
       ]
       ```
* **Bulk Labeled Association (POST):** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create` Request body includes `id` values and label details.


### B. Retrieve Associated Records

**1. Retrieve Individual Record Associations:**

* **Method:** `GET`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`
* **Parameters:**
    * `fromObjectType`: Source object ID.
    * `objectId`: Source record ID.
    * `toObjectType`: Target object ID.

**2. Retrieve Associated Records in Bulk:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Request Body:** Array of objects, each containing the `id` of the records to retrieve associations for.
* **Example:** Retrieve company associations for contacts with IDs "33451" and "29851":
  ```json
  {
    "inputs": [
      {"id": "33451"},
      {"id": "29851"}
    ]
  }
  ```

### C. Update Record Association Labels

* Use the same endpoints as creating associations (`PUT` or `POST`) and include the new label(s) in the request body.  Existing labels are replaced or appended depending on the request.


### D. Remove Record Associations

**1. Remove All Associations:**

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
* **Bulk Removal (POST):** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive` Request body contains an array of objects specifying `from` and `to` records.

**2. Remove Specific Association Labels:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
* **Request Body:** Array of objects, each specifying `from`, `to` record IDs and the `associationTypeId` and `category` of the label to remove.


## II. Association Schema Endpoints

These endpoints manage association definitions, configurations, and labels.

### A. Understand Association Definitions, Configurations, and Labels

This section covers HubSpot-defined and custom association labels, along with managing association types and limits.

### B. Create and Manage Association Types

* **Create Association Labels:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
    * **Request Body:**
        * `name`: Internal name (no hyphens, no leading numbers).
        * `label`: Display name.
        * `inverseLabel` (optional, for paired labels): Second label in the pair.
* **Retrieve Association Labels:**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Update Association Labels:**
    * **Method:** `PUT`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
    * **Request Body:** `associationTypeId` and updated `label` (and `inverseLabel` if applicable).
* **Delete Association Labels:**
    * **Method:** `DELETE`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`

### C. Set and Manage Association Limits

* **Create or Update Association Limits:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (create) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (update)
    * **Request Body:** Array of objects, each containing:
        * `category`: `"HUBSPOT_DEFINED"` or `"USER_DEFINED"`.
        * `typeId`: Association type ID.
        * `maxToObjectIds`: Maximum number of associations allowed.
* **Retrieve Association Limits:**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/all` (all limits) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (specific objects)
* **Delete Association Limits:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
    * **Request Body:** Array of objects, each specifying the `category` and `typeId` of the limit to remove.

### D. Report on High Association Usage

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/usage/high-usage-report/{userId}`
* **Parameters:** `userId`: ID of the user to receive the report.


## III. Object Type IDs

A list of `objectTypeId` values is required for many API calls. While some common objects allow using the object name (e.g., `contact`, `company`), it's recommended to always refer to the official documentation for the most up-to-date list. The provided text includes extensive tables of example `typeId` values.


## IV. Limitations

* **Daily Limits:** Vary by subscription tier (Professional/Enterprise: 500,000; with API limit increase: 1,000,000).
* **Burst Limits:** Vary by subscription tier (Free/Starter: 100 requests/10 seconds; Professional/Enterprise: 150 requests/10 seconds; with API limit increase: 200 requests/10 seconds).


This markdown documentation provides a comprehensive overview of the HubSpot CRM API v4 for Associations. Remember to consult the official HubSpot API documentation for the most accurate and up-to-date information, including detailed error handling and further examples.
