# HubSpot Postal Mail Engagement API Documentation

This document details the HubSpot Postal Mail Engagement API, allowing you to manage postal mail engagements within the HubSpot CRM.  You can create, retrieve, update, associate, and delete postal mail entries.

## API Endpoints

All endpoints are under the `/crm/v3/objects/postal_mail` base path.  Remember to replace placeholders like `{postalMail}` and `{toObjectId}` with actual values.

### 1. Create a Postal Mail Engagement

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/postal_mail`

**Request Body:**

```json
{
  "properties": {
    "hs_timestamp": "YYYY-MM-DD", // Date sent/received (ISO 8601 format)
    "hs_postal_mail_body": "Mail body text",
    "hubspot_owner_id": 12345, // HubSpot user ID
    "hs_attachment_ids": "123;456;789" // Semicolon-separated attachment IDs
  },
  "associations": [
    {
      "to": {
        "id": 501 // ID of associated record (e.g., Contact ID)
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 453 // Association type ID (see notes below)
        }
      ]
    }
    // Add more associations as needed
  ]
}
```

**Response:**  A JSON object representing the created postal mail engagement, including its ID.

**Notes:**

* `associationTypeId`:  Default association type IDs are available in the HubSpot documentation.  Custom association types can be retrieved using the HubSpot Associations API.


### 2. Retrieve Postal Mail Engagements

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/postal_mail` (for list) or `/crm/v3/objects/postal_mail/{postalMail}` (for single)

**Parameters (for list):**

* `limit`: Maximum number of results per page.
* `properties`: Comma-separated list of properties to return.

**Parameters (for single):**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.

**Response:**  A JSON object (or array for list) containing the requested postal mail engagement(s).

### 3. Update a Postal Mail Engagement

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}`

**Request Body:**

```json
{
  "properties": {
    "hs_postal_mail_body": "Updated mail body text"
  }
}
```

**Response:** A JSON object representing the updated postal mail engagement.


### 4. Associate Existing Postal Mail with Records

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Parameters:**

* `postalMail`: ID of the postal mail engagement.
* `toObjectType`: Object type (e.g., `contact`, `company`).
* `toObjectId`: ID of the record to associate.
* `associationTypeId`: Association type ID.


**Response:**  A confirmation of the successful association.


### 5. Remove an Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Parameters:** Same as Associate Existing Postal Mail.

**Response:** A confirmation of the successful removal of the association.


### 6. Pin a Postal Mail Engagement

This is not a direct API call.  To pin a postal mail engagement to a record, include the postal mail's `id` in the `hs_pinned_engagement_id` field when creating or updating the record via the relevant object API (Contacts, Companies, etc.).


### 7. Delete a Postal Mail Engagement

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}`

**Response:** A confirmation of the successful deletion.


## Error Handling

The API will return standard HTTP status codes to indicate success or failure.  Error responses will include a JSON object with details about the error.


## Authentication

Refer to the HubSpot API documentation for authentication details.  Typically, this involves using an API key.


This documentation provides a concise overview.  Refer to the official HubSpot API documentation for complete details, including rate limits and other important information.
