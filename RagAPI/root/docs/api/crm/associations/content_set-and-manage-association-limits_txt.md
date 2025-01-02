# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 Associations endpoints.  This version supersedes the v3 API.  Refer to the v3 documentation for legacy integrations.

## Overview

The Associations API v4 manages relationships between records in the HubSpot CRM.  These associations can be between different object types (e.g., Contact to Company) or within the same object type (e.g., Company to Company).  The API is divided into two parts:

* **Association Endpoints:** Create, update, and delete associations between records.
* **Association Schema Endpoints:** Manage association definitions (types), custom labels, and association limits.

**Note:** The v4 Associations API requires HubSpot NodeJS Client version 9.0.0 or later.  The number of associations per record depends on the object type and your HubSpot subscription.


## Association Endpoints

### Associate Records

#### Without a Label (Default Association)

**Method:** `PUT`

**Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`

**Parameters:**

* `fromObjectType`: ID of the object being associated (e.g., `contact`, `company`).  See [Object Type IDs](#association-type-id-values)
* `fromObjectId`: ID of the record being associated.
* `toObjectType`: ID of the object the record is being associated *to*.  See [Object Type IDs](#association-type-id-values)
* `toObjectId`: ID of the record being associated to.

**Example:** Associate Contact (ID 12345) with Company (ID 67891):

`PUT /crm/v4/objects/contact/12345/associations/default/company/67891`

#### With a Label

**Method:** `PUT`

**Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`

**Request Body:**  An array of objects, each specifying an association label.

* `associationCategory`: `"HUBSPOT_DEFINED"` (for default labels) or `"USER_DEFINED"` (for custom labels).
* `associationTypeId`: Numerical ID of the label.  See [Object Type IDs](#association-type-id-values) and [Retrieve Association Labels](#retrieve-association-labels).

**Example:** Associate Contact with Deal using a custom label (typeId 36):

1. **GET `/crm/v4/associations/contact/deal/labels`** to retrieve the `typeId` for the custom label.
2. **PUT `/crm/v4/objects/contact/{objectId}/associations/deal/{toObjectId}`**

   ```json
   [
     {
       "associationCategory": "USER_DEFINED",
       "associationTypeId": 36
     }
   ]
   ```

**Example Response:**

```json
{
  "fromObjectTypeId": "0-1",
  "fromObjectId": 29851,
  "toObjectTypeId": "0-3",
  "toObjectId": 21678228008,
  "labels": ["Point of contact"]
}
```

#### Bulk Associate Records (Without Label)

**Method:** `POST`

**Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`

**Request Body:** Array of `objectId` values to associate.

#### Bulk Associate Records (With Label)

**Method:** `POST`

**Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`

**Request Body:** Array of association objects, each including `fromObjectId`, `toObjectId`, `associationCategory`, and `associationTypeId`.


### Retrieve Associated Records

#### Individual Record

**Method:** `GET`

**Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`

#### Bulk Records

**Method:** `POST`

**Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`

**Request Body:** Array of `id` values for records whose associations need retrieving.


**Example Request:**

```json
{
  "inputs": [
    {"id": "33451"},
    {"id": "29851"}
  ]
}
```

**Example Response:** (Illustrative, structure varies based on associations)

```json
{
  "status": "COMPLETE",
  "results": [
    // ... (results for each input ID) ...
  ]
}
```


### Update Record Association Labels

Use the bulk create endpoints (`POST /crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`) to update labels. To replace an existing label, only include the new label. To append, include both old and new labels.

### Remove Record Associations

#### Remove All Associations Between Two Records

**Method:** `DELETE`

**Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`

#### Bulk Remove All Associations

**Method:** `POST`

**Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`

**Request Body:** Array of objects, each specifying a `from` and `to` record to remove associations from.

#### Remove Specific Association Labels

**Method:** `POST`

**Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`

**Request Body:** Array of objects, each specifying the `from`, `to`, `associationCategory`, and `associationTypeId` of the label to remove.


## Association Schema Endpoints

These endpoints manage association definitions, custom labels, and limits.


### Create and Manage Association Types

**Method:** `POST` (create), `PUT` (update), `DELETE` (delete)

**Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`

**Request Body (Create):**

* `name`: Internal name (no hyphens, no leading numbers).
* `label`: Display name.
* `inverseLabel` (optional, for paired labels):  Name of the inverse label.

### Retrieve Association Labels

**Method:** `GET`

**Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`

### Update Association Labels

**Method:** `PUT`

**Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`

**Request Body:**

* `associationTypeId`: ID of the label to update.
* `label`: New label name.
* `inverseLabel` (optional, for paired labels): New inverse label name.


### Delete Association Labels

**Method:** `DELETE`

**Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`


### Set and Manage Association Limits

#### Create or Update Limits

**Method:** `POST`

**Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (create) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (update)

**Request Body:** Array of objects, each specifying:

* `category`: `"HUBSPOT_DEFINED"` or `"USER_DEFINED"`.
* `typeId`: ID of the association type.
* `maxToObjectIds`: Maximum number of associations allowed.

#### Retrieve Association Limits

**Method:** `GET`

**Endpoint:** `/crm/v4/associations/definitions/configurations/all` (all limits) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (limits between two objects)

#### Delete Association Limits

**Method:** `POST`

**Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`

**Request Body:** Array of objects, each specifying `category` and `typeId` of the limits to delete.


## Report on High Association Usage

**Method:** `POST`

**Endpoint:** `/crm/v4/associations/usage/high-usage-report/{userId}`

This endpoint sends a report of records nearing or exceeding association limits to the specified user's email.


## Association Type ID Values

See the provided table in the original text for a comprehensive list of `associationTypeId` values for various object types and association directions.


## Limitations

* **Daily Limits:**  Vary by HubSpot subscription (500,000 for Professional/Enterprise, potentially increased with API limit increase).
* **Burst Limits:**  Vary by HubSpot subscription (100/10 seconds for Free/Starter, 150/10 seconds for Professional/Enterprise, potentially increased with API limit increase).  Note that API limit increases don't affect the burst limit for the Associations API.


This markdown documentation provides a structured overview of the HubSpot CRM API v4 Associations. Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
