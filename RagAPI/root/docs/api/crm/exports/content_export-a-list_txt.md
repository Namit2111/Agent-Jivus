# HubSpot CRM Exports API Documentation

This document details the HubSpot CRM Exports API, allowing you to export records and property data from your HubSpot account.  You can initiate exports, retrieve download URLs, and check export status.  HubSpot also provides in-app tools for exporting records and viewing export history.


## Starting an Export

To initiate an export, send a `POST` request to `/crm/v3/exports/export/async`. The request body must specify details like file format, objects, properties, and export type (view or list).  You can also filter data using operators.

### Request Parameters

| Parameter             | Description                                                                                                                                        |
|------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| `exportType`           | Type of export: `VIEW` (from an object index page) or `LIST` (from a list).                                                                       |
| `format`               | File format: `XLSX`, `CSV`, or `XLS`.                                                                                                           |
| `exportName`           | Name of the export.                                                                                                                             |
| `language`             | Export file language: `DE`, `EN`, `ES`, `FI`, `FR`, `IT`, `JA`, `NL`, `PL`, `PT`, or `SV`. [See supported languages](LINK_TO_SUPPORTED_LANGUAGES) |
| `objectType`           | Object name or ID (use `objectTypeId` for custom objects – retrievable via `GET /crm/v3/schemas`).                                                |
| `associatedObjectType` | Associated object name or ID to include (only one allowed). Includes associated record IDs and primary display property value.                  |
| `objectProperties`     | List of properties to include.  Defaults to human-readable labels; use `exportInternalValuesOptions` for internal names/values.                 |
| `exportInternalValuesOptions` | Array to export internal property names (`NAMES`) and/or values (`VALUES`).                                                                     |


## Exporting a View

For exporting an index page view, set `exportType` to `VIEW`. Use `publicCrmSearchRequest` to filter and sort records.

### `publicCrmSearchRequest` Parameters

| Parameter | Description                                                                     |
|-----------|---------------------------------------------------------------------------------|
| `filters`  | Array of property/value filters.                                                |
| `sorts`   | Array of property sort orders (`ASC` or `DES`).                               |
| `query`    | Search string for record values.                                                |


**Example Request (View Export):**

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

For exporting a list, set `exportType` to `LIST` and specify the `listId` (ILS List ID – find it in HubSpot's Contacts > Lists).

**Example Request (List Export):**

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

After a successful export, the response contains the export `id`. Retrieve the export status via a `GET` request to `/crm/v3/exports/export/async/tasks/{exportId}/status`.  Possible statuses: `COMPLETE`, `PENDING`, `PROCESSING`, `CANCELED`.  A download URL (expires after 5 minutes) is returned for `COMPLETE` exports.

**Important Note:** Download URLs are accessible without additional authorization before expiration. Handle them cautiously.


## Limits

* Maximum three `filterGroups` with up to three `filters` each.
* Up to 30 exports within a 24-hour rolling window, one at a time.
* CSV files > 2MB are automatically zipped.

**(Remember to replace placeholders like `LINK_TO_SUPPORTED_LANGUAGES` with actual links.)**
