# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 for managing record associations.  Associations represent relationships between objects (e.g., Contact to Company) and activities within the HubSpot CRM.  This version includes both association endpoints (for creating, editing, and deleting associations) and association schema endpoints (for managing association definitions, labels, and limits).  Requires HubSpot NodeJS Client Version 9.0.0 or later.

## I. Association Endpoints

These endpoints handle the creation, modification, and deletion of associations between records.  The number of associations a record can have depends on the object type and your HubSpot subscription.

### A. Associate Records

#### 1. Associate Records Without a Label

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Parameters:**
    * `fromObjectType`: ID of the source object (e.g., `contact`, `company`).  See [Object Type IDs](#association-type-id-values) for a complete list.
    * `fromObjectId`: ID of the source record.
    * `toObjectType`: ID of the target object.
    * `toObjectId`: ID of the target record.
* **Example:** Associate contact (ID 12345) with company (ID 67891):
    ```
    PUT /crm/v4/objects/contact/12345/associations/default/company/67891
    ```

#### 2. Bulk Associate Records Without a Label

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
* **Request Body:** Array of `objectId` values for records to associate.
    ```json
    [12345, 67890, 98765]
    ```

#### 3. Associate Records With a Label

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body:** Array of objects, each specifying an association label.
    ```json
    [
      {
        "associationCategory": "USER_DEFINED",
        "associationTypeId": 36
      }
    ]
    ```
    * `associationCategory`:  `"HUBSPOT_DEFINED"` (default label) or `"USER_DEFINED"` (custom label).
    * `associationTypeId`: Numerical ID of the label.  Obtain this via the `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels` endpoint.
* **Example:** Associate contact (ID 12345) with deal (ID 21678228008) using custom label (ID 36).  Requires prior retrieval of `associationTypeId` using the GET labels endpoint.
    ```
    PUT /crm/v4/objects/contact/12345/associations/deal/21678228008
    ```
* **Response:**
    ```json
    {
      "fromObjectTypeId": "0-1",
      "fromObjectId": 29851,
      "toObjectTypeId": "0-3",
      "toObjectId": 21678228008,
      "labels": ["Point of contact"]
    }
    ```

#### 4. Bulk Create Labelled Associations

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`
* **Request Body:** Array of objects, each specifying a labelled association (includes `fromObjectId`, `toObjectId`, `associationCategory`, and `associationTypeId`).

### B. Retrieve Associated Records

#### 1. Retrieve Individual Record's Associations

* **Method:** `GET`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`
* **Parameters:**
    * `fromObjectType`: Source object ID.
    * `objectId`: Source record ID.
    * `toObjectType`: Target object ID.

#### 2. Bulk Retrieve Associated Records

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Request Body:** Array of `id` values for records whose associated records are to be retrieved.
    ```json
    {
      "inputs": [
        {"id": "33451"},
        {"id": "29851"}
      ]
    }
    ```

### C. Update Record Association Labels

Use the same endpoints as for creating labelled associations (`PUT` and `POST` batch endpoints). To replace existing labels, only include the new label in the request. To append labels, include all labels in the request.


### D. Remove Record Associations

#### 1. Remove All Associations Between Two Records

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}/{toObjectId}`

#### 2. Bulk Remove All Associations

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`
* **Request Body:**  Array of objects, each specifying the source and target records.

#### 3. Remove Specific Association Labels

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
* **Request Body:** Array of objects, each specifying the association to remove (including `fromObjectId`, `toObjectId`, `associationTypeId`, and `category`).


## II. Association Schema Endpoints

These endpoints manage association definitions (types), labels, and limits.

### A. Understand Association Definitions, Configurations, and Labels

These endpoints allow for the management of association types and their configurations.

### B. HubSpot Defined Associations

HubSpot provides predefined association types, including "Primary" and "Unlabeled".  "Primary" indicates the main association. "Unlabeled" indicates an association without a specific label.


### C. Custom Association Labels

Allows for creating custom labels to provide additional context for record relationships.

#### 1. Create Association Labels

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:**
    * `name`: Internal name (no hyphens, cannot start with a number).
    * `label`: Display name.
    * `inverseLabel` (optional): For paired labels.
* **Example (Single Label):**
    ```json
    {
      "label": "Partner",
      "name": "partner"
    }
    ```
* **Example (Paired Label):**
    ```json
    {
      "label": "Manager",
      "inverseLabel": "Employee",
      "name": "manager_employee"
    }
    ```

#### 2. Retrieve Association Labels

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Response:** Array of objects, each containing `category`, `typeId`, and `label`.

#### 3. Update Association Labels

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:**  `associationTypeId` and updated `label` (and optionally `inverseLabel`).

#### 4. Delete Association Labels

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`


### D. Set and Manage Association Limits

#### 1. Create or Update Association Limits

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (create) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (update)
* **Request Body:** Array of objects, each specifying limit details:  `category`, `typeId`, `maxToObjectIds`.

#### 2. Retrieve Association Limits

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/all` (all limits) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (limits between specific objects).

#### 3. Delete Association Limits

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
* **Request Body:** Array of objects, each specifying the `category` and `typeId` of the limit to delete.


## III. Report on High Association Usage

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/usage/high-usage-report/{userId}`
* **Parameters:** `userId`: ID of the user to receive the report.  Obtain this using the HubSpot Users API.


## IV. Limitations

* **Daily Limits:**  Vary by subscription level (Professional/Enterprise: 500,000; with API limit increase: 1,000,000).
* **Burst Limits:** Vary by subscription level (Free/Starter: 100 requests/10 seconds; Professional/Enterprise: 150 requests/10 seconds; with API limit increase: 200 requests/10 seconds).


## V. Association Type ID Values

See the provided tables in the original text for a list of HubSpot-defined `associationTypeId` values.  Custom object and label types will have unique IDs.


## VI. Legacy v1 Associations API

The original text also includes a table of IDs for the legacy v1 Associations API.  This is provided for reference purposes only if you are still using the older API.  Migration to v4 is recommended.
