# HubSpot Custom Objects API Documentation

This document details the HubSpot API for creating, managing, and interacting with custom objects.  Custom objects extend the standard HubSpot CRM objects (contacts, companies, deals, tickets) to allow for tailored data representation.

**Supported Products:** Marketing Hub Enterprise, Sales Hub Enterprise, Content Hub Enterprise, Service Hub Enterprise, Operations Hub Enterprise.

**Authentication:** OAuth or Private app access tokens.  HubSpot API Keys are deprecated.

## I. Creating a Custom Object

This involves defining the object's schema, including name, properties, and associations.

**1. Object Schema Definition:**

*   **Endpoint:** `POST /crm/v3/schemas`
*   **Request Body:**  A JSON object containing:
    *   `name`: (String, required) The object's name (alphanumeric and underscores only, must start with a letter).  This is immutable after creation.
    *   `description`: (String, optional) Description of the object.
    *   `labels`: (Object, required)  Singular and plural labels for the object.
    *   `primaryDisplayProperty`: (String, required) Property used for naming individual records.
    *   `secondaryDisplayProperties`: (Array of Strings, optional) Properties displayed on individual records below `primaryDisplayProperty`.  The first property of this type (string, number, enumeration, boolean, datetime) will also be added as a fourth filter on the object index page.
    *   `searchableProperties`: (Array of Strings, optional) Properties indexed for searching.
    *   `requiredProperties`: (Array of Strings, required) Properties required when creating new records.
    *   `properties`: (Array of Objects, required)  Definition of each property.  See section II. Properties for details.
    *   `associatedObjects`: (Array of Strings, optional)  IDs of associated objects (standard objects use names; custom objects use `objectTypeId`).

**Example Request:**

```json
{
  "name": "cars",
  "description": "Car inventory",
  "labels": {"singular": "Car", "plural": "Cars"},
  "primaryDisplayProperty": "model",
  "secondaryDisplayProperties": ["make"],
  "searchableProperties": ["year", "make", "vin", "model"],
  "requiredProperties": ["year", "make", "vin", "model"],
  "properties": [
    {"name": "year", "label": "Year", "type": "number", "fieldType": "number"},
    {"name": "make", "label": "Make", "type": "string", "fieldType": "text"},
    // ... other properties
  ],
  "associatedObjects": ["CONTACT"]
}
```

**2.  Response:**  A JSON object containing the created object's details, including its `objectTypeId` (used in subsequent API calls).


## II. Properties

Properties define the data fields within a custom object.

**Property Types:**

| `type`       | Description                                         | Valid `fieldType` values     |
|--------------|-----------------------------------------------------|-----------------------------|
| `enumeration` | A string representing a set of options (`;` separated) | `booleancheckbox`, `checkbox`, `radio`, `select` |
| `date`       | ISO 8601 formatted date (YYYY-MM-DD)                | `date`                       |
| `dateTime`   | ISO 8601 formatted date and time                    | `date`                       |
| `string`     | Plain text (up to 65,536 characters)              | `file`, `text`, `textarea`   |
| `number`     | Numeric value                                       | `number`                     |

**Field Types:**  Specifies how the property is displayed in the UI.

*   `booleancheckbox`: Single checkbox (Yes/No).
*   `checkbox`: Multiple checkboxes.
*   `date`: Date picker.
*   `file`: File upload (stored as a URL).
*   `number`: Numeric input.
*   `radio`: Radio buttons.
*   `select`: Dropdown.
*   `text`: Single-line text input.
*   `textarea`: Multi-line text input.

**Unique Value Properties:**  A custom object can have up to 10 unique value properties.  Set `hasUniqueValue: true` in the property definition.


## III. Retrieving Custom Objects

**1. All Custom Objects:**

*   **Endpoint:** `GET /crm/v3/schemas`

**2. Specific Custom Object:**

*   **Endpoint:** `GET /crm/v3/schemas/{objectTypeId}` or `/crm/v3/schemas/p_{object_name}` or `/crm/v3/schemas/{fullyQualifiedName}`
*   `fullyQualifiedName` is derived from `p{portal_id}_{object_name}`.


## IV. Retrieving Custom Object Records

**1. Single Record:**

*   **Endpoint:** `GET /crm/v3/objects/{objectType}/{recordId}`
*   **Query Parameters:** `properties`, `propertiesWithHistory`, `associations`

**2. Multiple Records (Batch):**

*   **Endpoint:** `POST /crm/v3/objects/{objectType}/batch/read`
*   **Request Body:**
    *   `properties`: Array of properties to retrieve.
    *   `propertiesWithHistory`: Array of properties to retrieve with history.
    *   `idProperty`: (Optional) Name of a unique identifier property if not using `hs_object_id`.
    *   `inputs`: Array of objects, each with an `id` (record ID or unique identifier value).  Associations cannot be retrieved via batch read.


## V. Updating Custom Objects

**1. Update Object Schema:**

*   **Endpoint:** `PATCH /crm/v3/schemas/{objectTypeId}`

**2. Update Associations:**

*   **Endpoint:** `POST /crm/v3/schemas/{objectTypeId}/associations`
*   Request Body includes `fromObjectTypeId`, `toObjectTypeId`, and `name`.

## VI. Deleting a Custom Object

*   **Endpoint:** `DELETE /crm/v3/schemas/{objectType}` (soft delete; only possible if all records and associations are deleted)
*   **Hard Delete:** `DELETE /crm/v3/schemas/{objectType}?archived=true`  (required to recreate an object with the same name).


## VII.  Associations

Custom objects automatically associate with emails, meetings, notes, tasks, calls, and conversations.  Additional associations can be defined with standard or custom objects.  Use the `objectTypeId` for custom objects and the object name for standard objects.


## VIII. Example Walkthrough (Car Inventory)

The provided text contains a detailed example of creating a "cars" custom object, including creating properties, associations, and records.  This section should be reviewed directly within the provided text for a complete understanding.  The example shows all API calls and their respective request and response structures.


This documentation provides a concise overview. Refer to the complete original text for detailed examples and nuanced information. Remember to consult the official HubSpot API documentation for the most up-to-date information and error handling.
