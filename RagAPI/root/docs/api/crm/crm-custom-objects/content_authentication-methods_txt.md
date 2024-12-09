# HubSpot Custom Objects API Documentation

This document details the HubSpot Custom Objects API, allowing developers to create, manage, and interact with custom objects within their HubSpot accounts.

## Overview

HubSpot provides standard CRM objects (Contacts, Companies, Deals, Tickets).  Custom objects extend this functionality, enabling users to represent and organize data specific to their business needs.  This API allows for defining custom objects, their properties, and associations with other HubSpot objects.  Access requires a Marketing Hub, Sales Hub, Content Hub, Service Hub, or Operations Hub Enterprise subscription.  Usage is subject to account-specific limits.

## Authentication

The API supports two authentication methods:

* **OAuth:**  Recommended for most integrations.
* **Private App Access Tokens:**  Suitable for internal applications.

**Note:** HubSpot API Keys are deprecated as of November 30, 2022, and should not be used.  See the provided links for migration instructions.

## Creating a Custom Object

Creating a custom object involves defining its schema, which includes:

* **Object Name:**  Must start with a letter and contain only letters, numbers, and underscores.  Once created, the name cannot be changed.
* **Properties:**  Used to store information in individual records.  A maximum of 10 unique value properties are allowed per custom object.
    * `requiredProperties`: Properties required when creating new records.
    * `searchableProperties`: Properties indexed for searching.
    * `primaryDisplayProperty`: Property used for naming records.
    * `secondaryDisplayProperties`: Properties displayed on individual records (below `primaryDisplayProperty`).  The first property of this type will be added as a fourth filter on the object index page if it's a `string`, `number`, `enumeration`, `boolean`, or `datetime` type.  Removing a display property requires deleting and recreating it.
* **Associations:**  Links to other standard or custom HubSpot objects.  HubSpot automatically associates custom objects with emails, meetings, notes, tasks, calls, and conversations.

**Schema Request:**

A `POST` request to `/crm/v3/schemas` is used to create the schema. The request body should include the object's name, description, labels (singular and plural), properties, and associated objects.

**Property Types:**

| `type`       | Description                                                                    | Valid `fieldType` values     |
|--------------|--------------------------------------------------------------------------------|-----------------------------|
| `enumeration` | A string representing a set of options, separated by semicolons.                 | `booleancheckbox`, `checkbox`, `radio`, `select` |
| `date`       | An ISO 8601 formatted value representing a specific day, month, and year.         | `date`                      |
| `dateTime`   | An ISO 8601 formatted value representing a date and time. Time is not displayed. | `date`                      |
| `string`     | A plain text string (up to 65,536 characters).                                | `file`, `text`, `textarea`   |
| `number`     | A numeric value.                                                              | `number`                    |

**Field Type Descriptions:**

* `booleancheckbox`: A single checkbox (Yes/No).
* `checkbox`: Multiple checkboxes.
* `date`: A date picker.
* `file`: File upload (stored as a URL).
* `number`: Numeric input.
* `radio`: Radio buttons.
* `select`: Dropdown.
* `text`: Single-line text input.
* `textarea`: Multi-line text input.


## Retrieving Custom Objects

* **All Custom Objects:** `GET` request to `/crm/v3/schemas`.
* **Specific Custom Object:** `GET` request to one of:
    * `/crm/v3/schemas/{objectTypeId}`
    * `/crm/v3/schemas/p_{object_name}`
    * `/crm/v3/schemas/{fullyQualifiedName}`  (derived from `p{portal_id}_{object_name}`)


## Retrieving Custom Object Records

* **Specific Record:** `GET` request to `/crm/v3/objects/{objectType}/{recordId}`.  Query parameters: `properties`, `propertiesWithHistory`, `associations`.
* **Multiple Records:** `POST` request to `/crm/v3/objects/{objectType}/batch/read`.  This endpoint does *not* retrieve associations.  Retrieve records by `hs_object_id` or a custom unique identifier property (`idProperty` parameter).


## Updating Custom Objects

* **Update Schema:** `PATCH` request to `/crm/v3/schemas/{objectTypeId}`.  Object name and labels cannot be changed.
* **Update Associations:** `POST` request to `/crm/v3/schemas/{objectTypeId}/associations`.


## Deleting Custom Objects

To delete, all object instances, associations, and properties must be deleted first.

* **Delete Custom Object:** `DELETE` request to `/crm/v3/schemas/{objectType}`.
* **Hard Delete (for object name reuse):** `DELETE` request to `/crm/v3/schemas/{objectType}?archived=true`.


## Example: Creating a "Cars" Custom Object

This section provides a detailed walkthrough of creating a "Cars" custom object, including creating records, associations, and properties.  The complete request bodies for each step are shown in the original text.


## Conclusion

This documentation provides a comprehensive overview of the HubSpot Custom Objects API.  Refer to the original text for detailed code examples and further specifics.
