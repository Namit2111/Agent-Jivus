# HubSpot CRM API: Properties Documentation

This document details the HubSpot CRM API endpoints and methods for managing properties. Properties are used to store information on CRM records (Contacts, Companies, Deals, etc.).  HubSpot provides default properties, and you can create custom properties via the API or the HubSpot UI.

## I.  Property Types and Field Types

When creating or updating properties, you must specify both `type` and `fieldType`.

| `type`        | Description                                                                    | Valid `fieldType` Values                     |
|----------------|--------------------------------------------------------------------------------|---------------------------------------------|
| `bool`         | Boolean value (true/false).                                                    | `booleancheckbox`, `calculation_equation` |
| `enumeration` | String representing a set of options (e.g., "option1;option2;option3").        | `booleancheckbox`, `checkbox`, `radio`, `select`, `calculation_equation` |
| `date`         | Date value (YYYY-MM-DD or EPOCH timestamp in milliseconds – midnight UTC).      | `date`                                      |
| `dateTime`     | Date and time value (YYYY-MM-DDThh:mm:ss.sTZD or UNIX timestamp in milliseconds). | `date`                                      |
| `string`       | Plain text string (max 65,536 characters).                                      | `file`, `text`, `textarea`, `calculation_equation`, `html`, `phonenumber` |
| `number`       | Numeric value.                                                                | `number`, `calculation_equation`           |
| `object_coordinates` | Internal use only.  Cannot be created or edited via API.                     | `text`                                      |
| `json`         | JSON formatted text. Internal use only. Cannot be created or edited via API.     | `text`                                      |


**`fieldType` Values:**

| `fieldType`          | Description                                                                                                    |
|-----------------------|----------------------------------------------------------------------------------------------------------------|
| `booleancheckbox`     | Single checkbox (Yes/No).                                                                                    |
| `calculation_equation` | Calculated value based on a formula.                                                                         |
| `checkbox`            | Multiple checkboxes.                                                                                       |
| `date`                | Date picker.                                                                                                |
| `file`                | File upload (stores file ID).                                                                              |
| `html`                | Rich text editor (sanitized HTML).                                                                           |
| `number`              | Numeric input.                                                                                              |
| `phonenumber`         | Phone number input (formatted).                                                                            |
| `radio`               | Radio buttons (single selection).                                                                            |
| `select`              | Dropdown menu.                                                                                             |
| `text`                | Single-line text input.                                                                                      |
| `textarea`            | Multi-line text input.                                                                                     |


## II. API Endpoints and Calls

**Base URL:**  `https://api.hubapi.com/crm/v3`


**A. Create a Property:**

* **Method:** `POST`
* **Endpoint:** `/properties/{objectType}`
* **Request Body (JSON):**

```json
{
  "groupName": "propertyGroupName",
  "name": "propertyName",  // Internal name (e.g., "favorite_color")
  "label": "Property Label", // Display name (e.g., "Favorite Color")
  "type": "string",          // Property type (see table above)
  "fieldType": "text"       // Field type (see table above)
  "hasUniqueValue": false  // Optional: true for unique identifier properties (max 10 per object)
}
```

**Example (creating a contact property):**

```bash
curl -X POST \
  'https://api.hubapi.com/crm/v3/properties/contacts' \
  -H 'Content-Type: application/json' \
  -d '{
    "groupName": "contactinformation",
    "name": "favorite_food",
    "label": "Favorite Food",
    "type": "string",
    "fieldType": "text"
  }'
```


**B. Create a Unique Identifier Property:**

Set `hasUniqueValue: true` in the request body (see example above).  This ensures only one record can have a given value for that property.

**C. Create a Calculation Property:**

* **Method:** `POST`
* **Endpoint:** `/properties/{objectType}`
* **Request Body (JSON):**  Include `calculationFormula` and set `fieldType` to `calculation_equation`.

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

**Calculation Formula Syntax:**  The `calculationFormula` supports arithmetic, comparison, logical operators, conditional statements ( `if`, `elseif`, `else`, `endif`), and functions (`max`, `min`, `is_present`, `contains`, `concatenate`, `number_to_string`, `string_to_number`). See the original text for details on syntax and supported functions.


**D. Retrieve Properties:**

* **Method:** `GET`
* **Endpoint:** `/properties/{objectType}` (all properties) or `/properties/{objectType}/{propertyName}` (single property).
* **Query Parameters:**
    * `dataSensitivity=sensitive`: (Optional) Include to retrieve sensitive properties (Enterprise only).


**E. Update Property Values:**

* **Method:** `PATCH`
* **Endpoint:** `/objects/{objectType}/{recordId}`
* **Request Body (JSON):**  Include properties to update in the `properties` object.

```json
{
  "properties": {
    "propertyName1": "newValue1",
    "propertyName2": "newValue2"
  }
}
```

**Special Considerations for Data Types:**

* **Dates:** Use ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDThh:mm:ss.sTZD) or UNIX timestamps (milliseconds since epoch).  `date` properties only store the date, while `dateTime` stores both date and time.
* **Checkboxes:** Boolean checkboxes use `true` or `false`. Multiple-select checkboxes use a semicolon-separated string (e.g., ";value1;value2;value3").  Adding a leading semicolon appends values instead of overwriting.

**F. Clear Property Value:**

Set the property value to an empty string (`""`) in a `PATCH` request.

**G. Assign Record Owners:**

Use the `hubspot_owner_id` property (user ID) in a `PATCH` request to assign a record owner.  You can obtain the user ID from the HubSpot UI or the Owners API.


## III. Examples:

See the original document for more complete examples of creating properties, calculation formulas, handling dates, checkboxes, and updating records.


This expanded documentation provides a more structured and comprehensive overview of the HubSpot CRM API's property management features.  Remember to consult the official HubSpot API documentation for the most up-to-date information and error handling details.
