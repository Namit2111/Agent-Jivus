# HubSpot CRM API: Leads

This document details the HubSpot CRM API endpoints for managing leads.  Leads represent potential customers who have shown interest in your products or services.  Before using the API, ensure leads are set up in your HubSpot account.  See [Understanding the CRM](link_to_understanding_crm_guide) for more information on objects, records, properties, and associations.


## API Endpoints

All endpoints are under the `/crm/v3/objects/leads` base path unless otherwise specified.  Replace `{leadsId}` with the actual lead ID.  All requests require proper authentication.


### 1. Create Leads

**Method:** `POST`
**Endpoint:** `/crm/v3/objects/leads`

Creates a new lead.  The request body must include:

* **`properties` (object):**  Lead details.  Requires `hs_lead_name`.  Should only be assigned to a user with a seat (leads can only be worked via the workspace).
* **`associations` (array, optional):**  Associates the new lead with existing contacts or other records.

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
          "associationTypeId": 578 // Example association type ID.  See below for details.
        }
      ],
      "to": {
        "id": "YOUR_CONTACT_ID" // ID of the existing contact to associate with
      }
    }
  ]
}
```

**Response (JSON - Example):**

```json
{
  "id": "newly_created_lead_id",
  "properties": {
    "hs_lead_name": "Jane Doe",
    "hs_lead_type": "NEW BUSINESS",
    "hs_lead_label": "WARM"
  },
  // ... other properties ...
}
```

**Association Type IDs:** Default association type IDs are listed [here](link_to_default_association_types).  Custom association types can be retrieved using the associations API ([link to associations API documentation](link_to_associations_api)).


### 2. Retrieve Leads

**a) Individual Lead:**

**Method:** `GET`
**Endpoint:** `/crm/v3/objects/leads/{leadsId}`

Retrieves a single lead by its ID.

**Query Parameters:**

* `properties` (string): Comma-separated list of properties to return.
* `propertiesWithHistory` (string): Comma-separated list of properties (including history) to return.
* `associations` (string): Comma-separated list of associated objects to retrieve.


**b) All Leads:**

**Method:** `GET`
**Endpoint:** `/crm/v3/objects/leads`

Retrieves a list of all leads.  Uses the same query parameters as retrieving an individual lead.

**c) Batch Read Leads:**

**Method:** `POST`
**Endpoint:** `/crm/v3/objects/leads/batch/read`

Retrieves a batch of leads.  Cannot retrieve associations.  Uses `input` parameter as a JSON array of IDs. Optionally include `idProperty` if using a custom unique identifier property instead of `hs_object_id`.

**Request Body Example (JSON):**

```json
{
  "inputs": [
    {"id": "lead_id_1"},
    {"id": "lead_id_2"}
  ]
}
```


### 3. Update Leads

**a) Individual Lead:**

**Method:** `PATCH`
**Endpoint:** `/crm/v3/objects/leads/{leadsId}`

Updates an existing lead.  The request body contains the properties to update.

**Request Body Example (JSON):**

```json
{
  "properties": {
    "hs_lead_label": "COLD"
  }
}
```


### 4. Associate Existing Leads with Records

**Method:** `PUT`
**Endpoint:** `/crm/v3/objects/leads/{leadsId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

Associates an existing lead with another record (e.g., contact).

* `{toObjectType}`: The type of object to associate with (e.g., `contacts`).
* `{toObjectId}`: The ID of the object to associate with.
* `{associationTypeId}`: The ID of the association type.


### 5. Remove an Association

**Method:** `DELETE`
**Endpoint:** `/crm/v3/objects/leads/{leadsId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

Removes an association between a lead and another record.  Removing all primary associations deletes the lead.


### 6. Delete Leads

**Method:** `DELETE`
**Endpoint:** `/crm/v3/objects/leads/{leadsId}`

Deletes a lead (moves it to the recycling bin).


## Properties

Lead details are stored in properties.  HubSpot provides default properties (like `hs_lead_name`, `hs_lead_type`, `hs_lead_label`), and you can create custom properties.  Retrieve a list of all available properties with a `GET` request to `/crm/v3/properties/leads`.


## Associations

Leads can be associated with other HubSpot records (e.g., contacts, companies) and activities.  The `associations` object in create/update requests specifies these relationships.


## Limits

Batch operations (create, update, delete) are limited to 100 records per batch.


## Error Handling

(Add a section describing error responses from the API, including status codes and error messages.)


This documentation provides a comprehensive overview. Refer to the HubSpot API documentation for complete details and the most up-to-date information.  Remember to replace placeholder values like `YOUR_CONTACT_ID` and  `{leadsId}` with actual values.
