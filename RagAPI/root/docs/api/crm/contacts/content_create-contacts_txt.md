# HubSpot CRM API: Contacts

This document details the HubSpot CRM API endpoints for managing contacts.  Contacts store information about individuals interacting with your business.  These endpoints allow creation, management, and synchronization of contact data.

## Understanding the CRM (Overview)

Before using the API, familiarize yourself with HubSpot's [CRM object model](LINK_TO_HUBSPOT_DOC_ON_CRM_OBJECT_MODEL). This includes understanding objects, records, properties, and associations.

## API Endpoints

All endpoints are under the `/crm/v3/objects/contacts` base path unless otherwise specified.  Requests require proper authentication (API key).  Responses are typically in JSON format.

### 1. Create Contacts

**Endpoint:** `POST /crm/v3/objects/contacts`

**Request Body:** JSON payload with `properties` object (at least one of `email`, `firstname`, or `lastname` required; `email` highly recommended).  Optionally includes `associations` object.

**Properties:**  Contact details.  Use [default HubSpot properties](LINK_TO_HUBSPOT_DOC_ON_DEFAULT_CONTACT_PROPERTIES) or create [custom properties](LINK_TO_HUBSPOT_DOC_ON_CUSTOM_CONTACT_PROPERTIES).  `lifecyclestage` values must be internal names (e.g., `"marketingqualifiedlead"`).

**Associations:**  Associate with existing records (companies, deals) or activities (meetings, notes).  Requires `to` (ID of the record/activity) and `types` (includes `associationCategory` and `associationTypeId`).  See [associations API documentation](LINK_TO_HUBSPOT_DOC_ON_ASSOCIATIONS_API) for details.

**Example Request (Create Contact with Associations):**

```json
{
  "properties": {
    "email": "example@hubspot.com",
    "firstname": "Jane",
    "lastname": "Doe",
    "phone": "(555) 555-5555",
    "company": "HubSpot",
    "website": "hubspot.com",
    "lifecyclestage": "marketingqualifiedlead"
  },
  "associations": [
    {
      "to": {"id": 123456},
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 279}]
    },
    {
      "to": {"id": 556677},
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 197}]
    }
  ]
}
```

**Example Response (Success):**  JSON object representing the created contact, including its ID.


### 2. Retrieve Contacts

**Individual Contact:**

* **Endpoint (by ID):** `GET /crm/v3/objects/contacts/{contactId}`
* **Endpoint (by email):** `GET /crm/v3/objects/contacts/{email}?idProperty=email`

**Batch Contact (by ID, email, or custom unique property):**

* **Endpoint:** `POST /crm/v3/objects/contacts/batch/read`
* Requires `inputs` array (each object with `id`).
* Use `idProperty` parameter for email or custom unique identifier.

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`:  For current and historical property values.
* `associations`: Comma-separated list of associated objects to retrieve.

**Example Request (Batch Read by ID):**

```json
{
  "properties": ["email", "lifecyclestage", "jobtitle"],
  "inputs": [{"id": "1234567"}, {"id": "987456"}]
}
```

**Example Response (Success):** JSON array of contact objects.


### 3. Update Contacts

**Individual Contact:**

* **Endpoint (by ID):** `PATCH /crm/v3/objects/contacts/{contactId}`
* **Endpoint (by email):** `PATCH /crm/v3/objects/contacts/{email}?idProperty=email`

**Batch Update:**

* **Endpoint:** `POST /crm/v3/objects/contacts/batch/update`
* Requires `inputs` array (each object with `id` and `properties`).

**Example Request (Individual Update by ID):**

```json
{
  "properties": {
    "favorite_food": "burger",
    "jobtitle": "Manager",
    "lifecyclestage": "Customer"
  }
}
```

**Example Response (Success):** JSON object representing updated contact.  Note that `lifecyclestage` can only be updated forward in the stage order.


### 4. Upsert Contacts

**Endpoint:** `POST /crm/v3/objects/contacts/batch/upsert`

Creates or updates contacts in batches using `email` or a custom unique identifier.

* Requires `inputs` array (each object with `id`, `idProperty`, and `properties`).

**Example Request (Upsert by email):**

```json
{
  "inputs": [
    {
      "properties": {"phone": "5555555555"},
      "id": "test@test.com",
      "idProperty": "email"
    }
  ]
}
```

**Example Response (Success):** JSON array with results for each input.


### 5. Associate/Dissociate Contacts

**Associate:**

* **Endpoint:** `PUT /crm/v3/objects/contacts/{contactId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Dissociate:**

* **Endpoint:** `DELETE /crm/v3/objects/contacts/{contactId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

Requires `associationTypeId` (from [default list](LINK_TO_DEFAULT_ASSOCIATION_TYPE_IDS) or [associations API](LINK_TO_HUBSPOT_DOC_ON_ASSOCIATIONS_API)).


### 6. Pin an Activity

Updates the `hs_pinned_engagement_id` property to pin an activity to a contact record.  Requires the activity ID.


### 7. Delete Contacts

**Individual Contact:**

* **Endpoint:** `DELETE /crm/v3/objects/contacts/{contactId}`

Batch deletion is also available (see [reference documentation](LINK_TO_BATCH_DELETE_DOC)).


### 8. Secondary Emails

Manage secondary emails using the `hs_additional_emails` property (semicolon-separated for multiple).


### 9. Limits

Batch operations are limited to 100 records.  See [contacts and form submissions limits](LINK_TO_LIMITS_DOC).


**Note:** Replace placeholders like `{contactId}`, `{email}`, `{toObjectType}`, `{toObjectId}`, and `{associationTypeId}` with actual values.  All examples assume you have the necessary authentication and authorization. Remember to replace the placeholder links with actual links to the relevant HubSpot documentation.
