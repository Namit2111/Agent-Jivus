# HubSpot CRM Exports API Documentation

This document details the HubSpot CRM Exports API, allowing you to export records and property data from your HubSpot account.  You can retrieve download URLs for export files and check export status.  HubSpot also provides a user interface for exporting records and viewing export logs.


## Starting an Export

To initiate an export, send a `POST` request to `/crm/v3/exports/export/async`. The request body must specify details like file format, objects and properties to export, and export type (view or list).  You can filter data using operators.

### Request Parameters (for both VIEW and LIST exports):

| Parameter             | Description                                                                                                                                 |
|------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| `exportType`           | Export type: `VIEW` (exports a view from an object index page) or `LIST` (exports a list).                                                       |
| `format`               | File format: `XLSX`, `CSV`, or `XLS`.                                                                                                    |
| `exportName`           | Name of the export.                                                                                                                        |
| `language`             | Export file language: `DE`, `EN`, `ES`, `FI`, `FR`, `IT`, `JA`, `NL`, `PL`, `PT`, or `SV`.  See documentation for supported languages. |
| `objectType`           | Name or ID of the object to export. Use object name (e.g., `CONTACT`) for standard objects; use `objectTypeId` for custom objects (obtain via a `GET` request to `/crm/v3/schemas`). |
| `associatedObjectType` | Name or ID of an associated object to include. Only one associated object is allowed per request.  Includes associated record IDs and primary display property value. |
| `objectProperties`     | List of properties to include.  Defaults to human-readable labels; use `exportInternalValuesOptions` for internal names/values.           |
| `exportInternalValuesOptions` | Array to export internal values for property names (`NAMES`) and/or property values (`VALUES`).                                         |


## Exporting a View

For exporting an index page view, set `exportType` to `VIEW`.  Use `publicCrmSearchRequest` to filter and sort records:

### `publicCrmSearchRequest` Parameters:

| Parameter | Description                                         |
|-----------|-----------------------------------------------------|
| `filters`  | Properties and values to filter records by.          |
| `sorts`   | Sort order (`ASC` or `DES`).                        |
| `query`    | String to search records' values for.                |


**Example Request Body (JSON):**

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


## Exporting a List

For exporting a list, set `exportType` to `LIST` and specify the list ID:

### Request Parameters:

| Parameter | Description                                                                                                        |
|-----------|--------------------------------------------------------------------------------------------------------------------|
| `listId`   | The ILS List ID of the list to export (found in HubSpot's Contact > Lists section; use the ILS List ID, not the other ID). |


**Example Request Body (JSON):**

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


## Retrieving Exports

After a successful export, the response includes the export `id`.  Retrieve the export using a `GET` request to `/crm/v3/exports/export/async/tasks/{exportId}/status`.

The response includes the export status (`COMPLETE`, `PENDING`, `PROCESSING`, or `CANCELED`).  For `COMPLETE` status, a download URL is provided (expires after 5 minutes; a new URL can be generated via another `GET` request).  **Caution:** The download URL is accessible without additional authorization before expiration.


## Limits

* Maximum three `filterGroups` with up to three `filters` each when setting filters.
* Up to thirty exports within a 24-hour rolling window, one at a time (additional exports are queued).
* CSV files larger than 2MB are automatically zipped.

