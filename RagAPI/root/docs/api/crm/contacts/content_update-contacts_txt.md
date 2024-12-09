# HubSpot CRM API: Contacts

This document details the HubSpot CRM API endpoints for managing contacts.  Contacts in HubSpot store information about individuals interacting with your business.  These endpoints allow creation, management, and synchronization of contact data between HubSpot and external systems.

## Understanding the CRM

For a comprehensive understanding of objects, records, properties, and associations within the HubSpot CRM API, refer to the [Understanding the CRM](<link_to_understanding_crm_guide>) guide.  For general CRM database management, see [how to manage your CRM database](<link_to_crm_database_management>).


## Create Contacts

Use a `POST` request to `/crm/v3/objects/contacts` to create new contacts.  The request body should include a `properties` object containing contact data.  An optional `associations` object can associate the new contact with existing records (companies, deals) or activities (meetings, notes).

**Required Properties:** At least one of `email`, `firstname`, or `lastname` is required.  `email` is strongly recommended as it's the primary unique identifier, preventing duplicates.

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

**Note on `lifecyclestage`:**  If included, values must use the lifecycle stage's internal name (e.g., `"marketingqualifiedlead"`).  Internal names for default stages are text values; custom stage names are numeric.  Find internal IDs in lifecycle stage settings or via the API.


## Properties

Contact details are stored in properties.  HubSpot provides default properties, and you can create custom ones.  To view all available properties, use a `GET` request to `/crm/v3/properties/contacts`.  Learn more about the [properties API](<link_to_properties_api>).


## Associations

Associate new contacts with existing records or activities using the `associations` object in the `POST` request to `/crm/v3/objects/contacts`.

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

* **`to.id`:** The ID of the record or activity.
* **`types`:** The association type.  Default IDs are listed [here](<link_to_default_association_types>), or retrieve custom types via the [associations API](<link_to_associations_api>).


## Retrieve Contacts

Contacts can be retrieved individually or in batches.

**Individual Contact:**

* By ID: `GET /crm/v3/objects/contacts/{contactId}`
* By Email: `GET /crm/v3/objects/contacts/{email}?idProperty=email`

**All Contacts:** `GET /crm/v3/objects/contacts`

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of current and historical properties.
* `associations`: Comma-separated list of associated objects to retrieve.


**Batch Retrieval:** `POST /crm/v3/objects/contacts/batch/read`

This endpoint allows retrieval by ID, email, or custom unique identifier property using the `idProperty` parameter.  Associations cannot be retrieved via this endpoint.  See the [associations API](<link_to_associations_api>) for batch association reads.

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

Contacts can be updated individually or in batches.

**Individual Update:**

* By ID: `PATCH /crm/v3/objects/contacts/{contactId}`
* By Email: `PATCH /crm/v3/objects/contacts/{email}?idProperty=email`

**Batch Update:** `POST /crm/v3/objects/contacts/batch/update`  (limited to 100 records)

**Note on `lifecyclestage` updates:**  Lifecycle stage updates can only move *forward* in the stage order. To move backward, clear the existing value manually, via workflow, or an integration.


## Upsert Contacts

Batch create and update contacts using: `POST /crm/v3/objects/contacts/batch/upsert`

Uses `email` or a custom unique identifier property (`idProperty`). Existing contacts are updated; new ones are created.


## Associate Existing Contacts

Associate a contact with records or activities: `PUT /crm/v3/objects/contacts/{contactId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


## Remove an Association

Remove an association: `DELETE /crm/v3/objects/contacts/{contactID}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


## Pin an Activity

Pin an activity to a contact record using the `hs_pinned_engagement_id` property.  Only one activity can be pinned per record.  The activity must already be associated with the contact.


## Delete Contacts

Delete contacts (moves to recycling bin): `DELETE /crm/v3/objects/contacts/{contactId}`.  See reference documentation for batch deletion.


## Secondary Emails

Manage secondary emails using the `hs_additional_emails` property.  Secondary emails are unique identifiers.


## Limits

Batch operations are limited to 100 records per request.  See documentation for other limits on contacts and form submissions.

**(Remember to replace placeholder links with actual links to HubSpot's documentation.)**
