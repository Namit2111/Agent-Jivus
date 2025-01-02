# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 for managing associations between records.  Associations represent relationships between different CRM objects (e.g., Contact to Company) or within the same object (e.g., Company to Company).  This API provides endpoints for managing associations and their schemas.

**Note:** This API requires HubSpot NodeJS Client v9.0.0 or later.  The number of associations a record can have depends on the object and your HubSpot subscription.

## API Endpoints Categories:

The v4 Associations API is divided into two main categories:

* **Association Endpoints:** Create, update, and delete associations between records.
* **Association Schema Endpoints:** Manage association definitions (types), custom labels, and association limits.

## I. Association Endpoints

### A. Associate Records

**1. Associate Records Without a Label:**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Parameters:**
    * `fromObjectType`: ID of the source object (e.g., `contact`, `company`).  See [Object Type IDs](#association-type-id-values)
    * `fromObjectId`: ID of the source record.
    * `toObjectType`: ID of the target object.
    * `toObjectId`: ID of the target record.
* **Example:** Associate contact (ID 12345) with company (ID 67891):
    `PUT /crm/v4/objects/contact/12345/associations/default/company/67891`

**2. Bulk Associate Records Without a Label:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
* **Request Body:** Array of `objectId` values for records to associate.
* **Example:**
    ```json
    [12345, 67891, 90123]
    ```

**3. Associate Records With a Label:**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body:** Array of objects, each with:
    * `associationCategory`:  `HUBSPOT_DEFINED` (default) or `USER_DEFINED` (custom).
    * `associationTypeId`: Numerical ID of the label.  See [Object Type IDs](#association-type-id-values) and [Retrieve Association Labels](#retrieve-association-labels) for custom labels.
* **Example:** Associate contact (ID 12345) with deal (ID 67891) using custom label (typeId: 36):
    ```json
    PUT /crm/v4/objects/contact/12345/associations/deal/67891
    Request Body:
    [{"associationCategory": "USER_DEFINED", "associationTypeId": 36}]
    ```
    *Response Example:*
    ```json
    {
      "fromObjectTypeId": "0-1",
      "fromObjectId": 29851,
      "toObjectTypeId": "0-3",
      "toObjectId": 21678228008,
      "labels": ["Point of contact"]
    }
    ```


**4. Bulk Create Labeled Associations:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`
* **Request Body:** Array of associations, each with `fromObjectId`, `toObjectId`, `associationCategory`, and `associationTypeId`.

### B. Retrieve Associated Records

**1. Retrieve Individual Record's Associations:**

* **Method:** `GET`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`

**2. Bulk Retrieve Associated Records:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Request Body:** Array of `id` values for records.
* **Example:** Retrieve companies associated with contacts with IDs "33451" and "29851":
    ```json
    POST /crm/v4/associations/contacts/companies/batch/read
    Request Body:
    {"inputs": [{"id": "33451"}, {"id": "29851"}]}
    ```
    *Response Example:*  (See example in original text)


### C. Update Record Association Labels

Use the `PUT` endpoint from section [Associate Records With a Label](#associate-records-with-a-label) to update labels.  To replace existing labels, provide only the new label(s). To append, include all labels.

### D. Remove Record Associations

**1. Remove All Associations:**

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`

**2. Bulk Remove All Associations:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`
* **Request Body:**  Array of objects with `from` and `to` object IDs.

**3. Remove Specific Association Labels:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
* **Request Body:** Array of objects, each with `from`, `to`, and `types` (array of `associationCategory` and `associationTypeId`).


### E. Report on High Association Usage

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/usage/high-usage-report/{userId}`
* **Description:** Sends a report of records nearing association limits to the specified user's email.


## II. Association Schema Endpoints

### A. Understand Association Definitions, Configurations, and Labels

This section covers managing association types, labels, and limits using schema endpoints.

### B. HubSpot Defined Associations

HubSpot provides predefined associations (`Primary` and `Unlabeled`).  `Primary` is the main association, while `Unlabeled` indicates an association without a specific label.

### C. Custom Association Labels

Create custom labels to provide more context to associations.  Labels can be:

* **Single:** One label for both associated records.
* **Paired:** Two labels, one for each record in the relationship.

### D. Create and Manage Association Types

* **Create Association Labels:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
    * **Request Body:**
        * `name`: Internal name (no hyphens, no leading numbers).
        * `label`: Display name.
        * `inverseLabel` (Paired labels only): Second label in the pair.
    * **Example:** (See examples in original text)

### E. Retrieve Association Labels

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Response:** Array of objects, each with `category`, `typeId`, and `label`.

### F. Update Association Labels

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:** `associationTypeId` and updated `label` (and `inverseLabel` if paired).

### G. Delete Association Labels

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`

### H. Set and Manage Association Limits

* **Create/Update Association Limits:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (create) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (update)
    * **Request Body:**  Array of objects with `category`, `typeId`, and `maxToObjectIds`.

* **Retrieve Association Limits:**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/all` (all limits) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (specific objects).

* **Delete Association Limits:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
    * **Request Body:** Array of objects with `category` and `typeId`.


## III. Limitations

* **Daily Limits:** 500,000 requests (Professional/Enterprise), 1,000,000 with API limit increase (but not increased for Associations API)
* **Burst Limits:** 100 requests/10 seconds (Free/Starter), 150 requests/10 seconds (Professional/Enterprise), 200 requests/10 seconds with API limit increase (but not increased for Associations API).


## IV. Association Type ID Values

See the tables in the original text for a complete list of `associationTypeId` values for various object types and association directions.


This markdown provides a comprehensive overview of the HubSpot CRM API v4 for associations.  Remember to consult the official HubSpot documentation for the most up-to-date information and details.
