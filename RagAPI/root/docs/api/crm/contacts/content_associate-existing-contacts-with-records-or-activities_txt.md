# HubSpot CRM API: Contacts

This document details the HubSpot CRM API endpoints for managing contacts.  Contacts in HubSpot store information about individuals interacting with your business.  These endpoints allow creation, management, and synchronization of contact data.

## Understanding the CRM (Prerequisites)

Before using the API, familiarize yourself with HubSpot's CRM concepts:

* **Objects:**  Represent data types (e.g., Contacts, Companies, Deals).
* **Records:** Individual entries within an object (e.g., a specific contact).
* **Properties:** Attributes of an object (e.g., email, firstname, lastname for Contacts).
* **Associations:** Links between records of different objects (e.g., a Contact associated with a Company).

For more information, see the [Understanding the CRM guide](link_to_hubspot_guide_here).  Learn how to [manage your CRM database](link_to_hubspot_guide_here).


## API Endpoints

All endpoints are under the base URL `/crm/v3/objects/contacts`.  Replace `{contactId}` with the contact's ID and `{email}` with the contact's email address.

### 1. Create Contacts

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/contacts`

**Request Body:** JSON

Requires at least one of `email`, `firstname`, or `lastname`.  `email` is strongly recommended as the primary unique identifier to prevent duplicates.

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
        "id": 123456 // Company ID
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 279 // Association type ID (see documentation for list)
        }
      ]
    }
  ]
}
```

**`lifecyclestage` Note:** Use the internal name (e.g., `marketingqualifiedlead`), not the label.  Custom stages use numeric IDs.


### 2. Retrieve Contacts

**Method:** `GET` (individual) & `GET` (list) & `POST` (batch)


**Individual Contact by ID:**

* **Endpoint:** `/crm/v3/objects/contacts/{contactId}`
* **Query Parameters:** `properties` (comma-separated list), `propertiesWithHistory` (for historical data), `associations` (comma-separated list of associated objects).

**Individual Contact by Email:**

* **Endpoint:** `/crm/v3/objects/contacts/{email}?idProperty=email`
* **Query Parameters:** Same as above.

**List of Contacts:**

* **Endpoint:** `/crm/v3/objects/contacts`
* **Query Parameters:** Same as above.


**Batch Retrieval:**

* **Method:** `POST`
* **Endpoint:** `/crm/v3/objects/contacts/batch/read`
* **Request Body (JSON):**

```json
{
  "properties": ["email", "lifecyclestage", "jobtitle"],
  "idProperty": "email", //Optional, use for email or custom unique identifier
  "inputs": [
    { "id": "lgilmore@thedragonfly.com" },
    { "id": "sstjames@thedragonfly.com" }
  ]
}
```
`idProperty` is required if using email or a custom unique identifier property; otherwise, `id` refers to the record ID.  The batch endpoint does not retrieve associations.



### 3. Update Contacts

**Method:** `PATCH` (individual) & `POST` (batch)

**Individual Contact by ID:**

* **Method:** `PATCH`
* **Endpoint:** `/crm/v3/objects/contacts/{contactId}`
* **Request Body (JSON):**

```json
{
  "properties": {
    "favorite_food": "burger",
    "jobtitle": "Manager",
    "lifecyclestage": "Customer"
  }
}
```

**Individual Contact by Email:**

* **Method:** `PATCH`
* **Endpoint:** `/crm/v3/objects/contacts/{email}?idProperty=email`
* **Request Body (JSON):**  Same as above.

**`lifecyclestage` Note:** Updating `lifecyclestage` only allows moving *forward* in the stage order.


**Batch Update:**

* **Method:** `POST`
* **Endpoint:** `/crm/v3/objects/contacts/batch/update`
* **Request Body (JSON):**

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


### 4. Upsert Contacts

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/contacts/batch/upsert`

Allows creating or updating contacts in a batch. Use `idProperty` to specify if using `email` or a custom unique identifier.

**Example Request (JSON):**

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

### 5. Associate Contacts

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/contacts/{contactId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


### 6. Remove Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/contacts/{contactID}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

### 7. Pin an Activity

**Method:** `PATCH` (update existing contact) or `POST` (create new contact and pin)

Use the `hs_pinned_engagement_id` property.  Requires the activity to already be associated with the contact.

### 8. Delete Contacts

**Method:** `DELETE` (individual)

**Endpoint:** `/crm/v3/objects/contacts/{contactId}`


### 9. Secondary Emails

Use the `hs_additional_emails` property to manage secondary emails.


### 10. Limits

Batch operations are limited to 100 records per request.  See documentation for other limits.


This documentation provides a comprehensive overview of the HubSpot CRM API for managing contacts. Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
