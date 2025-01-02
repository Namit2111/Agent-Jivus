# HubSpot Custom Objects API Documentation

This document details the HubSpot Custom Objects API, allowing developers to create, manage, and interact with custom objects within their HubSpot accounts.

## Supported Products

Requires one of the following HubSpot products or higher:

* Marketing Hub - Enterprise
* Sales Hub - Enterprise
* Content Hub - Enterprise
* Service Hub - Enterprise
* Operations Hub - Enterprise


## Authentication

The API supports the following authentication methods:

* **OAuth:**  Standard OAuth 2.0 flow for secure access.
* **Private app access tokens:**  Generate tokens for your private app to access the API.

**Note:**  HubSpot API Keys are deprecated as of November 30, 2022.  Migrate to OAuth or private app access tokens.


##  Creating a Custom Object

This involves defining the object schema, including name, properties, and associations.

**1. Define Object Schema:**

   The schema defines the structure of your custom object.  It includes:

   * **`name` (string):**  The internal name of the object.  Must start with a letter and contain only letters, numbers, and underscores.  Cannot be changed after creation.
   * **`description` (string):**  A description of the object's purpose.
   * **`labels` (object):**  Singular and plural labels for the object.
   * **`primaryDisplayProperty` (string):** The property used to display the object's name.
   * **`secondaryDisplayProperties` (array of strings):** Additional properties displayed on the object's record view.  The first property listed, if it's a `string`, `number`, `enumeration`, `boolean`, or `datetime` type, will also be added as a fourth filter on the object index page.
   * **`searchableProperties` (array of strings):** Properties indexed for searching.
   * **`requiredProperties` (array of strings):**  Properties that are required when creating a new record.
   * **`properties` (array of objects):**  An array defining each property of the object.  See "Properties" section below for details.
   * **`associatedObjects` (array of strings):**  Standard HubSpot objects (e.g., `CONTACT`, `COMPANY`, `DEAL`, `TICKET`) or custom object `objectTypeId`s to associate with.

**2. Make API Call:**

   Send a `POST` request to `/crm/v3/schemas`:

   ```bash
   POST https://api.hubapi.com/crm/v3/schemas
   ```

   **Request Body (Example):**

   ```json
   {
     "name": "cars",
     "description": "Car inventory",
     "labels": {"singular": "Car", "plural": "Cars"},
     "primaryDisplayProperty": "model",
     "secondaryDisplayProperties": ["make"],
     "searchableProperties": ["year", "make", "vin", "model"],
     "requiredProperties": ["year", "make", "vin", "model"],
     "properties": [
       // ... property definitions (see Properties section) ...
     ],
     "associatedObjects": ["CONTACT"]
   }
   ```

   **Response:**  The API will return the created object schema, including its `objectTypeId`.

### Properties

| `type`       | Description                                      | Valid `fieldType` values              |
|---------------|--------------------------------------------------|---------------------------------------|
| `enumeration` | A set of options (semicolon-separated string)   | `booleancheckbox`, `checkbox`, `radio`, `select` |
| `date`        | ISO 8601 formatted date (YYYY-MM-DD)           | `date`                                 |
| `dateTime`    | ISO 8601 formatted date and time                | `date`                                 |
| `string`      | Plain text (up to 65,536 characters)          | `file`, `text`, `textarea`            |
| `number`      | Numeric value                                    | `number`                                |

### Field Types

| `fieldType`       | Description                                                                     |
|--------------------|---------------------------------------------------------------------------------|
| `booleancheckbox` | Single checkbox (Yes/No)                                                        |
| `checkbox`         | Multiple checkbox selections                                                     |
| `date`             | Date picker                                                                     |
| `file`             | File upload (stored as a URL)                                                  |
| `number`           | Numeric input                                                                    |
| `radio`            | Set of radio buttons                                                            |
| `select`           | Dropdown selection                                                               |
| `text`             | Single-line text input                                                          |
| `textarea`         | Multi-line text input                                                           |


## Retrieving Custom Objects

* **All Custom Objects:** `GET /crm/v3/schemas`
* **Specific Custom Object:**
    * `GET /crm/v3/schemas/{objectTypeId}` (using `objectTypeId` from schema creation)
    * `GET /crm/v3/schemas/p_{object_name}` (using object name)
    * `GET /crm/v3/schemas/{fullyQualifiedName}` (using `fullyQualifiedName` from schema)


## Retrieving Custom Object Records

* **Single Record:** `GET /crm/v3/objects/{objectType}/{recordId}`  (Include `properties`, `propertiesWithHistory`, `associations` query parameters as needed)
* **Multiple Records (batch):** `POST /crm/v3/objects/{objectType}/batch/read` (Request body specifies IDs or unique identifiers)  Associations are not supported in batch retrieval.

## Updating Custom Objects

* **Update Schema:** `PATCH /crm/v3/schemas/{objectTypeId}` (Update `requiredProperties`, `searchableProperties`, `primaryDisplayProperty`, `secondaryDisplayProperties`)
* **Update Associations:** `POST /crm/v3/schemas/{objectTypeId}/associations`


## Deleting a Custom Object

`DELETE /crm/v3/schemas/{objectType}` (requires all object instances to be deleted first)

To recreate an object with the same name, perform a hard delete:
`DELETE /crm/v3/schemas/{objectType}?archived=true` (requires all instances, associations, and properties to be deleted)


## Example Walkthrough: Creating a "Cars" Custom Object

This section provides a detailed example of creating a custom object, including creating records, associations, and properties.  The example demonstrates the API calls and request/response structures. (The provided text already contains this example).


##  Error Handling

The API returns standard HTTP status codes to indicate success or failure.  Error responses include details about the issue.


## Rate Limits

Be mindful of HubSpot's API rate limits to avoid throttling.


This documentation provides a comprehensive overview of the HubSpot Custom Objects API.  Refer to the official HubSpot API documentation for the most up-to-date information and details.
