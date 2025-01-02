# HubSpot Postal Mail Engagement API Documentation

This document details the HubSpot Postal Mail Engagement API, allowing you to manage postal mail engagements within the HubSpot CRM.  This includes creating, retrieving, updating, associating, and deleting postal mail records.

## API Endpoints

All endpoints are under the `/crm/v3/objects/postal_mail` base path.  You'll need a valid HubSpot API key for authentication.

### 1. Create a Postal Mail Engagement

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/postal_mail`

**Request Body:**

The request body must contain a `properties` object and optionally an `associations` array.

* **`properties` (object):**
    * `hs_timestamp` (string):  Date and time of sending/receiving the mail (ISO 8601 format, e.g., "2024-10-27T10:30:00").
    * `hs_postal_mail_body` (string): The content of the postal mail.
    * `hubspot_owner_id` (string): ID of the HubSpot user who created the engagement.
    * `hs_attachment_ids` (string): IDs of attached files, separated by semicolons.

* **`associations` (array, optional):**  Associates the postal mail with existing records (Contacts, Companies, etc.). Each array element is an object:
    * `to` (object):
        * `id` (integer): ID of the record to associate.
    * `types` (array):
        * `associationCategory` (string): `"HUBSPOT_DEFINED"`
        * `associationTypeId` (integer):  The association type ID (see [Associations API](link_to_associations_api_doc_here)).  Examples include 453 for contact associations.


**Example Request:**

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27T10:30:00",
    "hs_postal_mail_body": "Sent contract to John Doe",
    "hubspot_owner_id": "12345",
    "hs_attachment_ids": "67890;123456"
  },
  "associations": [
    {
      "to": { "id": 501 },
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 453 }]
    }
  ]
}
```

**Response:**  A JSON object representing the created postal mail engagement, including its ID.


### 2. Retrieve Postal Mail Engagements

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/postal_mail` (for list) or `/crm/v3/objects/postal_mail/{postalMailId}` (for single)


**Parameters (for list):**

* `limit` (integer): Maximum number of results per page.
* `properties` (string): Comma-separated list of properties to return.


**Parameters (for single):**

* `properties` (string): Comma-separated list of properties to return.
* `associations` (string): Comma-separated list of association types to retrieve associated IDs for.

**Example Request (Single):**

```
GET /crm/v3/objects/postal_mail/12345?properties=hs_timestamp,hs_postal_mail_body
```


**Response:** A JSON object (single) or a JSON array (list) containing the requested postal mail engagements.


### 3. Update a Postal Mail Engagement

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/postal_mail/{postalMailId}`

**Request Body:**

An object containing the properties to update.  Omitted properties remain unchanged.  An empty string clears a property value.

**Example Request:**

```json
{
  "properties": {
    "hs_postal_mail_body": "Contract sent. Follow-up call scheduled."
  }
}
```

**Response:** A JSON object representing the updated postal mail engagement.


### 4. Associate Existing Postal Mail with Records

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/postal_mail/{postalMailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Parameters:**

* `postalMailId` (integer): ID of the postal mail engagement.
* `toObjectType` (string): Type of object to associate (e.g., "contact", "company").
* `toObjectId` (integer): ID of the object to associate.
* `associationTypeId` (integer or string): Association type ID (numerical or snake_case).


**Example Request:**

```
PUT /crm/v3/objects/postal_mail/12345/associations/contact/67890/POSTAL_MAIL_TO_CONTACT
```

**Response:**  A success/failure indication.



### 5. Remove an Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/postal_mail/{postalMailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Parameters:**  Same as Associate Existing Postal Mail.

**Response:** A success/failure indication.


### 6. Pin a Postal Mail Engagement (Indirectly)

Pinning is done indirectly by including the `hs_pinned_engagement_id` property in the record's update request (using the Contacts, Companies, etc. APIs).  This is not a direct postal mail API call.


### 7. Delete a Postal Mail Engagement

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/postal_mail/{postalMailId}`

**Response:** A success/failure indication.


## Error Handling

The API will return standard HTTP status codes (e.g., 400 for bad requests, 404 for not found, 500 for server errors) along with JSON error messages providing details.


## Rate Limits

Consult the HubSpot API documentation for rate limits to avoid exceeding allowed request frequency.


This documentation provides a concise overview.  Refer to the official HubSpot API documentation for complete details, including advanced features and error handling.
