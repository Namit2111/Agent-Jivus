# HubSpot CRM API v3: Associations

This document details the HubSpot CRM API v3 endpoints for managing associations between objects.  The v4 API offers enhanced functionality, including label creation and management; refer to the [v4 Associations API documentation](link_to_v4_docs_here) for those features.  This v3 API allows bulk creation, retrieval, and removal of associations.

## Understanding Associations

Associations define relationships between objects (e.g., contacts, companies, deals) and activities within the HubSpot CRM. They are unidirectional, meaning you need different definitions depending on the starting object type (`fromObjectType`) and ending object type (`toObjectType`).

## Endpoints

All endpoints are under the base URL `/crm/v3/associations/`.  Replace placeholders like `{fromObjectType}` and `{toObjectType}` with the actual object types (e.g., `Contacts`, `Companies`, `Deals`).  Remember that object types are case-sensitive.

### 1. Retrieve Association Types

**Endpoint:** `/crm/v3/associations/{fromObjectType}/{toObjectType}/types`

**Method:** `GET`

**Description:** Retrieves all defined association types between specified `fromObjectType` and `toObjectType`, including default and custom labels (but not the ability to create or edit them).

**Example Request:**

`/crm/v3/associations/contacts/companies/types`

**Example Response:**

```json
{
  "results": [
    {
      "id": "136",
      "name": "franchise_owner_franchise_location"
    },
    {
      "id": "26",
      "name": "manager"
    },
    {
      "id": "1",
      "name": "contact_to_company"
    },
    // ... more association types
  ]
}
```

* **`id`:** Numerical ID of the association type.  Default association IDs are consistent across accounts, while custom label IDs are unique.
* **`name`:**  Name of the association type.


### 2. Create Associations

**Endpoint:** `/crm/v3/associations/{fromObjectType}/{toObjectType}/batch/create`

**Method:** `POST`

**Description:** Creates multiple associations in a single request.

**Request Body:**

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
      "type": "contact_to_company" // Association type ID or name obtained from the GET endpoint above.
    }
    // ... more associations
  ]
}
```

**Response:**  A successful response indicates the creation of associations.  Error responses will provide details on any failures.


### 3. Retrieve Associations

**Endpoint:** `/crm/v3/associations/{fromObjectType}/{toObjectType}/batch/read`

**Method:** `POST`

**Description:** Retrieves associations for a list of records.

**Request Body:**

```json
{
  "inputs": [
    {
      "id": "5790939450" // ID of the 'from' record
    },
    {
      "id": "6108662573" // ID of another 'from' record
    }
    // ... more 'from' record IDs
  ]
}
```

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
        // ... associated 'to' records
      ]
    },
    // ... results for other 'from' records
  ],
  "startedAt": "...",
  "completedAt": "..."
}
```

**Note:** When retrieving associations with companies (`/crm/v3/associations/{fromObjectType}/companies/batch/read`), only the *primary* associated company will be returned. Use the v4 API for all associated companies.


### 4. Remove Associations

**Endpoint:** `/crm/v3/associations/{fromObjectType}/{toObjectType}/batch/archive`

**Method:** `POST`

**Description:** Removes multiple associations.

**Request Body:**

```json
{
  "inputs": [
    {
      "from": {
        "id": "5790939450" // ID of the 'from' record
      },
      "to": {
        "id": "21678228008" // ID of the 'to' record
      },
      "type": "company_to_deal" // Association type
    }
    // ... more associations to remove
  ]
}
```

**Response:** Similar to create, a successful response indicates successful removal.  Error responses detail any failures.


## Error Handling

The API returns standard HTTP status codes to indicate success or failure. Error responses will contain detailed information about the errors encountered. Refer to the HubSpot API documentation for details on error handling.


## Rate Limits

Be mindful of HubSpot's API rate limits to avoid throttling.  Check the HubSpot API documentation for current limits.
