# HubSpot CRM API: Properties

This document details the HubSpot CRM API's functionality for managing properties. Properties store information on CRM records.  HubSpot provides default properties, and you can create custom properties via the API or the HubSpot UI.

## I.  Default Properties

Each CRM object (Contacts, Companies, Deals, Tickets, Activities, Leads) has a predefined set of default properties. These are name-value pairs and cannot be modified directly through the API (except for potentially adding values).  Refer to the HubSpot documentation for details on default properties for each object type.

## II. Property Groups

Property groups organize related properties for better record organization.  Custom properties should ideally be grouped for easy identification.

## III. Property Types and `fieldType` Values

When creating or updating properties, `type` and `fieldType` are crucial.  `type` defines the data type (string, number, bool, etc.), while `fieldType` determines how the property appears in the HubSpot UI (text field, dropdown, checkbox, etc.).

| `type`        | Description                                         | Valid `fieldType` Values                                      |
|---------------|-----------------------------------------------------|-------------------------------------------------------------|
| `bool`        | Boolean value (true/false)                          | `booleancheckbox`, `calculation_equation`                    |
| `enumeration` | String with options separated by semicolons           | `booleancheckbox`, `checkbox`, `radio`, `select`, `calculation_equation` |
| `date`        | Date (YYYY-MM-DD, ISO 8601, or EPOCH milliseconds) | `date`                                                     |
| `dateTime`    | Date and time (ISO 8601 or UNIX milliseconds)       | `date`                                                     |
| `string`      | Plain text string (up to 65,536 characters)        | `file`, `text`, `textarea`, `calculation_equation`, `html`, `phonenumber` |
| `number`      | Numeric value                                        | `number`, `calculation_equation`                            |
| `object_coordinates` | Internal use only, cannot be created/edited       | `text`                                                     |
| `json`        | JSON formatted text, internal use only              | `text`                                                     |


**`fieldType` Values:**

| `fieldType`          | Description                                                                         |
|----------------------|-------------------------------------------------------------------------------------|
| `booleancheckbox`    | Single checkbox (Yes/No)                                                            |
| `calculation_equation` | Property calculated from a formula                                                  |
| `checkbox`           | Multiple checkboxes                                                                  |
| `date`               | Date picker                                                                         |
| `file`               | File upload (stores file ID)                                                        |
| `html`               | Rich text editor                                                                    |
| `number`             | Numeric input                                                                        |
| `phonenumber`        | Phone number input                                                                   |
| `radio`              | Radio buttons (single selection)                                                    |
| `select`             | Dropdown menu                                                                        |
| `text`               | Single-line text input                                                              |
| `textarea`           | Multi-line text input                                                               |


## IV. API Calls

### A. Create a Property

**Endpoint:** `/crm/v3/properties/{objectType}`

**Method:** `POST`

**Request Body (JSON):**

```json
{
  "groupName": "groupName",
  "name": "propertyName",
  "label": "Property Label",
  "type": "string",  //e.g., "string", "number", "bool", "enumeration"
  "fieldType": "text" // e.g., "text", "number", "booleancheckbox", etc.
}
```

**Example (creating a "Favorite Food" contact property):**

```json
{
  "groupName": "contactinformation",
  "name": "favorite_food",
  "label": "Favorite Food",
  "type": "string",
  "fieldType": "text"
}
```

### B. Create Unique Identifier Properties

**Endpoint:** `/crm/v3/properties/{objectType}`

**Method:** `POST`

**Request Body (JSON):**  Add `hasUniqueValue: true` to the request body from section IV.A

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

**Example Usage:**  Retrieve a deal using this unique ID: `GET https://api.hubapi.com/crm/v3/objects/deals/abc?idProperty=system_a_unique`


### C. Create Calculation Properties

**Endpoint:** `/crm/v3/properties/{objectType}`

**Method:** `POST`

**Request Body (JSON):**  Use `calculation_equation` for `fieldType` and include the `calculationFormula`.

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

**Calculation Formula Syntax:**  See section V below for details on formula syntax, operators, functions, and conditional statements.

**Note:** API-created calculation properties cannot be edited in the HubSpot UI.

### D. Retrieve Properties

**Endpoint (individual property):** `/crm/v3/properties/{object}/{propertyName}`

**Method:** `GET`

**Endpoint (all properties):** `/crm/v3/properties/{objectType}`

