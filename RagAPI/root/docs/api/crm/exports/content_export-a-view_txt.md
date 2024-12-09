# HubSpot CRM Exports API Documentation

This document details the HubSpot CRM Exports API, allowing you to export data from your HubSpot account.  It covers starting an export, retrieving its status, and understanding the API's limitations.  You can also export records and view a log of past exports within the HubSpot UI.

## Starting an Export

To initiate an export, send a `POST` request to `/crm/v3/exports/export/async`.  The request body must specify details such as file format, objects, properties, and export type (view or list).  You can also filter and sort data using various parameters.

### Request Parameters

| Parameter             | Description                                                                                                                                                                                  | Example Value(s) |
|----------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|
| `exportType`          | Type of export: `VIEW` (for object index page views) or `LIST` (for lists).                                                                                                                     | `VIEW`, `LIST`     |
| `format`              | File format: `XLSX`, `CSV`, or `XLS`.                                                                                                                                                       | `XLSX`, `CSV`, `XLS` |
| `exportName`          | Name of the export.                                                                                                                                                                       | "All contacts"   |
| `language`            | Export file language: `DE`, `EN`, `ES`, `FI`, `FR`, `IT`, `JA`, `NL`, `PL`, `PT`, or `SV`.                                                                                         | `EN`             |
| `objectType`          | Object name or ID (use `objectTypeId` for custom objects).  Retrieve `objectTypeId` via a `GET` request to `/crm/v3/schemas`.                                                              | `CONTACT`        |
| `associatedObjectType` | Associated object name or ID to include (one only).  The export will include associated record IDs and primary display property values.                                                       | `COMPANY`        |
| `objectProperties`     | List of properties to include.  Default is human-readable labels; use `exportInternalValuesOptions` for internal names/values.                                                       | `["email", "firstname"]` |
| `exportInternalValuesOptions` | Array to export internal names (`NAMES`) and/or values (`VALUES`) for properties.                                                                                                       | `["NAMES", "VALUES"]` |
| `publicCrmSearchRequest` | (For `exportType: VIEW`) Object containing filters, sorts, and a query to filter and sort exported records.                                                                               | See Example       |
| `listId`              | (For `exportType: LIST`) The ILS List ID of the list to export. Find this ID in HubSpot under Contacts > Lists > [List Details] > Copy List ID (ILS List ID). | `1234567`        |


#### `publicCrmSearchRequest` Parameters (Used only with `exportType: VIEW`)

| Parameter  | Description                                                                        | Example Value(s) |
|------------|------------------------------------------------------------------------------------|-----------------|
| `filters`   | Array of filters, each with `value`, `propertyName`, and `operator` (e.g., `EQ`). | See Example       |
| `sorts`    | Array of sorts, each with `propertyName` and `order` (`ASC` or `DES`).             | See Example       |
| `query`    | String to search records' values for.                                              | "hello"          |


## Exporting a View

For exporting a view from an index page, set `exportType` to `VIEW` and use `publicCrmSearchRequest` to filter and sort data as needed.

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

For exporting a list, set `exportType` to `LIST` and provide the `listId` (ILS List ID).

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

After initiating an export, the response will include an `id`. To check the status, send a `GET` request to `/crm/v3/exports/export/async/tasks/{exportId}/status`.  Possible statuses are `COMPLETE`, `PENDING`, `PROCESSING`, and `CANCELED`.  A `COMPLETE` status returns a download URL (expires after 5 minutes).

## Limits

* Maximum 3 `filterGroups` with up to 3 `filters` each.
* Up to 30 exports within a 24-hour rolling window, one at a time.
* CSV files larger than 2MB are automatically zipped.


## Note on Download URL Security

Download URLs expire after 5 minutes and are accessible without additional authorization before expiration. Exercise caution when sharing URLs or integrating with this API.
