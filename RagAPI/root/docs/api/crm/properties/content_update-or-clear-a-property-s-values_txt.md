# HubSpot CRM API: Properties

This document details the HubSpot CRM API's functionality for managing properties. Properties are used to store information on CRM records (Contacts, Companies, Deals, etc.).  HubSpot provides default properties, and you can create custom properties via the API or the HubSpot UI.

## I.  Default Properties

Each CRM object type (Contacts, Companies, Deals, etc.) has a predefined set of default properties.  These are name-value pairs and cannot be modified directly.  Refer to the HubSpot documentation for the specific default properties of each object type.

## II. Property Groups

Property groups organize related properties for better record organization.  Properties within a group appear together on HubSpot records.  Custom object properties should ideally be grouped.

## III. Property Types and Field Types

When creating properties, you specify both `type` and `fieldType`.

| `type`         | Description                                                              | `fieldType` Values                     |
|-----------------|--------------------------------------------------------------------------|---------------------------------------|
| `bool`          | Binary options (True/False, Yes/No)                                      | `booleancheckbox`, `calculation_equation` |
| `enumeration`   | String representing a set of options (separated by semicolons)            | `booleancheckbox`, `checkbox`, `radio`, `select`, `calculation_equation` |
| `date`          | Specific date (YYYY-MM-DD or EPOCH milliseconds at midnight UTC)          | `date`                               |
| `dateTime`      | Specific date and time (ISO 8601 or UNIX milliseconds UTC)                | `date`                               |
| `string`        | Plain text string (up to 65,536 characters)                             | `file`, `text`, `textarea`, `calculation_equation`, `html`, `phonenumber` |
| `number`        | Numeric value                                                             | `number`, `calculation_equation`      |
| `object_coordinates` | Internal use only, references other HubSpot objects. Cannot be created or edited via API. | `text`                               |
| `json`          | Text value stored as formatted JSON.  Cannot be created or edited via API. | `text`                               |


**`fieldType` Values:**

| `fieldType`          | Description                                                                                             |
|-----------------------|---------------------------------------------------------------------------------------------------------|
| `booleancheckbox`    | Single checkbox (Yes/No)                                                                              |
| `calculation_equation` | Calculated value based on a formula.  Cannot be edited in HubSpot UI after API creation.          |
| `checkbox`           | Multiple checkboxes                                                                                    |
| `date`               | Date picker                                                                                            |
| `file`               | File upload (stores file ID)                                                                          |
| `html`               | Rich text editor (sanitized HTML)                                                                     |
| `number`             | Numeric input                                                                                          |
| `phonenumber`        | Formatted phone number input                                                                           |
| `radio`              | Radio buttons (single selection)                                                                      |
| `select`             | Dropdown menu                                                                                          |
| `text`               | Single-line text input                                                                                |
| `textarea`           | Multi-line text input                                                                               |


## IV. Creating Properties

Use a `POST` request to `/crm/v3/properties/{objectType}`.

**Required Fields:**

* `groupName`: Property group name.
* `name`: Internal property name (e.g., `favorite_food`).
* `label`: Display name in HubSpot (e.g., "Favorite Food").
* `type`: Property type (see table above).
* `fieldType`: Field type (see table above).

**Example (Create "Favorite Food" contact property):**

```json
{
  "groupName": "contactinformation",
  "name": "favorite_food",
  "label": "Favorite Food",
  "type": "string",
  "fieldType": "text"
}
```

## V. Creating Unique Identifier Properties

To create a property that must have unique values per object:

* Send a `POST` request to `/crm/v3/properties/{objectType}`.
* Set `hasUniqueValue` to `true` in the request body.  You can have up to ten unique ID properties per object.

**Example:**

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

## VI. Creating Calculation Properties

Calculation properties derive their value from a formula based on other properties within the same record.

* Use `fieldType: calculation_equation`.
* Use `type`: `number`, `bool`, `string`, or `enumeration`.
* Define the formula using the `calculationFormula` field.  See the section below for formula syntax.

**Important:** Calculation properties created via the API cannot be edited in the HubSpot UI.


## VII. Calculation Property Syntax

The `calculationFormula` uses a custom expression language.

**A. Literal Syntax:**

