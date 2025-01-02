# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 for managing record associations.  Associations represent relationships between objects and activities within the HubSpot CRM.  This API allows for creating, updating, retrieving, and deleting associations, including labeled associations.  It supports both individual record associations and batch operations.

**Note:** The v4 Associations API is supported in HubSpot NodeJS Client version 9.0.0 or later.  Association limits depend on the object and your HubSpot subscription.

## API Endpoints

The v4 Associations API consists of two main endpoint categories:

* **Association Endpoints:** Create, edit, and remove associations between records.
* **Association Schema Endpoints:** Manage association definitions (types), custom labels, and limits.


### I. Association Endpoints

#### A. Associate Records

**1. Associate records without a label:**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Parameters:**
    * `fromObjectType`: ID of the source object (e.g., `contact`, `company`). See "Association type ID values" section for a complete list.
    * `fromObjectId`: ID of the source record.
    * `toObjectType`: ID of the target object.
    * `toObjectId`: ID of the target record.
* **Example:** Associate contact (ID 12345) with company (ID 67891):
    * `PUT /crm/v4/objects/contact/12345/associations/default/company/67891`

**2. Associate records without a label (bulk):**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
* **Request Body:** Array of `objectId` values for records to associate.
* **Example:**  Associate multiple contacts with companies (details omitted for brevity).

**3. Associate records with a label:**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body:** Array of objects, each containing:
    * `associationCategory`:  `HUBSPOT_DEFINED` or `USER_DEFINED`.
    * `associationTypeId`: Numeric ID of the label.  Retrieve using `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`.
* **Example:** Associate contact with deal using custom label (ID 36):
    ```json
    [{"associationCategory": "USER_DEFINED", "associationTypeId": 36}]
    ```
* **Response:** Contains associated record IDs and label.

**4. Associate records with a label (bulk):**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`
* **Request Body:** Array of objects, each specifying record IDs and labels.  Similar structure to the single record PUT request above.


#### B. Retrieve Associated Records

**1. Retrieve associated records (single):**

* **Method:** `GET`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`
* **Parameters:**
    * `fromObjectType`: Source object ID.
    * `objectId`: Source record ID.
    * `toObjectType`: Target object ID.

**2. Retrieve associated records (bulk):**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Request Body:** Array of `id` values for records whose associations should be retrieved.
* **Response:**  Includes `toObjectId`, `associationTypes` (with `category`, `typeId`, `label`).

#### C. Update Record Association Labels

Use the bulk create endpoints (`/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`) to update existing associations.  To replace a label, only include the new label. To append, include all labels.

#### D. Remove Record Associations

**1. Remove all associations (single):**

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}/{toObjectId}`

**2. Remove all associations (bulk):**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`
* **Request Body:** Array of objects, each specifying source and target record IDs.

**3. Remove specific association labels (bulk):**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
* **Request Body:** Array of objects, each specifying record IDs and `associationTypeId` and `category` of labels to remove.


### II. Association Schema Endpoints

#### A. Create and Manage Association Types

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:**
    * `name`: Internal name (no hyphens, cannot start with a number).
    * `label`: Display name in HubSpot.
    * `inverseLabel` (optional, for paired labels): Second label in the pair.
* **Response:** Returns `category` and `typeId` for the new label.

#### B. Retrieve Association Labels

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Response:** Array of association types with `category`, `typeId`, and `label`.

#### C. Update Association Labels

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:** `associationTypeId` and new `label` (and optionally `inverseLabel`).

#### D. Delete Association Labels

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`


#### E. Set and Manage Association Limits

**1. Create or update association limits:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (create) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (update)
* **Request Body:** Array of objects, each with `category`, `typeId`, and `maxToObjectIds`.

**2. Retrieve association limits:**

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/all` (all limits) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (limits between specific objects).

**3. Delete association limits:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
* **Request Body:** Array of objects, each with `category` and `typeId` of limits to delete.


## Association Type ID Values

Detailed tables of HubSpot-defined `associationTypeId` values are provided in the original text.  These tables list the ID for each association type between different object pairs (e.g., Contact to Company, Deal to Ticket).


## Rate Limits

* **Daily Limits:**  Professional and Enterprise accounts: 500,000 requests.  With API limit increase: 1,000,000 requests (association requests do not benefit from additional increases).
* **Burst Limits:** Free and Starter accounts: 100 requests per 10 seconds. Professional and Enterprise accounts: 150 requests per 10 seconds. With API limit increase: 200 requests per 10 seconds (association requests do not benefit from additional increases).


## High Association Usage Report

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/usage/high-usage-report/{userId}`
* **Parameter:** `userId`: ID of the user to receive the report.  The report is sent via email and contains records nearing or exceeding association limits.


This markdown documentation provides a comprehensive overview of the HubSpot CRM API v4 for associations, including examples and details to facilitate API interaction.  Remember to consult the official HubSpot API documentation for the most up-to-date information.
