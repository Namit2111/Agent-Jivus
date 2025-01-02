# HubSpot CRM API Imports Documentation

This document details the HubSpot CRM API's import functionality, allowing you to import CRM records and activities (contacts, companies, notes, etc.) into your HubSpot account.  After import, you can manage these records via other CRM API endpoints.  This API complements HubSpot's guided import tool.

## API Endpoints

* **POST `/crm/v3/imports`**: Starts a new import.  This is a `multipart/form-data` request.
* **GET `/crm/v3/imports`**: Retrieves all imports for the account (limited to imports by the private app if using a private app token).
* **GET `/crm/v3/imports/{importId}`**: Retrieves details of a specific import.
* **POST `/crm/v3/imports/{importId}/cancel`**: Cancels an active import.
* **GET `/crm/v3/imports/{importId}/errors`**: Retrieves errors for a specific import.

##  Request Body (POST `/crm/v3/imports`)

The POST request to start an import uses `multipart/form-data`.  It requires two parts:

* **`importRequest` (text):** A JSON object specifying import details. See below for details.
* **`files` (file):** The import file itself (CSV or Spreadsheet).

**`importRequest` JSON Structure:**

```json
{
  "name": "Import Name", // Required: Display name in HubSpot
  "importOperations": { "objectTypeId": "operationType" }, // Optional: CREATE, UPDATE, UPSERT (default: UPSERT).  Example: {"0-1": "CREATE"} for contacts.
  "dateFormat": "DAY_MONTH_YEAR" | "MONTH_DAY_YEAR" | "YEAR_MONTH_DAY", // Optional: Date format in the file (default: MONTH_DAY_YEAR)
  "marketableContactImport": true | false, // Optional: For contacts, sets marketing status (requires marketing access).
  "createContactListFromImport": true | false, // Optional: Creates a static list from imported contacts.
  "files": [ // Required: Array of file objects (even for single-file imports)
    {
      "fileName": "file.csv", // Required: Filename
      "fileFormat": "CSV" | "SPREADSHEET", // Required: File format
      "fileImportPage": { // Required
        "hasHeader": true | false, // Required: Indicates if the file has a header row
        "columnMappings": [ // Required: Array of column mappings
          {
            "columnObjectTypeId": "objectTypeId", // Required: HubSpot object type ID (e.g., "0-1" for contacts).
            "columnName": "Column Header", // Required: Column name from the file
            "propertyName": "HubSpot Property Name", // Required (except for common columns in multi-file imports)
            "columnType": "STANDARD" | "HUBSPOT_OBJECT_ID" | "HUBSPOT_ALTERNATE_ID" | "FLEXIBLE_ASSOCIATION_LABEL" | "ASSOCIATION_KEYS" | "EVENT_TIMESTAMP", // Optional: Specifies column data type
            "toColumnObjectTypeId": "objectTypeId", // Optional: For multi-file imports, object type ID of the related object (common column).
            "foreignKeyType": { "associationTypeId": 123, "associationCategory": "HUBSPOT_DEFINED" }, // Optional: For multi-file imports, association type.
            "associationIdentifierColumn": true | false, // Optional: For multi-file imports, identifies the common column.
            "marketingEventSubmissionType": "REGISTERED" | "JOINED" | "LEFT" | "CANCELLED", // Optional: For Marketing Event Participant imports.
          }
        ]
      }
    }
  ]
}
```

## Example Imports

### Single File, Single Object (Contacts)

```json
{
  "name": "November Marketing Event Leads",
  "importOperations": { "0-1": "CREATE" },
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

### Single File, Multiple Objects (Association with Labels)

```json
{
  "name": "Association Label Import",
  "dateFormat": "DAY_MONTH_YEAR",
  "files": [
    {
      "fileName": "association_label_example.xlsx",
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


### Multiple Files (Contacts and Companies)

```json
{
  "name": "Contact Company import",
  "dateFormat": "YEAR_MONTH_DAY",
  "files": [
    // ... (Contact file details similar to the single-file example) ...
    {
      "fileName": "company-import-file.csv",
      "fileFormat": "CSV",
      "fileImportPage": {
        "hasHeader": true,
        "columnMappings": [
          // ... (Company properties) ...
          {"columnObjectTypeId": "0-2", "toColumnObjectTypeId": "0-1", "columnName": "Email", "propertyName": null, "foreignKeyType": {"associationTypeId": 280, "associationCategory": "HUBSPOT_DEFINED"}}
        ]
      }
    }
  ]
}
```

## Response

A successful import returns a JSON object containing the `importId`.  Error responses will contain an HTTP error code and details about the issue.


## Import States

* `STARTED`: Import recognized but not yet processing.
* `PROCESSING`: Import is in progress.
* `DONE`: Import completed successfully.
* `FAILED`: Import failed due to an error.
* `CANCELED`: Import cancelled by the user.
* `DEFERRED`: Import delayed because the maximum number of concurrent imports is reached (limit of 3).

## Limits

* **Daily Row Limit:** 80,000,000
* **File Row Limit:** 1,048,576
* **File Size Limit:** 512 MB

Exceeding limits results in a 429 HTTP error.  Large imports should be split into smaller batches.


## Error Handling and Troubleshooting

The `/crm/v3/imports/{importId}/errors` endpoint provides details about import failures.  Common errors include incorrect column counts, parsing errors, and unmatched header rows.  Ensure that:

* Column order in the request and file match.
* All columns are mapped.
* File name in the request matches the actual file name, including extension.
* The `Content-Type` header is correctly set to `multipart/form-data`.

Remember to remove duplicate headers (e.g., `Content-Type`) if present in your request.
