# HubSpot Custom Objects API Documentation

This document details how to interact with HubSpot's custom objects API.  It covers creating, retrieving, updating, and deleting custom objects, as well as managing their properties and associations.

## Supported Products

Requires one of the following HubSpot products or higher:

* Marketing Hub - Enterprise
* Sales Hub - Enterprise
* Content Hub - Enterprise
* Service Hub - Enterprise
* Operations Hub - Enterprise

## Introduction

In addition to standard CRM objects (contacts, companies, deals, tickets), HubSpot allows you to create custom objects to represent and organize your CRM data. This can be done through the HubSpot UI or using the custom objects API. This documentation focuses on the API approach.


## Authentication Methods

* OAuth
* Private app access tokens

**Note:** HubSpot API Keys are deprecated as of November 30, 2022.  Use private app access tokens or OAuth instead.


## Create a Custom Object

To create a custom object, you must define its schema, including:

* **Object Name:**  Must start with a letter, contain only letters, numbers, and underscores.  Once created, the name and label cannot be changed. Long labels may be truncated.
* **Properties:**  Used to store information on individual custom object records.  A maximum of 10 unique value properties are allowed per custom object.  Properties are defined with `name`, `label`, `type`, and `fieldType`.
* **Associations:**  Connect the custom object to other HubSpot objects (standard or custom).


### Object Schema Request

Use a `POST` request to `/crm/v3/schemas`:

```json
{
  "name": "object_name",
  "description": "Description of the object",
  "labels": {
    "singular": "Singular Label",
    "plural": "Plural Label"
  },
  "primaryDisplayProperty": "property_name",
  "secondaryDisplayProperties": ["property_name1", "property_name2"],
  "searchableProperties": ["property_name1", "property_name2"],
  "requiredProperties": ["property_name1", "property_name2"],
  "properties": [
    // Array of property definitions (see below)
  ],
  "associatedObjects": ["CONTACT", "COMPANY", "objectTypeId"] // Standard objects or custom objectTypeIds
}
```

### Property Definitions

| `type`       | Description                                                              | Valid `fieldType` values             |
|--------------|--------------------------------------------------------------------------|--------------------------------------|
| `enumeration` | A string representing a set of options, separated by semicolons.          | `booleancheckbox`, `checkbox`, `radio`, `select` |
| `date`        | ISO 8601 formatted date (YYYY-MM-DD).                                   | `date`                               |
| `dateTime`    | ISO 8601 formatted date and time. Time is not displayed in the HubSpot app. | `date`                               |
| `string`      | Plain text string (up to 65,536 characters).                             | `file`, `text`, `textarea`             |
| `number`      | Numeric value.                                                           | `number`                              |


### Field Type Descriptions

| `fieldType`       | Description                                                                                                 |
|--------------------|-------------------------------------------------------------------------------------------------------------|
| `booleancheckbox` | Single checkbox (Yes/No).                                                                                   |
| `checkbox`        | Multiple checkboxes.                                                                                        |
| `date`            | Date picker.                                                                                               |
| `file`            | File upload (stored as a URL).                                                                               |
| `number`          | Numeric input.                                                                                             |
| `radio`           | Set of radio buttons.                                                                                       |
| `select`          | Dropdown menu.                                                                                             |
| `text`            | Single-line text input.                                                                                      |
| `textarea`        | Multi-line text input.                                                                                       |


## Retrieve Existing Custom Objects

* **All custom objects:** `GET` request to `/crm/v3/schemas`
* **Specific custom object:** `GET` request to one of the following:
    * `/crm/v3/schemas/{objectTypeId}`
    * `/crm/v3/schemas/p_{object_name}`
    * `/crm/v3/schemas/{fullyQualifiedName}`  (found in the object's schema, derived from `p{portal_id}_{object_name}`)


## Retrieve Custom Object Records

* **Single record:** `GET` request to `/crm/v3/objects/{objectType}/{recordId}`.  Query parameters: `properties`, `propertiesWithHistory`, `associations`.
* **Multiple records:** `POST` request to `/crm/v3/objects/{objectType}/batch/read`.  This endpoint does *not* support retrieving associations.  Use the `id` (record ID) or a custom `unique identifier property` with the `idProperty` parameter.


## Update Existing Custom Objects

Use a `PATCH` request to `/crm/v3/schemas/{objectTypeId}` to update the object's schema.  Object name and labels cannot be changed.  `requiredProperties`, `searchableProperties`, `primaryDisplayProperty`, and `secondaryDisplayProperties` can be updated.


## Update Associations

Use a `POST` request to `/crm/v3/schemas/{objectTypeId}/associations` to add associations.  Specify custom objects using their `objectTypeId` and standard objects by name.


## Delete a Custom Object

* Delete all instances of the custom object before deleting the object itself.  Use a `DELETE` request to `/crm/v3/schemas/{objectType}`.
* For a "hard delete" (to recreate an object with the same name), use `/crm/v3/schemas/{objectType}?archived=true`.  This requires deleting all instances, associations, and properties.


## Custom Object Example (Car Dealership)

This section provides a detailed walkthrough of creating a "Cars" custom object, including properties, associations, and record creation.  See the original document for the complete code examples.


## Feedback

[Link to feedback form]


This markdown documentation provides a structured and searchable representation of the original text, improving readability and searchability.  Code blocks are clearly formatted, and information is organized logically for easy understanding.
