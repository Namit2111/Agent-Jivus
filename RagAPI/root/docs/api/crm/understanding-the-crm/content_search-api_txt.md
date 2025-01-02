# HubSpot CRM APIs Documentation

This document provides an overview of the HubSpot CRM APIs, enabling developers to interact with HubSpot's customer relationship management database.

## I. Core Concepts

* **Objects:** Represent types of relationships or processes within HubSpot (e.g., Contacts, Companies, Deals).
* **Records:** Individual instances of an object (e.g., a specific contact, a specific company).
* **Properties:** Fields within records that store data (e.g., email address, company name).  HubSpot provides default properties, and custom properties can be created.
* **Associations:** Relationships between records of different objects (e.g., associating a contact with a company).
* **Pipelines:**  Represent stages in a process (e.g., sales pipeline stages for deals, support statuses for tickets).
* **Object Type IDs:** Unique numerical identifiers for each object type (e.g., `0-1` for Contacts, `0-2` for Companies).  These IDs are crucial for API interactions.

## II. API Endpoints and Usage

All CRM API endpoints generally follow the pattern `/crm/v3/...`.

### A. Object APIs

Provide access to records and activities.  The `objectTypeId` is a key component of most requests.

* **Endpoint:** `/crm/v3/objects/{objectTypeId}`
* **Methods:** `GET`, `POST`, `PATCH`, `DELETE` (depending on the object and its functionality)
* **Example (Creating a Contact):**
    ```bash
    POST /crm/v3/objects/0-1
    {
      "properties": {
        "email": "john.doe@example.com",
        "firstname": "John",
        "lastname": "Doe"
      }
    }
    ```
* **Response:**  A JSON object containing the created record's details, including its `hs_object_id`.

**Object Type IDs:**

| Type ID | Object           | Description                                                              | API Reference                  |
|---------|-------------------|--------------------------------------------------------------------------|---------------------------------|
| 0-2     | Companies         | Stores information about businesses.                                    | [Companies API](link_to_companies_api) |
| 0-1     | Contacts          | Stores information about individuals.                                     | [Contacts API](link_to_contacts_api)  |
| 0-3     | Deals             | Represents sales opportunities.                                          | [Deals API](link_to_deals_api)      |
| 0-5     | Tickets           | Represents customer support requests.                                    | [Tickets API](link_to_tickets_api)    |
| ...     | ...               | ...                                                                     | ...                             |
| 2-XXX   | Custom Objects    | Stores custom data.  `objectTypeId` obtained via `/crm/v3/schemas` GET request. | [Custom Objects API](link_to_custom_objects_api) |


*(Replace `link_to_..._api` with actual links to API documentation)*

### B. Associations API

Manages relationships between records.

* **Endpoint:** `/crm/v4/associations/{fromObjectTypeId}/{toObjectTypeId}/[labels]`
* **Methods:** `GET`, `POST`, `DELETE`
* **Example (Associating a Contact with a Company):**
    ```bash
    POST /crm/v4/associations/0-1/0-2
    {
      "associations": [
        {
          "from": "123",  // Contact hs_object_id
          "to": "456"   // Company hs_object_id
        }
      ]
    }
    ```
* **Response:**  Confirmation of association creation or deletion.


### C. Properties API

Manages object properties (default and custom).

* **Endpoint:** `/crm/v3/properties/{objectTypeId}`
* **Methods:** `GET`, `POST`, `PATCH`, `DELETE`
* **Example (Creating a custom property for Contacts):**
    ```bash
    POST /crm/v3/properties/0-1
    {
      "name": "custom_property",
      "label": "Custom Property",
      "type": "string",
      // ...other property details
    }
    ```
* **Response:**  Details of the newly created property.

### D. Search API

Searches for records and activities based on properties and associations.

* **Endpoint:** `/crm/v3/objects/{objectTypeId}/search`
* **Method:** `POST`
* **Example (Searching for calls):**
   ```bash
   POST /crm/v3/objects/0-48/search
   {
     "filterGroups": [
       {
         "filters": [
           {
             "propertyName": "subject",
             "operator": "EQ",
             "value": "Sales Call"
           }
         ]
       }
     ]
   }
   ```
* **Response:** A list of matching records.

### E. Pipelines API

Manages pipelines and pipeline stages.

* **Endpoint (example for deals):** `/crm/v3/pipelines/deals`
* **Methods:** `GET`, `POST`, `PATCH`, `DELETE` (Specific methods depend on the endpoint.)

### F. Unique Identifiers and Record IDs

* `hs_object_id`: Automatically generated unique identifier for each record.  Treated as a string.
* Custom Unique Identifiers:  Can be created for specific objects using custom properties.  These can be used in certain API calls via the `idProperty` parameter.


## III.  Error Handling

The APIs return standard HTTP status codes to indicate success or failure.  Error responses typically contain JSON payloads with details about the error.


This documentation provides a high-level overview.  Refer to the official HubSpot API documentation for detailed information on each endpoint, request parameters, and response formats. Remember to replace placeholder values (e.g., `objectTypeId`, `hs_object_id`) with actual values.
