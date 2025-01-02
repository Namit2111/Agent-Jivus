# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 Associations endpoints.  This version supersedes the v3 Associations API.  It allows for managing relationships (associations) between different CRM objects and activities.

## Overview

Associations represent relationships between records in the HubSpot CRM.  These relationships can be between records of different object types (e.g., Contact to Company) or within the same object type (e.g., Company to Company).

The v4 API consists of two main endpoint categories:

* **Association Endpoints:** Create, update, and delete associations between records.
* **Association Schema Endpoints:** Manage association definitions (types), custom labels, and association limits.

**Note:** The v4 Associations API requires HubSpot NodeJS Client version 9.0.0 or later.  Association limits depend on the object type and your HubSpot subscription.

## API Endpoints

All endpoints are prefixed with `/crm/v4/`.  Replace `{fromObjectType}`, `{fromObjectId}`, `{toObjectType}`, `{toObjectId}`, and `{objectId}` with appropriate values.  Object type IDs can be found in the [Object Type ID Values](#object-type-id-values) section or, for contacts, companies, deals, tickets, and notes, can often be the object name (e.g., `contact`, `company`).


### Association Endpoints

#### Associate Records

* **Without a Label (Individual):** `PUT /objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
    * **Method:** `PUT`
    * **Example:** `/crm/v4/objects/contact/12345/associations/default/company/67891` (Associates contact 12345 with company 67891)
* **Without a Label (Bulk):** `POST /associations/{fromObjectType}/{toObjectType}/batch/associate/default`
    * **Method:** `POST`
    * **Request Body:** Array of `objectId` values.
* **With a Label (Individual):** `PUT /objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
    * **Method:** `PUT`
    * **Request Body:** Array of objects, each with `associationCategory` (e.g., `"USER_DEFINED"`) and `associationTypeId`.
    * **Example:**  Requires a prior `GET` request to `/crm/v4/associations/contact/deal/labels` to obtain the `associationTypeId` for a custom label.
* **With a Label (Bulk):** `POST /associations/{fromObjectType}/{toObjectType}/batch/create`
    * **Method:** `POST`
    * **Request Body:** Array of objects, each containing record IDs and label information (`associationCategory`, `associationTypeId`).

#### Retrieve Associated Records

* **Individual:** `GET /objects/{fromObjectType}/{objectId}/associations/{toObjectType}`
    * **Method:** `GET`
* **Bulk:** `POST /associations/{fromObjectType}/{toObjectType}/batch/read`
    * **Method:** `POST`
    * **Request Body:** Array of `id` values.


#### Update Record Association Labels

* Use the bulk create endpoints (`POST /associations/{fromObjectType}/{toObjectType}/batch/create`) to update existing labels. Include all desired labels; existing ones will be replaced.


#### Remove Record Associations

* **All Associations (Individual):** `DELETE /objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
    * **Method:** `DELETE`
* **All Associations (Bulk):** `POST /associations/{fromObjectType}/{toObjectType}/batch/archive`
    * **Method:** `POST`
    * **Request Body:** Array of `{from: {id}, to: [{id}]}` objects.
* **Specific Labels (Bulk):** `POST /associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
    * **Method:** `POST`
    * **Request Body:** Array of objects, each containing `from`, `to`, and `types` (array of `{associationCategory, associationTypeId}`).


### Association Schema Endpoints

#### Create and Manage Association Types

* **Create Association Labels:** `POST /associations/{fromObjectType}/{toObjectType}/labels`
    * **Method:** `POST`
    * **Request Body:** `{label, name, inverseLabel (optional)}`
    * **Response:** `{results: [{category, typeId, label}]}`
* **Retrieve Association Labels:** `GET /associations/{fromObjectType}/{toObjectType}/labels`
    * **Method:** `GET`
* **Update Association Labels:** `PUT /associations/{fromObjectType}/{toObjectType}/labels`
    * **Method:** `PUT`
    * **Request Body:** `{associationTypeId, label, inverseLabel (optional)}`
* **Delete Association Labels:** `DELETE /associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`
    * **Method:** `DELETE`

#### Set and Manage Association Limits

* **Create or Update Association Limits:** `POST /associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (create) or `/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (update)
    * **Method:** `POST`
    * **Request Body:** `{inputs: [{category, typeId, maxToObjectIds}]}`
* **Retrieve Association Limits (All):** `GET /associations/definitions/configurations/all`
    * **Method:** `GET`
* **Retrieve Association Limits (Specific):** `GET /associations/definitions/configurations/{fromObjectType}/{toObjectType}`
    * **Method:** `GET`
* **Delete Association Limits:** `POST /associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
    * **Method:** `POST`
    * **Request Body:** `{inputs: [{category, typeId}]}`

#### High Association Usage Report

* `POST /associations/usage/high-usage-report/{userID}`
    * **Method:** `POST`
    * Sends a report to the user's email address.


## Example Responses

See the original text for numerous example request and response bodies.

## Object Type ID Values

See the original text for a comprehensive table of HubSpot-defined `associationTypeId` values for various object types and association directions.


## Limitations

* **Daily Limits:** 500,000 requests (Professional and Enterprise accounts).  Can be increased to 1,000,000 with an API limit increase purchase (but this will not increase the limit for association API requests further).
* **Burst Limits:** 100 requests per 10 seconds (Free and Starter accounts), 150 requests per 10 seconds (Professional and Enterprise accounts). Can be increased to 200 requests per 10 seconds with an API limit increase purchase (but this will not increase the limit for association API requests further).


This markdown provides a structured and concise overview of the HubSpot CRM v4 Associations API. Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
