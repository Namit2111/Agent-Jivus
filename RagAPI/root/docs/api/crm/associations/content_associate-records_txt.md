# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 Associations endpoints.  It allows you to manage relationships between records in the HubSpot CRM.  These relationships can be between records of different object types (e.g., Contact to Company) or within the same object type (e.g., Company to Company).

The API is divided into two main sections:

* **Association Endpoints:** Create, update, and delete associations between records.
* **Association Schema Endpoints:** Manage association definitions (types), custom labels, and limits.

**Note:** The v4 Associations API requires HubSpot NodeJS Client version 9.0.0 or later.  Association limits depend on your HubSpot object and subscription.


## I. Association Endpoints

These endpoints handle the creation and manipulation of record associations.

### A. Associate Records

#### 1. Associate Records Without a Label

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Parameters:**
    * `fromObjectType`: ID of the source object (e.g., `contact`, `company`). See [Object Type IDs](#object-type-ids)
    * `fromObjectId`: ID of the source record.
    * `toObjectType`: ID of the target object. See [Object Type IDs](#object-type-ids)
    * `toObjectId`: ID of the target record.
* **Example:** Associate contact (ID 12345) with company (ID 67891):
    `PUT /crm/v4/objects/contact/12345/associations/default/company/67891`

#### 2. Bulk Associate Records Without a Label

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
* **Request Body:** Array of `objectId` values for records to associate.
* **Example:**  (Associating multiple contact records with multiple company records is not possible in this endpoint. Only one to many associations are possible.)
    ```json
    [
      "contactId1",
      "contactId2"
    ]
    ```

#### 3. Associate Records With a Label

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body:** Array of objects, each with:
    * `associationCategory`: `"HUBSPOT_DEFINED"` or `"USER_DEFINED"`.
    * `associationTypeId`: Numerical ID of the label.  See [Object Type IDs](#object-type-ids) and  [Retrieve Association Labels](#retrieve-association-labels).
* **Example:** Associate contact (ID 12345) with deal (ID 67890) using custom label (ID 36):
    ```json
    PUT /crm/v4/objects/contact/12345/associations/deal/67890

    Request Body:
    [
      {
        "associationCategory": "USER_DEFINED",
        "associationTypeId": 36
      }
    ]
    ```
    *Response:*  (The exact response will vary, but will include the associated IDs and labels)
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
* **Request Body:** An array of objects, each specifying the association and label details. (See example)


### B. Retrieve Associated Records

#### 1. Retrieve Individual Record Associations

* **Method:** `GET`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`
* **Parameters:**
    * `fromObjectType`: ID of the source object.
    * `objectId`: ID of the source record.
    * `toObjectType`: ID of the target object.

#### 2. Bulk Retrieve Associated Records

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Request Body:** Array of `id` values for records whose associations you want to retrieve.
* **Example:** Retrieve company associations for contacts with IDs "33451" and "29851":
    ```json
    POST /crm/v4/associations/contacts/companies/batch/read

    Request Body:
    {
      "inputs": [
        {"id": "33451"},
        {"id": "29851"}
      ]
    }
    ```

    *Response:* (Illustrative - actual response depends on associations)
    ```json
    {
      "status": "COMPLETE",
      "results": [
        // ... (Association data for each contact) ...
      ]
    }
    ```


### C. Update Record Association Labels

* Use the bulk create endpoints (`POST /crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`) to update existing associations by specifying all the labels, including those you wish to keep.  Including only new labels will *replace* existing labels.

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
* **Request Body:** Array of objects, each specifying `from`, `to` record IDs, `associationTypeId`, and `category` of the label to remove.


## II. Association Schema Endpoints

These endpoints manage the definitions and configurations of associations.

### A. Understand Association Definitions, Configurations, and Labels

This section explains HubSpot-defined and custom association labels, including their creation and management.

### B. Create and Manage Association Types

#### 1. Create Association Labels

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:**
    * `name`: Internal name (no hyphens, cannot start with a number).
    * `label`: Display name of the label.
    * `inverseLabel` (optional, for paired labels): Display name of the inverse label.
* **Example (Single Label):**
    ```json
    POST /crm/v4/associations/contact/company/labels

    Request Body:
    {
      "label": "Partner",
      "name": "partner"
    }
    ```
* **Example (Paired Label):**
    ```json
    POST /crm/v4/associations/contact/company/labels

    Request Body:
    {
      "label": "Manager",
      "inverseLabel": "Employee",
      "name": "manager_employee"
    }
    ```

#### 2. Retrieve Association Labels

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Example:** Retrieve labels between contacts and companies:
    `GET /crm/v4/associations/contacts/companies/labels`


#### 3. Update Association Labels

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:**  `associationTypeId` and updated `label` (and optionally `inverseLabel`).

#### 4. Delete Association Labels

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`


### C. Set and Manage Association Limits

#### 1. Create or Update Association Limits

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (create) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (update)
* **Request Body:** Array of objects, each specifying `category`, `typeId`, and `maxToObjectIds`.

#### 2. Retrieve Association Limits

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/all` (all limits) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (limits between specific objects).

#### 3. Delete Association Limits

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
* **Request Body:** Array of objects, each specifying `category` and `typeId` of the limits to delete.


## III.  Limitations

* **Daily Limits:**  Vary by subscription (Professional/Enterprise: 500,000;  with API limit increase: 1,000,000).
* **Burst Limits:** Vary by subscription (Free/Starter: 100 requests/10 seconds; Professional/Enterprise: 150 requests/10 seconds; with API limit increase: 200 requests/10 seconds).


## IV. Object Type IDs

The following tables list HubSpot-defined `associationTypeId` values.  Custom object and custom label IDs will be different and need to be retrieved using the API.

**(Tables for Company to object, Contact to object, Deal to object, Ticket to object, Lead to object, Appointment to object, Course to object, Listing to object, Service to object, Call to object, Email to object, Meeting to object, Note to object, Postal mail to object, Quote to object, Task to object, Communication (SMS, WhatsApp, or LinkedIn message) to object, Order to object, and Cart to object are omitted for brevity but are present in the original text.)**

**(Table for v1 associations (legacy) is omitted for brevity but is present in the original text.)**


This markdown provides a comprehensive overview of the HubSpot CRM API v4 Associations.  Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
