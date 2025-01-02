# HubSpot Postal Mail Engagement API

This document describes the HubSpot Postal Mail Engagement API, allowing you to log, manage, and interact with postal mail engagements within the HubSpot CRM.

## API Endpoints

All endpoints are under the `/crm/v3/objects/postal_mail` base path.  Replace `{postalMail}` with the unique ID of the postal mail engagement.

### 1. Create a Postal Mail Engagement

* **Method:** `POST`
* **Endpoint:** `/crm/v3/objects/postal_mail`
* **Request Body:**  JSON object with `properties` and optional `associations` objects.

**Properties Object:**

| Field             | Description                                                              | Type    |
|----------------------|--------------------------------------------------------------------------|---------|
| `hs_timestamp`      | Date and time the postal mail was sent or received (YYYY-MM-DD).           | String  |
| `hs_postal_mail_body` | Body text of the postal mail engagement.                                 | String  |
| `hubspot_owner_id`  | ID of the user who created the engagement.                               | String  |
| `hs_attachment_ids` | IDs of attachments (semicolon-separated).                              | String  |


**Associations Object:** (Optional, for associating with existing records)

This object is an array of association objects. Each object contains:

| Parameter       | Description                                                         | Type    |
|-----------------|---------------------------------------------------------------------|---------|
| `to.id`         | ID of the record to associate (e.g., Contact, Company ID).            | Integer |
| `types[0].associationCategory` | Association category ("HUBSPOT_DEFINED").                         | String  |
| `types[0].associationTypeId`   | Association type ID (e.g., 453 for Contact, see Associations API). | Integer |


**Example Request Body:**

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27",
    "hs_postal_mail_body": "Sent contract to John Doe",
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

**Response:**  JSON object representing the created postal mail engagement, including its ID.


### 2. Retrieve Postal Mail Engagements

* **Method:** `GET`
* **Endpoint:** `/crm/v3/objects/postal_mail` (for list) or `/crm/v3/objects/postal_mail/{postalMail}` (for individual)
* **Parameters:**
    * `limit`: Maximum number of results per page (list only).
    * `properties`: Comma-separated list of properties to return.
    * `associations`: Comma-separated list of object types to retrieve associated IDs for.

**Example GET Request (Individual):**

`/crm/v3/objects/postal_mail/12345?properties=hs_timestamp,hs_postal_mail_body`

**Response:** JSON object representing the postal mail engagement or a list of engagements.


### 3. Update Postal Mail Engagements

* **Method:** `PATCH`
* **Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}`
* **Request Body:** JSON object with `properties` to update.  HubSpot ignores read-only and non-existent properties.  Use an empty string to clear a property value.

**Example Request Body:**

```json
{
  "properties": {
    "hs_postal_mail_body": "Updated body text"
  }
}
```

**Response:** JSON object representing the updated postal mail engagement.


### 4. Associate Existing Postal Mail with Records

* **Method:** `PUT`
* **Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`
* **Parameters:**
    * `toObjectType`: Object type (e.g., `contact`, `company`).
    * `toObjectId`: ID of the record to associate.
    * `associationTypeId`:  Association type ID (retrieve from Associations API).

**Example Endpoint:**

`/crm/v3/objects/postal_mail/12345/associations/contact/67890/POSTAL_MAIL_TO_CONTACT`


### 5. Remove an Association

* **Method:** `DELETE`
* **Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`
* **Parameters:** Same as associate endpoint.

### 6. Pin a Postal Mail Engagement

Pinning is done by including the postal mail's `id` in the `hs_pinned_engagement_id` field when creating or updating a record via other HubSpot object APIs (Contacts, Companies, Deals, Tickets, etc.).


### 7. Delete Postal Mail Engagements

* **Method:** `DELETE`
* **Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}`

**Response:**  Success or error message.


##  Error Handling

The API will return standard HTTP status codes to indicate success or failure.  Error responses will include a JSON object with details about the error.


## Authentication

You will need a HubSpot API key for authentication.  Refer to the HubSpot developer documentation for details on obtaining and using an API key.  Typically this involves using an `Authorization` header with a `Bearer` token.


This documentation provides a concise overview. Refer to the official HubSpot API documentation for complete details and the latest information on endpoints, parameters, and error handling.
