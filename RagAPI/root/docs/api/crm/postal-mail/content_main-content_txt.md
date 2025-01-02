# HubSpot Postal Mail Engagement API Documentation

This document details the HubSpot API for managing postal mail engagements.  It covers creating, retrieving, updating, associating, and deleting postal mail entries within the HubSpot CRM.

## API Endpoints Base URL: `/crm/v3/objects/postal_mail`

All endpoints below are relative to this base URL.  Replace `{postalMail}` with the actual ID of the postal mail engagement.


## 1. Create a Postal Mail Engagement

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/postal_mail`

**Request Body:**

The request body must contain a `properties` object and optionally an `associations` array.

**Properties Object:**

| Field                | Description                                                              | Type      |
|-----------------------|--------------------------------------------------------------------------|-----------|
| `hs_timestamp`        | Date and time the postal mail was sent or received (YYYY-MM-DD).            | String    |
| `hs_postal_mail_body` | Body text of the postal mail engagement.                                  | String    |
| `hubspot_owner_id`    | ID of the user who created the engagement.                               | String    |
| `hs_attachment_ids`   | IDs of attached files, separated by semicolons.                            | String    |


**Associations Object:** (Optional, but recommended for associating with CRM records)

The `associations` array contains objects, each associating the postal mail with a record.

```json
[
  {
    "to": {
      "id": 501 // ID of the associated record (e.g., Contact ID)
    },
    "types": [
      {
        "associationCategory": "HUBSPOT_DEFINED",
        "associationTypeId": 453 // Association type ID. See note below.
      }
    ]
  },
  {
    "to": {
      "id": 502 // ID of another associated record
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

**Note:**  `associationTypeId` represents the type of association (e.g., `POSTAL_MAIL_TO_CONTACT`).  Default IDs are listed in the HubSpot documentation; use the Associations API for custom types.

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
      "to": {"id": 123},
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 453}]
    }
  ]
}
```

**Response:** (On success)  A JSON object representing the created postal mail engagement, including its ID.


## 2. Retrieve Postal Mail Engagements

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}` (Individual) or `/crm/v3/objects/postal_mail` (List)


**Individual Retrieval Parameters:**

| Parameter    | Description                                         | Type     |
|---------------|-----------------------------------------------------|----------|
| `properties` | Comma-separated list of properties to return.       | String   |
| `associations`| Comma-separated list of object types for associated IDs.| String   |

**List Retrieval Parameters:**

| Parameter    | Description                                               | Type     |
|---------------|-----------------------------------------------------------|----------|
| `limit`       | Maximum number of results per page.                       | Integer  |
| `properties` | Comma-separated list of properties to return.               | String   |


**Example (Individual):**  `GET /crm/v3/objects/postal_mail/1234?properties=hs_timestamp,hs_postal_mail_body`

**Example (List):** `GET /crm/v3/objects/postal_mail?limit=10`

**Response:** (Individual) A JSON object representing the postal mail engagement. (List) A JSON object with a list of postal mail engagements.



## 3. Update a Postal Mail Engagement

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}`

**Request Body:**

An object containing the properties to update.  Omit properties to leave them unchanged.  An empty string ("") will clear a property value.

**Example Request Body:**

```json
{
  "properties": {
    "hs_postal_mail_body": "Updated body text"
  }
}
```

**Response:** (On success) A JSON object representing the updated postal mail engagement.


## 4. Associate Existing Postal Mail with Records

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Parameters:**

| Parameter       | Description                                          | Type     |
|-----------------|------------------------------------------------------|----------|
| `postalMail`    | ID of the postal mail engagement.                   | String   |
| `toObjectType`  | Object type to associate (e.g., `contact`, `company`). | String   |
| `toObjectId`    | ID of the object to associate.                        | String   |
| `associationTypeId` | Association type ID.                               | String or Integer |


**Example URL:** `PUT /crm/v3/objects/postal_mail/5678/associations/contact/9101/POSTAL_MAIL_TO_CONTACT`

**Response:** (On success)  Confirmation of successful association.


## 5. Remove an Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Parameters:**  Same as for associating existing postal mail.

**Response:** (On success) Confirmation of successful removal of association.


## 6. Pin a Postal Mail Engagement

Postal mail is pinned to a record via the `hs_pinned_engagement_id` field when creating or updating the record using other object APIs (Contacts, Companies, etc.).


## 7. Delete a Postal Mail Engagement

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/postal_mail/{postalMail}`

**Response:** (On success) Confirmation of successful deletion.  The engagement is moved to the recycle bin.


This documentation provides a concise overview. Refer to the official HubSpot API documentation for complete details, error codes, and rate limits.
