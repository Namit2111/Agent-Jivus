# HubSpot Custom Objects API Documentation

This document details the HubSpot API for creating, managing, and interacting with custom objects.  Custom objects extend the standard HubSpot CRM objects (contacts, companies, deals, tickets) to represent your unique business data.

## Supported Products

Custom objects require one of the following HubSpot products or higher:

* Marketing Hub - Enterprise
* Sales Hub - Enterprise
* Content Hub - Enterprise
* Service Hub - Enterprise
* Operations Hub - Enterprise


## Authentication

You can authenticate using:

* **OAuth:**  Recommended for most integrations.
* **Private app access tokens:** Suitable for internal applications.

**Note:** HubSpot API Keys are deprecated as of November 30, 2022, and are no longer supported.


## Creating a Custom Object

1. **Define the Object Schema:** The schema defines the object's name, properties, and associations with other objects.  Use a `POST` request to `/crm/v3/schemas`.

    * **Object Name:**  Must start with a letter, contain only letters, numbers, and underscores.  Cannot be changed after creation.
    * **Long Labels:** May be truncated in the UI.

2. **Properties:** Define properties to store information for each custom object record.  Up to 10 unique value properties are allowed per custom object.

    * **`requiredProperties`:** Properties required when creating new records.
    * **`searchableProperties`:** Properties indexed for searching.
    * **`primaryDisplayProperty`:**  Property used for naming records.
    * **`secondaryDisplayProperties`:** Properties displayed on individual records (below `primaryDisplayProperty`). The first property in this list will also be a filter on the object index page if it is a `string`, `number`, `enumeration`, `boolean`, or `datetime` type.

    | `type`       | Description                                                                    | Valid `fieldType` values             |
    |--------------|--------------------------------------------------------------------------------|---------------------------------------|
    | `enumeration` | String representing a set of options (semicolon-separated).                   | `booleancheckbox`, `checkbox`, `radio`, `select` |
    | `date`       | ISO 8601 formatted date (YYYY-MM-DD).                                        | `date`                               |
    | `dateTime`   | ISO 8601 formatted date and time. Time is not displayed in the HubSpot app. | `date`                               |
    | `string`     | Plain text string (up to 65,536 characters).                               | `file`, `text`, `textarea`           |
    | `number`     | Numeric value.                                                               | `number`                              |

    | `fieldType`      | Description                                                                                    |
    |-------------------|------------------------------------------------------------------------------------------------|
    | `booleancheckbox` | Single checkbox (Yes/No).                                                                      |
    | `checkbox`        | Multiple checkboxes.                                                                         |
    | `date`            | Date picker.                                                                                  |
    | `file`            | File upload (stored as a URL).                                                              |
    | `number`          | Numeric input.                                                                                |
    | `radio`           | Set of radio buttons.                                                                       |
    | `select`          | Dropdown.                                                                                     |
    | `text`            | Single-line text input.                                                                       |
    | `textarea`        | Multi-line text input.                                                                        |

3. **Associations:**  Automatically associated with emails, meetings, notes, tasks, calls, and conversations.  You can add associations with other standard or custom objects using the `associatedObjects` array in the schema definition.  Use the object name for standard objects and the `objectTypeId` for custom objects.


## Retrieving Custom Objects

* **All Custom Objects:** `GET` request to `/crm/v3/schemas`.
* **Specific Custom Object:** `GET` request to one of the following:
    * `/crm/v3/schemas/{objectTypeId}`
    * `/crm/v3/schemas/p_{object_name}`
    * `/crm/v3/schemas/{fullyQualifiedName}` (derived from `p{portal_id}_{object_name}`)


## Retrieving Custom Object Records

* **Single Record:** `GET` request to `/crm/v3/objects/{objectType}/{recordId}`.  Use query parameters `properties`, `propertiesWithHistory`, and `associations`.
* **Multiple Records:** `POST` request to `/crm/v3/objects/{objectType}/batch/read`.  Cannot retrieve associations using this endpoint.  Retrieve records by `hs_object_id` or a custom unique identifier property (`idProperty` parameter).


## Updating Custom Objects

* **Update Schema:** `PATCH` request to `/crm/v3/schemas/{objectTypeId}`.  Object name and labels cannot be changed.
* **Update Associations:** `POST` request to `/crm/v3/schemas/{objectTypeId}/associations`.


## Deleting Custom Objects

* **Delete Custom Object:** `DELETE` request to `/crm/v3/schemas/{objectType}` (requires all object instances to be deleted).
* **Hard Delete Schema:** `DELETE` request to `/crm/v3/schemas/{objectType}?archived=true` (allows recreating an object with the same name).


## Custom Object Example: Car Inventory

This section provides a detailed walkthrough of creating a "Cars" custom object to track car inventory, associating it with contacts and tickets, and adding a new property.  The example includes code snippets for the various API calls involved.  Refer to the original document for complete code examples.


## Conclusion

This documentation provides a comprehensive overview of the HubSpot Custom Objects API.  Remember to consult the HubSpot Developer Blog for further insights and best practices.
