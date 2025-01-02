# HubSpot CRM Exports API Documentation

This document details the HubSpot CRM Exports API, allowing you to export data from your HubSpot account.  It covers starting exports, retrieving their status, and understanding limitations.

## API Endpoints

**1. Start an Export (POST):**

`/crm/v3/exports/export/async`

This endpoint initiates an asynchronous export job.  The response includes the `id` of the export task.

**Request Body (JSON):**

The request body depends on whether you're exporting a view or a list.  Common parameters include:

| Parameter             | Description                                                                                                         | Type      | Example                |
|------------------------|---------------------------------------------------------------------------------------------------------------------|-----------|-------------------------|
| `exportType`           | Type of export (`VIEW` or `LIST`)                                                                                 | String    | `"VIEW"`                |
| `format`              | File format (`XLSX`, `CSV`, `XLS`)                                                                                  | String    | `"XLSX"`                |
| `exportName`           | Name of the export                                                                                                 | String    | `"My Contact Export"`   |
| `language`            | Language of the export file (`DE`, `EN`, `ES`, `FI`, `FR`, `IT`, `JA`, `NL`, `PL`, `PT`, `SV`)                   | String    | `"EN"`                  |
| `objectType`           | Object to export (e.g., `CONTACT`, or `objectTypeId` for custom objects)                                            | String    | `"CONTACT"`             |
| `associatedObjectType` | Associated object to include (optional, one only)                                                                 | String    | `"COMPANY"`             |
| `objectProperties`     | List of properties to export                                                                                       | Array     | `["email", "firstname"]` |
| `exportInternalValuesOptions` | Array to export internal names and/or values (`NAMES`, `VALUES`)                                                 | Array     | `["NAMES", "VALUES"]`    |


**For `exportType: VIEW`:**

Include `publicCrmSearchRequest` to filter and sort:

| Parameter             | Description                                                                    | Type      | Example                    |
|------------------------|--------------------------------------------------------------------------------|-----------|-----------------------------|
| `publicCrmSearchRequest.filters` | Array of filters (each with `value`, `propertyName`, `operator`)            | Array     | See Example below           |
| `publicCrmSearchRequest.sorts`  | Array of sorts (each with `propertyName`, `order` (`ASC` or `DES`))          | Array     | See Example below           |
| `publicCrmSearchRequest.query`   | Search query string                                                           | String    | `"example"`                  |


**For `exportType: LIST`:**

Include `listId`:

| Parameter | Description                                               | Type      | Example     |
|-----------|-----------------------------------------------------------|-----------|-------------|
| `listId`  | ILS List ID (found in HubSpot's List details)              | Integer   | `1234567`   |


**Example Request Body (VIEW):**

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

**Example Request Body (LIST):**

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

**2. Retrieve Export Status (GET):**

`/crm/v3/exports/export/async/tasks/{exportId}/status`

Replace `{exportId}` with the ID returned from the POST request.

**Response (JSON):**

The response includes the export's `status` (`COMPLETE`, `PENDING`, `PROCESSING`, `CANCELED`).  If `status` is `COMPLETE`, a download URL will be provided (expires in 5 minutes).


## Limits

* Maximum 3 `filterGroups` with up to 3 `filters` each.
* Maximum 30 exports within a 24-hour rolling window, one at a time.
* CSV files larger than 2MB are automatically zipped.


This documentation provides a comprehensive overview of the HubSpot CRM Exports API. Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
