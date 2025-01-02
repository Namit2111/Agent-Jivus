# HubSpot Custom Objects API Documentation

This document details the HubSpot API for creating, managing, and interacting with custom objects.  Custom objects extend the standard HubSpot CRM (Contacts, Companies, Deals, Tickets) to represent your specific business needs.

## Supported Products

This API requires one of the following HubSpot products (Enterprise tier or higher):

* Marketing Hub
* Sales Hub
* Content Hub
* Service Hub
* Operations Hub


## Authentication

You can access the API using:

* **OAuth:**  Recommended for most integrations.
* **Private app access tokens:** Suitable for internal applications.

**Note:** HubSpot API Keys are deprecated as of November 30, 2022.  Migrate existing integrations to OAuth or private app access tokens.


## API Endpoints

All endpoints are under the base URL: `https://api.hubapi.com/crm/v3/`

### 1. Create a Custom Object

**Endpoint:** `/schemas`
**Method:** `POST`

**Request Body:**  Requires a JSON payload defining the object schema. This includes:

* `name`:  (String) The object's name (cannot be changed after creation). Must start with a letter and only contain letters, numbers, and underscores.
* `description`: (String) Description of the object.
* `labels`: (Object)  `singular` and `plural` labels for the object.
* `primaryDisplayProperty`: (String) Property used to display object records.
* `secondaryDisplayProperties`: (Array of Strings) Additional properties displayed on individual records. The first property listed here will be added as a fourth filter on the object index page (if it's a string, number, enumeration, boolean, or datetime type).
* `searchableProperties`: (Array of Strings) Properties indexed for search.
* `requiredProperties`: (Array of Strings) Properties required when creating new records.
* `properties`: (Array of Objects)  Definition of each property (see below).
* `associatedObjects`: (Array of Strings)  IDs of associated standard or custom objects (see below).


**Property Definition (within `properties` array):**

| Field          | Type     | Description                                                                      | `fieldType` Options                     |
|-----------------|----------|----------------------------------------------------------------------------------|------------------------------------------|
| `name`          | String   | Property name (unique within the object).                                          |                                          |
| `label`         | String   | Property label.                                                                   |                                          |
| `type`          | String   | Property type (`string`, `number`, `date`, `dateTime`, `enumeration`, `boolean`) |                                          |
| `fieldType`     | String   | UI field type (`text`, `textarea`, `number`, `date`, `checkbox`, `radio`, `select`, `file`) |  Dependent on `type`                     |
| `options`       | Array    | (For `enumeration` type) Array of `{label: string, value: string}` objects.      |                                          |
| `hasUniqueValue`| Boolean  | (Optional) True if the property should have unique values.                      |                                          |


**Associated Object IDs:**

* Standard Objects: Use the object name (e.g., "CONTACT", "COMPANY", "DEAL", "TICKET").
* Custom Objects: Use the `objectTypeId` value.


**Example Request:** (See the provided example in the original text)

**Example Response:** (Contains the newly created object's `objectTypeId` and other metadata)


### 2. Retrieve Existing Custom Objects

**Endpoint:** `/schemas`
**Method:** `GET`  (Retrieves all custom objects)

**Endpoint:** `/schemas/{objectTypeId}` or `/schemas/p_{object_name}` or `/schemas/{fullyQualifiedName}`
**Method:** `GET` (Retrieves a specific custom object)

* `{objectTypeId}`: The unique ID of the custom object.
* `{object_name}`: The name of the custom object.
* `{fullyQualifiedName}`:  `p{portal_id}_{object_name}` (Portal ID can be retrieved via the account information API)

**Example Response:** (JSON representation of the custom object schema)



### 3. Retrieve Custom Object Records

**Endpoint:** `/objects/{objectType}/{recordId}`
**Method:** `GET` (Retrieves a single record)

* `{objectType}`: The `objectTypeId` of the custom object.
* `{recordId}`: The ID of the record.

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `propertiesWithHistory`: Comma-separated list of properties to return (including history).
* `associations`: Comma-separated list of associated objects to retrieve IDs for.


**Endpoint:** `/objects/{objectType}/batch/read`
**Method:** `POST` (Retrieves multiple records)

**Request Body:**  JSON payload with:

* `properties`:  (Array of Strings) Properties to return.
* `propertiesWithHistory`: (Array of Strings) Properties to return (including history).
* `idProperty`: (String, optional)  Name of a unique identifier property (if not using `hs_object_id`).
* `inputs`: (Array of Objects) Array of `{id: string}` objects, where `id` is the record ID or unique identifier value.

**Example Request & Response:** (See examples in original text)


### 4. Update Existing Custom Objects

**Endpoint:** `/schemas/{objectTypeId}`
**Method:** `PATCH`

**Request Body:** JSON payload with properties to update (e.g., `searchableProperties`, `requiredProperties`, `secondaryDisplayProperties`).  You cannot change the object's name or labels.


### 5. Update Associations

**Endpoint:** `/schemas/{objectTypeId}/associations`
**Method:** `POST` (Add new associations)

**Request Body:**

* `fromObjectTypeId`:  ID of the custom object.
* `toObjectTypeId`: ID of the associated object (standard object name or custom object `objectTypeId`).
* `name`: Name of the association.


### 6. Delete a Custom Object

**Endpoint:** `/schemas/{objectType}`
**Method:** `DELETE` (Soft delete – object is archived, but data remains)

**Endpoint:** `/schemas/{objectType}?archived=true`
**Method:** `DELETE` (Hard delete – permanently removes the object and its data)


## Example Walkthrough (CarSpot Scenario)

The original text provides a detailed walkthrough of creating a "Cars" custom object, including creating properties, associations, and records.  Refer to that section for a step-by-step example.


## Rate Limits

HubSpot APIs have rate limits.  Refer to the HubSpot API documentation for details on your account's limits.


This markdown documentation provides a structured overview of the HubSpot Custom Objects API.  Always refer to the official HubSpot API documentation for the most up-to-date information and details.
