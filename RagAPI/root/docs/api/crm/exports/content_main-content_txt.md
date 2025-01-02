# HubSpot CRM Exports API Documentation

This document describes the HubSpot CRM Exports API, allowing you to export data from your HubSpot account.  The API allows initiating exports, retrieving their status, and downloading the exported files.  HubSpot also provides the ability to export data within the UI.


## API Endpoints

### 1. Start an Export (POST `/crm/v3/exports/export/async`)

This endpoint initiates an asynchronous export job.

**Request Method:** `POST`

**Request URL:** `/crm/v3/exports/export/async`

**Request Body (JSON):**

The request body depends on whether you're exporting a view or a list.  Common parameters include:

| Parameter             | Description                                                                                                  | Type      | Required | Example                               |
|----------------------|--------------------------------------------------------------------------------------------------------------|-----------|----------|---------------------------------------|
| `exportType`          | `VIEW` (for views) or `LIST` (for lists)                                                                    | String    | Yes       | `"VIEW"`                               |
| `format`              | File format: `XLSX`, `CSV`, or `XLS`                                                                        | String    | Yes       | `"XLSX"`                               |
| `exportName`          | Name of the export                                                                                           | String    | Yes       | `"My Contact Export"`                   |
| `language`            | Language of the export file (e.g., `DE`, `EN`, `ES`, `FI`, `FR`, `IT`, `JA`, `NL`, `PL`, `PT`, `SV`) | String    | Yes       | `"EN"`                                 |
| `objectType`          | Object type name (e.g., `CONTACT`) or ID (for custom objects). Get IDs via `/crm/v3/schemas` GET request. | String    | Yes       | `"CONTACT"`                            |
| `associatedObjectType`| Associated object type (optional, one only)                                                                 | String    | No        | `"COMPANY"`                            |
| `objectProperties`     | List of properties to export                                                                                 | Array     | Yes       | `["email", "firstname", "lastname"]` |
| `exportInternalValuesOptions` | Array to export internal names and/or values (`NAMES`, `VALUES`).                                    | Array     | No        | `["NAMES", "VALUES"]`                 |
| `listId`              | (For `exportType: LIST`) ILS List ID.  Find this in HubSpot under Contacts > Lists.                        | Integer   | Yes (if `exportType: LIST`) | `1234567`                             |
| `publicCrmSearchRequest` | (For `exportType: VIEW`) Object to filter and sort records (see below).                                  | Object    | No (if `exportType: VIEW`) |  (See Example)                       |


**`publicCrmSearchRequest` (nested object for `exportType: VIEW`):**

| Parameter | Description                                                              | Type     |
|-----------|--------------------------------------------------------------------------|----------|
| `filters` | Array of filter objects (max 3 groups, 3 filters per group)           | Array    |
| `sorts`   | Array of sort objects                                                    | Array    |
| `query`   | Search query string                                                      | String   |

Each filter object within `filters` has:

| Parameter     | Description             | Type    |
|---------------|--------------------------|---------|
| `value`       | Property value           | String  |
| `propertyName`| Property name             | String  |
| `operator`    | Operator (e.g., `EQ`, `LT`, `GT`) | String  |


Each sort object within `sorts` has:

| Parameter     | Description             | Type    |
|---------------|--------------------------|---------|
| `propertyName`| Property name             | String  |
| `order`       | `ASC` or `DES`           | String  |


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

**Response:**

On success, a JSON response containing the `id` of the export task is returned.

```json
{
  "id": "your_export_id"
}
```


### 2. Retrieve Export Status (GET `/crm/v3/exports/export/async/tasks/{exportId}/status`)

This endpoint retrieves the status of an export.

**Request Method:** `GET`

**Request URL:** `/crm/v3/exports/export/async/tasks/{exportId}/status`  (Replace `{exportId}` with the ID from the previous request)

**Response:**

The response will include the `status` (`COMPLETE`, `PENDING`, `PROCESSING`, `CANCELED`). If `status` is `COMPLETE`, a `redirectUrl` for downloading the file will be included.  This URL expires after 5 minutes.

```json
{
  "status": "COMPLETE",
  "redirectUrl": "https://your-download-url.com"
}
```


## Limits

* Maximum 3 `filterGroups`, each with up to 3 `filters`.
* Maximum 30 exports within a 24-hour rolling window, one at a time.
* CSV files larger than 2MB are automatically zipped.


## Error Handling

The API will return standard HTTP status codes to indicate success or failure.  Error responses will include details about the error.


This documentation provides a comprehensive overview of the HubSpot CRM Exports API.  Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
