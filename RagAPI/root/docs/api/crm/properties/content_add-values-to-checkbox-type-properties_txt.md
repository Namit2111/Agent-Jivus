# HubSpot CRM API: Properties Documentation

This document details the HubSpot CRM API's functionality for managing properties.  Properties are used to store information on CRM records (Contacts, Companies, Deals, etc.).  HubSpot provides default properties, and you can create custom properties via the API or the HubSpot UI.

## API Endpoints

All endpoints are under the `/crm/v3/properties` base path.  Replace `{objectType}` with the object type (e.g., `contacts`, `companies`, `deals`).  Replace `{propertyName}` with the name of the property.  Replace `{recordId}` with the ID of the CRM record.

**1. Create a Property:**

* **Method:** `POST /crm/v3/properties/{objectType}`
* **Request Body (JSON):**
  ```json
  {
    "groupName": "groupName", // Property group name
    "name": "propertyName", // Internal property name (e.g., favorite_food)
    "label": "Property Label", // Display name in HubSpot (e.g., Favorite Food)
    "type": "string", // Property type (bool, enumeration, date, dateTime, string, number, object_coordinates, json)
    "fieldType": "text", // Field type (booleancheckbox, calculation_equation, checkbox, date, file, html, number, phonenumber, radio, select, textarea)
    "hasUniqueValue": false // Set to true for unique identifier properties (max 10 per object)
  }
  ```
* **Example:** Creating a "Favorite Food" property for contacts:
  ```json
  {
    "groupName": "contactinformation",
    "name": "favorite_food",
    "label": "Favorite Food",
    "type": "string",
    "fieldType": "text"
  }
  ```
* **Response:**  Success response (HTTP 201) with the created property details.  Failure response with error details.


**2. Create a Unique Identifier Property:**

*  Similar to creating a regular property, but set `hasUniqueValue: true`.  This ensures only one record can have a specific value for this property.  Example request body is shown in the original text.

**3. Create Calculation Properties:**

* **Method:** `POST /crm/v3/properties/{objectType}`
* **Request Body (JSON):** Includes `calculationFormula` field defining the calculation logic.  `fieldType` must be `calculation_equation`.  `type` can be `number`, `bool`, `string`, or `enumeration`.
* **Example:**
   ```json
   {
     "groupName": "dealinformation",
     "name": "calculated_value",
     "label": "Calculated Value",
     "type": "number",
     "fieldType": "calculation_equation",
     "calculationFormula": "property1 + property2"
   }
   ```
* **Important:** Calculation properties created via API cannot be edited in the HubSpot UI.

**4. Retrieve Properties:**

* **Method:** `GET /crm/v3/properties/{objectType}` (all properties) or `GET /crm/v3/properties/{objectType}/{propertyName}` (single property)
* **Query Parameter (for GET /crm/v3/properties/{objectType}):** `dataSensitivity=sensitive` (to retrieve sensitive properties; Enterprise only).
* **Response:** JSON array (for all properties) or JSON object (for single property) containing property details.

**5. Update Property Values:**

* **Method:** `PATCH /crm/v3/objects/{objectType}/{recordId}`
* **Request Body (JSON):**
  ```json
  {
    "properties": {
      "propertyName": "newValue"
    }
  }
  ```
* **Example:** Updating the "Favorite Food" property for a contact with ID 123:
  ```json
  {
    "properties": {
      "favorite_food": "Pizza"
    }
  }
  ```
* **Special Handling:**
    * **Date/DateTime:** Use ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDThh:mm:ss.sTZD) or UNIX timestamp in milliseconds (UTC).  `date` properties only store the date; `dateTime` stores date and time.
    * **Checkbox:** `booleancheckbox`: `true` or `false`. `checkbox`:  Use semicolons to separate multiple values (e.g., ";value1;value2").  A leading semicolon appends values instead of overwriting.

**6. Clear Property Value:**

* Set the property value to an empty string in the `PATCH` request.


## Property Types and `fieldType` Values

| `type`       | Description                                  | Valid `fieldType` Values                      |
|--------------|----------------------------------------------|----------------------------------------------|
| `bool`       | Boolean value                               | `booleancheckbox`, `calculation_equation`   |
| `enumeration` | String with options separated by semicolons | `booleancheckbox`, `checkbox`, `radio`, `select`, `calculation_equation` |
| `date`       | Date (YYYY-MM-DD)                           | `date`                                      |
| `dateTime`   | Date and time (YYYY-MM-DDThh:mm:ss.sTZD)     | `date`                                      |
| `string`     | Text string                                   | `file`, `text`, `textarea`, `calculation_equation`, `html`, `phonenumber` |
| `number`     | Numeric value                                 | `number`, `calculation_equation`             |
| `object_coordinates` | Internal use only                         | `text`                                      |
| `json`       | JSON formatted text                          | `text`                                      |


## Calculation Property Syntax

Calculation properties use a custom formula language with:

* **Literals:** String ("text"), Number (123), Boolean (true/false)
* **Property Variables:** `string(propertyName)` (for strings), `propertyName` (for numbers), `bool(propertyName)` (for booleans). Case-sensitive except for strings.
* **Operators:** `+`, `-`, `*`, `/`, `<`, `>`, `<=`, `>=`, `=`, `equals`, `!=`, `or`, `and`, `not`
* **Functions:** `max()`, `min()`, `is_present()`, `contains()`, `concatenate()`, `number_to_string()`, `string_to_number()`
* **Conditional Statements:** `if`, `elseif`, `else`, `endif`


## Error Handling

The API returns standard HTTP status codes and JSON error responses to indicate success or failure.


This documentation provides a comprehensive overview of HubSpot's CRM API properties functionality.  Refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications.
