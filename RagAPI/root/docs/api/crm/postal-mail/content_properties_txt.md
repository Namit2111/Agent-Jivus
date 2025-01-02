# HubSpot Postal Mail Engagement API Documentation

This document describes the HubSpot API for managing postal mail engagements.  It allows you to log, retrieve, update, and delete postal mail interactions associated with CRM records.

## API Endpoints

All endpoints are under the `/crm/v3/objects/postal_mail` base path.  Remember to replace `{postalMail}` with the actual postal mail engagement ID.

### 1. Create a Postal Mail Engagement

* **Method:** `POST`
* **Endpoint:** `/crm/v3/objects/postal_mail`
* **Request Body:** JSON object with `properties` and optional `associations` objects.

    * **`properties` object:**
        * `hs_timestamp` (string): Date of sending/receiving (e.g., "2024-10-27").  *Required*.
        * `hs_postal_mail_body` (string): Body text of the mail. *Required*.
        * `hubspot_owner_id` (string): ID of the user creating the engagement. *Required*.
        * `hs_attachment_ids` (string): IDs of attachments, separated by semicolons. (e.g., "123;456;789").

    * **`associations` array (optional):**  Associates the postal mail with other records (contacts, companies, etc.).  Each element in the array should include:
        * `to` object:
            * `id` (integer): ID of the record to associate.
        * `types` array:
            * Each object in this array should specify the association type.
                * `associationCategory` (string):  "HUBSPOT_DEFINED".
                * `associationTypeId` (integer):  The specific association type ID.  (See HubSpot's documentation for default and custom IDs).


* **Example Request:**

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27",
    "hs_postal_mail_body": "Sent contract to client.",
    "hubspot_owner_id": "12345",
    "hs_attachment_ids": "67890"
  },
  "associations": [
    {
      "to": { "id": 501 },
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 453 }]
    }
  ]
}
```

* **Response:**  A JSON object representing the created postal mail engagement, including its ID.


### 2. Retrieve Postal Mail Engagements

* **Individual Retrieval:**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}`
    * **Parameters:**
        * `properties` (string): Comma-separated list of properties to return.
        * `associations` (string): Comma-separated list of object types to retrieve associated IDs for.

* **Bulk Retrieval:**
    * **Method:** `GET`
    * **Endpoint:** `/crm/v3/objects/postal_mail`
    * **Parameters:**
        * `limit` (integer): Maximum number of results per page.
        * `properties` (string): Comma-separated list of properties to return.

* **Example Response (Individual):**

```json
{
  "id": "123456789",
  "properties": {
    "hs_timestamp": "2024-10-27",
    "hs_postal_mail_body": "Sent contract to client.",
    "hubspot_owner_id": "12345",
    "hs_attachment_ids": "67890"
  },
  "associations": [...] //Association details if requested.
}
```


### 3. Update Postal Mail Engagements

* **Method:** `PATCH`
* **Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}`
* **Request Body:** JSON object with `properties` object containing the fields to update.  Omit fields you don't want to change.  An empty string will clear a property value.

* **Example Request:**

```json
{
  "properties": {
    "hs_postal_mail_body": "Sent contract; client responded."
  }
}
```

### 4. Associate Existing Postal Mail with Records

* **Method:** `PUT`
* **Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`
* **Parameters:**
    * `postalMail`: ID of the postal mail engagement.
    * `toObjectType`: Object type (e.g., "contact", "company").
    * `toObjectId`: ID of the record to associate.
    * `associationTypeId`: Association type ID.


### 5. Remove an Association

* **Method:** `DELETE`
* **Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`
* **Parameters:** Same as associating.


### 6. Pin a Postal Mail Engagement

Pinning is achieved by including the postal mail `id` in the `hs_pinned_engagement_id` field when creating or updating a record via the relevant object APIs (contacts, companies, deals, etc.).


### 7. Delete Postal Mail Engagements

* **Method:** `DELETE`
* **Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}`


##  Error Handling

The API will return appropriate HTTP status codes (e.g., 400 Bad Request, 404 Not Found, 500 Internal Server Error) along with JSON error messages indicating the cause of any failure.  Consult HubSpot's API documentation for detailed error codes and descriptions.


## Authentication

You'll need a HubSpot API key to authenticate your requests.  Refer to HubSpot's API documentation for authentication details.


This documentation provides a concise overview.  Refer to the official HubSpot API documentation for the most up-to-date information, including details on rate limits, pagination, and batch operations.
