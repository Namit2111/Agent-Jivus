# HubSpot CRM APIs Documentation

This document provides an overview of the HubSpot CRM APIs, explaining how to interact with the CRM database using various API endpoints.

## I. Introduction

HubSpot's CRM (Customer Relationship Management) stores data about your business relationships and processes.  This data is organized into *objects* (e.g., Contacts, Companies, Deals), with individual instances called *records*. Each record contains *properties* (e.g., email address, company name) and can be *associated* with other records.  Interactions (e.g., emails, calls) are stored as *engagements* or *activities*.

## II. Key Concepts

* **Objects:** Represent types of relationships or processes (e.g., Contacts, Companies, Deals). Each object has a unique `objectTypeId`.
* **Records:** Individual instances of an object (e.g., a specific contact, a specific deal).  Each record has a unique `hs_object_id` (Record ID).
* **Properties:** Fields within a record that store data (e.g., email, company name).  Default and custom properties exist.
* **Associations:** Links between records of different objects (e.g., associating a contact with a company).
* **Pipelines:** Track records through stages in a process (e.g., deal stages in a sales pipeline).
* **Unique Identifiers:** Values that uniquely identify a record (e.g., `hs_object_id`, email for contacts, domain for companies).  Custom unique identifier properties can be created.


## III. API Endpoints and Usage

The CRM APIs use RESTful endpoints.  Most endpoints include `{objectTypeId}` as a placeholder for the specific object type.

**A. Object APIs:**

Access records and activities.  Replace `{objectTypeId}` with the appropriate ID (see table below).

* **`POST /crm/v3/objects/{objectTypeId}`:** Create a new record.
* **`GET /crm/v3/objects/{objectTypeId}`:** Retrieve records.
* **`PATCH /crm/v3/objects/{objectTypeId}/{recordId}`:** Update a record.  `recordId` can be `hs_object_id` or a custom unique identifier (using `idProperty` parameter).
* **Example (Creating a Contact):**  `POST /crm/v3/objects/0-1`  (0-1 is the `objectTypeId` for Contacts)


**B. Object Type IDs:**

| Type ID | Object           | Description                                                                    | API Reference                               |
|---------|-------------------|--------------------------------------------------------------------------------|--------------------------------------------|
| 0-1     | Contacts          | Stores information about an individual person.                               | [Contacts API](link-to-contacts-api)      |
| 0-2     | Companies         | Stores information about a business or organization.                          | [Companies API](link-to-companies-api)    |
| 0-3     | Deals             | Represent sales opportunities.                                                | [Deals API](link-to-deals-api)            |
| 0-5     | Tickets           | Represent customer support requests.                                          | [Tickets API](link-to-tickets-api)        |
| ...     | ...               | ...                                                                          | ...                                        |
| 2-XXX   | Custom Objects    | Stores custom data.  `objectTypeId` obtained via `GET /crm/v3/schemas`.       | [Custom Objects API](link-to-custom-api)  |


**C. Associations API:**

Manage relationships between records. Replace `{fromObjectTypeId}` and `{toObjectTypeId}` with appropriate IDs.

* **`GET /crm/v4/associations/{fromObjectTypeId}/{toObjectTypeId}/labels`:** Retrieve association types between two objects.
* **`POST /crm/v4/associations/{fromObjectTypeId}/{toObjectTypeId}`:** Associate records.
* **`DELETE /crm/v4/associations/{fromObjectTypeId}/{toObjectTypeId}`:** Disassociate records.


**D. Properties API:**

Manage properties for objects. Replace `{objectTypeId}` with the appropriate ID.

* **`GET /crm/v3/properties/{objectTypeId}`:** Retrieve properties for an object.
* **`POST /crm/v3/properties/{objectTypeId}`:** Create a custom property.


**E. Search API:**

Search for records and activities based on properties and associations. Replace `{objectTypeId}` with the appropriate ID.

* **`POST /crm/v3/objects/{objectTypeId}/search`:** Perform a search.


**F. Pipelines API:**

Manage pipelines and stages.  Specific endpoints depend on the object.


## IV.  Example: Creating a Contact

```json
{
  "properties": {
    "firstname": "John",
    "lastname": "Doe",
    "email": "john.doe@example.com"
  }
}
```

This JSON would be sent in the body of a `POST` request to `/crm/v3/objects/0-1`.


## V. Error Handling

The APIs return standard HTTP status codes (e.g., 200 for success, 400 for bad request, 500 for server error).  Error responses usually include detailed error messages.


**Note:** Replace placeholder links (`link-to-contacts-api`, etc.) with actual HubSpot API documentation links.  This markdown provides a structured overview; the actual API details are extensive and should be referenced in the official HubSpot documentation.
