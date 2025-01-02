# HubSpot Custom Objects API Documentation

This document details the HubSpot API for creating, managing, and interacting with custom objects.  Custom objects extend the standard HubSpot CRM objects (contacts, companies, deals, tickets) to represent your specific business data.

## Supported Products

This API requires one of the following HubSpot products (Enterprise tier or higher):

* Marketing Hub Enterprise
* Sales Hub Enterprise
* Content Hub Enterprise
* Service Hub Enterprise
* Operations Hub Enterprise


## Authentication

The API supports two authentication methods:

* **OAuth:**  For web applications and integrations requiring user authorization.
* **Private app access tokens:** For server-side applications and integrations that don't require explicit user interaction.

**Note:** HubSpot API Keys are deprecated as of November 30, 2022.  Use private app access tokens or OAuth instead.


## API Endpoints

All endpoints are based on `https://api.hubapi.com/crm/v3/`.


### 1. Create a Custom Object

**Endpoint:** `/schemas`
**Method:** `POST`

**Request Body:**  The request body defines the object schema, including:

* `name`: (string, required) The object name (alphanumeric and underscores only, must start with a letter).  This cannot be changed after creation.
* `description`: (string, optional)  A description of the object.
* `labels`: (object, required)  Singular and plural labels for the object.
    * `singular`: (string, required) Singular label.
    * `plural`: (string, required) Plural label.
* `primaryDisplayProperty`: (string, required) The property used to display object records.
* `secondaryDisplayProperties`: (array of strings, optional) Additional properties displayed in the UI.  The first property of this array will also be added as a fourth filter on the object index page if it’s one of the following property types: string, number, enumeration, boolean, datetime.
* `searchableProperties`: (array of strings, optional) Properties indexed for searching.
* `requiredProperties`: (array of strings, required) Properties required when creating a new record.
* `properties`: (array of objects, required)  Definition of object properties.  See "Properties" section below.
* `associatedObjects`: (array of strings, optional)  Associated standard or custom objects (identified by name or `objectTypeId`).


**Example Request:**

```json
{
  "name": "cars",
  "description": "Car inventory",
  "labels": {"singular": "Car", "plural": "Cars"},
  "primaryDisplayProperty": "model",
  "secondaryDisplayProperties": ["make"],
  "searchableProperties": ["year", "make", "vin", "model"],
  "requiredProperties": ["year", "make", "vin", "model"],
  "properties": [
    {"name": "year", "label": "Year", "type": "number", "fieldType": "number"}
    // ... other properties
  ],
  "associatedObjects": ["CONTACT"]
}
```

**Response:** Contains the created object's `id` and other details.


### 2. Retrieve Custom Objects

**Endpoint:** `/schemas`
**Method:** `GET` (all objects) or `GET /schemas/{objectTypeId}` (specific object)

`/schemas/{objectTypeId}` parameters:

* `{objectTypeId}`: The ID of the custom object.
* `p_{object_name}`: The object name preceded by 'p_'.
* `{fullyQualifiedName}`:  Derived from `p{portal_id}_{object_name}`.


**Response:**  An array of custom object schemas or a single schema.


### 3. Retrieve Custom Object Records

**Endpoint:** `/objects/{objectType}/{recordId}` (single record) or `/objects/{objectType}/batch/read` (multiple records)
**Method:** `GET` (single) or `POST` (batch)

**Parameters:**

* `/objects/{objectType}`:  Custom object type ID or `p_{object_name}`.
* `/objects/{recordId}`: The ID of the record.
* Query parameters (for both):
    * `properties`: Comma-separated list of properties to return.
    * `propertiesWithHistory`: Comma-separated list of properties to return, including historical data.
    * `associations`: Comma-separated list of associated objects to retrieve.

**Batch Request Body:**

```json
{
  "properties": ["property1", "property2"],
  "inputs": [{"id": "recordId1"}, {"id": "recordId2"}]
}
```


**Response:**  The requested record(s) and their properties.


### 4. Update a Custom Object

**Endpoint:** `/schemas/{objectTypeId}`
**Method:** `PATCH`

**Request Body:**  Includes changes to the schema (e.g., adding/removing properties, changing display properties).  Properties cannot be deleted; you must recreate properties with the new definitions.


### 5. Update Associations

**Endpoint:** `/schemas/{objectTypeId}/associations`
**Method:** `POST`

**Request Body:** Defines a new association between the custom object and another object (standard or custom).

* `fromObjectTypeId`: The ID of the custom object.
* `toObjectTypeId`: The ID of the associated object (name or ID).
* `name`: The name of the association.


### 6. Delete a Custom Object

**Endpoint:** `/schemas/{objectType}` or `/schemas/{objectType}?archived=true`
**Method:** `DELETE`

**Note:**  You can only delete a custom object after deleting all its records and associations. Use `?archived=true` for a hard delete to allow recreating an object with the same name.


## Properties

When defining properties, you can specify the following:

* `name`: (string, required)  Property name (alphanumeric and underscores).
* `label`: (string, required)  User-friendly label.
* `type`: (string, required) Property type (e.g., `string`, `number`, `date`, `enumeration`, `boolean`).
* `fieldType`: (string, required) UI field type (e.g., `text`, `textarea`, `number`, `select`, `checkbox`, `radio`, `date`, `file`).
* `options`: (array of objects, required for `enumeration`)  Options for enumeration properties.
* `hasUniqueValue`: (boolean, optional) Indicates if the property must have a unique value.


## Associations

You can define associations between your custom object and standard HubSpot objects or other custom objects.  Use the object's name (for standard objects) or `objectTypeId` (for custom objects) to specify the associated object.


## Example: Creating a "Cars" Custom Object

The provided example in the original text demonstrates a complete workflow, including creating the schema, adding records, creating associations, and adding properties. Follow the steps and API calls outlined in the original text for a detailed walkthrough.


This documentation provides a comprehensive overview of the HubSpot Custom Objects API.  Refer to the HubSpot Developer documentation for the most up-to-date information and further details.
