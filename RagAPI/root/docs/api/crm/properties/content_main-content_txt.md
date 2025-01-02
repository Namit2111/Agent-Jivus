# HubSpot CRM API: Properties Documentation

This document details the HubSpot CRM API's functionality for managing properties. Properties are used to store information on CRM records (Contacts, Companies, Deals, etc.).  HubSpot provides default properties, and you can create custom properties using the API or the HubSpot UI.

## I. Property Types and Field Types

When creating or updating properties, both `type` and `fieldType` are required.

| `type`        | Description                                                                  | Valid `fieldType` Values                                      |
|---------------|------------------------------------------------------------------------------|-------------------------------------------------------------|
| `bool`        | Binary options (e.g., Yes/No, True/False)                                  | `booleancheckbox`, `calculation_equation`                   |
| `enumeration` | String representing a set of options (options separated by semicolons)       | `booleancheckbox`, `checkbox`, `radio`, `select`, `calculation_equation` |
| `date`        | Specific day, month, and year (UTC, ISO 8601 or EPOCH milliseconds)       | `date`                                                      |
| `dateTime`    | Specific day, month, year, and time (UTC, ISO 8601 or UNIX milliseconds) | `date`                                                      |
| `string`      | Plain text string (up to 65,536 characters)                               | `file`, `text`, `textarea`, `calculation_equation`, `html`, `phonenumber` |
| `number`      | Numeric value                                                              | `number`, `calculation_equation`                           |
| `object_coordinates` | Internal use only, cannot be created or edited.                         | `text`                                                      |
| `json`        | Text value stored as formatted JSON, internal use only.                   | `text`                                                      |


**`fieldType` Descriptions:**

| `fieldType`           | Description                                                                                                 |
|------------------------|-------------------------------------------------------------------------------------------------------------|
| `booleancheckbox`      | Single checkbox (Yes/No)                                                                                   |
| `calculation_equation` | Custom equation based on other property values.                                                            |
| `checkbox`             | Multiple checkboxes                                                                                         |
| `date`                 | Date picker                                                                                                 |
| `file`                 | File upload (stores file ID)                                                                               |
| `html`                 | Rich text editor (sanitized HTML)                                                                          |
| `number`               | Numeric input                                                                                               |
| `phonenumber`          | Formatted phone number input                                                                               |
| `radio`                | Set of radio buttons                                                                                      |
| `select`               | Dropdown menu                                                                                             |
| `text`                 | Single-line text input                                                                                    |
| `textarea`             | Multi-line text input                                                                                    |


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

**B. Create Unique Identifier Properties:**

* **Method:** `POST`
* **Endpoint:** `/crm/v3/properties/{objectType}`
* **Request Body (JSON):**  Set `hasUniqueValue` to `true`.

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

**C. Retrieve Properties:**

* **Individual Property:**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v3/properties/{object}/{propertyName}`
    * **Example:** `https://api.hubapi.com/crm/v3/properties/contacts/favorite_food`
* **All Properties:**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v3/properties/{objectType}`
    * **Query Parameter:** `dataSensitivity=sensitive` (for sensitive properties, Enterprise only)

**D. Update/Clear Property Values:**

* **Method:** `PATCH`
* **Endpoint:** `/crm/v3/objects/{objectType}/{recordId}`
* **Request Body (JSON):**  Include properties and values in an array.  To clear a value, set it to an empty string (`""`).

```json
{
  "properties": {
    "firstname": "Updated Name",
    "lastname": "" // Clears lastname
  }
}
```

**E. Add Values to Date/DateTime Properties:**

* Use ISO 8601 strings (YYYY-MM-DD or YYYY-MM-DDThh:mm:ss.sTZD) or UNIX timestamps in milliseconds (UTC).
* `date` properties: Use ISO 8601 complete date format or EPOCH millisecond timestamp (midnight UTC).
* `dateTime` properties:  Accept either format.

**F. Add Values to Checkbox Properties:**

* **Boolean Checkbox:** `true` (checked), `false` (unchecked)
* **Multiple Select Checkbox:** Use semicolons to separate values.  A leading semicolon appends values.

```json
{
  "properties": {
    "hs_buying_role": ";BUDGET_HOLDER;END_USER" // Appends values
  }
}
```

**G. Assign Record Owners:**

* Use the user's `id` (obtained from property settings or the Owners API).
* **Method:** `PATCH`
* **Endpoint:** `/crm/v3/objects/{objectType}/{recordId}`
* **Request Body (JSON):**

```json
{
  "properties": {
    "hubspot_owner_id": "41629779"
  }
}
```


## III. Calculation Properties

Calculation properties derive their value from a formula.

**A. Calculation Formula Syntax:**

* **Literal Syntax:**  Strings (single or double quotes), numbers, booleans (`true`, `false`).
* **Property Syntax:**  String properties must be wrapped in `string()`, number properties are used directly, boolean properties are wrapped in `bool()`. Case-sensitive except for strings.
* **Operators:**  `+`, `-`, `*`, `/`, `<`, `>`, `<=`, `>=`, `=`, `equals`, `!=`, `or`, `and`, `not`.
* **Functions:** `max()`, `min()`, `is_present()`, `contains()`, `concatenate()`, `number_to_string()`, `string_to_number()`.
* **Conditional Statements:** `if`, `elseif`, `else`, `endif`.


**B. Example Formulas:**

```javascript
// Simple subtraction
"calculationFormula": "closed - started"

// Conditional example
"calculationFormula": "if is_present(hs_latest_sequence_enrolled_date) then if is_present(hs_sequences_actively_enrolled_count) and hs_sequences_actively_enrolled_count >= 1 then true else false else ''"
```

## IV. Error Handling and Responses

The API will return standard HTTP status codes (e.g., 200 for success, 400 for bad request, etc.) and JSON responses containing details about errors or successes.  Refer to HubSpot's API documentation for specific error codes and responses.


This documentation provides a comprehensive overview of the HubSpot CRM API's property management features. Remember to consult the official HubSpot API documentation for the most up-to-date information and detailed specifications.
