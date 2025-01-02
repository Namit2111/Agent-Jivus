# HubSpot Custom Objects API Documentation

This document details the HubSpot API for creating, managing, and interacting with custom objects.  Custom objects allow you to extend the standard HubSpot CRM with data specific to your business needs.

## Authentication

The HubSpot Custom Objects API supports two authentication methods:

* **OAuth:**  Recommended for most integrations. Allows for robust user authorization and permission management.  See HubSpot's OAuth documentation for details.
* **Private App Access Tokens:**  Suitable for server-side integrations where user interaction isn't required.  Generate tokens within your HubSpot Private App settings.  **Note:**  HubSpot API Keys are deprecated as of November 30, 2022, and should not be used.

## API Endpoints

All API endpoints are based on the `https://api.hubapi.com/crm/v3` base URL.

### Custom Object Schema Management

* **`POST /schemas`**: Create a new custom object.  Requires a JSON payload defining the object's schema (name, properties, associations).
* **`GET /schemas`**: Retrieve all custom objects for the authenticated account.
* **`GET /schemas/{objectTypeId}`**: Retrieve a specific custom object by its `objectTypeId`.
* **`GET /schemas/p_{object_name}`**: Retrieve a specific custom object by its name (useful when you don't know the `objectTypeId`).
* **`GET /schemas/{fullyQualifiedName}`**: Retrieve a specific custom object using its `fullyQualifiedName` (e.g., `p1234_objectName`).
* **`PATCH /schemas/{objectTypeId}`**: Update an existing custom object's schema.  You cannot change the object's name or labels after creation.
* **`DELETE /schemas/{objectType}`**: Delete a custom object.  All records of that object type must be deleted first.  To completely remove the schema, use the parameter `?archived=true`.
* **`POST /schemas/{objectTypeId}/associations`**: Create a new association between the custom object and another object (standard or custom).


### Custom Object Records

* **`POST /objects/{objectType}`**: Create a new record for a custom object.
* **`GET /objects/{objectType}/{recordId}`**: Retrieve a specific custom object record by its `recordId`.  Supports query parameters `properties`, `propertiesWithHistory`, and `associations`.
* **`POST /objects/{objectType}/batch/read`**: Retrieve multiple custom object records in a batch.  Does not support retrieving associations.  Uses a JSON payload with an `inputs` array containing record IDs or unique identifiers.  Supports `idProperty` parameter for unique identifier retrieval.
* **`PATCH /objects/{objectType}/{recordId}`**: Update an existing custom object record.


### Properties

* **`POST /properties/{objectTypeId}`**: Create a new property for a custom object.
* **`PATCH /properties/{objectTypeId}/{propertyName}`**: Update an existing property for a custom object.

### Associations

* The API automatically creates associations with `emails`, `meetings`, `notes`, `tasks`, `calls`, and `conversations`.  Additional associations must be created using the `/schemas/{objectTypeId}/associations` endpoint.


## Request/Response Examples

See the provided text for detailed examples of request bodies and responses for various API calls.  These examples showcase creating a custom object schema, creating and retrieving records, associating records, and managing properties and associations.


## Rate Limits

HubSpot imposes rate limits on API calls.  Refer to the HubSpot API documentation for details on these limits.


## Error Handling

The API returns standard HTTP status codes and JSON error responses to indicate success or failure.  Refer to the HubSpot API documentation for details on error codes and handling.


## Data Types

The API utilizes various data types, including:

* **`string`**: Plain text.
* **`number`**: Numeric values.
* **`date`**: ISO 8601 formatted date (YYYY-MM-DD).
* **`dateTime`**: ISO 8601 formatted date and time.
* **`enumeration`**: A set of predefined options.
* **`boolean`**: True or False.


This documentation provides a high-level overview.  Always refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications.
