# HubSpot CRM Exports API Documentation

This document details the HubSpot CRM Exports API, allowing you to export data from your HubSpot account.  The API allows you to start exports, retrieve their status, and download the resulting files.

## API Endpoints

**1. Start an Export (POST):**

`/crm/v3/exports/export/async`

This endpoint initiates an asynchronous export job.  The response includes the `id` of the export task.

**Request Method:** `POST`

**Request Body (JSON):**  The request body depends on the `exportType` (either `VIEW` or `LIST`).  See examples below.

**Response (JSON):**

```json
{
  "id": "export_taskId" 
}
```

**Parameters (Common to both `VIEW` and `LIST` exports):**

| Parameter             | Description                                                                                             | Type      | Required | Example Value |
|------------------------|---------------------------------------------------------------------------------------------------------|-----------|----------|----------------|
| `exportType`           | `VIEW` (for views) or `LIST` (for lists)                                                              | String    | Yes       | `"VIEW"`       |
| `format`               | File format: `XLSX`, `CSV`, or `XLS`                                                                   | String    | Yes       | `"CSV"`        |
| `exportName`           | Name of the export                                                                                     | String    | Yes       | `"My Contact Export"` |
| `language`             | Language of the export file (e.g., `DE`, `EN`, `ES`, `FR`, `IT`, `JA`, `NL`, `PL`, `PT`, `SV`) | String    | Yes       | `"EN"`         |
| `objectType`           | Object type to export (e.g., `CONTACT`, `COMPANY`). For custom objects, use `objectTypeId`.          | String    | Yes       | `"CONTACT"`     |
| `associatedObjectType` | (Optional) Associated object type to include (e.g., `COMPANY`). Only one allowed.                       | String    | No        | `"COMPANY"`     |
| `objectProperties`      | List of properties to export                                                                            | Array     | Yes       | `["email", "firstname"]` |
| `exportInternalValuesOptions` | (Optional) Array of internal value options: `NAMES`, `VALUES`.  Exports internal names and/or values. | Array     | No        | `["NAMES", "VALUES"]` |


**Parameters specific to `VIEW` exports:**

| Parameter             | Description                                                                                                | Type      | Required | Example Value                |
|------------------------|------------------------------------------------------------------------------------------------------------|-----------|----------|-------------------------------|
| `publicCrmSearchRequest` | (Optional) Object containing `filters`, `sorts`, and `query` for filtering and sorting the view data.     | Object    | No        | See example below             |


**Parameters specific to `LIST` exports:**

| Parameter | Description                                                                        | Type      | Required | Example Value |
|-----------|------------------------------------------------------------------------------------|-----------|----------|----------------|
| `listId`   | HubSpot list ID to export                                                          | Integer   | Yes       | `1234567`     |


**2. Retrieve Export Status (GET):**

`/crm/v3/exports/export/async/tasks/{exportId}/status`

This endpoint retrieves the status of an export job.

**Request Method:** `GET`

**Path Parameter:**

| Parameter | Description                 | Type    |
|-----------|-----------------------------|---------|
| `exportId` | ID of the export task.     | String  |

**Response (JSON):**

```json
{
  "status": "COMPLETE",  // Or "PENDING", "PROCESSING", "CANCELED"
  "downloadUrl": "download_url" // Only present if status is "COMPLETE". Expires in 5 minutes.
}
```


## Examples

**Example 1: Exporting a View of Contacts with Associated Companies**

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

**Example 2: Exporting a List**

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


## Limits

* Maximum three `filterGroups` with up to three `filters` each when filtering view exports.
* Maximum thirty exports within a 24-hour rolling window, one at a time.
* CSV files larger than 2MB will be automatically zipped.


## Error Handling

The API returns standard HTTP status codes to indicate success or failure.  Error responses will include a JSON payload with details about the error.


This documentation provides a comprehensive overview of the HubSpot CRM Exports API. Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
