# HubSpot Custom Objects API Documentation

This document details the HubSpot Custom Objects API, allowing developers to create, manage, and interact with custom objects within their HubSpot accounts.

## Overview

HubSpot's standard CRM includes objects like contacts, companies, deals, and tickets. Custom objects extend this functionality, enabling the representation of business-specific data.  This API provides programmatic access to define custom objects, their properties, and associations with other CRM objects.  Note that custom objects are account-specific and subject to usage limits based on your HubSpot subscription.

**Supported Products:** Marketing Hub Enterprise, Sales Hub Enterprise, Content Hub Enterprise, Service Hub Enterprise, Operations Hub Enterprise.

## Authentication

The API supports the following authentication methods:

* **OAuth:**  Recommended for most integrations.
* **Private App Access Tokens:**  Suitable for internal applications or those requiring less user interaction.

**Deprecated:** HubSpot API Keys are no longer supported as of November 30, 2022.  Migrating existing integrations to OAuth or Private App Access Tokens is crucial for security.  [Learn more about the change](placeholder_link_to_migration_guide) and how to [migrate an API key integration](placeholder_link_to_migration_guide).


## Custom Object Management

### Creating a Custom Object

1. **Define the Object Schema:**  The schema defines the object's name, properties, and associations.  Use a `POST` request to `/crm/v3/schemas`.
    * **Object Name:** Must start with a letter, contain only letters, numbers, and underscores.  Cannot be changed after creation.  Long labels may be truncated.
    * **Properties:**  Define the data fields. Up to 10 unique value properties are allowed per custom object.  Specify `requiredProperties`, `searchableProperties`, `primaryDisplayProperty`, and `secondaryDisplayProperties`.
    * **Associations:** Specify associations to standard HubSpot objects (e.g., `CONTACT`, `COMPANY`, `DEAL`, `TICKET`) or other custom objects using their `objectTypeId`.  Automatic associations with emails, meetings, notes, tasks, calls, and conversations are built-in.

2. **Property Types:**

| `type`       | Description                                             | Valid `fieldType` values          |
|--------------|---------------------------------------------------------|---------------------------------|
| `enumeration` | A string representing a set of options (semicolon-separated). | `booleancheckbox`, `checkbox`, `radio`, `select` |
| `date`       | ISO 8601 formatted date (YYYY-MM-DD).                    | `date`                           |
| `dateTime`   | ISO 8601 formatted date and time. Time is not displayed in the UI. | `date`                           |
| `string`     | Plain text string (up to 65,536 characters).             | `file`, `text`, `textarea`       |
| `number`     | Numeric value.                                          | `number`                         |

3. **`fieldType` Descriptions:**

* `booleancheckbox`: Single checkbox (Yes/No).
* `checkbox`: Multiple checkbox selections.
* `date`: Date picker.
* `file`: File upload (stored as a URL).
* `number`: Numeric input.
* `radio`: Radio button selection.
* `select`: Dropdown selection.
* `text`: Single-line text input.
* `textarea`: Multi-line text input.

### Retrieving Custom Objects

* **All Custom Objects:** `GET` request to `/crm/v3/schemas`.
* **Specific Custom Object:** `GET` request to one of these endpoints:
    * `/crm/v3/schemas/{objectTypeId}`
    * `/crm/v3/schemas/p_{object_name}`
    * `/crm/v3/schemas/{fullyQualifiedName}` (`fullyQualifiedName` is derived from `p{portal_id}_{object_name}`)

### Retrieving Custom Object Records

* **Single Record:** `GET` request to `/crm/v3/objects/{objectType}/{recordId}`.  Use query parameters `properties`, `propertiesWithHistory`, and `associations`.
* **Multiple Records:** `POST` request to `/crm/v3/objects/{objectType}/batch/read`.  Retrieve by `hs_object_id` or a custom unique identifier property (`idProperty` parameter).  Associations cannot be retrieved using this endpoint.

### Updating Custom Objects

* **Update Schema:** `PATCH` request to `/crm/v3/schemas/{objectTypeId}`.  Object name and labels cannot be changed.
* **Update Associations:** `POST` request to `/crm/v3/schemas/{objectTypeId}/associations`.

### Deleting Custom Objects

* **Delete Custom Object:** `DELETE` request to `/crm/v3/schemas/{objectType}` (requires all object instances to be deleted first).
* **Hard Delete:** `DELETE` request to `/crm/v3/schemas/{objectType}?archived=true` (for deleting the schema to allow recreating an object with the same name).


## Example: Creating a "Cars" Custom Object

This example shows creating a custom object for tracking car inventory, associating it with contacts, and adding maintenance tracking using HubSpot tickets.  Detailed request bodies are included in the original text and are too extensive to reproduce here.  Refer to the original text for complete examples.


## Conclusion

The HubSpot Custom Objects API provides powerful tools for extending the CRM's capabilities.  By leveraging this API, developers can build customized solutions to manage unique business data within the HubSpot ecosystem.
