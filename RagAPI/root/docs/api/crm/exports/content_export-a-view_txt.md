# HubSpot CRM Exports API Documentation

This document describes the HubSpot CRM Exports API, allowing you to export records and property data from your HubSpot account.  You can initiate exports, retrieve download URLs, and check export status.

## API Endpoints

**1. Start an Export (POST):**

`/crm/v3/exports/export/async`

This endpoint initiates an asynchronous export job. The response includes the `id` of the export task.

**Request Body (JSON):**

The request body requires several parameters depending on the `exportType`.

**Common Parameters:**

* `exportType` (string, required):  `VIEW` (for exporting a view from an object index page) or `LIST` (for exporting a list).
* `format` (string, required): `XLSX`, `CSV`, or `XLS`.
* `exportName` (string, required):  The name of the export.
* `language` (string, optional): `DE`, `EN`, `ES`, `FI`, `FR`, `IT`, `JA`, `NL`, `PL`, `PT`, or `SV`.
* `objectType` (string, required): The name or ID of the object (e.g., `CONTACT`).  For custom objects, use the `objectTypeId` (obtainable via a GET request to `/crm/v3/schemas`).
* `associatedObjectType` (string, optional): The name or ID of an associated object to include. Only one allowed per request.
* `objectProperties` (array of strings, required): A list of properties to include in the export.
* `exportInternalValuesOptions` (array of strings, optional): `NAMES` (for internal property names) and/or `VALUES` (for internal property values).


**Parameters Specific to `exportType: VIEW`:**

* `publicCrmSearchRequest` (object, optional):  Allows filtering and sorting.  Contains:
    * `filters` (array of objects):  Each object specifies a filter with `value`, `propertyName`, and `operator` (e.g., `EQ`, `NE`, `GT`, `LT`, etc.).  Maximum of three filterGroups with up to three filters each.
    * `sorts` (array of objects):  Each object specifies a sort with `propertyName` and `order` (`ASC` or `DES`).
    * `query` (string): A search query string.


**Parameters Specific to `exportType: LIST`:**

* `listId` (integer, required): The ILS List ID of the list to export.  Find this ID in HubSpot's Contacts > Lists section.


**Example Request Body (VIEW export):**

```json
{
  "exportType": "VIEW",
  "exportName": "All contacts",
  "format": "xlsx",
  "language": "DE",
  "objectType": "CONTACT",
  "exportInternalValuesOptions": ["NAMES", "VALUES"],
  "objectProperties": ["email", "firstname", "lastname"],
  "associatedObjectType": "COMPANY",
  "publicCrmSearchRequest": {
    "filters": [
      {
        "value": "hello@test.com",
        "propertyName": "email",
        "operator": "EQ"
      }
    ],
    "query": "hello",
    "sorts": [
      {
        "propertyName": "email",
        "order": "ASC"
      }
    ]
  }
}
```

**Example Request Body (LIST export):**

```json
{
  "exportType": "LIST",
  "listId": 1234567,
  "exportName": "Marketing email contacts",
  "format": "xlsx",
  "language": "EN",
  "objectType": "CONTACT",
  "objectProperties": ["email"]
}
```


**2. Retrieve Export Status (GET):**

`/crm/v3/exports/export/async/tasks/{exportId}/status`

This endpoint retrieves the status of an export using its `exportId`.

**Response Body (JSON):**

The response includes the `status` (`COMPLETE`, `PENDING`, `PROCESSING`, or `CANCELED`).  If `status` is `COMPLETE`, a download URL will be included. This URL expires after 5 minutes.

**Example Response (COMPLETE):**

```json
{
  "status": "COMPLETE",
  "downloadUrl": "https://example.com/download/your_export.xlsx" 
}
```


## Limits

* Maximum 3 `filterGroups` with up to 3 `filters` each when setting filters.
* Up to 30 exports within a 24-hour rolling window, one at a time.  Additional exports are queued.
* CSV files larger than 2MB are automatically zipped.


## Error Handling

The API will return standard HTTP status codes and error messages in the response body (JSON) to indicate errors.  Check the documentation for details on specific error codes.


## Authentication

This API requires proper authentication with HubSpot.  Refer to the HubSpot API documentation for authentication details (likely using API keys or OAuth).
