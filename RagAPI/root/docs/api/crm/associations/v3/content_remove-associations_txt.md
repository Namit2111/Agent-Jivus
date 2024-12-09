# HubSpot CRM API: Associations v3

This document describes the HubSpot CRM API v3 for managing associations between objects and activities.  Note that a newer v4 API offers additional functionality, including creating and managing association labels.  Refer to the [v4 Associations API article](link_to_v4_article_here) for more details.

## Overview

Associations represent relationships between objects and activities within the HubSpot CRM. The v3 API allows for bulk creation, retrieval, and removal of these associations.

To understand the context of objects, records, properties, and associations within the HubSpot CRM, refer to the [Understanding the CRM](link_to_understanding_crm_guide_here) guide.  For general information on managing your CRM database, see [how to manage your CRM database](link_to_crm_database_management_here).

## Association Types

Associations are defined by object type and direction.  They are unidirectional, meaning different definitions are needed depending on the starting object type. Each endpoint requires a `{fromObjectType}` and `{toObjectType}` to specify the association's direction.

For example:

* `/crm/v3/associations/contacts/companies/types`: Retrieves association types from contacts to companies.
* `/crm/v3/associations/Contacts/Tickets/batch/read`: Retrieves tickets associated with a contact (Contacts = `{fromObjectType}`, Tickets = `{toObjectType}`).  The `objectId` in the request body identifies the specific contact.


Association types include:

* **Unlabeled associations:** (e.g., contact-to-company)
* **Default labeled associations:** (e.g., contact-to-primary company)
* **Custom labeled associations:** (e.g., `Decision maker` contact-to-company)

While you can reference custom association types (labels) using the v3 API, you cannot create or edit them with this version. Use the v4 API for label creation, update, and deletion.


## API Endpoints

### Retrieve Association Types

**Method:** `GET`

**Endpoint:** `/crm/v3/associations/{fromObjectType}/{toObjectType}/types`

Retrieves all defined association types between specified objects, including default associations and custom association labels.  Each type has a numerical `id` and a `name`.  Default association IDs are consistent across accounts, while custom label IDs are account-specific.

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
    // ... more association types
  ]
}
```

### Create Associations

**Method:** `POST`

**Endpoint:** `/crm/v3/associations/{fromObjectType}/{toObjectType}/batch/create`

Associates records. The request body includes the `id` values of the records to associate and the `type` of the association.

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

Retrieves associated records. The request body includes the `id` values of the records (the `{fromObjectType}`) whose associations you want to view.

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

Removes associations between records.  The request body includes the `id` values for the `from` and `to` records, and their association `type`.

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


Remember to replace placeholders like `{fromObjectType}` and `{toObjectType}` with the actual object types (e.g., "Contacts", "Companies", "Deals").  Also, replace example IDs with your actual record IDs.
