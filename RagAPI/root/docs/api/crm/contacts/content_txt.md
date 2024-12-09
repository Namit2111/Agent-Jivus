# HubSpot CRM API: Contacts

This document details the HubSpot CRM API endpoints for managing contacts.  Contacts in HubSpot store information about individuals interacting with your business.  These endpoints allow for creating, managing, and syncing contact data between HubSpot and other systems.

For a broader understanding of objects, records, properties, and associations within the HubSpot API, refer to the [Understanding the CRM](link-to-understanding-crm-guide) guide.  General information on managing your CRM database can be found [here](link-to-crm-database-management).


## Create Contacts

Use a `POST` request to `/crm/v3/objects/contacts` to create new contacts.  Include contact data within a `properties` object.  An optional `associations` object can associate the new contact with existing records (companies, deals) or activities (meetings, notes).

**Required Properties:** At least one of `email`, `firstname`, or `lastname` is required.  Using `email` is strongly recommended as it's the primary unique identifier to prevent duplicates.

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

**Note on `lifecyclestage`:**  If included, use the internal name (not the label). Default stage internal names are text values; custom stage internal names are numeric.  Find internal IDs in your lifecycle stage settings or via the API.


## Properties

Contact details are stored in properties.  HubSpot provides default properties, but you can also create custom ones. To view all available properties, use a `GET` request to `/crm/v3/properties/contacts`. Learn more about the [properties API](link-to-properties-api).


## Associations

Associate contacts with existing records or activities using the `associations` object when creating or updating contacts.

**Example Request Body (JSON):**

```json
{
  "properties": {
    "email": "example@hubspot.com",
    "firstname": "Jane",
    "lastname": "Doe"
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

* **`to.id`:** The ID of the record or activity.
* **`types`:**  The association type. Use default IDs ([list of default association type IDs](link-to-default-association-types)) or retrieve custom association type IDs via the [associations API](link-to-associations-api).


## Retrieve Contacts

Retrieve contacts individually or in batches.

**Individual Contacts:**

* `GET /crm/v3/objects/contacts/{contactId}` (by ID)
* `GET /crm/v3/objects/contacts/{email}?idProperty=email` (by email)

**All Contacts:**

* `GET /crm/v3/objects/contacts`

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of current and historical properties.
* `associations`: Comma-separated list of associated objects to retrieve IDs for.

**Batch Retrieval:**

* `POST /crm/v3/objects/contacts/batch/read`  (cannot retrieve associations)

Use `idProperty` parameter for email or custom unique identifier properties.  Defaults to `hs_object_id` (record ID).

**Example Request Body (Batch, by ID):**

```json
{
  "properties": ["email", "lifecyclestage", "jobtitle"],
  "inputs": [
    { "id": "1234567" },
    { "id": "987456" }
  ]
}
```

**Example Request Body (Batch, by Email):**

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


## Update Contacts

Update contacts individually or in batches.

**Individual Updates:**

* `PATCH /crm/v3/objects/contacts/{contactId}` (by ID)
* `PATCH /crm/v3/objects/contacts/{email}?idProperty=email` (by email)

**Batch Updates:**

* `POST /crm/v3/objects/contacts/batch/update` (uses record IDs)

**Note on `lifecyclestage` updates:** Can only be moved forward in the stage order.  To move backward, clear the existing value manually or via workflow/integration.


## Upsert Contacts

Batch create and update contacts using  `email` or a custom unique identifier property.

* `POST /crm/v3/objects/contacts/batch/upsert`

Use `idProperty` to specify whether `id` values are emails or custom identifiers.


## Associate Existing Contacts

Associate a contact with other records or activities:

* `PUT /crm/v3/objects/contacts/{contactId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

Retrieve `associationTypeId` from the [list of default values](link-to-default-association-types) or via a `GET` request to `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`.


## Remove an Association

Remove an association:

* `DELETE /crm/v3/objects/contacts/{contactID}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


## Pin an Activity

Pin an activity to a contact record using the `hs_pinned_engagement_id` property (requires activity ID from [engagements APIs](link-to-engagements-api)).  Only one activity can be pinned per record; the activity must already be associated with the contact.


## Delete Contacts

Delete contacts individually or in batches (moves contacts to the recycling bin; can be restored).

* Individual: `DELETE /crm/v3/objects/contacts/{contactId}`
* Batch:  [Reference Documentation](link-to-batch-delete-docs)


## Secondary Emails

Handle secondary emails using the `hs_additional_emails` property (separated by semicolons).  Secondary emails are unique identifiers.


## Limits

Batch operations are limited to 100 records per request.  See documentation for other limits on [contacts and form submissions](link-to-limits-docs).


**(Remember to replace bracketed placeholders like `[link-to-understanding-crm-guide]` with the actual links.)**
