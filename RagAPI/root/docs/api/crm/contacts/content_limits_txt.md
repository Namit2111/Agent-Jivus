# HubSpot CRM API: Contacts

This document details the HubSpot CRM API endpoints for managing contacts.  Contacts in HubSpot store information about individuals interacting with your business.  These endpoints allow you to create, manage, and sync contact data between HubSpot and other systems.

For a broader understanding of objects, records, properties, and associations within the HubSpot API, refer to the [Understanding the CRM](<link_to_understanding_crm_guide>) guide.  For general CRM database management, see [how to manage your CRM database](<link_to_crm_database_management>).


## Create Contacts

Use a `POST` request to `/crm/v3/objects/contacts` to create new contacts.  Include contact data within a `properties` object. You can also add an `associations` object to link the new contact to existing records (companies, deals) or activities (meetings, notes).

**Required Properties:** At least one of `email`, `firstname`, or `lastname` is required.  `email` is strongly recommended as it's the primary unique identifier, preventing duplicates.

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

**`lifecyclestage` Note:**  If included, use the internal name (not the label). Default stages use text values (e.g., `subscriber`, `marketingqualifiedlead`), while custom stages use numeric values.  Find the internal ID in your lifecycle stage settings or via the lifecycle stage property API.


## Properties

Contact details are stored in properties. HubSpot provides default properties, and you can also create custom ones.  Retrieve a list of available properties via a `GET` request to `/crm/v3/properties/contacts`.  Learn more about the [properties API](<link_to_properties_api>).


## Associations

Associate new contacts with existing records or activities using the `associations` object in your `POST` request to `/crm/v3/objects/contacts`.

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

* **`to.id`:** The ID of the record or activity.
* **`types`:** The association type.  Use the provided list of default `associationTypeId`s or retrieve custom types via the [associations API](<link_to_associations_api>).


## Retrieve Contacts

Retrieve contacts individually or in batches.

**Individual Contact:**

* Use a `GET` request to `/crm/v3/objects/contacts/{contactId}` (by ID) or `/crm/v3/objects/contacts/{email}?idProperty=email` (by email).

**All Contacts:**

* Use a `GET` request to `/crm/v3/objects/contacts`.

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of current and historical properties.
* `associations`: Comma-separated list of associated objects to retrieve IDs for.


**Batch Retrieval (`POST` to `/crm/v3/objects/contacts/batch/read`):**

This endpoint cannot retrieve associations.  Use the [associations API](<link_to_associations_api>) for batch association reads.

* `idProperty`:  Use `email` or a custom unique identifier property.  Required if not using record IDs (`hs_object_id`).
* Example request bodies for retrieving by record ID (with current and historical values) and by email/custom property are included in the original text.


## Update Contacts

Update contacts individually or in batches.

**Individual Contact:**

* Use a `PATCH` request to `/crm/v3/objects/contacts/{contactId}` (by ID) or `/crm/v3/objects/contacts/{email}?idProperty=email` (by email).

**Batch Update (`POST` to `/crm/v3/objects/contacts/batch/update`):**

Update multiple contacts using their record IDs.  Example request body is included in the original text.

**`lifecyclestage` Update Note:** You can only move forward in the lifecycle stage order. To move backward, first clear the existing value manually or via a workflow/integration.


## Upsert Contacts

Batch create and update contacts using `POST` to `/crm/v3/objects/contacts/batch/upsert`. Use `email` or a custom unique identifier property.

* `idProperty`: Specify whether using `email` or a custom property.
* Example request body using email is included in the original text.


## Associate/Remove Associations

* **Associate:** Use a `PUT` request to `/crm/v3/objects/contacts/{contactId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`.
* **Remove:** Use a `DELETE` request to `/crm/v3/objects/contacts/{contactID}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`.


## Pin an Activity

Pin an activity to a contact record using the `hs_pinned_engagement_id` property (containing the activity ID from the engagements APIs).  Only one activity can be pinned per contact.  Example request bodies for updating an existing contact and creating a contact with a pinned activity are in the original text.


## Delete Contacts

Delete contacts individually (using a `DELETE` request to `/crm/v3/objects/contacts/{contactId}`) or in batches (see reference documentation for batch deletion).  Deleted contacts are moved to the recycling bin and can be restored.


## Secondary Emails

Manage secondary emails using the `hs_additional_emails` property.  Multiple emails are separated by semicolons.


## Limits

Batch operations are limited to 100 records per request.  There are also limits on contacts and form submissions.
