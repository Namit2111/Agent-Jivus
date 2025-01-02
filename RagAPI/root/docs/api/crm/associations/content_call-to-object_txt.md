# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 for managing associations between records.  Associations represent relationships between objects and activities within the HubSpot CRM.  This version builds upon the v3 API, offering improved functionality and performance.

## Key Concepts

* **Objects:**  Represent different data types in HubSpot (e.g., Contacts, Companies, Deals). Each object has a unique ID.
* **Records:** Individual entries within an object (e.g., a specific Contact record). Each record has a unique ID.
* **Associations:** Relationships between records, potentially across different objects.
* **Association Types (Definitions):** Define the type of relationship between objects (e.g., "Primary Company," "Manager," "Billing Contact").  These can be HubSpot-defined or custom-created.
* **Association Labels:** Human-readable descriptions of association types.  They can be single labels or paired labels (e.g., "Manager" and "Employee").
* **`associationTypeId`:** A unique numerical ID identifying a specific association type.
* **`associationCategory`:**  Indicates whether an association type is `HUBSPOT_DEFINED` or `USER_DEFINED`.

## API Endpoints

The v4 Associations API comprises two main endpoint categories:

**1. Association Endpoints:** Manage the creation, modification, and deletion of associations between records.

**2. Association Schema Endpoints:** Manage association definitions, custom labels, and association limits.


### I. Association Endpoints

#### A. Associate Records

* **Without a label (default):**
    * **Method:** `PUT`
    * **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
    * **Example:** `PUT /crm/v4/objects/contact/12345/associations/default/company/67891` (Associates contact 12345 with company 67891)
    * **Bulk:**
        * **Method:** `POST`
        * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
        * **Request Body:**  Array of `objectId` values.

* **With a label:**
    * **Method:** `PUT`
    * **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/{toObjectType}/{toObjectId}`
    * **Request Body:** Array of objects, each with `associationCategory` and `associationTypeId`.
    * **Bulk:**
        * **Method:** `POST`
        * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`
        * **Request Body:**  Array of objects, each specifying `fromObjectId`, `toObjectId`, and label details (`associationCategory`, `associationTypeId`).

#### B. Retrieve Associated Records

* **Individual record:**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`
* **Bulk:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
    * **Request Body:** Array of `id` values for records.

#### C. Update Record Association Labels

* Uses the same endpoints as associating records with labels (`PUT` and `POST` batch endpoints).  To replace labels, only provide the new label(s) in the request. To append, include both old and new labels.

#### D. Remove Record Associations

* **All associations between two records:**
    * **Method:** `DELETE`
    * **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
* **Bulk (all associations):**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`
    * **Request Body:** Array of objects, each specifying `from` and `to` record IDs.
* **Specific association labels:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
    * **Request Body:** Array of objects, each specifying `from`, `to`, `associationTypeId`, and `associationCategory`.


### II. Association Schema Endpoints

#### A. Create and Manage Association Types

* **Create:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
    * **Request Body:**  `name`, `label`, `inverseLabel` (for paired labels).

#### B. Retrieve Association Labels

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`

#### C. Update Association Labels

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:** `associationTypeId`, `label`, `inverseLabel` (optional, for paired labels).

#### D. Delete Association Labels

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`

#### E. Set and Manage Association Limits

* **Create/Update:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (create) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (update)
    * **Request Body:** Array of objects, each with `category`, `typeId`, and `maxToObjectIds`.

* **Retrieve:**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/all` (all limits) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (specific objects)

* **Delete:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
    * **Request Body:** Array of objects, each with `category` and `typeId`.


#### F. High Association Usage Report

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/usage/high-usage-report/{userId}`
* **Response:** A report sent via email to the specified user ID.


## Example Responses (Snippets shown in the original text are fully formatted here)


**Example Response: Associate Records with a Label (PUT request):**

```json
{
  "fromObjectTypeId": "0-1",
  "fromObjectId": 29851,
  "toObjectTypeId": "0-3",
  "toObjectId": 21678228008,
  "labels": ["Point of contact"]
}
```

