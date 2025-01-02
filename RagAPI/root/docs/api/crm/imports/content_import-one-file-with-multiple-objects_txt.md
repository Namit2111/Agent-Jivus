# HubSpot CRM API Imports Documentation

This document details the HubSpot CRM API for importing data.  It covers starting an import, formatting the request data, mapping columns to properties, handling various import scenarios, retrieving import status, cancelling imports, troubleshooting errors, and API limits.

## API Endpoint

The primary endpoint for importing data is:

`POST /crm/v3/imports`

This endpoint accepts `multipart/form-data` requests.

## Request Body

The request body consists of two key fields:

*   **`importRequest` (text):** A JSON string containing the import specifications.
*   **`files` (file):** The import file itself (CSV or Spreadsheet).


### `importRequest` JSON Structure

The `importRequest` JSON object contains the following fields:

*   **`name` (string):**  The name of the import (displayed in HubSpot's import tool).  Example: `"November Marketing Event Leads"`
*   **`importOperations` (object, optional):** Specifies the import operation type for each object type.  Keys are `objectTypeId` values (e.g., `"0-1"` for contacts), and values are `"CREATE"`, `"UPDATE"`, or `"UPSERT"` (create and update). Default is `UPSERT`. Example: `{"0-1": "CREATE"}`
*   **`dateFormat` (string, optional):** The date format in the import file. Options: `"MONTH_DAY_YEAR"`, `"DAY_MONTH_YEAR"`, `"YEAR_MONTH_DAY"`. Default: `"MONTH_DAY_YEAR"`
*   **`marketableContactImport` (boolean, optional):**  Only for contact imports in marketing-enabled accounts. `true` for marketing contacts, `false` for non-marketing contacts.
*   **`createContactListFromImport` (boolean, optional):** Creates a static list of contacts from the import.  `true` to create a list.
*   **`files` (array):** An array containing file details (see below).  Note: even with a single file, this must be an array.


#### File Details within `files` array

Each element in the `files` array describes a file:

*   **`fileName` (string):** The name of the file, including extension (e.g., `"Nov-event-leads.csv"`).
*   **`fileFormat` (string):** `"CSV"` or `"SPREADSHEET"`.
*   **`fileImportPage` (object):** Contains column mapping details.
    *   **`hasHeader` (boolean):** `true` if the file has a header row.
    *   **`columnMappings` (array):** An array of column mappings (see below).

##### Column Mapping (`columnMappings`)

Each element in `columnMappings` maps a column in the import file to a HubSpot property:

*   **`columnObjectTypeId` (string):** The `objectTypeId` of the object the column belongs to (e.g., `"0-1"` for contacts).
*   **`columnName` (string):** The name of the column in the import file.
*   **`propertyName` (string):** The internal name of the HubSpot property.  Set to `null` for common columns in multi-file imports.
*   **`columnType` (string, optional):** Specifies the column's data type. Options include:
    *   `HUBSPOT_OBJECT_ID`:  A HubSpot record ID.
    *   `HUBSPOT_ALTERNATE_ID`: A unique identifier (e.g., email).
    *   `FLEXIBLE_ASSOCIATION_LABEL`: For association labels.
    *   `ASSOCIATION_KEYS`: For same-object association imports.
    *   `STANDARD`: Default standard column.
    *   `EVENT_TIMESTAMP`: For marketing event timestamps.
*   **`toColumnObjectTypeId` (string, optional):** For multi-file imports, the `objectTypeId` of the object the common column relates to (in the other file).
*   **`foreignKeyType` (object, optional):** For multi-file imports, specifies the association type (`associationTypeId` and `associationCategory`).
*   **`associationIdentifierColumn` (boolean, optional):** For multi-file imports; `true` if the column is the identifier for association.


## Examples

### Import One File with One Object (Contacts)

```json
{
  "name": "November Marketing Event Leads",
  "importOperations": {"0-1": "CREATE"},
  "dateFormat": "DAY_MONTH_YEAR",
  "files": [
    {
      "fileName": "Nov-event-leads.csv",
      "fileFormat": "CSV",
      "fileImportPage": {
        "hasHeader": true,
        "columnMappings": [
          {"columnObjectTypeId": "0-1", "columnName": "First Name", "propertyName": "firstname"},
          {"columnObjectTypeId": "0-1", "columnName": "Last Name", "propertyName": "lastname"},
          {"columnObjectTypeId": "0-1", "columnName": "Email", "propertyName": "email", "columnType": "HUBSPOT_ALTERNATE_ID"}
        ]
      }
    }
  ]
}
```

### Import One File with Multiple Objects (Association Labels)

```json
{
  "name": "Association Label Import",
  "dateFormat": "DAY_MONTH_YEAR",
  "files": [
    {
      "fileName": "association label example.xlsx",
      "fileFormat": "SPREADSHEET",
      "fileImportPage": {
        "hasHeader": true,
        "columnMappings": [
          {"columnObjectTypeId": "0-1", "columnName": "Email", "propertyName": "email"},
          {"columnObjectTypeId": "0-2", "columnName": "Domain", "propertyName": "domain"},
          {"columnName": "Association Label", "columnType": "FLEXIBLE_ASSOCIATION_LABEL", "columnObjectTypeId": "0-1", "toColumnObjectTypeId": "0-2"}
        ]
      }
    }
  ]
}
```


### Import Multiple Files (Contacts and Companies)

```json
{
  "name": "Contact Company import",
  "dateFormat": "YEAR_MONTH_DAY",
  "files": [
    // ... (contact file details) ...
    // ... (company file details) ...
  ]
}
```

(See the original documentation for the complete details of the contact and company file details)


## Response

A successful POST request returns a JSON response containing an `importId`.

```json
{
  "importId": 12345
}
```

## Retrieving Imports

*   **GET `/crm/v3/imports`:** Retrieves all imports.
*   **GET `/crm/v3/imports/{importId}`:** Retrieves a specific import.


## Cancelling Imports

`POST /crm/v3/imports/{importId}/cancel`


## Error Handling

GET `/crm/v3/imports/{importId}/errors` retrieves errors for a specific import.

## Limits

*   80,000,000 rows per day.
*   1,048,576 rows or 512 MB per file, whichever is reached first.  A 429 HTTP error indicates exceeding these limits.


This markdown documentation provides a structured and comprehensive overview of the HubSpot CRM API imports functionality, including detailed explanations, JSON examples, and API calls.  Remember to consult the official HubSpot API documentation for the most up-to-date information and a complete list of `objectTypeId` values.
