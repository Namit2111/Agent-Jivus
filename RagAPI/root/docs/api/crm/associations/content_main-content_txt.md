# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 for managing record associations.  Associations represent relationships between objects and activities within the HubSpot CRM.  This version builds upon the previous v3 API.


## API Overview

The v4 Associations API consists of two main endpoint categories:

* **Association Endpoints:** Create, update, and delete associations between records.
* **Association Schema Endpoints:** Manage association definitions (types), custom labels, and association limits.

**Note:** The v4 API requires HubSpot NodeJS Client Version 9.0.0 or later. Association limits depend on the object type and your HubSpot subscription.

## Association Endpoints

These endpoints handle the creation and management of associations between records.


### Associate Records

#### Without a Label (Default Association)

**Method:** `PUT`

**Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`

**Parameters:**

* `fromObjectType`: ID of the object being associated (e.g., `contact`, `company`).  See [Object Type IDs](#object-type-ids) below.
* `fromObjectId`: ID of the record being associated.
* `toObjectType`: ID of the object the record is being associated *to*.
* `toObjectId`: ID of the record being associated to.

**Example:** Associate contact (ID 12345) with company (ID 67891):

`PUT /crm/v4/objects/contact/12345/associations/default/company/67891`

#### Without a Label (Bulk Association)

**Method:** `POST`

**Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`

**Request Body:**  Array of `objectId` values for records to associate.

**Example:** Associate multiple contacts with companies.

```json
POST /crm/v4/associations/contact/company/batch/associate/default
[
  "12345",
  "67890"
]
```


#### With a Label

**Method:** `PUT` (single association), `POST` (bulk association)

**Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/{toObjectType}/{toObjectId}` (single)
`/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create` (bulk)

**Parameters (Single):**  Same as above, plus request body.

**Request Body (Single & Bulk):** Array of objects, each with:

* `associationCategory`:  `"HUBSPOT_DEFINED"` (default) or `"USER_DEFINED"` (custom).
* `associationTypeId`: Numerical ID of the label. See [Association Type IDs](#object-type-ids) and [Retrieve Association Labels](#retrieve-association-labels).

**Example (Single):** Associate a contact with a deal using custom label (ID 36):

```json
PUT /crm/v4/objects/contact/12345/associations/deal/67890
[
  {
    "associationCategory": "USER_DEFINED",
    "associationTypeId": 36
  }
]
```

**Example Response (Single):**

```json
{
  "fromObjectTypeId": "0-1",
  "fromObjectId": 29851,
  "toObjectTypeId": "0-3",
  "toObjectId": 21678228008,
  "labels": ["Point of contact"]
}
```

**Example (Bulk):**  Associate multiple contacts with companies.  Omitted for brevity.


### Retrieve Associated Records

#### Single Record

**Method:** `GET`

**Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`

**Parameters:**

* `fromObjectType`: Object type of the record.
* `objectId`: ID of the record.
* `toObjectType`: Object type of associated records to retrieve.

#### Bulk Records

**Method:** `POST`

**Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`

**Request Body:** Array of `id` values for records.

**Example:** Get all company associations for two contacts:

```json
POST /crm/v4/associations/contact/company/batch/read
{
  "inputs": [
    {"id": "33451"},
    {"id": "29851"}
  ]
}
```

**Example Response (Bulk):**  See detailed example in original text.


### Update Record Association Labels

Use the same `PUT` (single) or `POST` (bulk) create endpoints. To replace an existing label, provide only the new label. To append, include all labels.

### Remove Record Associations

#### Remove All Associations

**Method:** `DELETE` (single), `POST` (bulk)

**Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}` (single)
`/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive` (bulk)

#### Remove Specific Association Labels

**Method:** `POST`

**Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`

**Request Body:** Array of objects, each with `from`, `to`, and an array of `types` (each containing `associationCategory` and `associationTypeId`).


## Association Schema Endpoints

These endpoints manage association definitions, labels, and limits.


### Understand Association Definitions, Configurations, and Labels

This section covers managing association types, labels, and limits.


### HubSpot Defined Associations

HubSpot provides predefined association types (e.g., unlabeled contact to company) and two key types:

* **Primary:** The main association.
* **Unlabeled:** A default association, always returned with `label: null`.


### Custom Association Labels

Create custom labels to add context to relationships.

#### Create Association Labels

**Method:** `POST`

**Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`

**Request Body:**

* `name`: Internal name (no hyphens, cannot start with a number).
* `label`: Display name.
* `inverseLabel` (optional, for paired labels): Second label in the pair.

#### Retrieve Association Labels

**Method:** `GET`

**Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`

#### Update Association Labels

**Method:** `PUT`

**Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`

#### Delete Association Labels

**Method:** `DELETE`

**Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`


### Set and Manage Association Limits

#### Create or Update Association Limits

**Method:** `POST`

**Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (create)
`/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (update)

**Request Body:** Array of objects, each with `category`, `typeId`, and `maxToObjectIds`.

#### Retrieve Association Limits

**Method:** `GET`

**Endpoint:** `/crm/v4/associations/definitions/configurations/all` (all limits)
`/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (specific objects)

#### Delete Association Limits

**Method:** `POST`

**Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`


## Limitations

* **Daily Limits:**  Vary by subscription (Professional/Enterprise: 500,000, with API limit increase: 1,000,000).
* **Burst Limits:** Vary by subscription (Free/Starter: 100/10s, Professional/Enterprise: 150/10s, with API limit increase: 200/10s).


## Object Type IDs

See detailed table of `associationTypeId` values for different object pairings in the original document.  Note that these IDs vary based on the object types and the direction of the association.

## Report on High Association Usage

**Method:** `POST`

**Endpoint:** `/crm/v4/associations/usage/high-usage-report/{userId}`

This endpoint sends a report of records nearing or exceeding their association limits to the specified user's email.


This comprehensive documentation provides a detailed overview of the HubSpot CRM API v4 for Associations. Remember to consult the official HubSpot API documentation for the most up-to-date information and any changes.
