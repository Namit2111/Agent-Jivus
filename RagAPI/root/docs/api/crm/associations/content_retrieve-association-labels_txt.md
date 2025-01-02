# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 for managing record associations.  Associations represent relationships between objects (e.g., Contact to Company) and activities within the HubSpot CRM.  This version offers both association endpoints (for creating, editing, and removing associations) and association schema endpoints (for managing association definitions, labels, and limits).

**Note:** The v4 Associations API requires HubSpot NodeJS Client version 9.0.0 or later.  Association limits depend on the object and your HubSpot subscription.

## I. Association Endpoints

These endpoints manage the associations themselves.

### A. Associate Records

#### 1. Associate Records Without a Label

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Parameters:**
    * `fromObjectType`: ID of the source object (e.g., `contact`, `company`). See [Object Type IDs](#object-type-ids)
    * `fromObjectId`: ID of the source record.
    * `toObjectType`: ID of the target object. See [Object Type IDs](#object-type-ids)
    * `toObjectId`: ID of the target record.
* **Example:** Associate contact (ID 12345) with company (ID 67891):
    `/crm/v4/objects/contact/12345/associations/default/company/67891`

#### 2. Bulk Associate Records Without a Label

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
* **Request Body:** Array of `objectId` values for records to associate.
* **Example:** (see below for example JSON)

#### 3. Associate Records With a Label

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body:** Array of objects, each with:
    * `associationCategory`: `HUBSPOT_DEFINED` or `USER_DEFINED`
    * `associationTypeId`: Numerical ID of the label.  Retrieve this using the `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels` endpoint.
* **Example:** (see below for example JSON)

#### 4. Bulk Create Labeled Associations

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`
* **Request Body:**  Array of objects, each specifying record IDs and label details (`associationCategory`, `associationTypeId`).
* **Example:** (see below for example JSON)

### B. Retrieve Associated Records

#### 1. Retrieve Individual Record's Associations

* **Method:** `GET`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`
* **Parameters:**
    * `fromObjectType`: ID of the source object.
    * `objectId`: ID of the source record.
    * `toObjectType`: ID of the target object.

#### 2. Bulk Retrieve Associated Records

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Request Body:** Array of `{id: recordId}` objects.
* **Example:** (see below for example JSON)


### C. Update Record Association Labels

* Uses the same endpoints as association creation (PUT and POST batch endpoints), but replaces or appends labels.  Existing associations are updated, not created anew.

### D. Remove Record Associations

#### 1. Remove All Associations Between Two Records

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`

#### 2. Bulk Remove All Associations

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`
* **Request Body:** Array of `{from: {id: fromId}, to: [{id: toId}]}` objects.
* **Example:** (see below for example JSON)

#### 3. Remove Specific Association Labels

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
* **Request Body:** Array of objects, each with `types`, `from`, and `to` containing `associationTypeId`, `category`, and record IDs.
* **Example:** (see below for example JSON)


## II. Association Schema Endpoints

These endpoints manage the definitions and configurations of associations.


### A. Understand Association Definitions, Configurations, and Labels

This section covers managing association types, labels, and limits.

### B. HubSpot Defined Associations

HubSpot provides predefined association types: `Primary` (main association) and `Unlabeled`.

### C. Custom Association Labels

Create custom labels to add context to relationships (e.g., "Manager", "Employee").  There are two types: `Single` and `Paired`.

### D. Create and Manage Association Types

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:**
    * `name`: Internal name (no hyphens, no leading numbers).
    * `label`: Display name in HubSpot.
    * `inverseLabel` (optional, for paired labels): Second label in the pair.
* **Example:** (see below for example JSON)

### E. Retrieve Association Labels

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Returns:** Array of association type information (`category`, `typeId`, `label`).

### F. Update Association Labels

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:** `associationTypeId` and new `label` (and `inverseLabel` if paired).
* **Example:** (see below for example JSON)


### G. Delete Association Labels

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`


### H. Set and Manage Association Limits

#### 1. Create or Update Association Limits

* **Method:** `POST`
* **Endpoints:**
    * Create: `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create`
    * Update: `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update`
* **Request Body:** `inputs` array with: `category`, `typeId`, `maxToObjectIds`.
* **Example:** (see below for example JSON)


#### 2. Retrieve Association Limits

* **Method:** `GET`
* **Endpoints:**
    * All limits: `/crm/v4/associations/definitions/configurations/all`
    * Specific objects: `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}`


#### 3. Delete Association Limits

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
* **Request Body:** `inputs` array with `category` and `typeId`.
* **Example:** (see below for example JSON)


## III.  Limitations

* **Daily Limits:**  500,000 requests (Professional/Enterprise), potentially increased with API limit increase purchase (maximum 1,000,000).
* **Burst Limits:** 100 requests/10 seconds (Free/Starter), 150 requests/10 seconds (Professional/Enterprise), potentially increased with API limit increase purchase (maximum 200 requests/10 seconds).


## IV. Object Type IDs

See the provided table in the original text for a comprehensive list of `typeId` values for different object types and association directions.

## V. Example JSON Request/Response Bodies


**Bulk Associate Records Without Label (POST):**

```json
{
  "inputs": [12345, 67890] 
}
```

**Associate Records With Label (PUT):**

```json
[
  {
    "associationCategory": "USER_DEFINED",
    "associationTypeId": 36
  }
]
```

**Bulk Create Labeled Associations (POST):**

```json
[
  {
    "fromObjectId": 1,
    "toObjectId": 2,
    "associationCategory": "USER_DEFINED",
    "associationTypeId": 36
  },
  {
    "fromObjectId": 3,
    "toObjectId": 4,
    "associationCategory": "USER_DEFINED",
    "associationTypeId": 37
  }
]
```

**Bulk Retrieve Associated Records (POST):**

```json
{
  "inputs": [
    {"id": "33451"},
    {"id": "29851"}
  ]
}
```

**Bulk Remove All Associations (POST):**

```json
[
  {
    "from": {"id": "12345"},
    "to": [{"id": "67891"}]
  },
  {
    "from": {"id": "9876"},
    "to": [{"id": "54321"}]
  }
]
```

**Remove Specific Association Labels (POST):**

```json
{
  "inputs": [
    {
      "types": [
        {"associationCategory": "USER_DEFINED", "associationTypeId": 37}
      ],
      "from": {"id": "29851"},
      "to": {"id": "5790939450"}
    }
  ]
}
```

**Create Association Label (POST):**

```json
{
  "label": "Partner",
  "name": "partner"
}
```

**Create Paired Association Label (POST):**

```json
{
  "label": "Manager",
  "inverseLabel": "Employee",
  "name": "manager_employee"
}
```

**Update Association Label (PUT):**

```json
{
  "associationTypeId": 32,
  "label": "Contract worker"
}
```

**Create Association Limits (POST):**

```json
{
  "inputs": [
    {
      "category": "HUBSPOT_DEFINED",
      "typeId": 3,
      "maxToObjectIds": 5
    },
    {
      "category": "USER_DEFINED",
      "typeId": 35,
      "maxToObjectIds": 1
    }
  ]
}
```


**Delete Association Limits (POST):**

```json
{
  "inputs": [
    {"category": "USER_DEFINED", "typeId": 35}
  ]
}
```


This comprehensive markdown documentation provides a detailed overview of the HubSpot CRM API v4 for Associations, including clear explanations, code examples, and request/response structures.  Remember to consult the official HubSpot API documentation for the most up-to-date information.
