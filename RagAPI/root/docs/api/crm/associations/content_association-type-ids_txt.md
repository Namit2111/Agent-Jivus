# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 Associations endpoints.  This version supersedes the v3 Associations API.  It allows for managing relationships between different CRM objects (e.g., Contact to Company) and within the same object (e.g., Company to Company).  The API comprises two main sections: **Association Endpoints** (for creating, editing, and deleting associations) and **Association Schema Endpoints** (for managing association definitions, custom labels, and limits).

**Note:** The v4 Associations API requires HubSpot NodeJS Client Version 9.0.0 or later.  Association limits depend on the object type and your HubSpot subscription.

## I. Association Endpoints

These endpoints manage the associations between records.

### A. Associate Records

#### 1. Associate Records without a Label

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Parameters:**
    * `fromObjectType`: ID of the source object (e.g., `contact`, `company`). See [Object Type IDs](#association-type-id-values) for a list.
    * `fromObjectId`: ID of the source record.
    * `toObjectType`: ID of the target object.
    * `toObjectId`: ID of the target record.
* **Example:** Associate contact (ID 12345) with company (ID 67891):
    `PUT /crm/v4/objects/contact/12345/associations/default/company/67891`

#### 2. Bulk Associate Records without a Label

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
* **Request Body:** Array of `objectId` values to associate.
* **Example:** Associate multiple contacts with companies (requires an array of object IDs in the request body).

#### 3. Associate Records with a Label

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body:** Array of objects, each containing:
    * `associationCategory`: `"HUBSPOT_DEFINED"` or `"USER_DEFINED"`.
    * `associationTypeId`: Numerical ID of the label.  Retrieve IDs using `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`.
* **Example:** Associate a contact with a deal using custom label (ID 36):
    1. `GET /crm/v4/associations/contact/deal/labels` (to get `typeId`)
    2. `PUT /crm/v4/objects/contact/{objectId}/associations/deal/{toObjectId}` with body:
       ```json
       [{"associationCategory": "USER_DEFINED", "associationTypeId": 36}]
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
* **Request Body:** Requires `id` values of records to associate and `associationCategory` and `associationTypeId`.


### B. Retrieve Associated Records

#### 1. Retrieve Individual Record Associations

* **Method:** `GET`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`
* **Parameters:**
    * `fromObjectType`: Source object ID.
    * `objectId`: Source record ID.
    * `toObjectType`: Target object ID.

#### 2. Bulk Retrieve Associated Records

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Request Body:** Array of `id` values of records.
* **Example Request:**
  ```json
  {
    "inputs": [
      {"id": "33451"},
      {"id": "29851"}
    ]
  }
  ```
* **Example Response:** (See extensive example in provided text)


### C. Update Record Association Labels

Use the bulk create endpoints (`/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`)  to update existing labels.  To replace a label, only include the new label.  To append, include both old and new.

### D. Remove Record Associations

#### 1. Remove All Associations

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}/{toObjectId}`

#### 2. Bulk Remove All Associations

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`
* **Request Body:** Array of objects, each specifying `from` and `to` record IDs.


#### 3. Remove Specific Association Labels

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
* **Request Body:** Array of objects, each containing `from`, `to` IDs, `associationTypeId`, and `category`.


## II. Association Schema Endpoints

These endpoints manage the definitions, labels, and limits of associations.

### A. Understand Association Definitions, Configurations, and Labels

This section covers creating and managing custom association labels and setting limits.

### B. HubSpot Defined Associations

HubSpot provides predefined association types like "Primary" and "Unlabeled".

### C. Custom Association Labels

Allows creating custom labels for relationships (e.g., "Decision maker").

#### 1. Create Association Labels

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:**
    * `name`: Internal name (no hyphens, not starting with a number).
    * `label`: Display name.
    * `inverseLabel` (optional, for paired labels): Second label in the pair.
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

#### 2. Retrieve Association Labels

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`

#### 3. Update Association Labels

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:** `associationTypeId` and updated `label` (and `inverseLabel` if paired).

#### 4. Delete Association Labels

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`


### D. Set and Manage Association Limits

#### 1. Create or Update Association Limits

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (create) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (update)
* **Request Body:**  Array of objects, each with `category`, `typeId`, and `maxToObjectIds`.

#### 2. Retrieve Association Limits

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/all` (all limits) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (specific objects)

#### 3. Delete Association Limits

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
* **Request Body:** Array of objects, each with `category` and `typeId`.


## III. Report on High Association Usage

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/usage/high-usage-report/{userId}`
* This endpoint sends a report of records nearing or exceeding association limits to the specified user's email.


## IV. Limitations

* **Daily Limits:**  500,000 requests (Professional and Enterprise accounts).  Can be increased to 1,000,000 with an API limit increase (but Association API requests will not exceed 1,000,000).
* **Burst Limits:**  100 requests per 10 seconds (Free and Starter); 150 (Professional and Enterprise); 200 with API limit increase (but Association API requests will not exceed 200).


## V. Association Type ID Values

See the extensive tables in the provided text for a comprehensive list of `associationTypeId` values for different object pairings and association types (HubSpot-defined and custom).


This markdown provides a structured and comprehensive overview of the HubSpot CRM API v4 Associations, making it easier to understand and use.  Remember to always refer to the official HubSpot documentation for the most up-to-date information.
