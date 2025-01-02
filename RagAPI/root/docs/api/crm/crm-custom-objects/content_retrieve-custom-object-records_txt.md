# HubSpot Custom Objects API Documentation

This document details the HubSpot API for managing custom objects.  Custom objects extend the standard HubSpot CRM objects (contacts, companies, deals, tickets) to represent your specific business needs.

## Supported Products

Requires one of the following HubSpot products or higher:

* Marketing Hub - Enterprise
* Sales Hub - Enterprise
* Content Hub - Enterprise
* Service Hub - Enterprise
* Operations Hub - Enterprise


## Authentication

Use one of the following authentication methods:

* **OAuth:**  Recommended for most integrations.
* **Private App Access Tokens:**  Suitable for internal apps and integrations with restricted access.

**Note:** HubSpot API Keys are deprecated as of November 30, 2022.


## API Endpoints

All endpoints are under the base URL: `https://api.hubapi.com/crm/v3/`


### 1. Create a Custom Object

**Endpoint:** `/schemas`

**Method:** `POST`

**Request Body:**  The request body defines the object schema, including:

* `name`:  Object name (alphanumeric and underscores only, must start with a letter).  Cannot be changed after creation.
* `description`:  A description of the object.
* `labels`:  Singular and plural labels for the object.
* `primaryDisplayProperty`:  The property used to display the object's name.
* `secondaryDisplayProperties`:  Additional properties displayed on the object record.  The first property here, if it's a `string`, `number`, `enumeration`, `boolean`, or `datetime` type, is added as a fourth filter on the object index page.
* `searchableProperties`:  Properties indexed for searching.
* `requiredProperties`: Properties required when creating new records.
* `properties`: An array of property definitions (see section below).
* `associatedObjects`: An array of object IDs or names to associate with (e.g., `"CONTACT"`, `"COMPANY"`, `"TICKET"`, `"DEAL"`, or a custom object's `objectTypeId`).

**Example Request Body:** (See complete example in original text)

**Response:**  Returns the created object schema, including its `objectTypeId`.


### 2. Properties

**Defining Properties (during schema creation):** Properties are defined within the `properties` array of the create schema request.  Each property object includes:

* `name`: Property name.
* `label`: Property label.
* `type`: Property type (`enumeration`, `date`, `dateTime`, `string`, `number`).
* `fieldType`:  UI field type (`booleancheckbox`, `checkbox`, `date`, `file`, `number`, `radio`, `select`, `text`, `textarea`).
* `options` (for `enumeration` type): An array of option objects, each with `label` and `value`.
* `hasUniqueValue`: (boolean) True if the property must have unique values.


**Updating Properties:** Use the properties API (`/crm/v3/properties/{objectTypeId}`) to create, update, and delete properties after the schema is created.


### 3. Retrieve Custom Objects

**Endpoint:** `/schemas`

**Method:** `GET` (for all objects)  or `GET` `/schemas/{objectTypeId}` or `/schemas/p_{object_name}` or `/schemas/{fullyQualifiedName}` (for a specific object).


**Response:**  Returns an array of custom object schemas (for `GET /schemas`) or a single custom object schema.


### 4. Retrieve Custom Object Records

**Endpoint:** `/objects/{objectType}/{recordId}` (single record) or `/objects/{objectType}/batch/read` (multiple records)

**Method:** `GET` (single) or `POST` (batch)

**Query Parameters (single record):**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`:  Comma-separated list of properties to return with history.
* `associations`: Comma-separated list of associated objects to retrieve.

**Request Body (batch):**

* `properties`:  Array of properties to return.
* `propertiesWithHistory`: Array of properties to return with history.
* `inputs`:  Array of input objects, each with an `id` (record ID or unique identifier, depending on `idProperty`).
* `idProperty`: Name of the unique identifier property (if not using record ID).


**Example Batch Request Body (record ID):** (See complete example in original text)

**Example Batch Request Body (unique value property):** (See complete example in original text)


**Response:** Returns the requested custom object record(s).


### 5. Update Existing Custom Objects

**Endpoint:** `/schemas/{objectTypeId}`

**Method:** `PATCH`

**Request Body:**  Only certain fields can be updated (e.g., `requiredProperties`, `searchableProperties`, `primaryDisplayProperty`, `secondaryDisplayProperties`).  Adding a new property requires first creating it via the properties API.

**Response:** Returns the updated custom object schema.


### 6. Update Associations

**Endpoint:** `/schemas/{objectTypeId}/associations`

**Method:** `POST` (to add associations)

**Request Body:**

* `fromObjectTypeId`:  The ID of the custom object.
* `toObjectTypeId`: The ID or name of the object to associate with.
* `name`:  The name of the association.


**Example Request Body:** (See complete example in original text)


**Response:** Returns the created association.


### 7. Delete a Custom Object

**Endpoint:** `/schemas/{objectType}` (soft delete) or `/schemas/{objectType}?archived=true` (hard delete)

**Method:** `DELETE`

**Note:** Soft delete requires all object instances, associations, and properties to be deleted first.  Hard delete permanently removes the schema.


## Example Walkthrough (Car Dealership)

The provided text contains a detailed walkthrough of creating a "Cars" custom object, including creating the schema, adding records, associating with contacts and tickets, and defining new properties and associations.  This example showcases the API calls and responses for each step. (Refer to the original text for the step-by-step details).


This documentation provides a comprehensive overview of the HubSpot Custom Objects API.  Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
