# HubSpot CRM Imports API Documentation

This document details the HubSpot CRM Imports API, allowing you to import CRM records and activities (contacts, companies, notes, etc.) into your HubSpot account.  After import, records are accessible and updatable via other CRM API endpoints (Contacts, Associations, Engagements APIs).  HubSpot also offers a guided import tool.


## Before You Begin

* Understand file requirements (refer to HubSpot documentation for specifics).
* Know the required properties for record/activity and marketing event participant imports.
* Use the custom events API for creating custom events or associating events with records, instead of importing.


## API Endpoints

All endpoints are under the `/crm/v3/imports` base path.  Replace `{importId}` with the ID returned after a successful import.

**1. Start an Import (POST /crm/v3/imports)**

This endpoint initiates a data import.  The request uses `multipart/form-data` and includes:

* **Headers:**
    * `Content-Type: multipart/form-data`

* **Body (form-data):**
    * `importRequest`: (text) JSON containing import details (see below).
    * `files`: (file) The import file (CSV or Spreadsheet).


**2. Get Previous Imports (GET /crm/v3/imports)**

Retrieves a list of all imports.  Add `/ {importId}` to retrieve a specific import.

**3. Cancel an Import (POST /crm/v3/imports/{importId}/cancel)**

Cancels an active import.


**4. View Import Errors (GET /crm/v3/imports/{importId}/errors)**

Retrieves error details for a specific import.


## `importRequest` JSON Structure

The `importRequest` JSON field within the POST request body dictates the import process.  Key fields include:

* `name`: (string)  Import name (displayed in HubSpot and referenced in other tools).
* `importOperations`: (object, optional) Specifies create/update behavior per object type (`0-1` for contacts, `0-2` for companies, etc.):
    * `"0-1": "CREATE"` (only creates)
    * `"0-1": "UPDATE"` (only updates)
    * `"0-1": "UPSERT"` (creates or updates - default)
* `dateFormat`: (string) Date format in the file (`MONTH_DAY_YEAR`, `DAY_MONTH_YEAR`, `YEAR_MONTH_DAY`).
* `marketableContactImport`: (boolean, optional) For contact imports with marketing contact access; `true` for marketing contacts, `false` for non-marketing.
* `createContactListFromImport`: (boolean, optional) Creates a static list of contacts from the import.
* `files`: (array)  An array of file objects (see below).


## File Object Structure within `importRequest`

Each element within the `files` array describes an import file:

* `fileName`: (string) File name (including extension).
* `fileFormat`: (string) File format (`CSV` or `SPREADSHEET`).
* `fileImportPage`: (object)  Contains column mapping information.
    * `hasHeader`: (boolean) Indicates if the file has a header row.
    * `columnMappings`: (array) Array of column mapping objects (see below).


## Column Mapping Object Structure

Each element within `columnMappings` maps a file column to a HubSpot property:

* `columnObjectTypeId`: (string) Object type ID (e.g., `0-1` for contacts, `0-2` for companies).
* `columnName`: (string) Column header name.
* `propertyName`: (string) HubSpot property internal name.  `null` for common columns in multi-file imports.
* `columnType`: (string, optional) Specifies column data type:
    * `HUBSPOT_OBJECT_ID`: HubSpot record ID.
    * `HUBSPOT_ALTERNATE_ID`: Unique identifier (e.g., email).
    * `FLEXIBLE_ASSOCIATION_LABEL`: Association labels.
    * `ASSOCIATION_KEYS`: Unique identifiers for same-object associations.
    * `STANDARD`: Default column type.
    * `EVENT_TIMESTAMP`: Timestamp for marketing event participation (requires `marketingEventSubmissionType`).
* `toColumnObjectTypeId`: (string, optional) For multi-file imports; the object type of the common column property.
* `foreignKeyType`: (object, optional) For multi-file imports; association type.
    * `associationTypeId`: (integer) Association type ID.
    * `associationCategory`: (string) Association category (`HUBSPOT_DEFINED`).
* `associationIdentifierColumn`: (boolean, optional) For multi-file imports; indicates the common column property.
* `marketingEventSubmissionType`: (string, optional) For `EVENT_TIMESTAMP` columns;  submission type (`REGISTERED`, `JOINED`, `LEFT`, `CANCELLED`).


## Import Examples

See the provided examples in the original text for single-file, multi-object, and multi-file imports.  These illustrate the JSON structures and column mappings.


## Response Codes

* **200 OK:** Successful import; includes `importId`.
* **400 Bad Request:** Invalid request parameters.
* **401 Unauthorized:** Invalid API key.
* **404 Not Found:**  Resource not found.
* **429 Too Many Requests:** Rate limit exceeded.


## Import States

* `STARTED`: Import recognized but not yet processing.
* `PROCESSING`: Import in progress.
* `DONE`: Import complete.
* `FAILED`: Import failed.
* `CANCELED`: Import canceled.
* `DEFERRED`: Import deferred due to concurrent import limits (maximum 3 concurrent imports).


## Limits

* Maximum 80,000,000 rows per day.
* Individual file limit: 1,048,576 rows or 512 MB (whichever is reached first).  Exceeding limits results in a 429 error.


## Error Handling and Troubleshooting

Refer to the original text for common errors and troubleshooting steps.  Key points include checking column headers, ensuring correct column order and mappings, and verifying the `Content-Type` header.  Duplicate headers should be avoided.
