# HubSpot CRM API: Leads

This document details the HubSpot CRM API endpoints for managing leads.  Leads are contacts or companies representing potential customers.  Before using the API, ensure leads are set up in your HubSpot account.

## Understanding the CRM

For comprehensive information on HubSpot's object, record, property, and association APIs, refer to the [Understanding the CRM](link_to_understanding_crm_guide) guide.  For general CRM database management, see [Managing your CRM database](link_to_crm_management_guide).

## API Endpoints

All endpoints are under the `/crm/v3/objects/leads` base path unless otherwise specified.  Replace `{leadsId}` with the actual lead ID.

### 1. Create Leads

**Endpoint:** `/crm/v3/objects/leads`

**Method:** `POST`

**Request Body:** JSON containing `properties` and optionally `associations`.

**`properties` Object:**  At minimum, requires `hs_lead_name`.  Other properties can be added (see Properties section below).

**`associations` Object:**  Allows associating the new lead with existing contacts or other records.

**Example Request (JSON):**

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
          "associationTypeId": 578 // Example association type ID.  See Associations section below.
        }
      ],
      "to": {
        "id": "YOUR_CONTACT_ID" // ID of an existing contact
      }
    }
  ]
}
```

**Response:** JSON containing the newly created lead's details, including its ID.


### 2. Properties

Lead details are stored in properties.  HubSpot provides default properties; custom properties can also be created.

**Endpoint (retrieve all properties):** `/crm/v3/properties/leads`

**Method:** `GET`

**Response:** JSON listing available lead properties.

**Common Properties:**

| PROPERTY        | DESCRIPTION                                                                     |
|-----------------|---------------------------------------------------------------------------------|
| `hs_lead_name`  | The full name of the lead.                                                     |
| `hs_lead_type`  | A dropdown list of lead types (editable/addable in lead property settings).     |
| `hs_lead_label` | The current status of the lead (editable/addable in lead property settings). |


### 3. Associations

Associate leads with other records using the `associations` object in create requests or dedicated endpoints for existing leads.

**Endpoint (create/update association):** `/crm/v3/objects/leads/{leadsId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `PUT`

**Parameters:**

* `toObjectType`:  The type of object (e.g., `contacts`).
* `toObjectId`: The ID of the object to associate with.
* `associationTypeId`: The type of association.  Find default IDs [here](link_to_default_association_type_ids) or retrieve custom types via the associations API.


**Example (Associating an existing lead with a contact):**  A `PUT` request to the above endpoint with appropriate parameters.


**Endpoint (remove association):** `/crm/v3/objects/leads/{leadsID}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `DELETE`

Removing all primary associations deletes the lead.

### 4. Retrieve Leads

**Endpoint (single lead):** `/crm/v3/objects/leads/{leadsId}`

**Method:** `GET`

**Endpoint (all leads):** `/crm/v3/objects/leads`

**Method:** `GET`

**Endpoint (batch read):** `/crm/v3/objects/leads/batch/read`

**Method:** `POST` (Can't retrieve associations).  Use `idProperty` parameter for custom identifiers; otherwise, it defaults to `hs_object_id`.

**Query Parameters (for individual and all leads endpoints):**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`:  Comma-separated list of properties (including history) to return.
* `associations`: Comma-separated list of association types to retrieve.


### 5. Update Leads

**Endpoint:** `/crm/v3/objects/leads/{leadsId}`

**Method:** `PATCH`

**Request Body:** JSON containing the properties to update.

### 6. Delete Leads

**Endpoint:** `/crm/v3/objects/leads/{leadsId}`

**Method:** `DELETE`

Moves the lead to the recycle bin; it can be restored later in HubSpot.


### 7. Limits

Batch operations (create, update, delete) are limited to 100 records per batch.


##  Error Handling

The API will return standard HTTP status codes (e.g., 400 for bad requests, 404 for not found, etc.) along with JSON error details.  Refer to HubSpot's API documentation for detailed error codes and handling.
