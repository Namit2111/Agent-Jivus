# HubSpot CRM APIs Documentation

This document provides an overview of the HubSpot CRM APIs, focusing on key concepts and usage examples.

## Introduction

The HubSpot CRM is a database storing business relationships and processes.  It's structured around objects (representing relationship/process types) and records (individual instances of objects). Data within records is managed using properties, and relationships between records are established via associations.  Interactions are recorded as engagements/activities.

## Key Concepts

* **Objects:**  Represent types of relationships or processes (e.g., Contacts, Companies, Deals).  Each object has a unique `objectTypeId`.
* **Records:** Individual instances of an object (e.g., a specific contact record).  Each record has a unique `hs_object_id` (Record ID).
* **Properties:** Fields storing data within a record (e.g., email address, company name).  Default and custom properties exist.
* **Associations:** Links between records of different objects (e.g., associating a contact with a company).
* **Pipelines:**  Track records through stages in a process (e.g., deal stages in a sales process).


## API Endpoints and Usage

The CRM APIs use RESTful principles.  Many endpoints utilize the `objectTypeId` to specify the object being accessed.

### 1. Object APIs

Access records and activities.  Replace `{objectTypeId}` with the appropriate ID.

* **Example (Creating a Contact):**
    ```bash
    POST /crm/v3/objects/0-1
    ```
* **Example (Creating a Course):**
    ```bash
    POST /crm/v3/objects/0-410
    ```

  See [this article](replace_with_actual_article_link) for more information on object endpoints.  Some objects have limited API functionality; check object-specific documentation.


### 2. Object Type IDs

Each object has a numerical `objectTypeId`.

| Type ID | Object             | Description                                                                | API Reference                               |
|---------|----------------------|----------------------------------------------------------------------------|-------------------------------------------|
| 0-2     | Companies           | Stores information about businesses.                                        | [Companies API](replace_with_actual_link) |
| 0-1     | Contacts            | Stores information about individuals.                                       | [Contacts API](replace_with_actual_link)  |
| 0-3     | Deals               | Represents sales opportunities.                                            | [Deals API](replace_with_actual_link)    |
| 0-5     | Tickets             | Represents customer support requests.                                      | [Tickets API](replace_with_actual_link)   |
| ...     | ...                 | ...                                                                        | ...                                       |
| 2-XXX   | Custom Objects      | Stores data not fitting existing objects.  Get `objectTypeId` via `/crm/v3/schemas` GET request. | [Custom Objects API](replace_with_actual_link) |


You can sometimes use object names (contact, company, deal, ticket, note) instead of the numerical ID.


### 3. Unique Identifiers and Record IDs

Each record has a unique `hs_object_id` (`Record ID`). For contacts and companies, other unique identifiers (email, domain) exist. Custom unique identifiers can be created.

* **Example (Editing a Contact using `hs_object_id`):**
    ```bash
    PATCH /crm/v3/objects/0-1/{contactId}
    ```
* **Example (Editing a Contact using email as unique identifier):**
    ```bash
    PATCH /crm/v3/objects/0-1/{contactEmail}?idProperty=email
    ```


### 4. Associations API

Manage relationships between records. Replace `{toObjectTypeId}` and `{fromObjectTypeId}` with appropriate IDs.

* **Example (Retrieving association types between contacts and companies):**
    ```bash
    GET /crm/v4/associations/contact/company/labels  OR  GET /crm/v4/associations/0-1/0-2/labels
    ```

See [associations API endpoints](replace_with_actual_link) and learn how to retrieve association types.


### 5. Properties API

Manage properties (fields) for objects.

* **Example (Accessing contact properties):**
    ```bash
    GET /crm/v3/properties/0-1
    ```
* **Example (Accessing ticket properties):**
    ```bash
    GET /crm/v3/properties/0-5
    ```

See [this article](replace_with_actual_article_link) for details.


### 6. Search API

Filter and sort records.  Replace `{objectTypeId}` with the target object.

* **Example (Searching calls):**
    ```bash
    POST /crm/v3/objects/0-48/search
    ```

See [this article](replace_with_actual_article_link) for details.


### 7. Pipelines API

Manage pipelines (process stages) for objects. See [this article](replace_with_actual_article_link) for details.


##  Error Handling

(Add a section describing how errors are handled by the API, including status codes and error responses.  Example responses would be beneficial.)


## Authentication

(Add a section describing how to authenticate with the API.  This likely involves API keys or OAuth.)


Remember to replace placeholder links (`replace_with_actual_link`, `replace_with_actual_article_link`) with the correct HubSpot documentation links.
