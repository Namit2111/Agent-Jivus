# HubSpot CRM API: Properties Documentation

This document details the HubSpot CRM API's functionality for managing properties.  Properties are used to store information on CRM records (Contacts, Companies, Deals, etc.).  HubSpot provides default properties, and you can create custom ones via the API or the HubSpot UI.

## I.  Default Properties

Each CRM object type (Contacts, Companies, Deals, etc.) has a predefined set of default properties.  These are name-value pairs and cannot be deleted.  Refer to the HubSpot documentation for a complete list of default properties for each object type.

## II. Property Groups

Property groups organize related properties, improving UI readability.  Custom object properties are typically grouped for better identification.


## III. Property Types and `fieldType` Values

When creating or updating properties, you must specify both `type` and `fieldType`.  `type` defines the data type (string, number, boolean, etc.), while `fieldType` determines the UI element (text input, dropdown, checkbox, etc.).

| `type`        | Description                                      | Valid `fieldType` Values             |
|----------------|--------------------------------------------------|--------------------------------------|
| `bool`         | Boolean value (true/false)                       | `booleancheckbox`, `calculation_equation` |
| `enumeration` | String with options separated by semicolons        | `booleancheckbox`, `checkbox`, `radio`, `select`, `calculation_equation` |
| `date`         | Date (YYYY-MM-DD)                               | `date`                               |
| `dateTime`     | Date and time (YYYY-MM-DDThh:mm:ss.sTZD)          | `date`                               |
| `string`       | Plain text string (up to 65,536 characters)     | `file`, `text`, `textarea`, `calculation_equation`, `html`, `phonenumber` |
| `number`       | Numeric value                                     | `number`, `calculation_equation`     |
| `object_coordinates` | Internal use only, cannot be created/edited       | `text`                               |
| `json`         | JSON formatted text, internal use only           | `text`                               |


| `fieldType`       | Description                                                                    |
|--------------------|--------------------------------------------------------------------------------|
| `booleancheckbox` | Single checkbox (true/false)                                                  |
| `calculation_equation` | Calculated value based on a formula.                                        |
| `checkbox`        | Multiple checkboxes                                                            |
| `date`            | Date picker                                                                    |
| `file`            | File upload (stores file ID)                                                  |
| `html`            | Rich text editor (sanitized HTML)                                              |
| `number`          | Numeric input                                                                  |
| `phonenumber`     | Phone number input                                                             |
| `radio`           | Radio buttons (single selection)                                               |
| `select`          | Dropdown menu                                                                  |
| `text`            | Single-line text input                                                        |
| `textarea`        | Multi-line text input                                                         |


## IV. API Endpoints

### A. Create a Property

**Method:** `POST`

**Endpoint:** `/crm/v3/properties/{objectType}`

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

* **`groupName`:** Property group name.
* **`name`:** Internal property name (e.g., `favorite_food`).
* **`label`:** Display name in HubSpot (e.g., `Favorite Food`).
* **`type`:** Property type (see table above).
* **`fieldType`:** Field type (see table above).
* **`hasUniqueValue` (Optional):** Set to `true` to enforce unique values (up to 10 unique ID properties per object).


### B. Retrieve Properties

**Method:** `GET`

**Endpoint (Individual Property):** `/crm/v3/properties/{object}/{propertyName}`
Example: `https://api.hubapi.com/crm/v3/properties/contacts/favorite_food`

**Endpoint (All Properties):** `/crm/v3/properties/{objectType}`

**Query Parameter (for all properties):**
* `dataSensitivity=sensitive` (Retrieve sensitive properties – BETA, Enterprise only)

### C. Update or Clear Property Values

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/{objectType}/{recordId}`

**Request Body (JSON):**

```json
{
  "properties": {
    "propertyName": "newValue"
  }
}
```

To clear a value, set `newValue` to an empty string (`""`).


### D.  Specific Value Handling

* **Date and `dateTime`:** Use ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDThh:mm:ss.sTZD) or UNIX timestamps (milliseconds since epoch).  `date` properties only store the date; `dateTime` stores date and time.
* **Checkbox (`fieldType`):**
    * **Boolean Checkbox:** `true` for checked, `false` for unchecked.
    * **Multiple Checkboxes:** Use semicolons to separate values (e.g., `;value1;value2`).  A leading semicolon appends to existing values.
* **Record Owners:** Use the user's `id` (obtainable via the Owners API or property settings).


## V. Calculation Properties

Calculation properties dynamically calculate values based on other properties within the same record using formulas.

**Method:** `POST`  (to create)

**Endpoint:** `/crm/v3/properties/{objectType}`

**Request Body (JSON):**  Includes `calculationFormula` field

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

**Formula Syntax:**

* **Literals:**  Numbers (10, 1.5), strings ('text', "text"), booleans (true, false).
* **Property Variables:**  `string(propertyName)` for strings, `propertyName` for numbers, `bool(propertyName)` for booleans (case-sensitive except strings).
* **Operators:** `+`, `-`, `*`, `/`, `<`, `>`, `<=`, `>=`, `=`, `equals`, `!=`, `or`, `and`, `not`.
* **Functions:** `max`, `min`, `is_present`, `contains`, `concatenate`, `number_to_string`, `string_to_number`.
* **Conditional Statements:** `if`, `elseif`, `else`, `endif`.


**Example Formulas:**

```
"calculationFormula": "closed - started" // Simple subtraction

"calculationFormula": "if is_present(propertyA) then propertyB else 0 endif" // Conditional
```

**Important Note:** Calculation properties created via the API cannot be edited in the HubSpot UI.  Only the API can modify them.


## VI. Error Handling

The API returns standard HTTP status codes and error responses.  Refer to the HubSpot API documentation for details on error handling and response codes.


This documentation provides a concise overview. For detailed information and the most up-to-date specifications, always consult the official HubSpot API documentation.
