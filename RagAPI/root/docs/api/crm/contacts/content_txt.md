# HubSpot CRM API: Contacts

This document describes the HubSpot CRM API endpoints for managing contacts.  Contacts store information about individuals interacting with your business.  These endpoints allow creation, management, and synchronization of contact data.

## Understanding the CRM

Before using these APIs, familiarize yourself with HubSpot's [Understanding the CRM guide](link_to_hubspot_guide_here) and [managing your CRM database](link_to_hubspot_guide_here).  This will clarify concepts like objects, records, properties, and associations.

## Endpoints

All endpoints are prefixed with `/crm/v3/objects/contacts`.  Replace `{contactId}` with the contact's record ID and `{email}` with the contact's email address.

### 1. Create Contacts

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/contacts`

**Request Body:**

The request body must include a `properties` object containing contact data. At least one of `email`, `firstname`, or `lastname` is required.  `email` is strongly recommended as it's the primary unique identifier.  You can also include an `associations` object to link the contact to existing records (companies, deals) or activities (meetings, notes).

**Example Request (JSON):**

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
    }
  ]
}
```

**Response:**  A JSON object representing the newly created contact, including its ID.

**Note on `lifecyclestage`:**  Use the internal name (e.g., "marketingqualifiedlead", "subscriber"), not the label.  For custom stages, use the numeric ID.


### 2. Retrieve Contacts

**Method:** `GET` (individual) or `POST` (batch)

**Endpoints:**

* **Individual:** `/crm/v3/objects/contacts/{contactId}` or `/crm/v3/objects/contacts/{email}?idProperty=email`
* **Batch:** `/crm/v3/objects/contacts/batch/read`

**Query Parameters (Individual):**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including history.
* `associations`: Comma-separated list of association types to retrieve.

**Request Body (Batch):**

```json
{
  "properties": ["email", "lifecyclestage", "jobtitle"],
  "idProperty": "email",  //Optional, use for email or custom unique identifier
  "inputs": [
    { "id": "lgilmore@thedragonfly.com" },
    { "id": "sstjames@thedragonfly.com" }
  ]
}
```


**Response:**  A JSON object (individual) or array (batch) containing contact data.


### 3. Update Contacts

**Method:** `PATCH` (individual) or `POST` (batch)

**Endpoints:**

* **Individual:** `/crm/v3/objects/contacts/{contactId}` or `/crm/v3/objects/contacts/{email}?idProperty=email`
* **Batch:** `/crm/v3/objects/contacts/batch/update`

**Request Body (Individual):**

```json
{
  "properties": {
    "favorite_food": "burger",
    "jobtitle": "Manager",
    "lifecyclestage": "Customer"
  }
}
```

**Request Body (Batch):**

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

**Response:** A JSON object indicating success or failure.  Note that `lifecyclestage` updates only allow moving *forward* in the stage order.


### 4. Upsert Contacts

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/contacts/batch/upsert`

**Request Body:**

Uses `idProperty` (email or custom unique identifier) and `id` to identify contacts.  Existing contacts are updated; new ones are created.

**Example Request (JSON):**

```json
{
  "inputs": [
    {
      "properties": { "phone": "5555555555" },
      "id": "test@test.com",
      "idProperty": "email"
    }
  ]
}
```

**Response:** A JSON object indicating success or failure for each contact.


### 5. Associate Contacts

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/contacts/{contactId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Parameters:**

* `{toObjectType}`:  Type of object to associate (e.g., `companies`, `deals`).
* `{toObjectId}`: ID of the object to associate.
* `{associationTypeId}`: Type of association (see HubSpot documentation for default IDs or use the `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels` endpoint to get custom IDs).


### 6. Remove Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/contacts/{contactID}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

### 7. Pin Activity

**Method:** `PATCH` (update existing contact) or `POST` (create contact and pin simultaneously)


**Endpoint:** `/crm/v3/objects/contacts/{contactId}` (PATCH) or `/crm/v3/objects/contacts` (POST)

**Request Body (PATCH):**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```

**Request Body (POST - combined with contact creation):**  Similar to create contact, but adds `hs_pinned_engagement_id` and associates with the activity.

### 8. Delete Contacts

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/contacts/{contactId}` (individual delete)  - See HubSpot documentation for batch delete.


### 9. Secondary Emails

Retrieve secondary emails using `properties=email,hs_additional_emails`.  Add secondary emails using the `hs_additional_emails` property (semicolon-separated).


## Limits

Batch operations are limited to 100 records per request.  Refer to HubSpot documentation for other limits.


This markdown provides a comprehensive overview. Always refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications.  Remember to replace placeholder values like `{contactId}`, `{email}`, and IDs with actual values.  Also note that  `link_to_hubspot_guide_here` needs to be replaced with the actual links from the HubSpot documentation.
