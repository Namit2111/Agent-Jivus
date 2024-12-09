# HubSpot Custom Objects API Documentation

This document details the HubSpot Custom Objects API, allowing developers to create, manage, and interact with custom objects within their HubSpot accounts.  This API extends the standard CRM objects (contacts, companies, deals, tickets) to accommodate specific business needs.

## Supported Products

Requires one of the following HubSpot products or higher:

* Marketing Hub - Enterprise
* Sales Hub - Enterprise
* Content Hub - Enterprise
* Service Hub - Enterprise
* Operations Hub - Enterprise

## Authentication Methods

* OAuth
* Private app access tokens

**Note:** HubSpot API Keys are deprecated as of November 30, 2022.  Use private app access tokens or OAuth for authentication.  [Learn more about this change](link_to_change_documentation) and how to [migrate an API key integration](link_to_migration_documentation).

## Creating a Custom Object

1. **Define the Object Schema:** The schema defines the object's name, properties, and associations with other CRM objects.  See the "Object Schema" section for details.

2. **`POST` Request to `/crm/v3/schemas`:** Send a `POST` request to this endpoint with the schema definition in the request body.

   * **Object Name:**  Must start with a letter, contain only letters, numbers, and underscores.  Once created, the name and label cannot be changed.  Long labels may be truncated in the UI.

### Object Schema

**Required Fields:**

* `name` (string): The internal name of the custom object.
* `description` (string): A description of the custom object.
* `labels`: (object)  `singular` (string) and `plural` (string) labels for the object.
* `primaryDisplayProperty` (string): The property used to name individual records.
* `properties`: (array) An array of property definitions (see "Properties" section below).
* `associatedObjects`: (array) An array of object type IDs or names to associate with (see "Associations" section below).

**Optional Fields:**

* `secondaryDisplayProperties`: (array) Additional properties displayed on individual records.  The first property in this array, if it's a string, number, enumeration, boolean, or datetime type, will also be added as a fourth filter on the object index page.
* `searchableProperties`: (array) Properties indexed for searching.
* `requiredProperties`: (array) Properties required when creating new records.


### Properties

Properties define the data fields within your custom object.  Each property has the following attributes:

* `name` (string): Internal property name.
* `label` (string): Display name of the property.
* `type` (string): Property data type.
* `fieldType` (string): UI field type.


| `type`       | Description                                              | Valid `fieldType` values     |
|--------------|----------------------------------------------------------|-----------------------------|
| `enumeration` | A string representing a set of options (semicolon-separated). | `booleancheckbox`, `checkbox`, `radio`, `select` |
| `date`       | ISO 8601 formatted date (YYYY-MM-DD).                     | `date`                       |
| `dateTime`   | ISO 8601 formatted date and time.  Time is not displayed in the UI. | `date`                       |
| `string`     | Plain text string (up to 65,536 characters).             | `file`, `text`, `textarea`  |
| `number`     | Numeric value.                                           | `number`                     |


| `fieldType`       | Description                                                                  |
|--------------------|------------------------------------------------------------------------------|
| `booleancheckbox` | Single checkbox (Yes/No).                                                    |
| `checkbox`         | Multiple checkboxes.                                                         |
| `date`             | Date picker.                                                                 |
| `file`             | File upload (stored and displayed as a URL).                               |
| `number`           | Numeric input.                                                              |
| `radio`            | Radio buttons (single selection).                                             |
| `select`           | Dropdown.                                                                    |
| `text`             | Single-line text input.                                                      |
| `textarea`         | Multi-line text input.                                                       |


**Unique Value Properties:**  You can have up to 10 unique value properties per custom object.  Set `hasUniqueValue: true` in the property definition.

### Associations

You can associate your custom object with other standard HubSpot objects (contacts, companies, deals, tickets) or other custom objects.  Use the `associatedObjects` array in your schema definition.  Identify standard objects by their name and custom objects by their `objectTypeId`.

## Retrieving Custom Objects

* **All Custom Objects:** `GET` request to `/crm/v3/schemas`
* **Specific Custom Object:** `GET` request to one of the following:
    * `/crm/v3/schemas/{objectTypeId}`
    * `/crm/v3/schemas/p_{object_name}`
    * `/crm/v3/schemas/{fullyQualifiedName}`  (derived from `p{portal_id}_{object_name}`)

## Retrieving Custom Object Records

* **Single Record:** `GET` request to `/crm/v3/objects/{objectType}/{recordId}`.  Use query parameters `properties`, `propertiesWithHistory`, and `associations` to control the returned data.
* **Multiple Records:** `POST` request to `/crm/v3/objects/{objectType}/batch/read`.  This endpoint does not support retrieving associations.  Use `idProperty` to specify a custom unique identifier property; otherwise, it defaults to `hs_object_id`.

## Updating Custom Objects

* **Update Schema:** `PATCH` request to `/crm/v3/schemas/{objectTypeId}`.  You cannot change the object name or labels.
* **Update Associations:** `POST` request to `/crm/v3/schemas/{objectTypeId}/associations`.

## Deleting a Custom Object

* **Soft Delete:** `DELETE` request to `/crm/v3/schemas/{objectType}` (requires all object instances and associations to be deleted first).
* **Hard Delete:** `DELETE` request to `/crm/v3/schemas/{objectType}?archived=true` (allows recreating an object with the same name).


## Custom Object Example (Car Dealership Inventory)

This section provides a detailed walkthrough of creating a custom object to manage car inventory, including creating properties, associations, and records.  The example code snippets are included in the original text.


##  Feedback

[Link to Feedback Form]


This Markdown documentation provides a more structured and readable representation of the provided text. Remember to replace placeholder links like `link_to_change_documentation` with actual links to relevant HubSpot documentation.
