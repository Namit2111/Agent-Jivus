# HubSpot CRM Imports API Documentation

This document details the HubSpot CRM Imports API, allowing you to import CRM records and activities (contacts, companies, notes, etc.) into your HubSpot account.  After import, you can manage these records via other CRM API endpoints.

## API Endpoints

All endpoints are located under the `/crm/v3/imports` base path.  Replace `{importId}` with the specific import ID.

* **POST `/crm/v3/imports`**: Starts a new import.  This is a `multipart/form-data` request.
* **GET `/crm/v3/imports`**: Retrieves all imports for the account (limited by private app access token).
* **GET `/crm/v3/imports/{importId}`**: Retrieves details for a specific import.
* **POST `/crm/v3/imports/{importId}/cancel`**: Cancels an active import.
* **GET `/crm/v3/imports/{importId}/errors`**: Retrieves errors for a specific import.


## API Calls

### 1. Start an Import (POST `/crm/v3/imports`)

This endpoint accepts a `multipart/form-data` request with the following parts:

* **`importRequest` (text):**  A JSON object defining the import details (see below).
* **`files` (file):** The import file (CSV or Spreadsheet).

**Request Headers:**

```
Content-Type: multipart/form-data
```

**`importRequest` JSON Structure:**

```json
{
  "name": "Import Name", // Required. Displayed in HubSpot and used for referencing.
  "importOperations": { "objectTypeId": "operation" }, // Optional.  "objectTypeId" is e.g., "0-1" for contacts. "operation" is one of "UPSERT", "CREATE", or "UPDATE". Default is UPSERT.
  "dateFormat": "DAY_MONTH_YEAR" | "MONTH_DAY_YEAR" | "YEAR_MONTH_DAY", // Optional. Default is MONTH_DAY_YEAR.
  "marketableContactImport": true | false, // Optional. Only for contacts in marketing-enabled accounts.
  "createContactListFromImport": true | false, // Optional. Creates a static list of imported contacts.
  "files": [
    {
      "fileName": "file.csv", // Required. File name including extension.
      "fileFormat": "CSV" | "SPREADSHEET", // Required.  CSV or Spreadsheet.
      "fileImportPage": {
        "hasHeader": true | false, // Required. Indicates if the file has a header row.
        "columnMappings": [ // Required. Array of column mappings.
          {
            "columnObjectTypeId": "objectTypeId", // Required.  Object type ID (e.g., "0-1" for contacts).
            "columnName": "Column Header", // Required. Header name from the file.
            "propertyName": "HubSpot Property Name", // Required. HubSpot property's internal name (except for common columns in multi-file imports).
            "columnType": "STANDARD" | "HUBSPOT_OBJECT_ID" | "HUBSPOT_ALTERNATE_ID" | "FLEXIBLE_ASSOCIATION_LABEL" | "ASSOCIATION_KEYS" | "EVENT_TIMESTAMP", //Optional. Specifies column type.
            "toColumnObjectTypeId": "objectTypeId", // Optional. For multi-file imports; object type ID of the related object.
            "foreignKeyType": { "associationTypeId": int, "associationCategory": "HUBSPOT_DEFINED" }, // Optional.  For multi-file imports; association type.
            "associationIdentifierColumn": true | false // Optional. For multi-file imports; indicates common column for association.
            "marketingEventSubmissionType": "REGISTERED" | "JOINED" | "LEFT" | "CANCELLED" //Optional, only for EVENT_TIMESTAMP columnType
          },
          // ... more column mappings
        ]
      }
    }
    // ... more files (for multi-file imports)
  ]
}
```

**Example (Single File, Single Object - Contacts):**

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

**Response (Success):**

```json
{
  "importId": 12345
}
```


### 2. Get Imports (GET `/crm/v3/imports`)

**Response (Success):**  Returns an array of import objects, each containing details like `importId`, `name`, `state` (STARTED, PROCESSING, DONE, FAILED, CANCELED, DEFERRED), etc.


### 3. Get Import Details (GET `/crm/v3/imports/{importId}`)

**Response (Success):** Returns a single import object with detailed information.

### 4. Cancel Import (POST `/crm/v3/imports/{importId}/cancel`)

**Response (Success):**  Confirms cancellation.


### 5. Get Import Errors (GET `/crm/v3/imports/{importId}/errors`)

**Response (Success):**  Returns an array of error objects detailing import failures.


## File Requirements

* **Format:** CSV or Spreadsheet (XLSX).
* **Header Row:**  A header row is generally required, indicated by `hasHeader: true` in the `importRequest`.
* **Column Mapping:** Each column must be mapped to a HubSpot property in the `columnMappings` array.  The order of columns in the file and the `columnMappings` array *must* match.
* **Size Limits:** Maximum 1,048,576 rows or 512 MB per file.  Daily limit of 80,000,000 rows.


## Error Handling

The API returns standard HTTP status codes.  Check the response body for detailed error messages. Common errors include incorrect column counts, parsing errors, and exceeding import limits.


## Examples (provided in the original text are already well formatted and explained)


## Limits

* **Rows per file:** 1,048,576
* **File size:** 512 MB
* **Rows per day:** 80,000,000

Exceeding these limits results in a 429 HTTP error.  Split large imports into smaller chunks.
