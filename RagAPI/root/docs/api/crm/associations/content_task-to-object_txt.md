# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 for managing associations between records.  Associations represent relationships between different CRM objects (e.g., Contact to Company) or within the same object (e.g., Company to Company).  This version improves upon v3, offering enhanced functionality and efficiency.  Note that this API is supported in HubSpot NodeJS Client version 9.0.0 and later.

## Key Concepts

* **Object:** A type of data in HubSpot (e.g., Contacts, Companies, Deals). Each object has a unique ID.
* **Record:** A single instance of an object (e.g., a specific contact). Each record has a unique ID.
* **Association:** A relationship between two records.  Associations can be labeled or unlabeled.
* **Association Type (or Definition):**  Defines the type of relationship between objects.  Can be HubSpot-defined (e.g., "Primary") or custom-defined.
* **Association Label:** A human-readable name for a specific association type (e.g., "Billing Contact").  Labels are supported between Contacts, Companies, Deals, Tickets, and custom objects.
* **`typeId`:** A numeric ID uniquely identifying an association type.


## API Endpoints

The v4 Associations API provides two main endpoint categories:

**1. Association Endpoints:** Create, update, and delete associations between records.

**2. Association Schema Endpoints:** Manage association definitions, custom labels, and association limits.


### I. Association Endpoints

#### A. Associate Records

* **Without a Label (Default Association):**

    * **Method:** `PUT`
    * **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
    * **Example:**  `/crm/v4/objects/contact/12345/associations/default/company/67891` (Associates contact 12345 with company 67891).
    * **Bulk Association:**
        * **Method:** `POST`
        * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
        * **Request Body:** Array of `objectId` values.


* **With a Label:**

    * **Method:** `PUT`
    * **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
    * **Request Body:**  Array of objects, each containing `associationCategory` ("HUBSPOT_DEFINED" or "USER_DEFINED") and `associationTypeId`.
    * **Example (Custom Label):** Requires a prior `GET` request to `/crm/v4/associations/contact/deal/labels` to obtain the `typeId` for the custom label.
    * **Bulk Labeled Association:**
        * **Method:** `POST`
        * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`
        * **Request Body:**  Array of association objects, including `objectId`, `associationCategory`, and `associationTypeId` for each association.


#### B. Retrieve Associated Records

* **Individual Record:**

    * **Method:** `GET`
    * **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`

* **Batch Retrieval:**

    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
    * **Request Body:** Array of `id` values for records to retrieve associations for.


#### C. Update Record Association Labels

* Use the bulk create endpoints (`PUT` or `POST`) to update existing labels.  Including only the new label replaces the existing label; including both old and new labels appends the new label.


#### D. Remove Record Associations

* **Remove All Associations:**

    * **Method:** `DELETE`
    * **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
    * **Bulk Removal:**
        * **Method:** `POST`
        * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`


* **Remove Specific Association Labels:**

    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
    * **Request Body:** Array of objects, each containing `from`, `to`, and an array of `types` to remove (specifying `associationCategory` and `associationTypeId`).


### II. Association Schema Endpoints

#### A. Create and Manage Association Types

* **Create Association Labels:**

    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
    * **Request Body:** `name`, `label`, `inverseLabel` (for paired labels).

#### B. Retrieve Association Labels

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`

#### C. Update Association Labels

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:** `associationTypeId` and updated `label` (and optionally `inverseLabel`).

#### D. Delete Association Labels

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`


#### E. Set and Manage Association Limits

* **Create/Update Limits:**

    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (create) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (update)
    * **Request Body:** Array of objects, each containing `category`, `typeId`, and `maxToObjectIds`.

* **Retrieve Limits:**

    * **Method:** `GET`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/all` (all limits) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (specific objects)

* **Delete Limits:**

    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
    * **Request Body:** Array of objects, each containing `category` and `typeId` of limits to delete.


#### F. Report on High Association Usage

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/usage/high-usage-report/{userId}`
* This endpoint sends a report of records nearing or exceeding association limits to the specified user's email.


##  Object Type IDs

Refer to the provided tables in the original text for a comprehensive list of `typeId` values for different object types and association directions.


## Rate Limits

* **Daily Limits:** Vary depending on your HubSpot subscription (Professional/Enterprise: 500,000 requests;  with API limit increase: 1,000,000 requests).
* **Burst Limits:** Vary depending on your HubSpot subscription (Free/Starter: 100 requests/10 seconds; Professional/Enterprise: 150 requests/10 seconds; with API limit increase: 200 requests/10 seconds).


## Examples (See original text for detailed examples of requests and responses for each endpoint.)


This documentation provides a structured overview.  Always refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications.
