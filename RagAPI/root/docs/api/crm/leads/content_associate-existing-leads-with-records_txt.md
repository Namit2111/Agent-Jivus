# HubSpot CRM API: Leads

This document details the HubSpot CRM API endpoints for managing leads.  Leads represent potential customers who have shown interest in your products or services.  Before using these APIs, ensure leads are set up in your HubSpot account.  Refer to the [Understanding the CRM](LINK_TO_UNDERSTANDING_CRM_GUIDE) guide for more information on objects, records, properties, and associations.


## API Endpoints

All endpoints are under the `/crm/v3/objects/leads` base path unless otherwise specified.  Replace `{leadsId}` with the specific lead ID.  HTTP methods are indicated for each operation.


### 1. Create Leads (POST `/crm/v3/objects/leads`)

Creates a new lead.  The request body must include:

* **`properties` (object):**  Contains lead details.  Requires `hs_lead_name`.  Should only be assigned to a user with a seat (leads can only be worked via the workspace).
* **`associations` (array, optional):**  Associates the lead with existing records.  See [Associations](#associations) section for details.

**Request Body Example (JSON):**

```json
{
  "properties": {
    "hs_lead_name": "Jane Doe",
    "hs_lead_type": "NEW BUSINESS",
    "hs_lead_label": "WARM"
  },
  "associations": [
    {
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 578 // Example ID, check HubSpot documentation for current values.
        }
      ],
      "to": {
        "id": "YOUR_CONTACT_ID" // ID of an existing contact
      }
    }
  ]
}
```

**Response (JSON - Example):**

```json
{
  "id": "12345",
  "properties": {
    "hs_lead_name": "Jane Doe",
    "hs_lead_type": "NEW BUSINESS",
    "hs_lead_label": "WARM"
  },
  // ... other properties ...
}
```


### 2. Properties (GET `/crm/v3/properties/leads`)

Retrieves a list of all available lead properties (both default and custom).

**Request:**  A simple GET request to the endpoint.

**Response (JSON - Example):**

```json
[
  {
    "name": "hs_lead_name",
    "label": "Lead Name",
    "type": "STRING",
    // ... other properties ...
  },
  {
    "name": "hs_lead_type",
    "label": "Lead Type",
    "type": "SELECT",
    // ... other properties ...
  }
  // ... other properties ...
]
```

**Common Lead Properties:**

| PROPERTY         | DESCRIPTION                                                              |
|-----------------|--------------------------------------------------------------------------|
| `hs_lead_name`  | The full name of the lead.                                              |
| `hs_lead_type`  | A dropdown list of lead types (editable in lead property settings).      |
| `hs_lead_label` | The current status of the lead (editable in lead property settings).     |


### 3. Associations

**3.1. Associate Existing Leads with Records (PUT `/crm/v3/objects/leads/{leadsId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)**

Associates a lead with another CRM record or activity.

* `{toObjectType}`: The type of object (e.g., `contacts`).
* `{toObjectId}`: The ID of the object to associate.
* `{associationTypeId}`: The type of association.  Find default IDs [here](LINK_TO_DEFAULT_ASSOCIATION_IDS) or retrieve custom IDs via the Associations API.

**3.2. Remove an Association (DELETE `/crm/v3/objects/leads/{leadsID}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)**

Removes an association. Removing all primary associations deletes the lead.

**3.3.  Associations in Create/Retrieve:**  The `associations` object in the create request (section 1) and the `associations` query parameter in the retrieve requests (section 4) control association handling.


### 4. Retrieve Leads

**4.1. Retrieve Individual Lead (GET `/crm/v3/objects/leads/{leadsId}`)**

Retrieves a single lead by its ID.

**4.2. Retrieve All Leads (GET `/crm/v3/objects/leads`)**

Retrieves a list of all leads.

**4.3. Batch Read Leads (POST `/crm/v3/objects/leads/batch/read`)**

Retrieves a batch of leads by ID.  Cannot retrieve associations. Use `idProperty` for custom unique identifiers.


**Query Parameters (for 4.1 and 4.2):**

| Parameter           | Description                                                                  |
|--------------------|------------------------------------------------------------------------------|
| `properties`        | Comma-separated list of properties to return.                             |
| `propertiesWithHistory` | Comma-separated list of properties (including history) to return.             |
| `associations`      | Comma-separated list of associated objects to retrieve IDs for.             |


### 5. Update Leads (PATCH `/crm/v3/objects/leads/{leadsId}`)

Updates an existing lead.  The request body contains the properties to update.


### 6. Delete Leads (DELETE `/crm/v3/objects/leads/{leadsId}`)

Deletes a lead (moves it to the recycling bin).


### 7. Limits

Batch operations (create, update, delete) are limited to 100 records per batch.


##  Error Handling

The API will return appropriate HTTP status codes (e.g., 400 Bad Request, 404 Not Found, 500 Internal Server Error) along with JSON error messages.  Refer to HubSpot's API documentation for detailed error codes and descriptions.


This documentation provides a concise overview.  Consult the official HubSpot API documentation for the most up-to-date information, including detailed descriptions of all properties, association types, and error handling.  Remember to replace placeholder IDs (`YOUR_CONTACT_ID`, etc.) with your actual values.
