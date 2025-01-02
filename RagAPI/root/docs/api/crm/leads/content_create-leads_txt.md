# HubSpot CRM API: Leads

This document details the HubSpot CRM API endpoints for managing leads.  Leads are contacts or companies who've shown interest in your products or services.  Before using this API, ensure leads are set up in your HubSpot account.  See the [Understanding the CRM](link_to_understanding_crm_guide) guide for more on objects, records, properties, and associations.


## API Endpoints

All endpoints are under the `/crm/v3/objects/leads` base path unless otherwise specified.  Replace `{leadsId}` with the actual lead ID.


### 1. Create Leads

**Endpoint:** `/crm/v3/objects/leads`

**Method:** `POST`

**Request Body:** JSON containing `properties` and optionally `associations`.

* **`properties` (required):**  An object containing lead details.  `hs_lead_name` (lead name) is required.  It should also be associated with an existing contact and assigned to a user with a seat.

* **`associations` (optional):** An array of objects associating the new lead with existing records or activities.  See the Associations section below.

**Example Request:**

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
          "associationTypeId": 578 // Example ID, check HubSpot documentation for current IDs
        }
      ],
      "to": {
        "id": "YOUR_CONTACT_ID"
      }
    }
  ]
}
```

**Response:** A JSON object representing the newly created lead, including its ID.


### 2. Properties

**Endpoint:** `/crm/v3/properties/leads`

**Method:** `GET`

**Response:** A JSON array of available lead properties (default and custom).


**Common Lead Properties:**

| PROPERTY         | DESCRIPTION                                                                   |
|-----------------|-------------------------------------------------------------------------------|
| `hs_lead_name`   | The full name of the lead.                                                   |
| `hs_lead_type`   | A dropdown list of lead types (editable in lead property settings).           |
| `hs_lead_label`  | The current status of the lead (editable in lead property settings).         |


### 3. Associations

Associates leads with other records (e.g., contacts) or activities.

**Creating Associations (during lead creation or update):** Included in the `associations` array within the request body of the create or update endpoints (see above).

**Associating Existing Leads:**

**Endpoint:** `/crm/v3/objects/leads/{leadsId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `PUT`

* `{toObjectType}`: The type of object to associate (e.g., "contacts").
* `{toObjectId}`:  The ID of the object to associate.
* `{associationTypeId}`:  The ID specifying the association type.  See the [default association types](link_to_default_association_types) or use the Associations API to retrieve custom type IDs.

**Removing Associations:**

**Endpoint:** `/crm/v3/objects/leads/{leadsId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `DELETE`

Removing all primary associations deletes the lead.


### 4. Retrieve Leads

**Individual Lead:**

**Endpoint:** `/crm/v3/objects/leads/{leadsId}`

**Method:** `GET`

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties (including history) to return.
* `associations`: Comma-separated list of associated objects to retrieve IDs for.

**Batch Lead Retrieval:**

**Endpoint:** `/crm/v3/objects/leads/batch/read`

**Method:** `POST`

**Request Body:** JSON array of lead IDs.  Can use `idProperty` to specify a custom unique identifier property if not using `hs_object_id`.  Associations are not retrievable via this endpoint.


**All Leads (List):**

**Endpoint:** `/crm/v3/objects/leads`

**Method:** `GET`

**Query Parameters:** Same as individual lead retrieval.



### 5. Update Leads

**Individual Lead:**

**Endpoint:** `/crm/v3/objects/leads/{leadsId}`

**Method:** `PATCH`

**Request Body:** JSON containing the properties to update.


### 6. Delete Leads

**Individual Lead:**

**Endpoint:** `/crm/v3/objects/leads/{leadsId}`

**Method:** `DELETE`

Leads are moved to the recycling bin, not permanently deleted.


### 7. Limits

Batch operations (create, update, delete) are limited to 100 records per batch.


##  Error Handling

The API will return appropriate HTTP status codes (e.g., 400 Bad Request, 404 Not Found, 500 Internal Server Error) along with JSON error messages. Consult the HubSpot API documentation for detailed error codes and their meanings.


This documentation provides a concise overview.  Refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications.  Remember to replace placeholder values like `YOUR_CONTACT_ID` with actual values.
