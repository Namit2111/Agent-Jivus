# HubSpot CRM API: Contacts

This document details the HubSpot CRM API endpoints for managing contacts.  Contacts store information about individuals interacting with your business.  These endpoints allow for creating, managing, and syncing contact data.

## Understanding the CRM (Prerequisites)

Before using the API, familiarize yourself with HubSpot's [CRM object model](link_to_hubspot_crm_object_guide),  [properties](link_to_hubspot_properties_guide), and [associations](link_to_hubspot_associations_guide).  Understanding these concepts is crucial for effective API usage.


## API Endpoints

All endpoints are under the `/crm/v3/objects/contacts` base path unless otherwise specified.

### 1. Create Contacts

**Endpoint:** `POST /crm/v3/objects/contacts`

**Request:**  Requires a JSON body with at least one of the following properties: `email`, `firstname`, or `lastname`.  `email` is strongly recommended as the primary unique identifier.

**Request Body (Example):**

```json
{
  "properties": {
    "email": "example@hubspot.com",
    "firstname": "Jane",
    "lastname": "Doe",
    "phone": "(555) 555-5555",
    "company": "HubSpot",
    "website": "hubspot.com",
    "lifecyclestage": "marketingqualifiedlead"  // Use internal name, not label
  },
  "associations": [
    {
      "to": { "id": 123456 }, // ID of associated company
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 279 }] // Association type ID. See default types or Associations API.
    },
    {
      "to": { "id": 556677 }, // ID of associated activity (e.g. email)
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 197 }]
    }
  ]
}
```

**Response:** A JSON object representing the newly created contact, including its ID.


**Note on `lifecyclestage`:** Use the *internal name* of the lifecycle stage (e.g., `"marketingqualifiedlead"`, `"subscriber"`).  Custom stages use numeric IDs.


### 2. Retrieve Contacts

**Individual Contact:**

* **Endpoint:** `GET /crm/v3/objects/contacts/{contactId}` (by ID) or `GET /crm/v3/objects/contacts/{email}?idProperty=email` (by email)

* **Query Parameters:**
    * `properties`: Comma-separated list of properties to return.
    * `propertiesWithHistory`: Comma-separated list of properties to return, including history.
    * `associations`: Comma-separated list of associated objects to retrieve.

**Batch Contact Retrieval:**

* **Endpoint:** `POST /crm/v3/objects/contacts/batch/read`

* **Request Body (Example - by ID):**

```json
{
  "properties": ["email", "lifecyclestage", "jobtitle"],
  "inputs": [
    { "id": "1234567" },
    { "id": "987456" }
  ]
}
```

* **Request Body (Example - by email):**

```json
{
  "properties": ["email", "lifecyclestage", "jobtitle"],
  "idProperty": "email",
  "inputs": [
    { "id": "lgilmore@thedragonfly.com" },
    { "id": "sstjames@thedragonfly.com" }
  ]
}
```

* **Response:** A JSON array of contact objects.  Associations are not retrievable through batch read.


### 3. Update Contacts

**Individual Contact:**

* **Endpoint:** `PATCH /crm/v3/objects/contacts/{contactId}` (by ID) or `PATCH /crm/v3/objects/contacts/{email}?idProperty=email` (by email)

* **Request Body (Example):**

```json
{
  "properties": {
    "favorite_food": "burger",
    "jobtitle": "Manager",
    "lifecyclestage": "Customer"
  }
}
```

**Batch Contact Update:**

* **Endpoint:** `POST /crm/v3/objects/contacts/batch/update`

* **Request Body (Example):**

```json
{
  "inputs": [
    {
      "id": "123456789",
      "properties": { "favorite_food": "burger" }
    },
    {
      "id": "56789123",
      "properties": { "favorite_food": "Donut" }
    }
  ]
}
```

**Note on `lifecyclestage` update:**  Only forward movement in the lifecycle stage is allowed. To move backward, clear the existing value first.


### 4. Upsert Contacts

* **Endpoint:** `POST /crm/v3/objects/contacts/batch/upsert`

* **Request Body (Example - using email):**

```json
{
  "inputs": [
    {
      "properties": { "phone": "5555555555" },
      "id": "test@test.com",
      "idProperty": "email"
    },
    {
      "properties": { "phone": "7777777777" },
      "id": "example@hubspot.com",
      "idProperty": "email"
    }
  ]
}
```

This endpoint allows creating or updating contacts in a batch.


### 5. Associate Contacts

* **Endpoint:** `PUT /crm/v3/objects/contacts/{contactId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

* Requires specifying the `toObjectType` (e.g., `companies`), `toObjectId`, and `associationTypeId`.


### 6. Remove Association

* **Endpoint:** `DELETE /crm/v3/objects/contacts/{contactID}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


### 7. Pin an Activity

* **Endpoint:** `PATCH /crm/v3/objects/contacts/{contactId}`

* **Request Body (Example):**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```

This can also be done during contact creation.


### 8. Delete Contacts

* **Endpoint:** `DELETE /crm/v3/objects/contacts/{contactId}`

Deletes a contact (moves it to the recycle bin).


### 9. Secondary Emails

Use the `hs_additional_emails` property to manage secondary email addresses.


### 10. Limits

Batch operations are limited to 100 records per request.  See HubSpot's documentation for overall contact and form submission limits.



This markdown provides a comprehensive overview.  Always refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications. Remember to replace placeholder values (IDs, emails, etc.) with your actual data.  You will need appropriate HubSpot API keys and authentication for making requests.
