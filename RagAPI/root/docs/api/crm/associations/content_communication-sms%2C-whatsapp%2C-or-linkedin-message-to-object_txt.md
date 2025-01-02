# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 for managing associations between records.  Associations represent relationships between different objects (e.g., Contact to Company) or within the same object (e.g., Company to Company).  This API includes endpoints for managing associations and their schemas.

**Note:** This API requires HubSpot NodeJS Client version 9.0.0 or later. The number of associations a record can have depends on the object and your HubSpot subscription.


## I. Association Endpoints

These endpoints allow you to create, update, and delete associations between records.

### A. Associate Records

#### 1. Associate Records Without a Label

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Parameters:**
    * `fromObjectType`: Object ID of the source record (e.g., `contact`, `company`). See [Object Type IDs](#object-type-ids).
    * `fromObjectId`: ID of the source record.
    * `toObjectType`: Object ID of the target record.
    * `toObjectId`: ID of the target record.
* **Example:** Associate contact (ID 12345) with company (ID 67891):
    ```
    PUT /crm/v4/objects/contact/12345/associations/default/company/67891
    ```

#### 2. Bulk Associate Records Without a Label

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
* **Request Body:** Array of `objectId` values for records to associate.
* **Example:**
    ```json
    POST /crm/v4/associations/contact/company/batch/associate/default
    {
      "objectIds": ["12345", "67890"]
    }
    ```

#### 3. Associate Records With a Label

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body:** Array of objects, each with:
    * `associationCategory`: `"HUBSPOT_DEFINED"` (default) or `"USER_DEFINED"` (custom).
    * `associationTypeId`: Numeric ID of the label.  Get this from the [Association Schema Endpoints](#association-schema-endpoints).
* **Example:** Associate contact (ID 12345) with deal (ID 67891) using custom label (ID 36):
    ```json
    PUT /crm/v4/objects/contact/12345/associations/deal/67891
    [
      {
        "associationCategory": "USER_DEFINED",
        "associationTypeId": 36
      }
    ]
    ```
    **Example Response:**
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
* **Request Body:** Array of association objects, including `id` values for records and label details (`associationCategory`, `associationTypeId`).

### B. Retrieve Associated Records

#### 1. Retrieve Individual Record Associations

* **Method:** `GET`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`

#### 2. Bulk Retrieve Associated Records

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Request Body:** Array of `id` values for records.
* **Example:** Retrieve companies associated with contacts (ID 33451 and 29851):
    ```json
    POST /crm/v4/associations/contact/company/batch/read
    {
      "inputs": [
        {"id": "33451"},
        {"id": "29851"}
      ]
    }
    ```
    **Example Response:**  (See detailed example in original document)


### C. Update Record Association Labels

Use the same endpoints as for creating labeled associations (`PUT` and `POST` batch endpoints) to update existing labels.  Include all desired labels in the request body; existing labels not included will be removed.

### D. Remove Record Associations

#### 1. Remove All Associations Between Two Records

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`

#### 2. Bulk Remove All Associations

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`
* **Request Body:** Array of objects, each with `from` and `to` objects containing record IDs.

#### 3. Remove Specific Association Labels

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
* **Request Body:** Array of objects, each with `from`, `to`, and `types` (array of `associationCategory` and `associationTypeId` to remove).


### E. High Association Usage Report

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/usage/high-usage-report/{userId}`
* **Description:**  Generates a report of records nearing or exceeding association limits. Sent via email to the specified user.


## II. Association Schema Endpoints

These endpoints manage association definitions (types) and labels.

### A. HubSpot Defined Associations

HubSpot provides predefined association types, including "Primary" and "Unlabeled".  See [Object Type IDs](#object-type-ids) for default `typeId` values.

### B. Custom Association Labels

#### 1. Create Association Labels

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:**
    * `name`: Internal name (no hyphens, no leading number).
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

#### 3. Update Association Labels

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:** `associationTypeId` and updated `label` (and optionally `inverseLabel`).

#### 4. Delete Association Labels

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`


### C. Association Limits

#### 1. Create or Update Association Limits

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (create) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (update)
* **Request Body:** Array of `inputs`, each with:
    * `category`: `"HUBSPOT_DEFINED"` or `"USER_DEFINED"`.
    * `typeId`: Numeric ID of the association type.
    * `maxToObjectIds`: Maximum number of associations allowed.

#### 2. Retrieve Association Limits

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/all` (all limits) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (limits between two objects).

#### 3. Delete Association Limits

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
* **Request Body:** Array of `inputs`, each with `category` and `typeId` of limits to delete.


## III. Object Type IDs

*(Detailed table of Object Type IDs provided in the original document)*


## IV. Limitations

* **Daily Limits:**  Vary by subscription (see original document).
* **Burst Limits:** Vary by subscription (see original document).


This markdown documentation provides a concise overview of the HubSpot CRM API v4 for Associations.  Refer to the original document for the complete table of `typeId` values and more detailed examples.
