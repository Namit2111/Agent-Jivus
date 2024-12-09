# HubSpot Custom Objects API Documentation

This document details the HubSpot Custom Objects API, allowing developers to create, manage, and interact with custom objects within their HubSpot account.

## Introduction

HubSpot's standard CRM includes objects like contacts, companies, deals, and tickets.  Custom objects extend this functionality, enabling users to represent and organize CRM data based on their specific business needs.  This API allows for the creation and management of custom objects, their properties, and associations with other CRM objects.


## Supported Products

Access to the Custom Objects API requires one of the following HubSpot products at the Enterprise level:

* Marketing Hub
* Sales Hub
* Content Hub
* Service Hub
* Operations Hub

## Authentication Methods

The API supports the following authentication methods:

* **OAuth:**  The recommended method for secure authentication.
* **Private app access tokens:** A suitable alternative to OAuth.

**Note:** HubSpot API Keys are deprecated as of November 30, 2022, and are no longer supported.


## Creating a Custom Object

Creating a custom object involves defining its schema, which includes:

* **Object Name:**  Must start with a letter, contain only letters, numbers, and underscores.  Once created, the name cannot be changed.  Long labels might be truncated in the UI.
* **Properties:**  Define the data fields for individual records.  Up to 10 unique value properties are allowed per custom object.  Properties include:
    * `requiredProperties`: Properties required when creating new records.
    * `searchableProperties`: Properties indexed for searching.
    * `primaryDisplayProperty`:  The property used for naming records.
    * `secondaryDisplayProperties`: Properties displayed on individual records below the `primaryDisplayProperty`.  The first property in this list will also be added as a fourth filter on the object index page if it is of type `string`, `number`, `enumeration`, `boolean`, or `datetime`.
* **Associations:** Define relationships between the custom object and other HubSpot objects (standard or custom).

To create a custom object, make a `POST` request to `/crm/v3/schemas`.  The request body should contain the complete object schema definition.  See the **Custom Object Example** section for a detailed walkthrough.


### Property Types

| `type`       | Description                                                                 | Valid `fieldType` Values          |
|--------------|-----------------------------------------------------------------------------|-----------------------------------|
| `enumeration` | A string representing a set of options, separated by semicolons.              | `booleancheckbox`, `checkbox`, `radio`, `select` |
| `date`       | An ISO 8601 formatted date (YYYY-MM-DD).                                     | `date`                            |
| `dateTime`   | An ISO 8601 formatted date and time.  The time of day is not displayed in the app. | `date`                            |
| `string`     | A plain text string (up to 65,536 characters).                             | `file`, `text`, `textarea`       |
| `number`     | A numeric value.                                                            | `number`                          |


### Field Types

| `fieldType`       | Description                                                                                             |
|--------------------|---------------------------------------------------------------------------------------------------------|
| `booleancheckbox` | A single checkbox (Yes/No).                                                                           |
| `checkbox`        | Multiple checkboxes to select multiple options from a set.                                              |
| `date`            | A date picker.                                                                                          |
| `file`            | Allows file uploads.  Stored and displayed as a URL link to the file.                                  |
| `number`          | A numeric input.                                                                                       |
| `radio`           | Radio buttons to select one option from a set.                                                         |
| `select`          | A dropdown menu to select one option from a set.                                                      |
| `text`            | A single-line text input.                                                                              |
| `textarea`        | A multi-line text input.                                                                               |


## Retrieving Custom Objects

* **All custom objects:** `GET` request to `/crm/v3/schemas`
* **Specific custom object:** `GET` request to one of the following:
    * `/crm/v3/schemas/{objectTypeId}`
    * `/crm/v3/schemas/p_{object_name}`
    * `/crm/v3/schemas/{fullyQualifiedName}`  (derived from `p{portal_id}_{object_name}`)


## Retrieving Custom Object Records

* **Single record:** `GET` request to `/crm/v3/objects/{objectType}/{recordId}`.  Query parameters: `properties`, `propertiesWithHistory`, `associations`.
* **Multiple records:** `POST` request to `/crm/v3/objects/{objectType}/batch/read`.  This endpoint does *not* support retrieving associations.  Records can be retrieved by `hs_object_id` or a custom unique identifier property (using the `idProperty` parameter).


## Updating Custom Objects

* **Update schema:** `PATCH` request to `/crm/v3/schemas/{objectTypeId}`.  The object name and labels cannot be changed.
* **Update associations:** `POST` request to `/crm/v3/schemas/{objectTypeId}/associations`.


## Deleting a Custom Object

A custom object can only be deleted after all its instances, associations, and properties are deleted.

* **Delete:** `DELETE` request to `/crm/v3/schemas/{objectType}`.
* **Hard delete (for recreating with the same name):** `DELETE` request to `/crm/v3/schemas/{objectType}?archived=true`


## Custom Object Example

This section provides a detailed walkthrough of creating a sample custom object for a car dealership.  The example covers creating the object schema, creating records, associating records with contacts and tickets, defining new associations and properties, and updating the object schema.  Refer to the original document for the code snippets illustrating the API requests and responses.


## Conclusion

This document provides a comprehensive overview of the HubSpot Custom Objects API.  By leveraging this API, developers can create powerful and customized CRM solutions tailored to their specific business needs.
