# HubSpot CRM Exports API Documentation

This document describes the HubSpot CRM Exports API, allowing you to export data from your HubSpot account.  You can also export records and view a log of past exports within the HubSpot interface.

## Starting an Export

To initiate an export, send a `POST` request to `/crm/v3/exports/export/async`. The request body should contain details such as file format, objects and properties to export, and the export type (view or list).  You can also filter data using specific operators.

### Request Parameters

| Parameter                | Description                                                                                                                                                  |
|-------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `exportType`             | Type of export: `VIEW` (for views from object index pages) or `LIST` (for lists).                                                                              |
| `format`                 | File format: `XLSX`, `CSV`, or `XLS`.                                                                                                                          |
| `exportName`             | Name of the export.                                                                                                                                         |
| `language`               | Language of the export file: `DE`, `EN`, `ES`, `FI`, `FR`, `IT`, `JA`, `NL`, `PL`, `PT`, or `SV`.  See [supported languages](link-to-supported-languages-here) for details. |
| `objectType`             | Name or ID of the object to export. Use the object's name (e.g., `CONTACT`) for standard objects; use `objectTypeId` for custom objects (obtainable via a `GET` request to `/crm/v3/schemas`). |
| `associatedObjectType`   | Name or ID of an associated object to include. Only one associated object is allowed per request.  Includes associated record IDs and primary display property value. |
| `objectProperties`       | List of properties to include.  Defaults to human-readable labels; use `exportInternalValuesOptions` for internal names/values.                              |
| `exportInternalValuesOptions` | Array to export internal values for property names (`NAMES`) and/or property values (`VALUES`).                                                              |


## Exporting a View

For exporting an index page view, set `exportType` to `VIEW`.  Use `publicCrmSearchRequest` to filter and sort records.

### `publicCrmSearchRequest` Parameters

| Parameter  | Description                                                              |
|-------------|--------------------------------------------------------------------------|
| `filters`   | Properties and property values to filter records by.                      |
| `sorts`     | Sort order (`ASC` or `DES`).                                              |
| `query`     | String to search records' values for.                                    |


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

For exporting a list, set `exportType` to `LIST` and specify the `listId` (the ILS List ID, found in HubSpot under *Contacts* > *Lists* > *Details*).

### Request Parameters (List Export)

| Parameter | Description                                                                                                |
|------------|------------------------------------------------------------------------------------------------------------|
| `listId`    | The ILS List ID of the list to export.                                                                    |


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

After a successful export, the `id` is returned in the response.  Retrieve the export status with a `GET` request to `/crm/v3/exports/export/async/tasks/{exportId}/status`.

Possible statuses: `COMPLETE`, `PENDING`, `PROCESSING`, `CANCELED`.  A download URL (valid for 5 minutes) is provided for `COMPLETE` exports.


## Limits

* Maximum 3 `filterGroups` with up to 3 `filters` each.
* Maximum 30 exports within a 24-hour rolling window; one at a time (others are queued).
* CSV files larger than 2MB are automatically zipped.


## Security Note

Download URLs for completed exports are accessible without additional authorization before expiration.  Exercise caution when sharing URLs or integrating via this API.
