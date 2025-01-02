# HubSpot CRM API: Properties

This document details the HubSpot CRM API endpoints for managing properties. Properties are used to store information on CRM records (Contacts, Companies, Deals, etc.). HubSpot provides default properties, and you can create custom properties using the API or the HubSpot UI.

## API Endpoints

All endpoints are under the `/crm/v3/properties` base path.  Replace `{objectType}` with the object type (e.g., `contacts`, `companies`, `deals`).  Replace `{propertyName}` with the name of the property.  Replace `{recordId}` with the ID of the record.

### 1. Create a Property (POST `/crm/v3/properties/{objectType}`)

Creates a new custom property.

**Request Body (JSON):**

```json
{
  "groupName": "propertyGroupName", // Property group name
  "name": "propertyName", // Internal property name (e.g., "favorite_color")
  "label": "Property Label", // Display name in HubSpot (e.g., "Favorite Color")
  "type": "string|number|bool|enumeration|date|dateTime|object_coordinates|json", // Property type
  "fieldType": "text|textarea|number|select|radio|checkbox|booleancheckbox|date|file|html|phonenumber|calculation_equation", // Field type
  "hasUniqueValue": false|true // Optional: True for unique identifier properties (max 10 per object)
  "calculationFormula": "formula" // Optional, for calculation properties.  See "Calculation Property Syntax" below.
}
```

**Example (Creating a string property):**

```bash
curl -X POST \
  'https://api.hubapi.com/crm/v3/properties/contacts' \
  -H 'Content-Type: application/json' \
  -d '{
        "groupName": "contactinformation",
        "name": "favorite_food",
        "label": "Favorite Food",
        "type": "string",
        "fieldType": "text"
      }'
```

**Response (JSON - on success):**  A representation of the created property.

### 2. Retrieve a Property (GET `/crm/v3/properties/{objectType}/{propertyName}`)

Retrieves a specific property.

**Example:**

```bash
curl 'https://api.hubapi.com/crm/v3/properties/contacts/favorite_food'
```

**Response (JSON):**  Details of the specified property.

### 3. Retrieve All Properties (GET `/crm/v3/properties/{objectType}`)

Retrieves all properties for an object type.  By default, only non-sensitive properties are returned.  Use `dataSensitivity=sensitive` to include sensitive data (Enterprise only).

**Example:**

```bash
curl 'https://api.hubapi.com/crm/v3/properties/contacts?dataSensitivity=sensitive'
```

**Response (JSON):** An array of property objects.

### 4. Update a Property's Values (PATCH `/crm/v3/objects/{objectType}/{recordId}`)


Updates the value of a property for a specific record.  Requires an array of property updates in the request body.

**Example (Updating "favorite_food" for a contact):**

```bash
curl -X PATCH \
  'https://api.hubapi.com/crm/v3/objects/contacts/123' \
  -H 'Content-Type: application/json' \
  -d '{
        "properties": {
          "favorite_food": "Pizza"
        }
      }'
```

**Response (JSON):**  Updated record details.


### 5. Clear a Property Value (PATCH `/crm/v3/objects/{objectType}/{recordId}`)

Clears a property value by setting it to an empty string.

**Example:**

```bash
curl -X PATCH \
  'https://api.hubapi.com/crm/v3/objects/contacts/123' \
  -H 'Content-Type: application/json' \
  -d '{
        "properties": {
          "favorite_food": ""
        }
      }'
```

**Response (JSON):** Updated record details.


## Property Types and Field Types

| Type        | Description                                    | Valid `fieldType` Values                      |
|-------------|------------------------------------------------|----------------------------------------------|
| `bool`      | Boolean value (true/false)                     | `booleancheckbox`, `calculation_equation`     |
| `enumeration` | String representing a set of options           | `booleancheckbox`, `checkbox`, `radio`, `select`, `calculation_equation` |
| `date`       | Date (YYYY-MM-DD or EPOCH milliseconds)        | `date`                                      |
| `dateTime`   | Date and time (ISO 8601 or UNIX milliseconds)  | `date`                                      |
| `string`    | Plain text string                             | `text`, `textarea`, `file`, `html`, `phonenumber`, `calculation_equation` |
| `number`     | Numeric value                                  | `number`, `calculation_equation`            |
| `object_coordinates` | Internal use only                           | `text`                                      |
| `json`       | JSON formatted text                           | `text`                                      |

## Calculation Property Syntax

Calculation properties use a formula to derive their value from other properties.

**Literals:**

* Strings: `'string'` or `"string"`
* Numbers: `10`, `3.14`
* Booleans: `true`, `false`

**Property Variables:**

* Strings: `string(propertyName)`
* Numbers: `propertyName`
* Booleans: `bool(propertyName)`

**Operators:** `+`, `-`, `*`, `/`, `<`, `>`, `<=`, `>=`, `=`, `equals`, `!=`, `and`, `or`, `not`

**Functions:** `max()`, `min()`, `is_present()`, `contains()`, `concatenate()`, `number_to_string()`, `string_to_number()`

**Conditional Statements:**

`if boolean_expression then statement [elseif expression then statement]* [else statement] endif`


**Example Formula:**

`"calculationFormula": "if bool(isSubscribed) then 100 else 0"`


##  Error Handling

The API responses will include error codes and messages if something goes wrong.  Refer to the HubSpot API documentation for details.


This documentation provides a comprehensive overview of the HubSpot CRM API's property management features.  Always refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications.
