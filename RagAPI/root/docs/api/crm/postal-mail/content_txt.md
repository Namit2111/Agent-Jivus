# HubSpot Postal Mail Engagement API Documentation

This document details the HubSpot Postal Mail Engagement API, allowing you to manage postal mail records within HubSpot.  You can create, retrieve, update, and delete postal mail engagements, and associate them with other HubSpot records (contacts, companies, etc.).

## API Endpoints

All endpoints are under the `/crm/v3/objects/postal_mail` base path.  Remember to replace placeholders like `{postalMail}` and `{toObjectId}` with actual IDs.

### 1. Create a Postal Mail Engagement

**Method:** `POST /crm/v3/objects/postal_mail`

**Request Body:**

```json
{
  "properties": {
    "hs_timestamp": "YYYY-MM-DD", // Date sent/received (ISO 8601 format)
    "hs_postal_mail_body": "Mail body text",
    "hubspot_owner_id": 12345, // HubSpot user ID
    "hs_attachment_ids": "123;456;789" // Semicolon-separated list of attachment IDs
  },
  "associations": [
    {
      "to": { "id": 501 }, // ID of the record to associate (e.g., contact ID)
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 453 // Association type ID (see below)
        }
      ]
    }
  ]
}
```

**Response:**  A JSON object representing the created postal mail engagement, including its ID.

**Example:**

```bash
curl -X POST \
  'https://api.hubspot.com/crm/v3/objects/postal_mail' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -d '{
    "properties": {
      "hs_timestamp": "2024-10-27",
      "hs_postal_mail_body": "Sent contract",
      "hubspot_owner_id": "12345",
      "hs_attachment_ids": "67890"
    },
    "associations": [
      {
        "to": {"id": 1001},
        "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 453}]
      }
    ]
  }'
```


### 2. Retrieve Postal Mail Engagements

**Method:** `GET /crm/v3/objects/postal_mail` (for multiple) or `GET /crm/v3/objects/postal_mail/{postalMailId}` (for a single engagement)

**Parameters (for multiple):**

* `limit`: Maximum number of results per page.
* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.

**Parameters (for single):**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.

**Response:** A JSON object (or array for multiple) containing the postal mail engagement details.

**Example (single):**

```bash
curl -X GET \
  'https://api.hubspot.com/crm/v3/objects/postal_mail/12345' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```


### 3. Update a Postal Mail Engagement

**Method:** `PATCH /crm/v3/objects/postal_mail/{postalMailId}`

**Request Body:**

```json
{
  "properties": {
    "hs_postal_mail_body": "Updated mail body"
  }
}
```

**Response:** A JSON object representing the updated postal mail engagement.


### 4. Associate Existing Postal Mail with Records

**Method:** `PUT /crm/v3/objects/postal_mail/{postalMailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Parameters:**

* `postalMailId`: ID of the postal mail engagement.
* `toObjectType`: Type of object to associate (e.g., `contact`, `company`).
* `toObjectId`: ID of the object to associate.
* `associationTypeId`: ID of the association type.

**Example:**

```bash
curl -X PUT \
  'https://api.hubspot.com/crm/v3/objects/postal_mail/12345/associations/contact/67890/POSTAL_MAIL_TO_CONTACT' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

### 5. Remove an Association

**Method:** `DELETE /crm/v3/objects/postal_mail/{postalMailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Parameters:** Same as associate existing postal mail.


### 6. Delete a Postal Mail Engagement

**Method:** `DELETE /crm/v3/objects/postal_mail/{postalMailId}`

**Response:** A success message or error code.


## Association Type IDs

You need to find the appropriate `associationTypeId` for your associations.  HubSpot's documentation should list default IDs, or you can use the HubSpot Associations API to retrieve them.


## Error Handling

The API will return standard HTTP status codes and JSON error responses to indicate success or failure.  Check the HubSpot API documentation for details on error codes.

## Authentication

Use your HubSpot API key for authentication in the `Authorization` header as `Bearer YOUR_API_KEY`.


This documentation provides a concise overview. Refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications.
