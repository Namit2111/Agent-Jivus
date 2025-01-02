# HubSpot CRM API: Contacts

This document details the HubSpot CRM API endpoints for managing contacts.  Contacts store information about individuals interacting with your business.  These endpoints allow for creating, managing, and syncing contact data between HubSpot and other systems.

## Understanding the CRM

For a comprehensive understanding of HubSpot's object, record, property, and association APIs, refer to the [Understanding the CRM guide](link_to_understanding_crm_guide).  For general information on managing your CRM database, see [Managing your CRM database](link_to_managing_crm_database).


## Endpoints

All endpoints are under the `/crm/v3/objects/contacts` base URL unless otherwise specified.

### 1. Create Contacts

**Endpoint:** `/crm/v3/objects/contacts`

**Method:** `POST`

**Request Body:** JSON

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

* **properties:**  An object containing contact details.  At least one of `email`, `firstname`, or `lastname` is required. `email` is recommended as the primary unique identifier.  See the [Properties](#2-properties) section for details.
* **associations (optional):** An array of objects associating the contact with existing records or activities.  See the [Associations](#3-associations) section for details.


**Response:** JSON (Contact object)


### 2. Properties

Contact details are stored in properties.  HubSpot provides default properties, and you can create custom ones.  To view available properties, use:

**Endpoint:** `/crm/v3/properties/contacts`

**Method:** `GET`

**Response:** JSON (List of contact properties)

**Important Note:**  If including `lifecyclestage`, use the internal name (text for default, numeric for custom). Find the internal ID in lifecycle stage settings or via API.


### 3. Associations

When creating or updating contacts, you can associate them with other records (e.g., companies, deals) or activities (e.g., meetings, notes).

**Parameters (within the `associations` array):**

* **to.id:** The ID of the record or activity to associate.
* **types:** An array of association types.  `associationCategory` and `associationTypeId` are required.  Default `associationTypeId` values are listed [here](link_to_association_type_ids), or retrieve custom values via the Associations API.

### 4. Retrieve Contacts

**Individual Contact:**

**Endpoint:** `/crm/v3/objects/contacts/{contactId}` or `/crm/v3/objects/contacts/{email}?idProperty=email`

**Method:** `GET`

**Query Parameters (optional):**

* **properties:** Comma-separated list of properties to return.
* **propertiesWithHistory:** Comma-separated list of current and historical properties.
* **associations:** Comma-separated list of associated objects to retrieve.

**Batch Retrieval:**

**Endpoint:** `/crm/v3/objects/contacts/batch/read`

**Method:** `POST`

**Request Body:** JSON

**Example Request Body (by record ID):**

```json
{
  "properties": ["email", "lifecyclestage", "jobtitle"],
  "inputs": [
    {"id": "1234567"},
    {"id": "987456"}
  ]
}
```

**Example Request Body (by email):**

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

* **properties:** Comma-separated list of properties to return.
* **propertiesWithHistory:** Comma-separated list of current and historical properties to return.
* **idProperty:**  Specify if using `email` or a custom unique identifier property.  Required if not using record ID.
* **inputs:** Array of objects, each with an `id` matching the `idProperty`.

**Response:** JSON (Array of contact objects)


### 5. Update Contacts

**Individual Contact:**

**Endpoint:** `/crm/v3/objects/contacts/{contactId}` or `/crm/v3/objects/contacts/{email}?idProperty=email`

**Method:** `PATCH`

**Request Body:** JSON (properties to update)

**Example Request Body (by record ID):**

```json
{
  "properties": {
    "favorite_food": "burger",
    "jobtitle": "Manager",
    "lifecyclestage": "Customer"
  }
}
```

**Batch Update:**

**Endpoint:** `/crm/v3/objects/contacts/batch/update`

**Method:** `POST`

**Request Body:** JSON

**Example Request Body:**

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

**Note on `lifecyclestage` update:** Can only be set forward in the stage order.  To move backward, clear the existing value manually or via workflow/integration.


### 6. Upsert Contacts

**Endpoint:** `/crm/v3/objects/contacts/batch/upsert`

**Method:** `POST`

**Request Body:** JSON

**Example Request Body (using email):**

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

Uses `email` or a custom unique identifier property (`idProperty`) to determine whether to create or update.


### 7. Associate Existing Contacts

**Endpoint:** `/crm/v3/objects/contacts/{contactId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `PUT`

Requires `associationTypeId` (from default list or via Associations API).


### 8. Remove Association

**Endpoint:** `/crm/v3/objects/contacts/{contactID}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `DELETE`


### 9. Pin Activity

**Endpoint:** `/crm/v3/objects/contacts/{contactId}`

**Method:** `PATCH`

**Request Body:** JSON (include `hs_pinned_engagement_id` with the activity ID).  Activity must already be associated with the contact.


### 10. Delete Contacts

**Individual Contact:**

**Endpoint:** `/crm/v3/objects/contacts/{contactId}`

**Method:** `DELETE`

Batch delete is covered in the [reference documentation](link_to_batch_delete_docs).


### 11. Secondary Emails

Use `hs_additional_emails` property to view or add secondary emails (separated by semicolons).


### 12. Limits

Batch operations are limited to 100 records.  See [contacts and form submissions limits](link_to_limits_docs) for further information.


Remember to replace placeholders like `{contactId}`, `{email}`, `{toObjectId}`, and `{associationTypeId}` with actual values.  Always refer to the official HubSpot API documentation for the most up-to-date information and details.  Replace the bracketed links with the actual links from the HubSpot documentation.
