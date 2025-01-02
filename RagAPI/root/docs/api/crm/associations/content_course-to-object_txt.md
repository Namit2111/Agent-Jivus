# HubSpot CRM API v4: Associations

This document describes the HubSpot CRM API v4 for managing record associations.  Associations represent relationships between different CRM objects (e.g., Contact to Company) or within the same object (e.g., Company to Company).  This API provides endpoints for managing associations and their schemas.

## API Endpoints Categories:

The v4 Associations API is divided into two main categories:

* **Association Endpoints:** Create, update, and delete associations between records.
* **Association Schema Endpoints:** Manage association definitions (types), custom labels, and association limits.

##  Key Concepts:

* **Objects:**  Represent different data types in HubSpot (e.g., Contacts, Companies, Deals). Each object has a unique ID.
* **Records:** Individual entries within an object.  Each record has a unique ID within its object.
* **Associations:** Relationships between records.  Associations can be labeled or unlabeled.
* **Labels:**  Descriptive tags for associations (e.g., "Primary Contact," "Manager").  Can be HubSpot-defined or custom.
* **Association Types:** Define the type of relationship between objects (e.g., Contact to Company).  Each type has a unique `typeId`.
* **Association Limits:**  Restrictions on the number of associations a record can have, based on object type, label, and HubSpot subscription.

## Supported Objects:

The API supports associations between the following objects (and potentially custom objects):

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


##  Endpoints and Usage:

### 1. Associate Records:

**a) Without a Label:**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Parameters:**
    * `fromObjectType`: ID of the source object (e.g., "contact", "company").
    * `fromObjectId`: ID of the source record.
    * `toObjectType`: ID of the target object.
    * `toObjectId`: ID of the target record.
* **Example:** Associate contact (12345) with company (67891):
  `PUT /crm/v4/objects/contact/12345/associations/default/company/67891`

**b) With a Label:**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body:**  An array of objects, each with:
    * `associationCategory`: "HUBSPOT_DEFINED" or "USER_DEFINED".
    * `associationTypeId`:  Numeric ID of the label.
* **Example:** Associate contact (12345) with deal (67890) using custom label (typeId: 36):
  `PUT /crm/v4/objects/contact/12345/associations/deal/67890`
  ```json
  [
    {
      "associationCategory": "USER_DEFINED",
      "associationTypeId": 36
    }
  ]
  ```

### 2. Retrieve Associated Records:

**a) Individual Record:**

* **Method:** `GET`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`
* **Parameters:**
    * `fromObjectType`: ID of the source object.
    * `objectId`: ID of the source record.
    * `toObjectType`: ID of the target object.

**b) Batch Retrieval:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Request Body:**
    ```json
    {
      "inputs": [
        { "id": "33451" },
        { "id": "29851" }
      ]
    }
    ```

### 3. Update Record Association Labels:

* Use the same `PUT` endpoints as associating records, providing the updated label(s).  To append labels, include all existing and new labels.


### 4. Remove Record Associations:

**a) Remove All Associations:**

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`

**b) Remove Specific Labels:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
* **Request Body:**  Specify `associationTypeId` and `category` of labels to remove.


### 5. Manage Association Schema:

This section details endpoints for managing association types, labels, and limits.  Refer to the original document for detailed examples and explanations of each endpoint.  The key endpoints include:

* Creating/Updating/Retrieving/Deleting Association Labels
* Creating/Updating/Retrieving/Deleting Association Limits


##  Error Handling:

The API returns standard HTTP status codes to indicate success or failure.  Error responses will contain details about the issue.

## Rate Limits:

The API has rate limits based on the HubSpot account type. Refer to the original document for details on daily and burst limits.

##  Further Information:

Refer to the original HubSpot documentation for complete details, including comprehensive examples and specific error handling.  This markdown summary provides a concise overview of the key features and functionality of the HubSpot CRM API v4 for associations.
