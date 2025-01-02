# HubSpot CRM API: Leads

This document details the HubSpot CRM API endpoints for managing leads.  Leads are contacts or companies representing potential customers.  Before using the API, ensure leads are set up in your HubSpot account.  See [Understanding the CRM](link-to-understanding-crm-guide) for more on objects, records, properties, and associations.

## API Endpoints

All endpoints are under the `/crm/v3/objects/leads` base path unless otherwise specified.  Remember to replace placeholders like `{leadsId}` with actual values.

### 1. Create Leads

**Endpoint:** `POST /crm/v3/objects/leads`

**Method:** `POST`

**Request Body:** JSON containing `properties` and optionally `associations`.

**`properties` object:**  Contains lead details.  `hs_lead_name` is required.  Other properties can be added (see "Properties" section below).

**`associations` object (optional):** Associates the lead with existing contacts or activities.

**Example Request (creating a warm lead):**

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
          "associationTypeId": 578 // Example association type ID.  See documentation for details.
        }
      ],
      "to": {
        "id": "YOUR_CONTACT_ID" // Replace with existing contact ID
      }
    }
  ]
}
```

**Response:**  A JSON object representing the newly created lead, including its ID.


### 2. Properties

**Endpoint (retrieve all properties):** `GET /crm/v3/properties/leads`

**Method:** `GET`

**Response:**  A JSON array of all available lead properties.

**Common Lead Properties:**

| PROPERTY         | DESCRIPTION                                                                     |
|-----------------|---------------------------------------------------------------------------------|
| `hs_lead_name`   | Full name of the lead (required for creation).                               |
| `hs_lead_type`   | Lead type (dropdown; customizable in HubSpot settings).                         |
| `hs_lead_label`  | Current status of the lead (dropdown; customizable in HubSpot settings).       |


### 3. Retrieve Leads

**Endpoint (single lead):** `GET /crm/v3/objects/leads/{leadsId}`

**Endpoint (all leads):** `GET /crm/v3/objects/leads`

**Endpoint (batch read):** `POST /crm/v3/objects/leads/batch/read`

**Method:** `GET` (single/all), `POST` (batch)

**Query Parameters (single/all):**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return with history.
* `associations`: Comma-separated list of associated objects to retrieve.

**Query Parameters (batch read):**

* `idProperty`:  The property used for unique identification (default is `id`/`hs_object_id`).


**Response:** JSON representing the requested lead(s).  The batch endpoint does not support associations.


### 4. Update Leads

**Endpoint:** `PATCH /crm/v3/objects/leads/{leadsId}`

**Method:** `PATCH`

**Request Body:** JSON containing the properties to update.

**Example Request:**

```json
{
  "properties": {
    "hs_lead_label": "HOT"
  }
}
```

**Response:** JSON representing the updated lead.

### 5. Associate Existing Leads with Records

**Endpoint:** `PUT /crm/v3/objects/leads/{leadsId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `PUT`

**Parameters:**

* `{toObjectType}`: Type of object to associate (e.g., `contacts`).
* `{toObjectId}`: ID of the object to associate.
* `{associationTypeId}`: ID of the association type (see HubSpot documentation for default IDs or use the associations API to retrieve custom IDs).

**Response:**  Success or error message.


### 6. Remove an Association

**Endpoint:** `DELETE /crm/v3/objects/leads/{leadsID}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `DELETE`

**Parameters:** Same as associating leads.

**Response:**  Success or error message.  Removing all primary associations deletes the lead.


### 7. Delete Leads

**Endpoint:** `DELETE /crm/v3/objects/leads/{leadsId}`

**Method:** `DELETE`

**Response:**  Success or error message.  Leads are moved to the recycle bin.


### 8. Limits

Batch operations (create, update, delete) are limited to 100 records per request.


##  Associations API

The Associations API allows management of relationships between leads and other HubSpot objects. Refer to the separate HubSpot documentation for details on this API.


This documentation provides a concise overview. Refer to the official HubSpot API documentation for complete details, error handling, and authentication information.
