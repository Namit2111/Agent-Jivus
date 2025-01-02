# HubSpot CRM API: Properties Documentation

This document details the HubSpot CRM API's functionality for managing properties.  Properties are used to store information on CRM records (Contacts, Companies, Deals, etc.).  HubSpot provides default properties, and you can create custom properties via the API or the HubSpot UI.

## I. Property Types and `fieldType` Values

When creating or updating properties, both `type` and `fieldType` are required.  `type` defines the data type, while `fieldType` determines the UI representation in HubSpot.

| `type`        | Description                                                                | Valid `fieldType` Values                     |
|---------------|----------------------------------------------------------------------------|---------------------------------------------|
| `bool`        | Boolean value (True/False).                                                | `booleancheckbox`, `calculation_equation` |
| `enumeration` | String representing a set of options (e.g., "option1;option2;option3"). | `booleancheckbox`, `checkbox`, `radio`, `select`, `calculation_equation` |
| `date`        | Date (YYYY-MM-DD). Must be in UTC.                                      | `date`                                     |
| `dateTime`    | Date and time (YYYY-MM-DDThh:mm:ss.sTZD). Must be in UTC.                | `date`                                     |
| `string`      | Plain text string (max 65,536 characters).                               | `file`, `text`, `textarea`, `calculation_equation`, `html`, `phonenumber` |
| `number`      | Numeric value.                                                             | `number`, `calculation_equation`           |
| `object_coordinates` | (Internal use only)                                                        | `text`                                     |
| `json`        | (Internal use only)                                                        | `text`                                     |


| `fieldType`       | Description                                                                                                 |
|--------------------|-------------------------------------------------------------------------------------------------------------|
| `booleancheckbox` | Single checkbox (Yes/No).                                                                                  |
| `calculation_equation` | Calculated value based on a formula.                                                                     |
| `checkbox`        | Multiple checkboxes.                                                                                       |
| `date`            | Date picker.                                                                                                |
| `file`            | File upload (stores file ID).                                                                              |
| `html`            | Rich text editor (sanitized HTML).                                                                         |
| `number`          | Numeric input.                                                                                             |
| `phonenumber`     | Phone number input (formatted).                                                                            |
| `radio`           | Radio buttons (single selection).                                                                           |
| `select`          | Dropdown menu.                                                                                             |
| `text`            | Single-line text input.                                                                                    |
| `textarea`        | Multi-line text input.                                                                                    |


## II. API Endpoints

**A. Create a Property:**

* **Method:** `POST`
* **Endpoint:** `/crm/v3/properties/{objectType}`
* **Request Body (JSON):**

```json
{
  "groupName": "groupName", // Property group name
  "name": "propertyName",    // Internal property name (e.g., "favorite_food")
  "label": "Property Label", // Display name in HubSpot (e.g., "Favorite Food")
  "type": "string",          // Property type
  "fieldType": "text"       // Field type
}
```

**Example (Create a Contact Property):**

```bash
curl -X POST \
  https://api.hubapi.com/crm/v3/properties/contacts \
  -H 'Content-Type: application/json' \
  -d '{
    "groupName": "contactinformation",
    "name": "favorite_food",
    "label": "Favorite Food",
    "type": "string",
    "fieldType": "text"
  }'
```

**B. Create Unique Identifier Properties:**

* **Method:** `POST`
* **Endpoint:** `/crm/v3/properties/{objectType}`
* **Request Body (JSON):**  Add `hasUniqueValue: true` to the request body from A.

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
* **Request Body (JSON):** Add `calculationFormula` field.  `fieldType` must be `calculation_equation`.

```json
{
  "groupName": "calculations",
  "name": "calculated_value",
  "label": "Calculated Value",
  "type": "number",
  "fieldType": "calculation_equation",
  "calculationFormula": "property1 + property2" // Example formula
}
```


**D. Retrieve Properties:**

* **Method:** `GET`
* **Endpoint:**
    * Individual Property: `/crm/v3/properties/{objectType}/{propertyName}`
    * All Properties: `/crm/v3/properties/{objectType}` (add `dataSensitivity=sensitive` for sensitive properties - Enterprise only)

**E. Update Property Values:**

* **Method:** `PATCH`
* **Endpoint:** `/crm/v3/objects/{objectType}/{recordId}`
* **Request Body (JSON):**

```json
{
  "properties": {
    "propertyName": "newValue"
  }
}
```

**F. Clear Property Value:**

* **Method:** `PATCH`
* **Endpoint:** `/crm/v3/objects/{objectType}/{recordId}`
* **Request Body (JSON):** Set property value to an empty string.

```json
{
  "properties": {
    "propertyName": ""
  }
}
```


## III. Calculation Property Syntax

Calculation properties use a custom formula language.

**A. Literals:**

* String: `'string'` or `"string"`
* Number: `10`, `3.14`
* Boolean: `true`, `false`

**B. Property Variables:**

* String: `string(propertyName)`
* Number: `propertyName`
* Boolean: `bool(propertyName)`

**C. Operators:** `+`, `-`, `*`, `/`, `<`, `>`, `<=`, `>=`, `=`, `equals`, `!=`, `or`, `and`, `not`

**D. Functions:** `max()`, `min()`, `is_present()`, `contains()`, `concatenate()`, `number_to_string()`, `string_to_number()`

**E. Conditional Statements:**

```
if boolean_expression then statement [elseif expression then statement]* [else statement] endif
```

## IV. Date and DateTime Properties

* **ISO 8601:**  `YYYY-MM-DD` (date), `YYYY-MM-DDThh:mm:ss.sTZD` (datetime)
* **UNIX Timestamp (milliseconds):**  Epoch time in milliseconds (UTC).  For `date` type, use midnight UTC.


## V. Checkbox Properties

* **Boolean Checkbox:** `true` (checked), `false` (unchecked)
* **Multiple Select Checkbox:**  Use semicolons to separate values.  A leading semicolon appends to existing values.  e.g., `;value1;value2`


## VI.  Error Handling

The API returns standard HTTP status codes and JSON responses indicating success or failure, including error messages.  Check the response carefully for errors.


This documentation provides a comprehensive overview.  Refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications.
