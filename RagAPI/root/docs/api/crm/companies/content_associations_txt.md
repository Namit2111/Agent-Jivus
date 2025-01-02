# HubSpot CRM API: Companies

This document details the HubSpot CRM API endpoints for managing companies.  Companies in HubSpot store information about organizations interacting with your business.  This API allows creation, management, and synchronization of company data between HubSpot and external systems.


## Understanding the CRM

For a comprehensive understanding of HubSpot's object, record, property, and association APIs, refer to the [Understanding the CRM](link_to_understanding_crm_guide) guide.  For general CRM database management, see [Managing your CRM database](link_to_crm_management_guide).


## API Endpoints

All endpoints are under the `/crm/v3/objects/companies` base path unless otherwise specified.


### 1. Create Companies

**Endpoint:** `/crm/v3/objects/companies`

**Method:** `POST`

**Request Body:** JSON

This endpoint creates new company records.  The request body must include a `properties` object containing company details.  An optional `associations` object can be included to associate the new company with existing records (contacts, deals) or activities (meetings, notes).

**Required Properties:** At least one of `name` or `domain` is required.  `domain` is strongly recommended as the primary unique identifier to prevent duplicates. Multiple domains can be added using the `hs_additional_domains` property (e.g., `"hs_additional_domains": "domain.com;domain2.com"`).

**Example Request Body (with associations):**

```json
{
  "properties": {
    "name": "HubSpot",
    "domain": "hubspot.com",
    "city": "Cambridge",
    "industry": "Technology",
    "phone": "555-555-555",
    "state": "Massachusetts",
    "lifecyclestage": "51439524"
  },
  "associations": [
    {
      "to": {
        "id": 101
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 280
        }
      ]
    },
    {
      "to": {
        "id": 556677
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 185
        }
      ]
    }
  ]
}
```

**Response:**  A JSON object containing the newly created company's details, including its ID.


### 2. Retrieve Companies

**Individual Company:**

**Endpoint:** `/crm/v3/objects/companies/{companyId}`

**Method:** `GET`

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `associations`: Comma-separated list of associated objects to retrieve IDs for.


**Batch Companies:**

**Endpoint:** `/crm/v3/objects/companies/batch/read`

**Method:** `POST`

**Request Body:** JSON

This endpoint allows retrieving multiple companies by record ID or a custom unique identifier property.  Associations cannot be retrieved using this endpoint.

**Request Body Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `inputs`: Array of objects, each with an `id` property representing the company ID or custom unique identifier.
* `idProperty`: (Optional) The name of the custom unique identifier property to use for lookup.  Defaults to `hs_object_id` (record ID).


**Example Request Body (Batch, with record IDs):**

```json
{
  "properties": ["name", "domain"],
  "inputs": [
    {"id": "56789"},
    {"id": "23456"}
  ]
}
```

**Example Request Body (Batch, with custom unique identifier):**

```json
{
  "properties": ["name", "domain"],
  "idProperty": "uniquepropertyexample",
  "inputs": [
    {"id": "abc"},
    {"id": "def"}
  ]
}
```

**Response:**  A JSON object containing an array of company details.


### 3. Update Companies

**Endpoint:** `/crm/v3/objects/companies/{companyId}`

**Method:** `PATCH`

**Request Body:** JSON

Updates an existing company. Include only the properties you wish to modify.  Note the restrictions on updating `lifecyclestage`.


**Example Request Body:**

```json
{
  "properties": {
    "name": "Updated Company Name",
    "city": "New City"
  }
}
```

**Response:** A JSON object containing the updated company's details.


### 4. Associate Existing Companies

**Endpoint:** `/crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `PUT`

Associates an existing company with other CRM records or activities.  `associationTypeId` can be found in the [list of default values](link_to_association_type_ids) or retrieved via the associations API.


### 5. Remove Association

**Endpoint:** `/crm/v3/objects/companies/{companyId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `DELETE`

Removes an association between a company and another record or activity.


### 6. Pin an Activity

**Endpoint:** `/crm/v3/objects/companies/{companyId}`

**Method:** `PATCH`

Pins an activity to a company record using the `hs_pinned_engagement_id` property.  The activity ID must be obtained via the engagements APIs and must already be associated with the company.


**Example Request Body:**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```


### 7. Delete Companies

**Endpoint:** `/crm/v3/objects/companies/{companyId}`

**Method:** `DELETE`

Deletes a company (moves it to the recycling bin).  See reference documentation for batch deletion.


## Properties API

Retrieve a list of available company properties using a `GET` request to `/crm/v3/properties/companies`.  See the [properties API documentation](link_to_properties_api) for more details.


## Associations API

For more information on associations, refer to the [associations API documentation](link_to_associations_api).


##  Error Handling

The API responses will include standard HTTP status codes and JSON error messages indicating success or failure.  Refer to the HubSpot API documentation for detailed error codes and handling.


**Note:** Replace placeholders like `{companyId}`, `{toObjectType}`, `{toObjectId}`, and `{associationTypeId}` with actual values.  Remember to include your HubSpot API key in the request headers.  Links to referenced guides and API documentation need to be replaced with the actual URLs.
