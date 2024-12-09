# HubSpot Custom Objects API Documentation

This document details the HubSpot Custom Objects API, allowing developers to create, manage, and interact with custom objects within their HubSpot accounts.

## Overview

HubSpot's standard CRM includes contacts, companies, deals, and tickets.  Custom objects extend this functionality, enabling users to represent and organize CRM data tailored to their specific business needs. This API provides the tools to define custom objects, their properties, and associations with other HubSpot objects.

**Supported Products:**  Requires Marketing Hub Enterprise, Sales Hub Enterprise, Content Hub Enterprise, Service Hub Enterprise, or Operations Hub Enterprise.

**Account Specificity:** Custom objects are specific to each HubSpot account and are subject to creation limits depending on the subscription.  Refer to the HubSpot Products & Services catalog for details on your account's limits.

**Authentication:**  Use OAuth or private app access tokens for authentication. HubSpot API Keys are deprecated and no longer supported as of November 30, 2022.  [Learn more about migrating from API Keys](migration_link_needed).


## Authentication Methods

* **OAuth:**  [Link to OAuth documentation needed]
* **Private App Access Tokens:** [Link to Private App documentation needed]


## Create a Custom Object

Creating a custom object requires defining its schema, encompassing the object's name, properties, and associations.

**Request:** `POST /crm/v3/schemas`

**Request Body:** The request body must define the object schema, including:

* `name`:  (String) Object name.  Must start with a letter and contain only letters, numbers, and underscores.  Cannot be changed after creation.
* `description`: (String) Description of the object.
* `labels`: (Object)  Singular and plural labels for the object.
* `primaryDisplayProperty`: (String)  Property used to name individual object records.
* `secondaryDisplayProperties`: (Array of Strings) Properties displayed on individual records below the `primaryDisplayProperty`. The first property listed will also be added as a fourth filter on the object index page if it's a string, number, enumeration, boolean, or datetime type.
* `searchableProperties`: (Array of Strings) Properties indexed for searching.
* `requiredProperties`: (Array of Strings) Properties required when creating new records.
* `properties`: (Array of Objects)  Definition of each property (detailed below).
* `associatedObjects`: (Array of Strings)  Objects to associate with. Use object type IDs for custom objects and names for standard objects (e.g., "CONTACT", "COMPANY", "TICKET", "DEAL").


### Properties

Each property within the schema is defined as an object with the following attributes:

* `name`: (String) Property name.
* `label`: (String) Property label.
* `type`: (String) Property type. Valid values: `enumeration`, `date`, `dateTime`, `string`, `number`.
* `fieldType`: (String)  Field type in the UI. Valid values: `booleancheckbox`, `checkbox`, `date`, `file`, `number`, `radio`, `select`, `text`, `textarea`.
* `options`: (Array of Objects, only for `enumeration` type)  Array of label-value pairs for enumeration options.  Each object should have `label` and `value` properties.
* `hasUniqueValue`: (Boolean, optional) Set to `true` if the property should have unique values.  (Maximum of 10 unique value properties per custom object.)


| `type`       | Description                                         | Valid `fieldType` values                      |
|--------------|-----------------------------------------------------|----------------------------------------------|
| `enumeration` | A string representing a set of options (semicolon-separated). | `booleancheckbox`, `checkbox`, `radio`, `select` |
| `date`        | ISO 8601 formatted date (YYYY-MM-DD).             | `date`                                        |
| `dateTime`    | ISO 8601 formatted date and time.                   | `date`                                        |
| `string`      | Plain text string (up to 65,536 characters).      | `file`, `text`, `textarea`                   |
| `number`      | Number value.                                      | `number`                                      |


### Field Type Descriptions

* `booleancheckbox`: Single checkbox (Yes/No).
* `checkbox`: Multiple checkboxes.
* `date`: Date picker.
* `file`: File upload (stored as a URL).
* `number`: Numeric input.
* `radio`: Radio buttons.
* `select`: Dropdown.
* `text`: Single-line text input.
* `textarea`: Multi-line text input.



## Retrieve Existing Custom Objects

**Retrieve All:** `GET /crm/v3/schemas`

**Retrieve Specific:**

* `GET /crm/v3/schemas/{objectTypeId}`
* `GET /crm/v3/schemas/p_{object_name}`
* `GET /crm/v3/schemas/{fullyQualifiedName}`  (Use `fullyQualifiedName` from the schema response, derived from `p{portal_id}_{object_name}`)


## Retrieve Custom Object Records

**Single Record:** `GET /crm/v3/objects/{objectType}/{recordId}`

Query Parameters:

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return (including history).
* `associations`: Comma-separated list of associated objects to retrieve IDs for.


**Multiple Records:** `POST /crm/v3/objects/{objectType}/batch/read`

Request Body:

* `properties`:  Array of properties to retrieve.
* `idProperty`: (Optional) Name of a custom unique identifier property (used instead of `hs_object_id`).
* `inputs`: Array of objects, each containing an `id` (record ID or unique identifier value).

(Note: The batch endpoint does not retrieve associations.)


## Update Existing Custom Objects

Update an object's schema: `PATCH /crm/v3/schemas/{objectTypeId}`

**Note:** The object's name and labels cannot be changed after creation.  `requiredProperties`, `searchableProperties`, `primaryDisplayProperty`, and `secondaryDisplayProperties` can be updated.


## Update Associations

Add object associations: `POST /crm/v3/schemas/{objectTypeId}/associations`

Request Body:

* `fromObjectTypeId`: ID of the custom object.
* `toObjectTypeId`: ID or name of the object to associate with.
* `name`: Name of the association.


## Delete a Custom Object

Delete a custom object: `DELETE /crm/v3/schemas/{objectType}` (Requires all object instances, associations, and properties to be deleted first).

Hard delete (for recreating with the same name): `DELETE /crm/v3/schemas/{objectType}?archived=true`


## Custom Object Example: Car Inventory

This section provides a detailed walkthrough of creating a custom object to manage car inventory, including schema creation, record creation, associations, and property definition.  The full details of each request can be found in the original document's "Object Definition" tab (link needed).


**(This section would then include a detailed step-by-step guide with code examples as provided in the original text.)**


## Feedback

[Link to feedback form needed]


This markdown document provides a structured and readable version of the provided text, enhancing its usability as API documentation.  Remember to replace the bracketed placeholders with actual links where necessary.
