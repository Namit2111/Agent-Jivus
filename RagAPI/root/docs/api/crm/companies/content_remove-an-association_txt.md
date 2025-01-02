# HubSpot CRM API: Companies

This document details the HubSpot CRM API endpoints for managing companies.  Companies in HubSpot store information about organizations interacting with your business.  These endpoints allow creation, management, and synchronization of company data between HubSpot and external systems.


## Understanding the CRM (Prerequisite)

Before using these APIs, familiarize yourself with HubSpot's CRM concepts:

* **Objects:** Represent data types (e.g., companies, contacts).
* **Records:** Individual instances of an object (e.g., a specific company).
* **Properties:** Attributes of an object (e.g., company name, domain).
* **Associations:** Connections between records of different objects.

For more details, refer to the [Understanding the CRM guide](link_to_guide_here) and [managing your CRM database](link_to_guide_here).


## API Endpoints

All endpoints are under the `/crm/v3/objects/companies` base URL unless otherwise specified.  Remember to replace placeholders like `{companyId}` with actual values.

### 1. Create Companies

**Endpoint:** `POST /crm/v3/objects/companies`

**Method:** `POST`

**Request Body (JSON):**

```json
{
  "properties": {
    "name": "HubSpot",
    "domain": "hubspot.com",
    "city": "Cambridge",
    "industry": "Technology",
    "phone": "555-555-555",
    "state": "Massachusetts",
    "lifecyclestage": "51439524" // Use internal ID for lifecycle stage
  },
  "associations": [ // Optional: Associate with existing records/activities
    {
      "to": { "id": 101 }, // ID of existing record
      "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 280 } ] // Association type
    },
    {
      "to": { "id": 556677 },
      "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 185 } ]
    }
  ]
}
```

**Response:**  A JSON object representing the newly created company, including its ID.

**Notes:**

* At least `name` or `domain` is required in the `properties` object.  `domain` is recommended as the primary unique identifier.
* Use semicolons to separate multiple domains in the `hs_additional_domains` property (e.g., `"hs_additional_domains": "domain.com;domain2.com"`).
* `lifecyclestage` values must use the internal name (for default stages) or numeric ID (for custom stages).


### 2. Retrieve Companies

**a) Individual Company:**

**Endpoint:** `GET /crm/v3/objects/companies/{companyId}`

**Method:** `GET`

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return with history.
* `associations`: Comma-separated list of associated objects to retrieve.

**Response:** A JSON object representing the company.

**b) List of Companies:**

**Endpoint:** `GET /crm/v3/objects/companies`

**Method:** `GET`

**Query Parameters:** Same as above.

**Response:** A JSON object containing a list of companies.


**c) Batch Read:**

**Endpoint:** `POST /crm/v3/objects/companies/batch/read`

**Method:** `POST`

**Request Body (JSON):**

```json
{
  "properties": ["name", "domain"],
  "inputs": [ { "id": "56789" }, { "id": "23456" } ] // IDs can be record IDs or custom unique identifiers
  "idProperty": "uniquepropertyexample" // Optional: Use a custom unique identifier property
}
```

**Response:** A JSON object containing a list of companies.  Associations are not retrieved using this endpoint.


### 3. Update Companies

**Endpoint:** `PATCH /crm/v3/objects/companies/{companyId}`

**Method:** `PATCH`

**Request Body (JSON):**

```json
{
  "properties": {
    "name": "Updated Name",
    "city": "New City"
  }
}
```

**Response:** A JSON object representing the updated company.

**Notes:**  `lifecyclestage` updates can only move forward in the stage order. To move backward, clear the existing value first.


### 4. Associate Existing Companies

**Endpoint:** `PUT /crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `PUT`

**Parameters:**

* `{toObjectType}`: Type of object to associate (e.g., `contacts`).
* `{toObjectId}`: ID of the object to associate.
* `{associationTypeId}`: ID of the association type.  Obtain from the default list or the associations API (`GET /crm/v4/associations/{fromObjectType}/{toObjectType}/labels`).

**Response:** Success/failure indication.


### 5. Remove Association

**Endpoint:** `DELETE /crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `DELETE`

**Parameters:** Same as above.

**Response:** Success/failure indication.


### 6. Pin an Activity

**a) Update Existing Company:**

**Endpoint:** `PATCH /crm/v3/objects/companies/{companyId}`

**Method:** `PATCH`

**Request Body (JSON):**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789 // ID of the activity to pin
  }
}
```

**b) Create Company and Pin Activity Simultaneously:**

**Endpoint:** `POST /crm/v3/objects/companies`

**Method:** `POST`

**Request Body (JSON):** (See example in the original text).  Includes both `properties` (with `hs_pinned_engagement_id`) and `associations` to link the activity.


### 7. Delete Companies

**Endpoint:** `DELETE /crm/v3/objects/companies/{companyId}`

**Method:** `DELETE`

**Response:** Success/failure indication.  The company is moved to the recycling bin.


## Error Handling

The API will return appropriate HTTP status codes (e.g., 400 Bad Request, 404 Not Found) and JSON error responses to indicate problems.


##  Rate Limits

Be aware of HubSpot's API rate limits to avoid throttling.


This documentation provides a comprehensive overview of the HubSpot CRM API for companies.  Always refer to the official HubSpot API documentation for the most up-to-date information and details.
