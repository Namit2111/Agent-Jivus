# HubSpot CRM API: Contacts

This document details the HubSpot CRM API endpoints for managing contacts.  Contacts in HubSpot store information about individuals interacting with your business.  These endpoints allow creation, management, and synchronization of contact data.

## Understanding the CRM (Prerequisites)

Before using these APIs, familiarize yourself with HubSpot's CRM concepts:

* **Objects:**  Represent data categories (e.g., Contacts, Companies, Deals).
* **Records:** Individual entries within an object (e.g., a specific contact).
* **Properties:**  Attributes of a record (e.g., email, firstname, lastname).  HubSpot provides default properties, but you can create custom ones.
* **Associations:**  Links between records of different objects (e.g., associating a contact with a company).

For more information, refer to the [Understanding the CRM guide](link_to_guide_here) and [managing your CRM database](link_to_database_management).

## API Endpoints

All endpoints are under the `/crm/v3/objects/contacts` base URL, unless otherwise specified.  Requests typically require authentication via an API key.


### 1. Create Contacts (POST `/crm/v3/objects/contacts`)

Creates a new contact. Requires at least one of `email`, `firstname`, or `lastname`.  `email` is strongly recommended as the primary unique identifier to prevent duplicates.

**Request Body (JSON):**

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
  "associations": [ // Optional: Associate with existing records/activities
    {
      "to": { "id": 123456 }, // ID of the associated record/activity
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 279 // Association type ID (see documentation for defaults)
        }
      ]
    }
  ]
}
```

**Response (JSON):**  A JSON object representing the newly created contact, including its ID.


### 2. Retrieve Contacts

**a) Individual Contact (GET `/crm/v3/objects/contacts/{contactId}` or `/crm/v3/objects/contacts/{email}?idProperty=email`)**

Retrieves a single contact by ID or email.

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`:  Comma-separated list of properties to return, including historical values.
* `associations`: Comma-separated list of associated objects to retrieve.

**b) All Contacts (GET `/crm/v3/objects/contacts`)**

Retrieves a list of all contacts.  Uses the same query parameters as above.

**c) Batch Read (POST `/crm/v3/objects/contacts/batch/read`)**

Retrieves a batch of contacts by ID, email, or custom unique property.  **Does not support associations.**

**Request Body (JSON):**

```json
{
  "properties": ["email", "lifecyclestage", "jobtitle"],
  "idProperty": "email", // Optional: Specify if using email or custom property as ID
  "inputs": [
    { "id": "lgilmore@thedragonfly.com" },
    { "id": "sstjames@thedragonfly.com" }
  ]
}
```

**Response (JSON):** An array of contact objects.


### 3. Update Contacts

**a) Individual Contact (PATCH `/crm/v3/objects/contacts/{contactId}` or `/crm/v3/objects/contacts/{email}?idProperty=email`)**

Updates a single contact by ID or email.

**Request Body (JSON):**

```json
{
  "properties": {
    "favorite_food": "burger",
    "jobtitle": "Manager",
    "lifecyclestage": "Customer" // Updating lifecycle stage: only forward movement allowed.
  }
}
```

**b) Batch Update (POST `/crm/v3/objects/contacts/batch/update`)**

Updates multiple contacts by their IDs.  Limited to 100 contacts per request.

**Request Body (JSON):**

```json
{
  "inputs": [
    { "id": "123456789", "properties": { "favorite_food": "burger" } },
    { "id": "56789123", "properties": { "favorite_food": "Donut" } }
  ]
}
```


### 4. Upsert Contacts (POST `/crm/v3/objects/contacts/batch/upsert`)

Creates or updates contacts in a batch. Uses `email` or a custom unique identifier property.

**Request Body (JSON):**

```json
{
  "inputs": [
    {
      "properties": { "phone": "5555555555" },
      "id": "test@test.com",
      "idProperty": "email"
    },
    // ... more contacts
  ]
}
```


### 5. Associate Contacts (PUT `/crm/v3/objects/contacts/{contactId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates a contact with other CRM records or activities.

### 6. Remove Association (DELETE `/crm/v3/objects/contacts/{contactID}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Removes an association between a contact and another record or activity.

### 7. Pin Activity (PATCH `/crm/v3/objects/contacts/{contactId}`)

Pins an activity to a contact record using the `hs_pinned_engagement_id` property.

### 8. Delete Contacts (DELETE `/crm/v3/objects/contacts/{contactId}`)

Deletes a contact (moves to recycling bin).


### 9. Secondary Emails

Manage secondary emails using the `hs_additional_emails` property (multiple emails separated by semicolons).


### Limits

Batch operations are limited to 100 records per request.  See documentation for other limits.


This documentation provides a comprehensive overview.  Refer to the official HubSpot API documentation for detailed specifications and error handling.
