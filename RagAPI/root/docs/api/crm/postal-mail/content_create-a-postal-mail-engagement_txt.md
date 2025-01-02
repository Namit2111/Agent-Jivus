# HubSpot Postal Mail Engagement API Documentation

This document details the HubSpot Postal Mail Engagement API, allowing you to manage postal mail engagements within the HubSpot CRM.  You can create, retrieve, update, and delete postal mail engagements, and associate them with other HubSpot records.

## API Endpoints

All endpoints are located under the `/crm/v3/objects/postal_mail` base path.  Replace `{postalMail}` with the unique ID of the postal mail engagement.

**Base URL:** `/crm/v3/objects/postal_mail`


## API Methods

### 1. Create a Postal Mail Engagement

* **Method:** `POST`
* **Endpoint:** `/crm/v3/objects/postal_mail`
* **Request Body:** JSON object with `properties` and optional `associations` objects.

**Properties Object:**

| Field             | Description                                                                    | Type     | Example                                    |
|----------------------|--------------------------------------------------------------------------------|----------|---------------------------------------------|
| `hs_timestamp`      | Date and time the postal mail was sent or received.                          | String   | `"2024-10-27"`                             |
| `hs_postal_mail_body` | Body text of the postal mail engagement.                                      | String   | `"Sent contract to client."`                |
| `hubspot_owner_id`   | ID of the user who created the engagement.                                    | String   | `"12345"`                                  |
| `hs_attachment_ids` | IDs of attached files (semicolon-separated).                                 | String   | `"67890;12345"`                             |


**Associations Object:**  (Optional, used to associate with other records)

```json
[
  {
    "to": { "id": 501 }, // ID of the record to associate with
    "types": [
      {
        "associationCategory": "HUBSPOT_DEFINED",
        "associationTypeId": 453 // Default association type ID (See notes below for details)
      }
    ]
  },
  {
    "to": { "id": 502 },
    "types": [
      {
        "associationCategory": "HUBSPOT_DEFINED",
        "associationTypeId": 453
      }
    ]
  }
]
```

**Example Request:**

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27",
    "hs_postal_mail_body": "Sent contract to client.",
    "hubspot_owner_id": "12345",
    "hs_attachment_ids": "67890;12345"
  },
  "associations": [
    {
      "to": { "id": 501 },
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 453 }]
    }
  ]
}
```

**Response:** (On success, returns the created postal mail engagement object)


### 2. Retrieve Postal Mail Engagements

* **Method:** `GET`
* **Endpoint:** `/crm/v3/objects/postal_mail` (for list) or `/crm/v3/objects/postal_mail/{postalMail}` (for single)
* **Parameters:**
    * `limit`: (List only) Maximum number of results per page.
    * `properties`: Comma-separated list of properties to return.
    * `associations`: Comma-separated list of object types to retrieve associated IDs for.

**Example Request (Single):** `GET /crm/v3/objects/postal_mail/12345?properties=hs_timestamp,hs_postal_mail_body`

**Example Request (List):** `GET /crm/v3/objects/postal_mail?limit=10&properties=hs_timestamp`


**Response:** (JSON array of postal mail engagement objects for list requests; single object for single requests)


### 3. Update a Postal Mail Engagement

* **Method:** `PATCH`
* **Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}`
* **Request Body:** JSON object with `properties` to update.  HubSpot ignores read-only and non-existent properties. To clear a property, send an empty string.

**Example Request:**

```json
{
  "properties": {
    "hs_postal_mail_body": "Sent contract to client. Follow-up call scheduled."
  }
}
```

**Response:** (Updated postal mail engagement object)


### 4. Associate Existing Postal Mail with Records

* **Method:** `PUT`
* **Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`
* **Parameters:**
    * `postalMail`: ID of the postal mail engagement.
    * `toObjectType`: Type of object to associate (e.g., `contact`, `company`).
    * `toObjectId`: ID of the record to associate with.
    * `associationTypeId`:  Association type ID (See notes below for details).

**Example URL:** `/crm/v3/objects/postal_mail/12345/associations/contact/67890/POSTAL_MAIL_TO_CONTACT`

**Response:**  (Confirmation or error message)


### 5. Remove an Association

* **Method:** `DELETE`
* **Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`
* **Parameters:** Same as associating postal mail.

**Response:** (Confirmation or error message)


### 6. Pin a Postal Mail Engagement

Pinning is handled indirectly by including the `hs_pinned_engagement_id` field with the postal mail ID when updating associated records (Contacts, Companies, etc.) via their respective APIs.


### 7. Delete a Postal Mail Engagement

* **Method:** `DELETE`
* **Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}`

**Response:** (Confirmation or error message)


**Notes:**

*  **Association Type IDs:**  The documentation mentions obtaining default and custom association type IDs via the Associations API.  This API call is not detailed here, but is necessary for associating postal mail with records if you are not using the default `associationTypeId`.
* **Error Handling:**  The API will return appropriate error codes and messages in case of failures.  Refer to the HubSpot API documentation for details on error codes.
* **Authentication:**  You'll need a HubSpot API key for authentication.  Refer to the HubSpot developer portal for instructions on obtaining an API key.


This documentation provides a concise overview.  Always refer to the official HubSpot API documentation for the most up-to-date information and details on error handling, rate limits, and other important aspects.
