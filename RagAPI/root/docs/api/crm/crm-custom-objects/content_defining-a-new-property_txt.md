# HubSpot Custom Objects API Documentation

This document details the HubSpot Custom Objects API, allowing developers to create, manage, and interact with custom objects within their HubSpot accounts.  It requires a HubSpot account with the necessary permissions and either OAuth or a Private App access token for authentication (HubSpot API Keys are deprecated).

## Supported Products

Custom objects are available in the following HubSpot products (Enterprise tier and above):

* Marketing Hub
* Sales Hub
* Content Hub
* Service Hub
* Operations Hub

## Authentication

Use either OAuth or Private App access tokens for authentication.  API Keys are no longer supported.

## API Endpoints

All endpoints below are accessed via the base URL `https://api.hubapi.com`.  Replace `{objectTypeId}` with the unique identifier for your custom object, and `{recordId}` with the ID of a specific record.  `{fullyQualifiedName}` is derived from `p{portal_id}_{object_name}` (where `portal_id` is your account's ID and `object_name` is your object's name).

### 1. Create a Custom Object

* **Endpoint:** `/crm/v3/schemas`
* **Method:** `POST`
* **Request Body:**  JSON object defining the schema (see **Object Schema Definition** below).
* **Response:** JSON object containing the created object's details, including `objectTypeId` and `fullyQualifiedName`.

### 2. Retrieve Custom Objects

* **Endpoint:** `/crm/v3/schemas`
* **Method:** `GET`
* **Response:** JSON array containing details of all custom objects.

* **Endpoint:** `/crm/v3/schemas/{objectTypeId}` or `/crm/v3/schemas/p_{object_name}` or `/crm/v3/schemas/{fullyQualifiedName}`
* **Method:** `GET`
* **Response:** JSON object containing details of a specific custom object.


### 3. Retrieve Custom Object Records

* **Endpoint:** `/crm/v3/objects/{objectType}/{recordId}`
* **Method:** `GET`
* **Query Parameters:**
    * `properties`: Comma-separated list of properties to return.
    * `propertiesWithHistory`: Comma-separated list of properties to return with history.
    * `associations`: Comma-separated list of associated objects to retrieve.
* **Response:** JSON object containing the record's properties.

* **Endpoint:** `/crm/v3/objects/{objectType}/batch/read`
* **Method:** `POST`
* **Request Body:** JSON object with:
    * `properties`:  Comma-separated list of properties to return.
    * `idProperty`: (Optional) Name of a unique identifier property.  If omitted, `id` refers to `hs_object_id`.
    * `inputs`: Array of objects, each with an `id` property representing the record ID or unique identifier.
* **Response:** JSON object containing multiple records.  Associations cannot be retrieved via this endpoint.

### 4. Update a Custom Object

* **Endpoint:** `/crm/v3/schemas/{objectTypeId}`
* **Method:** `PATCH`
* **Request Body:** JSON object containing the updated schema properties (e.g., `requiredProperties`, `searchableProperties`, `secondaryDisplayProperties`).  The object name cannot be changed.
* **Response:** JSON object representing the updated custom object.

### 5. Update Associations

* **Endpoint:** `/crm/v3/schemas/{objectTypeId}/associations`
* **Method:** `POST`
* **Request Body:** JSON object with:
    * `fromObjectTypeId`: ID of your custom object.
    * `toObjectTypeId`: ID of the object to associate with (use object name for standard objects).
    * `name`: Name of the association.
* **Response:**  JSON object containing details of the created association.

### 6. Delete a Custom Object

* **Endpoint:** `/crm/v3/schemas/{objectType}`
* **Method:** `DELETE`
* **Query Parameter:** `archived=true` (for hard delete – required if recreating an object with the same name).
* **Note:** All instances and associated data must be deleted before the object can be deleted.

## Object Schema Definition

When creating a custom object (`POST /crm/v3/schemas`), the request body must include the following:

* `name`:  (String, required) The internal name of the object (alphanumeric and underscores only; must start with a letter).  Cannot be changed after creation.
* `description`: (String) A description of the object.
* `labels`: (Object) Singular and plural labels for the object.
* `primaryDisplayProperty`: (String) The property used to display the object's name.
* `secondaryDisplayProperties`: (Array of Strings) Properties displayed alongside the `primaryDisplayProperty`.
* `searchableProperties`: (Array of Strings) Properties indexed for searching.
* `requiredProperties`: (Array of Strings) Properties required when creating records.
* `properties`: (Array of Objects)  An array defining each property (see **Property Definition** below).
* `associatedObjects`: (Array of Strings)  Array of object type IDs or names to associate the custom object with (standard objects can be referenced by name, e.g., "CONTACT").

## Property Definition

Each property within the `properties` array requires:

* `name`: (String, required) Internal name of the property (alphanumeric and underscores only).
* `label`: (String, required)  Display name of the property.
* `type`: (String, required) Property type (e.g., `string`, `number`, `date`, `dateTime`, `enumeration`, `boolean`).
* `fieldType`: (String, required) UI field type (e.g., `text`, `textarea`, `number`, `date`, `select`, `checkbox`, `radio`).  Related to `type`.
* `options`: (Array of Objects) - For `enumeration` type, an array of `{ label, value }` objects defining each option.
* `hasUniqueValue`: (Boolean) - For `string` type, indicates if the property should have a unique value.


## Examples

See the provided text for comprehensive examples of creating, updating, and retrieving custom objects and their records.


## Error Handling

The API returns standard HTTP status codes and JSON error responses with details about any issues encountered.

## Rate Limits

HubSpot imposes rate limits on API requests.  Refer to the HubSpot API documentation for details on these limits.


This documentation provides a concise overview.  Refer to the official HubSpot API documentation for the most up-to-date information and comprehensive details.
