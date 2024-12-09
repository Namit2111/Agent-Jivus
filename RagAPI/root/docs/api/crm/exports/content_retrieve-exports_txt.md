# HubSpot CRM Exports API Documentation

This document details the HubSpot CRM Exports API, allowing you to export records and property data from your HubSpot account.  You can retrieve download URLs for export files and monitor export status.  This API complements the in-HubSpot export functionality.


## Starting an Export

To initiate an export, send a `POST` request to `/crm/v3/exports/export/async`.  The request body must specify details like file format, objects, properties, and export type (view or list). You can also filter exported data using operators.


### Request Parameters

| Parameter                | Description                                                                                                                                 |
|-------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| `exportType`             | Export type: `VIEW` (for object index page views) or `LIST` (for lists).                                                                     |
| `format`                 | File format: `XLSX`, `CSV`, or `XLS`.                                                                                                      |
| `exportName`             | Name of the export.                                                                                                                          |
| `language`               | Export file language: `DE`, `EN`, `ES`, `FI`, `FR`, `IT`, `JA`, `NL`, `PL`, `PT`, or `SV`.  See supported languages for more details. |
| `objectType`             | Object name or ID (use `objectTypeId` for custom objects; retrieve using a `GET` request to `/crm/v3/schemas`).                               |
| `associatedObjectType`   | Associated object name or ID (only one allowed per request).  Includes associated record IDs and primary display property values.          |
| `objectProperties`       | List of properties to include.  Default is human-readable labels; use `exportInternalValuesOptions` for internal names/values.          |
| `exportInternalValuesOptions` | Array: `NAMES` (for internal property names), `VALUES` (for internal property values), or both.                                            |
| `publicCrmSearchRequest` | (For `VIEW` exports only) Object containing filters, sorts, and query parameters for refining exported data.                             |
    * `filters`: Array of filter objects (up to three `filterGroups` with three `filters` each).  Each filter object requires `value`, `propertyName`, and `operator`.
    * `sorts`: Array of sort objects. Each sort object requires `propertyName` and `order` (`ASC` or `DES`).
    * `query`: Search string.


### Example Request Body (View Export)

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

### Example Request Body (List Export)

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
Note:  The `listId` is the ILS List ID, found in HubSpot under Contacts > Lists.


## Retrieving Exports

After a successful export, the API returns an `id`.  Retrieve export status using a `GET` request to `/crm/v3/exports/export/async/tasks/{exportId}/status`.

Possible statuses: `COMPLETE`, `PENDING`, `PROCESSING`, `CANCELED`.  A `COMPLETE` status includes a download URL (expires after 5 minutes).


## Limits

* Maximum of three `filterGroups` (each with up to three `filters`) for export filtering.
* Up to 30 exports within a 24-hour rolling window, one at a time.  Additional exports are queued.
* CSV files larger than 2MB are automatically zipped.


## Security Note

Download URLs for completed exports are accessible without additional authorization before expiration.  Exercise caution when sharing these URLs or integrating via this API.
