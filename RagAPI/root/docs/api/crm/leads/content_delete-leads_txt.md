# HubSpot CRM API: Leads

This document details the HubSpot CRM API endpoints for managing leads.  Leads are potential customers who have shown interest in your products or services.  This API allows you to create, retrieve, update, and delete lead records, as well as manage their associations with other HubSpot records.

Before using this API, ensure leads are set up in your HubSpot account.  Refer to the [Understanding the CRM](<link_to_understanding_crm_guide>) guide for more information on objects, records, properties, and associations.


## API Endpoints

All endpoints are under the `/crm/v3/objects/leads` base path unless otherwise specified.  You will need a valid HubSpot API key for authentication.


### 1. Create Leads

**Endpoint:** `POST /crm/v3/objects/leads`

**Method:** `POST`

**Request Body:** JSON object with `properties` and optionally `associations`.

* **`properties`:**  An object containing lead properties.  At minimum, `hs_lead_name` (lead name) is required.  Leads *must* be associated with an existing contact.

* **`associations`:** (Optional) An array of objects specifying associations with other records (e.g., contacts).  Each association object requires:
    * `types`: An array of association type objects.  Each object needs `associationCategory` (e.g., `HUBSPOT_DEFINED`) and `associationTypeId` (e.g., 578 for associating with a contact). See [default association types](<link_to_default_association_types>) or use the Associations API to retrieve custom association type IDs.
    * `to`: An object with `id` specifying the ID of the record to associate with.

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

**Response:** JSON object representing the newly created lead, including its ID.


### 2. Retrieve Leads

**Endpoint (Single Lead):** `GET /crm/v3/objects/leads/{leadId}`

**Endpoint (All Leads):** `GET /crm/v3/objects/leads`

**Endpoint (Batch):** `POST /crm/v3/objects/leads/batch/read`

**Method:** `GET` (single & all), `POST` (batch)

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties (including history) to return.
* `associations`: Comma-separated list of association types to return.  (Not supported in batch read)

**Batch Read Parameters (POST):**

* `inputs`: Array of objects, each containing an `id` property representing the lead ID.  Use `idProperty` if using a custom unique identifier property instead of `hs_object_id`.
* `idProperty`: Name of the custom unique identifier property (only needed if not using `hs_object_id`).

**Example Request (Single Lead):**

```
GET /crm/v3/objects/leads/12345?properties=hs_lead_name,hs_lead_type
```

**Response:** JSON object (single lead) or array of JSON objects (all or batch leads).  Only specified properties and associations will be returned.


### 3. Update Leads

**Endpoint:** `PATCH /crm/v3/objects/leads/{leadId}`

**Method:** `PATCH`

**Request Body:** JSON object containing the properties to update.

**Example Request (JSON):**

```json
{
  "properties": {
    "hs_lead_label": "COLD"
  }
}
```

**Response:** JSON object representing the updated lead.


### 4. Associate Existing Leads with Records

**Endpoint:** `PUT /crm/v3/objects/leads/{leadId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `PUT`

* `{leadId}`: ID of the lead.
* `{toObjectType}`: Type of the object to associate with (e.g., `contacts`).
* `{toObjectId}`: ID of the object to associate with.
* `{associationTypeId}`: ID of the association type.

**Response:**  Success or error status.


### 5. Remove an Association

**Endpoint:** `DELETE /crm/v3/objects/leads/{leadId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `DELETE`

* Removing all primary associations will delete the lead.


**Response:** Success or error status.


### 6. Delete Leads

**Endpoint:** `DELETE /crm/v3/objects/leads/{leadId}`  (Individual)

**Method:** `DELETE`

**Note:**  This moves the lead to the recycle bin.  It's not permanently deleted.


**Response:** Success or error status.


## Properties

Leads have several properties, including default HubSpot properties and custom properties.  Use `/crm/v3/properties/leads` (GET request) to retrieve a list of available properties.

| Property          | Description                                                                   |
|----------------------|-------------------------------------------------------------------------------|
| `hs_lead_name`      | Full name of the lead (required for creation).                              |
| `hs_lead_type`     | Lead type (dropdown selection, customizable).                               |
| `hs_lead_label`    | Lead status (dropdown selection, customizable).                              |


## Limits

Batch operations (create, update, delete) are limited to 100 records per batch.


## Error Handling

The API will return standard HTTP status codes and JSON error responses to indicate success or failure.  Check the response body for detailed error messages.


This documentation provides a comprehensive overview. For more detailed information and specific examples, refer to the official HubSpot API documentation.
