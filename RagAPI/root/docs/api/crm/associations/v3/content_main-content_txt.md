# HubSpot CRM API v3: Associations

This document details the HubSpot CRM API v3 endpoints for managing associations between objects.  Note that a newer v4 API exists with enhanced functionality, including label creation and management.  Refer to the v4 documentation for those features.

## Understanding Associations

Associations represent relationships between objects (e.g., Contacts, Companies, Deals) and activities within the HubSpot CRM. The v3 API allows bulk creation, retrieval, and removal of these associations.  Associations are unidirectional; you need separate definitions based on the starting object type (`fromObjectType`).

Each association is defined by:

* **`fromObjectType`**: The starting object type.
* **`toObjectType`**: The ending object type.
* **`type`**: The type of association (can be unlabeled, default labeled, or custom labeled).  Custom labeled associations cannot be created or modified via v3.

## API Endpoints

All endpoints are under the base URL `/crm/v3/associations`.

### 1. Retrieve Association Types

**Endpoint:** `GET /crm/v3/associations/{fromObjectType}/{toObjectType}/types`

**Description:** Retrieves all defined association types between two specified objects. This includes default and custom association labels.

**Parameters:**

* `{fromObjectType}`:  The starting object type (e.g., `contacts`, `companies`).
* `{toObjectType}`: The ending object type (e.g., `companies`, `deals`).

**Response:**

A JSON object with a `results` array containing objects, each with:

* `id`:  A numerical ID representing the association type.  For default associations, this is consistent across accounts; for custom labels, it's account-specific.
* `name`: The name of the association type.


**Example:**

**Request:** `GET /crm/v3/associations/contacts/companies/types`

**Response:**

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
    // ... more association types
  ]
}
```

### 2. Create Associations

**Endpoint:** `POST /crm/v3/associations/{fromObjectType}/{toObjectType}/batch/create`

**Description:** Creates multiple associations between records.

**Request Body:**

A JSON object with an `inputs` array. Each element in the array should be an object with:

* `from`: An object with an `id` property specifying the ID of the from record.
* `to`: An object with an `id` property specifying the ID of the to record.
* `type`: The ID of the association type (obtained from the `/types` endpoint).

**Example:**

**Request:** `POST /crm/v3/associations/Contacts/Companies/batch/create`

**Request Body:**

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

### 3. Retrieve Associations

**Endpoint:** `POST /crm/v3/associations/{fromObjectType}/{toObjectType}/batch/read`

**Description:** Retrieves associations for a batch of records.

**Request Body:**

A JSON object with an `inputs` array. Each element contains an `id` property for the record from which to retrieve associations.

**Example:**

**Request:** `POST /crm/v3/associations/Companies/Deals/batch/read`

**Request Body:**

```json
{
  "inputs": [
    { "id": "5790939450" },
    { "id": "6108662573" }
  ]
}
```

**Response:**

A JSON object with a `results` array. Each element contains:

* `from`: An object with the `id` of the starting record.
* `to`: An array of associated records, each with an `id` and `type`.

**Important Note:** When retrieving associations with `companies` as the `fromObjectType`, only the *primary* associated company will be returned.


### 4. Remove Associations

**Endpoint:** `POST /crm/v3/associations/{fromObjectType}/{toObjectType}/batch/archive`

**Description:** Removes multiple associations between records.

**Request Body:**

A JSON object with an `inputs` array. Each element should be an object with:

* `from`: An object with an `id` property specifying the ID of the from record.
* `to`: An object with an `id` property specifying the ID of the to record.
* `type`: The ID of the association type.

**Example:**

**Request:** `POST /crm/v3/associations/companies/deals/batch/archive`

**Request Body:**

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

##  Error Handling

The API responses will include standard HTTP status codes and error messages in the JSON response body to indicate success or failure.  Consult the HubSpot API documentation for details on error codes.


This markdown provides a comprehensive overview of the HubSpot CRM v3 Associations API. Remember to consult the official HubSpot documentation for the most up-to-date information and detailed error handling.
