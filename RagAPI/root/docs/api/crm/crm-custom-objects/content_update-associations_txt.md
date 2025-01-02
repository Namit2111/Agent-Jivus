# HubSpot Custom Objects API Documentation

This document details the HubSpot Custom Objects API, allowing developers to create, manage, and interact with custom objects within their HubSpot accounts.

## Supported Products

This API requires one of the following HubSpot products or higher:

* Marketing Hub Enterprise
* Sales Hub Enterprise
* Content Hub Enterprise
* Service Hub Enterprise
* Operations Hub Enterprise


## Authentication

The API supports two authentication methods:

* **OAuth:**  Standard OAuth 2.0 flow for secure access.
* **Private App Access Tokens:**  Generate tokens for private apps to access the API.

**Note:** HubSpot API Keys are deprecated as of November 30, 2022.  Use OAuth or Private App Access Tokens instead.


## Custom Objects Overview

HubSpot provides standard CRM objects (Contacts, Companies, Deals, Tickets).  Custom objects extend this functionality, allowing you to model your unique business data.  You can create and manage custom objects via the HubSpot UI or the API.


## API Endpoints

All API endpoints are prefixed with `https://api.hubapi.com/crm/v3/`.

### 1. Create a Custom Object

**Endpoint:** `/schemas`

**Method:** `POST`

**Request Body:**  JSON object defining the object schema.  This includes:

* `name`:  Object name (alphanumeric, underscore allowed, must start with a letter).  Cannot be changed after creation.
* `labels`:  Singular and plural labels for the object.
* `description`:  Description of the object.
* `properties`:  Array of property definitions (see below).
* `associatedObjects`:  Array of associated object IDs (standard objects use names like "CONTACT", custom objects use `objectTypeId`).
* `primaryDisplayProperty`:  Property displayed prominently.
* `secondaryDisplayProperties`:  Additional properties displayed.  The first of these is used as a fourth filter in the object index page (if of type string, number, enumeration, boolean, or datetime).
* `requiredProperties`:  Properties required when creating new records.
* `searchableProperties`:  Properties indexed for search.


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
    {"name": "condition", "label": "Condition", "type": "enumeration", "fieldType": "select", "options": [{"label": "New", "value": "new"}, {"label": "Used", "value": "used"}]},
    {"name": "year", "label": "Year", "type": "number", "fieldType": "number"}
    // ... other properties
  ],
  "associatedObjects": ["CONTACT"]
}
```

**Response:**  JSON object including the created object's `objectTypeId` and other details.


### 2. Retrieve Custom Objects

**Endpoint:** `/schemas`

**Method:** `GET` (for all objects) or `GET` `/schemas/{objectTypeId}` or `/schemas/p_{object_name}` or `/schemas/{fullyQualifiedName}` (for a specific object)

**Response:**  JSON array of object schemas (for `GET /schemas`) or a single object schema.  `fullyQualifiedName` is derived from `p{portal_id}_{object_name}`.


### 3. Retrieve Custom Object Records

**Endpoint:** `/objects/{objectType}/{recordId}` (single record) or `/objects/{objectType}/batch/read` (multiple records)

**Method:** `GET` (single record) or `POST` (multiple records)

**Parameters (single record):**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return with history.
* `associations`: Comma-separated list of associated objects to retrieve.

**Request Body (multiple records):**

* `inputs`: Array of objects with `id` (record ID or custom unique identifier).
* `idProperty`: Name of the unique identifier property (if not using `hs_object_id`).
* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return with history.


**Response:** JSON object representing the record or an array of records.



### 4. Update Custom Objects

**Endpoint:** `/schemas/{objectTypeId}`

**Method:** `PATCH`

**Request Body:** JSON object containing the updates to the schema.


### 5. Update Associations

**Endpoint:** `/schemas/{objectTypeId}/associations`

**Method:** `POST`

**Request Body:** JSON object defining the new association.


### 6. Delete Custom Objects

**Endpoint:** `/schemas/{objectType}`

**Method:** `DELETE` (soft delete) or `/schemas/{objectType}?archived=true` (hard delete, only if all instances and associations are deleted)


### Property Types and `fieldType` Values

| `type`        | Description                                     | `fieldType` Values           |
|---------------|-------------------------------------------------|-------------------------------|
| `enumeration` | String representing a set of options (;)        | `booleancheckbox`, `checkbox`, `radio`, `select` |
| `date`        | ISO 8601 formatted date                         | `date`                         |
| `dateTime`    | ISO 8601 formatted date and time (time ignored in UI) | `date`                         |
| `string`      | Plain text string (max 65,536 chars)             | `file`, `text`, `textarea`     |
| `number`      | Number value                                     | `number`                       |


## Example Walkthrough (CarSpot)

The provided document includes a detailed walkthrough of creating a "Cars" custom object for a car dealership, including creating properties, associations, and records.  Refer to the original document for the complete example.


## Error Handling

The API returns standard HTTP status codes and JSON error responses to indicate success or failure.  Refer to the HubSpot API documentation for specific error codes and their meanings.


This markdown documentation provides a concise overview of the HubSpot Custom Objects API. For complete details, including detailed request and response structures, refer to the original HubSpot API documentation.
