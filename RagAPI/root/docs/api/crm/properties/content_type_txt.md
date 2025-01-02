# HubSpot CRM API: Properties

This document details the HubSpot CRM API for managing properties. Properties are used to store information on CRM records (Contacts, Companies, Deals, etc.). HubSpot provides default properties, and you can create custom properties via the API or the HubSpot UI.

## API Endpoints

The primary endpoint for interacting with properties is:

`/crm/v3/properties/{objectType}`

Where `{objectType}` represents the CRM object type (e.g., `contacts`, `companies`, `deals`).  Specific property access uses: `/crm/v3/properties/{objectType}/{propertyName}`

### HTTP Methods

* **GET:** Retrieve properties.
* **POST:** Create properties.
* **PATCH:** Update property values for a record.


## Property Types and `fieldType` Values

When creating a property, you must specify both `type` and `fieldType`.

| `type`       | Description                                                              | Valid `fieldType` Values                     |
|--------------|--------------------------------------------------------------------------|---------------------------------------------|
| `bool`       | Binary options (true/false)                                               | `booleancheckbox`, `calculation_equation` |
| `enumeration` | String representing a set of options (options separated by semicolons)     | `booleancheckbox`, `checkbox`, `radio`, `select`, `calculation_equation` |
| `date`       | Specific day, month, year (UTC, ISO 8601 or EPOCH milliseconds)           | `date`                                      |
| `dateTime`   | Specific date and time (UTC, ISO 8601 or UNIX milliseconds)               | `date`                                      |
| `string`     | Plain text string (up to 65,536 characters)                              | `file`, `text`, `textarea`, `calculation_equation`, `html`, `phonenumber` |
| `number`     | Numeric value                                                            | `number`, `calculation_equation`           |
| `object_coordinates` | Internal use only, cannot be created or edited.                       | `text`                                      |
| `json`       | Text value stored as formatted JSON, internal use only.                   | `text`                                      |


`fieldType` determines how the property appears in HubSpot:

| `fieldType`           | Description                                                                                                  |
|------------------------|--------------------------------------------------------------------------------------------------------------|
| `booleancheckbox`      | Single checkbox (Yes/No).                                                                                     |
| `calculation_equation` | Calculated value based on a formula.                                                                         |
| `checkbox`             | Multiple checkboxes.                                                                                         |
| `date`                 | Date picker.                                                                                                |
| `file`                 | File upload (stores file ID).                                                                               |
| `html`                 | Rich text editor.                                                                                           |
| `number`               | Numeric input.                                                                                             |
| `phonenumber`          | Formatted phone number input.                                                                                 |
| `radio`                | Radio buttons (select one option).                                                                            |
| `select`               | Dropdown menu.                                                                                             |
| `text`                 | Single-line text input.                                                                                     |
| `textarea`             | Multi-line text input.                                                                                      |


## Create a Property (POST)

To create a property, send a `POST` request to `/crm/v3/properties/{objectType}`.  The request body requires:

* `groupName`: Property group name.
* `name`: Internal property name (e.g., `favorite_food`).
* `label`: Display name in HubSpot (e.g., `Favorite Food`).
* `type`: Property type (see table above).
* `fieldType`: Field type (see table above).

**Example (JSON):**

```json
{
  "groupName": "contactinformation",
  "name": "favorite_food",
  "label": "Favorite Food",
  "type": "string",
  "fieldType": "text"
}
```

## Create Unique Identifier Properties

To create a property that requires unique values, set `hasUniqueValue` to `true` in the POST request.  You can have up to 10 unique ID properties per object.

**Example (JSON):**

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

## Calculation Properties

Calculation properties derive their value from a formula using other properties. Use `calculation_equation` for `fieldType` and specify the formula in `calculationFormula`.  Calculation properties created via API cannot be edited in the HubSpot UI.

**Formula Syntax:**  The formula language supports arithmetic, comparison, logic operators, conditional statements (`if`, `elseif`, `else`, `endif`), and functions (e.g., `max`, `min`, `is_present`, `contains`, `concatenate`, `number_to_string`, `string_to_number`).  See the original documentation for detailed syntax rules and function descriptions.


**Example (JSON):**

```json
{
  "groupName": "calculations",
  "name": "calculated_value",
  "label": "Calculated Value",
  "type": "number",
  "fieldType": "calculation_equation",
  "calculationFormula": "property1 + property2 * 10"
}
```

## Retrieve Properties (GET)

* **Individual Property:**  `GET /crm/v3/properties/{objectType}/{propertyName}`
* **All Properties:** `GET /crm/v3/properties/{objectType}` (use `dataSensitivity=sensitive` to retrieve sensitive properties - Enterprise only).


## Update Property Values (PATCH)

Send a `PATCH` request to `/crm/v3/objects/{objectType}/{recordId}`. Include the properties and their new values in the request body.  Refer to the original documentation for details on formatting values for different property types (dates, checkboxes, etc.).


**Example (JSON - Updating a text property):**

```json
{
  "properties": {
    "favorite_food": "Pizza"
  }
}
```

**Example (JSON - Updating a multiple-checkbox property):**

```json
{
  "properties": {
    "hs_buying_role": ";BUDGET_HOLDER;END_USER" //semicolon to append
  }
}
```

## Clearing Property Values

Set the property value to an empty string (`""`) in the `PATCH` request body to clear it.


This markdown documentation summarizes the key aspects of the HubSpot CRM Properties API. Refer to the original documentation for complete details and advanced features.
