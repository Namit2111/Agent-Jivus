# HubSpot CRM API: Properties Documentation

This document details the HubSpot CRM API's functionality for managing properties. Properties are used to store information on CRM records (Contacts, Companies, Deals, etc.).  HubSpot provides default properties, and you can create custom ones via the API or the HubSpot UI.

## I. Property Types and Field Types

When creating or updating properties, you need both `type` and `fieldType`.

| `type`       | Description                                                                  | Valid `fieldType` Values                                      |
|--------------|------------------------------------------------------------------------------|---------------------------------------------------------------|
| `bool`       | Binary options (e.g., Yes/No, True/False).                                  | `booleancheckbox`, `calculation_equation`                     |
| `enumeration`| String representing a set of options (options separated by semicolons).       | `booleancheckbox`, `checkbox`, `radio`, `select`, `calculation_equation` |
| `date`       | Specific day, month, year (UTC, ISO 8601 or EPOCH milliseconds).             | `date`                                                        |
| `dateTime`   | Specific day, month, year, and time (UTC, ISO 8601 or UNIX milliseconds).    | `date`                                                        |
| `string`     | Plain text string (up to 65,536 characters).                               | `file`, `text`, `textarea`, `calculation_equation`, `html`, `phonenumber` |
| `number`     | Numeric value (at most one decimal).                                        | `number`, `calculation_equation`                             |
| `object_coordinates` | Internal use only; cannot be created or edited.                          | `text`                                                        |
| `json`       | Text value stored as formatted JSON; internal use only.                     | `text`                                                        |


**Valid `fieldType` Values:**

| `fieldType`          | Description                                                                                             |
|-----------------------|---------------------------------------------------------------------------------------------------------|
| `booleancheckbox`     | Single checkbox (Yes/No).                                                                                |
| `calculation_equation`| Custom equation calculating values based on other properties.                                            |
| `checkbox`            | Multiple checkboxes.                                                                                   |
| `date`                | Date picker.                                                                                            |
| `file`                | File upload (stores file ID).                                                                           |
| `html`                | Rich text editor (sanitized HTML).                                                                     |
| `number`              | Numeric input.                                                                                         |
| `phonenumber`         | Formatted phone number input.                                                                          |
| `radio`               | Radio buttons.                                                                                        |
| `select`              | Dropdown menu.                                                                                         |
| `text`                | Single-line text input.                                                                               |
| `textarea`            | Multi-line text input.                                                                                |


## II. API Endpoints

**A. Create a Property:**

* **Method:** `POST`
* **Endpoint:** `/crm/v3/properties/{objectType}`
* **Request Body (JSON):**
```json
{
  "groupName": "groupName",
  "name": "propertyName",
  "label": "Property Label",
  "type": "string", // or bool, enumeration, date, dateTime, number
  "fieldType": "text" // or other valid fieldType
}
```
* **Example (creating a contact property "Favorite Food"):**
```json
{
  "groupName": "contactinformation",
  "name": "favorite_food",
  "label": "Favorite Food",
  "type": "string",
  "fieldType": "text"
}
```

**B. Create Unique Identifier Properties:**

* **Method:** `POST`
* **Endpoint:** `/crm/v3/properties/{objectType}`
* **Request Body (JSON):**  Include `hasUniqueValue: true`
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

**C. Create Calculation Properties:**

* **Method:** `POST`
* **Endpoint:** `/crm/v3/properties/{objectType}`
* **Request Body (JSON):** Include `calculationFormula` and `fieldType: calculation_equation`
```json
{
  "groupName": "calculations",
  "name": "calculated_value",
  "label": "Calculated Value",
  "type": "number", // or bool, string, enumeration
  "fieldType": "calculation_equation",
  "calculationFormula": "property1 + property2"
}
```

**D. Retrieve Properties:**

* **Individual Property:**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v3/properties/{object}/{propertyName}`
    * **Example:** `https://api.hubapi.com/crm/v3/properties/contacts/favorite_food`
* **All Properties:**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v3/properties/{objectType}`
    * **Query Parameter:** `dataSensitivity=sensitive` (for sensitive properties, Enterprise only)

**E. Update/Clear Property Values:**

* **Method:** `PATCH`
* **Endpoint:** `/crm/v3/objects/{objectType}/{recordId}`
* **Request Body (JSON):**  Include properties and their values in the `properties` object.  To clear a value, set it to an empty string (`""`).
```json
{
  "properties": {
    "propertyName": "newValue",
    "anotherProperty": "" // Clears the value
  }
}
```

## III. Calculation Property Syntax

Calculation properties use a formula language.

**A. Literals:**

* String: `'constant'` or `"constant"`
* Number:  `1005`, `1.5589`
* Boolean: `true`, `false`

**B. Property Variables:**

* String: `string(propertyName)`
* Number: `propertyName`
* Boolean: `bool(propertyName)`

**C. Operators:**  `+`, `-`, `*`, `/`, `<`, `>`, `<=`, `>=`, `=`, `equals`, `!=`, `or`, `and`, `not`

**D. Functions:** `max()`, `min()`, `is_present()`, `contains()`, `concatenate()`, `number_to_string()`, `string_to_number()`

**E. Conditional Statements:**

`if boolean_expression then statement [elseif expression then statement]* [else statement] endif`


## IV. Date and DateTime Properties

* **ISO 8601:**  `YYYY-MM-DD` (date), `YYYY-MM-DDThh:mm:ss.sTZD` (dateTime)
* **UNIX Timestamp (milliseconds):**  EPOCH milliseconds for `date` (midnight UTC), milliseconds for `dateTime`.

## V. Checkbox Properties

* **Boolean Checkbox:** `true` (checked), `false` (unchecked)
* **Multiple Select Checkbox:**  Append values with semicolons (`;value1;value2;value3`).


## VI.  Record Owners

Use the user's `id` (obtainable from property settings or the Owners API) in the `hubspot_owner_id` property.


This documentation provides a comprehensive overview of the HubSpot CRM API's property management capabilities.  Refer to the official HubSpot API documentation for the most up-to-date information and detailed error handling.
