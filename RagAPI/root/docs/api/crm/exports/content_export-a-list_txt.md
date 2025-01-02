# HubSpot CRM Exports API Documentation

This document details the HubSpot CRM Exports API, allowing you to export CRM data, retrieve download URLs, and check export statuses.  The API uses asynchronous requests; you initiate an export and then poll for its completion.

## API Endpoints

**1. Start an Export (POST):**

`/crm/v3/exports/export/async`

This endpoint initiates an export job.  The response includes the `id` of the export task.

**Request Body (JSON):**

The request body varies depending on whether you're exporting a view or a list.  Common parameters are:

| Parameter             | Description                                                                                                          | Type     | Example                               |
|----------------------|----------------------------------------------------------------------------------------------------------------------|----------|---------------------------------------|
| `exportType`          | `VIEW` (for views) or `LIST` (for lists)                                                                              | String   | `"VIEW"`                               |
| `format`              | File format: `XLSX`, `CSV`, or `XLS`                                                                                  | String   | `"CSV"`                               |
| `exportName`          | Name of the export                                                                                                    | String   | `"My Contact Export"`                  |
| `language`            | Language of the export file (e.g., `DE`, `EN`, `ES`)                                                              | String   | `"EN"`                                 |
| `objectType`          | Object type to export (e.g., `CONTACT`, or `objectTypeId` for custom objects)                                       | String   | `"CONTACT"`                            |
| `associatedObjectType` | (Optional) Associated object to include (e.g., `COMPANY`). Only one allowed per request.                            | String   | `"COMPANY"`                           |
| `objectProperties`     | List of properties to export                                                                                         | Array    | `["email", "firstname", "lastname"]` |
| `exportInternalValuesOptions` | (Optional) Array to export internal property names (`NAMES`) and/or values (`VALUES`).                          | Array    | `["NAMES", "VALUES"]`                |
| `listId`              | (Required for `LIST` exportType) ILS List ID of the list to export.                                                | Integer  | `1234567`                             |
| `publicCrmSearchRequest` | (Optional, for `VIEW` exportType) Object for filtering and sorting. Contains `filters`, `sorts`, and `query`.  | Object   | See example below                    |


**`publicCrmSearchRequest` Structure (Example):**

```json
{
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
```


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
  "id": "YOUR_EXPORT_ID"
}
```


**2. Retrieve Export Status (GET):**

`/crm/v3/exports/export/async/tasks/{exportId}/status`

This endpoint retrieves the status of an export.

**Parameters:**

* `{exportId}`: The ID returned from the POST request.

**Response (JSON):**

```json
{
  "status": "COMPLETE"|"PENDING"|"PROCESSING"|"CANCELED",
  "downloadUrl": "YOUR_DOWNLOAD_URL" // Only present if status is COMPLETE
}
```

**Note:** The `downloadUrl` expires after 5 minutes.


## Limits

* Maximum 3 `filterGroups` with up to 3 `filters` each.
* Maximum 30 exports within a 24-hour rolling window; only one export can run concurrently.
* CSV files larger than 2MB are automatically zipped.


## Example Usage (Python)

This example uses the `requests` library.  Remember to replace placeholders like `YOUR_API_KEY` and `YOUR_EXPORT_ID`.

```python
import requests
import json

# Replace with your HubSpot API key
api_key = "YOUR_API_KEY"
base_url = "https://api.hubapi.com"

# Start an export
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

export_data = {
    "exportType": "LIST",
    "listId": 1234567,
    "exportName": "My List Export",
    "format": "csv",
    "objectType": "CONTACT",
    "objectProperties": ["email", "firstname"]
}

response = requests.post(f"{base_url}/crm/v3/exports/export/async", headers=headers, data=json.dumps(export_data))
response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
export_id = response.json()["id"]


# Retrieve export status
while True:
    status_url = f"{base_url}/crm/v3/exports/export/async/tasks/{export_id}/status"
    status_response = requests.get(status_url, headers=headers)
    status_response.raise_for_status()
    status_data = status_response.json()
    print(f"Export status: {status_data['status']}")

    if status_data["status"] == "COMPLETE":
        download_url = status_data["downloadUrl"]
        print(f"Download URL: {download_url}")
        # Download the file using download_url
        break
    elif status_data["status"] == "CANCELED" or status_data["status"] == "ERROR":
        print("Export failed.")
        break
    else:
        import time
        time.sleep(5)  # Wait before checking again
```

This provides a comprehensive guide to using the HubSpot CRM Exports API.  Remember to consult the official HubSpot API documentation for the most up-to-date information and potential changes.
