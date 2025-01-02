# HubSpot Custom Objects API Documentation

This document details the HubSpot Custom Objects API, allowing developers to create, manage, and interact with custom objects within their HubSpot accounts.  This API extends the standard CRM objects (Contacts, Companies, Deals, Tickets) to accommodate specific business needs.


## Supported Products

This API requires one of the following HubSpot products (Enterprise tier or higher):

* Marketing Hub Enterprise
* Sales Hub Enterprise
* Content Hub Enterprise
* Service Hub Enterprise
* Operations Hub Enterprise


## Authentication

The API supports two authentication methods:

* **OAuth:**  Standard OAuth 2.0 flow for secure access.
* **Private App Access Tokens:**  Generated within your HubSpot Private App.

**Note:** HubSpot API Keys are deprecated and no longer supported as of November 30, 2022.


## API Endpoints

All endpoints are prefixed with `https://api.hubapi.com/crm/v3/`.

### 1. Custom Object Schema Management

* **`schemas` (POST): Create a Custom Object**

    * **Request:**  JSON payload defining the object schema (see "Object Schema Definition" below).
    * **Example Request:** (See example in original text)
    * **Response:**  JSON object containing the newly created object's details, including `objectTypeId` and `fullyQualifiedName`.
    * **Example Response:** (See example in original text)

* **`schemas` (GET): Retrieve All Custom Objects**

    * **Request:**  No request body.
    * **Response:**  JSON array containing details for all custom objects in the account.

* **`schemas/{objectTypeId}` (GET): Retrieve a Specific Custom Object**

    * **Request:**  `objectTypeId` is the unique identifier of the custom object.
    * **Response:**  JSON object representing the specified custom object's schema.

* **`schemas/p_{object_name}` (GET): Retrieve a Specific Custom Object (by name)**

    * **Request:** `object_name` is the name of the custom object.
    * **Response:** JSON object representing the specified custom object's schema.


* **`schemas/{fullyQualifiedName}` (GET): Retrieve a Specific Custom Object (by fully qualified name)**

    * **Request:** `fullyQualifiedName` is the fully qualified name (e.g., `p1234_lender`).
    * **Response:** JSON object representing the specified custom object's schema.

* **`schemas/{objectTypeId}` (PATCH): Update a Custom Object's Schema**

    * **Request:** JSON payload containing changes to the object's schema.  Only `requiredProperties`, `searchableProperties`, `primaryDisplayProperty`, and `secondaryDisplayProperties` can be updated.  New properties must be created separately using the Properties API before updating the schema.
    * **Response:** Updated custom object schema.

* **`schemas/{objectTypeId}/associations` (POST): Add Object Associations**

    * **Request:** JSON payload specifying the association (see "Associations" below).
    * **Response:**  JSON object representing the new association.


* **`schemas/{objectTypeId}` (DELETE): Delete a Custom Object**

    * **Request:**  Requires all records of the object type to be deleted first. To completely delete (hard delete) use `?archived=true` query parameter.
    * **Response:**  Success status.


### 2. Custom Object Record Management


* **`objects/{objectType}/{recordId}` (GET): Retrieve a Specific Custom Object Record**

    * **Request:** `objectType` is the `objectTypeId`; `recordId` is the ID of the record. Query parameters: `properties`, `propertiesWithHistory`, `associations`.
    * **Response:** JSON object representing the record.

* **`objects/{objectType}/batch/read` (POST): Retrieve Multiple Custom Object Records**

    * **Request:** JSON payload with `inputs` array (each input having an `id` - record ID or unique identifier if `idProperty` is specified), `properties`, `propertiesWithHistory`, and optional `idProperty` (for unique identifier lookups).
    * **Response:** JSON array containing the requested records.  Associations cannot be retrieved via this endpoint.

* **`objects/{objectType}` (POST): Create a Custom Object Record**

    * **Request:** JSON payload with properties to create.
    * **Response:**  JSON object with the created record's details, including its ID.

* **`objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}/{associationType}` (PUT): Create an Association between two Records**

   * **Request:** The association is created using the ID of the existing custom object record and the ID of another record.
   * **Response:** Success status.



### 3. Properties API

* **`properties/{objectTypeId}` (POST): Create a new Property**

    * **Request:** JSON payload defining the property (name, label, type, etc.).
    * **Response:**  JSON object with details of the created property.


## Object Schema Definition

The schema for creating a custom object includes:

* `name`:  (String) The internal name of the object (cannot be changed after creation).
* `description`: (String) Description of the object.
* `labels`: (Object)  Singular and plural labels for the object.
* `primaryDisplayProperty`: (String) The property used to display the object's name.
* `secondaryDisplayProperties`: (Array of Strings)  Properties displayed in the object's sidebar.
* `searchableProperties`: (Array of Strings) Properties indexed for searching.
* `requiredProperties`: (Array of Strings) Properties required when creating new records.
* `properties`: (Array of Objects)  Detailed definitions of each property (name, label, type, fieldType, options for enumeration types, etc.).  See Property Types below.
* `associatedObjects`: (Array of Strings)  IDs of associated standard and custom objects.


## Property Types

| `type`       | Description                                      | `fieldType` Values            |
|--------------|--------------------------------------------------|-------------------------------|
| `enumeration` | A set of options (semicolon-separated string)    | `checkbox`, `radio`, `select` |
| `date`        | ISO 8601 formatted date (YYYY-MM-DD)             | `date`                         |
| `dateTime`    | ISO 8601 formatted datetime (YYYY-MM-DDTHH:mm:ss) | `date`                         |
| `string`      | Plain text string (up to 65,536 characters)     | `text`, `textarea`, `file`     |
| `number`      | Numeric value                                     | `number`                      |


## Associations

Associations link custom objects to other objects (standard or custom).  When creating an association:

* Standard objects are identified by their name (e.g., "CONTACT", "COMPANY").
* Custom objects are identified by their `objectTypeId`.


## Example Walkthrough (Car Dealership)

(A complete example walkthrough is provided in the original text, demonstrating object creation, record creation, association creation, and property creation and updating)


## Rate Limits

HubSpot APIs have rate limits.  Refer to HubSpot's documentation for details on these limits.

## Error Handling

The API returns standard HTTP status codes and JSON error responses for error conditions. Consult HubSpot's API documentation for details on error codes.
