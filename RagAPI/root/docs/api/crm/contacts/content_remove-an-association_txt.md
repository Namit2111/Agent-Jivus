# HubSpot CRM API Contacts Documentation

This document details the HubSpot CRM API endpoints for managing contacts.  Contacts in HubSpot store information about individuals interacting with your business.  These endpoints allow for creating, managing, and syncing contact data between HubSpot and other systems.

## Understanding the CRM

For a comprehensive understanding of objects, records, properties, and associations within the HubSpot CRM API, refer to the [Understanding the CRM guide](link-to-understanding-crm-guide).  For general information on managing your CRM database, see [how to manage your CRM database](link-to-crm-database-management).


## Create Contacts

To create new contacts, send a `POST` request to `/crm/v3/objects/contacts`.

Include contact data within a `properties` object.  An optional `associations` object can link the new contact to existing records (companies, deals) or activities (meetings, notes).

**Required Properties:** At least one of the following properties must be included: `email`, `firstname`, or `lastname`.  Using `email` is strongly recommended as it's the primary unique identifier to prevent duplicates.

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

**Note on `lifecyclestage`:** If included, values must use the lifecycle stage's internal name (not the label).  Default stage internal names are text values; custom stage internal names are numeric.  Find the internal ID in your lifecycle stage settings or via the API.


## Properties

Contact details are stored in properties.  HubSpot provides default contact properties, and you can [create custom contact properties](link-to-custom-property-creation).  To view available properties, use a `GET` request to `/crm/v3/properties/contacts`.  Learn more about the [properties API](link-to-properties-api).


## Associations

When creating a contact, associate it with existing records or activities using the `associations` object.

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
| `to`            | Record or activity ID to associate with the contact.                                                    |
| `types`         | Association type. Include `associationCategory` and `associationTypeId`.  See [default association type IDs](link-to-association-types) or use the [associations API](link-to-associations-api) for custom types. |


## Retrieve Contacts

Contacts can be retrieved individually or in batches.

**Individual Contact:**

Use a `GET` request to `/crm/v3/objects/contacts/{contactId}` (by ID) or `/crm/v3/objects/contacts/{email}?idProperty=email` (by email).

**All Contacts:**

Use a `GET` request to `/crm/v3/objects/contacts`.

**Query Parameters:**

| Parameter           | Description                                                                                             |
|-----------------------|---------------------------------------------------------------------------------------------------------|
| `properties`         | Comma-separated list of properties to return.  Missing properties are omitted from the response.       |
| `propertiesWithHistory` | Comma-separated list of current and historical properties to return. Missing properties are omitted. |
| `associations`       | Comma-separated list of objects to retrieve associated IDs for. Missing associations are omitted.      |

**Batch Retrieval:**

Use a `POST` request to `/crm/v3/objects/contacts/batch/read`.  This endpoint *cannot* retrieve associations. Use the [associations API](link-to-associations-api) for batch association reads.

The optional `idProperty` parameter allows retrieval by email or a custom unique identifier property (default is `hs_object_id`).  Examples are provided in the original text.


## Update Contacts

Contacts can be updated individually or in batches.

**Individual Update (by ID):**

Use a `PATCH` request to `/crm/v3/objects/contacts/{contactId}`.

**Individual Update (by Email):**

Use a `PATCH` request to `/crm/v3/objects/contacts/{email}?idProperty=email`.

**Batch Update:**

Use a `POST` request to `/crm/v3/objects/contacts/batch/update`.  Examples are provided in the original text.

**Note on `lifecyclestage` updates:**  Updates can only move the stage *forward* in the stage order. To move backward, clear the existing value manually or via a workflow/integration.


## Upsert Contacts

Batch create and update contacts simultaneously using a `POST` request to `/crm/v3/objects/contacts/batch/upsert`.  Use `idProperty` to specify whether you're using `email` or a custom unique identifier. Examples are provided in the original text.


## Associate Existing Contacts

Associate a contact with other CRM records or activities using a `PUT` request to `/crm/v3/objects/contacts/{contactId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`.  Obtain `associationTypeId` from the [default values list](link-to-association-types) or via a `GET` request to `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`. Learn more about the [associations API](link-to-associations-api).


## Remove an Association

Remove an association using a `DELETE` request to `/crm/v3/objects/contacts/{contactID}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`.


## Pin an Activity

Pin an activity to a contact record using the `hs_pinned_engagement_id` property (containing the activity ID from the [engagements APIs](link-to-engagements-api)). Only one activity can be pinned per record.  The activity must already be associated with the contact. Examples are provided in the original text showing how to pin during contact creation or update.


## Delete Contacts

Delete contacts individually or in batches (moves them to the recycling bin; they can be restored).

**Individual Delete:** Use a `DELETE` request to `/crm/v3/objects/contacts/{contactId}`.

Batch deletion is discussed in the [reference documentation](link-to-batch-delete-reference).


## Secondary Emails

Secondary emails are handled using the `hs_additional_emails` property.  Multiple emails are separated by semicolons.  If using V1 APIs, see [this reference guide](link-to-v1-secondary-email-guide).


## Limits

Batch operations are limited to 100 records per request.  See [contacts and form submissions limits](link-to-limits) for other limitations.


**(Remember to replace the bracketed placeholders like `link-to-understanding-crm-guide` with actual links.)**
