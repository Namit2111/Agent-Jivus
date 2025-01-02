# HubSpot Custom Objects API Documentation

This document details the HubSpot API for managing custom objects.  Custom objects extend the standard HubSpot CRM (contacts, companies, deals, tickets) to accommodate specific business needs.

## Supported Products

This API requires one of the following HubSpot products or higher:

* Marketing Hub Enterprise
* Sales Hub Enterprise
* Content Hub Enterprise
* Service Hub Enterprise
* Operations Hub Enterprise

## Authentication

The API supports two authentication methods:

* **OAuth:**  Recommended for most integrations.
* **Private App Access Tokens:**  Suitable for internal applications.

**Note:** HubSpot API Keys are deprecated as of November 30, 2022, and are no longer supported.


## API Endpoints

All endpoints are under the base URL: `https://api.hubapi.com/crm/v3/`

### 1. Create a Custom Object

**Endpoint:** `/schemas`

**Method:** `POST`

**Request Body:**  JSON object defining the object schema.  This includes:

* `name`: (String, required)  Object name (alphanumeric and underscores only, must start with a letter).  Cannot be changed after creation.
* `description`: (String) Description of the object.
* `labels`: (Object, required) Singular and plural labels for the object.
    * `singular`: (String, required) Singular label.
    * `plural`: (String, required) Plural label.
* `primaryDisplayProperty`: (String, required) Property used for displaying object records.
* `secondaryDisplayProperties`: (Array of Strings)  Additional properties displayed with the `primaryDisplayProperty`.  The first property listed, if of type string, number, enumeration, boolean, or datetime, will also be added as a fourth filter on the object index page.
* `searchableProperties`: (Array of Strings) Properties indexed for searching.
* `requiredProperties`: (Array of Strings) Properties required when creating new records.
* `properties`: (Array of Objects, required)  Definitions for each property.  See "Properties" section below.
* `associatedObjects`: (Array of Strings)  IDs of associated standard or custom objects.  Standard object names (CONTACT, COMPANY, DEAL, TICKET) or custom object `objectTypeId` values are accepted.

**Example Request:** (See complete example in the original document)

**Example Response:** (Includes `objectTypeId` and `fullyQualifiedName`)

### 2. Retrieve Custom Objects

**Endpoint:** `/schemas` or `/schemas/{objectTypeId}` or `/schemas/p_{object_name}` or `/schemas/{fullyQualifiedName}`

**Method:** `GET`

* `/schemas`: Retrieves all custom objects.
* Other endpoints: Retrieve a specific custom object using its `objectTypeId`, simplified name (`p_{object_name}`), or `fullyQualifiedName` (derived from `p{portal_id}_{object_name}`).

**Example Request:** `GET /schemas/2-3465404` (replace with your `objectTypeId`)

**Example Response:** The custom object schema.


### 3. Retrieve Custom Object Records

**Endpoint:** `/objects/{objectType}/{recordId}` (single record) or `/objects/{objectType}/batch/read` (multiple records)

**Method:** `GET` (single) or `POST` (batch)

* **Single Record:** Retrieves a single record by its `recordId`.  Query parameters: `properties`, `propertiesWithHistory`, `associations`.
* **Batch Read:** Retrieves multiple records.  Request body includes `inputs` (array of `{id}` objects), `properties` (optional), `propertiesWithHistory` (optional), `idProperty` (optional - for custom unique identifiers).  Associations are *not* supported in batch reads.

**Example Single Record Request:** `GET /objects/2-3465404/181308?properties=year,make`

**Example Batch Request (using record IDs):** (See example in original document)

**Example Batch Request (using custom unique identifier):** (See example in original document)


**Example Response (single record):** (See example in original document)


### 4. Update a Custom Object

**Endpoint:** `/schemas/{objectTypeId}`

**Method:** `PATCH`

**Request Body:** JSON object with the properties to update.  `name` and labels cannot be changed.  `requiredProperties`, `searchableProperties`, `primaryDisplayProperty`, and `secondaryDisplayProperties` can be updated.  You must create new properties via the Properties API before modifying these arrays.

**Example Request:** (See example in original document)


### 5. Update Associations

**Endpoint:** `/schemas/{objectTypeId}/associations`

**Method:** `POST`

**Request Body:** JSON object defining the new association.

* `fromObjectTypeId`:  ID of the custom object.
* `toObjectTypeId`: ID of the associated object (standard object name or custom object ID).
* `name`: Name of the association.

**Example Request:** (See example in original document)


### 6. Delete a Custom Object

**Endpoint:** `/schemas/{objectType}` (soft delete) or `/schemas/{objectType}?archived=true` (hard delete)

**Method:** `DELETE`

* Soft delete: Removes the object but retains the data.  The object cannot be reused until all instances, associations, and properties are deleted.
* Hard delete: Permanently deletes the object and all associated data.


## Properties

When defining properties in the object schema, use the following types and `fieldType` values:

| `type`       | Description                                           | Valid `fieldType` values |
|--------------|-------------------------------------------------------|-------------------------|
| `enumeration` | String representing a set of options (semicolon-separated) | `booleancheckbox`, `checkbox`, `radio`, `select` |
| `date`       | ISO 8601 formatted date (YYYY-MM-DD)                  | `date`                   |
| `dateTime`   | ISO 8601 formatted datetime (YYYY-MM-DDTHH:mm:ssZ)      | `date`                   |
| `string`     | Plain text string (up to 65,536 characters)          | `file`, `text`, `textarea` |
| `number`     | Numeric value                                         | `number`                 |

`fieldType` values determine the UI element used for input.


## Examples

A complete walkthrough of creating a sample custom object ("Cars") is provided in the original document, demonstrating schema creation, record creation, association with contacts and tickets, and adding a new property.  Refer to the original document for detailed code examples.


## Rate Limits

Be aware of HubSpot's API rate limits to avoid exceeding allowed requests.  Refer to the HubSpot documentation for details on rate limits.

This markdown document provides a structured and concise overview of the HubSpot Custom Objects API.  Remember to consult the official HubSpot API documentation for the most up-to-date information and detailed specifications.
