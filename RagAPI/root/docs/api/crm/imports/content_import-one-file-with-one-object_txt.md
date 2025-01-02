# HubSpot CRM API Imports Documentation

This document details the HubSpot CRM API's import functionality, allowing you to import CRM records and activities (contacts, companies, notes, etc.) into your HubSpot account.  After import, records can be accessed and updated via other CRM API endpoints (Contacts API, Associations API, Engagements APIs).  Alternatively, HubSpot's guided import tool offers a user interface for imports.

## Before You Begin

* Understand file requirements (documented separately).
* Know the required properties for record and activity imports (documented separately).
* Know the required properties for marketing event participant imports (documented separately).
* **Note:** Use the custom events API for creating custom events or associating events with records, not imports.


## API Endpoints

**1. Start an Import (POST):**

`/crm/v3/imports`

This endpoint initiates an import.  The request uses `multipart/form-data` and includes two fields:

* `importRequest`: (text) JSON data specifying import details (see below).
* `files`: (file) The import file itself (CSV or Spreadsheet).


**2. Get Previous Imports (GET):**

`/crm/v3/imports/` (All imports)
`/crm/v3/imports/{importId}` (Specific import)

Retrieves information about past imports.  The response includes import name, source, format, language, date format, column mappings, and state.  States include: `STARTED`, `PROCESSING`, `DONE`, `FAILED`, `CANCELED`, `DEFERRED`.  Paging and limiting are supported (see reference documentation).  Private app access tokens only return imports performed by that app.

**3. Cancel an Import (POST):**

`/crm/v3/imports/{importId}/cancel`

Cancels an active import.


**4. View Import Errors (GET):**

`/crm/v3/imports/{importId}/errors`

Retrieves error details for a failed import.


## `importRequest` JSON Data Structure

The `importRequest` JSON data dictates how your file maps to HubSpot properties. Key fields include:

* `name`: (string) Import name (displayed in HubSpot).
* `importOperations`: (object, optional) Specifies create/update behavior for each object type (`objectTypeId`).  Keys are `objectTypeId` (e.g., `"0-1"` for contacts), values are `"CREATE"`, `"UPDATE"`, or `"UPSERT"` (default).  Example: `{"0-1": "CREATE"}`.
* `dateFormat`: (string) Date format in the file (`MONTH_DAY_YEAR`, `DAY_MONTH_YEAR`, `YEAR_MONTH_DAY`; defaults to `MONTH_DAY_YEAR`).
* `marketableContactImport`: (boolean, optional) For contacts, sets marketing status (only for accounts with marketing contacts access). `true` for marketing contacts, `false` for non-marketing.
* `createContactListFromImport`: (boolean, optional) Creates a static list from imported contacts. `true` to create a list.
* `files`: (array)  An array containing details for each file (see below).


### File Details within `files` array:

* `fileName`: (string) File name (including extension).
* `fileFormat`: (string)  `"CSV"` or `"SPREADSHEET"`.
* `fileImportPage`: (object) Contains the `columnMappings` array.
    * `hasHeader`: (boolean) `true` if the file has a header row.
    * `columnMappings`: (array)  An array of column mappings (see below).



### Column Mappings within `columnMappings` array:

* `columnObjectTypeId`: (string) Object type ID (e.g., `"0-1"` for contacts).
* `columnName`: (string) Column header name.
* `propertyName`: (string) HubSpot property name.  `null` for common columns in multi-file imports.
* `columnType`: (string) Column data type.
    * `HUBSPOT_OBJECT_ID`: HubSpot record ID.
    * `HUBSPOT_ALTERNATE_ID`: Unique identifier (e.g., email).
    * `FLEXIBLE_ASSOCIATION_LABEL`: Association label (for associating different object types).
    * `ASSOCIATION_KEYS`: Unique identifiers for same-object associations.
    * `STANDARD`: Standard column type.
    * `EVENT_TIMESTAMP`: For marketing event timestamps.
* `toColumnObjectTypeId`: (string, optional) For multi-file imports, the object type ID of the object the common column relates to.
* `foreignKeyType`: (object, optional) For multi-file imports, defines association type (`associationTypeId` and `associationCategory`).
* `associationIdentifierColumn`: (boolean, optional) `true` if this column is used for association in multi-file imports.
* `marketingEventSubmissionType`: (string, optional) For Marketing Events, sets the submission type.



## Examples

See the original text for numerous examples of `importRequest` JSON for single-file, multi-object, and multi-file imports.


## Limits

* 80,000,000 rows per day.
* Individual files: 1,048,576 rows or 512 MB, whichever is reached first.  Exceeding these limits results in a 429 HTTP error.  Split large imports into smaller requests.


## Error Handling

Examine the `/crm/v3/imports/{importId}/errors` endpoint for details on import failures.  Common errors include incorrect column counts or parsing issues.  Ensure column headers match the `columnMappings` exactly, and that the file name in the request matches the actual file name.  Check for duplicate `Content-Type` headers.


## Response Codes

* **200 OK:** Successful import initiation.  The response includes an `importId`.
* **400 Bad Request:** Invalid request data.
* **429 Too Many Requests:** Rate limit exceeded.
* **500 Internal Server Error:** Server-side error.


This documentation provides a comprehensive overview of HubSpot's CRM API import functionality. Refer to the HubSpot Developer documentation for more detailed information and the most up-to-date specifications.
