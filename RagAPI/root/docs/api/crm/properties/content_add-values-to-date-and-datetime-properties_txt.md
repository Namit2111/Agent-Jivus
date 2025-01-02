# HubSpot CRM API: Properties

This document details the HubSpot CRM API's functionalities for managing properties. Properties are used to store information on CRM records (Contacts, Companies, Deals, etc.).  HubSpot provides default properties, and you can create custom properties via the API or the HubSpot UI.

## I. Property Types and `fieldType` Values

When creating or updating properties, both `type` and `fieldType` are required.  `type` defines the data type, while `fieldType` determines how it appears in the HubSpot UI or on forms.

| `type`       | Description                                         | Valid `fieldType` Values                     |
|--------------|-----------------------------------------------------|---------------------------------------------|
| `bool`       | Boolean value (true/false)                         | `booleancheckbox`, `calculation_equation`    |
| `enumeration` | String representing a set of options (semicolon-separated) | `booleancheckbox`, `checkbox`, `radio`, `select`, `calculation_equation` |
| `date`       | Date (YYYY-MM-DD)                                  | `date`                                      |
| `dateTime`   | Date and time (YYYY-MM-DDThh:mm:ss.sTZD)            | `date`                                      |
| `string`     | Plain text string (up to 65,536 characters)          | `file`, `text`, `textarea`, `calculation_equation`, `html`, `phonenumber` |
| `number`     | Numeric value                                       | `number`, `calculation_equation`            |
| `object_coordinates` | Internal use only, cannot be created or edited. | `text`                                      |
| `json`       | JSON formatted text, internal use only.           | `text`                                      |


| `fieldType`       | Description                                                                       |
|--------------------|-----------------------------------------------------------------------------------|
| `booleancheckbox` | Single checkbox (Yes/No).                                                        |
| `calculation_equation` | Calculated value based on a formula.                                             |
| `checkbox`         | Multiple checkboxes.                                                             |
| `date`             | Date picker.                                                                     |
| `file`             | File upload (stores file ID).                                                    |
| `html`             | Rich text editor (sanitized HTML).                                                |
| `number`           | Numeric input.                                                                   |
| `phonenumber`      | Phone number input (formatted).                                                   |
| `radio`            | Radio buttons (single selection).                                                 |
| `select`           | Dropdown menu.                                                                    |
| `text`             | Single-line text input.                                                          |
| `textarea`         | Multi-line text input.                                                           |


## II. API Endpoints

All endpoints are under the `/crm/v3/` base path.

**A. Create a Property:**

* **Method:** `POST`
* **Endpoint:** `/properties/{objectType}`
* **Request Body (JSON):**

```json
{
  "groupName": "contactinformation",
  "name": "favorite_food",
  "label": "Favorite Food",
  "type": "string",
  "fieldType": "text"
}
```

**B. Create Unique Identifier Property:**

* **Method:** `POST`
* **Endpoint:** `/properties/{objectType}`
* **Request Body (JSON):**  Add `hasUniqueValue: true`

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

**C. Create Calculation Property:**

* **Method:** `POST`
* **Endpoint:** `/properties/{objectType}`
* **Request Body (JSON):** Use `calculationFormula` and specify `fieldType: calculation_equation`.  `type` can be `number`, `bool`, `string`, or `enumeration`.

```json
{
  "groupName": "calculations",
  "name": "calculated_value",
  "label": "Calculated Value",
  "type": "number",
  "fieldType": "calculation_equation",
  "calculationFormula": "property1 + property2"
}
```

**D. Retrieve Properties:**

* **Method:** `GET`
* **Endpoint:** `/properties/{objectType}` (all properties) or `/properties/{objectType}/{propertyName}` (single property)
* **Query Parameter (for all properties):** `dataSensitivity=sensitive` (to retrieve sensitive data, Enterprise only).

**E. Update or Clear Property Values:**

* **Method:** `PATCH`
* **Endpoint:** `/objects/{objectType}/{recordId}`
* **Request Body (JSON):** Include properties and values in an array.  To clear a value, set it to an empty string (`""`).

```json
{
  "properties": {
    "firstname": "Updated Name",
    "lastname": "" // Clears lastname
  }
}
```

**F. Add Values to Date/DateTime Properties:**

* Use ISO 8601 (`YYYY-MM-DD` or `YYYY-MM-DDThh:mm:ss.sTZD`) or UNIX timestamps (milliseconds since epoch).  `date` properties should use EPOCH timestamps representing midnight UTC for the date.


**G. Add Values to Checkbox Properties:**

* **Boolean Checkbox:** `true` (checked), `false` (unchecked)
* **Multiple Checkbox:** Semicolon-separated values (`;value1;value2`).  A leading semicolon appends to existing values.

## III. Calculation Property Syntax

Calculation properties use a custom formula language.

**A. Literals:**

* **String:** Single or double quotes (`'constant'`, `"constant"`)
* **Number:**  Real numbers (e.g., `1005`, `1.5589`)
* **Boolean:** `true`, `false`

**B. Property Variables:**

* **String:** `string(propertyName)`
* **Number:** `propertyName`
* **Boolean:** `bool(propertyName)`

**C. Operators:**  `+`, `-`, `*`, `/`, `<`, `>`, `<=`, `>=`, `=`, `equals`, `!=`, `or`, `and`, `not`

**D. Functions:** `max()`, `min()`, `is_present()`, `contains()`, `concatenate()`, `number_to_string()`, `string_to_number()`

**E. Conditional Statements:** `if`, `elseif`, `else`, `endif`

## IV. Examples

See the original text for numerous examples of creating, retrieving, and updating properties, including calculation property formulas and handling various property types.


This comprehensive documentation provides a detailed overview of HubSpot's CRM API for managing properties, including API endpoints, request structures, data formats, and example usage. Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
