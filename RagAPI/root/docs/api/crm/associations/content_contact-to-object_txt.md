# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 for managing associations between records.  Associations represent relationships between objects and activities within the HubSpot CRM.  This version offers both association endpoints (for creating, editing, and removing associations) and association schema endpoints (for managing association definitions, custom labels, and limits).

**Note:** This API is supported in HubSpot NodeJS Client version 9.0.0 or later.  The number of associations a record can have depends on the object type and your HubSpot subscription.

## I. Association Endpoints

These endpoints manage associations between records.

### A. Associate Records

**1. Associate Records Without a Label:**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Parameters:**
    * `fromObjectType`: ID of the source object (e.g., `contact`, `company`). See [Object Type IDs](#object-type-ids) for a list.
    * `fromObjectId`: ID of the source record.
    * `toObjectType`: ID of the target object.
    * `toObjectId`: ID of the target record.
* **Example:**  Associating contact 12345 with company 67891:
  `PUT /crm/v4/objects/contact/12345/associations/default/company/67891`

* **Bulk Association (POST):**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
    * **Request Body:** An array of `objectId` values for records to associate.


**2. Associate Records With a Label:**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body:** An array of objects, each with:
    * `associationCategory`:  `"HUBSPOT_DEFINED"` (default label) or `"USER_DEFINED"` (custom label).
    * `associationTypeId`: Numerical ID of the label.  Obtain this from the [Retrieve Association Labels](#retrieve-association-labels) endpoint.
* **Example:** Associating a contact with a deal using a custom label (assuming `associationTypeId` is 36):
  `PUT /crm/v4/objects/contact/{objectId}/associations/deal/{toObjectId}`
  ```json
  [
    {
      "associationCategory": "USER_DEFINED",
      "associationTypeId": 36
    }
  ]
  ```
* **Bulk Labeled Association (POST):**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`
    * **Request Body:**  Similar to the single association, but for multiple record pairs. Include `id` values of records and required parameters.

* **Response (Example):**
  ```json
  {
    "fromObjectTypeId": "0-1",
    "fromObjectId": 29851,
    "toObjectTypeId": "0-3",
    "toObjectId": 21678228008,
    "labels": ["Point of contact"]
  }
  ```

### B. Retrieve Associated Records

**1. Retrieve Individual Record's Associations:**

* **Method:** `GET`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`
* **Parameters:**
    * `fromObjectType`: ID of the source object.
    * `objectId`: ID of the source record.
    * `toObjectType`: ID of the target object.

**2. Retrieve Associated Records in Bulk:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Request Body:** An array of `id` values for records.
* **Example Request:**
  ```json
  {
    "inputs": [
      { "id": "33451" },
      { "id": "29851" }
    ]
  }
  ```
* **Example Response:** (Includes `toObjectId`, `associationTypes` with `category`, `typeId`, and `label`) - See full example in original text.


### C. Update Record Association Labels

* Use the same endpoints as `Associate Records With a Label` (`PUT` and `POST`).  To replace an existing label, only include the new label. To append, include both old and new.

### D. Remove Record Associations

**1. Remove All Associations:**

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`

* **Bulk Removal (POST):**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`
    * **Request Body:**  An array specifying `from` and `to` object IDs.

**2. Remove Specific Association Labels:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
* **Request Body:** An array of objects, each with:
    * `types`: Array of objects, each with `associationCategory` and `associationTypeId` of labels to remove.
    * `from`: Object with `id` of the source record.
    * `to`: Object with `id` of the target record.


## II. Association Schema Endpoints

These endpoints manage association definitions, labels, and limits.

### A. Understand Association Definitions, Configurations, and Labels

This section covers the management of association types and their configurations (limits).  It differentiates between HubSpot-defined associations (like `Primary` and `Unlabeled`) and custom associations.

### B. Create and Manage Association Types

* **Create Association Labels:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
    * **Request Body:**
        * `name`: Internal name (no hyphens, no leading numbers).
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
    * **Example Response:** (Returns `category`, `typeId`, and `label`) - See full example in original text.


### C. Retrieve Association Labels

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Example Response:** (Returns an array of objects with `category`, `typeId`, and `label`) - See full example in original text.

### D. Update Association Labels

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:**
    * `associationTypeId`: ID of the label to update.
    * `label`: New label name.
    * `inverseLabel` (optional, for paired labels): New second label name.

### E. Delete Association Labels

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`

### F. Set and Manage Association Limits

* **Create or Update Limits:**
    * **Method:** `POST`
    * **Endpoint:**  `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (create) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (update).
    * **Request Body:** `inputs` array with:
        * `category`: `"HUBSPOT_DEFINED"` or `"USER_DEFINED"`.
        * `typeId`: ID of the association type.
        * `maxToObjectIds`: Maximum number of allowed associations.

* **Retrieve Limits:**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/all` (all limits) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (limits between specific objects).

* **Delete Limits:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
    * **Request Body:** `inputs` array with `category` and `typeId` of limits to delete.

## III. High Association Usage Report

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/usage/high-usage-report/{userId}`
* **Parameters:**
    * `userId`: ID of the user to receive the report.
* The report (a file) is emailed to the specified user.  The file contains records using 80% or more of their association limit.


## IV. Limitations

* **Daily Limits:** 500,000 requests for Professional and Enterprise accounts (1,000,000 with API limit increase, but this increase doesn't apply to association API).
* **Burst Limits:** 100 requests per 10 seconds (Free/Starter), 150 (Professional/Enterprise), 200 with API limit increase (but increase doesn't apply to association API).


## V. Object Type IDs

The following tables list HubSpot-defined `associationTypeId` values for various object types and association directions.  Custom object and custom label IDs need to be retrieved from your HubSpot settings or via the API.

**(See extensive tables of `associationTypeId` values in the original text.)**


## VI. v1 Associations (Legacy)

The original text contains a table of `associationTypeId` values for the legacy v1 Associations API.  Refer to the original text for this information if needed.


This markdown provides a structured and detailed overview of the HubSpot CRM API v4 for associations, enhancing clarity and usability compared to the original text.  Remember to replace placeholder values like `{objectId}`, `{fromObjectType}`, etc. with actual values in your API calls.
