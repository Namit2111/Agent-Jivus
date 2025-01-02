# HubSpot CRM API: Properties Documentation

This document details the HubSpot CRM API's functionality for managing properties.  Properties are used to store information on CRM records (Contacts, Companies, Deals, etc.). HubSpot provides default properties, and you can create custom ones via the API or the HubSpot UI.

## I. Property Types and `fieldType` Values

When creating or updating properties, you need to specify both `type` and `fieldType`.

| `type`        | Description                                                                   | Valid `fieldType` Values                  |
|---------------|-------------------------------------------------------------------------------|------------------------------------------|
| `bool`        | Binary options (e.g., Yes/No, True/False).                                     | `booleancheckbox`, `calculation_equation` |
| `enumeration` | String representing a set of options (options separated by semicolons).       | `booleancheckbox`, `checkbox`, `radio`, `select`, `calculation_equation` |
| `date`        | Specific day, month, and year (UTC, ISO 8601 or EPOCH milliseconds).         | `date`                                   |
| `dateTime`    | Specific date and time (UTC, ISO 8601 or UNIX milliseconds).                   | `date`                                   |
| `string`      | Plain text string (up to 65,536 characters).                               | `file`, `text`, `textarea`, `calculation_equation`, `html`, `phonenumber` |
| `number`      | Numeric value (at most one decimal).                                          | `number`, `calculation_equation`          |
| `object_coordinates` | Internal use only; cannot be created or edited.                             | `text`                                   |
| `json`        | Text value stored as formatted JSON; internal use only; cannot be created or edited. | `text`                                   |


`fieldType` values determine how the property appears in HubSpot or on a form:

| `fieldType`           | Description                                                                                             |
|-----------------------|---------------------------------------------------------------------------------------------------------|
| `booleancheckbox`     | Single checkbox (Yes/No).                                                                            |
| `calculation_equation` | Custom equation to calculate values based on other properties.                                        |
| `checkbox`            | Multiple checkboxes to select multiple options.                                                        |
| `date`                | Date picker.                                                                                           |
| `file`                | File upload (stores file ID).                                                                         |
| `html`                | Rich text editor (sanitized HTML).                                                                     |
| `number`              | Numeric input.                                                                                        |
| `phonenumber`         | Formatted phone number input.                                                                         |
| `radio`               | Radio buttons to select one option.                                                                    |
| `select`              | Dropdown menu to select one option.                                                                    |
| `text`                | Single-line text input.                                                                               |
| `textarea`            | Multi-line text input.                                                                               |


## II. API Endpoints

All endpoints are under `/crm/v3/properties`.

### A. Create a Property

**Method:** `POST /crm/v3/properties/{objectType}`

**Request Body (JSON):**

```json
{
  "groupName": "contactinformation",
  "name": "favorite_food",
  "label": "Favorite Food",
  "type": "string",
  "fieldType": "text"
}
```

* `groupName`: Property group name.
* `name`: Internal property name (e.g., `favorite_food`).
* `label`: Display name (e.g., `Favorite Food`).
* `type`: Property type (see table above).
* `fieldType`: Field type (see table above).
* `hasUniqueValue`: (Optional) Set to `true` to enforce unique values (max 10 per object).


### B. Create Unique Identifier Properties

Similar to creating a property, but include `hasUniqueValue: true`.

**Request Body (JSON):**

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

Example GET request using unique identifier:
`GET https://api.hubapi.com/crm/v3/objects/deals/abc?idProperty=system_a_unique`

### C. Create Calculation Properties

**Method:** `POST /crm/v3/properties/{objectType}`

**Request Body (JSON):**

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

* `calculationFormula`: Formula defining the calculation (see section below).  **Note:** API-created calculation properties cannot be edited in the HubSpot UI.


### D. Retrieve Properties

**Method:** `GET /crm/v3/properties/{objectType}` or `GET /crm/v3/properties/{objectType}/{propertyName}`

* To get all properties for an object type, use the first endpoint.  Include `dataSensitivity=sensitive` to get sensitive data (Enterprise only).
* To get a single property, use the second endpoint.


### E. Update/Clear Property Values

**Method:** `PATCH /crm/v3/objects/{objectType}/{recordId}`

**Request Body (JSON):**

```json
{
  "properties": {
    "propertyName": "newValue"
  }
}
```

To clear a value, set it to an empty string: `""`.

### F.  Date/DateTime Property Value Formatting

* **ISO 8601:**
    * Date: `YYYY-MM-DD` (e.g., `2024-10-27`)
    * DateTime: `YYYY-MM-DDThh:mm:ss.sTZD` (e.g., `2024-10-27T14:30:00.000Z`)
* **UNIX Timestamp (milliseconds):**  UTC time.


### G. Checkbox Property Value Formatting

* **Boolean Checkbox:** `true` (checked), `false` (unchecked)
* **Multiple Checkbox:**  Use semicolons to separate values.  A leading semicolon appends to existing values.  e.g., `;value1;value2`


## III. Calculation Property Syntax

Calculation properties use a formula language with:

* **Literal Syntax:**  Strings (`'constant'`, `"constant"`), numbers (e.g., `1005`, `1.5589`), booleans (`true`, `false`).
* **Property Syntax:**  Use `string(propertyName)` for string properties, and `propertyName` for number properties, `bool(propertyName)` for boolean properties. Case-sensitive (except strings).
* **Operators:**  `+`, `-`, `*`, `/`, `<`, `>`, `<=`, `>=`, `=`, `equals`, `!=`, `or`, `and`, `not`.
* **Functions:** `max()`, `min()`, `is_present()`, `contains()`, `concatenate()`, `number_to_string()`, `string_to_number()`.
* **Conditional Statements:** `if`, `elseif`, `else`, `endif`.


## IV. Examples

**Example Calculation Formula:**

`"calculationFormula": "if is_present(propertyA) then propertyA * 2 else 0 endif"`


## V. Error Handling

The API will return appropriate HTTP status codes and error messages in the response body to indicate success or failure of the request.  Refer to the HubSpot API documentation for details on error codes.


This documentation provides a comprehensive overview of the HubSpot CRM API's properties functionality.  Remember to consult the official HubSpot API documentation for the most up-to-date information and detailed specifications.
