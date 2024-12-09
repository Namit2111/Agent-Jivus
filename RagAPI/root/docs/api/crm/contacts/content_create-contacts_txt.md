# HubSpot CRM API: Contacts

This document describes the HubSpot CRM API endpoints for managing contacts.  Contacts in HubSpot store information about individuals interacting with your business. These endpoints allow you to create, manage, and sync contact data between HubSpot and other systems.

For a broader understanding of objects, records, properties, and associations within the HubSpot API, refer to the [Understanding the CRM](LINK_TO_UNDERSTANDING_CRM_GUIDE) guide. For general CRM database management, see [Managing your CRM database](LINK_TO_CRM_DATABASE_MANAGEMENT).


## Create Contacts

Use a `POST` request to `/crm/v3/objects/contacts` to create new contacts.  The request body should include a `properties` object containing contact data. An optional `associations` object can associate the new contact with existing records (e.g., companies, deals) or activities (e.g., meetings, notes).

**Required Properties:** At least one of `email`, `firstname`, or `lastname` is required.  Using `email` is strongly recommended as it's the primary unique identifier to prevent duplicates.

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

**`lifecyclestage` Note:** If included, use the internal name (not the label).  Default stages use text values (e.g., `subscriber`, `marketingqualifiedlead`), while custom stages use numeric values. Find the internal ID in your lifecycle stage settings or via the lifecycle stage property API.


## Properties

Contact details are stored in properties.  HubSpot provides default properties, and you can create custom ones.  To view all available properties, use a `GET` request to `/crm/v3/properties/contacts`.  Learn more about the [properties API](LINK_TO_PROPERTIES_API).


## Associations

Associate contacts with existing records or activities using the `associations` object in your `POST` request when creating a contact.

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
* **`types`:**  The association type. Use the provided list of default `associationTypeId` values or retrieve custom types via the [associations API](LINK_TO_ASSOCIATIONS_API).


## Retrieve Contacts

Contacts can be retrieved individually or in batches.

* **Individual Contact (by ID):** `GET /crm/v3/objects/contacts/{contactId}`
* **Individual Contact (by Email):** `GET /crm/v3/objects/contacts/{email}?idProperty=email`
* **All Contacts:** `GET /crm/v3/objects/contacts`
* **Batch Read:** `POST /crm/v3/objects/contacts/batch/read` (cannot retrieve associations).


**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of current and historical properties.
* `associations`: Comma-separated list of associated objects to retrieve.

**Batch Read (using `idProperty` for email or custom unique identifiers):**


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

Contacts can be updated individually or in batches.

* **Individual Update (by ID):** `PATCH /crm/v3/objects/contacts/{contactId}`
* **Individual Update (by Email):** `PATCH /crm/v3/objects/contacts/{email}?idProperty=email`
* **Batch Update:** `POST /crm/v3/objects/contacts/batch/update` (uses record IDs).

**`lifecyclestage` Update Note:**  You can only update `lifecyclestage` forward in the stage order. To move backward, clear the existing value manually or via a workflow/integration.


## Upsert Contacts

Batch create and update contacts simultaneously using `POST /crm/v3/objects/contacts/batch/upsert`.  Use `idProperty` to specify whether you're using `email` or a custom unique identifier.


## Associate/Remove Associations

* **Associate:** `PUT /crm/v3/objects/contacts/{contactId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`
* **Remove:** `DELETE /crm/v3/objects/contacts/{contactID}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

Retrieve `associationTypeId` from the default list or via a `GET` request to `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`.


## Pin an Activity

Pin an activity to a contact record using the `hs_pinned_engagement_id` property (containing the activity ID).  You can only pin one activity per record, and it must already be associated with the contact.


## Delete Contacts

Delete contacts individually (`DELETE /crm/v3/objects/contacts/{contactId}`) or in batches (see reference documentation for batch delete).  Deleted contacts are moved to the recycling bin and can be restored.


## Secondary Emails

Manage secondary emails using the `hs_additional_emails` property (semicolon-separated).  These are unique identifiers.  For V1 APIs, see [this reference guide](LINK_TO_V1_SECONDARY_EMAIL_GUIDE).


## Limits

Batch operations are limited to 100 records per request.  See documentation for limits on contacts and form submissions.

**(Remember to replace placeholder links like `LINK_TO_UNDERSTANDING_CRM_GUIDE` with actual links.)**
