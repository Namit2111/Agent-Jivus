# HubSpot CRM API v4: Associations

This document details the HubSpot CRM API v4 Associations endpoints.  It allows you to manage relationships between HubSpot CRM objects.  This version supersedes the v3 Associations API.

**Note:** The v4 Associations API is supported in HubSpot NodeJS Client version 9.0.0 or later.  The number of associations a record can have depends on the object and your HubSpot subscription.

## I. Association Endpoints

These endpoints create, edit, and remove associations between records.

### A. Associate Records

**1. Associate Records without a Label:**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`
* **Parameters:**
    * `fromObjectType`: ID of the object being associated (e.g., `contact`, `company`). See [Object Type IDs](#object-type-ids) for a list.
    * `fromObjectId`: ID of the record being associated.
    * `toObjectType`: ID of the object the record is being associated *to*.
    * `toObjectId`: ID of the record being associated *to*.
* **Example:** Associate contact (ID 12345) with company (ID 67891):
    ```
    PUT /crm/v4/objects/contact/12345/associations/default/company/67891
    ```

* **Bulk Association (without labels):**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default`
    * **Request Body:**  An array of `objectId` values for records to associate.


**2. Associate Records with a Label:**

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
* **Request Body:** Array of objects, each with:
    * `associationCategory`:  `"HUBSPOT_DEFINED"` (default) or `"USER_DEFINED"` (custom).
    * `associationTypeId`: Numerical ID of the label.  Retrieve using `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels` (see below).
* **Example:** Associate contact with a deal using a custom label (typeId 36):
    ```
    PUT /crm/v4/objects/contact/{objectId}/associations/deal/{toObjectId}
    ```
    Request Body:
    ```json
    [
      {
        "associationCategory": "USER_DEFINED",
        "associationTypeId": 36
      }
    ]
    ```
    Example Response:
    ```json
    {
      "fromObjectTypeId": "0-1",
      "fromObjectId": 29851,
      "toObjectTypeId": "0-3",
      "toObjectId": 21678228008,
      "labels": ["Point of contact"]
    }
    ```

* **Bulk Labeled Association:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create`
    * **Request Body:**  Similar to individual association, but allows for multiple associations in a single request.


### B. Retrieve Associated Records

**1. Retrieve Individual Record Associations:**

* **Method:** `GET`
* **Endpoint:** `/crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}`
* **Parameters:**
    * `fromObjectType`: Object type of the record whose associations are being retrieved.
    * `objectId`: ID of the record.
    * `toObjectType`: Object type of the associated records.

**2. Batch Retrieve Associated Records:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read`
* **Request Body:** Array of objects, each with an `id` field representing the record ID.
* **Example:** Retrieve all company associations for contacts with IDs "33451" and "29851":
    ```json
    {
      "inputs": [
        {"id": "33451"},
        {"id": "29851"}
      ]
    }
    ```
    Example Response (truncated for brevity):
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
                // ...association type details...
              ]
            }
          ]
        },
        // ...more results...
      ]
    }
    ```


### C. Update Record Association Labels

* Use the `PUT` or `POST` endpoints from the "Associate Records" section to update labels.  To replace existing labels, only include the new label(s) in the request. To append, include all desired labels.

### D. Remove Record Associations

**1. Remove All Associations:**

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`
* **Bulk Removal:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive`
    * **Request Body:** Array of objects specifying `from` and `to` record IDs.

**2. Remove Specific Association Labels:**

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive`
* **Request Body:** Array of objects specifying `from`, `to` record IDs, `associationTypeId`, and `category` of the label(s) to remove.



## II. Association Schema Endpoints

These endpoints manage association definitions (types) and labels.

### A.  Understand Association Definitions, Configurations, and Labels

This section covers managing association types and their limits.  HubSpot provides pre-defined types (e.g., Primary company, Unlabeled).  Admins can define custom labels.

### B. HubSpot Defined Associations

* **Primary:** The main association.  Used in tools like lists and workflows.
* **Unlabeled:** A default association.  Always returned in responses with `label: null`.


### C. Custom Association Labels

You can create custom labels to provide more context to relationships.  There are two types:

* **Single:** One label for both records.
* **Paired:** A pair of labels for when different words describe each side of the relationship (e.g., "Manager" and "Employee").

### D. Create and Manage Association Types

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:**
    * `name`: Internal name (no hyphens, doesn't start with a number).
    * `label`: Display name.
    * `inverseLabel` (paired labels only):  Second label in the pair.

### E. Retrieve Association Labels

* **Method:** `GET`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`


### F. Update Association Labels

* **Method:** `PUT`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels`
* **Request Body:** `associationTypeId` and updated `label` (and optionally `inverseLabel`).

### G. Delete Association Labels

* **Method:** `DELETE`
* **Endpoint:** `/crm/v4/associations/{fromObjectType}/{toObjectType}/labels/{associationTypeId}`


### H. Set and Manage Association Limits

* **Create/Update Limits:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/create` (create) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/update` (update)
    * **Request Body:** `inputs` array with `category`, `typeId`, and `maxToObjectIds`.

* **Retrieve Limits:**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/all` (all limits) or `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}` (specific objects).

* **Delete Limits:**
    * **Method:** `POST`
    * **Endpoint:** `/crm/v4/associations/definitions/configurations/{fromObjectType}/{toObjectType}/batch/purge`
    * **Request Body:** `inputs` array with `category` and `typeId`.


## III.  Report on High Association Usage

* **Method:** `POST`
* **Endpoint:** `/crm/v4/associations/usage/high-usage-report/{userId}`
* Sends a report to the user's email.


## IV. Limitations

* **Daily Limits:** 500,000 requests (Professional and Enterprise), potentially increased with API limit increase purchase (but not exceeding 1,000,000).
* **Burst Limits:** 100 requests per 10 seconds (Free/Starter), 150 (Professional/Enterprise), potentially 200 with API limit increase (but not exceeding 200).


## V. Association Type ID Values

The following tables list HubSpot-defined `associationTypeId` values.  Custom objects and labels will have unique IDs.  Retrieve these IDs through the API or in your HubSpot association settings.

**(Tables omitted for brevity, refer to the original text for the detailed tables of `associationTypeId` values.)**

## VI. v1 Associations (Legacy)

(Table omitted for brevity, refer to original text)


This markdown provides a comprehensive overview of the HubSpot CRM API v4 Associations. Remember to consult the official HubSpot API documentation for the most up-to-date information and details.
