# HubSpot CRM API: Contacts

This document details the HubSpot CRM API endpoints for managing contacts.  Contacts in HubSpot store information about individuals interacting with your business.  These endpoints allow for creating, managing, and syncing contact data between HubSpot and other systems.

For a broader understanding of objects, records, properties, and associations within the HubSpot CRM API, refer to the [Understanding the CRM](link-to-understanding-crm-guide) guide.  For general CRM database management information, see [Managing your CRM database](link-to-crm-database-management).


## Create Contacts

Use a `POST` request to `/crm/v3/objects/contacts` to create new contacts.  The request body should include a `properties` object containing contact data.  Optionally, include an `associations` object to link the new contact with existing records (e.g., companies, deals) or activities (e.g., meetings, notes).

**Required Properties:** At least one of `email`, `firstname`, or `lastname` must be included.  Using `email` is strongly recommended as it's the primary unique identifier, preventing duplicates.

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

**Lifecycle Stage Note:** If `lifecyclestage` is included, use the internal name (not the label). Default stages use text values (e.g., `"subscriber"`, `"marketingqualifiedlead"`), while custom stages use numeric values.  Find the internal ID in your lifecycle stage settings or via the API.


## Properties

Contact details are stored in properties.  HubSpot provides default contact properties, and you can also [create custom contact properties](link-to-custom-properties-creation).  To view all available properties, use a `GET` request to `/crm/v3/properties/contacts`.  Learn more about the [properties API](link-to-properties-api).


## Associations

Associate new contacts with existing records or activities using the `associations` object in the `POST` request to `/crm/v3/objects/contacts`.

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

* **`to.id`:** The ID of the record or activity.
* **`types`:** The association type, including `associationCategory` and `associationTypeId`.  See [default association type IDs](link-to-default-association-types) or use the [associations API](link-to-associations-api) for custom types.


## Retrieve Contacts

Contacts can be retrieved individually or in batches.

**Individual Contacts:**

* Use a `GET` request to `/crm/v3/objects/contacts/{contactId}` (by ID) or `/crm/v3/objects/contacts/{email}?idProperty=email` (by email).

**All Contacts:**

* Use a `GET` request to `/crm/v3/objects/contacts`.

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of current and historical properties to return.
* `associations`: Comma-separated list of associated objects to retrieve IDs for.

**Batch Retrieval:**

* Use a `POST` request to `/crm/v3/objects/contacts/batch/read`.  This endpoint does *not* retrieve associations. Use the [associations API](link-to-associations-api) for batch association reads.
* `idProperty`:  Use this parameter to specify whether `id` values in the request body refer to record IDs (`hs_object_id`), email addresses, or a custom unique identifier property.

**Example Batch Request Body (by ID):**

```json
{
  "properties": ["email", "lifecyclestage", "jobtitle"],
  "inputs": [
    {
      "id": "1234567"
    },
    {
      "id": "987456"
    }
  ]
}
```

**Example Batch Request Body (by email):**

```json
{
  "properties": ["email", "lifecyclestage", "jobtitle"],
  "idProperty": "email",
  "inputs": [
    {
      "id": "lgilmore@thedragonfly.com"
    },
    {
      "id": "sstjames@thedragonfly.com"
    }
  ]
}
```


## Update Contacts

Contacts can be updated individually or in batches.

**Individual Updates:**

* Use a `PATCH` request to `/crm/v3/objects/contacts/{contactId}` (by ID) or `/crm/v3/objects/contacts/{email}?idProperty=email` (by email).

**Batch Updates:**

* Use a `POST` request to `/crm/v3/objects/contacts/batch/update`.

**Lifecycle Stage Update Note:** When updating `lifecyclestage`, you can only move it *forward* in the stage order. To move it backward, first clear the existing value (manually, via workflow, or integration).


## Upsert Contacts

Batch create and update contacts simultaneously using a `POST` request to `/crm/v3/objects/contacts/batch/upsert`.  Use `idProperty` to specify whether `id` values represent email or a custom unique identifier.


## Associate/Disassociate Contacts

* **Associate:** Use a `PUT` request to `/crm/v3/objects/contacts/{contactId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`.
* **Disassociate:** Use a `DELETE` request to `/crm/v3/objects/contacts/{contactID}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`.


## Pin an Activity

Pin an activity to a contact record using the `hs_pinned_engagement_id` property (containing the activity ID) in a `PATCH` request to `/crm/v3/objects/contacts/{contactId}`.  You can pin one activity per contact.


## Delete Contacts

Delete contacts individually (using a `DELETE` request to `/crm/v3/objects/contacts/{contactId}`) or in batches (see [reference documentation](link-to-batch-delete-docs)).  Deleted contacts are moved to the recycling bin and can be restored.


## Secondary Emails

Manage secondary emails using the `hs_additional_emails` property.  Multiple emails are separated by semicolons.


## Limits

Batch operations are limited to 100 records per request.  See further limits for [contacts and form submissions](link-to-limits-docs).


**(Remember to replace placeholder links like `link-to-understanding-crm-guide` with actual links to the relevant HubSpot documentation.)**
