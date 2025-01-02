# HubSpot Custom Objects API Documentation

This document details the HubSpot Custom Objects API, allowing you to create, manage, and interact with custom objects within your HubSpot account.

## Supported Products

This API requires one of the following HubSpot products (or higher):

* Marketing Hub Enterprise
* Sales Hub Enterprise
* Content Hub Enterprise
* Service Hub Enterprise
* Operations Hub Enterprise


## Authentication

You can authenticate using either:

* **OAuth:**  Recommended for most integrations.
* **Private app access tokens:** Suitable for internal tools and apps.

**Note:** HubSpot API Keys are deprecated as of November 30, 2022.  Migrate existing integrations to OAuth or private app access tokens.


## API Endpoints

All endpoints are prefixed with `https://api.hubapi.com/crm/v3/`.

### 1. Custom Object Schema Management

* **Create a custom object:**
    * `POST /schemas`
    * **Request Body:**  JSON object defining the object schema (see "Object Schema Definition" below).
    * **Response:**  JSON object containing the newly created object's details, including `objectTypeId` and `fullyQualifiedName`.

* **Retrieve existing custom objects:**
    * `GET /schemas` (Retrieves all custom objects)
    * `GET /schemas/{objectTypeId}` (Retrieves a specific object by `objectTypeId`)
    * `GET /schemas/p_{object_name}` (Retrieves a specific object by name)
    * `GET /schemas/{fullyQualifiedName}` (Retrieves a specific object by fully qualified name)
    * **Response:** JSON array (for `GET /schemas`) or JSON object (for others) containing the custom object schema.


* **Update existing custom objects:**
    * `PATCH /schemas/{objectTypeId}`
    * **Request Body:** JSON object containing the properties to update.  Only `requiredProperties`, `searchableProperties`, `primaryDisplayProperty`, and `secondaryDisplayProperties` can be modified.  New properties must be created separately using the Properties API before updating the schema.
    * **Response:** Updated custom object schema.

* **Delete a custom object:**
    * `DELETE /schemas/{objectType}` (Soft delete - object can be recreated)
    * `DELETE /schemas/{objectType}?archived=true` (Hard delete - object cannot be recreated with the same name)
    * **Response:** Confirmation of deletion.


### 2. Custom Object Records

* **Create a custom object record:**
    * `POST /objects/{objectType}`
    * **Request Body:** JSON object with `properties` field containing the record data.
    * **Response:**  JSON object representing the created record, including the `id`.

* **Retrieve custom object records:**
    * `GET /objects/{objectType}/{recordId}` (Retrieves a single record)
        * Query parameters: `properties`, `propertiesWithHistory`, `associations`.
    * `POST /objects/{objectType}/batch/read` (Retrieves multiple records)
        * Request Body: JSON object with `inputs` array (each containing `id`), `properties`, `propertiesWithHistory` (cannot retrieve associations via batch).  Use `idProperty` to specify a custom unique identifier instead of `hs_object_id`.
    * **Response:**  JSON object (single record) or JSON array (multiple records).


* **Update existing custom objects:** (Not explicitly documented, implied by overall structure)
    * Likely a `PATCH` request to `/objects/{objectType}/{recordId}`
    * **Request Body:** JSON object with updated `properties`.

* **Delete a custom object record:** (Not explicitly documented, implied by overall structure)
    * Likely a `DELETE` request to `/objects/{objectType}/{recordId}`



### 3. Associations

* **Create an association between records:**
    * `PUT /objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}/{associationType}`
* **Create a new association definition between custom objects:**
    * `POST /schemas/{objectTypeId}/associations`
    * **Request Body:** JSON object with `fromObjectTypeId`, `toObjectTypeId`, and `name`.
    * **Response:** JSON object representing the new association.

## Object Schema Definition

When creating or updating a custom object schema, the request body should include:

* `name`:  The object's internal name (alphanumeric and underscores only; first character must be a letter).
* `description`: Description of the object.
* `labels`:  Singular and plural labels.
* `primaryDisplayProperty`: The property used to display the object's name.
* `secondaryDisplayProperties`: Properties displayed in the record sidebar.
* `searchableProperties`: Properties indexed for search.
* `requiredProperties`:  Properties required when creating new records.
* `properties`: An array of property definitions (see below).
* `associatedObjects`: An array of associated object type IDs or names (e.g., `CONTACT`, `COMPANY`, `TICKET`, `DEAL`, or a custom object's `objectTypeId`).


### Property Definitions

Each property definition within the `properties` array should include:

* `name`: Internal property name.
* `label`: Display label.
* `type`: Property type (`string`, `number`, `date`, `dateTime`, `enumeration`, `boolean`).
* `fieldType`: UI field type (`text`, `textarea`, `number`, `date`, `checkbox`, `radio`, `select`, `file`).
* `options` (for `enumeration` type): An array of option objects, each with `label` and `value`.
* `hasUniqueValue` (optional, for `string` type):  Indicates if the property should have a unique value.


## Example Walkthrough

The provided document includes a detailed walkthrough of creating a "Cars" custom object, including schema creation, record creation, association creation, property creation, and schema updates.  Refer to the original document for the complete example.


## Rate Limits

The API has rate limits. Refer to HubSpot's documentation for details on these limits.


This markdown documentation provides a structured overview of the HubSpot Custom Objects API. Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
