# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 Associations endpoints.  This version supersedes the v3 API.  The v4 API manages relationships (associations) between HubSpot CRM objects.

## Overview

Associations represent connections between records of different or the same object types (e.g., Contact to Company, Company to Company).  The v4 API consists of two main sections:

* **Association Endpoints:** Create, update, and delete associations between records.
* **Association Schema Endpoints:** Manage association definitions (types), custom labels, and association limits.

**Note:** The v4 Associations API requires HubSpot NodeJS Client Version 9.0.0 or later. Association limits depend on the object type and your HubSpot subscription.

## API Endpoints

All endpoints are under the base URL `/crm/v4/`.

### Association Endpoints

#### Associate Records

**1. Without a Label (Default Association):**

* **Method:** `PUT`
* **Endpoint:** `/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Parameters:**
    * `fromObjectType`: ID of the source object (e.g., `contact`, `company`). See [Object Type IDs](#object-type-ids)
    * `fromObjectId`: ID of the source record.
    * `toObjectType`: ID of the target object.
    * `toObjectId`: ID of the target record.
* **Example:** Associate contact (ID 12345) with company (ID 67891):
  `PUT /crm/v4/objects/contact/12345/associations/default/company/67891`

**2. Without a Label (Bulk):**

* **Method:** `POST`
* **Endpoint:** `/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
* **Request Body:**  Array of `objectId` values to associate.
* **Example:** Associate multiple contacts with companies (omitted for brevity).

**3. With a Label:**

* **Method:** `PUT`
* **Endpoint:** `/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body:** Array of objects, each with:
    * `associationCategory`: `"HUBSPOT_DEFINED"` or `"USER_DEFINED"`.
    * `associationTypeId`: Numerical ID of the label (see [Retrieving Association Labels](#retrieve-association-labels)).
* **Example:** Associate contact (ID 12345) with deal (ID 67891) using custom label (ID 36):
    `PUT /crm/v4/objects/contact/12345/associations/deal/67891`
    ```json
    [
      {
        "associationCategory": "USER_DEFINED",
        "associationTypeId": 36
      }
    ]
    ```
* **Response:**
    ```json
    {
      "fromObjectTypeId": "0-1",
      "fromObjectId": 29851,
      "toObjectTypeId": "0-3",
      "toObjectId": 21678228008,
      "labels": ["Point of contact"]
    }
    ```

**4. With a Label (Bulk):**

* **Method:** `POST`
* **Endpoint:** `/associations/{fromObjectType}/{toObjectType}/batch/create`
* **Request Body:** Similar to single association with label, but in a batched format.

#### Retrieve Associated Records

**1. Single Record:**

* **Method:** `GET`
* **Endpoint:** `/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`
* **Parameters:**
    * `fromObjectType`: Source object ID.
    * `objectId`: Source record ID.
    * `toObjectType`: Target object ID.

**2. Multiple Records (Bulk):**

* **Method:** `POST`
* **Endpoint:** `/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Request Body:** Array of `{id: recordId}` objects.
* **Example:**
    ```json
    {
      "inputs": [
        {"id": "33451"},
        {"id": "29851"}
      ]
    }
    ```
* **Response (Example):**  See example in original document.

#### Update Record Association Labels

Use the same endpoints as for creating labelled associations (`PUT` and `POST` batch endpoints).  To replace a label, only include the new label.  To append, include all labels.

#### Remove Record Associations

**1. All Associations (Single):**

* **Method:** `DELETE`
* **Endpoint:** `/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`

**2. All Associations (Bulk):**

* **Method:** `POST`
* **Endpoint:** `/associations/{fromObjectType}/{toObjectType}/batch/archive`
* **Request Body:** Array of `{from: {id: ...}, to: [{id: ...}]}` objects.

**3. Specific Association Labels (Bulk):**

* **Method:** `POST`
* **Endpoint:** `/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
* **Request Body:** Array of objects, each with:
    * `types`: Array of `{associationCategory, associationTypeId}` objects to remove.
    * `from`: `{id: recordId}`
    * `to`: `{id: recordId}`


### Association Schema Endpoints

#### Create and Manage Association Types

* **Method:** `POST`
* **Endpoint:** `/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:**
    * `name`: Internal name (no hyphens, no leading numbers).
    * `label`: Display name.
    * `inverseLabel` (optional, for paired labels): Second label in the pair.
* **Example (Single Label):**
    ```json
    {
      "label": "Partner",
      "name": "partner"
    }
    ```
* **Example (Paired Labels):**
    ```json
    {
      "label": "Manager",
      "inverseLabel": "Employee",
      "name": "manager_employee"
    }
    ```

#### Retrieve Association Labels

* **Method:** `GET`
* **Endpoint:** `/associations/{fromObjectType}/{toObjectType}/labels`
* **Response (Example):** See example in original document.

#### Update Association Labels

* **Method:** `PUT`
* **Endpoint:** `/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:**
    * `associationTypeId`: ID of the label to update.
    * `label`: New label name.
    * `inverseLabel` (optional): New inverse label name (for paired labels).

#### Delete Association Labels

* **Method:** `DELETE`
* **Endpoint:** `/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`

#### Set and Manage Association Limits

**1. Create or Update Limits:**

* **Method:** `POST`
* **Endpoint:** `/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (create) or `/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (update)
* **Request Body:** Array of `{category, typeId, maxToObjectIds}` objects.

**2. Retrieve Limits:**

* **Method:** `GET`
* **Endpoint:** `/associations/definitions/configurations/all` (all limits) or `/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (limits between two objects)

**3. Delete Limits:**

* **Method:** `POST`
* **Endpoint:** `/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
* **Request Body:** Array of `{category, typeId}` objects.


#### High Association Usage Report

* **Method:** `POST`
* **Endpoint:** `/associations/usage/high-usage-report/{userId}`
* **Parameters:** `userId`: ID of the user to receive the report.


## Object Type IDs

A complete list of object type IDs is not provided in this excerpt, but the documentation mentions it is available within the HubSpot documentation.  The most common object types (contacts, companies, deals, tickets, notes) can use their names directly in the API calls.

##  HubSpot Defined Associations

* **Primary:** The main association.  Used in HubSpot tools like lists and workflows.  Only one primary association is allowed per object pair.
* **Unlabeled:** A default association with no label. Always returned in responses with `label: null`.

##  Custom Association Labels

Allows for more specific relationships between records (e.g., "Decision Maker", "Billing Contact").  You can create single or paired labels.


## Limitations

* **Daily Limits:** 500,000 requests (Professional and Enterprise), potentially higher with API limit increase (but not exceeding 1,000,000 for Associations API).
* **Burst Limits:** 100 requests/10 seconds (Free, Starter), 150 requests/10 seconds (Professional, Enterprise), potentially higher with API limit increase (but not exceeding 200 for Associations API).


This markdown provides a comprehensive overview of the HubSpot CRM API v4 Associations. Remember to consult the official HubSpot documentation for the most up-to-date information and detailed specifications.
