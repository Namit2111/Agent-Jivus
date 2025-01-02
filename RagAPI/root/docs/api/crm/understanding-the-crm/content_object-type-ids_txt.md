# HubSpot CRM APIs Documentation

This document provides an overview of the HubSpot CRM APIs, focusing on key concepts and functionalities.

## 1. Introduction

The HubSpot CRM is a database of business relationships and processes.  It uses *objects* to represent relationship/process types, and *records* as individual instances of those objects.  Data within records is stored using *properties*.  Relationships between records are managed via *associations*.  Processes are tracked using *pipelines*.

## 2. Core Concepts

* **Objects:** Represent types of relationships or processes (e.g., Contacts, Companies, Deals).  Each object has a unique `objectTypeId`.
* **Records:** Individual instances of an object (e.g., a specific contact, a specific deal). Each record has a unique `hs_object_id`.
* **Properties:** Fields within a record that store data (e.g., contact's email address, deal's value).  Default and custom properties exist.
* **Associations:** Links between records of different objects (e.g., associating a contact with a company).
* **Pipelines:**  Represent stages in a process (e.g., deal stages, ticket statuses).
* **Unique Identifiers:** Values that uniquely identify a record (e.g., `hs_object_id`, email for contacts, domain for companies).  Custom unique identifiers can also be created.


## 3. API Endpoints

HubSpot's CRM APIs provide access to various functionalities.  Many endpoints use the `objectTypeId` to specify the target object.

### 3.1 Object APIs

The Object APIs provide access to records and activities.  Endpoints generally follow this pattern: `/crm/v3/objects/{objectTypeId}`.

* **`POST /crm/v3/objects/{objectTypeId}`:** Create a new record.  Example: `POST /crm/v3/objects/0-1` (create a contact).
* **`GET /crm/v3/objects/{objectTypeId}`:** Retrieve records.
* **`PATCH /crm/v3/objects/{objectTypeId}/{recordId}`:** Update a record.  `recordId` can be `hs_object_id` or a custom unique identifier (using `idProperty` parameter).
* **Example:** To create a contact:

```json
POST /crm/v3/objects/0-1
{
  "properties": {
    "firstname": "John",
    "lastname": "Doe",
    "email": "john.doe@example.com"
  }
}
```

### 3.2 Object Type IDs

| Type ID | Object          | Description                                                              | API Reference                                      |
|---------|-----------------|--------------------------------------------------------------------------|---------------------------------------------------|
| 0-1     | Contacts        | Stores information about an individual person.                           | [Contacts API](link_to_contacts_api)            |
| 0-2     | Companies       | Stores information about a business or organization.                     | [Companies API](link_to_companies_api)           |
| 0-3     | Deals           | Represent sales opportunities.                                           | [Deals API](link_to_deals_api)                   |
| ...     | ...             | ...                                                                    | ...                                               |
| 2-XXX   | Custom Objects  | Stores custom data. `objectTypeId` retrieved via `GET /crm/v3/schemas`. | [Custom Objects API](link_to_custom_objects_api) |


### 3.3 Associations API

This API manages associations between records. Endpoints use `{fromObjectTypeId}` and `{toObjectTypeId}`.

* **`GET /crm/v4/associations/{fromObjectTypeId}/{toObjectTypeId}/labels`:** Retrieve association types.
* **`POST /crm/v4/associations/{fromObjectTypeId}/{toObjectTypeId}`:** Create an association.
* **`DELETE /crm/v4/associations/{fromObjectTypeId}/{toObjectTypeId}`:** Delete an association.


### 3.4 Properties API

This API manages properties for objects. Endpoints use `{objectTypeId}`.

* **`GET /crm/v3/properties/{objectTypeId}`:** Retrieve properties for an object.
* **`POST /crm/v3/properties/{objectTypeId}`:** Create a custom property.


### 3.5 Search API

This API allows searching for records based on properties and associations.  Endpoints use `{objectTypeId}`.

* **`POST /crm/v3/objects/{objectTypeId}/search`:** Perform a search.


### 3.6 Pipelines API

This API manages pipelines and stages.

* **`GET /pipelines/v3/pipelines/{objectTypeId}`:** Retrieve pipelines for an object.


## 4.  Error Handling

(Include details on how errors are returned by the API, including status codes and error messages.)

## 5. Rate Limits

(Include information about API rate limits and how to handle them.)


**(Replace placeholder links with actual links to relevant HubSpot API documentation.)**
