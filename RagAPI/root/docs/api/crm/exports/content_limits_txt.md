# HubSpot CRM Exports API Documentation

This document details the HubSpot CRM Exports API, allowing you to export data from your HubSpot account.  It covers starting exports, retrieving their status, and understanding associated limits.

## API Endpoints

### 1. Start an Export (POST)

**Endpoint:** `/crm/v3/exports/export/async`

This endpoint initiates an asynchronous export job.  The response includes the `id` of the export task.

**Request Body (JSON):**

The request body requires several parameters, depending on the export type (VIEW or LIST).

**Common Parameters:**

| Parameter             | Description                                                                                                        | Type     | Example             |
|----------------------|--------------------------------------------------------------------------------------------------------------------|----------|----------------------|
| `exportType`          | `VIEW` (for exporting a view) or `LIST` (for exporting a list).                                                    | String   | `"VIEW"`             |
| `format`              | File format: `XLSX`, `CSV`, or `XLS`.                                                                            | String   | `"CSV"`              |
| `exportName`          | Name of the export.                                                                                             | String   | `"My Contact Export"` |
| `language`            | Language of the export file (e.g., `DE`, `EN`, `ES`). See documentation for supported languages.                   | String   | `"EN"`               |
| `objectType`          | Object type to export (e.g., `CONTACT`). Use `objectTypeId` for custom objects (obtainable via `/crm/v3/schemas`). | String   | `"CONTACT"`           |
| `objectProperties`    | List of properties to include.                                                                                   | Array    | `["email", "name"]`   |
| `associatedObjectType` | (Optional) Associated object to include (e.g., `COMPANY`). Only one allowed per request.                        | String   | `"COMPANY"`           |
| `exportInternalValuesOptions` | (Optional) Array including `NAMES` and/or `VALUES` to export internal property names and values.             | Array    | `["NAMES", "VALUES"]` |


**VIEW Export Specific Parameter:**

| Parameter             | Description                                                                                                                               | Type     | Example                                       |
|----------------------|------------------------------------------------------------------------------------------------------------------------------------------|----------|---------------------------------------------------|
| `publicCrmSearchRequest` | Object containing filters, sorts, and query for refining the exported data. See example below.                                             | Object   | See Example                                      |
| `publicCrmSearchRequest.filters` | Array of filter objects, each with `value`, `propertyName`, and `operator` (e.g., `EQ`, `NE`, `LT`, `GT`, `LTE`, `GTE`, `CONTAINS`). | Array    | `[{ "value": "test@example.com", "propertyName": "email", "operator": "EQ" }]` |
| `publicCrmSearchRequest.sorts`  | Array of sort objects, each with `propertyName` and `order` (`ASC` or `DES`).                                                        | Array    | `[{ "propertyName": "createdAt", "order": "DESC" }]` |
| `publicCrmSearchRequest.query`   | Search query string.                                                                                                                     | String   | `"test"`                                         |


**LIST Export Specific Parameter:**

| Parameter | Description                                                                    | Type     | Example    |
|-----------|--------------------------------------------------------------------------------|----------|------------|
| `listId`  | The ILS List ID of the list to export.                                          | Integer  | `1234567` |


**Example Request Body (VIEW Export):**

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

**Example Request Body (LIST Export):**

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


**Response (JSON):**

```json
{
  "id": "exportTaskId123"
}
```


### 2. Retrieve Export Status (GET)

**Endpoint:** `/crm/v3/exports/export/async/tasks/{exportId}/status`

Retrieves the status of an export.  Replace `{exportId}` with the ID returned from the POST request.

**Response (JSON):**

```json
{
  "status": "COMPLETE",  // Or "PENDING", "PROCESSING", "CANCELED"
  "downloadUrl": "https://example.com/export.csv" // Only present if status is "COMPLETE". Expires after 5 minutes.
}
```


## Limits

* Maximum of three `filterGroups` with up to three `filters` each.
* Maximum of thirty exports within a 24-hour rolling window; only one can run concurrently.
* CSV files larger than 2MB are automatically zipped.


## Error Handling

The API will return appropriate HTTP status codes and error messages in the response body to indicate failures.  Consult the HubSpot API documentation for detailed error codes and their meanings.


This documentation provides a comprehensive overview of the HubSpot CRM Exports API.  Remember to consult the official HubSpot API documentation for the most up-to-date information and detailed specifications.
