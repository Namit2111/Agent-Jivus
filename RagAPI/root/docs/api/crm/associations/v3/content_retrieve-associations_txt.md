# HubSpot CRM API: Associations v3

This document describes the HubSpot CRM API v3 for managing associations between objects and activities.  Note that a newer v4 API offers additional functionality, including creating and managing association labels; see the [v4 Associations API article](link_to_v4_article_here) for details.

## Overview

Associations represent relationships between objects in the HubSpot CRM.  The v3 API allows bulk creation, retrieval, and removal of these associations.  For a deeper understanding of objects, records, properties, and associations within the HubSpot CRM, refer to the [Understanding the CRM guide](link_to_crm_guide_here) and learn how to [manage your CRM database](link_to_crm_management_here).

## Association Types

Associations are defined by `fromObjectType` and `toObjectType`, indicating the direction of the relationship (unidirectional).  Each endpoint requires these parameters.

**Example:**

* To retrieve association types from contacts to companies: `/crm/v3/associations/contacts/companies/types`
* To retrieve tickets associated with a contact: `/crm/v3/associations/Contacts/Tickets/batch/read` (Contact is `fromObjectType`, Tickets is `toObjectType`).

Association types include:

* Unlabeled associations (e.g., contact-to-company)
* Default labeled associations (e.g., contact-to-primary company)
* Custom labeled associations (e.g., `Decision maker` contact-to-company)

While v3 supports using custom association types, it does *not* allow creating or editing new labels. Use the v4 API for label management.

## API Endpoints

### Retrieve Association Types

**Endpoint:** `GET /crm/v3/associations/{fromObjectType}/{toObjectType}/types`

Retrieves all defined association types between specified objects, including default and custom labels.  The response includes an `id` (numerical) and `name` for each type.  Default association IDs are consistent across accounts, while custom label IDs are account-specific.

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

**Endpoint:** `POST /crm/v3/associations/{fromObjectType}/{toObjectType}/batch/create`

Associates records. The request body includes an array of `inputs`, each specifying:

* `from`: The ID of the `fromObjectType` record.
* `to`: The ID of the `toObjectType` record.
* `type`: The ID of the association type.

**Example Request Body:**

```json
{
  "inputs": [
    {
      "from": { "id": "53628" },
      "to": { "id": "12726" },
      "type": "contact_to_company"
    }
  ]
}
```

### Retrieve Associations

**Endpoint:** `POST /crm/v3/associations/{fromObjectType}/{toObjectType}/batch/read`

Retrieves associated records. The request body includes an array of `inputs` containing the IDs of the `fromObjectType` records.

**Example Request Body:**

```json
{
  "inputs": [
    { "id": "5790939450" },
    { "id": "6108662573" }
  ]
}
```

**Example Response:**

```json
{
  "status": "COMPLETE",
  "results": [
    {
      "from": { "id": "5790939450" },
      "to": [
        { "id": "1467822235", "type": "company_to_deal" },
        // ... more associated records
      ]
    },
    // ... more results for other fromObjectIds
  ],
  "startedAt": "...",
  "completedAt": "..."
}
```

**Note:** When retrieving associations with companies (`crm/v3/associations/{fromObjectType}/companies/batch/read`), only the primary associated company is returned.  Use the v4 API for all associated companies.


### Remove Associations

**Endpoint:** `POST /crm/v3/associations/{fromObjectType}/{toObjectType}/batch/archive`

Removes associations between records. The request body includes an array of `inputs`, each specifying:

* `from`: The ID of the `fromObjectType` record.
* `to`: The ID of the `toObjectType` record.
* `type`: The ID of the association type.

**Example Request Body:**

```json
{
  "inputs": [
    {
      "from": { "id": "5790939450" },
      "to": { "id": "21678228008" },
      "type": "company_to_deal"
    }
  ]
}
```

Remember to replace placeholders like `{fromObjectType}` and `{toObjectType}` with the actual object types (e.g., "contacts", "companies", "deals").  Consult the HubSpot API documentation for a complete list of object types and further details.
