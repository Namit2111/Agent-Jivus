# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 for managing record associations.  Associations represent relationships between records in the HubSpot CRM, allowing connections between different object types (e.g., Contact to Company) or within the same object type (e.g., Company to Company).  This API provides endpoints for managing associations and their schemas.

## API Endpoints Categories:

The v4 Associations API is divided into two main categories of endpoints:

* **Association Endpoints:**  Used to create, update, and delete associations between records.
* **Association Schema Endpoints:** Used to manage association definitions (types), custom labels, and association limits.

##  Supported Objects:

The API supports associations between the following objects (and custom objects):

* Contacts
* Companies
* Deals
* Tickets
* Leads
* Appointments
* Courses
* Listings
* Services
* Calls
* Emails
* Meetings
* Notes
* Postal Mail
* Quotes
* Tasks
* Communications (SMS, WhatsApp, LinkedIn messages)
* Orders
* Carts


##  Association Types:

* **HubSpot Defined:** Predefined association types (e.g., "Primary company").
* **User Defined:** Custom association types created by the user, allowing for more granular relationship descriptions (e.g., "Billing Contact", "Manager").  These require creating and managing association labels.
* **Unlabeled:** A default association type, indicating a relationship exists without a specific label. Always returned with `label: null`.


##  Endpoints and Usage:

### 1. Associate Records

#### 1.1 Associate Records Without a Label:

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Parameters:**
    * `fromObjectType`: ID of the source object.  Use object name (e.g., `contact`, `company`) for contacts, companies, deals, tickets, and notes; otherwise, use the object type ID.
    * `fromObjectId`: ID of the source record.
    * `toObjectType`: ID of the target object.  Use object name (e.g., `contact`, `company`) for contacts, companies, deals, tickets, and notes; otherwise, use the object type ID.
    * `toObjectId`: ID of the target record.
* **Example:**  Associate contact (12345) with company (67891):
    `PUT /crm/v4/objects/contact/12345/associations/default/company/67891`

#### 1.2 Associate Records With a Label:

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body (Example):**
```json
[
  {
    "associationCategory": "USER_DEFINED",
    "associationTypeId": 36 // Get this ID from /crm/v4/associations/{fromObjectType}/{toObjectType}/labels
  }
]
```
* **Parameters:**  Similar to 1.1, but includes a label.  `associationTypeId` specifies the label. Obtain `associationTypeId` using the `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels` endpoint.
* **Example:** Associate contact with deal using custom label (typeId 36):
   `PUT /crm/v4/objects/contact/12345/associations/deal/67891` with the above request body.


#### 1.3 Bulk Associate Records (Without Label):

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
* **Request Body (Example):**
```json
{
  "inputs": [
    {"objectId": "12345"},
    {"objectId": "98765"}
  ]
}
```
* **Parameters:** `fromObjectType`, `toObjectType` and an array of `objectId`s to associate.

#### 1.4 Bulk Associate Records (With Label):

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`
* **Request Body:**  Similar to 1.2, but with an array of associations, each specifying `objectId`, `toObjectId`, and labels.


### 2. Retrieve Associated Records

#### 2.1 Retrieve Individual Record's Associations:

* **Method:** `GET`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`

#### 2.2 Retrieve Associated Records in Bulk:

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Request Body (Example):**
```json
{
  "inputs": [
    {"id": "33451"},
    {"id": "29851"}
  ]
}
```

### 3. Update Record Association Labels:

* Use the bulk create endpoints (`POST /crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`) to update existing associations; include all labels (existing + new).  To replace labels, only include the new ones.

### 4. Remove Record Associations

#### 4.1 Remove All Associations Between Two Records:

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`

#### 4.2 Bulk Remove All Associations:

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`

#### 4.3 Remove Specific Association Labels:

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`


### 5. Association Schema Endpoints:

These endpoints manage association types, labels, and limits.

#### 5.1 Create Association Labels:

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body (Single Label):**
```json
{
  "label": "Partner",
  "name": "partner"
}
```
* **Request Body (Paired Label):**
```json
{
  "label": "Manager",
  "inverseLabel": "Employee",
  "name": "manager_employee"
}
```

#### 5.2 Retrieve Association Labels:

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`

#### 5.3 Update Association Labels:

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`

#### 5.4 Delete Association Labels:

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`

#### 5.5 Create/Update Association Limits:

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (create) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (update)

#### 5.6 Retrieve Association Limits:

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/all` (all limits) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (specific objects)

#### 5.7 Delete Association Limits:

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`

### 6. High Association Usage Report:

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/usage/high-usage-report/{userId}`
* Sends a report to the specified user's email.


##  Error Handling:

The API returns standard HTTP status codes to indicate success or failure.  Detailed error messages are included in the response body.

## Rate Limits:

Refer to the documentation for rate limits based on your HubSpot subscription.

##  Object Type IDs:

Refer to the tables in the original documentation for a list of HubSpot-defined `associationTypeId` values.  Custom object and custom label types will have unique IDs.  You can retrieve these IDs through the API.


This markdown documentation provides a structured overview of the HubSpot CRM API v4 for Associations.  Always refer to the official HubSpot API documentation for the most up-to-date information and details.
