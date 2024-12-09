# HubSpot Custom Objects API Documentation

This document details the HubSpot Custom Objects API, allowing you to create, manage, and interact with custom objects within your HubSpot account.

## Overview

HubSpot's standard CRM includes contacts, companies, deals, and tickets.  Custom objects extend this functionality, enabling you to represent and organize your data to meet specific business needs. You can create custom objects through the HubSpot UI or using the API.  This documentation focuses on the API approach. Note that custom objects are account-specific, and usage limits depend on your HubSpot subscription.


## Authentication

You can authenticate using one of the following methods:

* **OAuth:**  Recommended for most integrations.
* **Private app access tokens:** Suitable for applications with restricted access.

**Important:**  HubSpot API Keys are deprecated as of November 30, 2022, and are no longer supported.  Migrate your integrations to OAuth or private app access tokens.  [Learn more about this change](link_to_migration_guide) and how to [migrate an API key integration](link_to_migration_guide).


## Creating a Custom Object

Creating a custom object involves defining its schema, which includes:

* **Name:**  Must start with a letter, contain only letters, numbers, and underscores. Once created, the name cannot be changed.  Long labels may be truncated in the UI.
* **Properties:**  Fields used to store data for each custom object record.  There is a limit of 10 unique value properties per custom object.  You define `requiredProperties`, `searchableProperties`, `primaryDisplayProperty`, and `secondaryDisplayProperties`.  The first property in `secondaryDisplayProperties` (if it's a string, number, enumeration, boolean, or datetime type) will appear as a fourth filter on the object index page.
* **Associations:**  Links between your custom object and other HubSpot objects (standard or custom). HubSpot automatically associates custom objects with emails, meetings, notes, tasks, calls, and conversations.

To create the schema, make a `POST` request to `/crm/v3/schemas`.  The request body should include the complete schema definition.  [See the example walkthrough below](#custom-object-example) for a sample request.


### Properties Details

| `type`        | Description                                                                     | Valid `fieldType` values       |
|---------------|---------------------------------------------------------------------------------|-------------------------------|
| `enumeration` | A string representing a set of options, separated by semicolons.                 | `booleancheckbox`, `checkbox`, `radio`, `select` |
| `date`        | An ISO 8601 formatted date (YYYY-MM-DD).                                         | `date`                         |
| `dateTime`    | An ISO 8601 formatted date and time. The HubSpot app will not display the time. | `date`                         |
| `string`      | A plain text string (up to 65,536 characters).                                  | `file`, `text`, `textarea`     |
| `number`      | A numeric value.                                                                | `number`                       |

### `fieldType` Details

| `fieldType`      | Description                                                                                                    |
|-------------------|----------------------------------------------------------------------------------------------------------------|
| `booleancheckbox` | A single checkbox (Yes/No).                                                                                     |
| `checkbox`        | Multiple checkboxes to select from a set of options.                                                              |
| `date`            | Date picker.                                                                                                   |
| `file`            | Allows file upload; stored and displayed as a URL.                                                            |
| `number`          | Numeric input.                                                                                                 |
| `radio`           | Radio buttons to select a single option from a set.                                                              |
| `select`          | Dropdown input.                                                                                                 |
| `text`            | Single-line text input.                                                                                         |
| `textarea`        | Multi-line text input.                                                                                           |


### Associations Details

To associate with standard objects, use their names (e.g., "CONTACT", "COMPANY"). For custom objects, use their `objectTypeId`.


## Retrieving Custom Objects

* **All custom objects:** `GET` request to `/crm/v3/schemas`
* **Specific custom object:** `GET` request to one of the following:
    * `/crm/v3/schemas/{objectTypeId}`
    * `/crm/v3/schemas/p_{object_name}`
    * `/crm/v3/schemas/{fullyQualifiedName}` (derived from `p{portal_id}_{object_name}`)


## Retrieving Custom Object Records

* **Single record:** `GET` request to `/crm/v3/objects/{objectType}/{recordId}`.  Use query parameters `properties`, `propertiesWithHistory`, and `associations` to control the returned data.
* **Multiple records:** `POST` request to `/crm/v3/objects/{objectType}/batch/read`. This endpoint does *not* support retrieving associations.  You can retrieve by `hs_object_id` or a custom unique identifier property using the `idProperty` parameter.


## Updating Custom Objects

* **Update schema:** `PATCH` request to `/crm/v3/schemas/{objectTypeId}`.  The object's name and labels cannot be changed.
* **Update associations:** `POST` request to `/crm/v3/schemas/{objectTypeId}/associations`.


## Deleting Custom Objects

To delete a custom object, all its instances, associations, and properties must first be deleted.  Make a `DELETE` request to `/crm/v3/schemas/{objectType}`. To create a new object with the same name, use a hard delete:  `DELETE` request to `/crm/v3/schemas/{objectType}?archived=true`.


## Custom Object Example

This walkthrough demonstrates creating a "Cars" custom object for a car dealership.

### Creating the Object Schema

A `POST` request to `/crm/v3/schemas` with a JSON body defining the properties (condition, date received, year, make, model, VIN, color, mileage, price, notes), labels, primary and secondary display properties, searchable properties, required properties and associations with contacts is made.

### Creating a Custom Object Record

A `POST` request to `/crm/v3/objects/{objectTypeId}` with the properties for a specific car is made.

### Associating the Custom Object Record

A `PUT` request to the associations endpoint associates the car record with a contact record.

### Defining a New Association

A `POST` request to `/crm/v3/schemas/{objectTypeId}/associations` creates an association between the "Cars" object and HubSpot tickets for maintenance tracking.

### Defining a New Property

A `POST` request to `/crm/v3/properties/{objectTypeId}` adds a new "maintenance_package" property.

### Updating the Object Schema

A `PATCH` request to `/crm/v3/schemas/{objectTypeId}` updates the `secondaryDisplayProperties` to include the new "maintenance_package" property.


**(Note:  All code snippets from the original text are omitted here for brevity. Refer to the original text for the code examples.)**
