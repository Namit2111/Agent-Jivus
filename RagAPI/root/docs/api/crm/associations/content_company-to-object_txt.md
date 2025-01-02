# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 Associations endpoints, allowing developers to manage relationships between records in the HubSpot CRM.  The API supports both creating and managing associations between different object types (e.g., Contact to Company) and within the same object type (e.g., Company to Company).  It uses both association endpoints (for creating, updating, and deleting associations) and association schema endpoints (for managing association definitions, labels, and limits).

**Note:** The v4 Associations API requires HubSpot NodeJS Client version 9.0.0 or later.  Association limits depend on the object type and your HubSpot subscription.


## I. Association Endpoints

These endpoints manage the associations themselves.

### A. Associate Records

#### 1. Associate Records Without a Label

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Parameters:**
    * `fromObjectType`: ID of the source object (e.g., `contact`, `company`). See [Object Type IDs](#object-type-ids).
    * `fromObjectId`: ID of the source record.
    * `toObjectType`: ID of the target object. See [Object Type IDs](#object-type-ids).
    * `toObjectId`: ID of the target record.
* **Example:** Associate contact (ID 12345) with company (ID 67891):
  `/crm/v4/objects/contact/12345/associations/default/company/67891`

#### 2. Bulk Associate Records Without a Label

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
* **Request Body:** Array of `objectId` values for records to associate.
* **Example Request Body:**
```json
[12345, 67890, 98765]
```

#### 3. Associate Records With a Label

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body:** Array of objects, each with:
    * `associationCategory`: `"HUBSPOT_DEFINED"` or `"USER_DEFINED"`.
    * `associationTypeId`: Numeric ID of the association label.  Retrieve this using the `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels` endpoint.
* **Example Request Body (using custom label with `associationTypeId` 36):**
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

#### 4. Bulk Create Labeled Associations

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`
* **Request Body:**  Array of objects, each specifying `fromObjectId`, `toObjectId`, `associationCategory`, and `associationTypeId`.


### B. Retrieve Associated Records

#### 1. Retrieve Individual Record Associations

* **Method:** `GET`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`

#### 2. Bulk Retrieve Associated Records

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Request Body:** Array of `id` values for records.
* **Example Request Body:**
```json
{
  "inputs": [
    {"id": "33451"},
    {"id": "29851"}
  ]
}
```
* **Example Response:** (See detailed example in original documentation)


### C. Update Record Association Labels

Use the same endpoints as for creating labeled associations (`PUT` or `POST` batch).  To replace labels, only include the new label(s) in the request.  To append, include all existing and new labels.

### D. Remove Record Associations

#### 1. Remove All Associations Between Two Records

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`

#### 2. Bulk Remove All Associations

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`
* **Request Body:** Array of objects, each specifying `from` (with `id`) and `to` (array of `id` values).

#### 3. Remove Specific Association Labels

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
* **Request Body:** Array of objects, each specifying `from` (with `id`), `to` (with `id`), and `types` (array of objects with `associationCategory` and `associationTypeId`).


## II. Association Schema Endpoints

These endpoints manage the definitions and configurations of associations.

### A. Understand Association Definitions, Configurations, and Labels

This section covers creating and managing custom association labels and setting association limits.

### B. HubSpot Defined Associations

HubSpot provides pre-defined association types (e.g., unlabeled Contact to Company, Primary Company).  These are documented in the [Object Type IDs](#object-type-ids) section.


### C. Custom Association Labels

#### 1. Create Association Labels

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:**
    * `name`: Internal name (no hyphens, no leading numbers).
    * `label`: Display name in HubSpot.
    * `inverseLabel` (optional, for paired labels): Display name for the inverse relationship.
* **Example Request Body (single label):**
```json
{
  "label": "Partner",
  "name": "partner"
}
```
* **Example Request Body (paired labels):**
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

#### 2. Retrieve Association Labels

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`

#### 3. Update Association Labels

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:** `associationTypeId` and new `label` (and `inverseLabel` if applicable).

#### 4. Delete Association Labels

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`


### D. Set and Manage Association Limits

#### 1. Create or Update Association Limits

* **Method:** `POST`
* **Endpoint:**
    * Create: `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create`
    * Update: `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update`
* **Request Body:** Array of `inputs`, each with `category`, `typeId`, and `maxToObjectIds`.

#### 2. Retrieve Association Limits

* **Method:** `GET`
* **Endpoint:**
    * All limits: `/crm/v4/associations/definitions/configurations/all`
    * Specific objects: `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}`

#### 3. Delete Association Limits

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
* **Request Body:** Array of `inputs`, each with `category` and `typeId`.


## III.  High Association Usage Report

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/usage/high-usage-report/{userId}`
* **Description:** Generates a report of records approaching or exceeding association limits. The report is emailed to the user specified by `userId`.


## IV. Object Type IDs

The following tables list HubSpot-defined `associationTypeId` values.  Custom objects and custom labels will have unique `typeId` values.

**(See tables in the original documentation for a complete list of `typeId` values for various object combinations.)**


## V. Limitations

* **Daily Limits:**  Vary by HubSpot subscription (Professional/Enterprise: 500,000; API limit increase: 1,000,000).
* **Burst Limits:** Vary by HubSpot subscription (Free/Starter: 100 requests/10 seconds; Professional/Enterprise: 150 requests/10 seconds; API limit increase: 200 requests/10 seconds).


This markdown documentation provides a comprehensive overview of the HubSpot CRM API v4 Associations.  Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