* **String:** Single or double quotes (e.g., `'constant'`, `"constant"`).
* **Number:** Any real number (e.g., `1005`, `1.5589`).
* **Boolean:** `true` or `false`.

**B. Property Syntax:**

* **String:** `string(propertyName)`
* **Number:** `propertyName`
* **Boolean:** `bool(propertyName)`

**Case Sensitivity:** Case-sensitive except for strings. Spaces, tabs, and newlines are ignored.

**C. Operators:**

| Operator | Description                               | Examples                     |
|----------|-------------------------------------------|------------------------------|
| `+`      | Add numbers or strings                   | `property1 + 100`            |
| `-`      | Subtract numbers                          | `property1 + 100 - property2` |
| `*`      | Multiply numbers                         | `10 * property1`             |
| `/`      | Divide numbers                           | `property1 / property2`       |
| `<`      | Less than                               | `a < 100`                    |
| `>`      | Greater than                             | `a > 50`                     |
| `<=`     | Less than or equal to                     | `a <= b`                     |
| `>=`     | Greater than or equal to                 | `b >= c`                     |
| `=`      | Equal to                                 | `a = b`                      |
| `equals` | Equal to                                 | `a equals b`                 |
| `!=`     | Not equal to                             | `a != b`                     |
| `or`     | Logical OR                               | `a > b or b <= c`            |
| `and`    | Logical AND                              | `a and b`                    |
| `not`    | Logical NOT                              | `not a`                      |


**D. Functions:**

| Function     | Description                                                                     | Examples                  |
|--------------|---------------------------------------------------------------------------------|---------------------------|
| `max`        | Returns the maximum of 2-100 numbers                                          | `max(a, b, c, 100)`       |
| `min`        | Returns the minimum of 2-100 numbers                                          | `min(a, b, c, 100)`       |
| `is_present` | Checks if a property has a value (true for non-empty boolean properties)      | `is_present(bool(a))`     |
| `contains`   | Checks if a string contains another string                                      | `contains('hello', 'ello')` |
| `concatenate`| Joins strings                                                                 | `concatenate('a', 'b')`   |
| `number_to_string` | Converts a number to a string                                             | `number_to_string(a)`     |
| `string_to_number` | Converts a string to a number                                             | `string_to_number(a)`     |


**E. Conditional Statements:**

`if boolean_expression then statement [elseif expression then statement]* [else statement] endif`

**Example Formulas:**

* Simple: `"calculationFormula": "closed - started"`
* Advanced (with conditionals): `"calculationFormula": "if is_present(hs_latest_sequence_enrolled_date) then if is_present(hs_sequences_actively_enrolled_count) and hs_sequences_actively_enrolled_count >= 1 then true else false else ''"`


## VIII. Retrieving Properties

* **Individual Property:** `GET` `/crm/v3/properties/{object}/{propertyName}`
* **All Properties:** `GET` `/crm/v3/properties/{objectType}` (non-sensitive properties by default. Use `dataSensitivity=sensitive` for sensitive data - Enterprise only).


## IX. Updating/Clearing Property Values

Use a `PATCH` request to `/crm/v3/objects/{objectType}/{recordId}`.  Include properties and values in the request body.  See HubSpot's object API documentation for details.

## X.  Date/DateTime Property Values

* **ISO 8601:** YYYY-MM-DD (date only) or YYYY-MM-DDThh:mm:ss.sTZD (date and time, UTC).
* **UNIX Timestamp (milliseconds):**  UTC time. For `date` type, use EPOCH milliseconds (midnight UTC).


## XI. Checkbox Property Values

* **Boolean Checkbox:** `true` (Yes/checked), `false` (No/unchecked).
* **Multiple Checkbox:**  Use semicolons to separate values (e.g., `;value1;value2`).  A leading semicolon appends values instead of overwriting.


## XII. Assigning Record Owners

Use a `PATCH` request to update the `hubspot_owner_id` property with the user's ID.  Obtain the user ID from the HubSpot UI or the Owners API.

## XIII. Clearing Property Values

Set the property value to an empty string (`""`).


This documentation provides a comprehensive overview of the HubSpot CRM API's property management capabilities.  Refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications.
