# HubSpot CRM API: Properties

This document details the HubSpot CRM API's functionality for managing properties. Properties are used to store information on CRM records (Contacts, Companies, Deals, etc.).  HubSpot provides default properties, and you can create custom properties via the API or the HubSpot UI.

## I. Default Properties

Each CRM object type (Contacts, Companies, Deals, etc.) has a predefined set of default properties.  These are name-value pairs and are documented individually for each object type within the HubSpot documentation (links provided in the original text).

## II. Property Groups

Property groups organize related properties, improving usability in the HubSpot UI.  Custom properties should ideally be grouped for better organization.

## III. Property Types and Field Types

When creating a property, you must specify both `type` and `fieldType`.

| `type`        | Description                                      | Valid `fieldType` Values                     |
|----------------|--------------------------------------------------|---------------------------------------------|
| `bool`         | Boolean value (True/False)                       | `booleancheckbox`, `calculation_equation`    |
| `enumeration` | String representing a set of options (semicolon-separated) | `booleancheckbox`, `checkbox`, `radio`, `select`, `calculation_equation` |
| `date`         | Date (YYYY-MM-DD) in UTC                          | `date`                                      |
| `dateTime`     | Date and time (YYYY-MM-DDThh:mm:ss.sTZD) in UTC | `date`                                      |
| `string`       | Plain text string (up to 65,536 characters)       | `file`, `text`, `textarea`, `calculation_equation`, `html`, `phonenumber` |
| `number`       | Numeric value                                     | `number`, `calculation_equation`            |
| `object_coordinates` | Internal use only, not creatable/editable          | `text`                                      |
| `json`         | JSON formatted text, internal use only            | `text`                                      |


Valid `fieldType` values and their descriptions:

| `fieldType`         | Description                                                                                               |
|----------------------|-----------------------------------------------------------------------------------------------------------|
| `booleancheckbox`    | Single checkbox (Yes/No).                                                                                 |
| `calculation_equation` | Calculated value based on a formula.                                                                       |
| `checkbox`           | Multiple checkboxes.                                                                                      |
| `date`               | Date picker.                                                                                             |
| `file`               | File upload (stores file ID).                                                                            |
| `html`               | Rich text editor (sanitized HTML).                                                                         |
| `number`             | Numeric input.                                                                                           |
| `phonenumber`        | Phone number input (formatted).                                                                           |
| `radio`              | Radio buttons (single selection).                                                                          |
| `select`             | Dropdown menu.                                                                                           |
| `text`               | Single-line text input.                                                                                   |
| `textarea`           | Multi-line text input.                                                                                   |


## IV. API Endpoints

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

**B. Create Unique Identifier Properties:**

* **Method:** `POST`
* **Endpoint:** `/crm/v3/properties/{objectType}`
* **Request Body (JSON):**  Includes `hasUniqueValue: true`

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
* **Request Body (JSON):** Includes `calculationFormula` and `fieldType: calculation_equation`

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
* **Endpoint (Individual):** `/crm/v3/properties/{object}/{propertyName}`
* **Endpoint (All):** `/crm/v3/properties/{objectType}`  (Use `dataSensitivity=sensitive` for sensitive properties).

**E. Update/Clear Property Values:**

* **Method:** `PATCH`
* **Endpoint:** `/crm/v3/objects/{objectType}/{recordId}`
* **Request Body (JSON):**  An array of properties and their values.  To clear a value, set it to an empty string (`""`).

```json
{
  "properties": {
    "propertyName": "newValue"
  }
}
```


## V. Calculation Property Syntax

Calculation properties use a formula language supporting:

* **Literals:** String ("string"), Number (123), Boolean (true/false)
* **Property Variables:** `string(propertyName)`, `propertyName` (for numbers), `bool(propertyName)`
* **Operators:** +, -, \*, /, <, >, <=, >=, =, equals, !=, and, or, not
* **Functions:** `max`, `min`, `is_present`, `contains`, `concatenate`, `number_to_string`, `string_to_number`
* **Conditional Statements:** `if`, `elseif`, `else`, `endif`


## VI. Date and DateTime Property Value Formatting

* **ISO 8601:**  `YYYY-MM-DD` (date), `YYYY-MM-DDThh:mm:ss.sTZD` (datetime)
* **UNIX Timestamp (milliseconds):**  Epoch timestamp in milliseconds (UTC).  For `date` type, use midnight UTC.

## VII. Checkbox Property Value Formatting

* **Boolean Checkbox:** `true` (checked), `false` (unchecked)
* **Multiple Checkbox:** Semicolon-separated values (`;value1;value2;value3`).  A leading semicolon appends values.

## VIII. Record Owner Assignment

Use the user's `id` (obtainable from the owners API or property settings) in the `hubspot_owner_id` property.


This comprehensive documentation provides a clear understanding of the HubSpot CRM API's property management capabilities. Remember to consult the official HubSpot API documentation for the most up-to-date information and detailed specifications.
