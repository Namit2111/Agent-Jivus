# HubSpot CRM API: Contacts

This document details the HubSpot CRM API endpoints for managing contacts.  Contacts in HubSpot store information about individuals who interact with your business. These endpoints allow you to create, manage, and sync contact data between HubSpot and other systems.

## Understanding the CRM

For a comprehensive understanding of objects, records, properties, and associations within the HubSpot CRM API, refer to the [Understanding the CRM](link-to-understanding-crm-guide) guide.  For general CRM database management, see [Managing your CRM Database](link-to-crm-database-management).


## Create Contacts

To create new contacts, send a `POST` request to `/crm/v3/objects/contacts`.

Include contact data within a `properties` object in your request. You can also add an `associations` object to link the new contact with existing records (e.g., companies, deals) or activities (e.g., meetings, notes).

**Required Properties:** At least one of the following properties must be included: `email`, `firstname`, or `lastname`.  Using `email` is strongly recommended, as it's the primary unique identifier to prevent duplicates.

**Example Request Body (JSON):**

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

**Lifecycle Stage Note:** If including `lifecyclestage`, use the internal name (not the label).  Default stages use text values (e.g., `subscriber`, `marketingqualifiedlead`), while custom stages use numeric values. Find the internal ID in your lifecycle stage settings or via the API.


## Properties

Contact details are stored in properties.  HubSpot provides [default contact properties](link-to-default-properties), and you can [create custom contact properties](link-to-custom-properties).  Retrieve a list of available properties with a `GET` request to `/crm/v3/properties/contacts`. Learn more about the [properties API](link-to-properties-api).


## Associations

Associate new contacts with existing records or activities using the `associations` object.

**Example Request Body (JSON):**

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

| Parameter       | Description                                                                                             |
|-----------------|---------------------------------------------------------------------------------------------------------|
| `to.id`         | The ID of the record or activity to associate.                                                        |
| `types`         | Association type. Include `associationCategory` and `associationTypeId`.  See [default association type IDs](link-to-default-association-types) or use the [associations API](link-to-associations-api) for custom types. |


## Retrieve Contacts

Retrieve contacts individually or in batches.

**Individual Contact:** `GET /crm/v3/objects/contacts/{contactId}` or `GET /crm/v3/objects/contacts/{email}?idProperty=email`

**All Contacts:** `GET /crm/v3/objects/contacts`

**Batch Retrieval (POST /crm/v3/objects/contacts/batch/read):**  Retrieve a batch of contacts by record ID, email, or custom unique identifier property.  Associations cannot be retrieved via this endpoint.  Use the [associations API](link-to-associations-api) for batch association retrieval.

**Query Parameters:**

| Parameter           | Description                                                                                                            |
|--------------------|------------------------------------------------------------------------------------------------------------------------|
| `properties`        | Comma-separated list of properties to return.  Missing properties won't be included.                               |
| `propertiesWithHistory` | Comma-separated list of current and historical properties to return. Missing properties won't be included.              |
| `associations`      | Comma-separated list of objects to retrieve associated IDs for.  Non-existent associations are omitted.  |
| `idProperty`       |  Used for batch retrieval when using `email` or a custom unique identifier property (instead of `hs_object_id`).  |


**Example Request Body (Batch, Record IDs):**

```json
{
  "properties": ["email", "lifecyclestage", "jobtitle"],
  "inputs": [
    {"id": "1234567"},
    {"id": "987456"}
  ]
}
```

**Example Request Body (Batch, Email):**

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


## Update Contacts

Update contacts individually or in batches.

**Individual Contact (PATCH):**

* **By ID:** `PATCH /crm/v3/objects/contacts/{contactId}`
* **By Email:** `PATCH /crm/v3/objects/contacts/{email}?idProperty=email`

**Batch Update (POST /crm/v3/objects/contacts/batch/update):**  Updates multiple contacts using their record IDs.

**Lifecycle Stage Note (Updates):** When updating `lifecyclestage`, you can only move forward in the stage order.  To move backward, clear the existing value manually, via workflow, or through a data-syncing integration.


**Example Request Body (Individual Update):**

```json
{
  "properties": {
    "favorite_food": "burger",
    "jobtitle": "Manager",
    "lifecyclestage": "Customer"
  }
}
```

**Example Request Body (Batch Update):**

```json
{
  "inputs": [
    {"id": "123456789", "properties": {"favorite_food": "burger"}},
    {"id": "56789123", "properties": {"favorite_food": "Donut"}}
  ]
}
```


## Upsert Contacts

Batch create and update contacts using `POST /crm/v3/objects/contacts/batch/upsert`. Use `idProperty` to specify whether you're using `email` or a custom unique identifier.

**Example Request Body (Email as ID):**

```json
{
  "inputs": [
    {"properties": {"phone": "5555555555"}, "id": "test@test.com", "idProperty": "email"},
    {"properties": {"phone": "7777777777"}, "id": "example@hubspot.com", "idProperty": "email"}
  ]
}
```


## Associate Existing Contacts

Associate a contact with other CRM records or activities using a `PUT` request:

`PUT /crm/v3/objects/contacts/{contactId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

Retrieve `associationTypeId` from the [default values list](link-to-default-association-types) or via a `GET` request to `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`.  See the [associations API](link-to-associations-api) for details.


## Remove an Association

Remove an association with a `DELETE` request:

`DELETE /crm/v3/objects/contacts/{contactID}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


## Pin an Activity

Pin an activity to a contact record using the `hs_pinned_engagement_id` property.  You can pin one activity per record; it must already be associated with the contact.  The activity ID can be retrieved via the [engagements APIs](link-to-engagements-api).

**Example Request Body (PATCH):**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```


## Delete Contacts

Delete contacts (moves them to the recycling bin) individually or in batches.  See the [reference documentation](link-to-batch-delete-docs) for batch deletion.  Individual deletion: `DELETE /crm/v3/objects/contacts/{contactId}`.  Contacts can be restored from the recycling bin within HubSpot.


## Secondary Emails

Manage secondary emails using the `hs_additional_emails` property (multiple emails separated by semicolons).  For V1 APIs, see the [secondary email reference guide](link-to-v1-secondary-email-guide).


## Limits

Batch operations are limited to 100 records per request.  See limits for [contacts and form submissions](link-to-contact-form-submission-limits).


**(Remember to replace placeholder links like `link-to-understanding-crm-guide` with the actual links.)**
