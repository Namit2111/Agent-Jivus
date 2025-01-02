# HubSpot CRM Imports API Documentation

This document details the HubSpot CRM Imports API, allowing you to import CRM records and activities (contacts, companies, notes, etc.) into your HubSpot account.  Imported data can then be accessed and updated via other HubSpot CRM APIs.  This API complements HubSpot's guided import tool.

## API Endpoints

All endpoints are prefixed with `/crm/v3/imports`.

* **POST `/crm/v3/imports`**: Starts a new import.  Requires a `multipart/form-data` request.
* **GET `/crm/v3/imports`**: Retrieves all imports for the account (limited to imports by the private app using its access token).
* **GET `/crm/v3/imports/{importId}`**: Retrieves information for a specific import.
* **POST `/crm/v3/imports/{importId}/cancel`**: Cancels an active import.
* **GET `/crm/v3/imports/{importId}/errors`**: Retrieves errors for a specific import.


## Request Body (POST `/crm/v3/imports`)

The POST request to start an import uses `multipart/form-data` with the following fields:

* **`importRequest` (text):** A JSON object defining the import details (see below).
* **`files` (file):** The import file (CSV or Spreadsheet).

### `importRequest` JSON Structure

The `importRequest` JSON object contains the following fields:

* **`name` (string):**  The name of the import (displayed in HubSpot).
* **`importOperations` (object, optional):** Specifies create/update behavior for each object type.  Uses `objectTypeId` as keys (e.g., `"0-1": "CREATE"` for contacts).  Defaults to `UPSERT` (create and update).  Valid values: `CREATE`, `UPDATE`, `UPSERT`.
* **`dateFormat` (string, optional):** The date format in the import file. Defaults to `MONTH_DAY_YEAR`.  Options: `DAY_MONTH_YEAR`, `YEAR_MONTH_DAY`.
* **`marketableContactImport` (boolean, optional):** For contact imports, sets marketing contact status (only for accounts with marketing contacts access). `true` for marketing contacts, `false` for non-marketing.
* **`createContactListFromImport` (boolean, optional):** Creates a static list of contacts from the import. `true` to create a list.
* **`files` (array):** An array of file objects (even for single-file imports). Each object contains:
    * **`fileName` (string):** The name of the file (including extension).
    * **`fileFormat` (string):**  `"CSV"` or `"SPREADSHEET"`.
    * **`fileImportPage` (object):** Contains column mapping information.
        * **`hasHeader` (boolean):** Indicates if the file has a header row.
        * **`columnMappings` (array):**  An array of column mapping objects (see below).


### Column Mapping Object

Each element in the `columnMappings` array maps a column in your import file to a HubSpot property. It contains:

* **`columnObjectTypeId` (string):** The `objectTypeId` of the object the column belongs to (e.g., `"0-1"` for contacts).
* **`columnName` (string):** The name of the column header.
* **`propertyName` (string):** The internal name of the HubSpot property.  `null` for common columns in multi-file imports.
* **`columnType` (string, optional):** Specifies the column's data type.  Options: `HUBSPOT_OBJECT_ID`, `HUBSPOT_ALTERNATE_ID`, `FLEXIBLE_ASSOCIATION_LABEL`, `ASSOCIATION_KEYS`, `STANDARD`, `EVENT_TIMESTAMP`.
* **`toColumnObjectTypeId` (string, optional):** For multi-file imports, the `objectTypeId` of the object the common column property belongs to (in the file where it *doesn't* belong).
* **`foreignKeyType` (object, optional):** For multi-file imports, defines the association type ( `associationTypeId` and `associationCategory`).
* **`associationIdentifierColumn` (boolean, optional):** For multi-file imports, indicates if the column is the identifier for associations (only for the object where the property belongs).



## Response (POST `/crm/v3/imports`)

On success, the response will contain an `importId`.  This `importId` can be used to retrieve import status and errors.

## Import States

* `STARTED`: Import recognized but not yet processing.
* `PROCESSING`: Import is actively processing.
* `DONE`: Import completed successfully.
* `FAILED`: Import failed due to an error.
* `CANCELED`: Import was canceled by the user.
* `DEFERRED`: Import is delayed because the maximum number of concurrent imports (3) is reached.


## Examples

See the provided text for numerous JSON examples illustrating single-file, multi-file, and multi-object imports with various configurations.


## Error Handling

The API will return appropriate HTTP error codes (e.g., 429 for rate limiting, 400 for bad requests).  The `/crm/v3/imports/{importId}/errors` endpoint provides details on import errors.  Common errors include incorrect column numbers and mismatched column order.


## Limits

* **Daily Row Limit:** 80,000,000 rows per day.
* **File Size/Row Limit:** 1,048,576 rows or 512 MB, whichever is reached first.


This documentation provides a comprehensive overview of the HubSpot CRM Imports API. Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
