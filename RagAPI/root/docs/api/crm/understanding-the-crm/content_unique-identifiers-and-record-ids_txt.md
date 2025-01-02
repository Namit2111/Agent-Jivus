# HubSpot CRM APIs Documentation

This document provides an overview of the HubSpot CRM APIs, explaining how to interact with the CRM database using various endpoints.

## I. Core Concepts

The HubSpot CRM stores data about your business relationships and processes in the form of **objects** and **records**.

* **Objects:** Represent types of relationships or processes (e.g., Contacts, Companies, Deals).  Each object has a unique `objectTypeId`.
* **Records:** Individual instances of an object (e.g., a specific contact, a specific company). Each record has a unique `hs_object_id` (Record ID).
* **Properties:** Fields within records that store data (e.g., `email` for Contacts, `company` for Deals).  Default and custom properties exist.
* **Associations:** Links between records of different objects (e.g., associating a contact with a company).
* **Pipelines:**  Represent stages in business processes (e.g., sales pipeline stages for Deals, support statuses for Tickets).

## II. API Endpoints and Usage

The CRM APIs utilize a RESTful architecture with endpoints structured as follows:  `/crm/v3/...`

### A. Object APIs

These APIs provide access to records and activities for various objects.  The `objectTypeId` is crucial for specifying the target object.

**Example:**

* **Creating a Contact:** `POST /crm/v3/objects/0-1` (0-1 is the `objectTypeId` for Contacts)
* **Creating a Course:** `POST /crm/v3/objects/0-410` (0-410 is the `objectTypeId` for Courses)

**Note:** Some objects have limited API functionality. Refer to the individual object API documentation for details (links provided in the table below).  If documentation is absent, the generic Object API documentation can be used, substituting the appropriate `objectTypeId`.


### B. Object Type IDs

The following table lists `objectTypeId` values for common objects:

| Type ID | Object           | Description                                                                     | API Reference                               |
|---------|-------------------|---------------------------------------------------------------------------------|-------------------------------------------|
| 0-2     | Companies         | Stores information about businesses.                                           | [Companies API](link-to-companies-api)     |
| 0-1     | Contacts          | Stores information about individuals.                                          | [Contacts API](link-to-contacts-api)      |
| 0-3     | Deals             | Represent sales opportunities.                                                 | [Deals API](link-to-deals-api)            |
| 0-5     | Tickets           | Represent customer support requests.                                           | [Tickets API](link-to-tickets-api)        |
| 0-421   | Appointments      | Represent scheduled encounters.                                                | [Objects API](link-to-objects-api)         |
| 0-48    | Calls             | Represents phone call interactions.                                            | [Calls API](link-to-calls-api)            |
| ...     | ...               | ...                                                                           | ...                                       |
| 2-XXX   | Custom Objects    | Stores custom data.  `objectTypeId` retrieved via `GET /crm/v3/schemas`.       | [Custom Objects API](link-to-custom-api)   |


**Note:**  For Contacts, Companies, Deals, Tickets, and Notes, the object name (e.g., "contact") can sometimes be used instead of the numeric `objectTypeId`.


### C. Unique Identifiers and Record IDs

Each record has a unique `hs_object_id` (Record ID).  For Contacts and Companies, additional unique identifiers exist (email, domain).  Custom unique identifier properties can also be created.

**Example:** Editing a Contact using `hs_object_id`:

`PATCH /crm/v3/objects/0-1/{contactId}`

**Example:** Editing a Contact using email as the identifier:

`PATCH /crm/v3/objects/0-1/{contactEmail}?idProperty=email`


### D. Associations API

This API manages relationships between records of different objects.

**Example:** Retrieving association types between Contacts and Companies:

`GET /crm/v4/associations/contact/company/labels`  or  `GET /crm/v4/associations/0-1/0-2/labels`


### E. Properties API

This API manages properties (fields) within objects.

**Example:** Managing Contact properties:

`/crm/v3/properties/0-1`


### F. Search API

This API allows filtering and sorting records based on properties and associations.

**Example:** Searching Calls:

`POST /crm/v3/objects/0-48/search`


### G. Pipelines API

This API manages pipelines and their stages.  (See linked documentation for object support and usage.)


## III.  Further Information

* **HubSpot Knowledge Base:** (link to HubSpot Knowledge Base)  Provides additional information on CRM management.
* **Object API Documentation:** (link to Object API documentation)  Detailed information on object API endpoints.
* **Associations API Documentation:** (link to Associations API documentation)  Detailed information on Associations API endpoints.
* **Properties API Documentation:** (link to Properties API documentation) Detailed information on Properties API endpoints.
* **Search API Documentation:** (link to Search API documentation) Detailed information on Search API endpoints.
* **Pipelines API Documentation:** (link to Pipelines API documentation) Detailed information on Pipelines API endpoints.


**(Remember to replace placeholder links with actual links to HubSpot's documentation.)**
