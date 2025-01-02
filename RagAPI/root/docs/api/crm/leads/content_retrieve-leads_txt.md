# HubSpot CRM API: Leads

This document describes the HubSpot CRM API endpoints for managing leads.  Leads are potential customers who have shown interest in your products or services.  This API allows you to create, retrieve, update, associate, and delete lead records in your HubSpot account.

Before using the API, ensure leads are set up in your HubSpot account.  Refer to the [Understanding the CRM](link_to_understanding_crm_guide) guide for more information on objects, records, properties, and associations.  Learn how to [manage your CRM database](link_to_managing_crm_database) for general information.


## API Endpoints

All endpoints are under the `/crm/v3/objects/leads` base path unless otherwise specified.  Replace placeholders like `{leadsId}` with the actual ID.


### 1. Create Leads (POST `/crm/v3/objects/leads`)

Creates a new lead. The request body must include:

* **`properties` (object):**  Lead details.  At minimum, `hs_lead_name` is required.  The lead must be associated with an existing contact.
* **`associations` (array, optional):**  Associates the lead with existing records.  See "Associations" section below.


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
          "associationTypeId": 578 //  Association type ID for contact (check HubSpot documentation for current ID)
        }
      ],
      "to": {
        "id": "YOUR_CONTACT_ID" // ID of the existing contact
      }
    }
  ]
}
```

**Response (JSON):**  A JSON object representing the newly created lead, including its ID and properties.


### 2. Properties (GET `/crm/v3/properties/leads`)

Retrieves a list of all available lead properties.

**Request:**  A simple GET request.

**Response (JSON):** A list of property objects, each containing details like name, type, and description.


**Common Lead Properties:**

| PROPERTY        | DESCRIPTION                                                                    |
|-----------------|--------------------------------------------------------------------------------|
| `hs_lead_name`  | The full name of the lead.                                                    |
| `hs_lead_type`  | A dropdown list of lead types (editable in HubSpot settings).                  |
| `hs_lead_label` | The current status of the lead (editable in HubSpot settings).                 |



### 3. Associations

Associates leads with existing records (e.g., contacts) or activities.

**3.1 Create Association (PUT `/crm/v3/objects/leads/{leadsId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)**

Associates an existing lead with a record.

* `{leadsId}`:  The ID of the lead.
* `{toObjectType}`: The type of the object to associate (e.g., "contacts").
* `{toObjectId}`: The ID of the object to associate.
* `{associationTypeId}`: The ID of the association type.  See the default association type IDs [here](link_to_association_type_ids) or use the associations API to retrieve custom association types.


**3.2 Remove Association (DELETE `/crm/v3/objects/leads/{leadsID}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)**

Removes an association between a lead and another record.  Removing all primary associations deletes the lead.


### 4. Retrieve Leads

**4.1 Retrieve Individual Lead (GET `/crm/v3/objects/leads/{leadsId}`)**

Retrieves a single lead by ID.

**4.2 Retrieve All Leads (GET `/crm/v3/objects/leads`)**

Retrieves a list of all leads.


**Query Parameters (for both 4.1 and 4.2):**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties (including history) to return.
* `associations`: Comma-separated list of associated objects to retrieve.


**4.3 Batch Read Leads (POST `/crm/v3/objects/leads/batch/read`)**

Retrieves a batch of leads.  Does not retrieve associations.  Uses `idProperty` to specify if using a custom unique identifier.


### 5. Update Leads (PATCH `/crm/v3/objects/leads/{leadsId}`)

Updates an existing lead.  Include only the properties you want to modify in the request body.


### 6. Delete Leads (DELETE `/crm/v3/objects/leads/{leadsId}`)

Deletes a lead (moves to recycling bin).



## Limits

Batch operations (create, update, delete) are limited to 100 records per batch.


## Error Handling

The API returns standard HTTP status codes and JSON error responses to indicate success or failure.  Check the HubSpot API documentation for details on error handling and response codes.
