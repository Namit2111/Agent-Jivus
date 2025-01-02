# HubSpot CRM APIs Documentation

This document provides an overview of the HubSpot CRM APIs, explaining how to interact with the CRM's data using various endpoints.

## I. Understanding the HubSpot CRM

The HubSpot CRM is a database storing information about your business relationships and processes.  It uses the concept of **objects**, which represent types of relationships (e.g., contacts, companies, deals), and **records**, which are individual instances of these objects (e.g., a specific contact, a specific company).  Data within records is stored using **properties** (e.g., email address, company name). Relationships between records are managed through **associations**.  The CRM also tracks interactions (**engagements/activities**) like emails and calls.


## II. Key API Concepts

* **Object APIs:**  Provide access to records and activities.  Each object has a unique numerical `objectTypeId`.  Endpoints generally use `{objectTypeId}` as a placeholder. For example, to create a contact (objectTypeId: `0-1`), use a POST request to `/crm/v3/objects/0-1`.  Some objects have limited API functionality.

* **Object Type IDs:** A unique numerical identifier for each object type (e.g., contacts, companies, deals).  See the table below for a list of object types and their IDs.

* **Unique Identifiers and Record IDs:** Each record has a unique `hs_object_id` (Record ID).  For contacts and companies, additional unique identifiers like email and domain are available.  Some objects support custom unique identifier properties.  You can use either `hs_object_id` or a custom unique identifier (specified via the `idProperty` parameter) to identify records in API requests.

* **Associations API:** Manages relationships between records of different objects.  Endpoints use `{fromObjectTypeId}` and `{toObjectTypeId}` placeholders.  You can retrieve association types to understand which objects can be associated. Association labels can describe the relationship types.

* **Properties API:** Manages properties (fields) within objects.  Endpoints use `{objectTypeId}`. You can create and manage default and custom properties.

* **Search API:** Allows filtering and sorting records and activities based on properties and associations.  Endpoints use `{objectTypeId}`.

* **Pipelines API:** Manages pipelines (e.g., sales pipelines, support ticket statuses) for specific objects.


## III. Object Type IDs

| Type ID | Object             | Description                                                                     | API Reference                               |
|---------|----------------------|---------------------------------------------------------------------------------|-------------------------------------------|
| 0-2     | Companies           | Stores information about businesses.                                             | [Companies API](link-to-companies-api)     |
| 0-1     | Contacts            | Stores information about individuals.                                           | [Contacts API](link-to-contacts-api)      |
| 0-3     | Deals               | Represent sales opportunities.                                                  | [Deals API](link-to-deals-api)           |
| 0-5     | Tickets             | Represent customer support requests.                                            | [Tickets API](link-to-tickets-api)        |
| 0-421   | Appointments        | Represent scheduled encounters.                                               | [Objects API](link-to-objects-api)         |
| 0-48    | Calls               | Represents phone call interactions.                                             | [Calls API](link-to-calls-api)           |
| 0-18    | Communications      | Represents SMS, LinkedIn, and WhatsApp messages.                               | [Communications API](link-to-comm-api)    |
| 0-410   | Courses             | Represent structured learning programs.                                         | [Objects API](link-to-objects-api)         |
| 2-XXX   | Custom objects      | Stores data not fitting into existing objects.  Get `objectTypeId` via `/crm/v3/schemas` | [Custom Objects API](link-to-custom-api)   |
| 0-49    | Emails              | Represents one-to-one email interactions.                                      | [Email API](link-to-email-api)           |
| 0-19    | Feedback submissions | Stores information from feedback surveys.                                       | [Feedback Submissions API](link-to-feedback-api) |
| 0-52    | Invoices            | Represent invoices sent for sales transactions.                               | [Invoices API](link-to-invoices-api)      |
| 0-136   | Leads               | Represent potential customers.                                                 | [Leads API](link-to-leads-api)            |
| 0-8     | Line items          | Represent individual products/services in a deal.                              | [Line Items API](link-to-line-items-api)   |
| 0-420   | Listings            | Represent properties for sale/rent.                                            | [Objects API](link-to-objects-api)         |
| 0-54    | Marketing events    | Represent marketing events.                                                    | [Marketing Events API](link-to-marketing-api) |
| 0-47    | Meetings            | Represents meeting interactions.                                               | [Meetings API](link-to-meetings-api)      |
| 0-46    | Notes               | Represents notes associated with records.                                       | [Notes API](link-to-notes-api)           |
| 0-101   | Payments            | Represents payments made.                                                      | [Payments API](link-to-payments-api)      |
| 0-116   | Postal mail         | Represents physical mail interactions.                                         | [Postal Mail API](link-to-postal-api)     |
| 0-7     | Products            | Represent goods or services for sale.                                          | [Products API](link-to-products-api)     |
| 0-14    | Quotes              | Represent pricing information.                                                  | [Quotes API](link-to-quotes-api)         |
| 0-162   | Services            | Represent intangible offerings.                                                 | [Objects API](link-to-objects-api)         |
| 0-69    | Subscriptions       | Represent recurring payments.                                                  | [Subscriptions API](link-to-subscriptions-api) |
| 0-27    | Tasks               | Represent to-dos.                                                              | [Tasks API](link-to-tasks-api)           |
| 0-115   | Users               | Represent HubSpot account users.                                               | [User Details API](link-to-user-api)       |


**(Note:  Replace `link-to-api-name` with actual API documentation links.)**


## IV. API Examples

**(Note: These are simplified examples.  Refer to the individual API documentation for detailed request parameters and responses.)**


**A. Create a Contact:**

```http
POST /crm/v3/objects/0-1
{
  "properties": {
    "email": "john.smith@example.com",
    "firstname": "John",
    "lastname": "Smith"
  }
}
```

**B. Get a Contact by Email:**

```http
GET /crm/v3/objects/0-1/john.smith@example.com?idProperty=email
```

**C. Associate a Contact with a Company:**

```http
PUT /crm/v4/associations/0-1/0-2/{contactId}/associatedCompanyIds
{
  "associations": [
    {
      "id": "{companyId}",
      "type": "company"
    }
  ]
}
```

**D. Search for Deals:**

```http
POST /crm/v3/objects/0-3/search
{
  "filterGroups": [
    {
      "filters": [
        {
          "propertyName": "dealstage",
          "operator": "EQ",
          "value": "closedwon"
        }
      ]
    }
  ]
}
```


## V.  Further Information

* **HubSpot Knowledge Base:** For general CRM management information.
* **Individual API Documentation:**  Consult the specific API documentation for each object and functionality for detailed information, request parameters, response formats, and error handling.


This documentation provides a high-level overview.  Always refer to the official HubSpot API documentation for the most up-to-date and detailed information.
