# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 for managing associations between records.  Associations represent relationships between different objects (e.g., Contact to Company) or within the same object (e.g., Company to Company).  This API offers both association endpoints (create, edit, remove) and association schema endpoints (manage definitions, labels, limits).  Requires HubSpot NodeJS Client Version 9.0.0 or later.

## I. Association Endpoints

These endpoints handle the creation, modification, and deletion of associations between records.  The number of associations allowed per record depends on the object type and your HubSpot subscription.

### A. Associate Records

**1. Without a Label (Default Association):**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Parameters:**
    * `fromObjectType`: ID of the source object (e.g., `contact`, `company`).  See [Object Type IDs](#object-type-ids).
    * `fromObjectId`: ID of the source record.
    * `toObjectType`: ID of the target object.
    * `toObjectId`: ID of the target record.
* **Example:** Associate contact (ID 12345) with company (ID 67891):
    `PUT /crm/v4/objects/contact/12345/associations/default/company/67891`

* **Bulk Association:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
    * **Request Body:** Array of `objectId` values for records to associate.


**2. With a Label:**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body:** Array of objects, each with:
    * `associationCategory`:  `"HUBSPOT_DEFINED"` (default) or `"USER_DEFINED"` (custom).
    * `associationTypeId`: Numeric ID of the label.  See [Association Type IDs](#association-type-ids) and how to [Retrieve Association Labels](#retrieve-association-labels).
* **Example:** Associate contact with deal using custom label (ID 36):
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
    * **Request Body:** Array of association objects including `objectId` values and label details.


### B. Retrieve Associated Records

**1. Individual Record:**

* **Method:** `GET`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`
* **Parameters:**
    * `fromObjectType`: Source object ID.
    * `objectId`: Source record ID.
    * `toObjectType`: Target object ID.

**2. Batch Retrieval:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Request Body:**  Array of `{ "id": "recordId" }` objects.
* **Example Request:**
    ```json
    {
      "inputs": [
        { "id": "33451" },
        { "id": "29851" }
      ]
    }
    ```
* **Example Response:**  Includes `toObjectId`, `associationTypes` (with `category`, `typeId`, `label`).


### C. Update Record Association Labels

Use the same endpoints as associating records (`PUT` or `POST` batch) to update labels.  To replace an existing label, only provide the new label. To append, include all desired labels.


### D. Remove Record Associations

**1. Remove All Associations:**

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
* **Bulk Removal:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`
    * **Request Body:**  Array of `{ "from": { "id": "..." }, "to": [ { "id": "..." } ] }` objects.


**2. Remove Specific Association Labels:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
* **Request Body:** Array of objects, each with:
    * `types`: Array of `{ "associationCategory": "...", "associationTypeId": ... }`
    * `from`: `{ "id": "..." }`
    * `to`: `{ "id": "..." }`


## II. Association Schema Endpoints

These endpoints manage association definitions, custom labels, and limits.


### A. Understand Association Definitions, Configurations, and Labels

This section describes managing association types (definitions) and their configurations and labels.


### B. HubSpot Defined Associations

HubSpot provides predefined associations like "Primary" and "Unlabeled".


### C. Custom Association Labels

Create custom labels to add context to associations.


### D. Create and Manage Association Types

* **Create Label:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
    * **Request Body:**
        * `name`: Internal name (no hyphens, no leading number).
        * `label`: Display name in HubSpot.
        * `inverseLabel` (optional, for paired labels):  Second label in the pair.

### E. Retrieve Association Labels

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Response:** Array of objects with `category`, `typeId`, and `label`.


### F. Update Association Labels

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:**  `associationTypeId` and updated `label` (and optionally `inverseLabel`).


### G. Delete Association Labels

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`


### H. Set and Manage Association Limits

* **Create/Update Limits:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (create) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (update)
    * **Request Body:**  Array of objects with `category`, `typeId`, `maxToObjectIds`.

* **Retrieve Limits:**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/all` (all limits) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (specific objects).

* **Delete Limits:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
    * **Request Body:** Array of `{ "category": "...", "typeId": ... }` objects.


## III. Report on High Association Usage

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/usage/high-usage-report/{userId}`
* **Parameters:** `userId`: ID of the user to receive the report.


## IV. Limitations

* **Daily Limits:**  Vary by subscription (500,000 for Professional and Enterprise; up to 1,000,000 with API limit increase).
* **Burst Limits:** Vary by subscription (100 requests/10 seconds for Free/Starter; 150 for Professional/Enterprise; up to 200 with API limit increase).


## V. Association Type ID Values

[See the extensive tables in the original text for detailed Object Type IDs and Association Type IDs.]

<br>

**(Note:  The original text contained extensive tables listing `typeId` values for various object combinations.  Those tables have been omitted for brevity but are crucial for practical use of the API and are readily available in the original documentation.)**
