# HubSpot CRM APIs Documentation

This document provides an overview of the HubSpot CRM APIs, focusing on key concepts and usage examples.

## I. Core Concepts

The HubSpot CRM is a database of business relationships and processes.  It's structured around:

* **Objects:** Represent types of relationships or processes (e.g., Contacts, Companies, Deals).
* **Records:** Individual instances of objects (e.g., a specific contact, a particular deal).
* **Properties:** Fields within records that store data (e.g., contact's email address, deal's value).
* **Associations:** Links between records of different objects (e.g., associating a contact with a company).
* **Activities/Engagements:**  Records of interactions (emails, calls, meetings) associated with other records.
* **Pipelines:**  Represent stages in a process (e.g., deal stages in a sales pipeline).
* **`objectTypeId`:** A unique numerical identifier for each object type.


## II. API Endpoints and Usage

All CRM API endpoints generally follow the pattern `/crm/v3/...`.

**A. Object APIs:**

Provide access to records and activities.  The `objectTypeId` is used to specify the object.

* **Example (Creating a Contact):**
    * `POST /crm/v3/objects/0-1`
    * Requires a JSON payload with contact properties.

* **Example (Creating a Course):**
    * `POST /crm/v3/objects/0-410`
    * Requires a JSON payload with course properties.

* **Note:** Some objects have limited API functionality. Refer to individual object API documentation for details (links provided in the table below).  If documentation is missing, use the generic object API documentation and substitute the `objectTypeId`.


**B. Object Type IDs:**

| `objectTypeId` | Object           | Description                                                                     | API Documentation Link           |
|-----------------|-------------------|---------------------------------------------------------------------------------|------------------------------------|
| 0-2             | Companies         | Stores information about businesses.                                            | [Companies API](link_placeholder) |
| 0-1             | Contacts          | Stores information about individuals.                                           | [Contacts API](link_placeholder)  |
| 0-3             | Deals             | Represent sales opportunities.                                                  | [Deals API](link_placeholder)     |
| 0-5             | Tickets           | Represent customer support requests.                                           | [Tickets API](link_placeholder)   |
| 0-421           | Appointments      | Represent scheduled encounters or services.                                      | [Objects API](link_placeholder)   |
| 0-48            | Calls             | Represents phone call interactions.                                           | [Calls API](link_placeholder)    |
| ...             | ...               | ...                                                                           | ...                               |
| 2-XXX           | Custom Objects    | Stores data not fitting into existing objects.  Get `objectTypeId` via `/crm/v3/schemas` | [Custom Objects API](link_placeholder) |


**C. Unique Identifiers and Record IDs:**

Each record has a unique `Record ID` (`hs_object_id`).  For contacts and companies, other identifiers (email, domain) can also be used.  Custom unique identifier properties can be created for some objects.

* **Example (Editing a Contact using `hs_object_id`):**
    * `PATCH /crm/v3/objects/0-1/{contactId}`

* **Example (Editing a Contact using email):**
    * `PATCH /crm/v3/objects/0-1/{contactEmail}?idProperty=email`

**D. Associations API:**

Manages relationships between records.  Uses `fromObjectType` and `toObjectType` to specify objects.

* **Example (Retrieving association types between Contacts and Companies):**
    * `GET /crm/v4/associations/contact/company/labels`  or `GET /crm/v4/associations/0-1/0-2/labels`

**E. Properties API:**

Manages object properties (default and custom).

* **Example (Accessing Contact Properties):**
    * `/crm/v3/properties/0-1`

**F. Search API:**

Filters and sorts records based on properties and associations.

* **Example (Searching Calls):**
    * `POST /crm/v3/objects/0-48/search`

**G. Pipelines API:**

Manages pipelines and stages for specific objects.


## III.  Further Resources

* HubSpot's Knowledge Base (for CRM management within HubSpot)
* [Link to Object Endpoints Reference](link_placeholder)
* [Link to Objects API Documentation](link_placeholder)
* [Link to Properties API Documentation](link_placeholder)
* [Link to Search API Documentation](link_placeholder)
* [Link to Pipelines API Documentation](link_placeholder)
* [Link to Associations API Endpoints](link_placeholder)


**Note:**  Replace `link_placeholder` with actual links from the original text.  The original text lacks these essential links.  Also, detailed examples requiring JSON payloads are omitted for brevity, but should be included in a complete documentation.  Finally, proper authentication and API key usage are crucial aspects that require explicit inclusion in a comprehensive API documentation.
