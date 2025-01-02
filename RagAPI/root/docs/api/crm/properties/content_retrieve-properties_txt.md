# HubSpot CRM API: Properties

This document details the HubSpot CRM API's functionality for managing properties.  Properties are used to store information on CRM records (Contacts, Companies, Deals, etc.). HubSpot provides default properties, and you can create custom ones via the API or the HubSpot UI.

## I.  API Endpoints

All endpoints are under the `/crm/v3/properties` base path.  Replace `{objectType}` with the object type (e.g., `contacts`, `companies`, `deals`).  Replace `{propertyName}` with the specific property name. Replace `{recordId}` with the ID of the record you are updating.

* **`POST /crm/v3/properties/{objectType}`**: Create a new property.
* **`GET /crm/v3/properties/{objectType}`**: Retrieve all properties for a given object type.  Add `?dataSensitivity=sensitive` to retrieve sensitive data (Enterprise only).
* **`GET /crm/v3/properties/{objectType}/{propertyName}`**: Retrieve a specific property.
* **`PATCH /crm/v3/objects/{objectType}/{recordId}`**: Update or clear a property's value for a specific record.


## II. Property Types and `fieldType` Values

When creating a property, you must specify both `type` and `fieldType`.

| `type`       | Description                                      | Valid `fieldType` Values                     |
|--------------|--------------------------------------------------|---------------------------------------------|
| `bool`       | Boolean value (true/false)                       | `booleancheckbox`, `calculation_equation` |
| `enumeration` | String representing a set of options (semicolon-separated) | `booleancheckbox`, `checkbox`, `radio`, `select`, `calculation_equation` |
| `date`       | Date (YYYY-MM-DD or EPOCH milliseconds at midnight UTC) | `date`                                     |
| `dateTime`   | Date and time (ISO 8601 or UNIX milliseconds UTC) | `date`                                     |
| `string`     | Plain text string (up to 65,536 characters)      | `file`, `text`, `textarea`, `calculation_equation`, `html`, `phonenumber` |
| `number`     | Numeric value                                     | `number`, `calculation_equation`            |
| `object_coordinates` | Internal use only; cannot be created or edited. | `text`                                     |
| `json`       | JSON formatted text; Internal use only.         | `text`                                     |


`fieldType` determines how the property appears in the HubSpot UI or on forms.

| `fieldType`           | Description                                                                     |
|------------------------|---------------------------------------------------------------------------------|
| `booleancheckbox`     | Single checkbox (Yes/No)                                                        |
| `calculation_equation` | Calculated value based on a formula.                                            |
| `checkbox`            | Multiple checkboxes                                                              |
| `date`                | Date picker                                                                     |
| `file`                | File upload (stores file ID)                                                   |
| `html`                | Rich text editor (sanitized HTML)                                               |
| `number`              | Numeric input                                                                    |
| `phonenumber`         | Formatted phone number input                                                     |
| `radio`               | Radio buttons (single selection)                                                |
| `select`              | Dropdown menu                                                                    |
| `text`                | Single-line text input                                                          |
| `textarea`            | Multi-line text input                                                           |


## III. Creating a Property

Use a `POST` request to `/crm/v3/properties/{objectType}`.  The request body requires:

* `groupName`: Property group name.
* `name`: Internal property name (e.g., `favorite_food`).
* `label`: Display name (e.g., `Favorite Food`).
* `type`: Property type (see table above).
* `fieldType`: Field type (see table above).
* `hasUniqueValue` (optional): Set to `true` to enforce unique values (max 10 per object).


**Example (creating a `string` property):**

```json
{
  "groupName": "contactinformation",
  "name": "favorite_food",
  "label": "Favorite Food",
  "type": "string",
  "fieldType": "text"
}
```

## IV.  Calculation Properties

Calculation properties derive their value from a formula using other properties.  Use `fieldType: calculation_equation`.  The formula is specified using the `calculationFormula` field.  These properties *cannot* be edited in the HubSpot UI, only via the API.

**Syntax:**

* **Literals:**  `'string'`, `"string"`, `100`, `1.5`, `true`, `false`
* **Property Variables:** `string(property_name)`, `property_name` (for numbers), `bool(property_name)`
* **Operators:** `+`, `-`, `*`, `/`, `<`, `>`, `<=`, `>=`, `=`, `equals`, `!=`, `or`, `and`, `not`
* **Functions:** `max()`, `min()`, `is_present()`, `contains()`, `concatenate()`, `number_to_string()`, `string_to_number()`
* **Conditional Statements:** `if`, `elseif`, `else`, `endif`

**Example Formula:**

```json
{
  "groupName": "calculations",
  "name": "calculated_value",
  "label": "Calculated Value",
  "type": "number",
  "fieldType": "calculation_equation",
  "calculationFormula": "property1 + property2 * 10"
}
```


## V. Updating Property Values

Use a `PATCH` request to `/crm/v3/objects/{objectType}/{recordId}`.  Include the property updates in the `properties` field.

**Examples:**

* **String Property:**
  ```json
  {
    "properties": {
      "favorite_food": "Pizza"
    }
  }
  ```

* **Checkbox Property (single):**
  ```json
  {
    "properties": {
      "subscribed": true
    }
  }
  ```

* **Checkbox Property (multiple):**
  ```json
  {
    "properties": {
      "interests": ";Hiking;Camping;Skiing" // Semicolons separate values, leading semicolon appends
    }
  }
  ```

* **Date Property (ISO 8601):**
  ```json
  {
    "properties": {
      "birthdate": "1985-03-15"
    }
  }
  ```

* **Datetime Property (ISO 8601):**
  ```json
  {
    "properties": {
      "last_contact": "2024-10-27T10:30:00Z"
    }
  }
  ```

* **Clearing a Property Value:**
  ```json
  {
    "properties": {
      "favorite_food": ""
    }
  }
  ```

## VI.  Retrieving Properties

* **Individual Property:** `GET /crm/v3/properties/{objectType}/{propertyName}`
* **All Properties:** `GET /crm/v3/properties/{objectType}` (add `?dataSensitivity=sensitive` for sensitive data, Enterprise only)


This comprehensive guide provides a detailed overview of the HubSpot CRM API's properties functionality. Remember to consult the official HubSpot API documentation for the most up-to-date information and error handling.
