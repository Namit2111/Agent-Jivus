# HubSpot CRM API: Contacts

This document details the HubSpot CRM API endpoints for managing contacts.  Contacts in HubSpot store information about individuals interacting with your business.  These endpoints allow for creating, managing, and syncing contact data.

## Understanding the CRM (Prerequisites)

Before using these APIs, familiarize yourself with HubSpot's [CRM object model](link_to_hubspot_crm_object_guide), [records](link_to_hubspot_records_guide), [properties](link_to_hubspot_properties_guide), and [associations](link_to_hubspot_associations_guide).  Understanding how HubSpot manages its CRM database is crucial.  [Link to HubSpot CRM database management guide](link_to_hubspot_crm_db_management).

## API Endpoints

All endpoints are under the `/crm/v3/objects/contacts` base path unless otherwise specified.  Requests require proper authentication (API key).

### 1. Create Contacts

**Method:** `POST /crm/v3/objects/contacts`

**Request Body:** JSON

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

**Properties:**  Contact details are stored in properties.  Use default HubSpot properties or create custom ones. At least one of `email`, `firstname`, or `lastname` is required.  `email` is strongly recommended as the primary unique identifier to prevent duplicates.  Get a list of all available properties with a `GET /crm/v3/properties/contacts` request.  See [Properties API documentation](link_to_hubspot_properties_api).

**Associations:** Optionally associate the new contact with existing records (companies, deals) or activities (meetings, notes) using the `associations` object.

**Example Request Body with Associations:**

```json
{
  "properties": {
    "email": "example@hubspot.com",
    "firstname": "Jane",
    "lastname": "Doe"
  },
  "associations": [
    {
      "to": { "id": 123456 }, // Company ID
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 279 }] // Association type
    },
    {
      "to": { "id": 556677 }, // Deal ID
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 197 }] // Association type
    }
  ]
}
```

**`lifecyclestage` Note:**  Use the *internal name* (not the label) for lifecycle stages. Default stages use text values; custom stages use numeric IDs. Find IDs in lifecycle stage settings or via the API.


### 2. Retrieve Contacts

**Individual Contact:**

**Method:** `GET /crm/v3/objects/contacts/{contactId}` or `GET /crm/v3/objects/contacts/{email}?idProperty=email`

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of current and historical properties.
* `associations`: Comma-separated list of associated objects to retrieve.


**Batch Contacts:**

**Method:** `POST /crm/v3/objects/contacts/batch/read`

**Request Body:** JSON

**Example Request Body (by record ID):**

```json
{
  "properties": ["email", "lifecyclestage"],
  "inputs": [
    { "id": "1234567" },
    { "id": "987456" }
  ]
}
```

**Example Request Body (by email):**

```json
{
  "properties": ["email", "lifecyclestage"],
  "idProperty": "email",
  "inputs": [
    { "id": "lgilmore@thedragonfly.com" },
    { "id": "sstjames@thedragonfly.com" }
  ]
}
```

**`idProperty` Parameter:** Use `email` or a custom unique identifier property.  Default is `hs_object_id` (record ID).


### 3. Update Contacts

**Individual Contact:**

**Method:** `PATCH /crm/v3/objects/contacts/{contactId}` (by ID) or `PATCH /crm/v3/objects/contacts/{email}?idProperty=email` (by email)

**Request Body:** JSON

**Example Request Body:**

```json
{
  "properties": {
    "favorite_food": "burger",
    "jobtitle": "Manager",
    "lifecyclestage": "Customer"
  }
}
```

**`lifecyclestage` Note:** Can only be updated *forward* in the stage order. To move backward, clear the existing value first (manually, via workflow, or integration).


**Batch Contacts:**

**Method:** `POST /crm/v3/objects/contacts/batch/update`

**Request Body:** JSON

**Example Request Body:**

```json
{
  "inputs": [
    { "id": "123456789", "properties": { "favorite_food": "burger" } },
    { "id": "56789123", "properties": { "favorite_food": "Donut" } }
  ]
}
```


### 4. Upsert Contacts

**Method:** `POST /crm/v3/objects/contacts/batch/upsert`

**Request Body:** JSON

**Example Request Body (using email):**

```json
{
  "inputs": [
    {
      "properties": { "phone": "5555555555" },
      "id": "test@test.com",
      "idProperty": "email"
    },
    {
      "properties": { "phone": "7777777777" },
      "id": "example@hubspot.com",
      "idProperty": "email"
    }
  ]
}
```

Uses `email` or a custom unique identifier property (`idProperty`).  Creates new contacts if they don't exist; updates existing ones.


### 5. Associate Contacts

**Method:** `PUT /crm/v3/objects/contacts/{contactId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

Requires `associationTypeId` (find in default list or via `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`).


### 6. Remove Association

**Method:** `DELETE /crm/v3/objects/contacts/{contactID}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


### 7. Pin Activity

**Method:** `PATCH /crm/v3/objects/contacts/{contactId}` (update existing contact) or `POST /crm/v3/objects/contacts` (create new contact and pin)


Use `hs_pinned_engagement_id` property with the activity ID.  Only one activity can be pinned per contact.


### 8. Delete Contacts

**Individual Contact:**

**Method:** `DELETE /crm/v3/objects/contacts/{contactId}`

Moves the contact to the recycling bin; can be restored.


**Batch Deletion:** See reference documentation (link needed)


### 9. Secondary Emails

Use `hs_additional_emails` property to view or add secondary emails.  Multiple emails are separated by semicolons.


### 10. Limits

Batch operations are limited to 100 records per request.  See documentation for other limits on contacts and form submissions (link needed).


## Response Codes

Standard HTTP response codes are used to indicate success or failure (e.g., 200 OK, 400 Bad Request, 404 Not Found).  Error responses will contain details.


This documentation provides a comprehensive overview.  Consult the official HubSpot API documentation for the most up-to-date information and detailed specifications.  Remember to replace placeholder values (IDs, emails, etc.) with your actual data.
