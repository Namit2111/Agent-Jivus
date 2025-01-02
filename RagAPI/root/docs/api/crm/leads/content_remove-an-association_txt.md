# HubSpot CRM API: Leads

This document details the HubSpot CRM API endpoints for managing leads.  Leads in HubSpot represent potential customers who have shown interest in your products or services.  This API allows creation, retrieval, updating, association, and deletion of lead records.

**Before using the API:** Ensure leads are set up in your HubSpot account.  Refer to the [Understanding the CRM](link_to_understanding_crm_guide) guide for more information on objects, records, properties, and associations.  Learn how to [manage your CRM database](link_to_managing_crm_database) for general information.


## API Endpoints

All endpoints below are part of the `/crm/v3/objects/leads` base path unless otherwise specified.  Replace `{leadsId}` with the actual lead ID.  All requests require appropriate HubSpot API key authentication.


### 1. Create Leads

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/leads`

**Request Body:**  JSON containing `properties` and optionally `associations`.

* **`properties` (required):**  An object containing lead properties.  At minimum, `hs_lead_name` (lead name) is required.  The lead must also be associated with an existing contact.  Only users with a seat can create leads.

* **`associations` (optional):** An array of objects associating the lead with other records (e.g., contacts).  Each object requires:
    * `to`:  An object with `id` specifying the ID of the associated record.
    * `types`: An array of objects, each specifying:
        * `associationCategory`: `"HUBSPOT_DEFINED"`
        * `associationTypeId`: The ID of the association type (see default IDs or use the Associations API to retrieve custom type IDs).

**Example Request (Creating a warm lead):**

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
          "associationTypeId": 578 // Example association type ID - Replace with correct ID
        }
      ],
      "to": {
        "id": "YOUR_CONTACT_ID" // Replace with the ID of an existing contact
      }
    }
  ]
}
```

**Response:** A JSON object representing the created lead, including its ID and properties.


### 2. Retrieve Leads

**Method:** `GET` (individual), `GET` (all), `POST` (batch)

**Endpoint:**
* **Individual:** `/crm/v3/objects/leads/{leadsId}`
* **All:** `/crm/v3/objects/leads`
* **Batch:** `/crm/v3/objects/leads/batch/read`

**Query Parameters (for GET requests):**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical data.
* `associations`: Comma-separated list of association types to return associated IDs for.

**Batch Read Parameters (for POST request):**

* `inputs`: Array of lead IDs to retrieve.  If using a custom unique identifier property, also specify `idProperty`.
* `idProperty`: The name of the custom property used as a unique identifier (only needed if not using `hs_object_id`).

**Response:**
* **Individual/All:** JSON object representing the lead(s), including properties and optionally associations.
* **Batch:** JSON object with an array of lead objects.


### 3. Update Leads

**Method:** `PATCH` (individual), `POST` (batch - not detailed here)

**Endpoint:** `/crm/v3/objects/leads/{leadsId}`

**Request Body:** JSON containing the properties to update.

**Response:** JSON object representing the updated lead.


### 4. Associate Existing Leads with Records

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/leads/{leadsId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

* `{toObjectType}`: The type of object to associate (e.g., `contacts`).
* `{toObjectId}`: The ID of the object to associate.
* `{associationTypeId}`: The ID of the association type.


**Response:**  Success/failure indication.


### 5. Remove an Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/leads/{leadsId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Response:** Success/failure indication.  Removing all primary associations deletes the lead.


### 6. Delete Leads

**Method:** `DELETE` (individual), `POST` (batch - not detailed here)

**Endpoint:** `/crm/v3/objects/leads/{leadsId}`

**Response:** Success/failure indication.  Leads are moved to the recycling bin; they can be restored.


## Properties

Leads have default and custom properties.  Retrieve available properties via `GET /crm/v3/properties/leads`.

| Property        | Description                                         |
|-----------------|-----------------------------------------------------|
| `hs_lead_name`  | Lead's full name (required for creation)            |
| `hs_lead_type`  | Lead type (dropdown, customizable)                  |
| `hs_lead_label` | Lead status (dropdown, customizable)                |


## Associations

The Associations API ([link_to_associations_api]) provides details on association types and management.  Default association type IDs are available in the documentation.


## Limits

Batch operations (create, update, delete) are limited to 100 records per batch.

This documentation provides a concise overview.  Refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications. Remember to replace placeholder values like `YOUR_CONTACT_ID` with actual values.
