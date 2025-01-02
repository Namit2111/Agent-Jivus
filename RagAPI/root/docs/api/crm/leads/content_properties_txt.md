# HubSpot CRM API: Leads

This document details the HubSpot CRM API endpoints for managing leads.  Leads are contacts or companies who have shown interest in your products or services.  Before using this API, ensure leads are set up in your HubSpot account.  See [Understanding the CRM](hypothetical_link_to_crm_guide) and [Managing your CRM database](hypothetical_link_to_crm_management) for more context.


## API Endpoints

All endpoints below are under the `/crm/v3/objects/leads` base path unless otherwise specified.  Replace `{leadsId}` with the actual lead ID.  HTTP methods are indicated.

### 1. Create Leads (POST)

Creates a new lead.  The request body requires `properties` and optionally `associations`.

**Request Body:**

```json
{
  "properties": {
    "hs_lead_name": "Jane Doe", // Required: Lead's full name
    "hs_lead_type": "NEW BUSINESS", // Example custom property
    "hs_lead_label": "WARM" // Example custom property
  },
  "associations": [
    {
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 578 // Example association type ID. See below for details.
        }
      ],
      "to": {
        "id": "YOUR_CONTACT_ID" // Required: ID of an existing contact to associate with.
      }
    }
  ]
}
```

**Response:**  A JSON object representing the newly created lead, including its ID and properties.

**Requirements:**

* `hs_lead_name` property is mandatory.
* Lead must be associated with an existing contact.
* Only users with a seat can assign leads (leads are managed via workspace).


**Example Association Type IDs:**  Default association type IDs can be found at [Hypothetical link to default association types].  Custom association types can be retrieved via the Associations API.


### 2. Properties (GET)

Retrieves available lead properties.

**Endpoint:** `/crm/v3/properties/leads` (GET)

**Response:** A JSON array of available properties.  Each property object will contain details like name, type, and description.

**Common Properties:**

| PROPERTY       | DESCRIPTION                                                                |
|-----------------|----------------------------------------------------------------------------|
| `hs_lead_name` | The full name of the lead.                                                  |
| `hs_lead_type` | A dropdown list of lead types (customizable in your lead property settings). |
| `hs_lead_label` | The current status of the lead (customizable in your lead property settings). |


### 3. Retrieve Leads (GET)

Retrieves leads individually or in batches.

**Individual Lead (GET):** `/crm/v3/objects/leads/{leadsId}`

**All Leads (GET):** `/crm/v3/objects/leads`

**Batch Read (POST):** `/crm/v3/objects/leads/batch/read`

**Query Parameters (GET requests):**

| Parameter           | Description                                                                                             |
|----------------------|---------------------------------------------------------------------------------------------------------|
| `properties`        | Comma-separated list of properties to return.  Missing properties are omitted from the response.       |
| `propertiesWithHistory` | Comma-separated list of current and historical properties to return. Missing properties are omitted. |
| `associations`      | Comma-separated list of associated objects to retrieve IDs for.  Non-existent associations are omitted.|


**Batch Read (POST) parameters:**

The `idProperty` parameter is only required if you're using a custom unique identifier property instead of the default `id` (which refers to `hs_object_id`).

**Response:** A JSON object or array representing the requested lead(s), including properties and associated objects (if requested).


### 4. Update Leads (PATCH)

Updates an existing lead.

**Endpoint:** `/crm/v3/objects/leads/{leadsId}` (PATCH)

**Request Body:**  A JSON object containing the properties to update. Only the properties you want to change need to be included.

**Response:** A JSON object representing the updated lead.

### 5. Associate Existing Leads with Records (PUT)

Associates a lead with another CRM record or activity.

**Endpoint:** `/crm/v3/objects/leads/{leadsId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}` (PUT)

**Parameters:**

* `{toObjectType}`:  The type of the object to associate (e.g., `contacts`).
* `{toObjectId}`: The ID of the object to associate.
* `{associationTypeId}`: The ID of the association type.  See [Hypothetical link to default association types] or use the Associations API to retrieve custom types.


### 6. Remove an Association (DELETE)

Removes an association between a lead and another record or activity.

**Endpoint:** `/crm/v3/objects/leads/{leadsId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}` (DELETE)

**Warning:** Removing all primary associations from a lead will delete the lead.


### 7. Delete Leads (DELETE)

Deletes a lead (moves it to the recycling bin).

**Endpoint:** `/crm/v3/objects/leads/{leadsId}` (DELETE)

**Note:**  Batch delete operations are limited to 100 leads.  Refer to HubSpot documentation for batch delete endpoints.


## Rate Limits

Batch operations (create, update, delete) are limited to 100 records per batch.  Check HubSpot's documentation for specific rate limits.
