# HubSpot CRM API: Associations v3

This document describes the HubSpot CRM API v3 for managing associations between objects.  Note that a newer v4 API with enhanced functionality, including association label management, is available.  Refer to the [v4 Associations API article](link-to-v4-article-here) for details on the newer version.

## Overview

Associations represent relationships between objects and activities within the HubSpot CRM.  The v3 API allows for bulk creation, retrieval, and removal of these associations.

For a broader understanding of objects, records, properties, and associations APIs, consult the [Understanding the CRM guide](link-to-crm-guide-here). For general information on managing your CRM database, see [how to manage your CRM database](link-to-database-management-here).

## Association Types

Associations are defined by object and direction (unidirectional).  You need a different definition based on the starting object type (`fromObjectType`). Each endpoint requires `fromObjectType` and `toObjectType` specifying the association's direction.

**Example:**

* To get association types from contacts to companies: `/crm/v3/associations/contacts/companies/types`
* To see tickets associated with a contact: `/crm/v3/associations/Contacts/Tickets/batch/read` (Contact is `fromObjectType`, Tickets is `toObjectType`).  The contact's `objectId` is identified in the request body.

Association types include unlabeled associations (e.g., contact-to-company), default labeled associations (e.g., contact-to-primary company), and custom labeled associations (e.g., "Decision maker" contact-to-company).  While you can *reference* custom association types (labels) with v3, you cannot create or edit them using this API. Use the v4 API for label creation, update, and deletion.


## API Endpoints

### Retrieve Association Types

**Method:** `GET`

**Endpoint:** `/crm/v3/associations/{fromObjectType}/{toObjectType}/types`

Retrieves all defined association types between two objects, including default and custom association labels.  Each type has an `id` (numerical) and a `name`.  Default association IDs are consistent across accounts; custom label IDs are account-specific.


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
    // ... more results
  ]
}
```

### Create Associations

**Method:** `POST`

**Endpoint:** `/crm/v3/associations/{fromObjectType}/{toObjectType}/batch/create`

Creates associations between records. The request body includes the `id` values of the records to associate and the association `type`.

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

Retrieves associated records.  The request body includes the `id` values of the records (from `fromObjectType`) whose associations you want to view.


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

**Note:** When retrieving associations with companies (`/crm/v3/associations/{fromObjectType}/companies/batch/read`), only the primary associated company is returned. Use the v4 API for all associated companies.


### Remove Associations

**Method:** `POST`

**Endpoint:** `/crm/v3/associations/{fromObjectType}/{toObjectType}/batch/archive`

Removes associations between records.  The request body includes the `id` values of the `from` and `to` records, and the association `type`.

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

Remember to replace placeholders like `{fromObjectType}` and `{toObjectType}` with the actual object types (e.g., "contacts", "companies", "deals").  This documentation provides a general overview.  Refer to the official HubSpot API documentation for complete details, error handling, and rate limits.
