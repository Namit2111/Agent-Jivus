# HubSpot Custom Objects API Documentation

This document details the HubSpot Custom Objects API, allowing you to create, manage, and interact with custom objects within your HubSpot account.

## Overview

HubSpot provides standard CRM objects (contacts, companies, deals, tickets).  Custom objects extend this functionality, enabling you to represent and organize your CRM data according to your specific business needs. You can create custom objects within the HubSpot UI or utilize the API to define objects, properties, and associations.

**Supported Products:**  Requires Marketing Hub, Sales Hub, Content Hub, Service Hub, or Operations Hub Enterprise edition.

**Account-Specific:** Custom objects are specific to each HubSpot account, with usage limits depending on your subscription. Check the HubSpot Products & Services catalog for your limits.

**Authentication:**  Use OAuth or private app access tokens for authentication. HubSpot API Keys are deprecated as of November 30, 2022.  [Learn more about migrating from API Keys](link-to-migration-guide-needed).


## Creating a Custom Object

Creating a custom object involves defining its schema: name, properties, and associations.

**1. Object Schema Definition:**

*   **Endpoint:** `POST /crm/v3/schemas`
*   **Request Body:**  Includes:
    *   `name`: (String) Object name (letters, numbers, underscores only; must start with a letter).  Cannot be changed after creation.
    *   `description`: (String) Description of the object's purpose.
    *   `labels`: (Object)  `singular` and `plural` labels for the object. Long labels may be truncated.
    *   `primaryDisplayProperty`: (String) Property used to name individual records.
    *   `secondaryDisplayProperties`: (Array of Strings) Properties displayed under the `primaryDisplayProperty` on individual records.  The first property of this type will be added as a fourth filter on the object index page if it's a `string`, `number`, `enumeration`, `boolean`, or `datetime` type.
    *   `searchableProperties`: (Array of Strings) Properties indexed for searching.
    *   `requiredProperties`: (Array of Strings) Properties required when creating new records.
    *   `properties`: (Array of Objects)  Definition of each property (see "Properties" section below).
    *   `associatedObjects`: (Array of Strings)  Objects to associate with (standard object names or custom object `objectTypeId` values).  Automatically includes emails, meetings, notes, tasks, calls, and conversations.


**2. Naming Conventions:**

*   Object names are immutable after creation.
*   Names can contain only letters, numbers, and underscores.
*   The first character must be a letter.


## Properties

Properties define the data fields within your custom object.

**Unique Value Properties Limit:** Up to 10 unique value properties are allowed per custom object.


| `type`       | Description                                                                 | Valid `fieldType` values          |
|--------------|-----------------------------------------------------------------------------|------------------------------------|
| `enumeration` | String representing a set of options (semicolon-separated).                   | `booleancheckbox`, `checkbox`, `radio`, `select` |
| `date`        | ISO 8601 formatted date (YYYY-MM-DD).                                        | `date`                             |
| `dateTime`    | ISO 8601 formatted date and time (YYYY-MM-DDTHH:mm:ssZ). Time is not displayed. | `date`                             |
| `string`      | Plain text string (up to 65,536 characters).                                | `file`, `text`, `textarea`         |
| `number`      | Numeric value.                                                              | `number`                           |


| `fieldType`      | Description                                                                                                 |
|-------------------|-------------------------------------------------------------------------------------------------------------|
| `booleancheckbox` | Single checkbox (Yes/No).                                                                                |
| `checkbox`        | Multiple checkbox selections.                                                                               |
| `date`            | Date picker.                                                                                                |
| `file`            | File upload (stored and displayed as a URL).                                                              |
| `number`          | Numeric input.                                                                                             |
| `radio`           | Radio buttons (single selection).                                                                         |
| `select`          | Dropdown selection.                                                                                         |
| `text`            | Single-line text input.                                                                                    |
| `textarea`        | Multi-line text input.                                                                                      |


## Associations

Custom objects automatically associate with emails, meetings, notes, tasks, calls, and conversations.  You can add further associations with standard or custom objects.

*   **Adding Associations:** `POST /crm/v3/schemas/{objectTypeId}/associations`
*   **Request Body:**
    *   `fromObjectTypeId`: Your custom object's `objectTypeId`.
    *   `toObjectTypeId`:  Associated object's `objectTypeId` (custom object) or name (standard object).
    *   `name`:  Name for the association.


## Retrieving Data

**1. Retrieving Custom Objects:**

*   **All Objects:** `GET /crm/v3/schemas`
*   **Specific Object:**
    *   `GET /crm/v3/schemas/{objectTypeId}`
    *   `GET /crm/v3/schemas/p_{object_name}`
    *   `GET /crm/v3/schemas/{fullyQualifiedName}` (`fullyQualifiedName` found in the object's schema)


**2. Retrieving Custom Object Records:**

*   **Single Record:** `GET /crm/v3/objects/{objectType}/{recordId}`  (Use query parameters `properties`, `propertiesWithHistory`, `associations`)
*   **Multiple Records:** `POST /crm/v3/objects/{objectType}/batch/read` (Cannot retrieve associations; use the Associations API for batch association retrieval).  Use `idProperty` to specify a custom unique identifier property; otherwise, `id` refers to the `hs_object_id`.



## Updating Data

**1. Updating Object Schema:**

*   `PATCH /crm/v3/schemas/{objectTypeId}`
*   Object name and labels cannot be changed.  `requiredProperties`, `searchableProperties`, `primaryDisplayProperty`, and `secondaryDisplayProperties` can be updated.


**2. Updating Associations:**  (Add new associations - see Associations section above).


## Deleting a Custom Object

Only delete a custom object after deleting all its instances.

*   `DELETE /crm/v3/schemas/{objectType}` (Soft delete; allows recreation with the same name)
*   `DELETE /crm/v3/schemas/{objectType}?archived=true` (Hard delete; required for recreation with the same name after soft deletion).


## Example: Creating a "Cars" Custom Object

A detailed walkthrough of creating a "Cars" custom object, including adding properties, associations, and records, is provided in the original text.  Refer to that section for a comprehensive example.


##  Feedback

[Link to feedback form]


This markdown documentation provides a structured overview of the HubSpot Custom Objects API.  Remember to consult the official HubSpot API documentation for the most up-to-date information and detailed specifications.
