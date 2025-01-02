# HubSpot CRM API: Properties Documentation

This document details the HubSpot CRM API's functionality for managing properties.  Properties are used to store information on CRM records (Contacts, Companies, Deals, etc.).  HubSpot provides default properties, and you can create custom properties via the API or the HubSpot UI.

## I. Default Properties

CRM objects have a primary `type` and a set of `properties`. Each type has standard properties (name-value pairs).  See the HubSpot documentation for default properties of specific objects (Contacts, Companies, Deals, Tickets, Activities, Leads).

## II. Property Groups

Property groups organize related properties, improving UI presentation in HubSpot.  Custom object properties should be grouped for clarity.

## III. Property Types and Field Types

When creating or updating properties, `type` and `fieldType` are required:

* **`type`**:  Defines the data type (e.g., `string`, `number`, `bool`, `date`, `dateTime`, `enumeration`, `object_coordinates`, `json`).

* **`fieldType`**: Determines the UI element (e.g., `text`, `textarea`, `number`, `date`, `select`, `checkbox`, `radio`, `booleancheckbox`, `file`, `html`, `phonenumber`, `calculation_equation`).

| `type`          | Description                                      | Valid `fieldType` Values                     |
|-----------------|--------------------------------------------------|----------------------------------------------|
| `bool`          | Boolean (true/false)                             | `booleancheckbox`, `calculation_equation`   |
| `enumeration`   | String with semicolon-separated options           | `booleancheckbox`, `checkbox`, `radio`, `select`, `calculation_equation` |
| `date`          | Date (YYYY-MM-DD or EPOCH milliseconds, UTC)      | `date`                                      |
| `dateTime`      | Date and time (ISO 8601 or UNIX milliseconds, UTC) | `date`                                      |
| `string`        | Plain text string (max 65,536 characters)        | `file`, `text`, `textarea`, `calculation_equation`, `html`, `phonenumber` |
| `number`        | Numeric value                                     | `number`, `calculation_equation`           |
| `object_coordinates` | Internal use only, not editable.                  | `text`                                      |
| `json`          | JSON formatted text, internal use only, not editable.| `text`                                      |


`fieldType` descriptions:

| `fieldType`          | Description                                                                     |
|----------------------|---------------------------------------------------------------------------------|
| `booleancheckbox`    | Single checkbox (Yes/No).                                                      |
| `calculation_equation` | Computed value based on a formula.                                             |
| `checkbox`           | Multiple checkboxes.                                                            |
| `date`               | Date picker.                                                                   |
| `file`               | File upload (stores file ID).                                                   |
| `html`               | Rich text editor (sanitized HTML).                                              |
| `number`             | Numeric input.                                                                  |
| `phonenumber`        | Formatted phone number input.                                                   |
| `radio`              | Radio buttons.                                                                 |
| `select`             | Dropdown menu.                                                                  |
| `text`               | Single-line text input.                                                         |
| `textarea`           | Multi-line text input.                                                          |


## IV. API Endpoints

**A. Create a Property:**

* **Method:** `POST`
* **Endpoint:** `/crm/v3/properties/{objectType}`
* **Request Body (JSON):**

```json
{
  "groupName": "propertyGroupName",
  "name": "propertyName", // Internal name (e.g., "favorite_food")
  "label": "Property Label", // Display name (e.g., "Favorite Food")
  "type": "string",
  "fieldType": "text",
  "hasUniqueValue": false // Optional: true for unique identifier properties (max 10 per object)
  "calculationFormula": "...your formula..." // only applicable for Calculation properties
}
```


**B. Create Unique Identifier Properties:**

Set `hasUniqueValue: true` in the request body above.  This ensures that no two records have the same value for this property.  Useful for external IDs.

**C. Create Calculation Properties:**

Use `fieldType: calculation_equation` and specify the `calculationFormula`.  These cannot be edited in the HubSpot UI, only via the API.

**Calculation Property Syntax:**

* **Literals:**  `'string'`, `"string"`, `123`, `123.45`, `true`, `false`
* **Property Variables:** `string(propertyName)`, `propertyName` (for numbers), `bool(propertyName)`
* **Operators:** `+`, `-`, `*`, `/`, `<`, `>`, `<=`, `>=`, `=`, `equals`, `!=`, `or`, `and`, `not`
* **Functions:** `max()`, `min()`, `is_present()`, `contains()`, `concatenate()`, `number_to_string()`, `string_to_number()`
* **Conditional Statements:** `if`, `elseif`, `else`, `endif`


**Example Calculation Formulas:**

```
"calculationFormula": "closed - started" // Simple subtraction
"calculationFormula": "if is_present(hs_latest_sequence_enrolled_date) then if is_present(hs_sequences_actively_enrolled_count) and hs_sequences_actively_enrolled_count >= 1 then true else false else ''" // Conditional example
```

**D. Retrieve Properties:**

* **Individual Property:**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v3/properties/{objectType}/{propertyName}`
* **All Properties:**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v3/properties/{objectType}`
    * **Query Parameter:** `dataSensitivity=sensitive` (to retrieve sensitive properties - Enterprise only)


**E. Update/Clear Property Values:**

* **Method:** `PATCH`
* **Endpoint:** `/crm/v3/objects/{objectType}/{recordId}`
* **Request Body (JSON):**

```json
{
  "properties": {
    "propertyName": "newValue"  //or "" to clear the value
  }
}
```

**F.  Date/DateTime Properties:**

Use ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDThh:mm:ss.sTZD) or UNIX timestamps in milliseconds (UTC).  `date` properties only store the date; `dateTime` stores both date and time.

**G. Checkbox Properties:**

* **Boolean Checkbox:** `true` (checked), `false` (unchecked)
* **Multiple Select Checkbox:**  Append values with semicolons: `;value1;value2;value3`

**H. Assign Record Owners:**

Use the user's `id` (obtainable via the Owners API or property settings).

```json
{ "properties": { "hubspot_owner_id": "userId" } }
```


## V. Error Handling

The API will return appropriate HTTP status codes and error messages in the response body (JSON) to indicate success or failure.  Refer to HubSpot's API documentation for detailed error codes and their meanings.


## VI.  Rate Limits

Be mindful of HubSpot's API rate limits to avoid throttling.  Implement appropriate retry logic if necessary.


This documentation provides a comprehensive overview. Always refer to the official HubSpot API documentation for the most up-to-date information and details.
