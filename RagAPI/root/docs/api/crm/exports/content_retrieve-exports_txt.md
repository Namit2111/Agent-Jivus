# HubSpot CRM Exports API Documentation

This document describes the HubSpot CRM Exports API, allowing you to export data from your HubSpot account.  The API allows for exporting records and property data, retrieving download URLs, and checking export status.

## API Endpoints

**1. Start an Export (POST):**

`/crm/v3/exports/export/async`

This endpoint initiates an asynchronous export job.  The response includes the `id` of the export task.

**Request Method:** `POST`

**Request Body (JSON):**

The request body requires several parameters, depending on the `exportType`.  See sections below for details on `VIEW` and `LIST` exports.


**Common Parameters:**

| Parameter             | Description                                                                                                | Example                  |
|----------------------|------------------------------------------------------------------------------------------------------------|--------------------------|
| `exportType`         | `VIEW` (for views) or `LIST` (for lists)                                                                     | `"VIEW"`                  |
| `format`             | File format: `XLSX`, `CSV`, `XLS`                                                                           | `"XLSX"`                  |
| `exportName`         | Name of the export                                                                                           | `"My Contact Export"`     |
| `language`           | Language of the export file (e.g., `DE`, `EN`, `ES`, `FI`, `FR`, `IT`, `JA`, `NL`, `PL`, `PT`, `SV`) | `"EN"`                    |
| `objectType`         | Object type to export (e.g., `CONTACT`, or `objectTypeId` for custom objects)                              | `"CONTACT"`               |
| `associatedObjectType` | (Optional) Associated object type to include                                                               | `"COMPANY"`               |
| `objectProperties`    | List of properties to export                                                                                | `["email", "firstname"]` |
| `exportInternalValuesOptions` | (Optional) Array to export internal names and/or values (`NAMES`, `VALUES`)                                | `["NAMES", "VALUES"]`     |


**2. Export a View (POST - using `/crm/v3/exports/export/async`):**

For `exportType: "VIEW"`, add the following to the request body:

| Parameter            | Description                                                                                                  | Example                                      |
|-----------------------|--------------------------------------------------------------------------------------------------------------|----------------------------------------------|
| `publicCrmSearchRequest` | Object containing filters, sorts, and query parameters for refining the exported data.                       | See Example below                            |
| `publicCrmSearchRequest.filters` | Array of filter objects. Each filter object contains `propertyName`, `operator` (`EQ`, `NE`, etc.), and `value`. | `[{"propertyName": "email", "operator": "EQ", "value": "test@example.com"}]` |
| `publicCrmSearchRequest.sorts`  | Array of sort objects. Each sort object contains `propertyName` and `order` (`ASC` or `DES`).                  | `[{"propertyName": "createdAt", "order": "DES"}]` |
| `publicCrmSearchRequest.query`  | Search query string.                                                                                       | `"test"`                                      |


**3. Export a List (POST - using `/crm/v3/exports/export/async`):**

For `exportType: "LIST"`, add the following to the request body:

| Parameter | Description                                                                    | Example     |
|-----------|--------------------------------------------------------------------------------|-------------|
| `listId`  | The ILS List ID of the list to export.                                          | `1234567`  |



**4. Retrieve Export Status (GET):**

`/crm/v3/exports/export/async/tasks/{exportId}/status`

**Request Method:** `GET`

**Response (JSON):**  Contains the `status` (`COMPLETE`, `PENDING`, `PROCESSING`, `CANCELED`), and if `COMPLETE`, a download URL.  This URL expires after 5 minutes.

## Examples

**Example 1: Exporting a View of Contacts with Filters and Internal Values**

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

* Maximum 3 `filterGroups` with up to 3 `filters` each.
* Maximum 30 exports within a 24-hour rolling window, one at a time.
* CSV files larger than 2MB are automatically zipped.


## Error Handling

The API will return standard HTTP status codes to indicate success or failure.  Specific error details will be included in the response body as JSON.  Refer to the HubSpot API documentation for detailed error codes and their meanings.