**Example Response: Retrieve Associated Records (POST batch request):**

```json
{
  "status": "COMPLETE",
  "results": [
    {
      "from": {
        "id": "33451"
      },
      "to": [
        {
          "toObjectId": 5790939450,
          "associationTypes": [
            {
              "category": "HUBSPOT_DEFINED",
              "typeId": 1,
              "label": "Primary"
            },
            {
              "category": "HUBSPOT_DEFINED",
              "typeId": 279,
              "label": null
            },
            {
              "category": "USER_DEFINED",
              "typeId": 28,
              "label": "Billing contact"
            }
          ]
        }
      ]
    },
    {
      "from": {
        "id": "29851"
      },
      "to": [
        {
          "toObjectId": 5790939450,
          "associationTypes": [
            {
              "category": "HUBSPOT_DEFINED",
              "typeId": 1,
              "label": "Primary"
            },
            {
              "category": "USER_DEFINED",
              "typeId": 37,
              "label": "Chef"
            },
            {
              "category": "HUBSPOT_DEFINED",
              "typeId": 279,
              "label": null
            }
          ]
        },
        {
          "toObjectId": 6675245424,
          "associationTypes": [
            {
              "category": "HUBSPOT_DEFINED",
              "typeId": 279,
              "label": null
            }
          ]
        },
        {
          "toObjectId": 17705714757,
          "associationTypes": [
            {
              "category": "HUBSPOT_DEFINED",
              "typeId": 279,
              "label": null
            },
            {
              "category": "USER_DEFINED",
              "typeId": 30,
              "label": "Decision maker"
            }
          ]
        }
      ]
    }
  ],
  "startedAt": "2024-10-21T20:22:42.152Z",
  "completedAt": "2024-10-21T20:22:42.167Z"
}
```

**Example Response: Create Association Label (POST request):**

```json
{
  "results": [
    {
      "category": "USER_DEFINED",
      "typeId": 145,
      "label": "Employee"
    },
    {
      "category": "USER_DEFINED",
      "typeId": 144,
      "label": "Manager"
    }
  ]
}
```

**Example Response: Retrieve Association Labels (GET request):**

```json
{
  "results": [
    {
      "category": "HUBSPOT_DEFINED",
      "typeId": 1,
      "label": "Primary"
    },
    {
      "category": "USER_DEFINED",
      "typeId": 28,
      "label": "Billing contact"
    },
    {
      "category": "USER_DEFINED",
      "typeId": 142,
      "label": "Toy Tester"
    },
    {
      "category": "USER_DEFINED",
      "typeId": 26,
      "label": "Manager"
    },
    {
      "category": "USER_DEFINED",
      "typeId": 30,
      "label": "Decision maker"
    },
    {
      "category": "USER_DEFINED",
      "typeId": 37,
      "label": "Chef"
    },
    {
      "category": "USER_DEFINED",
      "typeId": 32,
      "label": "Contractor"
    },
    {
      "category": "HUBSPOT_DEFINED",
      "typeId": 279,
      "label": null
    }
  ]
}
```

**Example Response: Retrieve Association Limits (GET request):**

```json
{
  "results": [
    {
      "category": "HUBSPOT_DEFINED",
      "typeId": 3,
      "userEnforcedMaxToObjectIds": 5,
      "label": null
    }
  ]
}
```

##  Object Type IDs

The document provides extensive tables listing `typeId` values for various HubSpot-defined association types between different objects.  These tables are too large to reproduce here, but they are an integral part of the original document.  Refer to the original document for this critical information.

## Rate Limits

The API is subject to daily and burst rate limits, which vary depending on your HubSpot subscription plan.  Details on these limits are provided in the original document.


This comprehensive markdown documentation provides a clear overview of the HubSpot CRM API v4 for Associations, including key concepts, API endpoints, request/response examples, and important considerations such as rate limits and object type IDs. Remember to consult the original documentation for the complete tables of `typeId` values.
