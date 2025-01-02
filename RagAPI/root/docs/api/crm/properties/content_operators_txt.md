# HubSpot CRM API: Properties

This document details the HubSpot CRM API's functionality for managing properties.  Properties are used to store information on CRM records (contacts, companies, deals, etc.).  HubSpot provides default properties, and you can create custom properties using the API or the HubSpot UI.

## I. Property Types and Field Types

When creating or updating properties, you must specify both `type` and `fieldType`.

| `type`        | Description                                                                     | Valid `fieldType` values                     |
|---------------|---------------------------------------------------------------------------------|---------------------------------------------|
| `bool`        | Binary options (e.g., Yes/No, True/False).                                      | `booleancheckbox`, `calculation_equation` |
| `enumeration` | String representing a set of options (options separated by semicolons).           | `booleancheckbox`, `checkbox`, `radio`, `select`, `calculation_equation` |
| `date`        | Specific day, month, and year (UTC, ISO 8601 or EPOCH milliseconds).            | `date`                                      |
| `dateTime`    | Specific date and time (UTC, ISO 8601 or UNIX milliseconds).                     | `date`                                      |
| `string`      | Plain text string (up to 65,536 characters).                                   | `file`, `text`, `textarea`, `calculation_equation`, `html`, `phonenumber` |
| `number`      | Numeric value (at most one decimal).                                            | `number`, `calculation_equation`           |
| `object_coordinates` | (Internal use only) References other HubSpot objects. Cannot be created/edited. | `text`                                      |
| `json`        | (Internal use only) Text value stored as formatted JSON. Cannot be created/edited. | `text`                                      |


**`fieldType` Values:**

| `fieldType`           | Description                                                                                                     |
|-----------------------|-----------------------------------------------------------------------------------------------------------------|
| `booleancheckbox`     | Single checkbox (Yes/No).                                                                                       |
| `calculation_equation` | Custom equation based on other property values.                                                                 |
| `checkbox`            | Multiple checkboxes.                                                                                           |
| `date`                | Date picker.                                                                                                   |
| `file`                | File upload (stores file ID).                                                                                   |
| `html`                | Rich text editor.                                                                                             |
| `number`              | Numeric input.                                                                                                 |
| `phonenumber`         | Formatted phone number input.                                                                                   |
| `radio`               | Radio buttons (single selection).                                                                               |
| `select`              | Dropdown menu.                                                                                                |
| `text`                | Single-line text input.                                                                                       |
| `textarea`            | Multi-line text input.                                                                                        |


## II. API Endpoints

**A. Create a Property:**

* **Method:** `POST`
* **Endpoint:** `/crm/v3/properties/{objectType}`
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

**B. Create a Unique Identifier Property:**

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

**C. Create a Calculation Property:**

* **Method:** `POST`
* **Endpoint:** `/crm/v3/properties/{objectType}`
* **Request Body (JSON):**  Use `fieldType: calculation_equation` and specify the `calculationFormula`.

```json
{
  "groupName": "dealinformation",
  "name": "calculated_value",
  "label": "Calculated Value",
  "type": "number",
  "fieldType": "calculation_equation",
  "calculationFormula": "property1 + property2"
}
```

**D. Retrieve Properties:**

* **Method:** `GET`
* **Endpoint:**
    * Individual property: `/crm/v3/properties/{object}/{propertyName}`
    * All properties: `/crm/v3/properties/{objectType}`  (Use `dataSensitivity=sensitive` for sensitive properties).

**E. Update/Clear Property Values:**

* **Method:** `PATCH`
* **Endpoint:** `/crm/v3/objects/{objectType}/{recordId}`
* **Request Body (JSON):**  Update properties within the `properties` object.  Use an empty string `""` to clear a value.

```json
{
  "properties": {
    "firstname": "John",
    "lastname": "Doe"
  }
}
```


## III. Calculation Property Syntax

Calculation properties use a custom formula language.

**A. Literals:**

* String: `'constant'` or `"constant"`
* Number: `1005`, `1.5589`
* Boolean: `true`, `false`

**B. Property Variables:**

* String: `string(var1)`
* Number: `var1`
* Boolean: `bool(var1)`

**C. Operators:** `+`, `-`, `*`, `/`, `<`, `>`, `<=`, `>=`, `=`, `equals`, `!=`, `or`, `and`, `not`

**D. Functions:** `max()`, `min()`, `is_present()`, `contains()`, `concatenate()`, `number_to_string()`, `string_to_number()`

**E. Conditional Statements:**

```
if boolean_expression then statement [elseif expression then statement]* [else statement] endif
```


## IV. Date and DateTime Properties

* **ISO 8601:**  `YYYY-MM-DD` (date), `YYYY-MM-DDThh:mm:ss.sTZD` (datetime)
* **UNIX Timestamp (milliseconds):**  EPOCH milliseconds for `date` (midnight UTC), milliseconds for `datetime`.


## V. Checkbox Properties

* **Boolean Checkbox:** `true` (checked), `false` (unchecked)
* **Multiple Select Checkbox:**  Use semicolons to separate values (e.g., `;value1;value2`).  A leading semicolon appends values.


## VI.  Record Owners

Assign record owners using the user's `id` (obtainable via the Owners API or property settings) in a property like `hubspot_owner_id`.


This documentation provides a comprehensive overview of the HubSpot CRM API's property management capabilities.  Refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications.
