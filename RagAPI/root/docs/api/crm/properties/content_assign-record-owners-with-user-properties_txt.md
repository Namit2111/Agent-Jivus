# HubSpot CRM API: Properties

This document details the HubSpot CRM API's functionality for managing properties. Properties store information on CRM records.  HubSpot provides default properties, and you can create custom ones via the API or the HubSpot UI.

## I.  Default Properties

Each CRM object (Contacts, Companies, Deals, Tickets, Activities, Leads) has a set of default properties.  These are name-value pairs defining the object's structure.  Refer to the HubSpot documentation for a complete list of default properties per object type.

## II. Property Groups

Property groups organize related properties for better visibility in the HubSpot UI.  Custom properties should be grouped for easier identification.

## III. Property Types and Field Types

When creating properties, you must specify `type` and `fieldType`.

| `type`        | Description                                         | Valid `fieldType` Values                               |
|----------------|-----------------------------------------------------|--------------------------------------------------------|
| `bool`        | Binary option (True/False, Yes/No)                  | `booleancheckbox`, `calculation_equation`              |
| `enumeration` | String representing a set of options (semicolon-separated) | `booleancheckbox`, `checkbox`, `radio`, `select`, `calculation_equation` |
| `date`        | Specific day, month, year (UTC, ISO 8601 or EPOCH milliseconds) | `date`                                               |
| `dateTime`    | Specific date and time (UTC, ISO 8601 or UNIX milliseconds) | `date`                                               |
| `string`      | Plain text string (up to 65,536 characters)         | `file`, `text`, `textarea`, `calculation_equation`, `html`, `phonenumber` |
| `number`      | Numeric value                                      | `number`, `calculation_equation`                      |
| `object_coordinates` | Internal use only, not creatable or editable.     | `text`                                               |
| `json`        | JSON formatted text, internal use only.           | `text`                                               |


Valid `fieldType` values and their descriptions:

| `fieldType`           | Description                                                                        |
|------------------------|------------------------------------------------------------------------------------|
| `booleancheckbox`     | Single checkbox (Yes/No)                                                           |
| `calculation_equation` | Custom equation based on other properties                                          |
| `checkbox`            | Multiple checkboxes                                                              |
| `date`                | Date picker                                                                       |
| `file`                | File upload (stores file ID)                                                      |
| `html`                | Rich text editor                                                                  |
| `number`              | Numeric input                                                                     |
| `phonenumber`         | Formatted phone number input                                                        |
| `radio`               | Set of radio buttons                                                             |
| `select`              | Dropdown menu                                                                     |
| `text`                | Single-line text input                                                            |
| `textarea`            | Multi-line text input                                                            |


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

**Response:** A JSON representation of the newly created property.  This property will enforce uniqueness of values.


### C. Create Calculation Properties

**Endpoint:** `/crm/v3/properties/{objectType}`

**Method:** `POST`

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

**Response:** A JSON representation of the newly created calculation property.  **Note:** API-created calculation properties cannot be edited in the HubSpot UI.


#### Calculation Property Syntax

* **Literal Syntax:**  Numbers (e.g., `100`, `1.5`), strings (single or double quotes), booleans (`true`, `false`).
* **Property Syntax:**  `string(propertyName)` for string properties, `propertyName` for number properties, `bool(propertyName)` for boolean properties.  Case-sensitive except for strings.
* **Operators:**  `+`, `-`, `*`, `/`, `<`, `>`, `<=`, `>=`, `=`, `equals`, `!=`, `or`, `and`, `not`.
* **Functions:** `max()`, `min()`, `is_present()`, `contains()`, `concatenate()`, `number_to_string()`, `string_to_number()`.
* **Conditional Statements:** `if`, `elseif`, `else`, `endif`.


### D. Retrieve Properties

**Endpoint (Individual Property):** `/crm/v3/properties/{object}/{propertyName}`

**Method:** `GET`

**Endpoint (All Properties):** `/crm/v3/properties/{objectType}`

**Method:** `GET`

**Query Parameter (for sensitive data):** `dataSensitivity=sensitive` (BETA, Enterprise only)


### E. Update or Clear Property Values

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

To clear a property value, set it to an empty string (`""`).


### F.  Date and DateTime Properties

Use ISO 8601 format for responses.  For API requests, use either ISO 8601 or UNIX timestamps (milliseconds).  `date` properties store only the date; `dateTime` stores both date and time.


### G. Checkbox Properties

* **Boolean Checkbox:** Use `true` for checked, `false` for unchecked.
* **Multiple Select Checkbox:** Use semicolons to separate values (e.g., `;value1;value2`).  A leading semicolon appends to existing values.


### H. Assign Record Owners

Use the user's `id` (obtainable via the Owners API or property settings).


## V. Error Handling

The API will return appropriate HTTP status codes (e.g., 400 for bad requests, 404 for not found) and JSON error messages.


This markdown provides a comprehensive overview. Always refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications.
