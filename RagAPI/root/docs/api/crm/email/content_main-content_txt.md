# HubSpot Email Engagement API Documentation

This document describes the HubSpot Email Engagement API, allowing you to log and manage emails associated with CRM records.  You can interact with the API using various HTTP methods (POST, GET, PATCH, PUT, DELETE).  All API calls require authentication with a HubSpot API key.

## API Endpoints

All endpoints are under the base URL: `/crm/v3/objects/emails`

##  Methods

### 1. Create an Email (POST `/crm/v3/objects/emails`)

Creates a new email engagement.

**Request Body:**

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27T12:00:00.000Z",  // Required. Unix timestamp (milliseconds) or UTC format
    "hubspot_owner_id": "12345", // ID of the email owner
    "hs_email_direction": "EMAIL", // EMAIL, INCOMING_EMAIL, FORWARDED_EMAIL
    "hs_email_status": "SENT", // BOUNCED, FAILED, SCHEDULED, SENDING, SENT
    "hs_email_subject": "Test Email",
    "hs_email_text": "Email body text",
    "hs_email_html": "<html>Email body HTML</html>", //Optional
    "hs_attachment_ids": "123;456", //Multiple IDs separated by semicolon. Optional.
    "hs_email_headers": "{\"from\":{\"email\":\"from@example.com\",\"firstName\":\"FromFirst\",\"lastName\":\"FromLast\"},\"to\":[{\"email\":\"to@example.com\",\"firstName\":\"ToFirst\",\"lastName\":\"ToLast\"}],\"cc\":[],\"bcc\":[]}" //JSON escaped string.  See "Set Email Headers" section.
  },
  "associations": [ //Optional. Associate with records. See "Associations" section.
    {
      "to": {"id": 601},
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 210}]
    }
  ]
}
```

**Response:**  A JSON object representing the created email, including its ID.

**Example Response:**

```json
{
  "id": "123456789",
  // ... other properties ...
}
```


### 2. Retrieve Emails (GET `/crm/v3/objects/emails`)

Retrieves a list of emails.  For individual email retrieval, use GET `/crm/v3/objects/emails/{emailId}`.

**Query Parameters:**

* `limit`: Number of results per page.
* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.


**Example Request (GET `/crm/v3/objects/emails?limit=10&properties=hs_email_subject,hs_email_direction`):**


**Example Response (JSON array of email objects):**

```json
[
  {
    "id": "123456789",
    "properties": {
      "hs_email_subject": "Email 1",
      "hs_email_direction": "EMAIL"
    }
  },
  // ... more emails ...
]
```


### 3. Update an Email (PATCH `/crm/v3/objects/emails/{emailId}`)

Updates an existing email.

**Request Body:**

```json
{
  "properties": {
    "hs_email_subject": "Updated Subject",
    "hs_email_status": "SENT"
  }
}
```

**Response:** A JSON object representing the updated email.


### 4. Associate Existing Emails with Records (PUT `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates an email with a record (e.g., contact, deal).

**Path Parameters:**

* `emailId`: The ID of the email.
* `toObjectType`: The type of object (e.g., `contact`, `deal`).
* `toObjectId`: The ID of the object.
* `associationTypeId`:  The ID of the association type (obtainable via the Associations API).

**Example Request URL:**  `https://api.hubspot.com/crm/v3/objects/emails/12345/associations/contact/67890/198`

**Response:** Success/failure status.


### 5. Remove an Association (DELETE `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Removes an association between an email and a record.  Uses the same path parameters as the `PUT` association method.


### 6. Pin an Email (Update record via object APIs)

Pinning is not a direct email API call. To pin an email on a record, include the email's `id` in the `hs_pinned_engagement_id` field when creating or updating the associated record (contact, deal, etc.) using the respective object API.


### 7. Delete an Email (DELETE `/crm/v3/objects/emails/{emailId}`)

Permanently deletes an email.  Cannot be restored.


##  Properties

### Writable Properties

* `hs_timestamp`: (Required) Email creation timestamp (Unix milliseconds or UTC).
* `hubspot_owner_id`: ID of the email owner.
* `hs_email_direction`:  `EMAIL`, `INCOMING_EMAIL`, `FORWARDED_EMAIL`.
* `hs_email_status`: `BOUNCED`, `FAILED`, `SCHEDULED`, `SENDING`, `SENT`.
* `hs_email_subject`: Email subject.
* `hs_email_text`: Email body (plain text).
* `hs_email_html`: Email body (HTML).
* `hs_attachment_ids`: IDs of attachments (semicolon-separated).
* `hs_email_headers`: (JSON escaped string)  See "Set Email Headers" section.


### Read-only Properties (populated from `hs_email_headers`)

* `hs_email_from_email`: Sender's email address.
* `hs_email_from_firstname`: Sender's first name.
* `hs_email_from_lastname`: Sender's last name.
* `hs_email_to_email`: Recipient's email address(es).
* `hs_email_to_firstname`: Recipient's first name(s).
* `hs_email_to_lastname`: Recipient's last name(s).


## Set Email Headers

The `hs_email_headers` property is a JSON-escaped string containing email header information.  This populates the read-only properties.

**Example `hs_email_headers` Value:**

```json
"{\"from\":{\"email\":\"from@example.com\",\"firstName\":\"FromFirst\",\"lastName\":\"FromLast\"},\"to\":[{\"email\":\"to@example.com\",\"firstName\":\"ToFirst\",\"lastName\":\"ToLast\"}],\"cc\":[],\"bcc\":[]}"
```

## Associations

To associate an email with CRM records, use the `associations` array in the request body when creating an email.

**Example `associations` Array:**

```json
"associations": [
  {
    "to": {"id": 601}, //ID of the record
    "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 210}] //associationTypeId depends on the object type.
  }
]
```

You need to obtain the correct `associationTypeId` using the HubSpot Associations API.


## Error Handling

The API returns standard HTTP status codes (e.g., 400 Bad Request, 404 Not Found, 500 Internal Server Error) along with JSON error responses providing details.


This documentation provides a comprehensive overview of the HubSpot Email Engagement API. Refer to the official HubSpot API documentation for the most up-to-date information and detailed specifications for all endpoints and parameters.
