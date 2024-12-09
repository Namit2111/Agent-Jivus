# HubSpot CRM API: Associations v3

This document describes the HubSpot CRM API v3 for managing associations between objects.  Note that the v4 API offers expanded functionality, including label creation and management.  See the [v4 Associations API article](link_to_v4_article_here) for details.

## Overview

Associations represent relationships between objects and activities within the HubSpot CRM. The v3 API allows for bulk creation, retrieval, and removal of these associations.

For a broader understanding of objects, records, properties, and associations APIs, consult the [Understanding the CRM guide](link_to_understanding_crm_guide_here).  For general CRM database management information, see [how to manage your CRM database](link_to_crm_database_management_here).

## Association Types

Associations are defined by object and direction. They are unidirectional, meaning different definitions are required depending on the starting object type. Each endpoint uses `{fromObjectType}` and `{toObjectType}` parameters to specify the association direction.

**Example:**

* To view association types from contacts to companies: `/crm/v3/associations/contacts/companies/types`
* To see tickets associated with a contact: `/crm/v3/associations/Contacts/Tickets/batch/read` (identifying the contact by `objectId` in the request body).  Here, `Contacts` is `{fromObjectType}` and `Tickets` is `{toObjectType}`.

Association types include:

* Unlabeled associations (e.g., contact-to-company)
* Default labeled associations (e.g., contact-to-primary company)
* Custom labeled associations (e.g., `Decision maker` contact-to-company)

While v3 allows referencing custom association types (labels), it *does not* support creating or editing them. Use the v4 API for label creation, updates, and deletion.


## API Endpoints

### Retrieve Association Types

**Method:** `GET`

**Endpoint:** `/crm/v3/associations/{fromObjectType}/{toObjectType}/types`

This endpoint retrieves all defined association types between two objects, including default and custom association labels.  Each type has a numerical `id` and a `name`.  Default association IDs are consistent across accounts, while custom label IDs are account-specific.

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

This endpoint creates associations between records. The request body includes the `id` values of the records to associate and the association `type`.

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

This endpoint retrieves associated records. The request body includes the `id` values of the records (the `{fromObjectType}`) whose associations you want to view.

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

**Method:** `POST`

**Endpoint:** `/crm/v3/associations/{fromObjectType}/{toObjectType}/batch/archive`

This endpoint removes associations between records.  The request body includes the `id` values for the `from` and `to` records, and their association `type`.

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

Remember to replace placeholders like `{fromObjectType}` and `{toObjectType}` with the actual object types (e.g., `contacts`, `companies`, `deals`).  This documentation provides a general overview; always refer to the official HubSpot API documentation for the most up-to-date information and details.
