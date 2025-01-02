# HubSpot Custom Objects API Documentation

This document details the HubSpot Custom Objects API, allowing you to create, manage, and interact with custom objects within your HubSpot account.

## Supported Products

Requires one of the following HubSpot products or higher:

* Marketing Hub - Enterprise
* Sales Hub - Enterprise
* Content Hub - Enterprise
* Service Hub - Enterprise
* Operations Hub - Enterprise


## Authentication

Use one of the following authentication methods:

* **OAuth:**  Recommended for secure access.
* **Private app access tokens:**  Provides API access for your app.

**Note:** HubSpot API Keys are deprecated as of November 30, 2022.


## Custom Objects Overview

Beyond HubSpot's standard CRM objects (contacts, companies, deals, tickets), custom objects let you represent and organize your data.  You can create them within HubSpot or via this API.  Each account has limits on the number of custom objects; check your HubSpot Products & Services catalog for details.


## API Endpoints

All endpoints are prefixed with `/crm/v3/`.

### 1. Create a Custom Object

* **Endpoint:** `/schemas`
* **Method:** `POST`
* **Request Body:**  Defines the object schema.  See "Object Schema Definition" below for details.  The object name cannot be changed after creation.  It must start with a letter and only contain letters, numbers, and underscores.

**Example Request:** (See complete example in the original text)

```json
{
  "name": "cars",
  "description": "...",
  "labels": { ... },
  "properties": [ ... ],
  "associatedObjects": ["CONTACT"]
}
```

**Response:** Includes the `objectTypeId` and `fullyQualifiedName` of the newly created object.


### 2. Retrieve Existing Custom Objects

* **Endpoint:** `/schemas`
* **Method:** `GET`
* **Retrieves:** All custom objects in the account.

* **Endpoint:** `/schemas/{objectTypeId}`
* **Method:** `GET`
* **Retrieves:** A specific custom object by its `objectTypeId`.

* **Endpoint:** `/schemas/p_{object_name}`
* **Method:** `GET`
* **Retrieves:** A specific custom object by its name.

* **Endpoint:** `/schemas/{fullyQualifiedName}`
* **Method:** `GET`
* **Retrieves:**  A specific custom object by its fully qualified name (`p{portal_id}_{object_name}`).

**Example URL (using objectTypeId):**

`https://api.hubapi.com/crm/v3/schemas/2-3465404`


### 3. Retrieve Custom Object Records

* **Endpoint:** `/objects/{objectType}/{recordId}`
* **Method:** `GET`
* **Retrieves:** A single record by its `recordId`.  Uses query parameters `properties`, `propertiesWithHistory`, and `associations` to control the returned data.


* **Endpoint:** `/objects/{objectType}/batch/read`
* **Method:** `POST`
* **Retrieves:** Multiple records.  Request body includes `inputs` (array of IDs) and optionally `idProperty` (for custom unique identifiers) and `properties` or `propertiesWithHistory`.  **Note:** Associations cannot be retrieved via the batch endpoint.

**Example Request (by record ID):**

```json
{
  "properties": ["petname"],
  "inputs": [{"id": "12345"}, {"id": "67891"}]
}
```


### 4. Update Existing Custom Objects

* **Endpoint:** `/schemas/{objectTypeId}`
* **Method:** `PATCH`
* **Request Body:** Updates the object schema.  You cannot change the object's name or labels.  You *can* update `requiredProperties`, `searchableProperties`, `primaryDisplayProperty`, and `secondaryDisplayProperties`.  You must first create new properties via the Properties API before updating the schema to include them.

### 5. Update Associations

* **Endpoint:** `/schemas/{objectTypeId}/associations`
* **Method:** `POST`
* **Request Body:** Adds new associations to the custom object.  Use `objectTypeId` for custom objects, and names (e.g., "CONTACT") for standard objects.

**Example Request:**

```json
{
  "fromObjectTypeId": "2-3444025",
  "toObjectTypeId": "ticket",
  "name": "cat_to_ticket"
}
```

### 6. Delete a Custom Object

* **Endpoint:** `/schemas/{objectType}`
* **Method:** `DELETE`
* **Deletes:** The custom object.  Requires all associated records to be deleted first.

* **Endpoint:** `/schemas/{objectType}?archived=true`
* **Method:** `DELETE`
* **Deletes:**  Performs a hard delete of the schema, allowing you to recreate an object with the same name. Requires all associated records, associations and properties to be deleted first.


## Object Schema Definition

When creating or updating a custom object, you define its schema:

* **`name` (string):** The object's internal name.
* **`description` (string):**  A description of the object.
* **`labels` (object):**  `singular` and `plural` labels for the object.
* **`primaryDisplayProperty` (string):** The property used to display the object's name.
* **`secondaryDisplayProperties` (array of strings):** Additional properties displayed with the primary property.
* **`searchableProperties` (array of strings):** Properties indexed for search.
* **`requiredProperties` (array of strings):** Properties required when creating records.
* **`properties` (array of objects):**  Defines the object's properties (see below).
* **`associatedObjects` (array of strings):**  Objects this custom object can be associated with (use `objectTypeId` for custom objects).

### Property Definition

Each property in the `properties` array has the following fields:

* **`name` (string):** The property's internal name.
* **`label` (string):** The property's display label.
* **`type` (string):**  The property's data type (`string`, `number`, `enumeration`, `date`, `dateTime`, `boolean`).
* **`fieldType` (string):** The UI field type (`text`, `textarea`, `number`, `select`, `checkbox`, `radio`, `date`, `file`, `booleancheckbox`).
* **`options` (array of objects):** (For `enumeration` type) An array of label-value pairs.
* **`hasUniqueValue` (boolean):** (Optional) Set to `true` if the property should have unique values.


## Example Walkthrough (Car Dealership)

A detailed example demonstrating the creation and management of a "Cars" custom object is provided within the original text.  This example covers schema creation, record creation, association creation (with contacts and tickets), property definition, and schema updates.


## Error Handling

The API returns standard HTTP status codes to indicate success or failure.  Error responses will include details about the error.


## Rate Limits

Be aware of HubSpot's API rate limits to avoid throttling.


This markdown documentation provides a comprehensive overview of the HubSpot Custom Objects API.  Refer to the original text for detailed code examples and response structures. Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
