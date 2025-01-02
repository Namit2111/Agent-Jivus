# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 for managing record associations.  Associations represent relationships between different CRM objects (e.g., Contact to Company) or within the same object (e.g., Company to Company).  This API provides endpoints for creating, updating, retrieving, and deleting associations, as well as managing association definitions and limits.  This version requires HubSpot NodeJS Client version 9.0.0 or later.


## I. Core Concepts

* **Objects:**  Represent different data types within HubSpot (e.g., Contacts, Companies, Deals). Each object has a unique ID.
* **Records:** Individual entries within an object (e.g., a specific Contact record). Each record has a unique ID.
* **Associations:**  Relationships between records.  Can be labeled or unlabeled.
* **Association Types (Definitions):** Define the types of relationships between objects.  Include HubSpot-defined types (e.g., "Primary") and custom user-defined types. Each type has a unique `typeId` and `category` (HUBSPOT_DEFINED or USER_DEFINED).
* **Association Labels:** User-defined labels that provide additional context to an association (e.g., "Billing Contact").  Can be single or paired (e.g., "Manager" and "Employee").


## II. API Endpoints

All endpoints are under the base URL `/crm/v4/`.

### A. Association Endpoints (Managing Associations)

These endpoints create, update, and delete associations between records.

**1. Associate Records (without label):**

* **Method:** `PUT`
* **Endpoint:** `/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Description:** Creates a default (unlabeled) association between two records.
* **Example:**
    * Request URL: `/crm/v4/objects/contact/12345/associations/default/company/67891` (Associates contact 12345 with company 67891)


**2. Associate Records (in bulk, without label):**

* **Method:** `POST`
* **Endpoint:** `/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
* **Description:** Creates multiple default (unlabeled) associations in a single request.
* **Request Body (Example):**
    ```json
    {
      "inputs": [
        {"id": "123"},
        {"id": "456"}
      ]
    }
    ```


**3. Associate Records (with label):**

* **Method:** `PUT`
* **Endpoint:** `/objects/{fromObjectType}/{fromObjectId}/associations/{toObjectType}/{toObjectId}`
* **Description:** Creates an association with a specified label.
* **Request Body (Example):**
    ```json
    [
      {
        "associationCategory": "USER_DEFINED",
        "associationTypeId": 36
      }
    ]
    ```


**4. Associate Records (in bulk, with label):**

* **Method:** `POST`
* **Endpoint:** `/associations/{fromObjectType}/{toObjectType}/batch/create`
* **Description:** Creates multiple labeled associations in a single request.


**5. Retrieve Associated Records:**

* **Method:** `GET`
* **Endpoint:** `/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`
* **Description:** Retrieves all records associated with a specific record.

* **Method:** `POST`
* **Endpoint:** `/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Description:** Retrieves associated records for multiple records in a single request.
* **Request Body (Example):**
    ```json
    {
      "inputs": [
        {"id": "33451"},
        {"id": "29851"}
      ]
    }
    ```

**6. Update Record Association Labels:**

* **Description:**  Use the bulk create endpoints (`/associations/{fromObjectType}/{toObjectType}/batch/create`) to update labels.  Including only the new label replaces the existing label; including multiple labels appends them.


**7. Remove Record Associations:**

* **Method:** `DELETE`
* **Endpoint:** `/objects/{fromObjectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
* **Description:** Removes all associations between two records.

* **Method:** `POST`
* **Endpoint:** `/associations/{fromObjectType}/{toObjectType}/batch/archive`
* **Description:** Removes all associations for multiple record pairs in bulk.

* **Method:** `POST`
* **Endpoint:** `/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
* **Description:** Removes specific association labels from multiple record pairs in bulk.



### B. Association Schema Endpoints (Managing Association Definitions and Limits)

These endpoints manage association types, labels, and limits.

**1. Create and Manage Association Types:**

* **Method:** `POST`
* **Endpoint:** `/associations/{fromObjectType}/{toObjectType}/labels`
* **Description:** Creates a new custom association label.
* **Request Body (Example - Single Label):**
    ```json
    {
      "label": "Partner",
      "name": "partner"
    }
    ```
* **Request Body (Example - Paired Labels):**
    ```json
    {
      "label": "Manager",
      "inverseLabel": "Employee",
      "name": "manager_employee"
    }
    ```

**2. Retrieve Association Labels:**

* **Method:** `GET`
* **Endpoint:** `/associations/{fromObjectType}/{toObjectType}/labels`
* **Description:** Retrieves all association labels between two objects.


**3. Update Association Labels:**

* **Method:** `PUT`
* **Endpoint:** `/associations/{fromObjectType}/{toObjectType}/labels`
* **Description:** Updates an existing association label.  Only the `label` and `inverseLabel` (for paired labels) can be updated.


**4. Delete Association Labels:**

* **Method:** `DELETE`
* **Endpoint:** `/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`
* **Description:** Deletes a custom association label.


**5. Create or Update Association Limits:**

* **Method:** `POST`
* **Endpoint:** `/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (Create)
* **Endpoint:** `/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (Update)
* **Description:** Sets or updates association limits.
* **Request Body (Example):**
    ```json
    {
      "inputs": [
        {
          "category": "USER_DEFINED",
          "typeId": 35,
          "maxToObjectIds": 1
        }
      ]
    }
    ```

**6. Retrieve Association Limits:**

* **Method:** `GET`
* **Endpoint:** `/associations/definitions/configurations/all` (All limits)
* **Endpoint:** `/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (Limits between two objects)
* **Description:** Retrieves association limits.


**7. Delete Association Limits:**

* **Method:** `POST`
* **Endpoint:** `/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
* **Description:** Deletes association limits.


**8. High Association Usage Report:**

* **Method:** `POST`
* **Endpoint:** `/associations/usage/high-usage-report/{userId}`
* **Description:** Generates a report of records approaching or exceeding association limits.  The report is emailed to the user specified by `userId`.


## III.  Object Type IDs

Refer to the provided documentation for a comprehensive list of `typeId` values for various object types and association types.  Note that  `typeId` values for custom objects and labels must be retrieved using the API.


## IV. Rate Limits

* **Daily Limits:** Vary by HubSpot subscription (Professional/Enterprise: 500,000 requests; with API limit increase: 1,000,000 requests).
* **Burst Limits:** Vary by HubSpot subscription (Free/Starter: 100 requests/10 seconds; Professional/Enterprise: 150 requests/10 seconds; with API limit increase: 200 requests/10 seconds).

## V. Error Handling

The API responses include standard HTTP status codes and detailed error messages to facilitate debugging.  Refer to the HubSpot API documentation for complete error handling details.


This markdown provides a more structured and concise representation of the provided text, improving readability and understandability.  Remember to always consult the official HubSpot API documentation for the most up-to-date information.
