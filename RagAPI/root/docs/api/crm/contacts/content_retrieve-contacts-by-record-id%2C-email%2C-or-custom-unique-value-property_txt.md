# HubSpot CRM API: Contacts

This document details the HubSpot CRM API endpoints for managing contacts.  Contacts store information about individuals interacting with your business.  These endpoints allow creation, management, and synchronization of contact data with other systems.

## Understanding HubSpot CRM Objects, Records, Properties, and Associations

Before using the API, familiarize yourself with HubSpot's [CRM object model](link_to_hubspot_crm_object_guide).  This guide explains objects, records, properties, and associations.  For managing your CRM database, see [this guide](link_to_hubspot_crm_database_management).


## API Endpoints

All endpoints are prefixed with `/crm/v3/objects/contacts`.  Replace `{contactId}` with the contact's record ID, and `{email}` with the contact's email address.


### 1. Create Contacts

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/contacts`

**Request Body:** JSON

Requires at least one of `email`, `firstname`, or `lastname`.  `email` is strongly recommended as the primary unique identifier to prevent duplicates.

**Example Request (with associations):**

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

* **`properties`:**  Contact data.  Use default or custom properties.  See [default properties](link_to_default_contact_properties) and learn how to [create custom properties](link_to_creating_custom_properties).
* **`associations`:** (Optional)  Associates the contact with existing records or activities.  `to.id` is the ID of the record/activity.  `associationTypeId` can be found in the [default association types list](link_to_default_association_types) or retrieved via the [associations API](link_to_associations_api).  `associationCategory` is typically "HUBSPOT_DEFINED".


**Response:**  A JSON object representing the newly created contact, including its ID.

### 2. Retrieve Contacts

**Method:** `GET` (individual) and `POST` (batch)

**Endpoints:**

* **Individual:** `/crm/v3/objects/contacts/{contactId}` or `/crm/v3/objects/contacts/{email}?idProperty=email`
* **Batch:** `/crm/v3/objects/contacts/batch/read`


**Query Parameters (for individual GET requests):**

* **`properties`:** Comma-separated list of properties to return.
* **`propertiesWithHistory`:** Comma-separated list of properties to return, including historical data.
* **`associations`:** Comma-separated list of associated objects to retrieve.


**Batch Read Request Body (example with email):**

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

* **`properties` or `propertiesWithHistory`:**  Similar to individual requests.
* **`idProperty`:** Specifies whether IDs in `inputs` are record IDs (`hs_object_id`), emails, or custom unique properties.  Required when not using record IDs.
* **`inputs`:** Array of objects, each with an `id` matching the `idProperty`.


**Response:**  A JSON object (individual) or array of JSON objects (batch) representing the retrieved contact(s).


### 3. Update Contacts

**Method:** `PATCH` (individual) and `POST` (batch)

**Endpoints:**

* **Individual:** `/crm/v3/objects/contacts/{contactId}` or `/crm/v3/objects/contacts/{email}?idProperty=email`
* **Batch:** `/crm/v3/objects/contacts/batch/update`


**Request Body (PATCH - individual):**

```json
{
  "properties": {
    "favorite_food": "burger",
    "jobtitle": "Manager",
    "lifecyclestage": "Customer"
  }
}
```

**Request Body (POST - batch):**

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


**Response:**  A JSON object (individual) or array of JSON objects (batch) representing the updated contact(s).  Note lifecycle stage updates are unidirectional.



### 4. Upsert Contacts

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/contacts/batch/upsert`

**Request Body:**

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

* **`idProperty`:** Specifies whether IDs in `inputs` are emails or custom unique properties.  Required.
* **`inputs`:** Array of objects, each with an `id` matching the `idProperty` and `properties` to set or update.

**Response:** A JSON array of objects, one for each upserted contact, indicating whether it was created or updated.


### 5. Associate Contacts

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/contacts/{contactId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

* Replace `{toObjectType}` with the type of object to associate (e.g., `companies`).
* Replace `{toObjectId}` with the ID of the object.
* Replace `{associationTypeId}` with the association type ID (see default list or use associations API).

**Response:**  A success or failure indication.


### 6. Remove Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/contacts/{contactID}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

* Parameters same as Associate Contacts.

**Response:** A success or failure indication.


### 7. Pin Activity

**Method:** `PATCH` (to existing contact) or `POST` (when creating a contact)

**Endpoint:** `/crm/v3/objects/contacts/{contactId}` (PATCH) or `/crm/v3/objects/contacts` (POST)


**Request Body (PATCH):**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789 
  }
}
```

**Response:** A JSON object representing the updated contact.



### 8. Delete Contacts

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/contacts/{contactId}`

**Response:** A success or failure indication.  Contacts are moved to the recycle bin.


### 9. Secondary Emails

Use `hs_additional_emails` property to manage secondary emails (comma-separated list when updating).


### 10. Limits

Batch operations are limited to 100 records.  See [limits documentation](link_to_hubspot_api_limits) for further details.


**Note:**  Replace placeholder links with actual HubSpot documentation links.  Error handling and authentication details are omitted for brevity but are crucial in real-world implementations.  Remember to use appropriate HTTP headers (e.g., `Authorization` with your API key).
