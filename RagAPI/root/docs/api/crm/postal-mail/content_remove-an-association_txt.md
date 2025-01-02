# HubSpot Postal Mail Engagement API Documentation

This document details the HubSpot Postal Mail Engagement API, allowing you to manage postal mail engagements within the HubSpot CRM.  You can create, retrieve, update, and delete postal mail records, and associate them with other HubSpot records (contacts, companies, etc.).

## API Endpoints

All endpoints are under the `/crm/v3/objects/postal_mail` base path.  Replace `{postalMail}` with the ID of the specific postal mail engagement.

### 1. Create a Postal Mail Engagement

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/postal_mail`

**Request Body:**

The request body must contain a `properties` object, and optionally an `associations` array.

* **`properties` (required):**  An object with the following fields:

    * `hs_timestamp` (string): Date and time the postal mail was sent or received (ISO 8601 format, e.g., "2024-10-27T10:30:00").
    * `hs_postal_mail_body` (string): The body text of the postal mail.
    * `hubspot_owner_id` (string): ID of the HubSpot user who created the engagement.
    * `hs_attachment_ids` (string): Semicolon-separated list of attachment IDs.


* **`associations` (optional):** An array of objects, each associating the postal mail with another HubSpot record. Each object should include:

    * `to` (object): Contains the `id` of the record to associate with.
    * `types` (array): An array of objects, each specifying the association type:
        * `associationCategory`: "HUBSPOT_DEFINED"
        * `associationTypeId`:  The ID of the association type (e.g., 453 for contact).  See [Associations API](link_to_associations_api_if_available) for details on retrieving custom association type IDs.


**Example Request Body:**

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27T10:30:00",
    "hs_postal_mail_body": "Sent contract copy to John Doe",
    "hubspot_owner_id": "12345",
    "hs_attachment_ids": "67890"
  },
  "associations": [
    {
      "to": {"id": 501},
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 453}]
    }
  ]
}
```

**Response:**  A JSON object representing the created postal mail engagement, including its ID.


### 2. Retrieve Postal Mail Engagements

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/postal_mail` (for list) or `/crm/v3/objects/postal_mail/{postalMail}` (for single)

**Parameters:**

* **`limit` (integer, for list endpoint only):** Maximum number of results per page.
* **`properties` (string, for both endpoints):** Comma-separated list of properties to return.
* **`associations` (string, for single endpoint):** Comma-separated list of object types to retrieve associated IDs for.


**Example Request (single):**

`GET /crm/v3/objects/postal_mail/12345?properties=hs_timestamp,hs_postal_mail_body`


**Response:** A JSON object (single) or JSON array (list) containing the requested postal mail engagement(s).


### 3. Update a Postal Mail Engagement

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}`

**Request Body:**

A JSON object containing the properties to update.  HubSpot ignores read-only and non-existent properties.  Use an empty string to clear a property value.


**Example Request Body:**

```json
{
  "properties": {
    "hs_postal_mail_body": "Contract sent; follow-up call received."
  }
}
```

**Response:** A JSON object representing the updated postal mail engagement.


### 4. Associate Existing Postal Mail with Records

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Parameters:**

* `{postalMail}`: ID of the postal mail engagement.
* `{toObjectType}`: Type of object to associate (e.g., `contact`, `company`).
* `{toObjectId}`: ID of the object to associate.
* `{associationTypeId}`: ID of the association type.


**Example URL:**

`/crm/v3/objects/postal_mail/12345/associations/contact/67890/POSTAL_MAIL_TO_CONTACT`


**Response:**  A success or error response.


### 5. Remove an Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Parameters:** Same as Associate Existing Postal Mail.

**Response:** A success or error response.


### 6. Pin a Postal Mail Engagement

Pinning is done by including the `hs_pinned_engagement_id` field in the record creation or update API calls (not directly via this API).


### 7. Delete a Postal Mail Engagement

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}`

**Response:** A success or error response.


## Error Handling

The API will return standard HTTP status codes (e.g., 400 Bad Request, 404 Not Found, 500 Internal Server Error) with detailed error messages in the response body.


This documentation provides a concise overview.  Refer to the HubSpot developer portal for the most up-to-date information and complete API reference.
