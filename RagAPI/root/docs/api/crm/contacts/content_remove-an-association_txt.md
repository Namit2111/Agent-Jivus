# HubSpot CRM API: Contacts

This document details the HubSpot CRM API endpoints for managing contacts.  Contacts store information about individuals interacting with your business.  These endpoints allow creating, managing, and syncing contact data between HubSpot and other systems.

## Understanding the CRM

Before using these APIs, familiarize yourself with HubSpot's [CRM object model](link_to_hubspot_crm_object_guide) and [managing your CRM database](link_to_hubspot_crm_management_guide).  This includes understanding objects, records, properties, and associations.

## API Endpoints

All endpoints are under the `/crm/v3/objects/contacts` base URL unless otherwise specified.  Authentication is required; refer to HubSpot's API documentation for details.


### 1. Create Contacts

**Method:** `POST /crm/v3/objects/contacts`

**Request Body:** JSON

```json
{
  "properties": {
    "email": "example@hubspot.com",
    "firstname": "Jane",
    "lastname": "Doe",
    "phone": "(555) 555-5555",
    "company": "HubSpot",
    "website": "hubspot.com",
    "lifecyclestage": "marketingqualifiedlead" // Use internal name, not label
  },
  "associations": [
    {
      "to": {
        "id": 123456 // Existing record ID
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 279 // Association type ID (see below)
        }
      ]
    }
  ]
}
```

**Properties:** Contact details are stored in properties.  At least one of `email`, `firstname`, or `lastname` is required.  `email` is recommended as the primary unique identifier.  Use `/crm/v3/properties/contacts` (GET request) to view available properties.  Lifecycle stage values (`lifecyclestage`) must use the internal name (e.g., "marketingqualifiedlead", not its displayed label).

**Associations:**  Optionally associate the new contact with existing records or activities using the `associations` object.  `to.id` specifies the associated record/activity ID. `types` defines the association type; use the [default association type IDs](link_to_association_type_ids) or retrieve custom types via the associations API.


### 2. Retrieve Contacts

**Individual Contact:**

**Method:** `GET /crm/v3/objects/contacts/{contactId}` or `GET /crm/v3/objects/contacts/{email}?idProperty=email`

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of current and historical properties.
* `associations`: Comma-separated list of associated objects to retrieve.


**Batch Contact Retrieval:**

**Method:** `POST /crm/v3/objects/contacts/batch/read`

**Request Body:** JSON

```json
{
  "properties": ["email", "lifecyclestage", "jobtitle"],  //or "propertiesWithHistory"
  "idProperty": "email", // Optional, use for email or custom unique identifier
  "inputs": [
    { "id": "1234567" }, // Record ID, email, or custom ID depending on idProperty
    { "id": "lgilmore@thedragonfly.com" } //Example Email
  ]
}
```

This endpoint does not retrieve associations.


### 3. Update Contacts

**Individual Contact:**

**Method:** `PATCH /crm/v3/objects/contacts/{contactId}` or `PATCH /crm/v3/objects/contacts/{email}?idProperty=email`

**Request Body:** JSON

```json
{
  "properties": {
    "favorite_food": "burger",
    "jobtitle": "Manager",
    "lifecyclestage": "Customer"
  }
}
```

Updating `lifecyclestage` only allows moving forward in the stage order.


**Batch Contact Update:**

**Method:** `POST /crm/v3/objects/contacts/batch/update`

**Request Body:** JSON

```json
{
  "inputs": [
    { "id": "123456789", "properties": { "favorite_food": "burger" } },
    { "id": "56789123", "properties": { "favorite_food": "Donut" } }
  ]
}
```


### 4. Upsert Contacts

**Method:** `POST /crm/v3/objects/contacts/batch/upsert`

**Request Body:** JSON

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

Uses `email` or a custom unique identifier property (`idProperty`) to determine whether to create or update.


### 5. Associate Contacts

**Method:** `PUT /crm/v3/objects/contacts/{contactId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

Associates a contact with other CRM records or activities.  Obtain `associationTypeId` from the [default list](link_to_association_type_ids) or via the associations API.


### 6. Remove Association

**Method:** `DELETE /crm/v3/objects/contacts/{contactID}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


### 7. Pin an Activity

**Method:** `PATCH /crm/v3/objects/contacts/{contactId}`

**Request Body:** JSON (Include `hs_pinned_engagement_id` with the activity ID)

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```

Can also be done during contact creation.


### 8. Delete Contacts

**Method:** `DELETE /crm/v3/objects/contacts/{contactId}`

Moves the contact to the recycling bin.  Refer to the [HubSpot documentation](link_to_hubspot_batch_delete_guide) for batch deletion.


### 9. Secondary Emails

Use the `hs_additional_emails` property to manage secondary emails.  Multiple emails are separated by semicolons.


### Limits

Batch operations are limited to 100 records per request.  Check HubSpot's documentation for overall contact and form submission limits.


**Note:**  Replace placeholder URLs (`link_to...`) with actual HubSpot documentation links.  Also, remember to handle error responses appropriately in your code.  Always consult the official HubSpot API documentation for the most up-to-date information.
