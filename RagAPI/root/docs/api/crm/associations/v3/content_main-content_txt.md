# HubSpot CRM API: Associations v3

This document describes the HubSpot CRM API v3 for managing associations between objects.  Note that a newer v4 API with enhanced functionality, including association label management, is available.  Refer to the [v4 Associations API article](link-to-v4-article-here) for more details.

## Overview

Associations in the HubSpot CRM represent relationships between objects and activities.  The v3 API allows for bulk creation, retrieval, and removal of these associations.  For a comprehensive understanding of objects, records, properties, and associations APIs, consult the [Understanding the CRM guide](link-to-understanding-crm-guide-here).  For general CRM database management information, see [how to manage your CRM database](link-to-crm-management-guide-here).

## Association Types

Associations are defined by object and direction. They are unidirectional, meaning the definition varies depending on the starting object type.  Each endpoint requires a `{fromObjectType}` and `{toObjectType}` specifying the association direction.

**Example:**

* To get association types from contacts to companies: `/crm/v3/associations/contacts/companies/types`
* To get tickets associated with a contact: `/crm/v3/associations/Contacts/Tickets/batch/read` (Contact is `fromObjectType`, Tickets is `toObjectType`)

Association types include:

* Unlabeled associations (e.g., contact-to-company)
* Default labeled associations (e.g., contact-to-primary company)
* Custom labeled associations (e.g., `Decision maker` contact-to-company)

While you can use custom association types (labels) with the v3 API, you cannot create or edit them.  Use the v4 API for label creation, updates, and deletion.


## API Endpoints

### Retrieve Association Types

**Method:** `GET`

**Endpoint:** `/crm/v3/associations/{fromObjectType}/{toObjectType}/types`

This endpoint retrieves all defined association types between two objects, including default and custom association labels.  Each type has an `id` and `name`.  Default association IDs are consistent across accounts, while custom label IDs are account-specific.

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

**Method:** `POST`

**Endpoint:** `/crm/v3/associations/{fromObjectType}/{toObjectType}/batch/create`

Associates records. The request body includes the `id` values of the records to associate and the association `type`.

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

**Method:** `POST`

**Endpoint:** `/crm/v3/associations/{fromObjectType}/{toObjectType}/batch/read`

Retrieves associated records. The request body includes the `id` values of the records (`{fromObjectType}`) whose associations are to be retrieved.

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

**Note:** When retrieving associations with companies (`crm/v3/associations/{fromObjectType}/companies/batch/read`), only the primary associated company is returned. Use the v4 API for all associated companies.

### Remove Associations

**Method:** `POST`

**Endpoint:** `/crm/v3/associations/{fromObjectType}/{toObjectType}/batch/archive`

Removes associations between records. The request body includes the `id` values for the `from` and `to` records and their association `type`.

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

Remember to replace placeholders like `{fromObjectType}` and `{toObjectType}` with the actual object types (e.g., "contacts", "companies", "deals").  Always refer to the official HubSpot API documentation for the most up-to-date information and details.
