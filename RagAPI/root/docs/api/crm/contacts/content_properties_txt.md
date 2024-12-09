# HubSpot CRM API: Contacts

This document details the HubSpot CRM API endpoints for managing contacts.  Contacts in HubSpot store information about individuals who interact with your business. These endpoints allow you to create, manage, and sync contact data between HubSpot and other systems.

For a broader understanding of HubSpot's objects, records, properties, and associations APIs, refer to the [Understanding the CRM guide](link_to_understanding_crm_guide).  For general information on managing your CRM database, see [how to manage your CRM database](link_to_crm_database_management).

## Create Contacts

Use a `POST` request to `/crm/v3/objects/contacts` to create new contacts.  Include contact data within a `properties` object. You can also add an `associations` object to associate the new contact with existing records (e.g., companies, deals) or activities (e.g., meetings, notes).

**Properties:**

Contact details are stored in properties.  HubSpot provides [default contact properties](link_to_default_properties), but you can also [create custom contact properties](link_to_custom_properties).  When creating a contact, include at least one of the following: `email`, `firstname`, or `lastname`.  Using `email` is recommended as it's the primary unique identifier, preventing duplicates.

To view all available properties, use a `GET` request to `/crm/v3/properties/contacts`. Learn more about the [properties API](link_to_properties_api).

**Note:** If including `lifecyclestage`, values must use the internal name (not the label). Default stage internal names are text values and don't change even if you edit the label (e.g., `subscriber` or `marketingqualifiedlead`). Custom stage internal names are numeric. Find a stage's internal ID in your lifecycle stage settings or by retrieving the lifecycle stage property via API.


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

**Associations:**

Associate the contact with existing records or activities using an `associations` object.

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

* **`to`:** The record/activity ID.
* **`types`:** Association type, including `associationCategory` and `associationTypeId`.  See [default association type IDs](link_to_association_type_ids) or use the [associations API](link_to_associations_api) for custom types.


## Retrieve Contacts

Retrieve contacts individually or in batches.

* **Individual Contact:** Use a `GET` request to `/crm/v3/objects/contacts/{contactId}` or `/crm/v3/objects/contacts/{email}?idProperty=email`.
* **All Contacts:** Use a `GET` request to `/crm/v3/objects/contacts`.
* **Batch Read (Specific Contacts):** Use a `POST` request to `/crm/v3/objects/contacts/batch/read`.  This endpoint cannot retrieve associations. Use the [associations API](link_to_associations_api) for batch association reads.  Use `idProperty` parameter for `email` or custom unique identifier property; otherwise, it defaults to record ID (`hs_object_id`).


**Query Parameters:**

* **`properties`:** Comma-separated list of properties to return.
* **`propertiesWithHistory`:** Comma-separated list of current and historical properties.
* **`associations`:** Comma-separated list of objects to retrieve associated IDs for.


**Example Request Body (Batch Read by Record ID):**

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

**Example Request Body (Batch Read by Email):**

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

Update contacts individually or in batches.

* **Individual Update (by ID):** Use a `PATCH` request to `/crm/v3/objects/contacts/{contactId}`.
* **Individual Update (by Email):** Use a `PATCH` request to `/crm/v3/objects/contacts/{email}?idProperty=email`.
* **Batch Update:** Use a `POST` request to `/crm/v3/objects/contacts/batch/update`.


**Note on `lifecyclestage` Update:** You can only update `lifecyclestage` forward in the stage order. To move backward, clear the existing value manually, via a workflow, or a data-syncing integration.

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

Batch create and update contacts using a `POST` request to `/crm/v3/objects/contacts/batch/upsert`. Use `idProperty` to specify `email` or a custom unique identifier.

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

## Associate/Remove Associations

* **Associate:** Use a `PUT` request to `/crm/v3/objects/contacts/{contactId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`. Get `associationTypeId` from [default values](link_to_association_type_ids) or `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`.
* **Remove:** Use a `DELETE` request to `/crm/v3/objects/contacts/{contactID}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`.

## Pin an Activity

Pin an activity to a contact record using the `hs_pinned_engagement_id` property (containing the activity ID from the [engagements APIs](link_to_engagements_api)).  Only one activity can be pinned per record.  The activity must already be associated with the contact.


**Example Request Body (PATCH):**

```json
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```

## Delete Contacts

Delete contacts individually (using a `DELETE` request to `/crm/v3/objects/contacts/{contactId}`) or in batches ([see reference documentation](link_to_batch_delete_docs)). Deleted contacts move to the recycling bin; you can restore them within HubSpot.


## Secondary Emails

Use `hs_additional_emails` property to manage secondary emails.  Multiple emails are separated by semicolons.  If using V1 APIs, see [this reference guide](link_to_v1_secondary_email_guide).

## Limits

Batch operations are limited to 100 records per request.  See limits for [contacts and form submissions](link_to_contact_form_submission_limits).


**(Remember to replace placeholder links like `link_to_understanding_crm_guide` with actual links.)**
