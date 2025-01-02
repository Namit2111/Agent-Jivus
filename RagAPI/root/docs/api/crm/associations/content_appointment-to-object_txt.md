# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 Associations endpoints.  This version supersedes the v3 API.  For v3 documentation, see [v3 Associations API](link_to_v3_docs).

**Overview:**

The Associations API v4 manages relationships between records in the HubSpot CRM.  These relationships can be between different object types (e.g., Contact to Company) or within the same object type (e.g., Company to Company).  The API consists of two main sections:

* **Association Endpoints:** Create, update, and delete associations between records.
* **Association Schema Endpoints:** Manage association definitions (types), custom labels, and association limits.

**Note:** The v4 Associations API requires HubSpot NodeJS Client version 9.0.0 or later.  The number of associations a record can have depends on the object type and your HubSpot subscription.

## I. Association Endpoints

These endpoints handle the creation, modification, and deletion of associations between records.

### A. Associate Records

**1. Associate Records Without a Label (Default Association):**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Parameters:**
    * `fromObjectType`: ID of the source object (e.g., `contact`, `company`). See [Object Type IDs](#object-type-ids)
    * `fromObjectId`: ID of the source record.
    * `toObjectType`: ID of the target object.
    * `toObjectId`: ID of the target record.
* **Example:** Associate contact (ID 12345) with company (ID 67891):
    `PUT /crm/v4/objects/contact/12345/associations/default/company/67891`

**2. Bulk Associate Records Without a Label:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
* **Request Body:** Array of `objectId` values for records to associate.
* **Example:** (Associating multiple records would require a JSON body with an array of IDs.)

**3. Associate Records With a Label:**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body:** Array of objects, each with:
    * `associationCategory`: `"HUBSPOT_DEFINED"` or `"USER_DEFINED"`
    * `associationTypeId`: Numeric ID of the label.  See [Association Type IDs](#object-type-ids) and [Retrieve Association Labels](#retrieve-association-labels)
* **Example:** (Associating a contact with a deal using a custom label with `associationTypeId` 36):
    `PUT /crm/v4/objects/contact/{objectId}/associations/deal/{toObjectId}`
    ```json
    [
      {
        "associationCategory": "USER_DEFINED",
        "associationTypeId": 36
      }
    ]
    ```
* **Response:** Includes `fromObjectTypeId`, `fromObjectId`, `toObjectTypeId`, `toObjectId`, and `labels`.

**4. Bulk Create Labeled Associations:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`
* **Request Body:**  Array of association objects, each specifying `fromObjectId`, `toObjectId`, `associationCategory`, and `associationTypeId`.

### B. Retrieve Associated Records

**1. Retrieve Individual Record's Associations:**

* **Method:** `GET`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`
* **Parameters:**
    * `fromObjectType`: ID of the source object.
    * `objectId`: ID of the source record.
    * `toObjectType`: ID of the target object.

**2. Bulk Retrieve Associated Records:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Request Body:** Array of `id` values for records.
* **Example:** Retrieve companies associated with contacts (ID 33451 and 29851):
    ```json
    {
      "inputs": [
        {"id": "33451"},
        {"id": "29851"}
      ]
    }
    ```
* **Response:** Includes `from`, `to` (array of associated records with `toObjectId` and `associationTypes`), `status`, `startedAt`, and `completedAt`.

### C. Update Record Association Labels

* Use the bulk create endpoints (`/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`) to update existing labels. To replace, only include the new label. To append, include both old and new labels.

### D. Remove Record Associations

**1. Remove All Associations:**

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`

**2. Bulk Remove All Associations:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`
* **Request Body:** Array of objects, each with `from` and `to` (containing `id`).

**3. Remove Specific Association Labels:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
* **Request Body:** Array of objects, each with `from`, `to`, and `types` (array of objects containing `associationCategory` and `associationTypeId`).


## II. Association Schema Endpoints

These endpoints manage association definitions, labels, and limits.

### A. Understand Association Definitions, Configurations, and Labels

This section covers managing association types, labels, and limits.  HubSpot provides predefined association types (e.g., unlabeled contact to company) and allows administrators to define custom labels.  Two predefined types are:

* **Primary:** The main association (used in lists and workflows).
* **Unlabeled:** A default association with `label: null`.

### B. Create and Manage Association Types

* Use the definitions endpoints to create and manage association types.

### C. Create Association Labels

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:**
    * `name`: Internal name (no hyphens, doesn't start with a number).
    * `label`: Display name.
    * `inverseLabel` (optional, for paired labels): Second label in the pair.
* **Response:** Returns `category` and `typeId` for the new label.

### D. Retrieve Association Labels

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Response:** Array of objects, each with `category`, `typeId`, and `label`.

### E. Update Association Labels

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:** `associationTypeId` and new `label` (and optionally `inverseLabel`).

### F. Delete Association Labels

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`

### G. Set and Manage Association Limits

* **Create/Update Limits:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (create) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (update)
    * **Request Body:** Array of objects, each with `category`, `typeId`, and `maxToObjectIds`.
* **Retrieve Limits:**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/all` (all limits) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (limits between specific objects).
* **Delete Limits:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
    * **Request Body:** Array of objects, each with `category` and `typeId`.


## III. Report on High Association Usage

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/usage/high-usage-report/{userId}`
* **Parameters:** `userId`: ID of the user to receive the report.


## IV. Limitations

* **Daily Limits:**  500,000 requests (Professional and Enterprise accounts).  1,000,000 requests with API limit increase (This increase does not apply to Association API).
* **Burst Limits:** 100 requests per 10 seconds (Free and Starter), 150 requests per 10 seconds (Professional and Enterprise). 200 requests per 10 seconds with API limit increase (This increase does not apply to Association API).


## V. Association Type ID Values

*(See the extensive table provided in the original text.  This table lists the `typeId` values for various HubSpot-defined association types between different objects.)*


## VI. v1 Associations (Legacy)

*(See the table provided in the original text for legacy v1 association type IDs.)*


This markdown provides a comprehensive overview of the HubSpot CRM API v4 Associations. Remember to replace placeholder values like `{objectId}`, `{fromObjectType}`, etc., with actual values.  Always refer to the official HubSpot API documentation for the most up-to-date information.
