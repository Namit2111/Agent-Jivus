# HubSpot CRM Imports API Documentation

This document details the HubSpot CRM Imports API, allowing you to import data into your HubSpot account.  It covers various import scenarios, error handling, and API limits.


## API Endpoints

All endpoints are under the base URL: `/crm/v3/imports`

* **POST `/crm/v3/imports`**: Starts a new import.  Requires a `multipart/form-data` request.
* **GET `/crm/v3/imports`**: Retrieves a list of all imports. Supports paging and limiting.
* **GET `/crm/v3/imports/{importId}`**: Retrieves details for a specific import using its `importId`.
* **POST `/crm/v3/imports/{importId}/cancel`**: Cancels an active import.
* **GET `/crm/v3/imports/{importId}/errors`**: Retrieves errors for a specific import.


## Request Body (POST `/crm/v3/imports`)

The POST request to start an import uses `multipart/form-data` and contains:

* **`importRequest` (text):** A JSON object defining import details (see below).
* **`files` (file):** The import file itself (CSV or Spreadsheet).


### `importRequest` JSON Structure

The `importRequest` JSON object contains the following fields:

* **`name` (string):**  The name of the import (displayed in HubSpot).  *Example: "November Marketing Event Leads"*
* **`importOperations` (object, optional):** Specifies create/update behavior for each object type.  Key format:  `"objectTypeId": "operation"` where `operation` can be `CREATE`, `UPDATE`, or `UPSERT` (default).  *Example: `{"0-1": "CREATE"}` (creates contacts only)*
* **`dateFormat` (string, optional):** Date format in the file. Defaults to `MONTH_DAY_YEAR`. Options: `DAY_MONTH_YEAR`, `YEAR_MONTH_DAY`. *Example: `"DAY_MONTH_YEAR"`*
* **`marketableContactImport` (boolean, optional):** For contact imports, sets marketing status (only for accounts with marketing contacts access). `true` for marketing contacts, `false` for non-marketing.
* **`createContactListFromImport` (boolean, optional):** Creates a static list of contacts from the import. `true` to create a list.
* **`files` (array):** An array of file objects (see below).  Usually only one element for single-file imports.
    * **`fileName` (string):** The name of the file. *Example: "Nov-event-leads.csv"*
    * **`fileFormat` (string):**  `CSV` or `SPREADSHEET`. *Example: `"CSV"`*
    * **`fileImportPage` (object):** Contains column mapping information.
        * **`hasHeader` (boolean):** Indicates if the file has a header row. *Example: `true`*
        * **`columnMappings` (array):** An array of column mapping objects (see below).


### Column Mapping Objects

Each object in the `columnMappings` array maps a column in the import file to a HubSpot property.  Fields include:

* **`columnObjectTypeId` (string):** The `objectTypeId` of the object the column belongs to.  (See HubSpot documentation for a list of `objectTypeId`s).
* **`columnName` (string):** The name of the column in the import file.
* **`propertyName` (string):** The internal name of the HubSpot property.  `null` for common columns in multi-file imports.
* **`columnType` (string, optional):** Specifies the column's data type: `STANDARD`, `HUBSPOT_OBJECT_ID`, `HUBSPOT_ALTERNATE_ID`, `FLEXIBLE_ASSOCIATION_LABEL`, `ASSOCIATION_KEYS`, `EVENT_TIMESTAMP`.
* **`toColumnObjectTypeId` (string, optional):** For multi-file imports, the `objectTypeId` of the object the common column property belongs to.
* **`foreignKeyType` (object, optional):** For multi-file imports, the type of association.  Contains `associationTypeId` and `associationCategory`.
* **`associationIdentifierColumn` (boolean, optional):** For multi-file imports, indicates if the column is the identifier for association.


## Import Examples

Several examples are provided in the original text illustrating single-file, single-object; single-file, multi-object; and multi-file imports.  Refer to the original text for these detailed JSON examples.


## Response Codes

* **200 OK**: Successful import started.  Includes `importId`.
* **400 Bad Request**: Invalid request data.
* **401 Unauthorized**: Invalid API key.
* **429 Too Many Requests**: Rate limit exceeded.
* **500 Internal Server Error**: Server-side error.


## Error Handling

The `/crm/v3/imports/{importId}/errors` endpoint provides details on import failures. Common errors include incorrect column counts, parsing issues, and mismatched headers.


## Rate Limits

The API has a daily limit of 80,000,000 rows and a per-file limit of 1,048,576 rows or 512 MB.  Exceeding these limits results in a 429 error.


##  Authentication

Use your HubSpot API key in the request header.  Private app access tokens will only return imports created by that app.


This documentation provides a comprehensive overview of the HubSpot CRM Imports API.  Always refer to the official HubSpot API documentation for the most up-to-date information and details.
