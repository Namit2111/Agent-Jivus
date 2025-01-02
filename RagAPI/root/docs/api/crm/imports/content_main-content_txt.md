# HubSpot CRM API Imports Documentation

This document details the HubSpot CRM API's import functionality, allowing you to import CRM records and activities (contacts, companies, notes, etc.) into your HubSpot account.  After import, you can manage these records via other CRM API endpoints.  This API complements HubSpot's guided import tool.

## API Endpoints

All endpoints are under the `/crm/v3/imports` base path.

* **`POST /crm/v3/imports`**: Starts a new import.  Requires a `multipart/form-data` request.
* **`GET /crm/v3/imports`**: Retrieves a list of all imports.  Supports pagination.
* **`GET /crm/v3/imports/{importId}`**: Retrieves details for a specific import using its `importId`.
* **`POST /crm/v3/imports/{importId}/cancel`**: Cancels an active import.
* **`GET /crm/v3/imports/{importId}/errors`**: Retrieves error details for a specific import.


## API Calls

### Starting an Import (`POST /crm/v3/imports`)

This endpoint accepts a `multipart/form-data` request with the following parts:

* **`importRequest` (text):**  JSON payload defining the import details (see below).
* **`files` (file):** The import file itself (CSV or Spreadsheet).

**Request Headers:**

```
Content-Type: multipart/form-data
```

**`importRequest` JSON Structure:**

```json
{
  "name": "Import Name", // Displayed in HubSpot and used for referencing
  "importOperations": { // Optional; defaults to UPSERT
    "0-1": "CREATE", // objectTypeId: operation (CREATE, UPDATE, UPSERT)
    "0-2": "UPSERT"   // Multiple object types can be specified
  },
  "dateFormat": "DAY_MONTH_YEAR" | "MONTH_DAY_YEAR" | "YEAR_MONTH_DAY", // Date format in the file
  "marketableContactImport": true | false, // Optional; for marketing contacts (requires marketing access)
  "createContactListFromImport": true | false, // Optional; creates a static list of contacts
  "files": [
    {
      "fileName": "file.csv",
      "fileFormat": "CSV" | "SPREADSHEET",
      "fileImportPage": {
        "hasHeader": true, // Indicates if the file has a header row
        "columnMappings": [ // Array of column mappings
          {
            "columnObjectTypeId": "0-1", // Object type ID (e.g., "0-1" for contacts)
            "columnName": "Column Name",
            "propertyName": "hubspotPropertyName", // HubSpot property name
            "columnType": "STANDARD" | "HUBSPOT_OBJECT_ID" | "HUBSPOT_ALTERNATE_ID" | "FLEXIBLE_ASSOCIATION_LABEL" | "ASSOCIATION_KEYS", //Column Type (see details below)
            "toColumnObjectTypeId": "0-2", // For multi-file imports, object type ID of related object
            "foreignKeyType": { //For multi-file imports
              "associationTypeId": 280,
              "associationCategory": "HUBSPOT_DEFINED"
            },
            "associationIdentifierColumn": true | false // For multi-file imports
          },
          // ... more column mappings
        ]
      }
    }
    // ... more files (for multi-file imports)
  ]
}
```

**Column Types:**

* `STANDARD`: Default column type.
* `HUBSPOT_OBJECT_ID`:  Column contains HubSpot object IDs.
* `HUBSPOT_ALTERNATE_ID`: Column contains a unique identifier (e.g., email).
* `FLEXIBLE_ASSOCIATION_LABEL`: Column contains association labels (for single-file multi-object imports).
* `ASSOCIATION_KEYS`: For same-object association imports.


### Retrieving Imports (`GET /crm/v3/imports`, `GET /crm/v3/imports/{importId}`)

These endpoints return JSON data describing imports.  The response for a specific import includes its `state`:

* `STARTED`: Import is queued.
* `PROCESSING`: Import is in progress.
* `DONE`: Import completed successfully.
* `FAILED`: Import failed.
* `CANCELED`: Import was canceled.
* `DEFERRED`: Import is delayed (max 3 imports concurrently).


### Canceling an Import (`POST /crm/v3/imports/{importId}/cancel`)

Sends a `POST` request to the specified import ID to cancel it.


### Retrieving Import Errors (`GET /crm/v3/imports/{importId}/errors`)

Returns JSON data detailing any errors encountered during the import.


## Examples

See the provided text for detailed JSON examples of different import scenarios (single file, single object; single file, multiple objects; multiple files).


## Limits

* **Daily Row Limit:** 80,000,000
* **File Row Limit:** 1,048,576
* **File Size Limit:** 512 MB

Exceeding limits results in a 429 HTTP error.  Large imports should be split into smaller batches.


## Error Handling

The API returns standard HTTP status codes.  Examine the response body for detailed error messages.  Common errors include incorrect column counts, parsing failures, and mismatched data types.  Ensure your request data aligns precisely with the file's structure.  Check for duplicate headers (like `Content-Type`) in your requests.


This documentation provides a comprehensive overview of the HubSpot CRM API Imports.  Refer to the official HubSpot API documentation for the most up-to-date information and details.
