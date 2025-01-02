# HubSpot Custom Objects API Documentation

This document details the HubSpot Custom Objects API, allowing developers to create, manage, and interact with custom objects within their HubSpot accounts.

## Supported Products

Requires one of the following HubSpot products or higher:

* Marketing Hub Enterprise
* Sales Hub Enterprise
* Content Hub Enterprise
* Service Hub Enterprise
* Operations Hub Enterprise


## Authentication

The API supports two authentication methods:

* **OAuth:**  Standard OAuth 2.0 flow for secure access.
* **Private App Access Tokens:**  For applications needing dedicated access.

**Note:** HubSpot API Keys are deprecated as of November 30, 2022.  Use OAuth or Private App Access Tokens instead.


## Creating a Custom Object

To create a custom object, you must define its schema using a POST request.

**Endpoint:** `/crm/v3/schemas`

**Method:** `POST`

**Request Body:**

The request body requires several key components:

* `name`:  The object's name (alphanumeric and underscores only, must start with a letter).  **Cannot be changed after creation.**
* `description`: A description of the object.
* `labels`: An object containing `singular` and `plural` labels for the object.
* `primaryDisplayProperty`: The property displayed prominently on object records.
* `secondaryDisplayProperties`: Properties displayed alongside the `primaryDisplayProperty`.  The first property of this array will also be added as a fourth filter on the object index page if it is a string, number, enumeration, boolean, or datetime type.
* `searchableProperties`: Properties indexed for searching.
* `requiredProperties`: Properties required when creating new records.
* `properties`: An array of property definitions (see "Properties" section below).
* `associatedObjects`: An array of associated object IDs (e.g., `"CONTACT"`, `"COMPANY"`, `"DEAL"`, `"TICKET"` or custom object `objectTypeId`).


**Example Request Body:**

```json
{
  "name": "cars",
  "description": "Tracks car inventory.",
  "labels": { "singular": "Car", "plural": "Cars" },
  "primaryDisplayProperty": "model",
  "secondaryDisplayProperties": ["make"],
  "searchableProperties": ["year", "make", "vin", "model"],
  "requiredProperties": ["year", "make", "vin", "model"],
  "properties": [
    {
      "name": "condition",
      "label": "Condition",
      "type": "enumeration",
      "fieldType": "select",
      "options": [{"label": "New", "value": "new"}, {"label": "Used", "value": "used"}]
    },
    { "name": "year", "label": "Year", "type": "number", "fieldType": "number" }
    // ... other properties
  ],
  "associatedObjects": ["CONTACT"]
}
```

**Response:**  The response includes the created object's `objectTypeId` and other details.


## Properties

When defining properties, you can specify the following:

| `type`       | Description                               | Valid `fieldType` values      |
|--------------|-------------------------------------------|-------------------------------|
| `enumeration` | A set of options (semicolon-separated)    | `booleancheckbox`, `checkbox`, `radio`, `select` |
| `date`        | ISO 8601 formatted date                   | `date`                         |
| `dateTime`    | ISO 8601 formatted date and time          | `date`                         |
| `string`      | Plain text string (up to 65,536 characters)| `file`, `text`, `textarea`     |
| `number`      | Numeric value                             | `number`                       |

**Note:**  A maximum of 10 unique value properties are allowed per custom object.


## Associations

Custom objects automatically associate with emails, meetings, notes, tasks, calls, and conversations. You can add more associations using:

**Endpoint:** `/crm/v3/schemas/{objectTypeId}/associations`

**Method:** `POST`

**Request Body:**

* `fromObjectTypeId`: The ID of your custom object.
* `toObjectTypeId`: The ID of the object to associate with (use name for standard objects or `objectTypeId` for custom objects).
* `name`: The name of the association.


**Example Request Body:**

```json
{
  "fromObjectTypeId": "2-3444025",
  "toObjectTypeId": "ticket",
  "name": "cat_to_ticket"
}
```

## Retrieving Custom Objects

* **All custom objects:** `GET /crm/v3/schemas`
* **Specific custom object:** `GET /crm/v3/schemas/{objectTypeId}` or `GET /crm/v3/schemas/p_{object_name}` or `GET /crm/v3/schemas/{fullyQualifiedName}`


## Retrieving Custom Object Records

* **Single record:** `GET /crm/v3/objects/{objectType}/{recordId}` (use query parameters `properties`, `propertiesWithHistory`, `associations`)
* **Multiple records:** `POST /crm/v3/objects/{objectType}/batch/read` (supports retrieving by `hs_object_id` or custom unique identifier property using `idProperty`)


## Updating Custom Objects

* **Update schema:** `PATCH /crm/v3/schemas/{objectTypeId}`
* **Update associations:** `POST /crm/v3/schemas/{objectTypeId}/associations`

**Note:** Object name and labels cannot be changed after creation.


## Deleting Custom Objects

`DELETE /crm/v3/schemas/{objectType}` (requires all object instances to be deleted first).  For a hard delete (to recreate with the same name): `DELETE /crm/v3/schemas/{objectType}?archived=true`.


## Example Walkthrough (Car Inventory)

This section provides a detailed example of creating and managing a "Cars" custom object.  Refer to the provided text for the specific API calls and request/response bodies.  The example covers:

1. **Creating the object schema:** Defining properties like condition, year, make, model, VIN, etc.
2. **Creating a custom object record:**  Adding a new car to the inventory.
3. **Associating the custom object record to another record:** Linking a car to a contact.
4. **Defining a new association:** Creating an association between "Cars" and "Tickets".
5. **Defining a new property:** Adding a "maintenance_package" property.
6. **Updating the object schema:** Adding the new property to `secondaryDisplayProperties`.


This comprehensive documentation provides a complete overview of the HubSpot Custom Objects API.  Remember to consult the official HubSpot API documentation for the most up-to-date information and detailed specifications.
