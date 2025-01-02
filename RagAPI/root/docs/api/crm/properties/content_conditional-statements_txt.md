# HubSpot CRM API: Properties

This document details the HubSpot CRM API's functionality for managing properties.  Properties store information on CRM records (Contacts, Companies, Deals, etc.).  HubSpot provides default properties, and you can create custom ones via the API or the HubSpot UI.

## API Endpoints

All API endpoints are prefixed with `/crm/v3/properties/`.  Replace `{objectType}` with the object type (e.g., `contacts`, `companies`, `deals`).  Replace `{propertyName}` with the specific property name.  Replace `{recordId}` with the ID of the record you are updating.

* **`GET /{objectType}`:** Retrieve all properties for a given object type.  Include `dataSensitivity=sensitive` to retrieve sensitive data properties (Enterprise only, Beta).
* **`GET /{objectType}/{propertyName}`:** Retrieve a specific property's details.
* **`POST /{objectType}`:** Create a new property.
* **`PATCH /objects/{objectType}/{recordId}`:** Update or clear a property's value for a specific record.


## Property Types and `fieldType` Values

When creating or updating properties, you must specify both `type` and `fieldType`.

| `type`        | Description                                      | Valid `fieldType` Values            |
|----------------|--------------------------------------------------|------------------------------------|
| `bool`        | Boolean value (true/false)                       | `booleancheckbox`, `calculation_equation` |
| `enumeration` | String with options separated by semicolons       | `booleancheckbox`, `checkbox`, `radio`, `select`, `calculation_equation` |
| `date`        | Date (YYYY-MM-DD)                               | `date`                               |
| `dateTime`    | Date and time (YYYY-MM-DDThh:mm:ss.sTZD)        | `date`                               |
| `string`      | Plain text string (up to 65,536 characters)     | `file`, `text`, `textarea`, `calculation_equation`, `html`, `phonenumber` |
| `number`      | Numeric value                                    | `number`, `calculation_equation`     |
| `object_coordinates` | Internal use only, not creatable or editable     | `text`                               |
| `json`        | JSON formatted text, internal use only           | `text`                               |

`fieldType` values determine how the property appears in the HubSpot UI or on forms.

| `fieldType`           | Description                                                                     |
|------------------------|---------------------------------------------------------------------------------|
| `booleancheckbox`     | Single checkbox (Yes/No)                                                        |
| `calculation_equation` | Calculated value based on a formula                                             |
| `checkbox`            | Multiple checkboxes                                                             |
| `date`                | Date picker                                                                     |
| `file`                | File upload (stores file ID)                                                  |
| `html`                | Rich text editor                                                                |
| `number`              | Numeric input                                                                   |
| `phonenumber`         | Phone number input                                                              |
| `radio`               | Radio buttons (single selection)                                               |
| `select`              | Dropdown menu                                                                   |
| `text`                | Single-line text input                                                          |
| `textarea`            | Multi-line text input                                                           |


## Creating a Property (POST Request)

```json
{
  "groupName": "contactinformation",
  "name": "favorite_food",
  "label": "Favorite Food",
  "type": "string",
  "fieldType": "text"
}
```

This creates a contact property named "Favorite Food".  `groupName` is the property group (optional). `name` is the internal API name. `label` is the user-facing name.


## Creating Unique Identifier Properties

To create a property that accepts only unique values:

```json
{
  "groupName": "dealinformation",
  "name": "system_a_unique",
  "label": "Unique ID for System A",
  "hasUniqueValue": true,
  "type": "string",
  "fieldType": "text"
}
```

## Calculation Properties

Calculation properties derive their value from a formula.  They use a `calculationFormula` field and can be of type `number`, `bool`, `string`, or `enumeration`.

**Syntax:**

* **Literals:**  `"string"`, `100`, `true`
* **Property Variables:** `string(property_name)`, `property_name` (for numbers), `bool(property_name)`
* **Operators:** `+`, `-`, `*`, `/`, `<`, `>`, `<=`, `>=`, `=`, `equals`, `!=`, `or`, `and`, `not`
* **Functions:** `max()`, `min()`, `is_present()`, `contains()`, `concatenate()`, `number_to_string()`, `string_to_number()`
* **Conditional Statements:** `if`, `elseif`, `else`, `endif`

**Example Formula:**

```json
{
  "calculationFormula": "if is_present(propertyA) then propertyA + 10 else 0 endif"
}
```

**Note:** Calculation properties created via API cannot be edited in the HubSpot UI.


## Updating Property Values (PATCH Request)

```json
{
  "properties": {
    "favorite_food": "Pizza"
  }
}
```

This updates the `favorite_food` property for a specific record.


## Date and DateTime Properties

Use ISO 8601 format for dates (`YYYY-MM-DD`) and datetimes (`YYYY-MM-DDThh:mm:ss.sTZD`).  UNIX timestamps (milliseconds since epoch) are also accepted.  Remember that `date` properties only store the date, while `dateTime` properties store both date and time.


## Checkbox Properties

* **Boolean checkbox:** `true` (checked), `false` (unchecked)
* **Multiple select checkbox:** Use semicolons to separate values.  A leading semicolon appends values to existing ones.  Example: `;value1;value2`


## Clearing a Property Value

Set the property value to an empty string (`""`).


## Retrieving Properties


**Get all properties:** GET `/crm/v3/properties/{objectType}`

**Get a single property:** GET `/crm/v3/properties/{objectType}/{propertyName}`


This comprehensive documentation covers the essential aspects of HubSpot's CRM API for property management.  Refer to the HubSpot Developer documentation for the most up-to-date information and complete API specifications.
