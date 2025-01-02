# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 for managing associations between records.  Associations represent relationships between different CRM objects (e.g., Contact to Company) or within the same object (e.g., Company to Company). This version builds upon v3 and adds significant improvements.  For v3 documentation, see [v3 Associations API](link_to_v3_docs).

**Note:** The v4 Associations API is supported in HubSpot NodeJS Client version 9.0.0 or later.

## API Endpoints Categories

The v4 API is divided into two categories of endpoints:

* **Association Endpoints:** Create, update, and delete associations between records.
* **Association Schema Endpoints:** Manage association definitions (types), custom labels, and association limits.


## I. Association Endpoints

These endpoints handle the creation, modification, and deletion of associations between records.  The number of associations a record can have is dependent on the object type and your HubSpot subscription.

### A. Associate Records

**1. Associate records without a label:**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Parameters:**
    * `fromObjectType`: ID of the source object (e.g., `contact`, `company`). See [Object Type IDs](#association-type-id-values) for a list.
    * `fromObjectId`: ID of the source record.
    * `toObjectType`: ID of the target object.
    * `toObjectId`: ID of the target record.
* **Example:** Associate contact (ID 12345) with company (ID 67891):
    ```
    PUT /crm/v4/objects/contact/12345/associations/default/company/67891
    ```

* **Bulk Association (without labels):**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
    * **Request Body:**  An array of `objectId` values to associate.


**2. Associate records with a label:**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body:** An array of objects, each containing:
    * `associationCategory`: `"HUBSPOT_DEFINED"` (default) or `"USER_DEFINED"` (custom).
    * `associationTypeId`:  Numeric ID of the association label.  Obtain this ID via the `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels` endpoint.
* **Example:** Associate contact (ID 12345) with deal (ID 67891) using custom label (typeId 36):
    ```
    PUT /crm/v4/objects/contact/12345/associations/deal/67891
    ```
    ```json
    [
      {
        "associationCategory": "USER_DEFINED",
        "associationTypeId": 36
      }
    ]
    ```
* **Example Response:**
    ```json
    {
      "fromObjectTypeId": "0-1",
      "fromObjectId": 29851,
      "toObjectTypeId": "0-3",
      "toObjectId": 21678228008,
      "labels": ["Point of contact"]
    }
    ```
* **Bulk Create (labelled associations):**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`
    * **Request Body:** An array of association objects including `fromObjectId`, `toObjectId`, `associationCategory`, and `associationTypeId`.

### B. Retrieve Associated Records

**1. Retrieve individual record's associations:**

* **Method:** `GET`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`
* **Parameters:**
    * `fromObjectType`: ID of the source object.
    * `objectId`: ID of the source record.
    * `toObjectType`: ID of the target object.

**2. Retrieve associated records in bulk:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Request Body:** An array of `id` values for the source records.
* **Example Request:**
    ```json
    {
      "inputs": [
        { "id": "33451" },
        { "id": "29851" }
      ]
    }
    ```
* **Example Response:** (See detailed example in original text)


### C. Update Record Association Labels

Update existing associations' labels using the bulk create endpoints.  To replace labels, only include the new label(s). To append, include both old and new labels.


### D. Remove Record Associations

**1. Remove all associations:**

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
* **Bulk Archive (all associations):**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`
    * **Request Body:**  An array defining the associations to remove.

**2. Remove specific association labels:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
* **Request Body:** An array of objects specifying the `id` values of associated records and the `associationTypeId` and `category` of the label(s) to remove.



## II. Association Schema Endpoints

These endpoints manage association definitions, labels, and limits.


### A. Understand Association Definitions, Configurations, and Labels

These endpoints allow management of association types (definitions), their configurations (limits), and labels.


### B. HubSpot Defined Associations

HubSpot provides predefined association types, including:

* `Primary`: The main association.
* `Unlabeled`: A default association with a `label` value of `null`.


### C. Custom Association Labels

Create custom labels to provide additional context to associations.  Labels can be:

* **Single:** One label for both records.
* **Paired:** Two labels, one for each record in the association (e.g., "Manager" and "Employee").


### D. Create and Manage Association Types

Use these endpoints to create, update, and delete custom association types.


### E. Create Association Labels

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:**
    * `name`: Internal name (no hyphens, no leading numbers).
    * `label`: Display name.
    * `inverseLabel` (for paired labels): Second label in the pair.
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
* **Example Response:**
    ```json
    {
      "results": [
        {
          "category": "USER_DEFINED",
          "typeId": 145,
          "label": "Employee"
        },
        {
          "category": "USER_DEFINED",
          "typeId": 144,
          "label": "Manager"
        }
      ]
    }
    ```

### F. Retrieve Association Labels

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Response:** An array of association types, including `category`, `typeId`, and `label`.

### G. Update Association Labels

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:** `associationTypeId` and updated `label` (and optionally `inverseLabel`).

### H. Delete Association Labels

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`

### I. Set and Manage Association Limits

These endpoints allow setting limits on the number of associations per association type.


### J. Create or Update Association Limits

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (create) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (update)
* **Request Body:**  Array of objects, each containing `category`, `typeId`, and `maxToObjectIds`.

### K. Retrieve Association Limits

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/all` (all limits) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (limits between specific objects)

### L. Delete Association Limits

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
* **Request Body:** Array of objects, each containing `category` and `typeId` of the limits to delete.


## III.  Limitations

* **Daily Limits:**  Vary by subscription (Professional/Enterprise: 500,000; with API limit increase: 1,000,000).
* **Burst Limits:** Vary by subscription (Free/Starter: 100 requests/10 seconds; Professional/Enterprise: 150 requests/10 seconds; with API limit increase: 200 requests/10 seconds).


## IV. Association Type ID Values

[Detailed tables of `associationTypeId` values for various object combinations are provided in the original text.  These tables are too extensive to reproduce here, but they are crucial for using the API effectively.]  Refer to the original document for these tables.

## V. Legacy v1 Associations API

[Information regarding the legacy v1 API is present in the original text and should be consulted if needed.]


This markdown documentation provides a comprehensive overview of the HubSpot CRM API v4 for associations. Remember to always refer to the official HubSpot documentation for the most up-to-date information and any potential changes.
