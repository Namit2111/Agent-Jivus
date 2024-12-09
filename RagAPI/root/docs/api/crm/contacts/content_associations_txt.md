# HubSpot CRM API: Contacts

This document details the HubSpot CRM API endpoints for managing contacts.  Contacts in HubSpot store information about individuals who interact with your business.  These endpoints allow you to create, manage, and synchronize contact data between HubSpot and other systems.

For a broader understanding of objects, records, properties, and associations within the HubSpot CRM API, refer to the [Understanding the CRM guide](link_to_understanding_crm_guide) and [managing your CRM database](link_to_managing_crm_database).  (Replace `link_to_understanding_crm_guide` and `link_to_managing_crm_database` with actual links if available.)


## Create Contacts

To create new contacts, send a `POST` request to `/crm/v3/objects/contacts`.

Include contact data within a `properties` object.  You can also add an `associations` object to link the new contact with existing records (e.g., companies, deals) or activities (e.g., meetings, notes).

**Required Properties:** At least one of the following properties (`email`, `firstname`, or `lastname`) must be included.  Using `email` is strongly recommended, as it's the primary unique identifier for preventing duplicates.

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

**`lifecyclestage` Note:** If included, values must use the internal name (not the label).  Default stage internal names are text values, while custom stage internal names are numeric.  Find the internal ID in your lifecycle stage settings or by retrieving the lifecycle stage property via the API.


## Properties

Contact details are stored in properties.  HubSpot provides default contact properties, and you can create custom ones.  To view all available properties, make a `GET` request to `/crm/v3/properties/contacts`.  Learn more about the [properties API](link_to_properties_api). (Replace `link_to_properties_api` with actual link if available)


## Associations

When creating a contact, associate it with existing records or activities using the `associations` object.

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

| Parameter       | Description                                                                                   |
|-----------------|-----------------------------------------------------------------------------------------------|
| `to`            | The record or activity ID to associate.                                                       |
| `types`         | The association type.  Include `associationCategory` and `associationTypeId`.  See [this list](link_to_association_types) or use the associations API for custom types. (Replace `link_to_association_types` with actual link if available) |


## Retrieve Contacts

Contacts can be retrieved individually or in batches.

* **Individual Contact:** `GET /crm/v3/objects/contacts/{contactId}` or `GET /crm/v3/objects/contacts/{email}?idProperty=email`
* **All Contacts:** `GET /crm/v3/objects/contacts`
* **Batch Read:** `POST /crm/v3/objects/contacts/batch/read` (cannot retrieve associations)

**Query Parameters:**

| Parameter           | Description                                                                                                                               |
|----------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| `properties`         | Comma-separated list of properties to return.  Missing properties are omitted from the response.                                             |
| `propertiesWithHistory` | Comma-separated list of current and historical properties to return. Missing properties are omitted from the response.                      |
| `associations`       | Comma-separated list of associated objects to retrieve IDs for.  Non-existent associations are omitted. Learn more about the [associations API](link_to_associations_api). (Replace `link_to_associations_api` with actual link if available) |
| `idProperty`         |  (For batch read)  Specifies whether `id` values refer to record ID (`hs_object_id`), `email`, or a custom unique identifier property. Required when using `email` or custom unique property. |

**Batch Read Examples:** (Record ID, Email, Custom Property) -  Examples showing both current and historical properties are provided in the original text.


## Update Contacts

Contacts can be updated individually or in batches.

* **Individual Update (by ID):** `PATCH /crm/v3/objects/contacts/{contactId}`
* **Individual Update (by Email):** `PATCH /crm/v3/objects/contacts/{email}?idProperty=email`
* **Batch Update:** `POST /crm/v3/objects/contacts/batch/update` (uses record IDs)


**`lifecyclestage` Update Note:**  Can only be updated *forward* in the stage order. To move backward, clear the existing value manually, via workflow, or integration.


## Upsert Contacts

Batch create and update contacts simultaneously using: `POST /crm/v3/objects/contacts/batch/upsert`.  Uses `email` or a custom unique identifier property.


## Associate/Remove Associations

* **Associate:** `PUT /crm/v3/objects/contacts/{contactId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`
* **Remove:** `DELETE /crm/v3/objects/contacts/{contactID}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

Get `associationTypeId` values from [this list](link_to_association_types) of defaults or via `GET /crm/v4/associations/{fromObjectType}/{toObjectType}/labels` (Replace `link_to_association_types` with actual link if available).


## Pin an Activity

Pin an activity to a contact record using the `hs_pinned_engagement_id` property (activity ID from the engagements APIs).  Only one activity can be pinned per record.  The activity must already be associated with the contact.


## Delete Contacts

Contacts are moved to the recycling bin.  They can be restored later.

* **Individual Delete:** `DELETE /crm/v3/objects/contacts/{contactId}`
* **Batch Delete:** See reference documentation (link needed).


## Secondary Emails

Additional emails are stored in `hs_additional_emails`.  These are unique identifiers, like the primary email.


## Limits

Batch operations are limited to 100 records per request.  See documentation for limits on contacts and form submissions.
