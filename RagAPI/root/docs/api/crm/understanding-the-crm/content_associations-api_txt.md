# HubSpot CRM APIs Documentation

This document provides an overview of the HubSpot CRM APIs, explaining how to interact with the CRM database programmatically.  The CRM stores business relationships and processes as objects and records, using properties to store data and associations to link records.

## I. Core Concepts

* **Objects:** Represent types of relationships or processes (e.g., Contacts, Companies, Deals). Each object has a unique `objectTypeId`.
* **Records:** Individual instances of an object (e.g., a specific contact record). Each record has a unique `hs_object_id` (Record ID).
* **Properties:** Fields within a record that store data (e.g., email address, company name).  Default and custom properties are available.
* **Associations:** Links between records of different objects (e.g., associating a contact with a company).
* **Pipelines:** Tracks records through stages in a process (e.g., sales pipeline stages for deals).

## II. Object APIs

The Object APIs provide access to records and activities.  Endpoints use the `objectTypeId` to specify the object.

**Example:**

* **Creating a Contact:** `POST /crm/v3/objects/0-1`
* **Creating a Course:** `POST /crm/v3/objects/0-410`

**Note:** Some objects have limited API functionality. Refer to the object's specific documentation (links provided in the table below) or the general Objects API documentation, substituting `{objectTypeId}`.

## III. Object Type IDs

The `objectTypeId` is a numerical value uniquely identifying each object.

| Type ID | Object           | Description                                                                     | API Documentation Link                     |
|---------|-------------------|---------------------------------------------------------------------------------|---------------------------------------------|
| 0-2     | Companies         | Stores information about a business or organization.                           | [Companies API](link_to_companies_api)     |
| 0-1     | Contacts          | Stores information about an individual person.                               | [Contacts API](link_to_contacts_api)       |
| 0-3     | Deals             | Represent sales opportunities and transactions.                               | [Deals API](link_to_deals_api)             |
| 0-5     | Tickets           | Represent customer support requests.                                          | [Tickets API](link_to_tickets_api)         |
| 0-421   | Appointments      | Represent scheduled encounters or services.                                   | [Objects API](link_to_objects_api)         |
| 0-48    | Calls             | Phone call interactions.                                                      | [Calls API](link_to_calls_api)            |
| 0-18    | Communications    | SMS, LinkedIn, and WhatsApp message interactions.                             | [Communications API](link_to_comms_api)   |
| 0-410   | Courses           | Structured programs or series of lessons.                                     | [Objects API](link_to_objects_api)         |
| 2-XXX   | Custom objects    | Stores data not fitting in existing objects.  Use `/crm/v3/schemas` to find `objectTypeId`. | [Custom Objects API](link_to_custom_api)   |
| 0-49    | Emails            | One-to-one email interactions.                                                | [Email API](link_to_email_api)            |
| 0-19    | Feedback submissions | Information submitted to feedback surveys.                                   | [Feedback Submissions API](link_to_feedback_api) |
| 0-52    | Invoices          | Represent invoices sent for sales transactions.                              | [Invoices API](link_to_invoices_api)       |
| 0-136   | Leads             | Represent potential customers.                                                | [Leads API](link_to_leads_api)            |
| 0-8     | Line items        | Individual products and services sold in a deal.                             | [Line Items API](link_to_line_items_api)   |
| 0-420   | Listings          | Represent properties or units to be bought, sold, or rented.                 | [Objects API](link_to_objects_api)         |
| 0-54    | Marketing events  | Events related to marketing efforts.                                         | [Marketing Events API](link_to_marketing_events_api) |
| 0-47    | Meetings          | Meeting interactions.                                                        | [Meetings API](link_to_meetings_api)      |
| 0-46    | Notes             | Notes associated with records.                                                | [Notes API](link_to_notes_api)            |
| 0-101   | Payments          | Payments made by buyers.                                                     | [Payments API](link_to_payments_api)      |
| 0-116   | Postal mail       | Physical mail interactions.                                                   | [Postal Mail API](link_to_postal_mail_api)|
| 0-7     | Products          | Goods or services for sale.                                                  | [Products API](link_to_products_api)      |
| 0-14    | Quotes            | Pricing information shared with potential buyers.                             | [Quotes API](link_to_quotes_api)          |
| 0-162   | Services          | Intangible offerings provided to customers.                                  | [Objects API](link_to_objects_api)         |
| 0-69    | Subscriptions     | Recurring payments.                                                          | [Subscriptions API](link_to_subscriptions_api) |
| 0-27    | Tasks             | To-dos associated with records.                                               | [Tasks API](link_to_tasks_api)            |
| 0-115   | Users             | Users in your HubSpot account.                                                | [User Details API](link_to_user_details_api) |


**Note:** Replace `link_to_..._api` placeholders with actual API documentation links.


## IV. Unique Identifiers and Record IDs

Each record has a unique `hs_object_id` (Record ID).  For Contacts and Companies, other unique identifiers (email, domain) exist. Custom unique identifier properties can also be created.

**Example:**  Editing a contact using `email` as the identifier:

`PATCH /crm/v3/objects/0-1/{contactEmail}?idProperty=email`


## V. Associations API

Associates records across different objects.  Endpoints use `{fromObjectTypeId}` and `{toObjectTypeId}`.

**Example:** Retrieving association types for Contacts to Companies:

`GET /crm/v4/associations/contact/company/labels`  or  `GET /crm/v4/associations/0-1/0-2/labels`


## VI. Properties API

Manages properties (fields) within objects.

**Example:**  Accessing Contact properties:

`GET /crm/v3/properties/0-1`


## VII. Search API

Filters and sorts records and activities.

**Example:** Searching Calls:

`POST /crm/v3/objects/0-48/search`


## VIII. Pipelines API

Manages pipelines and pipeline stages for tracking records through processes.


**(Remember to replace placeholder API links with the actual links from the HubSpot Developer documentation.)**
