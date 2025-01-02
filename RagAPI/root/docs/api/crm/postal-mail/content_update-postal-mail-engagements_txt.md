# HubSpot Postal Mail Engagement API

This document details the HubSpot Postal Mail Engagement API, allowing developers to log, manage, and interact with postal mail engagements within the HubSpot CRM.

## API Endpoints

All endpoints are under the `/crm/v3/objects/postal_mail` base path.  Remember to replace `{postalMail}` and other bracketed placeholders with the appropriate values.

### 1. Create a Postal Mail Engagement

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/postal_mail`

**Request Body:**

The request body must contain a `properties` object and optionally an `associations` object.

* **`properties` object:**
    * `hs_timestamp` (string): Date the mail was sent/received (YYYY-MM-DD).
    * `hs_postal_mail_body` (string): Body text of the engagement.
    * `hubspot_owner_id` (string): ID of the user who created the engagement.
    * `hs_attachment_ids` (string): IDs of attached files, separated by semicolons.

* **`associations` object (optional):**  An array of objects, each associating the postal mail with a record.  Each object requires:
    * `to`: An object with an `id` property representing the ID of the record to associate (e.g., Contact, Company).
    * `types`: An array of objects, each containing:
        * `associationCategory`: `"HUBSPOT_DEFINED"`
        * `associationTypeId`:  The ID of the association type (see [Default Association Type IDs](link_to_default_ids) or use the Associations API for custom types).


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
      "to": {"id": 501},
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 453}]
    }
  ]
}
```

**Response:**  A JSON object representing the newly created postal mail engagement, including its ID.


### 2. Retrieve Postal Mail Engagements

**Method:** `GET`

**Endpoint:**

* **Individual Engagement:** `/crm/v3/objects/postal_mail/{postalMail}`
* **List of Engagements:** `/crm/v3/objects/postal_mail`

**Parameters (for both endpoints):**

* `properties`: (string) Comma-separated list of properties to return.
* `associations`: (string) Comma-separated list of object types to retrieve associated IDs for. (Individual endpoint only)
* `limit`: (integer) Maximum number of results per page (List endpoint only).


**Example Request (Individual):**  `/crm/v3/objects/postal_mail/123?properties=hs_timestamp,hs_postal_mail_body`

**Example Response (Individual):** A JSON object representing the postal mail engagement.

**Example Response (List):**  A JSON object containing a list of postal mail engagements and pagination information.


### 3. Update a Postal Mail Engagement

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}`

**Request Body:**

A JSON object containing the `properties` object with fields to update.  HubSpot ignores read-only and non-existent properties.  Use an empty string to clear a property value.


**Example Request Body:**

```json
{
  "properties": {
    "hs_postal_mail_body": "Contract sent, follow-up call scheduled."
  }
}
```

**Response:** A JSON object representing the updated postal mail engagement.


### 4. Associate Existing Postal Mail with Records

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Parameters:**

* `postalMail`: (string) ID of the postal mail engagement.
* `toObjectType`: (string) Type of object to associate (e.g., `contact`, `company`).
* `toObjectId`: (string) ID of the object to associate.
* `associationTypeId`: (string) ID of the association type (numerical or snake_case).


**Example URL:** `/crm/v3/objects/postal_mail/456/associations/contact/789/POSTAL_MAIL_TO_CONTACT`

**Response:**  A success indicator.


### 5. Remove an Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Parameters:** Same as associating existing postal mail.

**Response:** A success indicator.


### 6. Pin a Postal Mail Engagement

This is not a direct API call but rather a field within the record creation/update APIs (`companies`, `contacts`, `deals`, `tickets`, and custom objects). Include the postal mail `id` in the `hs_pinned_engagement_id` field.


### 7. Delete a Postal Mail Engagement

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}`

**Response:** A success indicator.


## Error Handling

The API will return standard HTTP status codes and JSON error responses indicating the nature of any failures.


## Authentication

You'll need a valid HubSpot API key for authentication.  Refer to the HubSpot API documentation for details on obtaining and using an API key.


This documentation provides a concise overview.  Refer to the official HubSpot API documentation for the most up-to-date information and complete details on parameters, error handling, and rate limits.  Also, explore the "Endpoints" tab within the HubSpot documentation for a more comprehensive listing of all available endpoints and their specifics.
