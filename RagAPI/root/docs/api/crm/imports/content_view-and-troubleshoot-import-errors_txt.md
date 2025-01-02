# HubSpot CRM API Imports Documentation

This document details the HubSpot CRM API for importing data.  It covers starting an import, formatting the request, mapping columns to properties, handling multiple files and objects, retrieving import status, cancelling imports, and troubleshooting errors.

## API Endpoints

* **Start an import:** `POST /crm/v3/imports`
* **Get all imports:** `GET /crm/v3/imports`
* **Get a specific import:** `GET /crm/v3/imports/{importId}`
* **Cancel an import:** `POST /crm/v3/imports/{importId}/cancel`
* **View import errors:** `GET /crm/v3/imports/{importId}/errors`

## API Calls

All API calls require authentication using a HubSpot API key.  Requests are made using HTTP methods as specified above.

### 1. Starting an Import (`POST /crm/v3/imports`)

This endpoint initiates a data import.  The request is a `multipart/form-data` type, containing:

* **`importRequest` (text):** JSON payload defining import parameters (detailed below).
* **`files` (file):** The import file (CSV or Spreadsheet).

**Headers:**

* `Content-Type: multipart/form-data`

**Example using Postman (Illustrative - actual implementation depends on your chosen client):**  *(Refer to provided screenshots in the original document for visual representation)*

A Postman request would include the `importRequest` JSON in the body and the import file attached as a file.

### 2. Formatting the `importRequest` Data (JSON)

The `importRequest` JSON payload specifies details about the import:

* **`name` (string):**  Name of the import (displayed in HubSpot).
* **`importOperations` (object, optional):** Specifies create/update behavior for each object type.  Key is `objectTypeId` (e.g., `"0-1"` for contacts), value is `"CREATE"`, `"UPDATE"`, or `"UPSERT"` (default).  Example: `{"0-1": "CREATE"}`.
* **`dateFormat` (string):** Date format in the file ("MONTH_DAY_YEAR", "DAY_MONTH_YEAR", or "YEAR_MONTH_DAY"). Default: "MONTH_DAY_YEAR".
* **`marketableContactImport` (boolean, optional):** For contacts, indicates marketing status (only for accounts with marketing contacts access). `true` for marketing contacts, `false` for non-marketing.
* **`createContactListFromImport` (boolean, optional):** Creates a static list of contacts from the import. `true` to create a list.
* **`files` (array):**  An array of file objects (detailed below).  Multiple file objects enable multi-file imports.
* **`marketingEventObjectId` (integer, optional):**  The ID of the marketing event (required for marketing event participant imports).


### 3.  `files` Array Structure

Each element in the `files` array describes a single file:

* **`fileName` (string):** File name (including extension).
* **`fileFormat` (string):** `"CSV"` or `"SPREADSHEET"`.
* **`fileImportPage` (object):**
    * **`hasHeader` (boolean):**  Indicates if the file has a header row.
    * **`columnMappings` (array):** Array of column mappings (detailed below).


### 4. Column Mappings (`columnMappings` Array)

Each element in `columnMappings` maps a file column to a HubSpot property:

* **`columnObjectTypeId` (string):**  HubSpot object type ID (e.g., `"0-1"` for contacts).
* **`columnName` (string):** Column header name in the file.
* **`propertyName` (string):** Internal name of the HubSpot property.  `null` for common columns in multi-file imports.
* **`columnType` (string, optional):**  Specifies column content type: `"HUBSPOT_OBJECT_ID"`, `"HUBSPOT_ALTERNATE_ID"`, `"FLEXIBLE_ASSOCIATION_LABEL"`, `"ASSOCIATION_KEYS"`, `"STANDARD"`, `"EVENT_TIMESTAMP"`.
* **`toColumnObjectTypeId` (string, optional):** For multi-file imports, the object type ID of the object the common column property belongs to.
* **`foreignKeyType` (object, optional):** For multi-file imports, association type.  Contains `associationTypeId` and `associationCategory`.
* **`associationIdentifierColumn` (boolean, optional):** For multi-file imports, indicates if the column is the association identifier.



## Import Types: Examples

The original document provides examples for:

* **One file, one object:** Importing contacts (using `CREATE`).
* **One file, multiple objects:** Importing contacts and companies with association labels.
* **Multiple files, multiple objects:** Importing contacts and companies with a common column (`Email`).
* **Marketing Event Participants:**  Importing and updating marketing event participant records.

*(Refer to the JSON examples provided in the original document for detailed code snippets)*

## Response

A successful import returns a JSON response including an `importId`.

```json
{
  "importId": 12345
}
```

Other states include: `STARTED`, `PROCESSING`, `DONE`, `FAILED`, `CANCELED`, `DEFERRED`.  These can be retrieved using the `GET` endpoints.


## Error Handling

The `/crm/v3/imports/{importId}/errors` endpoint provides details on import failures. Common errors include incorrect column numbers, parsing issues, and unmatched headers.


## Limits

* **Daily Row Limit:** 80,000,000 rows.
* **File Limit:** 1,048,576 rows or 512 MB, whichever is reached first.  Exceeding these limits results in a 429 HTTP error.

Remember to handle potential errors and implement proper retry mechanisms in your integration.  Always check the response codes and error messages returned by the API.
