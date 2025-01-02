# HubSpot CRM API: Contacts

This document details the HubSpot CRM API endpoints for managing contacts.  Contacts store information about individuals interacting with your business.  These endpoints allow creation, management, and synchronization of contact data.

## Understanding the CRM (Prerequisites)

Before using these APIs, familiarize yourself with HubSpot's CRM concepts:

* **Objects:**  Represent data categories (e.g., Contacts, Companies, Deals).
* **Records:** Individual entries within an object (e.g., a specific contact).
* **Properties:** Data fields within an object (e.g., email, firstname, lastname).
* **Associations:** Links between records of different objects (e.g., associating a contact with a company).

See the [Understanding the CRM guide](link_to_guide_here) and [managing your CRM database](link_to_guide_here) for more details.


## API Endpoints

All endpoints use `/crm/v3/objects/contacts` as a base.  Replace `{contactId}` with the contact's ID and `{email}` with the contact's email address.


### 1. Create Contacts

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/contacts`

**Request Body:** JSON

Requires at least one of `email`, `firstname`, or `lastname`.  `email` is strongly recommended as the primary unique identifier.  `lifecyclestage` values must use internal names (e.g., "subscriber", "marketingqualifiedlead" for default stages, numeric IDs for custom stages).

**Example Request:**

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
  }
}
```

**Example Request with Associations:**

```json
{
  "properties": {
    "email": "example@hubspot.com",
    "firstname": "Jane",
    "lastname": "Doe"
  },
  "associations": [
    {
      "to": { "id": 123456 }, // Company ID
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 279 }] // Association Type ID
    },
    {
      "to": { "id": 556677 }, // Deal ID
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 197 }] // Association Type ID
    }
  ]
}
```

**Response:** JSON (Contact record details including ID)


### 2. Retrieve Contacts

**Method:** `GET` (individual) / `GET` (all) / `POST` (batch)

**Endpoint:**

* Individual: `/crm/v3/objects/contacts/{contactId}` or `/crm/v3/objects/contacts/{email}?idProperty=email`
* All: `/crm/v3/objects/contacts`
* Batch: `/crm/v3/objects/contacts/batch/read`

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`:  Comma-separated list of current and historical properties.
* `associations`: Comma-separated list of associated objects to retrieve.

**Batch Read Request (Record IDs):**

```json
{
  "properties": ["email", "lifecyclestage", "jobtitle"],
  "inputs": [
    { "id": "1234567" },
    { "id": "987456" }
  ]
}
```

**Batch Read Request (Email or Custom Property):**

```json
{
  "properties": ["email", "lifecyclestage", "jobtitle"],
  "idProperty": "email", // or custom property name
  "inputs": [
    { "id": "lgilmore@thedragonfly.com" },
    { "id": "sstjames@thedragonfly.com" }
  ]
}
```

**Response:** JSON (Contact record details or array of contact records)


### 3. Update Contacts

**Method:** `PATCH` (individual) / `POST` (batch)

**Endpoint:**

* Individual: `/crm/v3/objects/contacts/{contactId}` or `/crm/v3/objects/contacts/{email}?idProperty=email`
* Batch: `/crm/v3/objects/contacts/batch/update`

**Request Body:** JSON (properties to update)

**Example Individual Update (Record ID):**

```json
{
  "properties": {
    "favorite_food": "burger",
    "jobtitle": "Manager",
    "lifecyclestage": "Customer"
  }
}
```

**Example Batch Update:**

```json
{
  "inputs": [
    { "id": "123456789", "properties": { "favorite_food": "burger" } },
    { "id": "56789123", "properties": { "favorite_food": "Donut" } }
  ]
}
```

**Response:** JSON (Success/failure indicators)


### 4. Upsert Contacts

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/contacts/batch/upsert`

**Request Body:** JSON (Uses `idProperty` (email or custom property) and `id` for identification, and `properties` for data)

**Example:**

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

**Response:** JSON (Success/failure indicators)


### 5. Associate/Disassociate Contacts

**Method:** `PUT` (associate) / `DELETE` (disassociate)

**Endpoint:** `/crm/v3/objects/contacts/{contactId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


### 6. Pin an Activity

**Method:** `PATCH` (update existing contact) / `POST` (create new contact and associate/pin)

**Endpoint:** `/crm/v3/objects/contacts/{contactId}` (PATCH) or `/crm/v3/objects/contacts` (POST)

Use the `hs_pinned_engagement_id` property to specify the activity ID.


### 7. Delete Contacts

**Method:** `DELETE` (individual) /  (Batch - see reference documentation)

**Endpoint:** `/crm/v3/objects/contacts/{contactId}`


### 8. Secondary Emails

Use the `hs_additional_emails` property to manage secondary emails.  Separate multiple emails with semicolons.


### Limits

Batch operations are limited to 100 records per request.  Check the [HubSpot API documentation](link_to_hubspot_api_docs) for updated limits on contacts and form submissions.


This documentation provides a concise overview.  Refer to the official HubSpot API documentation for the most up-to-date information, error codes, and detailed specifications. Remember to replace placeholder values like IDs and association type IDs with your actual data.
