# HubSpot CRM APIs Documentation

This document provides an overview of the HubSpot CRM APIs, focusing on key concepts and how to interact with them.

## I. Core Concepts

The HubSpot CRM is a database of business relationships and processes.  It's structured around:

* **Objects:** Represent types of relationships or processes (e.g., Contacts, Companies, Deals).  Each object has a unique `objectTypeId`.
* **Records:** Individual instances of an object (e.g., a specific Contact record). Each record has a unique `hs_object_id` (Record ID).
* **Properties:** Fields within records that store data (e.g., email address, company name).  Default and custom properties exist.
* **Associations:** Links between records of different objects (e.g., associating a Contact with a Company).
* **Pipelines:** Track records through stages in a process (e.g., Deal stages in a sales pipeline).

## II. API Endpoints and Usage

The CRM APIs use RESTful principles.  Base URLs typically include `/crm/v3/objects/{objectTypeId}` where `{objectTypeId}` is a numerical ID.

### A. Object APIs

Access records and activities.  Replace `{objectTypeId}` with the appropriate ID (see Table below).

* **Create a record:** `POST /crm/v3/objects/{objectTypeId}`
* **Get a record:** `GET /crm/v3/objects/{objectTypeId}/{recordId}`  (or using a unique identifier property like email)
* **Update a record:** `PATCH /crm/v3/objects/{objectTypeId}/{recordId}` (or using a unique identifier property)

**Example (Creating a Contact):**

```bash
curl -X POST \
  https://api.hubapi.com/crm/v3/objects/0-1 \
  -H 'Content-Type: application/json' \
  -d '{
    "properties": {
      "firstname": "John",
      "lastname": "Doe",
      "email": "john.doe@example.com"
    }
  }'
```

**Response (Example):**

```json
{
  "id": "123",
  "properties": {
    "firstname": "John",
    "lastname": "Doe",
    "email": "john.doe@example.com"
  }
}
```


### B. Object Type IDs

| Type ID | Object           | Description                                                              | API Reference                 |
|---------|-------------------|--------------------------------------------------------------------------|-------------------------------|
| 0-1     | Contacts          | Stores information about an individual person.                         | [/contacts API](link-to-contacts-api) |
| 0-2     | Companies         | Stores information about a business or organization.                    | [/companies API](link-to-companies-api) |
| 0-3     | Deals             | Represent sales opportunities.                                          | [/deals API](link-to-deals-api)     |
| 0-5     | Tickets           | Represent customer support requests.                                   | [/tickets API](link-to-tickets-api)   |
| ...     | ...               | ...                                                                    | ...                           |
| 2-XXX   | Custom Objects    | Stores custom data.  `objectTypeId` retrieved via `/crm/v3/schemas` GET request | [/custom objects API](link-to-custom-objects-api) |


### C. Unique Identifiers and Record IDs

Each record has a unique `hs_object_id` (`recordId`).  Some objects (Contacts, Companies) have additional unique identifiers (email, domain).  Custom unique identifiers can also be created.

* **Example (using email to update a contact):** `PATCH /crm/v3/objects/0-1/john.doe@example.com?idProperty=email`

### D. Associations API

Manage relationships between records.

* **Get association types:** `GET /crm/v4/associations/{fromObjectType}/{toObjectType}/labels` (using object type IDs or names)
* **Associate records:** `PUT /crm/v4/associations/{fromObjectType}/{toObjectType}/{fromObjectId}/{toObjectId}`

### E. Properties API

Manage object properties (default and custom).

* **Get properties for an object:** `GET /crm/v3/properties/{objectTypeId}`
* **Create a custom property:** `POST /crm/v3/properties/{objectTypeId}`

### F. Search API

Search for records based on properties and associations.

* **Search for records:** `POST /crm/v3/objects/{objectTypeId}/search`

### G. Pipelines API

Manage pipelines and stages.


## III.  Further Information

* **HubSpot's Knowledge Base:** [link-to-knowledge-base]  (For CRM management within HubSpot)
* **Object Endpoints Reference:** [link-to-object-endpoints]
* **Properties API Article:** [link-to-properties-api-article]
* **Search API Article:** [link-to-search-api-article]
* **Pipelines API Article:** [link-to-pipelines-api-article]


**(Note: Replace bracketed placeholders like `[link-to-contacts-api]` with actual links to relevant HubSpot documentation.)**
