# HubSpot Postal Mail Engagement API Documentation

This document details the HubSpot Postal Mail Engagement API, allowing you to manage postal mail engagements within the HubSpot CRM.  You can create, retrieve, update, associate, and delete postal mail engagements via various HTTP requests.

## API Endpoints Base URL: `/crm/v3/objects/postal_mail`

All endpoints below use this base URL unless otherwise specified.  Replace `{postalMail}` with the unique ID of the postal mail engagement.

## 1. Create a Postal Mail Engagement

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/postal_mail`

**Request Body:**

The request body contains a `properties` object (required) and an optional `associations` object.

**`properties` Object:**

| Field             | Description                                                                     | Type     | Example                               |
|----------------------|---------------------------------------------------------------------------------|-----------|---------------------------------------|
| `hs_timestamp`      | Date the postal mail was sent or received.                                     | String   | `"2024-10-27"`                         |
| `hs_postal_mail_body` | Body text of the postal mail engagement.                                        | String   | `"Sent contract to John Doe"`         |
| `hubspot_owner_id`   | ID of the user who created the engagement.                                     | String   | `"12345"`                             |
| `hs_attachment_ids` | IDs of attachments (semicolon-separated).                                      | String   | `"67890;123456"`                       |


**`associations` Object (Optional):**

This object allows associating the postal mail with existing records (contacts, companies, etc.).  You can associate with multiple records.

```json
[
  {
    "to": {
      "id": 501  // ID of the record
    },
    "types": [
      {
        "associationCategory": "HUBSPOT_DEFINED",
        "associationTypeId": 453 //  Association type ID (See HubSpot documentation for available IDs)
      }
    ]
  },
  {
    "to": {
      "id": 502
    },
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
    "hs_postal_mail_body": "Sent contract to John Doe",
    "hubspot_owner_id": "12345",
    "hs_attachment_ids": "67890;123456"
  },
  "associations": [
    {
      "to": {"id": 501},
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 453}]
    }
  ]
}
```

**Response:** (Success)  A JSON object representing the created postal mail engagement, including its ID.


## 2. Retrieve Postal Mail Engagements

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/postal_mail` (for a list) or `/crm/v3/objects/postal_mail/{postalMail}` (for a single engagement)

**Parameters (for list retrieval):**

| Parameter | Description                                     | Type    |
|-----------|-------------------------------------------------|---------|
| `limit`   | Max number of results per page.                  | Integer |
| `properties` | Comma-separated list of properties to return.    | String  |
| `associations` | Comma-separated list of object types for associated IDs. | String |


**Parameters (for single engagement retrieval):**

| Parameter | Description                                     | Type    |
|-----------|-------------------------------------------------|---------|
| `properties` | Comma-separated list of properties to return.    | String  |
| `associations` | Comma-separated list of object types for associated IDs. | String |

**Response:** (Success) A JSON object or array of JSON objects representing the postal mail engagements.


## 3. Update Postal Mail Engagements

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}`

**Request Body:**

Contains the `properties` object with fields to update.  Omit fields you don't want to change.  An empty string clears a property value.

**Example Request:**

```json
{
  "properties": {
    "hs_postal_mail_body": "Sent contract; follow-up call scheduled."
  }
}
```

**Response:** (Success) A JSON object representing the updated postal mail engagement.


## 4. Associate Existing Postal Mail with Records

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Parameters:**

| Parameter      | Description                                       | Type    |
|-----------------|---------------------------------------------------|---------|
| `postalMail`    | ID of the postal mail engagement.                  | Integer |
| `toObjectType` | Type of object to associate (e.g., `contact`, `company`) | String  |
| `toObjectId`   | ID of the record to associate.                     | Integer |
| `associationTypeId` | ID of the association type.                     | Integer |


**Example URL:**

`https://api.hubspot.com/crm/v3/objects/postal_mail/25727582880/associations/contact/104901/POSTAL_MAIL_TO_CONTACT`


## 5. Remove an Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

(Same parameters as associating)


## 6. Pin a Postal Mail Engagement

Pinning is handled indirectly through the `hs_pinned_engagement_id` field when creating or updating a record using other HubSpot object APIs (contacts, companies, etc.).  This field takes the postal mail's ID.


## 7. Delete Postal Mail Engagements

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}`

Deletes the engagement and moves it to the recycling bin.


**Note:**  Refer to the HubSpot developer documentation for detailed information on error codes, authentication, rate limits, and batch operations.  This documentation provides a concise overview of the core API functionality.
