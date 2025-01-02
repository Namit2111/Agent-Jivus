# HubSpot CRM API: Contacts

This document details the HubSpot CRM API endpoints for managing contacts.  Contacts store information about individuals interacting with your business.  These endpoints allow creation, management, and synchronization of contact data with other systems.

## Understanding HubSpot Objects, Records, Properties, and Associations

Before proceeding, familiarize yourself with HubSpot's concepts of [Objects](link_to_hubspot_objects_doc), [Records](link_to_hubspot_records_doc), [Properties](link_to_hubspot_properties_doc), and [Associations](link_to_hubspot_associations_doc)  within the CRM.


## Endpoints

### 1. Create Contacts

**Endpoint:** `/crm/v3/objects/contacts`

**Method:** `POST`

**Request Body:** JSON

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
  },
  "associations": [
    {
      "to": {
        "id": 123456  // Existing Company ID
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 279 // Association Type ID (e.g., company-contact)
        }
      ]
    },
    {
      "to": {
        "id": 556677 // Existing Email ID
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 197 // Association Type ID (e.g., email-contact)

        }
      ]
    }
  ]
}
```

**Properties:** Contact details are stored in properties.  Use at least one of `email`, `firstname`, or `lastname`. `email` is the recommended primary unique identifier.  Retrieve available properties with a `GET` request to `/crm/v3/properties/contacts`.

**Associations:**  Associate the new contact with existing records (companies, deals) or activities (meetings, notes) using the `associations` object.  `associationTypeId` values can be found in the [default association types list](link_to_default_association_types) or retrieved via the Associations API.

**Response:** JSON containing the created contact's information, including its ID.

### 2. Retrieve Contacts

**Endpoint:**

* Individual contact by ID: `/crm/v3/objects/contacts/{contactId}`
* Individual contact by email: `/crm/v3/objects/contacts/{email}?idProperty=email`
* All contacts: `/crm/v3/objects/contacts`
* Batch read: `/crm/v3/objects/contacts/batch/read` (POST request)

**Method:** `GET` (for individual and all contacts), `POST` (for batch read)

**Query Parameters (for individual and all contacts):**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of current and historical properties.
* `associations`: Comma-separated list of associated objects to retrieve.

**Request Body (for batch read):** JSON

**Example Batch Read Request (by ID):**

```json
{
  "properties": ["email", "lifecyclestage", "jobtitle"],
  "inputs": [
    {"id": "1234567"},
    {"id": "987456"}
  ]
}
```

**Example Batch Read Request (by email):**

```json
{
  "properties": ["email", "lifecyclestage", "jobtitle"],
  "idProperty": "email",
  "inputs": [
    {"id": "lgilmore@thedragonfly.com"},
    {"id": "sstjames@thedragonfly.com"}
  ]
}
```

**Response:** JSON containing the requested contact(s) information.


### 3. Update Contacts

**Endpoint:**

* Individual contact by ID: `PATCH /crm/v3/objects/contacts/{contactId}`
* Individual contact by email: `PATCH /crm/v3/objects/contacts/{email}?idProperty=email`
* Batch update: `POST /crm/v3/objects/contacts/batch/update`

**Method:** `PATCH` (individual), `POST` (batch)

**Request Body:** JSON

**Example Individual Update (by ID):**

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
    {
      "id": "123456789",
      "properties": {"favorite_food": "burger"}
    },
    {
      "id": "56789123",
      "properties": {"favorite_food": "Donut"}
    }
  ]
}
```

**Response:** JSON confirming the update.  Note that `lifecyclestage` updates can only move forward in the stage order.


### 4. Upsert Contacts

**Endpoint:** `/crm/v3/objects/contacts/batch/upsert`

**Method:** `POST`

**Request Body:** JSON

**Example Request (using email):**

```json
{
  "inputs": [
    {
      "properties": {"phone": "5555555555"},
      "id": "test@test.com",
      "idProperty": "email"
    },
    {
      "properties": {"phone": "7777777777"},
      "id": "example@hubspot.com",
      "idProperty": "email"
    }
  ]
}
```

**Response:** JSON confirming the upsert operation.


### 5. Associate/Disassociate Contacts

**Endpoint:**

* Associate: `PUT /crm/v3/objects/contacts/{contactId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`
* Disassociate: `DELETE /crm/v3/objects/contacts/{contactID}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `PUT` (associate), `DELETE` (disassociate)

**Response:**  JSON confirming the association or disassociation.


### 6. Pin an Activity

**Endpoint:** `/crm/v3/objects/contacts/{contactId}`

**Method:** `PATCH`

**Request Body:** JSON (includes `hs_pinned_engagement_id` property)

**Example:**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```

**Response:** JSON confirming the pinned activity.


### 7. Delete Contacts

**Endpoint:** `/crm/v3/objects/contacts/{contactId}`

**Method:** `DELETE`

**Response:** JSON confirming the deletion (moves to recycling bin).


### 8. Secondary Emails

* To view: Include `email` and `hs_additional_emails` in the `properties` parameter when retrieving contacts.
* To add: Include emails in the `hs_additional_emails` field (semicolon-separated) when creating or updating contacts.


## Limits

Batch operations are limited to 100 records per request.  Refer to HubSpot's documentation for overall contact and form submission limits.


This documentation provides a comprehensive overview of the HubSpot CRM Contacts API.  Always refer to the official HubSpot API documentation for the most up-to-date information and details. Remember to replace placeholders like `{contactId}`, `{email}`, `{toObjectId}`, and `{associationTypeId}` with actual values.
