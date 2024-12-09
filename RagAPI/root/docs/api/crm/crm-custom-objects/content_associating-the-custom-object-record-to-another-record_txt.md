# HubSpot Custom Objects API Documentation

This document details how to interact with HubSpot's Custom Objects API.  It covers creating, retrieving, updating, and deleting custom objects, properties, and associations.

## Overview

HubSpot's standard CRM includes objects like contacts, companies, deals, and tickets.  Custom objects allow you to extend the CRM to represent your unique business data.  You can manage custom objects through the HubSpot UI or via the API.  Note that custom objects are account-specific and subject to usage limits based on your subscription.  Check the [HubSpot Products & Services catalog](link-to-catalog) for details.

## Authentication

The API supports the following authentication methods:

* **OAuth:**  (Recommended)
* **Private app access tokens:** (Recommended)
* **HubSpot API Keys:** (Deprecated as of November 30, 2022.  Migrate existing integrations to OAuth or private app access tokens. See [this change](link-to-change-details) and [migration guide](link-to-migration-guide) for more information.)


## Create a Custom Object

To create a custom object, you must define its schema using a `POST` request to `/crm/v3/schemas`.  The schema includes:

* **`name`:**  The object's name (alphanumeric and underscores only, must start with a letter.  Cannot be changed after creation).
* **`labels`:**  Singular and plural labels for the object.
* **`description`:** A description of the object's purpose.
* **`primaryDisplayProperty`:** The property used to display the object's name.
* **`secondaryDisplayProperties`:**  Additional properties displayed on object records (up to one additional property will be added as a fourth filter in the object index page if it's of type `string`, `number`, `enumeration`, `boolean`, or `datetime`).
* **`searchableProperties`:** Properties indexed for searching.
* **`requiredProperties`:** Properties required when creating new records.
* **`properties`:** An array defining the object's properties (maximum 10 unique value properties per object).  See the "Properties" section for details.
* **`associatedObjects`:** An array of associated objects (standard objects by name or custom objects by `objectTypeId`).  See the "Associations" section for details.


### Properties

Properties define the data fields within your custom object.  Each property has the following attributes:

* **`name`:** The property's name (used in API requests).
* **`label`:** The property's display label.
* **`type`:** The property's data type (`enumeration`, `date`, `dateTime`, `string`, `number`).
* **`fieldType`:** The type of input field used for the property (`booleancheckbox`, `checkbox`, `date`, `file`, `number`, `radio`, `select`, `text`, `textarea`).
* **`options` (for `enumeration` type):** An array of options for select, radio, and checkbox field types.  Each option has a `label` and `value`.
* **`hasUniqueValue` (for `string` type):**  Indicates if the property should have a unique value.


| `type`       | Description                                       | Valid `fieldType` values          |
|--------------|---------------------------------------------------|------------------------------------|
| `enumeration` | A string representing a set of options (semicolon separated) | `booleancheckbox`, `checkbox`, `radio`, `select` |
| `date`        | ISO 8601 formatted date (YYYY-MM-DD)              | `date`                             |
| `dateTime`    | ISO 8601 formatted date and time                 | `date`                             |
| `string`      | Plain text (up to 65,536 characters)              | `file`, `text`, `textarea`         |
| `number`      | Numeric value                                     | `number`                           |


### Associations

Custom objects automatically associate with emails, meetings, notes, tasks, calls, and conversations. You can add associations to other standard HubSpot objects or custom objects using the `associatedObjects` array in the schema definition.  Custom objects are identified by their `objectTypeId`.

## Retrieve Existing Custom Objects

* **All custom objects:** `GET /crm/v3/schemas`
* **Specific custom object:**
    * `GET /crm/v3/schemas/{objectTypeId}`
    * `GET /crm/v3/schemas/p_{object_name}`
    * `GET /crm/v3/schemas/{fullyQualifiedName}` (`fullyQualifiedName` is derived from `p{portal_id}_{object_name}`)


## Retrieve Custom Object Records

* **Single record:** `GET /crm/v3/objects/{objectType}/{recordId}` (Use query parameters `properties`, `propertiesWithHistory`, and `associations` to specify what data to retrieve).
* **Multiple records:** `POST /crm/v3/objects/{objectType}/batch/read` (cannot retrieve associations; use the Associations API for batch association retrieval).  Use `idProperty` to specify a custom unique identifier property if not using `hs_object_id`.


## Update Existing Custom Objects

Use a `PATCH` request to `/crm/v3/schemas/{objectTypeId}` to update an object's schema.  You cannot change the object's name or labels. You *can* change `requiredProperties`, `searchableProperties`, `primaryDisplayProperty`, and `secondaryDisplayProperties`.


## Update Associations

Use a `POST` request to `/crm/v3/schemas/{objectTypeId}/associations` to add associations between your custom object and other objects.


## Delete a Custom Object

To delete a custom object, all its instances, associations, and properties must be deleted first.  Use a `DELETE` request to `/crm/v3/schemas/{objectType}`.  To hard delete the schema (allowing reuse of the name), use the query parameter `?archived=true`.

## Custom Object Example

A detailed walkthrough of creating a custom object for a car dealership ("CarSpot") is provided in the original text, showcasing the creation of the object schema, records, associations, and properties.  This example is too lengthy to fully reproduce here but is well-described within the provided text.

## Conclusion

This documentation provides a comprehensive overview of the HubSpot Custom Objects API.  Refer to the original text for detailed examples and code snippets to guide your development. Remember to consult the HubSpot developer blog for further insights and best practices.
