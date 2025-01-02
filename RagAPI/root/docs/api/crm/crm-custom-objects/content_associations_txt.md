# HubSpot Custom Objects API Documentation

This document details the HubSpot Custom Objects API, allowing you to create, manage, and interact with custom objects within your HubSpot account.  Requires Marketing Hub, Sales Hub, Content Hub, Service Hub, or Operations Hub Enterprise.


## Authentication

The API supports two authentication methods:

* **OAuth:**  Use OAuth 2.0 for secure authorization.  See HubSpot's OAuth documentation for details.
* **Private App Access Tokens:** Generate a private app access token within your HubSpot account.  This is the recommended approach over deprecated API Keys.


## API Endpoints

All endpoints are under the `/crm/v3` base path.  Remember to replace placeholders like `{objectTypeId}` and `{recordId}` with actual values.

### 1. Custom Object Schema Management

**a) Create a Custom Object:**

* **Method:** `POST`
* **Endpoint:** `/schemas`
* **Request Body:**  JSON object defining the object schema (see detailed example below).  Includes:
    * `name`: Object name (alphanumeric and underscores only, must start with a letter).
    * `description`: Description of the object.
    * `labels`: Singular and plural labels.
    * `properties`: Array of property definitions (see below).
    * `associatedObjects`: Array of associated object IDs (e.g., `"CONTACT"`, `"COMPANY"`, or a custom object's `objectTypeId`).
    * `primaryDisplayProperty`: Name of the primary display property.
    * `secondaryDisplayProperties`: Array of secondary display properties.
    * `searchableProperties`: Array of searchable properties.
    * `requiredProperties`: Array of required properties.

* **Response:** JSON object containing the created object's schema, including `objectTypeId` and `fullyQualifiedName`.

**b) Retrieve Custom Objects:**

* **Method:** `GET`
* **Endpoint:** `/schemas` (all objects) or `/schemas/{objectTypeId}`, `/schemas/p_{object_name}`, `/schemas/{fullyQualifiedName}` (specific object)
* **Response:** JSON array (for `/schemas`) or JSON object (for specific object) containing custom object schemas.

**c) Update a Custom Object:**

* **Method:** `PATCH`
* **Endpoint:** `/schemas/{objectTypeId}`
* **Request Body:** JSON object with the properties to update (e.g., `secondaryDisplayProperties`, `requiredProperties`, etc.).  **Note:**  Object name and labels cannot be changed.
* **Response:** Updated custom object schema.

**d) Delete a Custom Object:**

* **Method:** `DELETE`
* **Endpoint:** `/schemas/{objectTypeId}` (soft delete) or `/schemas/{objectTypeId}?archived=true` (hard delete).  Hard delete is only possible if all object instances, associations, and properties are deleted first.
* **Response:** Success or error message.


### 2. Custom Object Record Management

**a) Create a Custom Object Record:**

* **Method:** `POST`
* **Endpoint:** `/objects/{objectTypeId}`
* **Request Body:** JSON object with `properties`: a key-value pair of property names and values.
* **Response:** JSON object representing the newly created record, including the `id`.

**b) Retrieve Custom Object Records:**

* **Method:** `GET` (single record) or `POST` (batch read)
* **Endpoint:** `/objects/{objectTypeId}/{recordId}` (single) or `/objects/{objectTypeId}/batch/read` (batch)
* **Query Parameters (GET):** `properties`, `propertiesWithHistory`, `associations`
* **Request Body (POST):** JSON object with `inputs` (array of record IDs or unique identifier values), `properties` or `propertiesWithHistory`, and optionally `idProperty` if using a custom unique identifier.
* **Response:** JSON object (single record) or JSON array (batch read) of records.


**c) Update a Custom Object Record:**

* **Method:** `PATCH`
* **Endpoint:** `/objects/{objectTypeId}/{recordId}`
* **Request Body:** JSON object with `properties`: key-value pairs of properties to update.
* **Response:** Updated record details.


### 3. Custom Object Associations

**a) Create a New Association:**

* **Method:** `POST`
* **Endpoint:** `/schemas/{objectTypeId}/associations`
* **Request Body:** JSON object:
    * `fromObjectTypeId`: ID of the source custom object.
    * `toObjectTypeId`: ID of the target object (custom or standard - use names for standard objects).
    * `name`: Name of the association.
* **Response:**  The created association details.

**b) Associate/Disassociate Records:**

* **Method:** `PUT` (associate) or `DELETE` (disassociate)
* **Endpoint:** `/objects/{objectTypeId}/{objectId}/associations/{toObjectType}/{toObjectId}/{associationType}`.  Requires the `associationType` ID, which is retrieved from object schema.
* **Response:** Success or error message.



### 4. Custom Object Properties

**a) Create a Custom Property:**

* **Method:** `POST`
* **Endpoint:** `/properties/{objectTypeId}`
* **Request Body:** JSON object defining the property (name, label, type, fieldType, etc.).
* **Response:** The created property details.

**b) Update a Custom Property:** (Not explicitly detailed in provided text, but assumed possible via PATCH)

**c) Delete a Custom Property:** (Not explicitly detailed in provided text, but assumed possible via DELETE)


## Property Types and Field Types

| Type        | Description                                      | Valid `fieldType` Values |
|-------------|--------------------------------------------------|--------------------------|
| `enumeration` | Set of options (semicolon-separated)           | `checkbox`, `radio`, `select` |
| `date`       | ISO 8601 formatted date (YYYY-MM-DD)            | `date`                    |
| `dateTime`   | ISO 8601 formatted date and time               | `date`                    |
| `string`     | Plain text string (up to 65,536 characters)     | `text`, `textarea`, `file` |
| `number`     | Number value                                    | `number`                  |


## Example: Creating a "Cars" Custom Object

This example walks through creating a custom object to track car inventory, including properties, associations, and records.


**(1) Create Schema:**

```json
POST /schemas
{
  "name": "cars",
  "description": "Car inventory",
  "labels": { "singular": "Car", "plural": "Cars" },
  "primaryDisplayProperty": "model",
  "secondaryDisplayProperties": ["make"],
  "searchableProperties": ["year", "make", "vin", "model"],
  "requiredProperties": ["year", "make", "vin", "model"],
  "properties": [
    // ... property definitions (see below) ...
  ],
  "associatedObjects": ["CONTACT"]
}
```

**(2) Property Definitions (Example):**

```json
{
  "name": "make",
  "label": "Make",
  "type": "string",
  "fieldType": "text"
},
{
  "name": "vin",
  "label": "VIN",
  "type": "string",
  "hasUniqueValue": true,
  "fieldType": "text"
}
```

**(3) Create a Car Record:**

```json
POST /objects/{objectTypeId}
{
  "properties": {
    "make": "Nissan",
    "model": "Frontier",
    "vin": "12345",
    // ... other properties ...
  }
}
```

This detailed documentation provides a comprehensive overview of the HubSpot Custom Objects API.  Remember to consult the official HubSpot API documentation for the most up-to-date information and details on error handling.
