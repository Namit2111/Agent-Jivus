# HubSpot Custom Objects API Documentation

This document details the HubSpot Custom Objects API, allowing developers to create, manage, and interact with custom objects within their HubSpot accounts.

## Introduction

HubSpot's standard CRM includes objects like contacts, companies, deals, and tickets.  Custom objects extend this functionality, enabling you to represent and organize data specific to your business needs.  This API provides programmatic access to create, manage, and query these custom objects.

**Supported Products:**  Marketing Hub Enterprise, Sales Hub Enterprise, Content Hub Enterprise, Service Hub Enterprise, Operations Hub Enterprise.

**Account-Specific:** Custom objects are specific to each HubSpot account, and usage is subject to account limits.  Refer to the [HubSpot Products & Services catalog](link-to-catalog) for details.

**Authentication:**  Use OAuth or private app access tokens for authentication.  HubSpot API keys are deprecated as of November 30, 2022.  [Learn more about the deprecation and migration](link-to-deprecation-info).


## Creating a Custom Object

Creating a custom object involves defining its schema, which includes:

* **Name:**  Must start with a letter, contain only letters, numbers, and underscores.  Cannot be changed after creation.  Long labels may be truncated.
* **Properties:**  Fields for storing information about individual records.  Up to 10 unique value properties are allowed per custom object.
*   * **`requiredProperties`**: Properties required when creating new records.
*   * **`searchableProperties`**: Properties indexed for searching.
*   * **`primaryDisplayProperty`**: Property used for naming records.
*   * **`secondaryDisplayProperties`**: Properties displayed on individual records under the `primaryDisplayProperty`. The first property listed here will also be a fourth filter on the object index page if it's one of the following types: `string`, `number`, `enumeration`, `boolean`, `datetime`. To remove a display property from the UI, delete and recreate it.
* **Associations:**  Links to other HubSpot objects (standard or custom).

**Request:**  A `POST` request to `/crm/v3/schemas` with the object schema in the request body.  See the [Object schema](link-to-object-schema-details) for full request details and an example.

### Properties

| `type`       | Description                                                                     | Valid `fieldType` values |
|--------------|---------------------------------------------------------------------------------|--------------------------|
| `enumeration` | A string representing a set of options (semicolon-separated).                   | `booleancheckbox`, `checkbox`, `radio`, `select` |
| `date`       | ISO 8601 formatted date (YYYY-MM-DD).                                          | `date`                   |
| `dateTime`   | ISO 8601 formatted date and time.  Time is not displayed in the HubSpot app. | `date`                   |
| `string`     | Plain text string (up to 65,536 characters).                                  | `file`, `text`, `textarea` |
| `number`     | Numeric value.                                                                  | `number`                 |


### Field Types

| `fieldType`      | Description                                                                                                        |
|-------------------|--------------------------------------------------------------------------------------------------------------------|
| `booleancheckbox` | Single checkbox (Yes/No).                                                                                           |
| `checkbox`       | Multiple checkboxes (allows multiple selections from a set of options).                                              |
| `date`           | Date picker.                                                                                                      |
| `file`           | File upload (stored as a URL).                                                                                       |
| `number`         | Numeric input.                                                                                                     |
| `radio`          | Radio buttons (single selection from a set of options).                                                              |
| `select`         | Dropdown menu (single selection from a set of options).                                                             |
| `text`           | Single-line text input.                                                                                            |
| `textarea`       | Multi-line text input.                                                                                             |


### Associations

HubSpot automatically associates custom objects with emails, meetings, notes, tasks, calls, and conversations.  You can add further associations using the `associatedObjects` array in the schema request.  Use object names for standard objects and `objectTypeId` values for custom objects.


## Retrieving Custom Objects

* **All custom objects:** `GET` request to `/crm/v3/schemas`.
* **Specific custom object:** `GET` request to one of the following:
    * `/crm/v3/schemas/{objectTypeId}`
    * `/crm/v3/schemas/p_{object_name}`
    * `/crm/v3/schemas/{fullyQualifiedName}`  (derived from `p{portal_id}_{object_name}`)


## Retrieving Custom Object Records

* **Single record:** `GET` request to `/crm/v3/objects/{objectType}/{recordId}`.  Use query parameters `properties`, `propertiesWithHistory`, and `associations` to specify the data to retrieve.
* **Multiple records:** `POST` request to `/crm/v3/objects/{objectType}/batch/read`.  This endpoint does *not* support retrieving associations. Use `hs_object_id` or a custom unique identifier property (`idProperty` parameter).


## Updating Custom Objects

* **Schema update:** `PATCH` request to `/crm/v3/schemas/{objectTypeId}`.  Object name and labels cannot be changed.  `requiredProperties`, `searchableProperties`, `primaryDisplayProperty`, and `secondaryDisplayProperties` can be updated.  You must create properties via the properties API before adding them to these fields.
* **Associations:** To add object associations, send a `POST` request to `/crm/v3/schemas/{objectTypeId}/associations`.


## Deleting Custom Objects

A custom object can only be deleted after all its instances, associations, and properties have been deleted.

* **Soft delete:** `DELETE` request to `/crm/v3/schemas/{objectType}`.
* **Hard delete (for recreating with the same name):** `DELETE` request to `/crm/v3/schemas/{objectType}?archived=true`.


## Custom Object Example (Car Dealership)

This section provides a detailed walkthrough of creating a custom object for a car dealership, including creating the schema, records, associations, and properties.  The full requests are shown in the original text.  Refer to the original document for the detailed code examples.


## Conclusion

This API offers comprehensive control over custom objects in HubSpot.  Remember to consult the HubSpot documentation for the most up-to-date information and best practices.
