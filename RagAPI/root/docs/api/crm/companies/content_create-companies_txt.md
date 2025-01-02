# HubSpot CRM API: Companies

This document details the HubSpot CRM API endpoints for managing companies.  Companies in HubSpot store information about organizations interacting with your business.  These endpoints allow creation, management, and synchronization of company data between HubSpot and other systems.

## Understanding the CRM (Prerequisites)

Before using these APIs, familiarize yourself with HubSpot's [Understanding the CRM](link-to-hubspot-crm-guide) and [managing your CRM database](link-to-hubspot-crm-management).  Understanding objects, records, properties, and associations is crucial.

## API Endpoints

All endpoints use the `/crm/v3/objects/companies` base path unless otherwise specified.  Requests require appropriate authentication.

### 1. Create Companies

**Endpoint:** `POST /crm/v3/objects/companies`

**Method:** `POST`

**Request Body:** JSON

Requires at least `name` or `domain`.  `domain` is strongly recommended as the primary unique identifier to prevent duplicates.  Multiple domains can be added using the `hs_additional_domains` field (e.g., `"hs_additional_domains": "domain.com;domain2.com"`).

**Example Request Body:**

```json
{
  "properties": {
    "name": "HubSpot",
    "domain": "hubspot.com",
    "city": "Cambridge",
    "industry": "Technology",
    "phone": "555-555-555",
    "state": "Massachusetts",
    "lifecyclestage": "51439524" //Use internal name or ID for lifecycle stage
  },
  "associations": [
    {
      "to": { "id": 101 },
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 280 }]
    },
    {
      "to": { "id": 556677 },
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 185 }]
    }
  ]
}
```

**Response:** JSON containing the newly created company's details, including its `id`.

**Associations:**  The `associations` object allows associating the new company with existing records (contacts, deals) or activities (meetings, notes).  `to.id` specifies the associated record/activity ID.  `types` define the association type (use default IDs or retrieve custom IDs via the associations API).


### 2. Retrieve Companies

**Endpoint (Single Company):** `GET /crm/v3/objects/companies/{companyId}`

**Endpoint (List of Companies):** `GET /crm/v3/objects/companies`

**Endpoint (Batch Read):** `POST /crm/v3/objects/companies/batch/read`

**Method:** `GET` (single/list), `POST` (batch)

**Query Parameters (Single/List):**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return with history.
* `associations`: Comma-separated list of association types to retrieve.

**Request Body (Batch):** JSON

```json
//Example with record IDs
{
  "properties": ["name", "domain"],
  "inputs": [{"id": "56789"}, {"id": "23456"}]
}

// Example with a custom unique property
{
  "properties": ["name", "domain"],
  "idProperty": "uniquepropertyexample",
  "inputs": [{"id": "abc"}, {"id": "def"}]
}
```

**Response:** JSON containing company details (single) or an array of company details (list/batch).  Batch endpoint does not support associations.


### 3. Update Companies

**Endpoint:** `PATCH /crm/v3/objects/companies/{companyId}`

**Method:** `PATCH`

**Request Body:** JSON containing the properties to update.

**Note:** Updating `lifecyclestage` only allows moving *forward* in the stage order.  To move backward, clear the existing value first.

### 4. Associate Existing Companies

**Endpoint:** `PUT /crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `PUT`

**Parameters:**

* `{companyId}`: ID of the company.
* `{toObjectType}`: Type of object to associate (e.g., "contacts").
* `{toObjectId}`: ID of the object to associate.
* `{associationTypeId}`: ID of the association type (see default list or retrieve via associations API).


### 5. Remove Association

**Endpoint:** `DELETE /crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `DELETE`

### 6. Pin an Activity

**Endpoint:** `PATCH /crm/v3/objects/companies/{companyId}`

**Method:** `PATCH`

**Request Body:**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789 // ID of the activity to pin
  }
}
```

Can also be included in `POST /crm/v3/objects/companies` to pin on creation.


### 7. Delete Companies

**Endpoint:** `DELETE /crm/v3/objects/companies/{companyId}`

**Method:** `DELETE`

Moves the company to the recycling bin; it can be restored later.


## Error Handling

The API will return appropriate HTTP status codes and JSON error responses to indicate success or failure. Refer to HubSpot's API documentation for detailed error codes and their meanings.


##  Rate Limits

Be aware of HubSpot's API rate limits to avoid throttling.


This documentation provides a comprehensive overview. Refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications. Remember to replace placeholder values like `{companyId}` and IDs with actual values.
