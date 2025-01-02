# HubSpot CRM API: Leads

This document details the HubSpot CRM API endpoints for managing leads.  Leads are contacts or companies representing potential customers.  Before using the API, ensure leads are set up in your HubSpot account.  See [Understanding the CRM](link_to_understanding_crm_guide) and [Managing your CRM database](link_to_managing_crm_database) for background information.

## Endpoints

### 1. Create Leads

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/leads`

**Request Body:** JSON containing `properties` and optionally `associations`.

* **`properties` (required):**  An object containing lead properties.  At a minimum, `hs_lead_name` is required.  Leads should be associated with an existing contact and assigned to a user with a seat.

* **`associations` (optional):** An array of objects associating the lead with existing records or activities.  See the "Associations" section below for details.

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
          "associationTypeId": 578
        }
      ],
      "to": {
        "id": "YOUR_CONTACT_ID"
      }
    }
  ]
}
```

**Response:**  A JSON object representing the newly created lead, including its ID.


### 2. Retrieve Leads

**Individual Lead:**

* **Method:** `GET`
* **Endpoint:** `/crm/v3/objects/leads/{leadId}`
* **Query Parameters:**
    * `properties`: Comma-separated list of properties to return.
    * `propertiesWithHistory`: Comma-separated list of properties (including history) to return.
    * `associations`: Comma-separated list of associated objects to retrieve.

**All Leads:**

* **Method:** `GET`
* **Endpoint:** `/crm/v3/objects/leads`
* **Query Parameters:** Same as individual lead retrieval.

**Batch Lead Retrieval:**

* **Method:** `POST`
* **Endpoint:** `/crm/v3/objects/leads/batch/read`
* **Request Body:** JSON array of lead IDs.  Use `idProperty` parameter if using a custom unique identifier instead of `hs_object_id`.
* **Query Parameter:** `idProperty` (optional): The name of the custom property used as the unique identifier.
* **Note:** Associations cannot be retrieved using the batch endpoint.

**Example Response (Individual Lead):**

```json
{
  "id": "12345",
  "properties": {
    "hs_lead_name": "Jane Doe",
    "hs_lead_type": "NEW BUSINESS"
  }
}
```


### 3. Update Leads

**Individual Lead:**

* **Method:** `PATCH`
* **Endpoint:** `/crm/v3/objects/leads/{leadId}`
* **Request Body:** JSON containing the properties to update.


### 4. Associate Existing Leads with Records

* **Method:** `PUT`
* **Endpoint:** `/crm/v3/objects/leads/{leadId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`
* **Parameters:**
    * `leadId`: ID of the lead.
    * `toObjectType`: Type of the object to associate (e.g., "contacts").
    * `toObjectId`: ID of the object to associate.
    * `associationTypeId`: ID of the association type.  See [Default Association Type IDs](link_to_default_association_ids) or use the `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels` endpoint to retrieve custom types.

### 5. Remove an Association

* **Method:** `DELETE`
* **Endpoint:** `/crm/v3/objects/leads/{leadId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`
* **Warning:** Removing all primary associations deletes the lead.

### 6. Delete Leads

* **Method:** `DELETE`
* **Endpoint:** `/crm/v3/objects/leads/{leadId}`


## Properties

Lead details are stored in properties.  See [Default HubSpot Lead Properties](link_to_default_properties) and how to [Create Custom Lead Properties](link_to_custom_properties).  Use a `GET` request to `/crm/v3/properties/leads` to retrieve a list of all available properties.  Common properties include:

| PROPERTY       | DESCRIPTION                                                                     |
|-----------------|---------------------------------------------------------------------------------|
| `hs_lead_name` | The full name of the lead. (Required when creating a lead)                     |
| `hs_lead_type` | A dropdown list of lead types.                                                  |
| `hs_lead_label`| The current status of the lead.                                                |


## Associations

Associating leads with other records (e.g., contacts) is done using the `associations` object in the request body.  This object requires a `to` object specifying the record ID and `types` specifying the association category and type ID.  Refer to the [Associations API](link_to_associations_api) for more details.


## Limits

Batch operations (create, update, delete) are limited to 100 records per batch.


**Note:**  Replace `link_to_...` placeholders with actual links to relevant HubSpot documentation pages.
