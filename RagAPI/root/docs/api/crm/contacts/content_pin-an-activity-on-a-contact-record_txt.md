# HubSpot CRM API: Contacts

This document details the HubSpot CRM API endpoints for managing contacts.  Contacts in HubSpot store information about individuals interacting with your business. These endpoints allow for creation, management, and synchronization of contact data between HubSpot and external systems.

## Understanding the Basics

Before using the API, familiarize yourself with:

* **Objects, Records, Properties, and Associations APIs:** [Understanding the CRM guide](link-to-guide-needed)
* **Managing your CRM database:** (link-to-guide-needed)


## Endpoints

### 1. Create Contacts

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/contacts`

**Request Body:**  Includes a `properties` object containing contact data.  An optional `associations` object can associate the new contact with existing records (companies, deals) or activities (meetings, notes).

**Required Properties:** At least one of `email`, `firstname`, or `lastname`.  `email` is strongly recommended as the primary unique identifier to prevent duplicates.

**Example Request Body:**

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

**Note on `lifecyclestage`:**  Values must use the internal name (text for default stages, numeric for custom stages).  Find the internal ID in your lifecycle stage settings or via the API.


### 2. Retrieve Contacts

**Individual Contact:**

* **Method:** `GET`
* **Endpoint:** `/crm/v3/objects/contacts/{contactId}` or `/crm/v3/objects/contacts/{email}?idProperty=email`

**All Contacts:**

* **Method:** `GET`
* **Endpoint:** `/crm/v3/objects/contacts`

**Batch Retrieval:**

* **Method:** `POST`
* **Endpoint:** `/crm/v3/objects/contacts/batch/read`
* **Cannot retrieve associations.** Use the Associations API for batch association reads.

**Query Parameters (for individual and all contacts):**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of current and historical properties to return.
* `associations`: Comma-separated list of objects to retrieve associated IDs for.

**Batch Read Request Body (example with record ID):**

```json
{
  "properties": ["email", "lifecyclestage", "jobtitle"],
  "inputs": [
    { "id": "1234567" },
    { "id": "987456" }
  ]
}
```

**Batch Read Request Body (example with email or custom unique identifier):**

```json
{
  "properties": ["email", "lifecyclestage", "jobtitle"],
  "idProperty": "email",  // or "internalcustomerid"
  "inputs": [
    { "id": "lgilmore@thedragonfly.com" },
    { "id": "sstjames@thedragonfly.com" }
  ]
}
```

### 3. Update Contacts

**Individual Contact:**

* **Method:** `PATCH`
* **Endpoint:** `/crm/v3/objects/contacts/{contactId}` (by ID) or `/crm/v3/objects/contacts/{email}?idProperty=email` (by email)

**Batch Update:**

* **Method:** `POST`
* **Endpoint:** `/crm/v3/objects/contacts/batch/update`

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
    { "id": "123456789", "properties": { "favorite_food": "burger" } },
    { "id": "56789123", "properties": { "favorite_food": "Donut" } }
  ]
}
```

**Note on `lifecyclestage` updates:**  Can only be set *forward* in the stage order.  To move backward, clear the existing value manually or via workflow/integration.


### 4. Upsert Contacts

* **Method:** `POST`
* **Endpoint:** `/crm/v3/objects/contacts/batch/upsert`
* Uses `email` or a custom unique identifier property (`idProperty`). Existing contacts are updated; new ones are created.

**Example Request Body (using email):**

```json
{
  "inputs": [
    { "properties": { "phone": "5555555555" }, "id": "test@test.com", "idProperty": "email" },
    { "properties": { "phone": "7777777777" }, "id": "example@hubspot.com", "idProperty": "email" }
  ]
}
```

### 5. Associate Contacts

* **Method:** `PUT`
* **Endpoint:** `/crm/v3/objects/contacts/{contactId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

### 6. Remove Association

* **Method:** `DELETE`
* **Endpoint:** `/crm/v3/objects/contacts/{contactID}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


### 7. Pin an Activity

* Uses the `hs_pinned_engagement_id` property (requires the activity ID from the Engagements APIs).  Can be done during contact creation or update.


### 8. Delete Contacts

* **Individual:** `DELETE` `/crm/v3/objects/contacts/{contactId}` (moves to recycling bin)
* **Batch:** (See reference documentation for batch delete)


### 9. Secondary Emails

* Use `hs_additional_emails` property for managing secondary emails.  Multiple emails are separated by semicolons.


### 10. Limits

Batch operations are limited to 100 records per request.  Refer to documentation for limits on contacts and form submissions.


This markdown provides a structured overview.  Always refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications.  Remember to replace placeholders like `{contactId}`, `{email}`, etc., with actual values.
