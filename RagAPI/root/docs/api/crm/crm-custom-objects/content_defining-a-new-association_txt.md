# HubSpot Custom Objects API Documentation

This document details the HubSpot Custom Objects API, allowing you to create, manage, and interact with custom objects within your HubSpot account.  Custom objects extend the standard CRM objects (contacts, companies, deals, tickets) to represent your specific business needs.

**Supported Products:** Marketing Hub Enterprise, Sales Hub Enterprise, Content Hub Enterprise, Service Hub Enterprise, Operations Hub Enterprise.

**Authentication:**

* OAuth
* Private app access tokens (HubSpot API Keys are deprecated)


## 1. Create a Custom Object

Creates a new custom object schema.  The schema defines the object's name, properties, and associations with other objects.

**Endpoint:** `POST /crm/v3/schemas`

**Request Body:**

```json
{
  "name": "object_name", // Must start with a letter, contain only letters, numbers, and underscores.  Cannot be changed after creation.
  "description": "Object description",
  "labels": {
    "singular": "Singular label",
    "plural": "Plural label"
  },
  "primaryDisplayProperty": "property_name", // Property used for naming individual records.
  "secondaryDisplayProperties": ["property_name1", "property_name2"], // Properties displayed on individual records.  The first property of this type (string, number, enumeration, boolean, datetime) will be added as a fourth filter on the object index page.
  "searchableProperties": ["property_name1", "property_name2"], // Properties indexed for searching.
  "requiredProperties": ["property_name1", "property_name2"], // Properties required when creating new records.
  "properties": [ // Array of property definitions (see section 2)
    {
      "name": "property_name",
      "label": "Property Label",
      "type": "string", // or "number", "date", "dateTime", "enumeration", "boolean"
      "fieldType": "text" // or "textarea", "number", "date", "checkbox", "radio", "select", "file", "booleancheckbox" (See section 2 for details)
      // ... other property options ...
    }
  ],
  "associatedObjects": ["CONTACT", "COMPANY", "objectTypeId"] // Array of associated object types. Use objectTypeId for custom objects.
}
```

**Response:**  The created object schema, including `objectTypeId` and `fullyQualifiedName`.

**Example:**  (See the "Custom object example" section in the provided text for a complete example.)


## 2. Properties

Defines the data fields within a custom object.

**Property Types and `fieldType` values:**

| `type`       | Description                                      | Valid `fieldType` values          |
|--------------|--------------------------------------------------|-----------------------------------|
| `enumeration` | String representing a set of options (semicolon-separated). | `booleancheckbox`, `checkbox`, `radio`, `select` |
| `date`       | ISO 8601 formatted date (YYYY-MM-DD).            | `date`                             |
| `dateTime`   | ISO 8601 formatted date and time. Time is not displayed in the UI. | `date`                             |
| `string`     | Plain text string (max 65,536 characters).        | `text`, `textarea`, `file`        |
| `number`     | Numeric value.                                   | `number`                           |
| `boolean`    | Boolean value.                                  | `booleancheckbox`, `checkbox`     |


**Unique Value Properties:**  A maximum of 10 unique value properties are allowed per custom object.  Set `hasUniqueValue: true` in the property definition.


## 3. Associations

Defines relationships between your custom object and other HubSpot objects.

**Create Association:**

**Endpoint:** `POST /crm/v3/schemas/{objectTypeId}/associations`

**Request Body:**

```json
{
  "fromObjectTypeId": "objectTypeId", // Your custom object's objectTypeId
  "toObjectTypeId": "objectTypeId or objectName", // Associated object's objectTypeId or name (e.g., "CONTACT", "COMPANY")
  "name": "association_name"
}
```

**Response:**  The created association details.


## 4. Retrieve Custom Objects

**Retrieve All Custom Objects:**

**Endpoint:** `GET /crm/v3/schemas`


**Retrieve a Specific Custom Object:**

**Endpoint Options:**

* `/crm/v3/schemas/{objectTypeId}`
* `/crm/v3/schemas/p_{object_name}`
* `/crm/v3/schemas/{fullyQualifiedName}`


## 5. Retrieve Custom Object Records

**Retrieve Single Record:**

**Endpoint:** `GET /crm/v3/objects/{objectType}/{recordId}`

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return with history.
* `associations`: Comma-separated list of associated objects to retrieve.


**Retrieve Multiple Records:**

**Endpoint:** `POST /crm/v3/objects/{objectType}/batch/read`

**Request Body:**

```json
{
  "properties": ["property_name1", "property_name2"],
  "idProperty": "unique_property_name", //Optional. Use for custom unique identifier.
  "inputs": [
    {"id": "recordId1"},
    {"id": "recordId2"}
  ]
}
```

**Response:**  An array of custom object records.


## 6. Update Custom Objects

**Update Object Schema:**

**Endpoint:** `PATCH /crm/v3/schemas/{objectTypeId}`

**Request Body:**  Update properties like `requiredProperties`, `searchableProperties`, `primaryDisplayProperty`, `secondaryDisplayProperties`.  You cannot change the object's name or labels.


**Update Associations:**  Use the same `POST` endpoint as creating an association (section 3) if adding new associations.  There isn't a direct API for removing associations.


## 7. Delete Custom Object

**Delete Custom Object:**

**Endpoint:** `DELETE /crm/v3/schemas/{objectType}`

*This endpoint only works if all object instances and properties of this object have been deleted.*

**Hard Delete (For recreating with same name):**

**Endpoint:** `DELETE /crm/v3/schemas/{objectType}?archived=true`


This documentation provides a comprehensive overview. Refer to the HubSpot API documentation for detailed specifications and error handling. Remember to replace placeholders like `{objectTypeId}`, `{objectType}`, `{recordId}` with your actual values.
