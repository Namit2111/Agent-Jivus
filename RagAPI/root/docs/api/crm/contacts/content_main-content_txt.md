# HubSpot CRM API: Contacts

This document details the HubSpot CRM API endpoints for managing contacts.  Contacts store information about individuals interacting with your business.  These endpoints allow for creating, managing, and syncing contact data between HubSpot and other systems.

## Understanding HubSpot CRM Objects, Records, Properties, and Associations

Before proceeding, familiarize yourself with the concepts of [HubSpot Objects](link_to_hubspot_objects_documentation), [Records](link_to_hubspot_records_documentation), [Properties](link_to_hubspot_properties_documentation), and [Associations](link_to_hubspot_associations_documentation) as described in the HubSpot documentation.

## API Endpoints

All endpoints use `/crm/v3/objects/contacts` as a base unless otherwise specified.  Remember to include your HubSpot API key in the request headers.

### 1. Create Contacts

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/contacts`

**Request Body:**

JSON payload containing a `properties` object with contact details.  At least one of `email`, `firstname`, or `lastname` is required.  `email` is strongly recommended as it's the primary unique identifier.  You can also include an `associations` object to link the new contact to existing records or activities.

**Example Request Body (with Associations):**

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
        "id": 123456
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 279
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
          "associationTypeId": 197
        }
      ]
    }
  ]
}
```

**Response:**  A JSON object representing the newly created contact, including its `id`.

**Note:**  `lifecyclestage` values must use the internal name (not the label).  Internal names for custom stages are numeric.


### 2. Retrieve Contacts

**Method:** `GET` (individual) or `POST` (batch)

**Endpoints:**

* **Individual:** `/crm/v3/objects/contacts/{contactId}` or `/crm/v3/objects/contacts/{email}?idProperty=email`
* **Batch:** `/crm/v3/objects/contacts/batch/read`

**Query Parameters (for individual retrieval):**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of current and historical properties.
* `associations`: Comma-separated list of associated objects to retrieve.

**Request Body (for batch retrieval):**

```json
{
  "properties": ["email", "lifecyclestage", "jobtitle"],
  "inputs": [
    { "id": "1234567" },
    { "id": "987456" }
  ]
}
```

or using email:

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

**Response:** JSON object (individual) or array (batch) of contact data.


### 3. Update Contacts

**Method:** `PATCH` (individual) or `POST` (batch)

**Endpoints:**

* **Individual:** `/crm/v3/objects/contacts/{contactId}` or `/crm/v3/objects/contacts/{email}?idProperty=email`
* **Batch:** `/crm/v3/objects/contacts/batch/update`


**Request Body (individual):**

```json
{
  "properties": {
    "favorite_food": "burger",
    "jobtitle": "Manager",
    "lifecyclestage": "Customer"
  }
}
```

**Request Body (batch):**

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

**Response:** JSON object representing the updated contact (individual) or an array of updated contacts (batch).

**Note:** Updating `lifecyclestage` only allows moving forward in the stage order.


### 4. Upsert Contacts

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/contacts/batch/upsert`

**Request Body:**  Similar to batch update, but uses `idProperty` (e.g., "email") to identify whether `id` is an email or custom unique identifier.  Creates new contacts if they don't exist, updates if they do.

**Example Request Body:**

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

**Response:**  JSON array of upserted contact data.


### 5. Associate/Dissociate Contacts

**Method:** `PUT` (associate) or `DELETE` (dissociate)

**Endpoint (both):** `/crm/v3/objects/contacts/{contactId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Request Body (PUT):** None


**Response:** JSON object confirming the association/dissociation.


### 6. Pin an Activity

**Method:** `PATCH` (update existing contact) or `POST` (create new contact)

**Endpoint (PATCH):** `/crm/v3/objects/contacts/{contactId}`

**Endpoint (POST):** `/crm/v3/objects/contacts`

**Request Body (both):** Include `hs_pinned_engagement_id` property with activity ID. For the `POST` request, association to the activity must also be included.


### 7. Delete Contacts

**Method:** `DELETE` (individual) or refer to documentation for batch deletion.

**Endpoint (individual):** `/crm/v3/objects/contacts/{contactId}`

**Response:**  JSON object confirming the deletion.


### 8. Secondary Emails

Retrieve secondary emails using the `hs_additional_emails` property when retrieving contacts. Add or update secondary emails by including them in the `hs_additional_emails` field, separated by semicolons.


### 9. Limits

Batch operations are limited to 100 records at a time.  See HubSpot documentation for other limits.


This documentation provides a comprehensive overview.  Refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications.  Remember to replace placeholder values like `{contactId}`, `{email}`, and IDs with actual values.
