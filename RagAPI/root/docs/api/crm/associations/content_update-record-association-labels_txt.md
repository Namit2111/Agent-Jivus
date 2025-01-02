# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 Associations endpoints.  This version supersedes the v3 Associations API.  The v4 API allows for managing relationships (associations) between HubSpot CRM objects and activities.  Associations can be between different object types (e.g., Contact to Company) or within the same object type (e.g., Company to Company).

The API is divided into two main sections:

* **Association Endpoints:** Create, update, and delete associations between records.
* **Association Schema Endpoints:** Manage association definitions (types), custom labels, and association limits.

**Note:** The v4 Associations API requires HubSpot NodeJS Client Version 9.0.0 or later.  Association limits depend on the object type and your HubSpot subscription.


## I. Association Endpoints

### A. Associate Records

#### 1. Associate Records Without a Label

**Method:** PUT

**Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`

**Parameters:**

* `fromObjectType`: ID of the object being associated (e.g., `contact`, `company`). See [Object Type IDs](#object-type-ids) for a list.
* `fromObjectId`: ID of the record being associated.
* `toObjectType`: ID of the object the record is being associated *to*. See [Object Type IDs](#object-type-ids) for a list.
* `toObjectId`: ID of the record being associated *to*.


**Example:** Associate contact with ID 12345 to company with ID 67891:

```bash
PUT /crm/v4/objects/contact/12345/associations/default/company/67891
```

#### 2. Bulk Associate Records Without a Label

**Method:** POST

**Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`

**Request Body:**  Array of `objectId` values for records to associate.

```json
[12345, 67891, 90123]
```

#### 3. Associate Records With a Label

**Method:** PUT

**Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/{toObjectType}/{toObjectId}`

**Request Body:** Array of objects, each specifying a label:

```json
[
  {
    "associationCategory": "USER_DEFINED",
    "associationTypeId": 36 
  }
]
```

* `associationCategory`:  `HUBSPOT_DEFINED` (default label) or `USER_DEFINED` (custom label).
* `associationTypeId`: Numerical ID of the label.  Obtain this from the [Association Schema Endpoints](#ii-association-schema-endpoints)


**Example:**  Associate a contact with a deal using a custom label (requires prior retrieval of `associationTypeId`):

1. **GET** `/crm/v4/associations/contact/deal/labels` to get available labels.
2. **PUT** `/crm/v4/objects/contact/{objectId}/associations/deal/{toObjectId}` with the request body above.

#### 4. Bulk Create Labeled Associations

**Method:** POST

**Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`

**Request Body:** Array of objects, each specifying a pair of records and labels.  Similar to the single labeled association PUT request, but allows for multiple associations in one request.


### B. Retrieve Associated Records

#### 1. Retrieve Individual Record's Associations

**Method:** GET

**Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`

**Parameters:**

* `fromObjectType`: Object type of the record.
* `objectId`: ID of the record.
* `toObjectType`: Object type of associated records to retrieve.

#### 2. Bulk Retrieve Associated Records

**Method:** POST

**Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`

**Request Body:**

```json
{
  "inputs": [
    {"id": "33451"},
    {"id": "29851"}
  ]
}
```

### C. Update Record Association Labels

Use the bulk create endpoints (POST `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`) to update existing association labels.  Include all labels to keep, including new ones.

### D. Remove Record Associations

#### 1. Remove All Associations Between Two Records

**Method:** DELETE

**Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/{toObjectType}/{toObjectId}`

#### 2. Bulk Remove All Associations

**Method:** POST

**Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`

**Request Body:** Array of objects specifying `from` and `to` object IDs.


#### 3. Remove Specific Association Labels

**Method:** POST

**Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`

**Request Body:** Array of objects specifying `from`, `to` object IDs, and the `associationTypeId` and `category` of the labels to remove.


## II. Association Schema Endpoints

These endpoints manage association definitions, configurations, and labels.


### A. Understand Association Definitions, Configurations, and Labels

This section covers HubSpot-defined and custom association labels, as well as managing association types and limits.

### B. HubSpot Defined Associations

HubSpot provides predefined associations like "Primary" and "Unlabeled."  "Primary" associations are used in HubSpot tools like lists and workflows.  "Unlabeled" associations indicate a relationship exists, always returned with `label: null`.

### C. Custom Association Labels

You can create custom labels (single or paired) to add context to associations.

### D. Create and Manage Association Types

#### 1. Create Association Labels

**Method:** POST

**Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`

**Request Body:**

* `name`: Internal name (no hyphens, doesn't start with a number).
* `label`: Display name of the label.
* `inverseLabel` (for paired labels):  Name of the inverse label.

**Example (Single Label):**

```json
{
  "label": "Partner",
  "name": "partner"
}
```

**Example (Paired Label):**

```json
{
  "label": "Manager",
  "inverseLabel": "Employee",
  "name": "manager_employee"
}
```

#### 2. Retrieve Association Labels

**Method:** GET

**Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`

#### 3. Update Association Labels

**Method:** PUT

**Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`

**Request Body:**

* `associationTypeId`: ID of the label to update.
* `label`: New label name.
* `inverseLabel` (optional, for paired labels): New inverse label name.

#### 4. Delete Association Labels

**Method:** DELETE

**Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`


### E. Set and Manage Association Limits

#### 1. Create or Update Association Limits

**Method:** POST

**Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (create) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (update)

**Request Body:**

* `inputs`: Array of objects specifying `category`, `typeId`, and `maxToObjectIds`.

#### 2. Retrieve Association Limits

**Method:** GET

**Endpoint:** `/crm/v4/associations/definitions/configurations/all` (all limits) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (limits between specific objects)

#### 3. Delete Association Limits

**Method:** POST

**Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`


## III.  Limitations

* **Daily Limits:**  Vary by HubSpot subscription (500,000 for Professional and Enterprise, potentially 1,000,000 with API limit increase).
* **Burst Limits:** Vary by HubSpot subscription (100 requests per 10 seconds for Free/Starter, 150 for Professional/Enterprise, potentially 200 with API limit increase).


## IV. Object Type IDs

See the provided table in the original document for a comprehensive list of `typeId` values for various object and association types.  This list includes both HubSpot-defined and examples of custom types.  Note that custom object and custom label types will have unique `typeId` values.


## V. Reporting on High Association Usage

**Method:** POST

**Endpoint:** `/crm/v4/associations/usage/high-usage-report/{userId}`

This endpoint sends a report of records nearing or exceeding association limits to the specified user's email.


This markdown documentation provides a comprehensive overview of the HubSpot CRM API v4 Associations.  Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
