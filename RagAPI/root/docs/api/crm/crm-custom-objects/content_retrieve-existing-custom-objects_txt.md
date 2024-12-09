# HubSpot Custom Objects API Documentation

This document details how to create, manage, and interact with custom objects within the HubSpot CRM using their API.  Custom objects extend the standard CRM objects (contacts, companies, deals, tickets) to represent your unique business data.

## Supported Products

Requires one of the following HubSpot products or higher:

* Marketing Hub - Enterprise
* Sales Hub - Enterprise
* Content Hub - Enterprise
* Service Hub - Enterprise
* Operations Hub - Enterprise


## Authentication

Use one of the following authentication methods:

* OAuth
* Private app access tokens

**Note:** HubSpot API Keys are deprecated as of November 30, 2022.  Migrate to OAuth or private app access tokens.  [Learn more about this change](link_to_migration_guide) and how to [migrate an API key integration](link_to_migration_guide).


## Creating a Custom Object

1. **Define the Object Schema:**  The schema defines the object's name, properties, and associations with other CRM objects.

   *   **Endpoint:** `POST /crm/v3/schemas`
   *   **Request Body:**  Includes `name`, `description`, `labels` (singular and plural), `properties`, `associatedObjects`, `primaryDisplayProperty`, `secondaryDisplayProperties`, `searchableProperties`, and `requiredProperties`.

   * **Naming Conventions:**
      * Object name and label cannot be changed after creation.
      * Name can only contain letters, numbers, and underscores.
      * The first character of the name must be a letter.
      * Long labels may be truncated in the UI.


2. **Properties:** Define properties to store information within custom object records.

   *   **Limit:** Up to 10 unique value properties per custom object.
   *   **Property Types:**
      | `type`        | Description                                      | Valid `fieldType` Values             |
      |---------------|--------------------------------------------------|--------------------------------------|
      | `enumeration` | A string representing a set of options (semicolon-separated) | `booleancheckbox`, `checkbox`, `radio`, `select` |
      | `date`        | ISO 8601 formatted date (YYYY-MM-DD)             | `date`                               |
      | `dateTime`    | ISO 8601 formatted date and time (YYYY-MM-DDTHH:mm:ssZ) | `date`                               |
      | `string`      | Plain text string (up to 65,536 characters)     | `file`, `text`, `textarea`             |
      | `number`      | Numeric value                                     | `number`                              |

   *   **`fieldType` Descriptions:**
      * `booleancheckbox`: Single checkbox (Yes/No).
      * `checkbox`: Multiple checkboxes.
      * `date`: Date picker.
      * `file`: File upload (stored as a URL).
      * `number`: Numeric input.
      * `radio`: Radio buttons.
      * `select`: Dropdown.
      * `text`: Single-line text input.
      * `textarea`: Multi-line text input.

3. **Associations:**  Associate your custom object with standard HubSpot objects (contacts, companies, deals, tickets) or other custom objects.  HubSpot automatically associates custom objects with emails, meetings, notes, tasks, calls, and conversations.

   *   Identify standard objects by name.
   *   Identify custom objects using their `objectTypeId`.


## Retrieving Custom Objects

* **All Custom Objects:** `GET /crm/v3/schemas`
* **Specific Custom Object:**
    * `GET /crm/v3/schemas/{objectTypeId}`
    * `GET /crm/v3/schemas/p_{object_name}`
    * `GET /crm/v3/schemas/{fullyQualifiedName}`  (derived from `p{portal_id}_{object_name}`)


## Retrieving Custom Object Records

* **Single Record:** `GET /crm/v3/objects/{objectType}/{recordId}`  (Use query parameters `properties`, `propertiesWithHistory`, `associations`)
* **Multiple Records:** `POST /crm/v3/objects/{objectType}/batch/read` (cannot retrieve associations; use the Associations API for batch association reads).  Retrieve by `hs_object_id` (default) or a custom unique identifier property (using the `idProperty` parameter).


## Updating Custom Objects

* **Update Schema:** `PATCH /crm/v3/schemas/{objectTypeId}` (Object name and labels cannot be changed).
* **Update Associations:** `POST /crm/v3/schemas/{objectTypeId}/associations`


## Deleting Custom Objects

* **Delete Custom Object:** `DELETE /crm/v3/schemas/{objectType}` (Requires all object instances and associations to be deleted first).
* **Hard Delete Schema:** `DELETE /crm/v3/schemas/{objectType}?archived=true` (Allows recreating an object with the same name).


## Example: Creating a "Cars" Custom Object

This section provides a detailed walkthrough of creating a "Cars" custom object, including creating records, associations, and properties.  (The example code snippets from the original text are included here as well)


## Feedback

[Link to Feedback Form]


This markdown documentation provides a structured and readable overview of the HubSpot Custom Objects API.  Remember to replace placeholder links like `link_to_migration_guide` with actual links to relevant HubSpot documentation.
