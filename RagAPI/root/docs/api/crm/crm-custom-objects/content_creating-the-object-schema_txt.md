# HubSpot Custom Objects API Documentation

This document details the HubSpot API for creating, managing, and interacting with custom objects.  Custom objects extend the standard HubSpot CRM objects (contacts, companies, deals, tickets) to represent your unique business data.

## Supported Products

Requires one of the following HubSpot products or higher:

* Marketing Hub - Enterprise
* Sales Hub - Enterprise
* Content Hub - Enterprise
* Service Hub - Enterprise
* Operations Hub - Enterprise


## Getting Started

In addition to the standard CRM objects, you can create custom objects to represent and organize your CRM data. You can create custom objects in the HubSpot UI or use the custom objects API.  This document focuses on the API.

**Authentication Methods:**

* OAuth
* Private app access tokens  (HubSpot API Keys are deprecated as of November 30, 2022).  [Learn more about migrating from API Keys](link-to-migration-guide-needed)


## Custom Object Management

### Creating a Custom Object

1. **Define the Object Schema:** The schema includes the object's name, properties, and associations with other CRM objects.  A `POST` request to `/crm/v3/schemas` is used.

    * **Object Name:**  Must start with a letter, contain only letters, numbers, and underscores.  Cannot be changed after creation. Long labels may be truncated.
    * **Properties:**  Up to 10 unique value properties are allowed per custom object.  Properties have `type` (string, number, enumeration, date, dateTime, boolean) and `fieldType` (text, textarea, number, date, file, booleancheckbox, checkbox, radio, select) attributes.  Define `requiredProperties`, `searchableProperties`, `primaryDisplayProperty`, and `secondaryDisplayProperties`.  The first property in `secondaryDisplayProperties` (if string, number, enumeration, boolean, or datetime) will appear as a fourth filter on the object index page.
    * **Associations:**  Automatically associated with emails, meetings, notes, tasks, calls, and conversations.  You can add associations to other standard objects or custom objects using their `objectTypeId` (for custom objects) or name (for standard objects).


2. **`POST` Request to `/crm/v3/schemas`:** Submit the object schema definition in the request body.  See the [Custom Object Example](#custom-object-example) for a sample request.


### Retrieving Existing Custom Objects

* **All Custom Objects:** `GET` request to `/crm/v3/schemas`.
* **Specific Custom Object:** `GET` request to one of the following:
    * `/crm/v3/schemas/{objectTypeId}`
    * `/crm/v3/schemas/p_{object_name}`
    * `/crm/v3/schemas/{fullyQualifiedName}` (derived from `p{portal_id}_{object_name}`)

### Retrieving Custom Object Records

* **Specific Record:** `GET` request to `/crm/v3/objects/{objectType}/{recordId}`.  Use query parameters `properties`, `propertiesWithHistory`, and `associations`.
* **Multiple Records:** `POST` request to `/crm/v3/objects/{objectType}/batch/read`.  This endpoint does *not* support retrieving associations.  Retrieve records by `hs_object_id` (record ID) or a custom unique identifier property (using the `idProperty` parameter).


### Updating Existing Custom Objects

* **Update Schema:** `PATCH` request to `/crm/v3/schemas/{objectTypeId}`.  Object name and labels cannot be changed.  You can modify `requiredProperties`, `searchableProperties`, `primaryDisplayProperty`, and `secondaryDisplayProperties`.  New properties must be created before being added to the schema.


### Updating Associations

* **Add Associations:** `POST` request to `/crm/v3/schemas/{objectTypeId}/associations`.  Specify `fromObjectTypeId`, `toObjectTypeId`, and `name`.


### Deleting a Custom Object

* **Delete Custom Object:** `DELETE` request to `/crm/v3/schemas/{objectType}`.  All object instances, associations, and properties must be deleted first.
* **Hard Delete (for recreating with same name):** `DELETE` request to `/crm/v3/schemas/{objectType}?archived=true`.


## Custom Object Example

This walkthrough demonstrates creating a "Cars" custom object for a car dealership:

### Creating the Object Schema

A `POST` request to `/crm/v3/schemas` with a JSON body defining properties like `condition`, `date_received`, `year`, `make`, `model`, `vin` (unique), `color`, `mileage`, `price`, and `notes`, along with associations to `CONTACT` is used.  (See the provided example code snippet in the original text).

### Creating a Custom Object Record

A `POST` request to `/crm/v3/objects/{objectTypeId}` with a JSON body containing property values for a specific car. (See the provided example code snippet in the original text).


### Associating the Custom Object Record to Another Record

A `PUT` request to `/crm/v3/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}/{associationType}` associates a car record with a contact record.


### Defining a New Association

A `POST` request to `/crm/v3/schemas/{objectTypeId}/associations` creates an association between the "Cars" object and "Tickets" for tracking maintenance. (See the provided example code snippet in the original text).


### Defining a New Property

A `POST` request to `/crm/v3/properties/{objectTypeId}` adds a "maintenance_package" property. (See the provided example code snippet in the original text).


### Updating the Object Schema

A `PATCH` request to `/crm/v3/schemas/{objectTypeId}` adds the new property to `secondaryDisplayProperties` to show it in the sidebar. (See the provided example code snippet in the original text).


This example illustrates the API's capabilities for building and managing custom objects within HubSpot.  Remember to replace placeholders like `{objectTypeId}` with your actual values.  Refer to the original text for complete code examples.
