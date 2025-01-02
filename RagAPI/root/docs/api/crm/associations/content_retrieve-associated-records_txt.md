# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 for managing associations between records.  Associations represent relationships between objects and activities within the HubSpot CRM.  This API supports both creating custom associations and working with HubSpot-defined associations.

## API Endpoints

The v4 Associations API includes two categories of endpoints:

* **Association Endpoints:** Create, edit, and remove associations between records.
* **Association Schema Endpoints:** Manage association definitions (types), custom labels, and association limits.

**Note:** The v4 Associations API is supported in HubSpot NodeJS Client version 9.0.0 or later.  The number of associations a record can have depends on the object type and your HubSpot subscription.

## Association Endpoints

### 1. Associate Records

#### 1.1 Associate Records Without a Label

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Parameters:**
    * `fromObjectType`: ID of the source object (e.g., `contact`, `company`). See [Object Type IDs](#object-type-ids).
    * `fromObjectId`: ID of the source record.
    * `toObjectType`: ID of the target object. See [Object Type IDs](#object-type-ids).
    * `toObjectId`: ID of the target record.
* **Example:** Associate contact (ID 12345) with company (ID 67891):
    `PUT /crm/v4/objects/contact/12345/associations/default/company/67891`

#### 1.2 Associate Records in Bulk Without a Label

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
* **Request Body:** Array of `objectId` values for records to associate.
* **Example:**  Associate multiple contacts with companies (details omitted for brevity).

#### 1.3 Associate Records With a Label

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body:** Array of objects, each with:
    * `associationCategory`: `"HUBSPOT_DEFINED"` or `"USER_DEFINED"`.
    * `associationTypeId`: Numerical ID of the label.  Retrieve using `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`.
* **Example:** Associate contact with deal using custom label (ID 36):
    ```json
    [
      {
        "associationCategory": "USER_DEFINED",
        "associationTypeId": 36
      }
    ]
    ```
* **Response:** Contains `fromObjectTypeId`, `fromObjectId`, `toObjectTypeId`, `toObjectId`, and `labels`.  Example:
    ```json
    {
      "fromObjectTypeId": "0-1",
      "fromObjectId": 29851,
      "toObjectTypeId": "0-3",
      "toObjectId": 21678228008,
      "labels": ["Point of contact"]
    }
    ```

#### 1.4 Associate Records in Bulk With a Label

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`
* **Request Body:** Similar to 1.3, but in bulk.


### 2. Retrieve Associated Records

#### 2.1 Retrieve Associated Records (Individual)

* **Method:** `GET`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`
* **Parameters:**
    * `fromObjectType`: Source object ID.
    * `objectId`: Source record ID.
    * `toObjectType`: Target object ID.

#### 2.2 Retrieve Associated Records (Batch)

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Request Body:** Array of `id` values for records.
* **Example Request:**
    ```json
    {
      "inputs": [
        {"id": "33451"},
        {"id": "29851"}
      ]
    }
    ```
* **Example Response:** (Extensive, showing multiple associated records and labels)


### 3. Update Record Association Labels

Use the bulk create endpoints (`/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`) to update labels. To replace, only include the new label. To append, include all labels.

### 4. Remove Record Associations

#### 4.1 Remove All Associations

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`

#### 4.2 Remove All Associations (Batch)

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`
* **Request Body:** Array of objects, each with `from` (containing `id`) and `to` (array of `id` objects).

#### 4.3 Remove Specific Association Labels

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
* **Request Body:** Array of objects, each with `from`, `to`, and `types` (array of objects with `associationCategory` and `associationTypeId`).


## Association Schema Endpoints

These endpoints manage association definitions, configurations, and labels.

### 1. Create and Manage Association Types

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
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
* **Response:** Contains `category` and `typeId` for the new label(s).

### 2. Retrieve Association Labels

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Response:** Array of objects, each with `category`, `typeId`, and `label`.

### 3. Update Association Labels

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:** `associationTypeId` and updated `label` (and `inverseLabel` if needed).

### 4. Delete Association Labels

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`


### 5. Set and Manage Association Limits

#### 5.1 Create or Update Association Limits

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (create) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (update)
* **Request Body:** Array of objects, each with `category`, `typeId`, and `maxToObjectIds`.

#### 5.2 Retrieve Association Limits

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/all` (all limits) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (specific objects).

#### 5.3 Delete Association Limits

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
* **Request Body:** Array of objects, each with `category` and `typeId`.


## High Association Usage Report

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/usage/high-usage-report/{userId}`
* **Parameters:** `userId`: ID of the user to receive the report.
* **Description:** Sends a report of records nearing or exceeding association limits to the specified user's email.


## Object Type IDs

The following table lists some common object type IDs.  Refer to the HubSpot documentation for a complete list and IDs for custom objects.

| Object Type      | ID     |
|-----------------|--------|
| Contact          | 0-1    |
| Company          | 0-2    |
| Deal             | 0-3    |
| Ticket           | 0-4    |
| Note             | 0-5    |
| ...              | ...    |


## Limitations

* **Daily Limits:** Vary by subscription (Professional/Enterprise: 500,000; with API limit increase: 1,000,000).
* **Burst Limits:** Vary by subscription (Free/Starter: 100 requests/10 seconds; Professional/Enterprise: 150 requests/10 seconds; with API limit increase: 200 requests/10 seconds).

Refer to the HubSpot documentation for the most up-to-date information on API limits and other details.  This documentation provides a comprehensive overview but may not cover all edge cases or nuanced scenarios.  Always consult the official HubSpot API reference for the most accurate and detailed information.
