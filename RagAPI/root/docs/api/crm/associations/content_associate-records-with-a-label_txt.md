# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 for managing record associations.  Associations represent relationships between objects and activities within the HubSpot CRM.  This version improves upon v3, offering enhanced functionality and efficiency.  Note that the v4 API requires HubSpot NodeJS Client version 9.0.0 or later.

## Core Concepts

* **Objects:**  Represent data types in HubSpot (e.g., Contacts, Companies, Deals).
* **Records:** Individual instances of an object (e.g., a specific contact).
* **Associations:** Relationships between records, possibly across different objects.
* **Association Types:** Define the nature of an association (e.g., "Primary Company," "Manager," custom labels).  These are identified by `typeId` and `category`.
    * `HUBSPOT_DEFINED`: Predefined association types by HubSpot.
    * `USER_DEFINED`: Custom association types created by the user.
* **Labels:** Human-readable names for association types.  A label can be associated with multiple record pairs.  Paired labels allow different descriptions on either side of the association (e.g., "Manager" and "Employee").
* **Limits:** Constraints on the number of associations a record can have, both system-wide and user-defined.


## API Endpoints

The v4 Associations API consists of two main endpoint categories:

**1. Association Endpoints:** Create, update, and delete associations between records.

**2. Association Schema Endpoints:** Manage association definitions (types) and labels, and set association limits.


### I. Association Endpoints

#### A. Associate Records

**1. Without a Label (Default Association):**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Example:** Associate contact (ID 12345) with company (ID 67891):
    `PUT /crm/v4/objects/contact/12345/associations/default/company/67891`

**2. Without a Label (Bulk):**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
* **Request Body:**  Array of `objectId` values.

**3. With a Label (Individual):**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body:** Array of objects: `{ "associationCategory": "USER_DEFINED" or "HUBSPOT_DEFINED", "associationTypeId": <typeId> }`

**4. With a Label (Bulk):**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`
* **Request Body:** Array of objects specifying `objectId`s and labels.

#### B. Retrieve Associated Records

**1. Individual Record:**

* **Method:** `GET`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`

**2. Bulk:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Request Body:** Array of `id` values for records to retrieve associations for.

#### C. Update Record Association Labels

Use the bulk create endpoints (`/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`) to update existing associations.  To replace an existing label, only specify the new label. To add labels, include both old and new.

#### D. Remove Record Associations

**1. Remove All Associations (Individual):**

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`

**2. Remove All Associations (Bulk):**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`
* **Request Body:** Array of `{ "from": { "id": ... }, "to": [{ "id": ... }] }` objects.

**3. Remove Specific Labels (Bulk):**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
* **Request Body:** Array of objects specifying `id`, `associationTypeId`, and `category` of labels to remove.


### II. Association Schema Endpoints

#### A.  Create and Manage Association Types

* **Method:** `POST` (Create), `PUT` (Update), `DELETE` (Delete)
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels` (Create/Update),  `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}` (Delete)
* **Request Body (Create):** `{ "name": <name>, "label": <label>, "inverseLabel": <inverseLabel> (optional for paired labels) }`

#### B. Retrieve Association Labels

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`

#### C. Update Association Labels

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:** `{ "associationTypeId": <typeId>, "label": <newLabel>, "inverseLabel": <newInverseLabel> (optional) }`

#### D. Delete Association Labels

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`

#### E. Set and Manage Association Limits

**1. Create/Update Limits:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (create) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (update)
* **Request Body:** Array of `{ "category": <category>, "typeId": <typeId>, "maxToObjectIds": <limit> }` objects.

**2. Retrieve Limits:**

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/all` (all limits) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (limits between two objects)

**3. Delete Limits:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
* **Request Body:** Array of `{ "category": <category>, "typeId": <typeId> }` objects.

#### F. Report on High Association Usage

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/usage/high-usage-report/{userID}`
* This sends a report to the specified user's email.


##  Example Responses (Simplified)

Many examples in the provided text are shown across multiple lines with line numbers.  Here are simplified versions for clarity:


**GET /crm/v4/objects/contacts/29851/associations/companies**

```json
{
  "results": [
    {
      "toObjectId": 5790939450,
      "associationTypes": [
        { "category": "HUBSPOT_DEFINED", "typeId": 279, "label": null }
      ]
    }
  ]
}
```

**POST /crm/v4/associations/contacts/companies/batch/labels/archive**

```json
{
  "inputs": [
    {
      "types": [{ "associationCategory": "USER_DEFINED", "associationTypeId": 37 }],
      "from": { "id": "29851" },
      "to": { "id": "5790939450" }
    }
  ]
}
```

##  Error Handling

The API will return standard HTTP status codes to indicate success or failure.  Consult the HubSpot API documentation for details on specific error codes and responses.


## Rate Limits

HubSpot imposes rate limits on API requests.  These limits vary depending on your account type.  Exceeding these limits will result in throttling.  Refer to the HubSpot documentation for current rate limit information.


##  Object Type IDs

A table listing all `typeId` values for HubSpot-defined association types is provided in the original text.  Refer to that table for the specific `typeId` values needed when making API requests.  Custom object types and custom association labels will have unique `typeId`s.


This markdown documentation provides a comprehensive overview of the HubSpot CRM API v4 for associations. Remember to consult the official HubSpot API documentation for the most up-to-date information and detailed specifications.
