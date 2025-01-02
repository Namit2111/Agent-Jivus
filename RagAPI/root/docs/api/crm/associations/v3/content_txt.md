# HubSpot CRM API: Associations v3

This document describes the HubSpot CRM API v3 for managing associations between objects.  Note that v4 offers enhanced functionality, including label management; see the [v4 Associations API article](link_to_v4_article) for details.

## Overview

Associations define relationships between objects and activities within the HubSpot CRM.  This v3 API allows bulk creation, retrieval, and removal of these associations.  Understanding HubSpot's concepts of objects, records, properties, and associations is crucial; refer to the [Understanding the CRM guide](link_to_crm_guide) and [managing your CRM database](link_to_crm_management) for more information.

Associations are unidirectional.  You need separate definitions based on the starting (`fromObjectType`) and ending (`toObjectType`) object types.

## Association Types

Associations are categorized by object and direction, including unlabeled, default labeled, and custom labeled associations.  Custom labels cannot be created or modified via this v3 API; use the v4 API for that.

### Retrieving Association Types

**API Call:** `GET /crm/v3/associations/{fromObjectType}/{toObjectType}/types`

**Request:**  No request body is needed.

**Response:** A JSON object containing an array of association types. Each type has an `id` (numerical, unique for custom labels within your account) and a `name`.

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
    {
      "id": "30",
      "name": "decision_maker"
    }
  ]
}
```


## Creating Associations

**API Call:** `POST /crm/v3/associations/{fromObjectType}/{toObjectType}/batch/create`

**Request Body:**  A JSON object with an `inputs` array. Each element in the array defines an association:

```json
{
  "inputs": [
    {
      "from": {
        "id": "53628" // ID of the 'from' record
      },
      "to": {
        "id": "12726" // ID of the 'to' record
      },
      "type": "contact_to_company" // Association type ID or name
    }
  ]
}
```

**Response:**  (Success response structure not provided in original text.  Expect a success indicator or error details.)


## Retrieving Associations

**API Call:** `POST /crm/v3/associations/{fromObjectType}/{toObjectType}/batch/read`

**Request Body:** A JSON object with an `inputs` array. Each element contains the `id` of a record from the `fromObjectType` whose associations you want to retrieve.

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

**Response:** A JSON object with a `results` array. Each element shows the `from` record ID and an array of associated `to` records, including their `id` and `type`.  Note that when retrieving associations *with* companies (`...companies/batch/read`), only the primary associated company is returned.

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
        }
      ]
    }
  ],
  "startedAt": "2024-10-21T16:40:47.810Z",
  "completedAt": "2024-10-21T16:40:47.833Z"
}
```

## Removing Associations

**API Call:** `POST /crm/v3/associations/{fromObjectType}/{toObjectType}/batch/archive`

**Request Body:** A JSON object with an `inputs` array. Each element specifies the `from` and `to` record IDs and their `type` to be removed.

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

**Response:** (Success response structure not provided in original text.  Expect a success indicator or error details.)


**Note:** Replace `{fromObjectType}` and `{toObjectType}` with the actual object types (e.g., `Contacts`, `Companies`, `Deals`).  All IDs are HubSpot record IDs. Remember that this is the v3 API; v4 offers more comprehensive features.
