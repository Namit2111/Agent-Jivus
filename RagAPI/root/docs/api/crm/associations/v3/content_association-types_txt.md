# HubSpot CRM API: Associations v3

This document describes the HubSpot CRM API v3 for managing associations between objects.  Note that a newer version (v4) offers additional functionality, including creating and managing association labels.  Refer to the [v4 Associations API article](link_to_v4_article_here) for more advanced features.

## Overview

Associations represent relationships between objects and activities within the HubSpot CRM.  The v3 API allows for bulk creation, retrieval, and removal of these associations.

For a comprehensive understanding of objects, records, properties, and associations APIs, consult the [Understanding the CRM guide](link_to_crm_guide_here).  For general CRM database management information, see [how to manage your CRM database](link_to_db_management_here).

## Association Types

Associations are defined by object and direction (unidirectional).  You need different definitions depending on the starting object type (`fromObjectType`). Each endpoint requires `fromObjectType` and `toObjectType` to specify the association direction.

**Example:**

* To get association types from contacts to companies: `/crm/v3/associations/contacts/companies/types`
* To see tickets associated with a contact: `/crm/v3/associations/Contacts/Tickets/batch/read` (Contact is `fromObjectType`, Tickets is `toObjectType`).  The specific contact is identified in the request body using `objectId`.

Association types include:

* Unlabeled associations (e.g., contact-to-company)
* Default labeled associations (e.g., contact-to-primary company)
* Custom labeled associations (e.g., `Decision maker` contact-to-company)

While you can use custom association types (labels) with v3, you *cannot* create or edit them using this API. Use the v4 API for label management.


## API Endpoints

### Retrieve Association Types

**Method:** `GET`

**Endpoint:** `/crm/v3/associations/{fromObjectType}/{toObjectType}/types`

Retrieves all defined association types between specified objects, including default and custom labels.  The response includes an `id` (numerical) and `name` for each type. Default association IDs are consistent across accounts, while custom label IDs are account-specific.

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

Creates associations between records. The request body includes `id` values for the records to be associated and the `type` of association.

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

Retrieves associated records. The request body includes `id` values for the `fromObjectType` records.

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

Removes associations between records.  The request body specifies the `id` values for the `from` and `to` records, and their association `type`.

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


Remember to replace placeholders like `{fromObjectType}` and `{toObjectType}` with the actual object types (e.g., "contacts", "companies", "deals").  This markdown provides a structured overview; refer to the official HubSpot API documentation for detailed specifications and error handling.
