# HubSpot CRM API: Properties Documentation

This document details the HubSpot CRM API's functionality for managing properties.  Properties are used to store information on CRM records (Contacts, Companies, Deals, etc.). HubSpot provides default properties, and you can create custom properties via the API or the HubSpot UI.

## I. Default Properties

Each CRM object type (Contacts, Companies, Deals, etc.) has a predefined set of default properties.  These are name-value pairs representing standard information.  Refer to the HubSpot documentation for a complete list of default properties for each object type.


## II. Property Groups

Property groups organize related properties, improving UI presentation.  Custom object properties are typically grouped together for clarity.

## III. Property Types and `fieldType` Values

When creating or updating properties, you must specify both `type` and `fieldType`.  `type` defines the data type (string, number, boolean, etc.), while `fieldType` determines the UI element (text field, dropdown, checkbox, etc.).

| `type`        | Description                                         | Valid `fieldType` Values                     |
|---------------|-----------------------------------------------------|---------------------------------------------|
| `bool`        | Boolean (true/false)                               | `booleancheckbox`, `calculation_equation` |
| `enumeration` | String with semicolon-separated options               | `booleancheckbox`, `checkbox`, `radio`, `select`, `calculation_equation` |
| `date`        | Date (YYYY-MM-DD, ISO 8601 or EPOCH milliseconds)   | `date`                                      |
| `dateTime`    | Date and Time (YYYY-MM-DDThh:mm:ss.sTZD, ISO 8601 or UNIX milliseconds) | `date`                                      |
| `string`      | Plain text string (up to 65,536 characters)         | `file`, `text`, `textarea`, `calculation_equation`, `html`, `phonenumber` |
| `number`      | Numeric value                                        | `number`, `calculation_equation`           |
| `object_coordinates` | Internal use only, cannot be created or edited.    | `text`                                      |
| `json`        | JSON formatted text, internal use only.             | `text`                                      |


`fieldType` Values:

| `fieldType`          | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| `booleancheckbox`     | Single checkbox (Yes/No)                                                    |
| `calculation_equation`| Calculated value based on a formula                                          |
| `checkbox`            | Multiple checkboxes                                                          |
| `date`                | Date picker                                                                  |
| `file`                | File upload (stores file ID)                                                |
| `html`                | Rich text editor (sanitized HTML)                                           |
| `number`              | Numeric input field                                                          |
| `phonenumber`         | Phone number input field (formatted)                                         |
| `radio`               | Radio buttons (single selection)                                             |
| `select`              | Dropdown menu                                                                |
| `text`                | Single-line text input                                                       |
| `textarea`            | Multi-line text input                                                        |


## IV. API Calls

### A. Create a Property

**Endpoint:** `/crm/v3/properties/{objectType}`

**Method:** `POST`

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

**Response:**  A JSON representation of the newly created property.


### B. Create Unique Identifier Properties

**Endpoint:** `/crm/v3/properties/{objectType}`

**Method:** `POST`

**Request Body (JSON):**  Similar to creating a regular property, but include `hasUniqueValue: true`.

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

**Response:** A JSON representation of the newly created property.


### C. Create Calculation Properties

**Endpoint:** `/crm/v3/properties/{objectType}`

**Method:** `POST`

**Request Body (JSON):**  Specify `fieldType: calculation_equation` and `calculationFormula`.

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

**Response:** A JSON representation of the newly created property.  Note: Calculation properties created via API cannot be edited in the HubSpot UI.


### D. Retrieve Properties

**Individual Property:**

**Endpoint:** `/crm/v3/properties/{object}/{propertyName}`

**Method:** `GET`

**Example:** `https://api.hubapi.com/crm/v3/properties/contacts/favorite_food`

**All Properties:**

**Endpoint:** `/crm/v3/properties/{objectType}`

**Method:** `GET`

**Query Parameter:** `dataSensitivity=sensitive` (to retrieve sensitive data properties - BETA, Enterprise only)


