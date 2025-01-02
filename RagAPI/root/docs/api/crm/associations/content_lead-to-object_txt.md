# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 for managing associations between records.  Associations represent relationships between different objects (e.g., Contact to Company) or within the same object (e.g., Company to Company).  This API comprises two main endpoint categories:  **Association endpoints** (for creating, editing, and removing associations) and **Association schema endpoints** (for managing association definitions, labels, and limits).

**Note:** The v4 Associations API requires HubSpot NodeJS Client version 9.0.0 or later.  The number of associations a record can have depends on the object type and your HubSpot subscription.

## I. Association Endpoints

These endpoints manage the associations between records.

### A. Associate Records

#### 1. Associate Records Without a Label

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Parameters:**
    * `fromObjectType`: ID of the source object (e.g., `contact`, `company`).  See [Object Type IDs](#object-type-ids).
    * `fromObjectId`: ID of the source record.
    * `toObjectType`: ID of the target object. See [Object Type IDs](#object-type-ids).
    * `toObjectId`: ID of the target record.
* **Example:** Associate contact (ID 12345) with company (ID 67891):
    `PUT /crm/v4/objects/contact/12345/associations/default/company/67891`

#### 2. Bulk Associate Records Without a Label

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
* **Request Body:** Array of `objectId` values for records to associate.
* **Example:** Associate multiple contacts with companies (IDs in the request body).

#### 3. Associate Records With a Label

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body:** Array of objects, each with:
    * `associationCategory`: `"HUBSPOT_DEFINED"` or `"USER_DEFINED"`.
    * `associationTypeId`: Numeric ID of the label. See [Default Type IDs](#default-type-ids) or retrieve custom label IDs using `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`.
* **Example:** Associate contact with deal using custom label (ID 36):

    `PUT /crm/v4/objects/contact/{objectId}/associations/deal/{toObjectId}`
    ```json
    [
      {
        "associationCategory": "USER_DEFINED",
        "associationTypeId": 36
      }
    ]
    ```
    **Response Example:**
    ```json
    {
      "fromObjectTypeId": "0-1",
      "fromObjectId": 29851,
      "toObjectTypeId": "0-3",
      "toObjectId": 21678228008,
      "labels": ["Point of contact"]
    }
    ```

#### 4. Bulk Create Labeled Associations

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`
* **Request Body:**  Array of associations, each with `id` values of records and label details (`associationCategory`, `associationTypeId`).


### B. Retrieve Associated Records

#### 1. Retrieve Individual Record's Associations

* **Method:** `GET`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`
* **Parameters:**
    * `fromObjectType`: ID of the source object.
    * `objectId`: ID of the source record.
    * `toObjectType`: ID of the target object.

#### 2. Bulk Retrieve Associated Records

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Request Body:** Array of `id` values for records whose associations need to be retrieved.
* **Example Request:**
    ```json
    {
      "inputs": [
        {"id": "33451"},
        {"id": "29851"}
      ]
    }
    ```
* **Example Response (Illustrative):**  See example in the original text.


### C. Update Record Association Labels

Use the bulk create endpoints (`/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`) to update existing associations. To replace, only include the new label. To append, include both old and new.

### D. Remove Record Associations

#### 1. Remove All Associations

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`

#### 2. Bulk Remove All Associations

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`
* **Request Body:** Array of objects, each specifying `from` and `to` record IDs.

#### 3. Remove Specific Association Labels

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
* **Request Body:** Array of objects, each specifying `from`, `to` record IDs, and the `associationTypeId` and `category` of the label to remove.


### E. Report on High Association Usage

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/usage/high-usage-report/{userId}`
* **Parameter:** `userId`: ID of the user to receive the report.  The report is emailed to this user.


## II. Association Schema Endpoints

These endpoints manage association definitions, labels, and limits.

### A. Understand Association Definitions, Configurations, and Labels

This section explains HubSpot-defined and custom association labels.  It covers the creation and management of association types.

### B. HubSpot Defined Associations

* **Primary:** The main association; used in HubSpot tools.
* **Unlabeled:** A default association; always returned in responses with `label: null`.


### C. Custom Association Labels

You can create single or paired labels.

### D. Create and Manage Association Types

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:**
    * `name`: Internal name (no hyphens, doesn't start with a number).
    * `label`: Display name.
    * `inverseLabel` (for paired labels only): Second label in the pair.
* **Example Request (Single Label):**
    ```json
    {
      "label": "Partner",
      "name": "partner"
    }
    ```
* **Example Request (Paired Labels):**
    ```json
    {
      "label": "Manager",
      "inverseLabel": "Employee",
      "name": "manager_employee"
    }
    ```
* **Example Response:**
    ```json
    {
      "results": [
        {"category": "USER_DEFINED", "typeId": 145, "label": "Employee"},
        {"category": "USER_DEFINED", "typeId": 144, "label": "Manager"}
      ]
    }
    ```


### E. Retrieve Association Labels

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`


### F. Update Association Labels

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:** `associationTypeId` and updated `label` (and optionally `inverseLabel`).

### G. Delete Association Labels

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`


### H. Set and Manage Association Limits

#### 1. Create or Update Association Limits

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (create) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (update)
* **Request Body:** Array of `inputs`, each with `category`, `typeId`, and `maxToObjectIds`.

#### 2. Retrieve Association Limits

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/all` (all limits) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (limits between specific objects).

#### 3. Delete Association Limits

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
* **Request Body:** Array of `inputs`, each with `category` and `typeId` of the limits to delete.


## III. Limitations

* **Daily Limits:**  500,000 requests (Professional and Enterprise;  1,000,000 with API limit increase, but this increase doesn't apply to associations).
* **Burst Limits:** 100 requests per 10 seconds (Free/Starter); 150 (Professional/Enterprise); 200 with API limit increase (but increase doesn't apply to associations).


## IV. Association Type ID Values

[See tables in the original text for a comprehensive list of `associationTypeId` values for various object combinations and association types.]


## V. v1 Associations (Legacy)

[See table in the original text for legacy v1 association type IDs.]


This markdown documentation provides a structured and detailed overview of the HubSpot CRM API v4 for associations.  Remember to consult the official HubSpot API documentation for the most up-to-date information and potential changes.
