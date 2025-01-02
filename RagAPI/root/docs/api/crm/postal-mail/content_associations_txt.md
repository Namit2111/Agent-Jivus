# HubSpot Postal Mail Engagement API

This document describes the HubSpot API for managing postal mail engagements.  It allows you to log, retrieve, update, and delete postal mail associated with CRM records.

## API Endpoints

All endpoints are under the `/crm/v3/objects/postal_mail` base path.  Remember to replace `{postalMail}` with the actual postal mail ID.

### 1. Create a Postal Mail Engagement

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/postal_mail`

**Request Body:**

The request body must contain a `properties` object and optionally an `associations` object.

```json
{
  "properties": {
    "hs_timestamp": "YYYY-MM-DD", // Date sent/received
    "hs_postal_mail_body": "Postal mail content",
    "hubspot_owner_id": 12345, // HubSpot user ID
    "hs_attachment_ids": "123;456;789" // Multiple attachment IDs separated by semicolons
  },
  "associations": [
    {
      "to": {
        "id": 501 // ID of the associated record (e.g., contact ID)
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 453 // Association type ID. See details below.
        }
      ]
    }
  ]
}
```

**Response:**  A JSON object representing the newly created postal mail engagement, including its ID.

**Association Type IDs:**  Default association type IDs are available in HubSpot's documentation. Custom association types can be retrieved using the HubSpot associations API.


### 2. Retrieve Postal Mail Engagements

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/postal_mail` (for multiple) or `/crm/v3/objects/postal_mail/{postalMail}` (for a single engagement)

**Parameters (for multiple):**

* `limit`: Maximum number of results per page.
* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.

**Parameters (for single):**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.


**Response:** A JSON object or array containing the requested postal mail engagements.


### 3. Update Postal Mail Engagements

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}`

**Request Body:**

```json
{
  "properties": {
    "hs_postal_mail_body": "Updated postal mail content"
  }
}
```

**Response:** A JSON object representing the updated postal mail engagement.

HubSpot ignores read-only and non-existent properties. To clear a property, pass an empty string.


### 4. Associate Existing Postal Mail with Records

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Parameters:**

* `postalMail`: ID of the postal mail engagement.
* `toObjectType`: Type of object (e.g., `contact`, `company`).
* `toObjectId`: ID of the record.
* `associationTypeId`: Association type ID (numeric or snake case).


### 5. Remove an Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Parameters:** Same as associating existing postal mail.


### 6. Pin a Postal Mail Engagement

This is done by including the postal mail's `id` in the `hs_pinned_engagement_id` field when creating or updating a record using the relevant object API (contacts, companies, deals, tickets, custom objects).


### 7. Delete Postal Mail Engagements

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}`

This moves the engagement to the recycle bin.  It can be restored from the record timeline.


## Error Handling

The API will return standard HTTP status codes and JSON error responses.  Refer to HubSpot's API documentation for detailed error codes and descriptions.


This documentation provides a concise overview.  Refer to the official HubSpot API documentation for exhaustive details and examples.
