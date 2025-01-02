# HubSpot CRM API: Properties

This document details the HubSpot CRM API's functionality for managing properties. Properties are used to store information on CRM records (Contacts, Companies, Deals, etc.).  HubSpot provides default properties, but you can also create and manage custom properties using the API.

## I. API Endpoints

All endpoints are under the `/crm/v3/properties` base path.  Replace `{objectType}` with the object type (e.g., `contacts`, `companies`, `deals`).  Replace `{propertyName}` with the name of the property.  Replace `{recordId}` with the ID of the record.


| Method | Endpoint                     | Description                                                                     |
|--------|------------------------------|---------------------------------------------------------------------------------|
| `POST`  | `/crm/v3/properties/{objectType}` | Create a new property.                                                            |
| `GET`   | `/crm/v3/properties/{objectType}` | Retrieve all properties for an object type.                                      |
| `GET`   | `/crm/v3/properties/{objectType}/{propertyName}` | Retrieve a specific property.                                                     |
| `PATCH` | `/crm/v3/objects/{objectType}/{recordId}` | Update or clear a property's value for a specific record.                       |


## II. Property Types and `fieldType` Values

When creating a property, you must specify its `type` and `fieldType`.

| `type`           | Description                                         | Valid `fieldType` Values                  |
|-------------------|-----------------------------------------------------|-------------------------------------------|
| `bool`           | Boolean value (true/false)                          | `booleancheckbox`, `calculation_equation` |
| `enumeration`    | String representing a set of options (semicolon-separated) | `booleancheckbox`, `checkbox`, `radio`, `select`, `calculation_equation` |
| `date`           | Date (YYYY-MM-DD)                                   | `date`                                     |
| `dateTime`        | Date and time (YYYY-MM-DDThh:mm:ss.sTZD)             | `date`                                     |
| `string`         | Text string                                          | `file`, `text`, `textarea`, `calculation_equation`, `html`, `phonenumber` |
| `number`         | Numeric value                                         | `number`, `calculation_equation`          |
| `object_coordinates` | Internal use only.                                  | `text`                                     |
| `json`           | JSON formatted text. Internal use only.               | `text`                                     |


`fieldType` values determine how the property appears in HubSpot.

| `fieldType`       | Description                                                                      |
|--------------------|----------------------------------------------------------------------------------|
| `booleancheckbox` | Single checkbox (true/false)                                                    |
| `calculation_equation` | Calculated value based on a formula.                                            |
| `checkbox`        | Multiple checkboxes (semicolon-separated values)                               |
| `date`            | Date picker                                                                      |
| `file`            | File upload (stores file ID)                                                   |
| `html`            | Rich text editor (sanitized HTML)                                                |
| `number`          | Numeric input                                                                     |
| `phonenumber`     | Formatted phone number input                                                     |
| `radio`           | Radio buttons (single selection)                                                |
| `select`          | Dropdown menu                                                                     |
| `text`            | Single-line text input                                                           |
| `textarea`        | Multi-line text input                                                            |


## III. Creating a Property

Use a `POST` request to `/crm/v3/properties/{objectType}`.

**Request Body (JSON):**

```json
{
  "groupName": "propertyGroupName",
  "name": "propertyName",  // e.g., "favorite_food"
  "label": "Property Label", // e.g., "Favorite Food"
  "type": "string",
  "fieldType": "text"
}
```

**Example (Creating a "Favorite Food" property for Contacts):**

```bash
curl -X POST \
  https://api.hubapi.com/crm/v3/properties/contacts \
  -H 'Content-Type: application/json' \
  -d '{
    "groupName": "contactinformation",
    "name": "favorite_food",
    "label": "Favorite Food",
    "type": "string",
    "fieldType": "text"
  }'
```

## IV. Unique Identifier Properties

To create a property requiring unique values, set `hasUniqueValue: true`.  You can have up to 10 unique ID properties per object.

## V. Calculation Properties

Calculation properties compute values based on formulas.  Use `fieldType: calculation_equation`.  The formula is specified in the `calculationFormula` field.


**Formula Syntax:**

*   **Literals:**  Strings (`'constant'`, `"constant"`), numbers (e.g., `1005`, `1.5589`), booleans (`true`, `false`).
*   **Property Variables:**  String properties need the `string()` function (e.g., `string(myProperty)`), number properties are used directly (e.g., `myNumberProperty`), boolean properties need the `bool()` function (e.g., `bool(myBoolProperty)`).
*   **Operators:** `+`, `-`, `*`, `/`, `<`, `>`, `<=`, `>=`, `=`, `equals`, `!=`, `or`, `and`, `not`.
*   **Functions:** `max()`, `min()`, `is_present()`, `contains()`, `concatenate()`, `number_to_string()`, `string_to_number()`.
*   **Conditional Statements:** `if`, `elseif`, `else`, `endif`.

**Example Calculation Formula:**

```json
{
  "calculationFormula": "if bool(isActive) then 100 else 0 endif"
}
```

## VI. Retrieving Properties

*   **Individual Property:** `GET /crm/v3/properties/{objectType}/{propertyName}`
*   **All Properties:** `GET /crm/v3/properties/{objectType}` (Use `dataSensitivity=sensitive` to retrieve sensitive properties).

## VII. Updating Property Values

Use a `PATCH` request to `/crm/v3/objects/{objectType}/{recordId}`.  Include properties and values in the request body.

**Example (Updating "favorite_food" for a contact):**

```json
{
  "properties": {
    "favorite_food": "pizza"
  }
}
```

## VIII.  Date and DateTime Properties

Use ISO 8601 format or UNIX timestamps in milliseconds.

*   **`date` type:** YYYY-MM-DD (ISO 8601) or EPOCH milliseconds (midnight UTC).
*   **`dateTime` type:** YYYY-MM-DDThh:mm:ss.sTZD (ISO 8601) or UNIX milliseconds.


## IX. Checkbox Properties

*   **Boolean checkbox:** `true` or `false`.
*   **Multiple select checkbox:** Semicolon-separated values (e.g., `;value1;value2`).  A leading semicolon appends values.


## X.  Record Owners

Assign record owners using the user's `id` (obtained from the owners API or property settings) in the `hubspot_owner_id` property.


## XI. Clearing Property Values

Set the property value to an empty string (`""`).


This markdown provides a comprehensive overview of the HubSpot CRM API's properties functionality.  Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
