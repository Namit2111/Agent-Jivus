# HubSpot CRM API: Associations v3

This document describes the HubSpot CRM API v3 for managing associations between objects.  Note that a newer v4 API offers additional functionality, including creating and managing association labels.  Refer to the [v4 Associations API article](link-to-v4-article-needed) for more advanced features.

## Overview

Associations represent relationships between objects and activities within the HubSpot CRM. The v3 API allows for bulk creation, retrieval, and removal of these associations.  For a deeper understanding of objects, records, properties, and associations APIs, consult the [Understanding the CRM](link-to-understanding-crm-guide-needed) guide. For general information on managing your CRM database, see [how to manage your CRM database](link-to-crm-management-needed).

## Association Types

Associations are defined by the `fromObjectType` and `toObjectType`, specifying a unidirectional relationship.  You'll need different definitions depending on the starting object type.

**Example:**

* To get association types from contacts to companies: `/crm/v3/associations/contacts/companies/types`
* To get tickets associated with a contact: `/crm/v3/associations/Contacts/Tickets/batch/read` (Contact is `fromObjectType`, Tickets is `toObjectType`)

Association types include:

* Unlabeled associations (e.g., contact-to-company)
* Default labeled associations (e.g., contact-to-primary company)
* Custom labeled associations (e.g., `Decision maker` contact-to-company)

Note: While you can reference custom association types (labels) with the v3 API, you cannot create or edit them. Use the v4 API for label management.


## API Endpoints

### Retrieve Association Types

**Endpoint:** `GET /crm/v3/associations/{fromObjectType}/{toObjectType}/types`

Retrieves all defined association types between two objects, including default and custom labels.  Each type has an `id` (numerical, unique for custom labels; same for default labels across accounts) and a `name`.

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

### Create Associations

**Endpoint:** `POST /crm/v3/associations/{fromObjectType}/{toObjectType}/batch/create`

Creates associations between records.  The request body includes an array of `inputs`, each specifying the `from` record ID, `to` record ID, and `type` of association.

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

### Retrieve Associations

**Endpoint:** `POST /crm/v3/associations/{fromObjectType}/{toObjectType}/batch/read`

Retrieves associated records. The request body includes an array of `inputs`, each specifying the ID of a record (`fromObjectType`) whose associations you want to retrieve.

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
        // ... more associated records
      ]
    },
    // ... more results for other input IDs
  ],
  "startedAt": "2024-10-21T16:40:47.810Z",
  "completedAt": "2024-10-21T16:40:47.833Z"
}
```

**Important Note:** When retrieving associations with companies (`/crm/v3/associations/{fromObjectType}/companies/batch/read`), only the primary associated company is returned. Use the v4 API to retrieve all associated companies.

### Remove Associations

**Endpoint:** `POST /crm/v3/associations/{fromObjectType}/{toObjectType}/batch/archive`

Removes associations between records. The request body includes an array of `inputs`, each specifying the `from` record ID, `to` record ID, and `type` of association to remove.

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

Remember to replace placeholders like `{fromObjectType}` and `{toObjectType}` with actual object types (e.g., "contacts", "companies", "deals").  Always consult the official HubSpot API documentation for the most up-to-date information and details.
