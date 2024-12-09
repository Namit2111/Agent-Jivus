# HubSpot Custom Objects API Documentation

This document details the HubSpot Custom Objects API, allowing you to create, manage, and interact with custom objects within your HubSpot account.

## Introduction

HubSpot's standard CRM objects (contacts, companies, deals, tickets) may not suffice for all business needs. Custom objects provide a flexible way to extend your CRM data model to represent and organize information specific to your organization. This API allows programmatic creation and manipulation of custom objects, their properties, and associations with other HubSpot objects.

**Supported Products:** Marketing Hub Enterprise, Sales Hub Enterprise, Content Hub Enterprise, Service Hub Enterprise, Operations Hub Enterprise.

**Account-Specific:** Custom objects are specific to each HubSpot account, with usage limits dependent on your subscription.  Refer to the HubSpot Products & Services catalog for details on your limits.

**Authentication:**  Use OAuth or private app access tokens.  HubSpot API keys are deprecated as of November 30, 2022, and should no longer be used.  [Learn more about migrating from API keys](<link_to_migration_guide>)

## Creating a Custom Object

Creating a custom object involves defining its schema: name, properties, and associations.

**1. Define the Object Schema:**

The schema is defined using a `POST` request to `/crm/v3/schemas`.  The request body includes:

*   `name`: (string) The object's name (alphanumeric and underscores only; must start with a letter).  This cannot be changed after creation.
*   `description`: (string) A description of the object.
*   `labels`: (object)  `singular` and `plural` labels for the object.  Long labels may be truncated in the UI.
*   `primaryDisplayProperty`: (string) The property used to name individual records.
*   `secondaryDisplayProperties`: (array of strings) Properties displayed below the `primaryDisplayProperty` on individual records. The first property listed will also be added as a fourth filter on the object index page if it's a `string`, `number`, `enumeration`, `boolean`, or `datetime` type.
*   `searchableProperties`: (array of strings) Properties indexed for search.
*   `requiredProperties`: (array of strings) Properties required when creating new records.
*   `properties`: (array of objects)  Defines the object's properties (detailed below).
*   `associatedObjects`: (array of strings)  Objects to associate with (standard objects by name, custom objects by `objectTypeId`).

**2. Property Definitions:**

Each property within the `properties` array requires:

*   `name`: (string) The property's name.
*   `label`: (string) The property's label.
*   `type`: (string) The property's data type.
*   `fieldType`: (string)  The UI field type.


| `type`       | Description                                         | Valid `fieldType` values |
|---------------|-----------------------------------------------------|--------------------------|
| `enumeration` | A string representing a set of options (semicolon-separated). | `booleancheckbox`, `checkbox`, `radio`, `select` |
| `date`        | ISO 8601 formatted date (YYYY-MM-DD).              | `date`                    |
| `dateTime`    | ISO 8601 formatted date and time. Time is not displayed in the UI. | `date`                    |
| `string`      | Plain text string (up to 65,536 characters).       | `file`, `text`, `textarea` |
| `number`      | Numeric value.                                      | `number`                  |

| `fieldType`       | Description                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| `booleancheckbox` | Single checkbox (Yes/No).                                                   |
| `checkbox`         | Multiple checkboxes.                                                        |
| `date`             | Date picker.                                                                |
| `file`             | File upload (stored as a URL).                                             |
| `number`           | Numeric input.                                                              |
| `radio`            | Radio buttons.                                                              |
| `select`           | Dropdown.                                                                  |
| `text`             | Single-line text input.                                                     |
| `textarea`         | Multi-line text input.                                                      |


**3. Unique Value Properties:**  You can have up to 10 unique value properties per custom object.  Specify `hasUniqueValue: true` in the property definition.

**4.  Associations:**  HubSpot automatically associates custom objects with emails, meetings, notes, tasks, calls, and conversations.  You can add additional associations using the `associatedObjects` array in the schema definition.


## Retrieving Custom Objects

*   **All Custom Objects:** `GET /crm/v3/schemas`
*   **Specific Custom Object:**
    *   `GET /crm/v3/schemas/{objectTypeId}`
    *   `GET /crm/v3/schemas/p_{object_name}`
    *   `GET /crm/v3/schemas/{fullyQualifiedName}` (derived from `p{portal_id}_{object_name}`)


## Retrieving Custom Object Records

*   **Single Record:** `GET /crm/v3/objects/{objectType}/{recordId}` (Use query parameters `properties`, `propertiesWithHistory`, `associations`).
*   **Multiple Records:** `POST /crm/v3/objects/{objectType}/batch/read` (Cannot retrieve associations; use the Associations API for batch association reads).  Retrieve by `hs_object_id` or a custom unique identifier property (using `idProperty` parameter).


## Updating Custom Objects

*   **Update Schema:** `PATCH /crm/v3/schemas/{objectTypeId}` (Name and labels cannot be changed).
*   **Update Associations:** `POST /crm/v3/schemas/{objectTypeId}/associations`


## Deleting Custom Objects

*   **Soft Delete:** `DELETE /crm/v3/schemas/{objectType}` (Requires all object instances, associations, and properties to be deleted first).
*   **Hard Delete:** `DELETE /crm/v3/schemas/{objectType}?archived=true` (Allows recreating an object with the same name).


## Example Walkthrough: Creating a "Cars" Custom Object

This section provides a step-by-step example of creating a custom object to track car inventory, associating it with contacts and tickets, and adding a new property.  The complete request bodies for each step are provided in the original text.

## API Reference

The complete API reference including request/response details, error handling, and rate limits should be available in the official HubSpot API documentation.  This markdown file provides a high-level overview.
