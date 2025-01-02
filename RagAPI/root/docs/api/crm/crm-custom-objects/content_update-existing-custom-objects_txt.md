# HubSpot Custom Objects API Documentation

This document details the HubSpot Custom Objects API, allowing you to create, manage, and interact with custom objects within your HubSpot account.  This API extends the standard CRM objects (contacts, companies, deals, tickets) to accommodate your specific business needs.

## Supported Products

Requires one of the following HubSpot products or higher:

* Marketing Hub - Enterprise
* Sales Hub - Enterprise
* Content Hub - Enterprise
* Service Hub - Enterprise
* Operations Hub - Enterprise


## Authentication

The API supports two authentication methods:

* **OAuth:**  Recommended for most integrations.
* **Private App Access Tokens:**  Suitable for server-side integrations.

**Note:** HubSpot API Keys are deprecated as of November 30, 2022, and are no longer supported.


## API Endpoints

All endpoints are under the `/crm/v3` base URL.  Replace placeholders like `{objectTypeId}` with actual values.

### 1. Custom Object Schema Management

* **Create a Custom Object:**

    * **Method:** `POST`
    * **Endpoint:** `/schemas`
    * **Request Body:**  JSON object defining the schema (see example below).  Includes object name, properties, associations, labels, and display properties.
    * **Response:** JSON object containing the newly created object's details, including `objectTypeId` and `fullyQualifiedName`.

* **Retrieve Custom Objects:**

    * **Method:** `GET`
    * **Endpoint:** `/schemas` (all objects) or `/schemas/{objectTypeId}` (specific object), `/schemas/p_{object_name}`, `/schemas/{fullyQualifiedName}`
    * **Response:** JSON array (for `/schemas`) or JSON object (for others) containing custom object schema details.

* **Update a Custom Object:**

    * **Method:** `PATCH`
    * **Endpoint:** `/schemas/{objectTypeId}`
    * **Request Body:** JSON object with updates to the schema.  Only properties, display properties (`primaryDisplayProperty`, `secondaryDisplayProperties`), required properties (`requiredProperties`), and searchable properties (`searchableProperties`) are updatable. The object name and labels cannot be changed.
    * **Response:** Updated JSON object representing the custom object schema.

* **Delete a Custom Object:**

    * **Method:** `DELETE`
    * **Endpoint:** `/schemas/{objectTypeId}`
    * **Note:**  Requires all associated records and properties to be deleted first. Use `?archived=true` for a hard delete to allow object recreation with the same name.
    * **Response:** Success or error message.


### 2. Custom Object Record Management

* **Create a Custom Object Record:**

    * **Method:** `POST`
    * **Endpoint:** `/objects/{objectTypeId}`
    * **Request Body:** JSON object with properties and their values.
    * **Response:** JSON object containing the newly created record's details, including `id`.

* **Retrieve Custom Object Records:**

    * **Method:** `GET` (single record) or `POST` (batch read)
    * **Endpoint (GET):** `/objects/{objectTypeId}/{recordId}`
    * **Endpoint (POST):** `/objects/{objectTypeId}/batch/read`
    * **Query Parameters (GET):** `properties` (comma-separated list), `propertiesWithHistory`, `associations`
    * **Request Body (POST):**  JSON object with `inputs` (array of IDs or unique identifiers) and optional `properties`, `propertiesWithHistory`, and `idProperty` (for custom unique identifier). Batch read does *not* support associations.
    * **Response:** JSON object (for single record) or JSON array (for batch read) containing record details.

* **Update a Custom Object Record:**

    * **Method:** `PATCH`
    * **Endpoint:** `/objects/{objectTypeId}/{recordId}`
    * **Request Body:** JSON object with properties and updated values.
    * **Response:** Updated JSON object representing the custom object record.


### 3. Associations

* **Create an Association:**

    * **Method:** `PUT`
    * **Endpoint:** `/objects/{objectTypeId}/{objectId}/associations/{toObjectType}/{toObjectId}/{associationType}`

* **Create a New Association Definition:**

    * **Method:** `POST`
    * **Endpoint:** `/schemas/{objectTypeId}/associations`
    * **Request Body:** JSON object defining the association (from object type, to object type, name).

* **Retrieve Associations:**  This is done as part of retrieving records using the `associations` query parameter in the `/objects/{objectTypeId}/{recordId}` endpoint.


### 4. Properties

* **Create a New Property:**

    * **Method:** `POST`
    * **Endpoint:** `/properties/{objectTypeId}`
    * **Request Body:** JSON object defining the property (name, label, type, fieldType, options for enumeration).

* **Update a Property:**  Indirectly updated by updating the custom object schema.

## Example Walkthrough: Creating a "Cars" Custom Object


This example demonstrates creating a custom object to track car inventory, associating it with contacts, and adding a maintenance package property.  See the provided text for detailed code examples for each step.


This comprehensive overview covers the core functionalities of the HubSpot Custom Objects API.  Remember to consult the official HubSpot API documentation for the most up-to-date information and detailed specifications.
