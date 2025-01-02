# HubSpot CRM API Imports Documentation

This document details the HubSpot CRM API's import functionality, allowing you to import CRM records and activities (contacts, companies, notes, etc.) into your HubSpot account.  After import, you can manage these records via other CRM API endpoints.  You can also import data using HubSpot's guided import tool.

## API Endpoints

* **POST `/crm/v3/imports`**: Starts a new import.  Requires `multipart/form-data` content type.
* **GET `/crm/v3/imports`**: Retrieves a list of all imports.  Supports paging and limiting.
* **GET `/crm/v3/imports/{importId}`**: Retrieves details for a specific import.
* **POST `/crm/v3/imports/{importId}/cancel`**: Cancels an active import.
* **GET `/crm/v3/imports/{importId}/errors`**: Retrieves error details for a specific import.


##  Starting an Import (POST `/crm/v3/imports`)

This endpoint accepts a `multipart/form-data` request with the following fields:

* **`importRequest` (text):** JSON payload defining the import details (see below).
* **`files` (file):** The import file (CSV or Spreadsheet).

**Request Headers:**

* `Content-Type: multipart/form-data`

**`importRequest` JSON Structure:**

```json
{
  "name": "Import Name", // Displayed in HubSpot & used for referencing
  "importOperations": { // Optional; defaults to UPSERT
    "0-1": "CREATE" // Example: Create only for object type "0-1" (Contacts).  UPDATE, UPSERT also supported.
  },
  "dateFormat": "DAY_MONTH_YEAR" | "DAY_MONTH_YEAR" | "YEAR_MONTH_DAY", // Defaults to DAY_MONTH_YEAR
  "marketableContactImport": true | false, // Optional; only for contacts in marketing-enabled accounts
  "createContactListFromImport": true | false, // Optional; creates a static list of contacts
  "files": [
    {
      "fileName": "file.csv",
      "fileFormat": "CSV" | "SPREADSHEET",
      "fileImportPage": {
        "hasHeader": true, // Indicates if the first row is a header
        "columnMappings": [ // Array of column mappings (see below)
          {
            "columnObjectTypeId": "0-1", // Object type ID (e.g., "0-1" for Contacts, "0-2" for Companies)
            "columnName": "Column Header",
            "propertyName": "hubspotPropertyName", // HubSpot property name
            "columnType": "HUBSPOT_OBJECT_ID" | "HUBSPOT_ALTERNATE_ID" | "FLEXIBLE_ASSOCIATION_LABEL" | "ASSOCIATION_KEYS" | "STANDARD" | "EVENT_TIMESTAMP", //Column Type (see details below)
            "toColumnObjectTypeId": "0-2", // For multi-file imports; object type ID of the related object
            "foreignKeyType": { // For multi-file imports; defines association type
              "associationTypeId": 1,
              "associationCategory": "HUBSPOT_DEFINED"
            },
            "associationIdentifierColumn": true | false // For multi-file imports; indicates common column for association
          }
        ]
      }
    }
  ]
}
```

**Column Types:**

* `HUBSPOT_OBJECT_ID`:  A HubSpot record ID.
* `HUBSPOT_ALTERNATE_ID`: A unique identifier (e.g., email).
* `FLEXIBLE_ASSOCIATION_LABEL`:  For associating records using labels.
* `ASSOCIATION_KEYS`: For same-object association imports.
* `STANDARD`: Default column type.
* `EVENT_TIMESTAMP`: For Marketing Event participant imports.


## Examples

**Example 1: Single File, Single Object (Contacts)**

```json
{
  "name": "Contacts Import",
  "files": [
    {
      "fileName": "contacts.csv",
      "fileFormat": "CSV",
      "fileImportPage": {
        "hasHeader": true,
        "columnMappings": [
          {"columnObjectTypeId": "0-1", "columnName": "FirstName", "propertyName": "firstname"},
          {"columnObjectTypeId": "0-1", "columnName": "LastName", "propertyName": "lastname"},
          {"columnObjectTypeId": "0-1", "columnName": "Email", "propertyName": "email", "columnType": "HUBSPOT_ALTERNATE_ID"}
        ]
      }
    }
  ]
}
```

**Example 2: Multi-File Import (Contacts and Companies)**

*(See the provided lengthy example in the original text for a detailed multi-file import scenario)*


## Retrieving Imports (GET `/crm/v3/imports` and GET `/crm/v3/imports/{importId}`)

**Response:**  Includes `importId`, `name`, `state` (STARTED, PROCESSING, DONE, FAILED, CANCELED, DEFERRED), and other import details.


## Cancelling Imports (POST `/crm/v3/imports/{importId}/cancel`)

**Response:**  Indicates success or failure.


## Viewing Import Errors (GET `/crm/v3/imports/{importId}/errors`)

**Response:**  A list of errors encountered during the import.


## Limits

* **Daily Row Limit:** 80,000,000
* **File Size/Row Limit:** 1,048,576 rows or 512 MB (whichever is reached first).  Exceeding this results in a 429 HTTP error.


## Error Handling

Common errors include incorrect column counts, parsing errors, and improper file formats. Carefully review your request JSON and input file for consistency and accuracy.  Check for duplicate headers, especially `Content-Type`.


This documentation provides a comprehensive overview of the HubSpot CRM API imports functionality. Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
