# HubSpot CRM Exports API Documentation

This document details the HubSpot CRM Exports API, allowing you to export records and property data from your HubSpot account.  You can retrieve a download URL for the export file and monitor its status.  This API complements the in-application export functionality within the HubSpot interface.

## Starting an Export

To initiate an export, send a `POST` request to `/crm/v3/exports/export/async`. The request body must specify details such as file format, objects, properties, and export type (view or list).  You can also filter data using operators.

### Request Parameters (Common to View and List Exports)

| Parameter             | Description                                                                                                                   |
|------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| `exportType`           | Export type: `VIEW` (for views from object index pages) or `LIST` (for lists).                                                   |
| `format`              | File format: `XLSX`, `CSV`, or `XLS`.                                                                                       |
| `exportName`          | Name of the export.                                                                                                         |
| `language`            | Export file language: `DE`, `EN`, `ES`, `FI`, `FR`, `IT`, `JA`, `NL`, `PL`, `PT`, or `SV`.  See supported languages for details. |
| `objectType`          | Name or ID of the object (use object name for standard objects, `objectTypeId` for custom objects – retrievable via `/crm/v3/schemas`). |
| `associatedObjectType` | Name or ID of an associated object to include (only one allowed per request).  Includes associated record IDs and display property values. |
| `objectProperties`     | List of properties to include in the export.  Defaults to human-readable labels; use `exportInternalValuesOptions` for internal names/values. |
| `exportInternalValuesOptions` | Array to include internal names (`NAMES`) and/or values (`VALUES`) for properties.                                           |


### Exporting a View

For exporting an index page view, set `exportType` to `VIEW`.  Use `publicCrmSearchRequest` to filter and sort records:

| Parameter              | Description                                                                                             |
|-------------------------|----------------------------------------------------------------------------------------------------------|
| `publicCrmSearchRequest` | Object containing:  `filters` (property/value filters), `sorts` (property sorting – `ASC` or `DES`), `query` (search string). |


**Example Request Body (View Export):**

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

### Exporting a List

For exporting a list, set `exportType` to `LIST` and include `listId`:

| Parameter | Description                                                                                                 |
|-----------|-------------------------------------------------------------------------------------------------------------|
| `listId`  | The ILS List ID (found in HubSpot under Contacts > Lists; hover over the list, click Details, then Copy List ID). |


**Example Request Body (List Export):**

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

After a successful export, the API returns an `id`.  To retrieve the export status and download URL, send a `GET` request to `/crm/v3/exports/export/async/tasks/{exportId}/status`.

Possible statuses: `COMPLETE`, `PENDING`, `PROCESSING`, `CANCELED`.  For `COMPLETE` exports, a download URL is provided (expires after 5 minutes; another `GET` request generates a new URL).

**Important Note:** Download URLs are accessible without additional authorization before expiration.  Handle these URLs securely.


## Limits

* Maximum 3 `filterGroups` with up to 3 `filters` each when setting filters.
* Up to 30 exports within a 24-hour rolling window, one at a time.  Additional exports are queued.
* CSV files larger than 2MB are automatically zipped.

