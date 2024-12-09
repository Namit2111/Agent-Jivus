# HubSpot CRM API: Contacts

This document details the HubSpot CRM API endpoints for managing contacts.  Contacts in HubSpot store information about individuals interacting with your business.  These endpoints enable creating, managing, and syncing contact data between HubSpot and other systems.

For a broader understanding of objects, records, properties, and associations within the HubSpot CRM API, refer to the [Understanding the CRM](link-to-understanding-crm-guide) guide.  For general CRM database management, see [Managing your CRM database](link-to-crm-database-management).


## Create Contacts

Use a `POST` request to `/crm/v3/objects/contacts` to create new contacts.  Include contact data within a `properties` object. Optionally, include an `associations` object to link the new contact to existing records (companies, deals) or activities (meetings, notes).

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

**Note on `lifecyclestage`:** If included, values must use the lifecycle stage's *internal name*. Default stages use text values (e.g., `"subscriber"`, `"marketingqualifiedlead"`) which don't change with label edits. Custom stages use numeric values, found in your lifecycle stage settings or via the lifecycle stage property API.


## Properties

Contact details are stored in properties.  HubSpot provides default contact properties, but you can also create custom ones.  To view available properties, use a `GET` request to `/crm/v3/properties/contacts`.  Learn more about the [properties API](link-to-properties-api).


## Associations

When creating contacts, associate them with existing records or activities using the `associations` object.

**Example Request Body (JSON):**

```json
{
  "properties": {
    "email": "example@hubspot.com",
    "firstname": "Jane",
    "lastname": "Doe",
    // ... other properties
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

* **`to.id`:**  The unique ID of the record or activity.
* **`types`:** The association type.  Use the [list of default association type IDs](link-to-default-association-types) or retrieve custom types via the [associations API](link-to-associations-api).


## Retrieve Contacts

Contacts can be retrieved individually or in batches.

**Individual Contact:**

* By ID: `GET /crm/v3/objects/contacts/{contactId}`
* By Email: `GET /crm/v3/objects/contacts/{email}?idProperty=email`

**All Contacts:** `GET /crm/v3/objects/contacts`

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of current and historical properties.
* `associations`: Comma-separated list of objects to retrieve associated IDs for.

**Batch Retrieval:** `POST /crm/v3/objects/contacts/batch/read`

This endpoint doesn't retrieve associations.  Use the [associations API](link-to-associations-api) for batch association reads.  The `idProperty` parameter specifies whether IDs refer to record IDs (`hs_object_id`), email, or a custom unique identifier property.

**Example Request Body (Batch, by Record ID):**

```json
{
  "properties": ["email", "lifecyclestage", "jobtitle"],
  "inputs": [ { "id": "1234567" }, { "id": "987456" } ]
}
```

**Example Request Body (Batch, by Email):**

```json
{
  "properties": ["email", "lifecyclestage", "jobtitle"],
  "idProperty": "email",
  "inputs": [ { "id": "lgilmore@thedragonfly.com" }, { "id": "sstjames@thedragonfly.com" } ]
}
```


## Update Contacts

Contacts can be updated individually or in batches.

**Individual Update:**

* By ID: `PATCH /crm/v3/objects/contacts/{contactId}`
* By Email: `PATCH /crm/v3/objects/contacts/{email}?idProperty=email`

**Batch Update:** `POST /crm/v3/objects/contacts/batch/update`  (limited to 100 records)

**Note on `lifecyclestage` updates:**  Only forward stage transitions are allowed. To move backward, clear the existing lifecycle stage value manually or via a workflow/integration.


## Upsert Contacts

Batch create and update contacts simultaneously using `POST /crm/v3/objects/contacts/batch/upsert`.  Use `idProperty` to specify if `id` values are emails or custom unique identifiers.


## Associate/Remove Associations

* **Associate:** `PUT /crm/v3/objects/contacts/{contactId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`
* **Remove:** `DELETE /crm/v3/objects/contacts/{contactID}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


## Pin an Activity

Pin an activity to a contact using the `hs_pinned_engagement_id` property (requires activity ID from [engagements APIs](link-to-engagements-api)).  Only one activity can be pinned per contact.


## Delete Contacts

Delete contacts individually or in batches (moves to recycling bin; can be restored).

* **Individual Delete:** `DELETE /crm/v3/objects/contacts/{contactId}`
* **Batch Delete:**  See [reference documentation](link-to-batch-delete-docs)


## Secondary Emails

Manage secondary emails using the `hs_additional_emails` property (semicolon-separated).  For V1 API, see [this reference guide](link-to-v1-secondary-email-guide).


## Limits

Batch operations are limited to 100 records.  See further limits on [contacts and form submissions](link-to-limits-docs).


**(Remember to replace placeholder links like `link-to-understanding-crm-guide` with actual links to the relevant HubSpot documentation.)**
