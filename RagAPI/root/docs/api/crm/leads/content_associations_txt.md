# HubSpot CRM API: Leads

This document details the HubSpot CRM API endpoints for managing leads.  Leads are contacts or companies representing potential customers.  Before using this API, ensure leads are set up in your HubSpot account.  See [Understanding the CRM](hypothetical_link_to_crm_guide) for more information on objects, records, properties, and associations.

## API Endpoints

All endpoints are under the `/crm/v3/objects/leads` base URL unless otherwise specified.  Replace placeholders like `{leadsId}` with actual IDs.


### 1. Create Leads

**Endpoint:** `/crm/v3/objects/leads`

**Method:** `POST`

**Request Body:** JSON containing `properties` and optionally `associations`.

**Required Properties:**

* `hs_lead_name`: The lead's full name (string).
* Association with an existing contact (via the `associations` object).  Leads must be associated with a contact.

**Optional Properties:**

* `hs_lead_type`: Lead type (string, e.g., "NEW BUSINESS").
* `hs_lead_label`: Lead status (string, e.g., "WARM").
* Any other custom lead properties.


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
          "associationTypeId": 578 //Default association type ID for contacts.  See documentation for other types.
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

**Endpoint:** `/crm/v3/objects/leads/{leadsId}`

**Method:** `GET`

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including history.
* `associations`: Comma-separated list of associated objects to retrieve.

**Example Request:** `/crm/v3/objects/leads/123?properties=hs_lead_name,hs_lead_type`

**Response:** JSON representing the lead with the specified properties.


**Multiple Leads:**

**Endpoint:** `/crm/v3/objects/leads`

**Method:** `GET`

**Query Parameters:** (Same as individual lead retrieval)

**Response:** JSON array of leads.


**Batch Lead Retrieval:**

**Endpoint:** `/crm/v3/objects/leads/batch/read`

**Method:** `POST`

**Request Body:**  JSON array of lead IDs (using `id` field) or custom unique identifiers (requires `idProperty` parameter).  Cannot retrieve associations.

**Query Parameters:**
* `idProperty`: Specify the name of a custom unique identifier property if not using the default `hs_object_id`.

**Example Request (using hs_object_id):**

```json
{
  "inputs": [
    {"id": "123"},
    {"id": "456"}
  ]
}
```


**Response:** JSON array of leads.


### 3. Update Leads

**Individual Lead:**

**Endpoint:** `/crm/v3/objects/leads/{leadsId}`

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


### 4. Associate Existing Leads with Records

**Endpoint:** `/crm/v3/objects/leads/{leadsId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `PUT`

**Parameters:**

* `{leadsId}`:  The ID of the lead.
* `{toObjectType}`: The type of the object to associate (e.g., "contacts").
* `{toObjectId}`: The ID of the object to associate.
* `{associationTypeId}`: The ID of the association type.  Obtain from the default list or via the Associations API.


### 5. Remove an Association

**Endpoint:** `/crm/v3/objects/leads/{leadsID}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `DELETE`

**Parameters:** (Same as associating leads)


### 6. Delete Leads

**Endpoint:** `/crm/v3/objects/leads/{leadsId}`

**Method:** `DELETE`

**Note:** Deleting leads moves them to the recycle bin.  They can be restored within HubSpot.


## Properties

Leads have default and custom properties.  Retrieve a list of available properties via a `GET` request to `/crm/v3/properties/leads`.

**Common Properties:**

| Property       | Description                                           |
|-----------------|-------------------------------------------------------|
| `hs_lead_name` | The lead's full name.                                |
| `hs_lead_type`  | A dropdown list of lead types.                       |
| `hs_lead_label` | The lead's current status.                           |


## Associations

Leads can be associated with other records (e.g., contacts) and activities.  Use the `associations` object when creating or updating leads, and specific endpoints for managing associations.  See the Associations API for details.


## Limits

Batch operations (create, update, delete) are limited to 100 records per batch.


## Error Handling

The API returns standard HTTP status codes and JSON error responses to indicate success or failure.  Consult the HubSpot API documentation for detailed error codes and handling.
