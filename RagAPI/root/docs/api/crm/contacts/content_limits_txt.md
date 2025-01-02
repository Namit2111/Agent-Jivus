# HubSpot CRM API: Contacts

This document describes the HubSpot CRM API endpoints for managing contacts.  Contacts store information about individuals interacting with your business.  These endpoints allow for creating, managing, and syncing contact data with other systems.

## Understanding HubSpot Contacts

In HubSpot, contact details are stored in properties.  These include default HubSpot properties and custom properties you can create.  `email`, `firstname`, or `lastname` are required when creating a new contact; `email` is strongly recommended as the primary unique identifier to prevent duplicates.

## API Endpoints

All endpoints are under the `/crm/v3/objects/contacts` base path unless otherwise specified.

### 1. Create Contacts

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/contacts`

**Request Body:**

The request body must include a `properties` object containing at least one of `email`, `firstname`, or `lastname`.  You can also include an `associations` object to link the new contact to existing records (companies, deals) or activities (meetings, notes).

**Example Request Body (with associations):**

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

**Response:**  A JSON object representing the newly created contact, including its ID.


**Note:**  `lifecyclestage` values must use the internal name (e.g., "marketingqualifiedlead," not the displayed label).  Custom lifecycle stage internal names are numeric.


### 2. Retrieve Contacts

**Method:** `GET` (individual) or `POST` (batch)

**Endpoint:**

* **Individual:** `/crm/v3/objects/contacts/{contactId}` (by ID) or `/crm/v3/objects/contacts/{email}?idProperty=email` (by email)
* **Batch:** `/crm/v3/objects/contacts/batch/read`

**Query Parameters (GET requests):**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return, including historical values.
* `associations`: Comma-separated list of associated objects to retrieve.

**Request Body (POST requests):**

```json
{
  "properties": ["email", "lifecyclestage", "jobtitle"], // or "propertiesWithHistory"
  "idProperty": "email", // Optional, required for email or custom unique identifier
  "inputs": [
    {
      "id": "1234567" // contactId or email or custom unique identifier
    },
    {
      "id": "987456"
    }
  ]
}
```

**Response:** A JSON object (individual) or array (batch) of contact data.


### 3. Update Contacts

**Method:** `PATCH` (individual) or `POST` (batch)

**Endpoint:**

* **Individual:** `/crm/v3/objects/contacts/{contactId}` (by ID) or `/crm/v3/objects/contacts/{email}?idProperty=email` (by email)
* **Batch:** `/crm/v3/objects/contacts/batch/update`

**Request Body (PATCH and POST):**

The request body includes a `properties` object with the fields to update.

**Example Request Body (PATCH individual):**

```json
{
  "properties": {
    "favorite_food": "burger",
    "jobtitle": "Manager",
    "lifecyclestage": "Customer"
  }
}
```

**Example Request Body (POST batch):**

```json
{
  "inputs": [
    {
      "id": "123456789",
      "properties": {
        "favorite_food": "burger"
      }
    },
    {
      "id": "56789123",
      "properties": {
        "favorite_food": "Donut"
      }
    }
  ]
}
```

**Response:**  A JSON object representing the updated contact(s).

**Note:** Updating `lifecyclestage` only allows moving forward in the stage order.  To move backward, clear the existing value first.


### 4. Upsert Contacts

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/contacts/batch/upsert`

**Request Body:**

Uses `idProperty` (`email` or a custom unique identifier) and `id` to identify contacts.  Existing contacts are updated; new contacts are created.

**Example Request Body:**

```json
{
  "inputs": [
    {
      "properties": {
        "phone": "5555555555"
      },
      "id": "test@test.com",
      "idProperty": "email"
    },
    {
      "properties": {
        "phone": "7777777777"
      },
      "id": "example@hubspot.com",
      "idProperty": "email"
    }
  ]
}
```

**Response:** A JSON array of results indicating success or failure for each contact.


### 5. Associate Contacts

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/contacts/{contactId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Request Body:** (Not needed for this endpoint)

**Response:** Confirmation of association.


### 6. Remove Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/contacts/{contactID}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Response:** Confirmation of removal.


### 7. Pin an Activity

**Method:** `PATCH` (update existing) or `POST` (create with activity)

**Endpoint:** `/crm/v3/objects/contacts/{contactId}`  (for update) or `/crm/v3/objects/contacts` (for create)

**Request Body:** Update the `hs_pinned_engagement_id` property.

**Example (PATCH):**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```


### 8. Delete Contacts

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/contacts/{contactId}`

**Response:** Confirmation of deletion (moves to recycling bin).


### 9. Secondary Emails

Use the `hs_additional_emails` property to manage secondary email addresses (semicolon-separated).


## Limits

Batch operations are limited to 100 records per request.  Refer to the HubSpot documentation for other limits.
