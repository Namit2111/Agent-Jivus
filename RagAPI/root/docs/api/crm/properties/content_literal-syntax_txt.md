# HubSpot CRM API: Properties

This document details the HubSpot CRM API's functionality for managing properties. Properties are used to store information on CRM records.  HubSpot provides default properties, and you can create custom properties via the API or the HubSpot UI.

## I. Default Properties

Each CRM object (Contacts, Companies, Deals, Tickets, Activities, Leads) has a predefined set of default properties.  These are represented as name-value pairs.  Refer to the HubSpot documentation for details on default properties for each object type.

## II. Property Groups

Property groups organize related properties, improving UI presentation.  Custom object properties should be grouped for clarity.

## III. Property Types and `fieldType` Values

When creating or updating properties, both `type` and `fieldType` are required.  `type` defines the data type (e.g., string, number, boolean), while `fieldType` determines the UI element (e.g., text field, dropdown, checkbox).

| `type`       | Description                                                              | Valid `fieldType` Values                  |
|--------------|--------------------------------------------------------------------------|------------------------------------------|
| `bool`       | Binary options (True/False, Yes/No)                                      | `booleancheckbox`, `calculation_equation` |
| `enumeration` | String representing a set of options (semicolon-separated)                | `booleancheckbox`, `checkbox`, `radio`, `select`, `calculation_equation` |
| `date`       | Specific day, month, year (UTC, ISO 8601 or EPOCH milliseconds)         | `date`                                   |
| `dateTime`   | Specific date and time (UTC, ISO 8601 or UNIX milliseconds)              | `date`                                   |
| `string`     | Plain text string (up to 65,536 characters)                             | `file`, `text`, `textarea`, `calculation_equation`, `html`, `phonenumber` |
| `number`     | Numeric value                                                             | `number`, `calculation_equation`          |
| `object_coordinates` | Internal use only, cannot be created or edited.                        | `text`                                   |
| `json`       | JSON formatted text, internal use only, cannot be created or edited.      | `text`                                   |


**`fieldType` Descriptions:**

| `fieldType`          | Description                                                                   |
|----------------------|-------------------------------------------------------------------------------|
| `booleancheckbox`    | Single checkbox (Yes/No)                                                      |
| `calculation_equation` | Custom calculation based on other properties.                               |
| `checkbox`           | Multiple checkboxes.                                                          |
| `date`               | Date picker.                                                                  |
| `file`               | File upload (stores file ID).                                                  |
| `html`               | Rich text editor.                                                             |
| `number`             | Numeric input.                                                                |
| `phonenumber`        | Formatted phone number input.                                                  |
| `radio`              | Set of radio buttons.                                                        |
| `select`             | Dropdown menu.                                                              |
| `text`               | Single-line text input.                                                      |
| `textarea`           | Multi-line text input.                                                       |


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

**Response:** A JSON representation of the newly created property.


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

**Response:** A JSON representation of the newly created property.  Note that these cannot be edited in the HubSpot UI, only via the API.


### D. Retrieve Properties

**Individual Property:**

**Endpoint:** `/crm/v3/properties/{object}/{propertyName}`

**Method:** `GET`

**Example:** `https://api.hubapi.com/crm/v3/properties/contacts/favorite_food`

**All Properties:**

**Endpoint:** `/crm/v3/properties/{objectType}`

**Method:** `GET`

**Query Parameter:** `dataSensitivity=sensitive` (for sensitive data, Enterprise only)

### E. Update or Clear Property Values

**Endpoint:** `/crm/v3/objects/{objectType}/{recordId}`

**Method:** `PATCH`

**Request Body (JSON - example for updating):**

```json
{
  "properties": {
    "favorite_food": "Pizza"
  }
}
```

**Request Body (JSON - example for clearing):**

```json
{
  "properties": {
    "favorite_food": ""
  }
}
```

### F. Add Values to Date/DateTime Properties

Use ISO 8601 strings (YYYY-MM-DD or YYYY-MM-DDThh:mm:ss.sTZD) or UNIX timestamps in milliseconds (UTC).  `date` properties only store the date; `dateTime` properties store both date and time.

### G. Add Values to Checkbox Properties

* **Boolean Checkbox:** `true` (checked), `false` (unchecked)
* **Multiple Select Checkbox:** Use semicolons to separate values.  A leading semicolon appends values to existing ones.  Example:  `;BUDGET_HOLDER;END_USER`

### H. Assign Record Owners

Use the user's `id` (obtainable from property settings or the Owners API).

**Endpoint:** `/crm/v3/objects/{objectType}/{recordId}`

**Method:** `PATCH`

**Request Body (JSON):**

```json
{
  "properties": {
    "hubspot_owner_id": "41629779"
  }
}
```


## V. Calculation Property Syntax

Calculation properties use a custom formula language.

**Literal Syntax:**

* Strings:  `'constant'` or `"constant"`
* Numbers:  `1005`, `1.5589`
* Booleans: `true`, `false`

**Property Syntax:**

* String properties: `string(propertyName)`
* Number properties: `propertyName`
* Boolean properties: `bool(propertyName)`

**Operators:** `+`, `-`, `*`, `/`, `<`, `>`, `<=`, `>=`, `=`, `equals`, `!=`, `or`, `and`, `not`

**Functions:** `max`, `min`, `is_present`, `contains`, `concatenate`, `number_to_string`, `string_to_number`

**Conditional Statements:** `if`, `elseif`, `else`, `endif`


## VI. Error Handling

The API will return appropriate HTTP status codes and JSON error messages to indicate failures.  Refer to the HubSpot API documentation for detailed error codes and their meanings.


This markdown provides a comprehensive overview.  Always refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications.
