# HubSpot Custom Objects API Documentation

This document details the HubSpot Custom Objects API, allowing developers to create, manage, and interact with custom objects within their HubSpot accounts.

## Overview

HubSpot's standard CRM includes objects like contacts, companies, deals, and tickets.  Custom objects extend this functionality, enabling users to represent and organize CRM data according to their specific business needs.  This API allows for the definition of custom objects, their properties, and associations with other CRM objects.

**Supported Products:**  Requires Marketing Hub, Sales Hub, Content Hub, Service Hub, or Operations Hub - Enterprise edition.

**Account-Specific:** Custom objects are unique to each HubSpot account and subject to creation limits based on your subscription. Check the HubSpot Products & Services catalog for details on your limits.


## Authentication Methods

* **OAuth:**  Recommended authentication method.
* **Private App Access Tokens:**  Alternative authentication method.

**Deprecated:** HubSpot API Keys are deprecated as of November 30, 2022, and are no longer supported.  Migrate existing integrations to use private app access tokens or OAuth.  [Learn more about this change](link_to_migration_guide_here) and how to [migrate an API key integration](link_to_migration_guide_here).


## Creating a Custom Object

Creating a custom object involves defining its schema, which includes the object's name, properties, and associations.

**Schema Request:**  A `POST` request to `/crm/v3/schemas` is used to create the custom object schema.  The request body includes the schema definition:

* **`name`:**  Object name (letters, numbers, underscores only; must start with a letter).  **Cannot be changed after creation.**
* **`labels`:**  Singular and plural labels for the object.  **Cannot be changed after creation.**
* **`description`:** (Optional) Description of the object's purpose.
* **`properties`:**  An array defining the object's properties (detailed below).
* **`associatedObjects`:** An array specifying associations with other CRM objects (detailed below).  Includes automatic associations with emails, meetings, notes, tasks, calls, and conversations.
* **`requiredProperties`:** An array of property names that are required when creating new records.
* **`searchableProperties`:** An array of property names indexed for searching.
* **`primaryDisplayProperty`:** The property used to name individual records.
* **`secondaryDisplayProperties`:** Properties displayed on individual records below the `primaryDisplayProperty`. The first property listed will also be added as a fourth filter on the object index page if it's a string, number, enumeration, boolean, or datetime type.


### Properties

Each property definition includes:

* **`name`:** Property name.
* **`label`:**  Display label for the property.
* **`type`:** Property data type (`enumeration`, `date`, `dateTime`, `string`, `number`).
* **`fieldType`:** UI field type (`booleancheckbox`, `checkbox`, `date`, `file`, `number`, `radio`, `select`, `text`, `textarea`).
* **`options` (for `enumeration` type):** An array of option objects, each with `label` and `value`.
* **`hasUniqueValue` (for `string` type):**  Indicates if the property should have unique values.

**Unique Value Properties Limit:** Up to 10 unique value properties per custom object.


### Associations

Associations link custom objects to other CRM objects (standard or custom).  Specify standard objects by name (e.g., "CONTACT", "COMPANY") and custom objects by their `objectTypeId`.


## Retrieving Custom Objects

* **All Custom Objects:** `GET` request to `/crm/v3/schemas`.
* **Specific Custom Object:** `GET` request to one of these endpoints:
    * `/crm/v3/schemas/{objectTypeId}`
    * `/crm/v3/schemas/p_{object_name}`
    * `/crm/v3/schemas/{fullyQualifiedName}`  (derived from `p{portal_id}_{object_name}`)


## Retrieving Custom Object Records

* **Specific Record:** `GET` request to `/crm/v3/objects/{objectType}/{recordId}`.  Supports query parameters: `properties`, `propertiesWithHistory`, `associations`.
* **Multiple Records:** `POST` request to `/crm/v3/objects/{objectType}/batch/read`.  Does *not* support retrieving associations.  Use the associations API for batch association retrieval.  Retrieve records by `hs_object_id` or a custom unique identifier property (using the `idProperty` parameter).


## Updating Custom Objects

* **Update Schema:** `PATCH` request to `/crm/v3/schemas/{objectTypeId}`.  Object name and labels cannot be changed.  `requiredProperties`, `searchableProperties`, `primaryDisplayProperty`, and `secondaryDisplayProperties` can be updated.
* **Update Associations:** `POST` request to `/crm/v3/schemas/{objectTypeId}/associations`.


## Deleting a Custom Object

A custom object can only be deleted after all its instances, associations, and properties are deleted.

* **Soft Delete:** `DELETE` request to `/crm/v3/schemas/{objectType}`.
* **Hard Delete:** `DELETE` request to `/crm/v3/schemas/{objectType}?archived=true` (required to create a new object with the same name).


## Custom Object Example: Car Inventory

A detailed walkthrough of creating a "Cars" custom object, including creating properties, associations, and records, is provided in the original document.  This example demonstrates the practical application of the API endpoints and request structures.


## Appendix:  API Endpoints Summary

| Method | Endpoint                     | Description                                      |
|--------|------------------------------|--------------------------------------------------|
| POST   | `/crm/v3/schemas`            | Create custom object schema                       |
| GET    | `/crm/v3/schemas`            | Retrieve all custom objects                       |
| GET    | `/crm/v3/schemas/{objectTypeId}` | Retrieve a specific custom object                 |
| GET    | `/crm/v3/schemas/p_{object_name}` | Retrieve a specific custom object                 |
| GET    | `/crm/v3/schemas/{fullyQualifiedName}` | Retrieve a specific custom object                 |
| PATCH  | `/crm/v3/schemas/{objectTypeId}` | Update custom object schema                       |
| POST   | `/crm/v3/objects/{objectType}` | Create a custom object record                    |
| GET    | `/crm/v3/objects/{objectType}/{recordId}` | Retrieve a specific custom object record          |
| POST   | `/crm/v3/objects/{objectType}/batch/read` | Retrieve multiple custom object records           |
| PUT    | `/crm/v3/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}/{associationType}` | Associate custom object record with another record |
| POST   | `/crm/v3/schemas/{objectTypeId}/associations` | Create a new association between objects       |
| DELETE | `/crm/v3/schemas/{objectType}` | Delete a custom object (soft delete)             |
| DELETE | `/crm/v3/schemas/{objectType}?archived=true` | Delete a custom object (hard delete)             |
| POST   | `/crm/v3/properties/{objectTypeId}` | Create a new custom object property              |


This markdown documentation provides a structured overview of the HubSpot Custom Objects API,  making it easier for developers to understand and use the API effectively. Remember to replace placeholders like `{objectTypeId}`, `{objectType}`, `{recordId}`, etc., with the appropriate values.
