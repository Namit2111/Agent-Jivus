# HubSpot CRM API: Contacts

This document details the HubSpot CRM API endpoints for managing contacts.  Contacts in HubSpot store information about individuals interacting with your business. These endpoints enable creating, managing, and syncing contact data between HubSpot and external systems.

For a broader understanding of objects, records, properties, and associations within the HubSpot API, refer to the [Understanding the CRM](<link_to_understanding_crm_guide>) guide.  For general CRM database management, see [managing your CRM database](<link_to_crm_database_management>).


## Create Contacts

Use a `POST` request to `/crm/v3/objects/contacts` to create new contacts.  The request body should include a `properties` object containing contact data. An optional `associations` object can link the new contact to existing records (e.g., companies, deals) or activities (e.g., meetings, notes).

**Required Properties:** At least one of `email`, `firstname`, or `lastname` is required.  Using `email` is strongly recommended, as it's the primary unique identifier to prevent duplicates.

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

**`lifecyclestage` Note:** If included, use the internal name of the lifecycle stage.  Default stages use text values (e.g., `"subscriber"`, `"marketingqualifiedlead"`), while custom stages use numeric values. Find the internal ID in your lifecycle stage settings or via the API.


## Properties

Contact details are stored in properties. HubSpot offers default contact properties, and you can create custom ones.  To view all available properties, use a `GET` request to `/crm/v3/properties/contacts`. Learn more about the [properties API](<link_to_properties_api>).


## Associations

When creating a contact, associate it with existing records or activities using the `associations` object.

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

**`associations` Parameters:**

* **`to.id`:** The ID of the record or activity to associate.
* **`types`:**  An array of association types.  `associationCategory` and `associationTypeId` are required. Default IDs are listed [here](<link_to_default_association_types>), or retrieve custom type values via the [associations API](<link_to_associations_api>).


## Retrieve Contacts

Contacts can be retrieved individually or in batches.

**Individual Contact:** Use a `GET` request to `/crm/v3/objects/contacts/{contactId}` (by ID) or `/crm/v3/objects/contacts/{email}?idProperty=email` (by email).

**All Contacts:** Use a `GET` request to `/crm/v3/objects/contacts`.

**Batch Retrieval:** Use a `POST` request to `/crm/v3/objects/contacts/batch/read`.  This endpoint does *not* retrieve associations. Use the [associations API](<link_to_associations_api>) for batch association retrieval.  The `idProperty` parameter is required if using email or a custom unique identifier; otherwise, it defaults to `hs_object_id`.

**Query Parameters (for individual and all contacts):**

* **`properties`:** Comma-separated list of properties to return.
* **`propertiesWithHistory`:** Comma-separated list of current and historical properties to return.
* **`associations`:** Comma-separated list of objects to retrieve associated IDs for.


**Example Batch Request Body (by record ID):**

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

**Individual Update (by ID):** Use a `PATCH` request to `/crm/v3/objects/contacts/{contactId}`.

**Individual Update (by email):** Use a `PATCH` request to `/crm/v3/objects/contacts/{email}?idProperty=email`.

**Batch Update:** Use a `POST` request to `/crm/v3/objects/contacts/batch/update`.

**`lifecyclestage` Update Note:**  Only forward changes are allowed. To move backward, clear the existing value manually or via a workflow/integration.


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

Batch create and update contacts simultaneously using a `POST` request to `/crm/v3/objects/contacts/batch/upsert`.  Use `idProperty` (e.g., `"email"` or a custom unique identifier) to specify the ID field.


**Example Upsert Request Body (using email):**

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

Use a `PUT` request to `/crm/v3/objects/contacts/{contactId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}` to associate a contact with other CRM records or activities.  Retrieve `associationTypeId` values from the list of defaults or via a `GET` request to `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`.  See the [associations API](<link_to_associations_api>) for more details.


## Remove an Association

Use a `DELETE` request to `/crm/v3/objects/contacts/{contactID}/associations/{toObjectType}/{toObjectId}/{associationTypeId}` to remove an association.


## Pin an Activity

Pin an activity to a contact record by including the `hs_pinned_engagement_id` property (containing the activity's ID) in your request.  You can pin one activity per contact; it must already be associated.  Use the [engagements APIs](<link_to_engagements_api>) to retrieve activity IDs.


**Example Request Body (pinning an activity):**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```


## Delete Contacts

Delete contacts individually (using a `DELETE` request to `/crm/v3/objects/contacts/{contactId}`) or in batches (see the [reference documentation](<link_to_batch_delete_docs>)).  Deleted contacts are moved to the recycling bin and can be restored.


## Secondary Emails

Secondary emails are handled via the `hs_additional_emails` property.  Multiple emails are separated by semicolons.


## Limits

Batch operations are limited to 100 records per request.  See the documentation for limits on contacts and form submissions.  [Link to contact and form submission limits](<link_to_limits_docs>)


**(Remember to replace `<link_to...>` placeholders with actual links to the relevant HubSpot documentation.)**