### E. Update/Clear Property Values

**Endpoint:** `/crm/v3/objects/{objectType}/{recordId}`

**Method:** `PATCH`

**Request Body (JSON):**

```json
{
  "properties": {
    "propertyName": "newValue" 
  }
}
```

To clear a property, set its value to an empty string: `"propertyName": ""`


### F.  Add Values to Date/DateTime Properties

Use ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDThh:mm:ss.sTZD) or UNIX timestamps in milliseconds (UTC).  `date` properties only store the date, while `dateTime` properties store both date and time.


### G. Add Values to Checkbox Properties

* **Boolean Checkbox:** Use `true` (checked) or `false` (unchecked).
* **Multiple Select Checkbox:** Use semicolons to separate values; prepend a semicolon to append to existing values.  Example: `;value1;value2`


### H. Assign Record Owners

Use the user's `id` (obtainable from the Owners API or property settings).  The property name is typically `hubspot_owner_id`.

## V. Calculation Property Syntax

### A. Literal Syntax

* **Strings:** Single or double quotes ('constant' or "constant")
* **Numbers:** Any real number (e.g., 1005, 1.5589)
* **Booleans:** `true` or `false`

### B. Property Syntax

* **String Properties:** `string(propertyName)`
* **Number Properties:** `propertyName`
* **Boolean Properties:** `bool(propertyName)`

**Note:** Case-sensitive except for strings. Spaces, tabs, and newlines are ignored.

### C. Operators

| Operator | Description             | Examples                    |
|----------|--------------------------|-----------------------------|
| `+`      | Add (numbers or strings) | `property1 + 100`          |
| `-`      | Subtract                | `property1 - property2`     |
| `*`      | Multiply                | `10 * property1`           |
| `/`      | Divide                  | `property1 / property2`     |
| `<`      | Less than               | `a < 100`                   |
| `>`      | Greater than            | `a > 50`                    |
| `<=`     | Less than or equal to   | `a <= b`                    |
| `>=`     | Greater than or equal to | `b >= c`                    |
| `=`      | Equals                  | `(a + b) = c`               |
| `equals` | Equals                  | `a equals b`                |
| `!=`     | Not equals              | `string(property1) != 'test'` |
| `or`     | Logical OR              | `a > b or b <= c`           |
| `and`    | Logical AND             | `bool(a) and bool(c)`       |
| `not`    | Logical NOT             | `not bool(a)`               |

### D. Functions

| Function      | Description                                                              | Examples                 |
|---------------|--------------------------------------------------------------------------|--------------------------|
| `max`         | Returns the maximum of 2-100 numbers                                     | `max(a, b, c, 100)`      |
| `min`         | Returns the minimum of 2-100 numbers                                     | `min(a, b, c)`          |
| `is_present` | Checks if a property exists and has a value                               | `is_present(bool(a))`   |
| `contains`    | Checks if one string contains another                                      | `contains('hello', 'lo')`|
| `concatenate` | Joins strings                                                            | `concatenate('a', 'b')` |
| `number_to_string` | Converts a number to a string                                           | `number_to_string(a)`   |
| `string_to_number` | Converts a string to a number                                           | `string_to_number(a)`   |


### E. Conditional Statements

Use `if`, `elseif`, `else`, and `endif`.

Example:

```
if bool(property1) then "Value 1" else "Value 2" endif
```

## VI.  Example Formulas

* Simple: `"calculationFormula": "closed - started"`
* Advanced (with conditionals): 

```
"calculationFormula": "if is_present(hs_latest_sequence_enrolled_date) then if is_present(hs_sequences_actively_enrolled_count) and hs_sequences_actively_enrolled_count >= 1 then true else false else ''" 
```


This comprehensive documentation provides a complete overview of the HubSpot CRM API's property management features, enabling developers to effectively interact with HubSpot's data.  Remember to always consult the official HubSpot API documentation for the most up-to-date information and details.
