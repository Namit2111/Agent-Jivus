# HubSpot CRM API: Contacts

This document details the HubSpot CRM API endpoints for managing contacts.  Contacts in HubSpot store information about individuals interacting with your business. These endpoints allow you to create, manage, and sync contact data between HubSpot and other systems.

## Understanding the Basics

Before using the API, familiarize yourself with:

* **Objects, Records, Properties, and Associations APIs:** [Understanding the CRM Guide](link_to_guide_needed)
* **Managing your CRM database:** [Learn how to manage your CRM database](link_to_guide_needed)

## Endpoints

### 1. Create Contacts

* **Method:** `POST`
* **Endpoint:** `/crm/v3/objects/contacts`

Create new contacts by sending a `POST` request to this endpoint.  Include contact data within a `properties` object.  You can also include an `associations` object to link the new contact with existing records (companies, deals) or activities (meetings, notes).

**Required Properties:** At least one of `email`, `firstname`, or `lastname` is required.  `email` is strongly recommended as it's the primary unique identifier to prevent duplicates.

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

**Note on `lifecyclestage`:** If included, use the internal name (text for default stages, numeric for custom stages).  Find the internal ID in your lifecycle stage settings or via the API.


### 2. Properties

Contact details are stored in properties.  HubSpot provides default properties, and you can create custom ones.  To view available properties, make a `GET` request to `/crm/v3/properties/contacts`.  Learn more about the [properties API](link_to_properties_api_needed).

### 3. Associations

Associate new contacts with existing records or activities using the `associations` object within the `POST` request to `/crm/v3/objects/contacts`.

**Example Request Body (with Associations):**

```json
{
  "properties": {
    "email": "example@hubspot.com",
    "firstname": "Jane",
    "lastname": "Doe"
  },
  "associations": [
    {
      "to": { "id": 123456 },
      "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 279 } ]
    },
    {
      "to": { "id": 556677 },
      "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 197 } ]
    }
  ]
}
```

* **`to.id`:** Unique ID of the record or activity.
* **`types`:** Association type.  Use the default IDs [here](link_to_default_ids_needed) or retrieve custom IDs via the [associations API](link_to_associations_api_needed).


### 4. Retrieve Contacts

* **Individual Contact:** `GET` `/crm/v3/objects/contacts/{contactId}` or `/crm/v3/objects/contacts/{email}?idProperty=email`
* **All Contacts:** `GET` `/crm/v3/objects/contacts`
* **Batch Read:** `POST` `/crm/v3/objects/contacts/batch/read` (cannot retrieve associations)

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of current and historical properties.
* `associations`: Comma-separated list of objects to retrieve associated IDs for.
* `idProperty`: For batch read, use `email` or a custom unique identifier property (default is `hs_object_id`).


**Example Batch Read Request Body (by record ID):**

```json
{
  "properties": ["email", "lifecyclestage", "jobtitle"],
  "inputs": [ { "id": "1234567" }, { "id": "987456" } ]
}
```

**Example Batch Read Request Body (by email):**

```json
{
  "properties": ["email", "lifecyclestage", "jobtitle"],
  "idProperty": "email",
  "inputs": [ { "id": "lgilmore@thedragonfly.com" }, { "id": "sstjames@thedragonfly.com" } ]
}
```


### 5. Update Contacts

* **Individual Contact (by ID):** `PATCH` `/crm/v3/objects/contacts/{contactId}`
* **Individual Contact (by email):** `PATCH` `/crm/v3/objects/contacts/{email}?idProperty=email`
* **Batch Update:** `POST` `/crm/v3/objects/contacts/batch/update`

**Note on `lifecyclestage` updates:**  Can only be moved forward in the stage order.  Clear the existing value to move backward.

**Example Individual Update Request Body:**

```json
{
  "properties": {
    "favorite_food": "burger",
    "jobtitle": "Manager",
    "lifecyclestage": "Customer"
  }
}
```

**Example Batch Update Request Body:**

```json
{
  "inputs": [
    { "id": "123456789", "properties": { "favorite_food": "burger" } },
    { "id": "56789123", "properties": { "favorite_food": "Donut" } }
  ]
}
```


### 6. Upsert Contacts

* **Method:** `POST`
* **Endpoint:** `/crm/v3/objects/contacts/batch/upsert`

Batch creates and updates contacts.  Uses `email` or a custom unique identifier property.

**Example Request Body (using email):**

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


### 7. Associate Existing Contacts

* **Method:** `PUT`
* **Endpoint:** `/crm/v3/objects/contacts/{contactId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

Associate a contact with other CRM records or activities.

### 8. Remove Association

* **Method:** `DELETE`
* **Endpoint:** `/crm/v3/objects/contacts/{contactID}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


### 9. Pin an Activity

Pin an activity to a contact record using the `hs_pinned_engagement_id` property.  Requires the activity ID (retrievable via [engagements APIs](link_to_engagements_api_needed)). Only one activity can be pinned per contact.

### 10. Delete Contacts

* **Individual Contact:** `DELETE` `/crm/v3/objects/contacts/{contactId}`
* **Batch Delete:** [Reference Documentation](link_to_batch_delete_doc_needed)

Adds the contact to the recycling bin; you can restore it later.


### 11. Secondary Emails

Manage secondary email addresses using the `hs_additional_emails` property.  Multiple emails are separated by semicolons.  For V1 API usage, see [this reference guide](link_to_v1_secondary_email_guide_needed).


### 12. Limits

Batch operations are limited to 100 records per request.  See limits for contacts and form submissions [here](link_to_limits_doc_needed).


**(Remember to replace placeholder links with the actual links from the HubSpot documentation.)**
