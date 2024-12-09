# HubSpot CRM API: Contacts

This document describes the HubSpot CRM API endpoints for managing contacts.  Contacts in HubSpot store information about individuals interacting with your business. These endpoints allow you to create, manage, and synchronize contact data between HubSpot and other systems.

## Understanding the CRM

For a comprehensive understanding of objects, records, properties, and associations within the HubSpot CRM API, refer to the [Understanding the CRM](link-to-understanding-crm-guide) guide.  For general information on managing your CRM database, see [Managing your CRM Database](link-to-crm-database-management).


## Create Contacts

Use a `POST` request to `/crm/v3/objects/contacts` to create new contacts.  Include contact data within a `properties` object.  Optionally, include an `associations` object to link the new contact with existing records (companies, deals) or activities (meetings, notes).

**Required Properties:** At least one of the following properties is required: `email`, `firstname`, or `lastname`.  Using `email` is strongly recommended as it's the primary unique identifier, preventing duplicate contacts.

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

**Note on `lifecyclestage`:** If included, values must use the lifecycle stage's *internal name*.  Default stages use text values (e.g., `"subscriber"`, `"marketingqualifiedlead"`) that don't change with label edits. Custom stages use numeric values, retrievable from lifecycle stage settings or via the API.


## Properties

Contact details are stored in properties. HubSpot provides default contact properties, and you can create custom ones.  To view all available properties, use a `GET` request to `/crm/v3/properties/contacts`.  Learn more about the [properties API](link-to-properties-api).


## Associations

Associate contacts with existing records or activities using the `associations` object in your `POST` request to `/crm/v3/objects/contacts`.

**Example Request Body (with Associations):**

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

**`associations` Object Parameters:**

| Parameter          | Description                                                                                             |
|----------------------|---------------------------------------------------------------------------------------------------------|
| `to.id`             | The ID of the record or activity to associate.                                                           |
| `types`             | An array of association types.  Each type includes `associationCategory` and `associationTypeId`.       |
| `associationTypeId` |  Use the list of [default association types](link-to-default-association-types) or retrieve custom types via the [associations API](link-to-associations-api). |


## Retrieve Contacts

Contacts can be retrieved individually or in batches.

**Individual Contacts:**

* Use a `GET` request to `/crm/v3/objects/contacts/{contactId}` (by record ID) or `/crm/v3/objects/contacts/{email}?idProperty=email` (by email).

**All Contacts:**

* Use a `GET` request to `/crm/v3/objects/contacts`.

**Query Parameters (for individual and all contacts):**

| Parameter            | Description                                                                                                |
|-----------------------|------------------------------------------------------------------------------------------------------------|
| `properties`          | Comma-separated list of properties to return.  Missing properties are omitted from the response.          |
| `propertiesWithHistory` | Comma-separated list of properties to return, including historical values. Missing properties are omitted. |
| `associations`        | Comma-separated list of objects to retrieve associated IDs for.  Missing associations are omitted.       |


**Batch Retrieval (`POST` to `/crm/v3/objects/contacts/batch/read`):**

This endpoint cannot retrieve associations. Use the [associations API](link-to-associations-api) for batch association reads.  The `idProperty` parameter specifies whether `id` values refer to record ID (`hs_object_id`), email, or a custom unique identifier property.

**Example Request Bodies (Batch Retrieval):**

* **By Record ID (current values):**  (Example shown, replace with actual IDs)
```json
{
  "properties": ["email", "lifecyclestage", "jobtitle"],
  "inputs": [
    {"id": "1234567"},
    {"id": "987456"}
  ]
}
```

* **By Record ID (current and historical values):** (Example shown, replace with actual IDs)
```json
{
  "propertiesWithHistory": ["lifecyclestage", "hs_lead_status"],
  "inputs": [
    {"id": "1234567"},
    {"id": "987456"}
  ]
}
```

* **By Email:** (Example shown, replace with actual emails)
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

* **By Custom Unique Identifier Property:** (Example shown, replace with actual IDs and property name)
```json
{
  "properties": ["email", "lifecyclestage", "jobtitle"],
  "idProperty": "internalcustomerid",
  "inputs": [
    {"id": "12345"},
    {"id": "67891"}
  ]
}
```


## Update Contacts

Contacts can be updated individually or in batches.

**Individual Updates:**

* Use a `PATCH` request to `/crm/v3/objects/contacts/{contactId}` (by record ID) or `/crm/v3/objects/contacts/{email}?idProperty=email` (by email).

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

**Note on `lifecyclestage` updates:**  Lifecycle stage values can only be updated *forward* in the stage order. To move backward, clear the existing value manually or via a workflow/integration.

**Batch Updates (`POST` to `/crm/v3/objects/contacts/batch/update`):**

Use record IDs (`id`) for batch updates.

**Example Request Body (Batch Update):**

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


## Upsert Contacts

Use the upsert endpoint (`POST` to `/crm/v3/objects/contacts/batch/upsert`) for batch creation and updates.  Use `email` or a custom unique identifier property (`idProperty`).  Existing contacts are updated; new ones are created.


**Example Request Body (Upsert with Email):**

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


## Associate Existing Contacts

Use a `PUT` request to `/crm/v3/objects/contacts/{contactId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}` to associate a contact with other CRM records or activities.  Retrieve `associationTypeId` from the list of default values or via a `GET` request to `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`. Learn more in the [associations API](link-to-associations-api) documentation.


## Remove an Association

Use a `DELETE` request to `/crm/v3/objects/contacts/{contactID}/associations/{toObjectType}/{toObjectId}/{associationTypeId}` to remove an association.


## Pin an Activity

Pin an activity to a contact record using the `hs_pinned_engagement_id` property (containing the activity ID, retrievable via the [engagements APIs](link-to-engagements-api)).  Only one activity can be pinned per record; the activity must already be associated with the contact.

**Example Request Body (Pinning Activity during Update):**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```

**Example Request Body (Pinning Activity during Creation):**

```json
{
  "properties": {
    "email": "example@hubspot.com",
    "firstname": "Jane",
    "lastname": "Doe",
    "phone": "(555) 555-5555",
    "hs_pinned_engagement_id": 123456789
  },
  "associations": [
    {
      "to": {
        "id": 123456789
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 201
        }
      ]
    }
  ]
}
```

## Delete Contacts

Contacts can be deleted individually or in batches (sent to the recycling bin; restorable later).

* **Individual Deletion:** Use a `DELETE` request to `/crm/v3/objects/contacts/{contactId}`.
* **Batch Deletion:** See the [reference documentation](link-to-batch-delete-reference) for details on batch deletion.


## Secondary Emails

Secondary emails are handled via the `hs_additional_emails` property (semicolon-separated).  When retrieving contacts, include `email` and `hs_additional_emails` in the `properties` parameter.  For V1 API usage, see the [V1 secondary email reference guide](link-to-v1-secondary-email-guide).


## Limits

Batch operations are limited to 100 records per request.  See the documentation for limits on contacts and form submissions.  (link to contacts and form submission limits)


**Remember to replace placeholder values (IDs, emails, etc.) with your actual data.**  Replace the bracketed placeholders like `[link-to-understanding-crm-guide]` with the actual links to the relevant HubSpot documentation.
