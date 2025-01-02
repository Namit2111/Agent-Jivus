# HubSpot CRM API: Properties Documentation

This document details the HubSpot CRM API's functionalities for managing properties.  Properties are used to store information on CRM records (Contacts, Companies, Deals, etc.). HubSpot provides default properties, and you can create custom properties via the API or the HubSpot UI.

## I. Core Concepts

* **Properties:** Data fields associated with CRM objects.  Each property has a `name`, `label`, `type`, and `fieldType`.
* **Property Groups:**  Organize related properties for better UI presentation.
* **`type`:** Defines the data type of the property (e.g., `string`, `number`, `bool`, `date`, `dateTime`, `enumeration`).
* **`fieldType`:** Determines how the property appears in the HubSpot UI (e.g., `text`, `textarea`, `number`, `date`, `checkbox`, `select`, `radio`).
* **Unique Identifier Properties:** Properties enforcing unique values across records of a specific object type.  Up to 10 allowed per object.
* **Calculation Properties:** Properties whose values are calculated based on formulas involving other properties within the same record.  These cannot be edited in the HubSpot UI, only via the API.

## II. Property Types and `fieldType` Values

| `type`        | Description                                    | Valid `fieldType` Values                       |
|----------------|------------------------------------------------|-----------------------------------------------|
| `bool`         | Boolean value (true/false)                     | `booleancheckbox`, `calculation_equation`      |
| `enumeration` | String with predefined options (semicolon-separated) | `booleancheckbox`, `checkbox`, `radio`, `select`, `calculation_equation` |
| `date`         | Date (YYYY-MM-DD or EPOCH milliseconds, midnight UTC) | `date`                                        |
| `dateTime`     | Date and time (ISO 8601 or UNIX milliseconds UTC) | `date`                                        |
| `string`       | Plain text string (up to 65,536 characters)    | `file`, `text`, `textarea`, `calculation_equation`, `html`, `phonenumber` |
| `number`       | Numeric value                                   | `number`, `calculation_equation`              |
| `object_coordinates` | Internal use only, not creatable/editable.   | `text`                                        |
| `json`         | JSON formatted text, internal use only.         | `text`                                        |

**`fieldType` Descriptions:**

* `booleancheckbox`: Single checkbox (Yes/No).
* `calculation_equation`:  Custom formula-based property.
* `checkbox`: Multiple checkbox selections.
* `date`: Date picker.
* `file`: File upload (stores file ID).
* `html`: Rich text editor.
* `number`: Numeric input.
* `phonenumber`: Formatted phone number input.
* `radio`: Radio button selection.
* `select`: Dropdown selection.
* `text`: Single-line text input.
* `textarea`: Multi-line text input.


## III. API Endpoints

**A. Create a Property:**

* **Method:** `POST`
* **Endpoint:** `/crm/v3/properties/{objectType}`
* **Request Body (JSON):**

```json
{
  "groupName": "propertyGroupName",
  "name": "propertyName",  // e.g., "favorite_food"
  "label": "Property Label", // e.g., "Favorite Food"
  "type": "string",
  "fieldType": "text",
  "hasUniqueValue": false //Optional, set to true for unique identifier properties
}
```

**B. Create a Unique Identifier Property:**

Same endpoint as above, but set `hasUniqueValue: true` in the request body.

**C. Create a Calculation Property:**

Same endpoint as above, using `fieldType: calculation_equation` and specifying the `calculationFormula`.

**D. Retrieve Properties:**

* **Method:** `GET`
* **Endpoint (Individual):** `/crm/v3/properties/{objectType}/{propertyName}`
* **Endpoint (All):** `/crm/v3/properties/{objectType}`  (Add `dataSensitivity=sensitive` for sensitive properties).

**E. Update/Clear Property Values:**

* **Method:** `PATCH`
* **Endpoint:** `/crm/v3/objects/{objectType}/{recordId}`
* **Request Body (JSON):**

```json
{
  "properties": {
    "propertyName": "newValue" // or "" to clear
  }
}
```

**Example for multiple checkbox:**

```json
{
  "properties": {
    "hs_buying_role": ";BUDGET_HOLDER;END_USER" // append values, existing values will be preserved
  }
}
```

**F. Assign Record Owners:**

* **Method:** `PATCH`
* **Endpoint:** `/crm/v3/objects/{objectType}/{recordId}`
* **Request Body (JSON):**

```json
{
  "properties": {
    "hubspot_owner_id": "userId" // user's ID
  }
}
```


## IV. Calculation Property Syntax

### A. Literals:

* **String:** Single ('constant') or double ("constant") quotes.
* **Number:** Any real number (e.g., 1005, 1.5589).
* **Boolean:** `true` or `false`.

### B. Property Variables:

* **String:** `string(propertyName)`
* **Number:** `propertyName`
* **Boolean:** `bool(propertyName)`

Case-sensitive except for strings.

### C. Operators:

| Operator | Description      | Example             |
|----------|-------------------|----------------------|
| `+`      | Add               | `property1 + 100`    |
| `-`      | Subtract          | `property1 - 100`    |
| `*`      | Multiply          | `10 * property1`    |
| `/`      | Divide            | `property1 / 100`    |
| `<`      | Less than         | `a < 100`           |
| `>`      | Greater than      | `a > 50`            |
| `<=`     | Less than or equal | `a <= b`            |
| `>=`     | Greater than or equal | `b >= c`            |
| `=`      | Equal             | `a = b`             |
| `equals` | Equal             | `a equals b`        |
| `!=`     | Not equal         | `a != b`            |
| `or`     | Logical OR        | `a > b or b <= c`   |
| `and`    | Logical AND       | `a and b`           |
| `not`    | Logical NOT       | `not a`             |

### D. Functions:

* `max(a, b, c, ...)`: Returns the maximum value.
* `min(a, b, c, ...)`: Returns the minimum value.
* `is_present(expression)`: Checks if an expression can be evaluated (true if not empty/null).
* `contains(string1, string2)`: Checks if string1 contains string2.
* `concatenate(string1, string2, ...)`: Concatenates strings.
* `number_to_string(number)`: Converts a number to a string.
* `string_to_number(string)`: Converts a string to a number.

### E. Conditional Statements:

```
if boolean_expression then statement [elseif expression then statement]* [else statement] endif
```


## V. Date and DateTime Properties

* **ISO 8601:**  YYYY-MM-DD (date) or YYYY-MM-DDThh:mm:ss.sTZD (dateTime).  UTC time.
* **UNIX Timestamp (milliseconds):**  Milliseconds since epoch (UTC).  For `date` type, use EPOCH millisecond timestamp representing midnight UTC.


This comprehensive documentation provides a detailed overview of HubSpot's CRM API for managing properties.  Remember to consult the official HubSpot API documentation for the most up-to-date information and error handling details.
