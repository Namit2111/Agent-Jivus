# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 for managing associations between records.  Associations represent relationships between different objects (e.g., Contact to Company) or within the same object (e.g., Company to Company).  This API includes endpoints for managing associations and their schemas (definitions, labels, and limits).

**Note:** This API requires HubSpot NodeJS Client version 9.0.0 or later.  The number of associations a record can have depends on the object type and your HubSpot subscription.


## I. Association Endpoints

These endpoints create, update, and remove associations between records.

### A. Associate Records

#### 1. Associate Records Without a Label

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Parameters:**
    * `fromObjectType`: ID of the source object (e.g., `contact`, `company`).  See [Object Type IDs](#object-type-ids)
    * `fromObjectId`: ID of the source record.
    * `toObjectType`: ID of the target object.  See [Object Type IDs](#object-type-ids)
    * `toObjectId`: ID of the target record.
* **Example:** Associate contact (ID 12345) with company (ID 67891):
  `/crm/v4/objects/contact/12345/associations/default/company/67891`

#### 2. Bulk Associate Records Without a Label

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
* **Request Body:** Array of `objectId` values to associate.
* **Example Request Body:**
  ```json
  [12345, 67890, 98765]
  ```

#### 3. Associate Records With a Label

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body:** Array of objects, each with:
    * `associationCategory`: `HUBSPOT_DEFINED` or `USER_DEFINED`
    * `associationTypeId`: Numeric ID of the label. See [Association Type IDs](#object-type-ids) and how to [Retrieve Association Labels](#retrieve-association-labels).
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
* **Request Body:**  Array of association objects, including `fromObjectId`, `toObjectId`, `associationCategory`, and `associationTypeId` for each association.


### B. Retrieve Associated Records

#### 1. Retrieve Individual Record's Associations

* **Method:** `GET`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`
* **Parameters:**
    * `fromObjectType`: Source object ID.
    * `objectId`: Source record ID.
    * `toObjectType`: Target object ID.

#### 2. Bulk Retrieve Associated Records

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Request Body:** Array of `id` values for records whose associations you want to retrieve.
* **Example Request Body:**
  ```json
  {
    "inputs": [
      {"id": "33451"},
      {"id": "29851"}
    ]
  }
  ```
* **Example Response:** (See extensive example in original text)


### C. Update Record Association Labels

Use the bulk create endpoints (`/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`) to update existing labels.  To replace a label, provide only the new label. To append, include both the old and new labels.


### D. Remove Record Associations

#### 1. Remove All Associations

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}/{toObjectId}`

#### 2. Bulk Remove All Associations

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`
* **Request Body:** Array of objects, each specifying `from` and `to` object IDs.


#### 3. Remove Specific Association Labels

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
* **Request Body:** Array of objects, each specifying `from`, `to` object IDs, and the `associationTypeId` and `category` of the label to remove.


## II. Association Schema Endpoints

These endpoints manage association definitions, custom labels, and limits.


### A. Understand Association Definitions, Configurations, and Labels


### B. HubSpot Defined Associations

Two main types: `Primary` and `Unlabeled`.  See the original document for details.

### C. Custom Association Labels

Create labels to provide additional context for record relationships.  Can be single or paired labels.


### D. Create and Manage Association Types

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:**
    * `name`: Internal name (no hyphens, no leading numbers).
    * `label`: Display name.
    * `inverseLabel` (for paired labels):  Second label in the pair.
* **Example Request Body (Single Label):**
  ```json
  {
    "label": "Partner",
    "name": "partner"
  }
  ```
* **Example Request Body (Paired Labels):**
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

### E. Retrieve Association Labels

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`

### F. Update Association Labels

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:** `associationTypeId` and new `label` (and optionally `inverseLabel`).

### G. Delete Association Labels

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`


### H. Set and Manage Association Limits

#### 1. Create or Update Association Limits

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (create) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (update)
* **Request Body:** Array of `inputs`, each with:
    * `category`: `HUBSPOT_DEFINED` or `USER_DEFINED`
    * `typeId`: Association type ID.
    * `maxToObjectIds`: Maximum number of associations allowed.

#### 2. Retrieve Association Limits

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/all` (all limits) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (limits between specific objects)

#### 3. Delete Association Limits

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
* **Request Body:** Array of `inputs`, each specifying `category` and `typeId` of the limit to delete.


## III. Limitations

* **Daily Limits:**  500,000 requests for Professional and Enterprise accounts.  1,000,000 with API limit increase (this increase doesn't apply to association API).
* **Burst Limits:** 100 requests per 10 seconds (Free/Starter), 150 (Professional/Enterprise), 200 with API limit increase (increase doesn't apply to association API).


## IV. Association Type ID Values

See the extensive tables in the original document for a complete list of `associationTypeId` values for various object pairings.


## V.  v1 Associations (Legacy)

The original document includes a table of IDs for the legacy v1 Associations API.


This Markdown documentation provides a comprehensive overview of the HubSpot CRM API v4 for associations.  Remember to consult the official HubSpot documentation for the most up-to-date information and detailed specifications.
