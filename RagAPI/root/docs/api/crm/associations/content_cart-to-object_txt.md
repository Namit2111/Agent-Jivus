# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 for managing record associations.  Associations represent relationships between objects and activities in the HubSpot CRM.  They can be between different object types (e.g., Contact to Company) or within the same object type (e.g., Company to Company).

This API consists of two main endpoint categories:

* **Association endpoints:** Create, edit, and remove associations between records.
* **Association schema endpoints:** Manage association definitions (types), custom labels, and limits.


## I. Association Endpoints

These endpoints handle the creation, modification, and deletion of associations between records.  Association limits depend on the object type and your HubSpot subscription.

### A. Associate Records

**1. Associate Records Without a Label:**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Parameters:**
    * `fromObjectType`: ID of the object being associated (e.g., `contact`, `company`).  See [Object Type IDs](#association-type-id-values) for a list.
    * `fromObjectId`: ID of the record being associated.
    * `toObjectType`: ID of the object the record is being associated *to*.
    * `toObjectId`: ID of the record being associated *to*.
* **Example:** Associate contact (ID 12345) with company (ID 67891):
    ```bash
    PUT /crm/v4/objects/contact/12345/associations/default/company/67891
    ```

* **Bulk Association (Without Label):**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
    * **Request Body:** Array of `objectId` values to associate.


**2. Associate Records With a Label:**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body:** Array of objects, each with:
    * `associationCategory`: `"HUBSPOT_DEFINED"` (default) or `"USER_DEFINED"` (custom).
    * `associationTypeId`: Numeric ID of the label.  Obtain this from the [Association Schema Endpoints](#ii-association-schema-endpoints).
* **Example:** Associate a contact with a deal using a custom label (typeId: 36):

    1. **GET `/crm/v4/associations/contact/deal/labels`** to retrieve available labels.
    2. **PUT `/crm/v4/objects/contact/{objectId}/associations/deal/{toObjectId}`**
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
    * **Request Body:**  Similar to the single association, but handles multiple associations in a batch.


### B. Retrieve Associated Records

**1. Retrieve Individual Record Associations:**

* **Method:** `GET`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`
* **Parameters:**
    * `fromObjectType`: Object type of the record whose associations are being retrieved.
    * `objectId`: ID of the record.
    * `toObjectType`: Object type of the associated records.

**2. Retrieve Associated Records in Bulk:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Request Body:** Array of `id` values for records.


### C. Update Record Association Labels

Use the bulk create endpoints (`POST /crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`) to update existing labels.  To replace a label, only include the new label. To append labels, include all desired labels.

### D. Remove Record Associations

**1. Remove All Associations:**

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
* **Bulk Removal:** `POST /crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`

**2. Remove Specific Association Labels:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
* **Request Body:** Array of objects, each specifying the associated records and the `associationTypeId` and `category` of the label(s) to remove.


## II. Association Schema Endpoints

These endpoints manage association definitions, configurations, and labels.

### A. Understand Association Definitions, Configurations, and Labels

This section covers managing association types, creating/managing custom labels, and setting association limits.

### B. HubSpot Defined Associations

HubSpot provides predefined association types, including "Primary" and "Unlabeled."

### C. Custom Association Labels

You can create custom labels to provide additional context for record relationships (Single or Paired).

### D. Create and Manage Association Types

Use the definition endpoints to create, manage, and delete custom association types.


**1. Create Association Labels:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:**
    * `name`: Internal name (no hyphens, doesn't start with a number).
    * `label`: Display name.
    * `inverseLabel` (for paired labels): Second label in the pair.

**2. Retrieve Association Labels:**

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`

**3. Update Association Labels:**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`

**4. Delete Association Labels:**

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`


### E. Set and Manage Association Limits

**1. Create or Update Association Limits:**

* **Method:** `POST`
* **Endpoint:**
    * Create: `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create`
    * Update: `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update`
* **Request Body:** Array of objects, each specifying `category`, `typeId`, and `maxToObjectIds`.

**2. Retrieve Association Limits:**

* **Method:** `GET`
* **Endpoint:**
    * All limits: `/crm/v4/associations/definitions/configurations/all`
    * Specific objects: `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}`

**3. Delete Association Limits:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`


## III.  Report on High Association Usage

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/usage/high-usage-report/{userId}`
* This endpoint sends a report (records using 80%+ of their association limit) to the specified user's email.


## IV. Limitations

* **Daily Limits:**  Vary by subscription (Professional/Enterprise: 500,000; with API increase: 1,000,000).
* **Burst Limits:** Vary by subscription (Free/Starter: 100 requests/10 seconds; Professional/Enterprise: 150 requests/10 seconds; with API increase: 200 requests/10 seconds).


## V. Association Type ID Values

[See the provided table in the original text for a comprehensive list of `associationTypeId` values for various object pairings and association types.]


## VI. v1 Associations (Legacy)

[See the provided table in the original text for legacy v1 `associationTypeId` values.]

This comprehensive documentation provides a detailed overview of the HubSpot CRM API v4 for Associations, including endpoints, request/response examples, and important considerations for usage. Remember to consult the official HubSpot API documentation for the most up-to-date information.
