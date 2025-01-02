# HubSpot CRM Imports API Documentation

This document details the HubSpot CRM Imports API, allowing you to import CRM records and activities (contacts, companies, notes, etc.) into your HubSpot account.  After import, you can manage these records via other CRM API endpoints.  This API complements the HubSpot guided import tool.

## API Endpoints

All endpoints are under the base URL: `/crm/v3/imports`

**1. Start an Import (POST /crm/v3/imports)**

This endpoint initiates a data import.  The request is a `multipart/form-data` type.

* **Request Body:**
    * `importRequest` (text): JSON payload detailing the import configuration (see below).
    * `files` (file): The import file (CSV or Spreadsheet).

* **Request Headers:**
    * `Content-Type: multipart/form-data`

* **`importRequest` JSON Structure:**

```json
{
  "name": "Import Name", // Displayed name in HubSpot
  "importOperations": { // Optional; defaults to UPSERT
    "0-1": "CREATE", // Example: Create only for object type "0-1" (Contacts)
    "0-2": "UPDATE" // Example: Update only for object type "0-2" (Companies)
  },
  "dateFormat": "DAY_MONTH_YEAR" | "MONTH_DAY_YEAR" | "YEAR_MONTH_DAY", // Default: MONTH_DAY_YEAR
  "marketableContactImport": true | false, // Optional; only for marketing contacts
  "createContactListFromImport": true | false, // Optional; creates a static list
  "files": [
    {
      "fileName": "file_name.csv",
      "fileFormat": "CSV" | "SPREADSHEET",
      "fileImportPage": {
        "hasHeader": true, // Indicates if the file has a header row
        "columnMappings": [ // Array of column mappings
          {
            "columnObjectTypeId": "0-1", // Object type ID (e.g., "0-1" for contacts)
            "columnName": "Column Header",
            "propertyName": "hubspot_property_name", // HubSpot property internal name
            "columnType": "STANDARD" | "HUBSPOT_OBJECT_ID" | "HUBSPOT_ALTERNATE_ID" | "FLEXIBLE_ASSOCIATION_LABEL" | "ASSOCIATION_KEYS", //Specifies column type (see below)
            "toColumnObjectTypeId": "0-2", // For multi-file imports, object type ID of related object
            "foreignKeyType": { //For multi-file imports, association details
              "associationTypeId": 123,
              "associationCategory": "HUBSPOT_DEFINED"
            },
            "associationIdentifierColumn": true | false // For multi-file imports, if the column is the association key
          },
          // ... more column mappings
        ]
      }
    }
    // ... more files for multi-file imports
  ]
}
```

* **Column Types:**
    * `STANDARD`:  A standard property.
    * `HUBSPOT_OBJECT_ID`:  A HubSpot record ID.
    * `HUBSPOT_ALTERNATE_ID`: A unique identifier (e.g., email).
    * `FLEXIBLE_ASSOCIATION_LABEL`: For associating records using labels (single-file, multiple object).
    * `ASSOCIATION_KEYS`: For associating same object records (single file).


* **Response:** On success, returns an `importId`.  On failure, returns an error code and message.


**2. Get Imports (GET /crm/v3/imports)**

Retrieves a list of imports.  Supports pagination and limiting results.

* **Response:**  Array of import objects, each with properties like `name`, `state`, `startDate`, `state`, etc.  `state` can be `STARTED`, `PROCESSING`, `DONE`, `FAILED`, `CANCELED`, or `DEFERRED`.

**3. Get a Specific Import (GET /crm/v3/imports/{importId})**

Retrieves details for a single import using its `importId`.

* **Response:** A single import object.

**4. Cancel an Import (POST /crm/v3/imports/{importId}/cancel)**

Cancels an active import.

* **Response:**  Confirmation of cancellation.


**5. Get Import Errors (GET /crm/v3/imports/{importId}/errors)**

Retrieves error details for a failed import.

* **Response:** Array of error objects.


## Examples

**Example 1: Single File, Single Object (Contacts)**

```json
{
  "name": "Contact Import",
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

**Example 2: Multi-File Import (Contacts & Companies)**

(See the detailed example in the provided text. This requires two separate CSV files and more complex mapping)

## Limits

* 80,000,000 rows per day.
* 1,048,576 rows or 512 MB per file, whichever is reached first.


## Error Handling

The API returns standard HTTP status codes.  Check the response body for detailed error messages.  Common errors include incorrect column counts, file format issues, and exceeding import limits.


## Notes

* Use a HubSpot API key for authentication.
*  Refer to the HubSpot documentation for a complete list of `objectTypeId` values and property names.
* Imports done via the API won't be filterable in HubSpot's UI.
* For private app access tokens, only imports performed by that app are returned.



This markdown documentation provides a more structured and clearer overview of the HubSpot CRM Imports API compared to the original text.  Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
