# HubSpot CRM API: Contacts

This document details the HubSpot CRM API endpoints for managing contacts.  Contacts store information about individuals interacting with your business.  These endpoints allow creation, management, and synchronization of contact data between HubSpot and other systems.

## Understanding the CRM (Prerequisites)

Before using these APIs, familiarize yourself with HubSpot's CRM concepts:

* **Objects:** Represent data categories (e.g., contacts, companies).
* **Records:** Individual entries within an object (e.g., a specific contact).
* **Properties:** Data fields within an object (e.g., email, firstname for contacts).
* **Associations:** Links between records of different objects (e.g., a contact associated with a company).

See the [Understanding the CRM guide](link-to-guide) and [managing your CRM database](link-to-guide) for more information.


## API Endpoints

All endpoints use the `/crm/v3/objects/contacts` base path unless otherwise specified.  Requests require proper authentication (API key).

### 1. Create Contacts (POST `/crm/v3/objects/contacts`)

Creates new contacts.  Requires at least one of `email`, `firstname`, or `lastname`.  `email` is strongly recommended as the primary unique identifier.

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
  "associations": [  // Optional: Associate with existing records/activities
    {
      "to": {"id": 123456}, // ID of the associated record/activity
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 279}] // Association type (see below)
    }
  ]
}
```

* **`properties`:**  Object containing contact data.  Use [default](link-to-default-properties) or [custom](link-to-custom-properties) properties.
* **`associations`:** (Optional) Array of objects associating the contact with existing records or activities.  `associationTypeId` can be found in [this list](link-to-association-types) or via the [associations API](link-to-associations-api).

**Response (JSON):**  A successful response will contain the created contact's ID and other details.


### 2. Retrieve Contacts

**a) Individual Contact (GET `/crm/v3/objects/contacts/{contactId}` or `/crm/v3/objects/contacts/{email}?idProperty=email`)**

Retrieves a single contact by ID or email.

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including history.
* `associations`: Comma-separated list of associated objects to retrieve.


**b) All Contacts (GET `/crm/v3/objects/contacts`)**

Retrieves a list of all contacts.  Use pagination for large datasets.  Same query parameters as above.

**c) Batch Read (POST `/crm/v3/objects/contacts/batch/read`)**

Retrieves multiple contacts by ID, email, or a custom unique identifier property.  Does *not* retrieve associations.

**Request Body (JSON):**

```json
{
  "properties": ["email", "lifecyclestage", "jobtitle"],  // Or "propertiesWithHistory"
  "idProperty": "email", // Optional, required for email or custom unique ID
  "inputs": [
    {"id": "lgilmore@thedragonfly.com"},
    {"id": "12345"} // ID based on idProperty
  ]
}
```


### 3. Update Contacts

**a) Individual Contact (PATCH `/crm/v3/objects/contacts/{contactId}` or `/crm/v3/objects/contacts/{email}?idProperty=email`)**

Updates a single contact by ID or email.

**Request Body (JSON):**

```json
{
  "properties": {
    "favorite_food": "burger",
    "jobtitle": "Manager",
    "lifecyclestage": "Customer" // Updating lifecycleStage: only forward movement allowed.
  }
}
```

**b) Batch Update (POST `/crm/v3/objects/contacts/batch/update`)**

Updates multiple contacts.  Uses contact IDs.  Limited to 100 contacts per request.


### 4. Upsert Contacts (POST `/crm/v3/objects/contacts/batch/upsert`)

Creates or updates contacts in batches. Uses `email` or a custom unique identifier.

**Request Body (JSON):**

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

### 5. Associate/Disassociate Contacts (PUT/DELETE `/crm/v3/objects/contacts/{contactId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates or removes associations between contacts and other records/activities.  Use the [associations API](link-to-associations-api) to get `associationTypeId`.


### 6. Pin Activity (PATCH `/crm/v3/objects/contacts/{contactId}`)

Pins an activity to a contact record using `hs_pinned_engagement_id`.  Requires the activity ID from the [engagements API](link-to-engagements-api).  Only one activity can be pinned per contact.


### 7. Delete Contacts (DELETE `/crm/v3/objects/contacts/{contactId}`)

Deletes contacts (moves them to the recycling bin).  See documentation for batch deletion.


### 8. Secondary Emails

Use `hs_additional_emails` property to manage secondary emails.  Multiple emails are separated by semicolons.


### Limits

Batch operations are limited to 100 records at a time.  See documentation for other limits.


**Note:**  Replace placeholder links (e.g., `link-to-guide`) with actual HubSpot documentation links.  Error handling and authentication details are omitted for brevity but are crucial in a production implementation.
