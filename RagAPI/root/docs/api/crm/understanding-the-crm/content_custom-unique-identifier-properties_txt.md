# HubSpot CRM APIs Documentation

This document provides an overview of the HubSpot CRM APIs, enabling developers to interact with HubSpot's Customer Relationship Management (CRM) database programmatically.

## I. Core Concepts

* **Objects:** Represent types of relationships or processes within the CRM (e.g., Contacts, Companies, Deals).
* **Records:** Individual instances of an object (e.g., a specific contact, a specific company).
* **Properties:** Fields within records that store data (e.g., email address, company name).  Default and custom properties are supported.
* **Associations:** Links between records of different objects (e.g., associating a contact with a company).
* **Pipelines:**  Represent stages in processes (e.g., sales pipeline stages for deals, support statuses for tickets).
* **Object Type ID (`objectTypeId`):** A unique numerical identifier for each object type (e.g., `0-1` for Contacts, `0-2` for Companies).  This ID is crucial for API interactions.


## II. API Endpoints and Examples

The base URL for many CRM API endpoints is `/crm/v3/`.  Specific object types are referenced using their `objectTypeId`.

**A. Object APIs:** Provide access to records and activities.

* **Endpoint:** `/crm/v3/objects/{objectTypeId}`
* **Methods:** `GET`, `POST`, `PATCH`, `DELETE` (depending on object and permissions).
* **Example (creating a contact):**
    ```bash
    POST /crm/v3/objects/0-1
    {
      "properties": {
        "firstname": "John",
        "lastname": "Doe",
        "email": "john.doe@example.com"
      }
    }
    ```
    *Response:*  A JSON object containing the newly created contact's details, including its `hs_object_id`.

* **Object Type IDs:**  A table is provided in the source text detailing `objectTypeId` for various objects (Contacts, Companies, Deals, etc.).  Custom objects have their `objectTypeId` retrievable via a `GET` request to `/crm/v3/schemas`.

**B. Associations API:** Manages relationships between records.

* **Endpoint (example for associating a contact with a company):** `/crm/v4/associations/{fromObjectType}/{toObjectType}/<association_id>`
    * Replace `{fromObjectType}` and `{toObjectType}` with object type IDs (e.g., `0-1` for Contacts, `0-2` for Companies) or names (where applicable, like 'contact', 'company').
    * `<association_id>` is the ID of the association being managed (created, deleted, updated).
* **Methods:** `GET`, `POST`, `DELETE`
* **Example (retrieving association types between contacts and companies):**
    ```bash
    GET /crm/v4/associations/contact/company/labels  //or /crm/v4/associations/0-1/0-2/labels
    ```


**C. Properties API:** Creates, retrieves, updates, and deletes properties for objects.

* **Endpoint:** `/crm/v3/properties/{objectTypeId}`
* **Methods:** `GET`, `POST`, `PATCH`, `DELETE`
* **Example (getting properties for contacts):**
    ```bash
    GET /crm/v3/properties/0-1
    ```


**D. Search API:** Searches for records and activities based on properties and associations.

* **Endpoint:** `/crm/v3/objects/{objectTypeId}/search`
* **Method:** `POST`
* **Example (searching for calls):**
    ```bash
    POST /crm/v3/objects/0-48/search
    {
      "filterGroups": [
        // Add filter criteria here
      ]
    }
    ```


**E. Pipelines API:** Manages pipelines and their stages.

* **Endpoint:** (varies, dependent on the object and its pipeline) Consult HubSpot's documentation for specific endpoints.
* **Methods:** `GET`, `POST`, `PATCH`, `DELETE`


## III. Unique Identifiers and Record IDs

* **`hs_object_id`:**  Automatically generated unique identifier for each record. Treated as a string.
* **Custom Unique Identifiers:** Can be created for certain objects (Contacts, Companies, etc.) to provide additional ways to identify records (e.g., email for Contacts, domain for Companies).  These are specified using the `idProperty` parameter in some API calls.

## IV.  Error Handling

The APIs return standard HTTP status codes to indicate success or failure.  Detailed error messages are included in the response body for troubleshooting.

## V. Rate Limits

HubSpot APIs have rate limits to prevent abuse.  Developers should be mindful of these limits and implement appropriate retry mechanisms if necessary.  Refer to HubSpot's documentation for specific details.


This documentation provides a high-level overview.  For detailed information and the most up-to-date specifications, please consult the official HubSpot API documentation.
