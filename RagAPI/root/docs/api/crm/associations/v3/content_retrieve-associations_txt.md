# HubSpot CRM API: Associations v3

This document describes the HubSpot CRM v3 Associations API, which allows you to manage relationships between objects in the HubSpot CRM.  Note that the v4 API offers extended functionality, including label management; refer to the v4 documentation for those features.

## Understanding Associations

Associations represent relationships between different HubSpot CRM objects (e.g., Contacts, Companies, Deals).  They are unidirectional, meaning you need to specify the `fromObjectType` and `toObjectType` to define the direction of the association.


## API Endpoints

All endpoints are located under the `/crm/v3/associations` base path and utilize HTTP methods as described below.  Remember to replace placeholders like `{fromObjectType}` and `{toObjectType}` with the actual object types (e.g., `Contacts`, `Companies`, `Deals`).  These are case-sensitive.

**Note:**  When retrieving associations with companies (`/crm/v3/associations/{fromObjectType}/companies/batch/read`), only the *primary* associated company will be returned. Use the v4 API for all associated companies.


### 1. Retrieve Association Types

* **Method:** `GET`
* **Endpoint:** `/crm/v3/associations/{fromObjectType}/{toObjectType}/types`
* **Description:** Retrieves all defined association types between two specified object types, including default and custom labels (though you cannot create or edit labels via v3).
* **Example Request:**
  ```bash
  GET /crm/v3/associations/contacts/companies/types
  ```
* **Example Response:**
  ```json
  {
    "results": [
      {
        "id": "136",
        "name": "franchise_owner_franchise_location"
      },
      {
        "id": "26",
        "name": "manager"
      },
      {
        "id": "1",
        "name": "contact_to_company"
      },
      // ... more association types
    ]
  }
  ```
  The `id` field represents the numerical identifier for the association type.  For custom labels, this ID is account-specific.


### 2. Create Associations

* **Method:** `POST`
* **Endpoint:** `/crm/v3/associations/{fromObjectType}/{toObjectType}/batch/create`
* **Description:** Creates multiple associations between records of two specified object types.
* **Request Body:**  An array of objects, each specifying the `from` and `to` object IDs and the `type` of association.
* **Example Request:**
  ```json
  {
    "inputs": [
      {
        "from": {
          "id": "53628"
        },
        "to": {
          "id": "12726"
        },
        "type": "contact_to_company"
      }
    ]
  }
  ```


### 3. Retrieve Associations

* **Method:** `POST`
* **Endpoint:** `/crm/v3/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Description:** Retrieves associations for a batch of records of the `fromObjectType`.
* **Request Body:** An array of `id` values for the records whose associations you want to retrieve.
* **Example Request:**
  ```json
  {
    "inputs": [
      {
        "id": "5790939450"
      },
      {
        "id": "6108662573"
      }
    ]
  }
  ```
* **Example Response:**
  ```json
  {
    "status": "COMPLETE",
    "results": [
      {
        "from": {
          "id": "5790939450"
        },
        "to": [
          {
            "id": "1467822235",
            "type": "company_to_deal"
          },
          // ... more associated records
        ]
      },
      // ... more results for other input IDs
    ],
    "startedAt": "2024-10-21T16:40:47.810Z",
    "completedAt": "2024-10-21T16:40:47.833Z"
  }
  ```


### 4. Remove Associations

* **Method:** `POST`
* **Endpoint:** `/crm/v3/associations/{fromObjectType}/{toObjectType}/batch/archive`
* **Description:** Removes multiple associations between records.
* **Request Body:** An array of objects, each specifying the `from` and `to` object IDs and the `type` of association to remove.
* **Example Request:**
  ```json
  {
    "inputs": [
      {
        "from": {
          "id": "5790939450"
        },
        "to": {
          "id": "21678228008"
        },
        "type": "company_to_deal"
      }
    ]
  }
  ```


## Error Handling

The API will return standard HTTP status codes to indicate success or failure.  Detailed error messages will be included in the response body for failed requests.


## Rate Limits

Be mindful of HubSpot's API rate limits to avoid exceeding allowed request frequency.


This documentation provides a concise overview.  Always refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications.
