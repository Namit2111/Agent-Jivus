# HubSpot CRM API Imports Documentation

This document details the HubSpot CRM API for importing data.  It covers initiating imports, formatting the request data, mapping columns to properties, handling various import scenarios, retrieving import status, canceling imports, troubleshooting errors, and API limits.

## API Endpoints

The primary endpoints for the HubSpot CRM Imports API are:

* **POST `/crm/v3/imports`**: Starts a new import job.  This is a `multipart/form-data` request.
* **GET `/crm/v3/imports`**: Retrieves a list of all imports (paginated).  Uses `private app access token` for private app imports only.
* **GET `/crm/v3/imports/{importId}`**: Retrieves details of a specific import using its `importId`.
* **POST `/crm/v3/imports/{importId}/cancel`**: Cancels a running import.
* **GET `/crm/v3/imports/{importId}/errors`**: Retrieves error details for a specific import.


## Request Body (POST `/crm/v3/imports`)

The `POST /crm/v3/imports` request uses `multipart/form-data`.  It consists of two parts:

* `importRequest`: A JSON string containing the import configuration.
* `files`: The import file itself (CSV or Spreadsheet).


### `importRequest` JSON Structure

The `importRequest` JSON has the following fields:

* `name` (string, required):  The name of the import (displayed in HubSpot).
* `importOperations` (object, optional): Specifies the import operation type for each object type.  Key format:  `{objectTypeId}-{activityTypeId}: operation`.  Values: `"CREATE"`, `"UPDATE"`, `"UPSERT"` (default). Example: `{"0-1": "CREATE"}` (creates contacts).
* `dateFormat` (string, optional): Date format in the import file. Options: `"MONTH_DAY_YEAR"` (default), `"DAY_MONTH_YEAR"`, `"YEAR_MONTH_DAY"`.
* `marketableContactImport` (boolean, optional):  For contact imports only, sets contacts as marketing contacts (requires marketing access). `true` or `false`.
* `createContactListFromImport` (boolean, optional): Creates a static list from imported contacts. `true` or `false`.
* `files` (array, required): An array containing file information (see below).


### `files` Array Structure

The `files` array contains objects, one per file in the import:

* `fileName` (string, required): The filename (including extension).
* `fileFormat` (string, required): `"CSV"` or `"SPREADSHEET"`.
* `fileImportPage` (object, required): Contains column mapping details.
    * `hasHeader` (boolean, required): `true` if the file has a header row.
    * `columnMappings` (array, required): An array of column mapping objects (see below).


### `columnMappings` Array Structure

Each object in the `columnMappings` array maps a column to a HubSpot property:

* `columnObjectTypeId` (string, required): The `objectTypeId` of the object (e.g., `"0-1"` for contacts).
* `columnName` (string, required): The column header name.
* `propertyName` (string, required): The internal name of the HubSpot property.  For common columns in multi-file imports, set to `null`.
* `columnType` (string, optional): Specifies the column data type. Options: `"HUBSPOT_OBJECT_ID"`, `"HUBSPOT_ALTERNATE_ID"`, `"FLEXIBLE_ASSOCIATION_LABEL"`, `"ASSOCIATION_KEYS"`, `"STANDARD"`, `"EVENT_TIMESTAMP"`.
* `toColumnObjectTypeId` (string, optional): For multi-file imports, the `objectTypeId` of the related object for common columns.
* `foreignKeyType` (object, optional): For multi-file imports, the association type.  Contains `associationTypeId` and `associationCategory`.
* `associationIdentifierColumn` (boolean, optional): For multi-file imports, indicates if the column is the association identifier (`true` or `false`).
* `marketingEventSubmissionType` (string, optional): For marketing event participant imports, specifies the event submission type (e.g., `"REGISTERED"`, `"JOINED"`, `"LEFT"`, `"CANCELLED"`).


## Import Scenarios & Examples

The provided text includes detailed JSON examples for:

* Importing one file with one object type (contacts).
* Importing one file with multiple object types (contacts and marketing event participants).
* Importing one file with multiple objects and association labels.
* Importing multiple files with associations (contacts and companies).

These examples are thorough and should be examined carefully within the context of their respective sections within the original document.


## Response Codes

* **200 OK**: Successful import initiation.  Includes the `importId`.
* **400 Bad Request**: Invalid request parameters.
* **401 Unauthorized**:  Authentication failure.
* **403 Forbidden**: Insufficient permissions.
* **404 Not Found**: Resource not found.
* **429 Too Many Requests**: Rate limit exceeded.


## Error Handling and Troubleshooting

The API provides an endpoint (`/crm/v3/imports/{importId}/errors`) to retrieve error details for failed imports.  Common errors include incorrect column counts, parsing errors, and mismatched column mappings.  The documentation thoroughly explains how to debug these issues.

## API Limits

The API has limits on the number of rows per day (80,000,000) and the size of individual files (1,048,576 rows or 512 MB).  Exceeding these limits results in a `429` error.  Large imports should be split into smaller batches.


This Markdown documentation summarizes the key aspects of the HubSpot CRM Imports API. Remember to consult the original HubSpot documentation for the most up-to-date information and detailed specifications.