**Method:** `GET`

**Query Parameter (for sensitive data):** `dataSensitivity=sensitive` (Beta, Enterprise only)

### E. Update or Clear Property Values

**Endpoint:** `/crm/v3/objects/{objectType}/{recordId}`

**Method:** `PATCH`

**Request Body (JSON):**  Update properties within the `properties` object. To clear a property, set its value to an empty string (`""`).


```json
{
  "properties": {
    "propertyName": "newValue",
    "anotherProperty": "" // Clears this property
  }
}
```

### F.  Date and DateTime Properties

Use ISO 8601 format for responses.  For API requests, use either ISO 8601 or UNIX timestamps in milliseconds (UTC).  `date` properties only store the date, while `datetime` stores both date and time.

### G. Checkbox Properties

* **Boolean checkbox:** Use `true` for checked, `false` for unchecked.
* **Multiple select checkbox:** Use semicolons to separate values. A leading semicolon appends values instead of overwriting.


### H. Assign Record Owners

Use the user's `id` (obtained from property settings or the owners API) in the `hubspot_owner_id` property.


## V. Calculation Property Syntax

### A. Literal Syntax

* **String:** Single or double quotes ('constant' or "constant")
* **Number:** Any real number (e.g., 1005, 1.5589)
* **Boolean:** `true` or `false`

### B. Property Syntax

* **String:** `string(propertyName)`
* **Number:** `propertyName`
* **Boolean:** `bool(propertyName)`

**Case Sensitivity:** Case-sensitive except for strings.

### C. Operators

| Operator | Description                               | Examples                                     |
|----------|-------------------------------------------|---------------------------------------------|
| `+`      | Add numbers or strings                    | `property1 + 100`                           |
| `-`      | Subtract numbers                           | `property1 + 100 - property2`                |
| `*`      | Multiply numbers                          | `10 * property1`                            |
| `/`      | Divide numbers                            | `property1 * (100 - property2 / (50 - property3))` |
| `<`      | Less than                                 | `a < 100`                                  |
| `>`      | Greater than                              | `a > 50`                                   |
| `<=`     | Less than or equal to                     | `a <= b`                                   |
| `>=`     | Greater than or equal to                  | `b >= c`                                   |
| `=`      | Equal to                                  | `(a + b - 100 * c * 150.652) = 150 - 230 * b` |
| `equals` | Equal to                                  | `a + b - 100.2 * c * 150 equals 150 - 230`    |
| `!=`     | Not equal to                              | `string(property1) != 'test_string'`       |
| `or`     | Logical OR                               | `a > b or b <= c`                          |
| `and`    | Logical AND                               | `bool(a) and bool(c)`                       |
| `not`    | Logical NOT                               | `not (bool(a) and bool(c))`                 |


### D. Functions

| Function      | Description                                                                   | Examples                     |
|---------------|-------------------------------------------------------------------------------|------------------------------|
| `max`         | Returns the maximum of 2-100 numbers                                        | `max(a, b, c, 100)`          |
| `min`         | Returns the minimum of 2-100 numbers                                        | `min(a, b, c, 100)`          |
| `is_present` | Checks if an expression can be evaluated (true if property exists and is boolean) | `is_present(bool(a))`       |
| `contains`   | Checks if one string contains another                                          | `contains('hello', 'ello')` |
| `concatenate`| Joins strings                                                                 | `concatenate('a', 'b', string(a), string(b))` |
| `number_to_string` | Converts a number to a string                                                | `number_to_string(num_cars)`|
| `string_to_number` | Converts a string to a number                                                | `string_to_number("123")`   |


### E. Conditional Statements

`if boolean_expression then statement [elseif expression then statement]* [else statement] endif`

**Example:**

```
if is_present(hs_latest_sequence_enrolled_date) then
  if is_present(hs_sequences_actively_enrolled_count) and hs_sequences_actively_enrolled_count >= 1 then
    true
  else
    false
  endif
else
  ''
endif
```

## VI.  Error Handling and Best Practices

* Always validate API responses for errors.
* Use appropriate HTTP methods (POST, GET, PATCH) for each operation.
* Follow HubSpot's API rate limits.
* Consider data sensitivity when retrieving properties.


This documentation provides a comprehensive overview of the HubSpot CRM API's property management features.  Refer to the official HubSpot API documentation for the most up-to-date information and details.
