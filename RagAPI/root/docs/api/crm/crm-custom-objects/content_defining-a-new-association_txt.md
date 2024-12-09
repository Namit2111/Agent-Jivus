# HubSpot Custom Objects API Documentation

This document details the HubSpot Custom Objects API, allowing developers to create, manage, and interact with custom objects within their HubSpot accounts.

## Overview

HubSpot provides standard CRM objects (contacts, companies, deals, tickets).  Custom objects extend this functionality, enabling representation of business-specific data.  This API allows defining custom objects, their properties, and associations with other HubSpot objects.  Access requires a Marketing Hub, Sales Hub, Content Hub, Service Hub, or Operations Hub Enterprise subscription.  Limits on the number of custom objects per account apply.

## Authentication

The API supports two authentication methods:

* **OAuth:**  Recommended for most integrations.
* **Private app access tokens:**  Suitable for applications with limited scope.

**Note:** HubSpot API Keys are deprecated as of November 30, 2022.  Migrating to OAuth or private app access tokens is mandatory.


## Creating a Custom Object

Creating a custom object involves defining its schema: name, properties, and associations.

### Object Schema

The schema is defined using a `POST` request to `/crm/v3/schemas`.  The request body includes:

* **`name`:** Object name (alphanumeric and underscores only; must start with a letter; cannot be changed after creation).
* **`description`:**  A description of the object.
* **`labels`:** Singular and plural labels for the object.
* **`primaryDisplayProperty`:**  Property used to name individual records.
* **`secondaryDisplayProperties`:** Properties displayed on individual records below the primary display property.  The first property of this type (string, number, enumeration, boolean, datetime) will also be added as a fourth filter on the object index page.
* **`searchableProperties`:** Properties indexed for searching.
* **`requiredProperties`:** Properties required when creating new records.
* **`properties`:** An array defining individual properties (see below).
* **`associatedObjects`:** An array of associated object IDs (objectTypeId for custom objects, names for standard objects).  Automatically includes emails, meetings, notes, tasks, calls, and conversations.

### Properties

Properties define the data fields within a custom object.  Each property is defined with:

* **`name`:** Property name (alphanumeric and underscores only).
* **`label`:**  User-friendly label for the property.
* **`type`:** Property data type (`enumeration`, `date`, `dateTime`, `string`, `number`).
* **`fieldType`:** UI field type (`booleancheckbox`, `checkbox`, `date`, `file`, `number`, `radio`, `select`, `text`, `textarea`).
* **`options` (for `enumeration` type):** Array of label-value pairs for select options.
* **`hasUniqueValue` (optional):** Set to `true` if the property must have unique values.

Maximum 10 unique value properties are allowed per custom object.


| `type`       | Description                                       | Valid `fieldType` values      |
|--------------|---------------------------------------------------|-----------------------------|
| `enumeration` | A string representing a set of options (semicolon-separated). | `booleancheckbox`, `checkbox`, `radio`, `select` |
| `date`       | ISO 8601 formatted date (YYYY-MM-DD).             | `date`                       |
| `dateTime`   | ISO 8601 formatted date and time.                | `date`                       |
| `string`     | Plain text string (up to 65,536 characters).      | `file`, `text`, `textarea`  |
| `number`     | Numeric value.                                     | `number`                     |


### Associations

Define associations with other HubSpot objects using the `associatedObjects` array in the schema.  Custom objects are identified by their `objectTypeId`.


## Retrieving Custom Objects

* Retrieve all custom objects: `GET /crm/v3/schemas`
* Retrieve a specific custom object:
    * `GET /crm/v3/schemas/{objectTypeId}`
    * `GET /crm/v3/schemas/p_{object_name}`
    * `GET /crm/v3/schemas/{fullyQualifiedName}` (`fullyQualifiedName` is derived from `p{portal_id}_{object_name}`)


## Retrieving Custom Object Records

* Retrieve a single record by ID: `GET /crm/v3/objects/{objectType}/{recordId}` (parameters: `properties`, `propertiesWithHistory`, `associations`)
* Retrieve multiple records: `POST /crm/v3/objects/{objectType}/batch/read` (parameters: `properties`, `idProperty` for custom ID retrieval).  This endpoint does *not* retrieve associations.


## Updating Custom Objects

* Update object schema: `PATCH /crm/v3/schemas/{objectTypeId}` (e.g., to change `requiredProperties`, `searchableProperties`, `primaryDisplayProperty`, `secondaryDisplayProperties`).
* Update associations: `POST /crm/v3/schemas/{objectTypeId}/associations`.


## Deleting Custom Objects

Deleting a custom object requires all its instances to be deleted first.

* Delete a custom object: `DELETE /crm/v3/schemas/{objectType}`
* Hard delete a custom object schema (to allow recreation with the same name): `DELETE /crm/v3/schemas/{objectType}?archived=true`


## Example: Creating a "Cars" Custom Object

This section walks through creating a "Cars" custom object with properties like condition, year, make, model, VIN, etc., and associating it with contacts and tickets.  It demonstrates creating properties and associations.


## Conclusion

This API empowers developers to tailor HubSpot to their specific data needs by creating and managing custom objects seamlessly.  Refer to the detailed examples and request bodies provided throughout this document for implementing these API calls effectively.
