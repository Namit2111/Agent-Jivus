# HubSpot CRM API: Properties

This document details the HubSpot CRM API's functionality for managing properties.  Properties are used to store information on CRM records (Contacts, Companies, Deals, etc.). HubSpot provides default properties, and you can create custom properties via the API or the HubSpot UI.

## API Endpoints

The primary endpoint for interacting with properties is:

`/crm/v3/properties/{objectType}`

where `{objectType}` is the type of CRM object (e.g., `contacts`, `companies`, `deals`).

Methods:

* **`POST`**: Create a new property.
* **`GET`**: Retrieve properties (individual or all for an object type).
* **`PATCH`**: Update a property's value for a specific record.

## Property Types and `fieldType` Values

When creating a property, you must specify both `type` and `fieldType`.

| `type`         | Description                                                              | Valid `fieldType` Values             |
|-----------------|--------------------------------------------------------------------------|--------------------------------------|
| `bool`          | Boolean value (True/False).                                             | `booleancheckbox`, `calculation_equation` |
| `enumeration`   | String representing a set of options (e.g., "Option1;Option2;Option3"). | `booleancheckbox`, `checkbox`, `radio`, `select`, `calculation_equation` |
| `date`          | Date (YYYY-MM-DD or EPOCH milliseconds at midnight UTC).                 | `date`                               |
| `dateTime`      | Date and time (ISO 8601 or UNIX milliseconds).                            | `date`                               |
| `string`        | Plain text string (up to 65,536 characters).                             | `file`, `text`, `textarea`, `calculation_equation`, `html`, `phonenumber` |
| `number`        | Numeric value.                                                            | `number`, `calculation_equation`     |
| `object_coordinates` | Internal use only.                                                      | `text`                               |
| `json`          | JSON formatted text. Internal use only.                                  | `text`                               |


`fieldType` determines the UI representation:

| `fieldType`        | Description                                                                    |
|---------------------|--------------------------------------------------------------------------------|
| `booleancheckbox`  | Single checkbox (Yes/No).                                                    |
| `calculation_equation` | Calculated value based on a formula.                                         |
| `checkbox`         | Multiple checkboxes.                                                        |
| `date`             | Date picker.                                                                 |
| `file`             | File upload (stores file ID).                                                  |
| `html`             | Rich text editor (sanitized HTML).                                            |
| `number`           | Numeric input.                                                               |
| `phonenumber`      | Formatted phone number input.                                                |
| `radio`            | Radio buttons (single selection).                                             |
| `select`           | Dropdown menu.                                                              |
| `text`             | Single-line text input.                                                      |
| `textarea`         | Multi-line text input.                                                      |


## API Calls: Examples

### Create a Property

```json
POST /crm/v3/properties/contacts
{
  "groupName": "contactinformation",
  "name": "favorite_food",
  "label": "Favorite Food",
  "type": "string",
  "fieldType": "text"
}
```

### Create a Unique Identifier Property

```json
POST /crm/v3/properties/deals
{
  "groupName": "dealinformation",
  "name": "system_a_unique",
  "label": "Unique ID for System A",
  "hasUniqueValue": true,
  "type": "string",
  "fieldType": "text"
}
```

### Create a Calculation Property

```json
POST /crm/v3/properties/deals
{
  "groupName": "dealinformation",
  "name": "calculated_value",
  "label": "Calculated Value",
  "type": "number",
  "fieldType": "calculation_equation",
  "calculationFormula": "property1 + property2" 
}
```

### Retrieve a Property

```
GET /crm/v3/properties/contacts/favorite_food
```

### Retrieve All Properties

```
GET /crm/v3/properties/contacts
```

### Update a Property Value

```json
PATCH /crm/v3/objects/contacts/{contactId}
{
  "properties": {
    "favorite_food": "Pizza"
  }
}
```

### Add Values to Checkbox Properties (Multiple Select)

```json
PATCH /crm/v3/objects/contacts/{contactId}
{
  "properties": {
    "hs_buying_role": ";BUDGET_HOLDER;END_USER" //Append values
  }
}
```

### Clear a Property Value

```json
PATCH /crm/v3/objects/contacts/{contactId}
{
  "properties": {
    "firstname": ""
  }
}
```

## Calculation Property Syntax

Calculation properties use a custom formula language.  It supports:

* **Literals**: String ("string"), Number (123), Boolean (true/false).
* **Property Variables**: `string(propertyName)` for strings, `propertyName` for numbers, `bool(propertyName)` for booleans. Case-sensitive except for strings.
* **Operators**: +, -, *, /, =, equals, !=, <, >, <=, >=, and, or, not.
* **Functions**: `max()`, `min()`, `is_present()`, `contains()`, `concatenate()`, `number_to_string()`, `string_to_number()`.
* **Conditional Statements**: `if`, `elseif`, `else`, `endif`.


##  Date and DateTime Properties

Use ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDThh:mm:ss.sTZD) or UNIX timestamps (milliseconds since epoch, UTC).  `date` properties only store the date; `dateTime` properties store both date and time.  Time zones are handled automatically by HubSpot.


This documentation provides a comprehensive overview of the HubSpot CRM API's property management features.  Refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications.
