# HubSpot CRM Exports API Documentation

This document describes the HubSpot CRM Exports API, allowing you to export records and property data from your HubSpot account.  You can retrieve a download URL for the exported file or check the export status.  This API complements the ability to export records and view export logs within the HubSpot interface.

## Starting an Export

To initiate an export, send a `POST` request to `/crm/v3/exports/export/async`. The request body must specify details like file format, objects, properties, and export type (view or list).  You can also filter exported data using specific operators.

### Request Parameters (Common to View and List Exports):

| Parameter             | Description                                                                                                                                |
|----------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| `exportType`          | Export type: `VIEW` (exports a view from an object index page) or `LIST` (exports a list).                                                    |
| `format`              | File format: `XLSX`, `CSV`, or `XLS`.                                                                                                     |
| `exportName`          | Name of the export.                                                                                                                        |
| `language`            | Export file language: `DE`, `EN`, `ES`, `FI`, `FR`, `IT`, `JA`, `NL`, `PL`, `PT`, or `SV`.  See supported languages for more information. |
| `objectType`          | Name or ID of the object to export. Use the object's name (e.g., `CONTACT`) for standard objects; use `objectTypeId` for custom objects (obtainable via a `GET` request to `/crm/v3/schemas`). |
| `associatedObjectType` | Name or ID of an associated object to include. Only one associated object is allowed per request.  Includes associated record IDs and primary display property values. |
| `objectProperties`    | List of properties to include in the export.  Defaults to human-readable labels; use `exportInternalValuesOptions` for internal names/values. |
| `exportInternalValuesOptions` | Array to export internal values for property names (`NAMES`) and/or property values (`VALUES`).                                          |


## Exporting a View

For exporting an index page view, set `exportType` to `VIEW`.  Use `publicCrmSearchRequest` to filter and sort records:

### `publicCrmSearchRequest` Parameters:

| Parameter | Description                                                                   |
|-----------|-------------------------------------------------------------------------------|
| `filters`  | Array of objects defining property filters (value, propertyName, operator).  |
| `sorts`   | Array of objects defining sort order for properties (propertyName, order: `ASC` or `DES`). |
| `query`    | String to search record values.                                               |


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

## Exporting a List

For exporting a list, set `exportType` to `LIST` and include the `listId`.

### `listId` Parameter:

| Parameter | Description                                                                                                                  |
|-----------|------------------------------------------------------------------------------------------------------------------------------|
| `listId`   | The ILS List ID. Obtain this from the list details page in HubSpot (Contacts > Lists; hover over the list, click Details, then copy the ILS List ID).  |


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

After a successful export, the `id` is returned.  Retrieve the export status with a `GET` request to `/crm/v3/exports/export/async/tasks/{exportId}/status`.  Possible statuses: `COMPLETE`, `PENDING`, `PROCESSING`, `CANCELED`.  A download URL (expiring after 5 minutes) is returned for `COMPLETE` exports.  Requesting the status again generates a new URL.  **Caution:** Download URLs are accessible without authorization before expiration.


## Limits

* Maximum three `filterGroups`, each with up to three `filters`.
* Maximum thirty exports within a 24-hour rolling window; one at a time (others are queued).
* CSV files larger than 2MB are automatically zipped.

