# HubSpot CRM API v3: Associations

This document describes the HubSpot CRM API v3 endpoints for managing associations between objects.  This version allows for bulk operations but lacks the functionality to create or edit association labels (for that, see the v4 API).  Associations define relationships between objects and activities within the HubSpot CRM.

## Understanding Associations

Associations are unidirectional and defined by `fromObjectType` and `toObjectType`.  For example, an association from `Contacts` to `Companies` is different from an association from `Companies` to `Contacts`.

* **`fromObjectType`**: The starting object type of the association.
* **`toObjectType`**: The ending object type of the association.
* **Association Types**:  Can be unlabeled, default labeled, or custom labeled.  While custom labels can be referenced, they cannot be created or modified via this v3 API.

## API Endpoints

All endpoints use the base URL `/crm/v3/associations/`.  Remember to replace placeholders like `{fromObjectType}` and `{toObjectType}` with the actual object types (e.g., `Contacts`, `Companies`, `Deals`, `Tickets`).

**Note:**  Object type names are case-sensitive.


### 1. Retrieve Association Types

**Endpoint:** `GET /crm/v3/associations/{fromObjectType}/{toObjectType}/types`

**Description:** Retrieves all defined association types between two specified objects, including default and custom association labels.

**Request:**  A simple GET request to the endpoint with the `fromObjectType` and `toObjectType` as path parameters.  No request body is required.

**Response:** A JSON object with a `results` array. Each element in the array represents an association type with `id` (numerical ID) and `name` properties.  Custom label IDs are account-specific.

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
    }
    // ... more association types
  ]
}
```


### 2. Create Associations

**Endpoint:** `POST /crm/v3/associations/{fromObjectType}/{toObjectType}/batch/create`

**Description:** Creates multiple associations between records in bulk.

**Request:** A POST request with a JSON body containing an `inputs` array. Each element in the array defines an association with:

* `from`: An object with an `id` property representing the `fromObjectType` record.
* `to`: An object with an `id` property representing the `toObjectType` record.
* `type`: The name of the association type (obtained from the `/types` endpoint).

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

**Response:**  A successful response indicates the associations were created.  Error handling should be implemented to manage failures.


### 3. Retrieve Associations

**Endpoint:** `POST /crm/v3/associations/{fromObjectType}/{toObjectType}/batch/read`

**Description:** Retrieves associations for specified records.

**Request:** A POST request with a JSON body containing an `inputs` array.  Each element contains an `id` property representing a record of the `fromObjectType`.

**Example Request Body:**

```json
{
  "inputs": [
    { "id": "5790939450" },
    { "id": "6108662573" }
  ]
}
```

**Response:** A JSON object with:

* `status`: "COMPLETE" on success.
* `results`: An array of objects. Each object represents a record from the `fromObjectType` and its associated `toObjectType` records, including their IDs and association type.
* `startedAt`, `completedAt`: Timestamps indicating the start and end of the operation.

**Example Response:**

```json
{
  "status": "COMPLETE",
  "results": [
    {
      "from": { "id": "5790939450" },
      "to": [
        { "id": "1467822235", "type": "company_to_deal" },
        // ... more associated deals
      ]
    }
    // ... more records
  ],
  "startedAt": "...",
  "completedAt": "..."
}
```

**Important Note:** When retrieving associations with companies (`crm/v3/associations/{fromObjectType}/companies/batch/read`), only the primary associated company is returned.  Use the v4 API for all associated companies.


### 4. Remove Associations

**Endpoint:** `POST /crm/v3/associations/{fromObjectType}/{toObjectType}/batch/archive`

**Description:** Removes associations between records in bulk.

**Request:** A POST request with a JSON body containing an `inputs` array. Each element defines an association to be removed, specifying `from`, `to` record IDs, and `type`.

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

**Response:** A successful response indicates the associations were removed.  Error handling is necessary.


##  Error Handling

The API will return appropriate HTTP status codes and error messages in the JSON response body to indicate failure.  Proper error handling should be implemented in your code to gracefully handle these situations.


This markdown documentation provides a comprehensive overview of the HubSpot CRM v3 Associations API.  Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
