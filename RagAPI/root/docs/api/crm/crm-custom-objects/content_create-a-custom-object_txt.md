# HubSpot Custom Objects API Documentation

This document details the HubSpot Custom Objects API, allowing developers to create, manage, and interact with custom objects within their HubSpot accounts.

## Supported Products

Requires one of the following HubSpot products or higher:

* Marketing Hub - Enterprise
* Sales Hub - Enterprise
* Content Hub - Enterprise
* Service Hub - Enterprise
* Operations Hub - Enterprise


## Authentication

The API supports two authentication methods:

* **OAuth:**  Recommended for secure access.
* **Private app access tokens:**  Suitable for internal applications.

**Note:** HubSpot API Keys are deprecated and no longer supported as of November 30, 2022.


##  API Endpoints

All endpoints are under the base URL: `https://api.hubapi.com/crm/v3/`

### 1. Create a Custom Object

**Endpoint:** `/schemas`

**Method:** `POST`

**Request Body:**  Requires a JSON payload defining the object schema:

* `name` (string): The object's name (alphanumeric and underscores only, must start with a letter).  Cannot be changed after creation.
* `description` (string): Description of the object.
* `labels` (object):  `singular` and `plural` labels for the object.
* `primaryDisplayProperty` (string):  Name of the property used to display object records.
* `secondaryDisplayProperties` (array of strings):  Additional properties displayed with `primaryDisplayProperty`. The first property of this array will be added as a fourth filter on the object index page if its type is string, number, enumeration, boolean, or datetime.
* `searchableProperties` (array of strings): Properties indexed for searching.
* `requiredProperties` (array of strings): Properties required when creating a new record.
* `properties` (array of objects): Defines individual properties.  Each object requires:
    * `name` (string): Property name.
    * `label` (string): Property label.
    * `type` (string): Property type (`string`, `number`, `enumeration`, `date`, `dateTime`, `boolean`).
    * `fieldType` (string): UI field type (`text`, `textarea`, `number`, `select`, `radio`, `checkbox`, `booleancheckbox`, `date`, `file`).
    * `options` (array of objects, optional for `enumeration` type): Array of option objects, each with `label` and `value`.
    * `hasUniqueValue` (boolean, optional):  Indicates if the property should have a unique value.

* `associatedObjects` (array of strings): Object IDs of associated HubSpot objects (e.g., `"CONTACT"`, `"COMPANY"`,  or custom object `objectTypeId`).


**Example Request:** (See example in provided text)

**Response:**  Returns the created object schema, including its `objectTypeId` and `fullyQualifiedName`.


### 2. Retrieve Existing Custom Objects

**Endpoint:** `/schemas`

**Method:** `GET`  (for all objects)

**Endpoint:** `/schemas/{objectTypeId}` or `/schemas/p_{object_name}` or `/schemas/{fullyQualifiedName}`

**Method:** `GET` (for a specific object)


**Response:** Returns a JSON array or single object representing the custom object schema(s).


### 3. Retrieve Custom Object Records

**Endpoint:** `/objects/{objectType}/{recordId}`

**Method:** `GET` (single record)

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including history.
* `associations`: Comma-separated list of associated objects to retrieve IDs for.

**Endpoint:** `/objects/{objectType}/batch/read`

**Method:** `POST` (multiple records)

**Request Body:**  JSON payload with:

* `properties`:  Array of properties to return.
* `propertiesWithHistory`:  Array of properties to return with history.
* `idProperty`: (optional) Name of a custom unique identifier property.  Use this if not using `hs_object_id`.
* `inputs`: Array of input objects, each with an `id` (record ID or unique identifier value).

**Example Request (single):**  (See example in provided text)
**Example Request (batch):** (See example in provided text)


**Response:** Returns a JSON array of custom object records or a single record with requested properties.


### 4. Update Existing Custom Objects

**Endpoint:** `/schemas/{objectTypeId}`

**Method:** `PATCH`

**Request Body:** JSON payload containing updates to the schema.  Only `requiredProperties`, `searchableProperties`, `primaryDisplayProperty`, and `secondaryDisplayProperties` can be updated.  New properties must be created separately using the properties API.

**Example Request:** (See example in provided text)


**Response:** Returns the updated object schema.


### 5. Update Associations

**Endpoint:** `/schemas/{objectTypeId}/associations`

**Method:** `POST`

**Request Body:** JSON payload:

* `fromObjectTypeId`:  ID of the custom object.
* `toObjectTypeId`: ID of the associated object (standard object name or custom object `objectTypeId`).
* `name`: Name of the association.

**Example Request:** (See example in provided text)


**Response:** Returns the newly created association details.


### 6. Delete a Custom Object

**Endpoint:** `/schemas/{objectType}`

**Method:** `DELETE` (soft delete; object can be recreated)

**Endpoint:** `/schemas/{objectType}?archived=true`

**Method:** `DELETE` (hard delete; prevents recreating with the same name)

**Note:**  All instances of the object, associated data, and properties must be deleted before deletion is possible.


## Example Walkthrough (Car Dealership)

A detailed example walkthrough is included in the original text, demonstrating schema creation, record creation, associations, and property management.  Refer to that section for a comprehensive practical example.


## Error Handling

The API returns standard HTTP status codes to indicate success or failure.  Error responses will include detailed JSON error messages.


This documentation provides a concise overview of the HubSpot Custom Objects API. Refer to the original text for complete details, including code examples and response structures.  Remember to consult the official HubSpot API documentation for the most up-to-date information.
