# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 for managing associations between records.  Associations represent relationships between different objects (e.g., Contact to Company) or within the same object (e.g., Company to Company).  This API includes endpoints for managing associations and their schemas.

**Note:** This API is supported in HubSpot NodeJS Client version 9.0.0 or later. The number of associations a record can have depends on the object and your HubSpot subscription.


## I. Association Endpoints

These endpoints create, edit, and remove associations between records.

### A. Associate Records

**1. Without a Label (Default Association):**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Parameters:**
    * `fromObjectType`: ID of the object being associated (e.g., `contact`, `company`). See [Object Type IDs](#object-type-ids)
    * `fromObjectId`: ID of the record being associated.
    * `toObjectType`: ID of the object the record is being associated *to*. See [Object Type IDs](#object-type-ids)
    * `toObjectId`: ID of the record being associated *to*.
* **Example:** Associate contact (ID 12345) with company (ID 67891):
    `PUT /crm/v4/objects/contact/12345/associations/default/company/67891`

* **Bulk Association:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
    * **Request Body:** Array of `objectId` values to associate.


**2. With a Label:**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body:** Array of objects, each with:
    * `associationCategory`: `"HUBSPOT_DEFINED"` or `"USER_DEFINED"`.
    * `associationTypeId`: Numeric ID of the label.  Obtain this via `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels` (see [Retrieve Association Labels](#retrieve-association-labels)).
* **Example:** Associate contact with deal using custom label (typeId 36):
    1. `GET /crm/v4/associations/contact/deal/labels` (to get `typeId`)
    2. `PUT /crm/v4/objects/contact/{objectId}/associations/deal/{toObjectId}`
       ```json
       [{"associationCategory": "USER_DEFINED", "associationTypeId": 36}]
       ```
* **Bulk Labeled Association:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`
    * **Request Body:**  Array of association objects. Each object includes `fromObjectId`, `toObjectId` and the label information (`associationCategory`, `associationTypeId`).

### B. Retrieve Associated Records

* **Individual Record:**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`
* **Batch:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
    * **Request Body:**  Array of `id` values for records.
* **Example Batch Request:** Retrieve companies associated with contacts (ID 33451 and 29851)
    ```json
    POST /crm/v4/associations/contacts/companies/batch/read
    {
      "inputs": [{"id": "33451"}, {"id": "29851"}]
    }
    ```


### C. Update Record Association Labels

Use the `PUT` (single) or `POST` (bulk) association endpoints. To replace existing labels, provide only the new labels. To append, include both old and new labels.

### D. Remove Record Associations

**1. Remove All Associations:**

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
* **Bulk Removal:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`
    * **Request Body:** Array of `{from: {id: ...}, to: [{id: ...}]}` objects.

**2. Remove Specific Association Labels:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
* **Request Body:** Array of objects, each with: `types` (array of `{associationCategory, associationTypeId}`), `from: {id: ...}`, and `to: {id: ...}`.


## II. Association Schema Endpoints

These endpoints manage association definitions (types), custom labels, and limits.


### A. Create and Manage Association Types

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:**
    * `name`: Internal name (no hyphens, doesn't start with number).
    * `label`: Display name.
    * `inverseLabel` (optional): For paired labels.

### B. Retrieve Association Labels

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`

### C. Update Association Labels

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:** `associationTypeId` and updated `label` (and `inverseLabel` if paired).

### D. Delete Association Labels

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`

### E. Set and Manage Association Limits

* **Create/Update Limits:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (create) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (update)
    * **Request Body:** `inputs`: array of `{category, typeId, maxToObjectIds}`.
* **Retrieve Limits:**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/all` (all limits) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (specific objects).
* **Delete Limits:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
    * **Request Body:** `inputs`: array of `{category, typeId}`.

## III.  High Association Usage Report

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/usage/high-usage-report/{userId}`
* This sends a report (records at or above 80% of their association limit) to the specified user's email.


## IV. Object Type IDs

[This section would contain a table summarizing object type IDs. The provided text only references a list of these IDs, but doesn't provide the list itself.  This needs to be added from the HubSpot documentation.]


## V. Limitations

* **Daily Limits:** 500,000 requests (Professional & Enterprise);  1,000,000 with API limit increase (but not increased for association API).
* **Burst Limits:** 100 requests/10 seconds (Free & Starter); 150 requests/10 seconds (Professional & Enterprise); 200 requests/10 seconds with API limit increase (but not increased for association API).


This documentation provides a comprehensive overview of the HubSpot CRM API v4 for associations.  Remember to consult the official HubSpot API documentation for the most up-to-date information and detailed specifications.
