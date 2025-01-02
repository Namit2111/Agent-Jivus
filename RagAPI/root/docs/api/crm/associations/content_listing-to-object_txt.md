# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 for managing record associations.  Associations represent relationships between records in the HubSpot CRM, allowing connections between different object types (e.g., Contact to Company) or within the same object type (e.g., Company to Company).  This version improves upon v3 with enhanced functionality and efficiency.

## API Endpoints

The v4 Associations API is divided into two main categories:

**1. Association Endpoints:**  Create, update, and delete associations between records.

**2. Association Schema Endpoints:** Manage association definitions (types), custom labels, and limits.

**Note:** The v4 API is supported by HubSpot's NodeJS client v9.0.0 and later. The number of associations a record can have depends on the object type and your HubSpot subscription.


## Association Endpoints

### Associate Records

**a) Associate Records Without a Label:**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Parameters:**
    * `fromObjectType`: ID of the source object (e.g., `contact`, `company`).  See "Association type ID values" section for a complete list.
    * `fromObjectId`: ID of the source record.
    * `toObjectType`: ID of the target object.
    * `toObjectId`: ID of the target record.
* **Example:** Associate contact (ID 12345) with company (ID 67891):
    `PUT /crm/v4/objects/contact/12345/associations/default/company/67891`

* **Bulk Association (Without Label):**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
    * **Request Body:**  An array of `objectId` values to associate.


**b) Associate Records With a Label:**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body:** An array of objects, each with:
    * `associationCategory`: `"HUBSPOT_DEFINED"` (default) or `"USER_DEFINED"` (custom).
    * `associationTypeId`: Numeric ID of the label (see "Association type ID values" and "Retrieve Association Labels").
* **Example:** Associate contact (ID 12345) with deal (ID 67891) using custom label (typeId: 36):
    `PUT /crm/v4/objects/contact/12345/associations/deal/67891`
    ```json
    [
      {
        "associationCategory": "USER_DEFINED",
        "associationTypeId": 36
      }
    ]
    ```
* **Bulk Association (With Label):**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`
    * **Request Body:** Array of association objects, each specifying `fromObjectId`, `toObjectId`, `associationCategory`, and `associationTypeId`.


### Retrieve Associated Records

**a) Retrieve Individual Record Associations:**

* **Method:** `GET`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`

**b) Retrieve Associated Records in Bulk:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Request Body:** Array of `id` values for records to retrieve associations for.
* **Example Request:**
    ```json
    {
      "inputs": [
        {"id": "33451"},
        {"id": "29851"}
      ]
    }
    ```
* **Example Response:** (See example in the original text)


### Update Record Association Labels

* Uses the same endpoints as creating associations (`PUT` or `POST` batch). To replace labels, include only the new label(s). To append, include all labels.


### Remove Record Associations

**a) Remove All Associations:**

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
* **Bulk Removal:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`
    * **Request Body:** Array of `{from: {id: ...}, to: [{id: ...}]}` objects.

**b) Remove Specific Association Labels:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
* **Request Body:** Array of objects, each with `types` (array of `{associationCategory, associationTypeId}`), `from`, and `to` (objects with `id`).


## Association Schema Endpoints

### Understand Association Definitions, Configurations, and Labels

This section details managing association types, custom labels, and limits using schema endpoints.

### HubSpot Defined Associations

* **Primary:** The main association (used in lists and workflows).
* **Unlabeled:** A default association with `label: null`.


### Custom Association Labels

Allows creating single or paired labels to further define relationships.

### Create and Manage Association Types

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:**
    * `name`: Internal name (no hyphens, cannot start with a number).
    * `label`: Display name.
    * `inverseLabel` (paired labels only): Second label in the pair.


### Retrieve Association Labels

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`


### Update Association Labels

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:**  `associationTypeId` and updated `label` (and `inverseLabel` for paired labels).


### Delete Association Labels

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`


### Set and Manage Association Limits

* **Create/Update Limits:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (create) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (update)
    * **Request Body:** Array of `{category, typeId, maxToObjectIds}` objects.
* **Retrieve Limits:**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/all` (all limits) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (specific objects)
* **Delete Limits:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
    * **Request Body:** Array of `{category, typeId}` objects to delete.


## Report on High Association Usage

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/usage/high-usage-report/{userId}`
* Sends a report of records nearing or exceeding association limits to the specified user's email.


## Limitations

* **Daily Limits:** 500,000 requests (Professional and Enterprise; can be increased with API limit increase, but not for association requests).
* **Burst Limits:** 100 requests/10 seconds (Free and Starter), 150 requests/10 seconds (Professional and Enterprise; can be increased with API limit increase, but not for association requests).


## Association Type ID Values

(See extensive tables in the original text providing `typeId` values for various object and association types.)


## v1 Associations (Legacy)

(See table in the original text for legacy v1 `typeId` values.)


This markdown documentation provides a comprehensive overview of the HubSpot CRM API v4 for associations. Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
