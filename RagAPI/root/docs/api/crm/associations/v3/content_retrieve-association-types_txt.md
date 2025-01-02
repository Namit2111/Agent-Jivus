# HubSpot CRM API v3: Associations

This document describes the HubSpot CRM API v3 endpoints for managing associations between objects.  Note that a newer v4 API offers enhanced functionality, including label management.  Refer to the v4 documentation for those features.

## Overview

Associations represent relationships between objects (e.g., contacts, companies, deals) and activities within the HubSpot CRM.  This API allows for bulk creation, retrieval, and removal of associations.  Associations are unidirectional; the direction is specified by `fromObjectType` and `toObjectType`.

**Key Concepts:**

* **`fromObjectType`:** The starting object type of the association.
* **`toObjectType`:** The ending object type of the association.
* **Association Type:** Defined by `fromObjectType`, `toObjectType`, and optionally a label (custom or default).  Types are identified by a numerical `id` and a `name`.  Default association IDs are consistent across accounts, while custom label IDs are account-specific.


## API Endpoints

All endpoints are under the base URL `/crm/v3/associations`.

### 1. Retrieve Association Types

**Endpoint:** `GET /crm/v3/associations/{fromObjectType}/{toObjectType}/types`

**Description:** Retrieves all defined association types between the specified `fromObjectType` and `toObjectType`, including default and custom labeled associations.

**Request:**  A simple GET request with the object types as path parameters.

**Example Request:**

```bash
GET /crm/v3/associations/contacts/companies/types
```

**Response:** A JSON object containing an array of association types. Each type has an `id` and a `name`.

**Example Response:**

```json
{
  "results": [
    {
      "id": "136",
      "name": "franchise_owner_franchise_location"
    },
    {
      "id": "1",
      "name": "contact_to_company"
    },
    // ... more association types
  ]
}
```

### 2. Create Associations

**Endpoint:** `POST /crm/v3/associations/{fromObjectType}/{toObjectType}/batch/create`

**Description:** Creates associations between records in bulk.

**Request:** A POST request with a JSON body containing an array of `inputs`. Each `input` specifies the `from` and `to` object IDs and the `type` of association.

**Example Request Body:**

```json
{
  "inputs": [
    {
      "from": {
        "id": "53628"
      },
      "to": {
        "id": "12726"
      },
      "type": "contact_to_company"
    }
  ]
}
```

**Response:**  (Not specified in the provided text, but likely a success/failure indication for each input).


### 3. Retrieve Associations

**Endpoint:** `POST /crm/v3/associations/{fromObjectType}/{toObjectType}/batch/read`

**Description:** Retrieves associations for a set of records.

**Request:** A POST request with a JSON body containing an array of `inputs`. Each `input` specifies the `id` of a `fromObjectType` record.

**Example Request Body:**

```json
{
  "inputs": [
    {
      "id": "5790939450"
    },
    {
      "id": "6108662573"
    }
  ]
}
```

**Response:** A JSON object containing the results.  Each result includes the `from` object ID and an array of associated `to` objects, each with its `id` and `type`.  Note that when retrieving associations with companies, only the primary associated company is returned in v3.

**Example Response:**

```json
{
  "status": "COMPLETE",
  "results": [
    {
      "from": {
        "id": "5790939450"
      },
      "to": [
        {
          "id": "1467822235",
          "type": "company_to_deal"
        },
        // ... more associated deals
      ]
    },
    // ... more results for other companies
  ],
  "startedAt": "...",
  "completedAt": "..."
}
```


### 4. Remove Associations

**Endpoint:** `POST /crm/v3/associations/{fromObjectType}/{toObjectType}/batch/archive`

**Description:** Removes associations between records in bulk.

**Request:** A POST request with a JSON body containing an array of `inputs`. Each `input` specifies the `from` and `to` object IDs and the `type` of association to remove.

**Example Request Body:**

```json
{
  "inputs": [
    {
      "from": {
        "id": "5790939450"
      },
      "to": {
        "id": "21678228008"
      },
      "type": "company_to_deal"
    }
  ]
}
```

**Response:** (Not specified in the provided text, but likely a success/failure indication for each input.)


## Important Notes

* The v3 API does not support creating or editing custom association labels. Use the v4 API for those functionalities.
* When retrieving associations with companies (`/crm/v3/associations/{fromObjectType}/companies/batch/read`), only the primary associated company will be returned. Use the v4 API to retrieve all associated companies.


This markdown documentation provides a concise and clear overview of the HubSpot CRM API v3 for associations, including examples of requests and responses for each endpoint. Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
