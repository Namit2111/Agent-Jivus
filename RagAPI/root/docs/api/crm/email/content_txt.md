# HubSpot Email Engagement API Documentation

This document details the HubSpot Email Engagement API, allowing you to log and manage emails associated with CRM records.  You can interact with emails either directly within HubSpot or programmatically via this API.

## API Endpoints

All endpoints are under the `/crm/v3/objects/emails` base path.  Remember to replace placeholders like `{emailId}` with actual values.  Authentication is required (details not provided in the source text).

##  Methods

### 1. Create an Email (POST `/crm/v3/objects/emails`)

Creates a new email engagement.

**Request Body:**

```json
{
  "properties": {
    "hs_timestamp": "2019-10-30T03:30:17.883Z", // Required. Unix timestamp (milliseconds) or UTC format.
    "hubspot_owner_id": "47550177", // ID of the email owner.
    "hs_email_direction": "EMAIL", // "EMAIL", "INCOMING_EMAIL", or "FORWARDED_EMAIL"
    "hs_email_status": "SENT", // "BOUNCED", "FAILED", "SCHEDULED", "SENDING", or "SENT"
    "hs_email_subject": "Let's talk",
    "hs_email_text": "Thanks for your email",
    "hs_email_html": "Email body in HTML", // Optional - Body of email if sent from CRM record.
    "hs_attachment_ids": "123;456", // Optional - Semicolon-separated list of attachment IDs.
    "hs_email_headers": "{\"from\":{\"email\":\"from@domain.com\",\"firstName\":\"FromFirst\",\"lastName\":\"FromLast\"},\"sender\":{\"email\":\"sender@domain.com\",\"firstName\":\"SenderFirst\",\"lastName\":\"SenderLast\"},\"to\":[{\"email\":\"ToFirst+ToLast<to@test.com>\",\"firstName\":\"ToFirst\",\"lastName\":\"ToLast\"}],\"cc\":[],\"bcc\":[]}" // JSON-escaped string; see below for structure.
  },
  "associations": [ // Optional - Associate with existing records
    {
      "to": {"id": 601}, // ID of the record
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 210}] // Association type; see below for details.
    },
    {
      "to": {"id": 602},
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 198}]
    }
  ]
}
```

**`hs_email_headers` Structure:**

This field uses a JSON-escaped string with the following structure:

```json
{
  "from": {
    "email": "from@domain.com",
    "firstName": "FromFirst",
    "lastName": "FromLast"
  },
  "to": [
    {
      "email": "ToFirst ToLast<to@test.com>",
      "firstName": "ToFirst",
      "lastName": "ToLast"
    }
  ],
  "cc": [],
  "bcc": []
}
```

**Associations:**

*   `to.id`: ID of the record to associate (e.g., contact, deal).
*   `types.associationTypeId`:  Association type ID.  Default IDs are listed in the HubSpot documentation;  custom types can be retrieved using the Associations API.


**Response:**  A JSON object representing the created email, including its ID.

### 2. Retrieve an Email (GET `/crm/v3/objects/emails/{emailId}`)

Retrieves a single email by its ID.

**Query Parameters:**

*   `properties`: Comma-separated list of properties to return.
*   `associations`: Comma-separated list of object types to retrieve associated IDs for.


**Response:** A JSON object representing the email.

### 3. Retrieve Emails (GET `/crm/v3/objects/emails`)

Retrieves a list of emails.

**Query Parameters:**

*   `limit`: Maximum number of results per page.
*   `properties`: Comma-separated list of properties to return.

**Response:** A JSON object containing a list of emails and pagination information.

### 4. Update an Email (PATCH `/crm/v3/objects/emails/{emailId}`)

Updates an existing email.

**Request Body:**

```json
{
  "properties": {
    "hs_timestamp": "updated_timestamp",
    "hs_email_subject": "Updated subject",
    // ... other properties to update
  }
}
```

**Response:** A JSON object representing the updated email.  Read-only properties will be ignored.  To clear a property, send an empty string.


### 5. Associate Existing Email with Records (PUT `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates an email with a record.

**Path Parameters:**

*   `emailId`: The email's ID.
*   `toObjectType`: Object type (e.g., "contact", "company").
*   `toObjectId`: The record's ID.
*   `associationTypeId`: Association type ID.


**Response:**  A success or error response.

### 6. Remove an Association (DELETE `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Removes an association between an email and a record.  Uses the same path parameters as the association method.

**Response:** A success or error response.

### 7. Pin an Email (Update Record via Object APIs)

Pins an email to a record's timeline. This is done by including the email's `id` in the `hs_pinned_engagement_id` field when creating or updating the associated record (contact, company, deal, etc.) using the respective object APIs.


### 8. Delete an Email (DELETE `/crm/v3/objects/emails/{emailId}`)

Permanently deletes an email.

**Response:** A success or error response.


## Read-Only Properties

Several properties are automatically populated by HubSpot based on the `hs_email_headers` value:

*   `hs_email_from_email`
*   `hs_email_from_firstname`
*   `hs_email_from_lastname`
*   `hs_email_to_email`
*   `hs_email_to_firstname`
*   `hs_email_to_lastname`


## Error Handling

The API will return appropriate HTTP status codes and error messages in the response body to indicate success or failure of requests.  Specific error codes are not detailed in the provided text.


This documentation summarizes the key aspects of the HubSpot Email Engagement API.  For comprehensive details, including batch operations and complete endpoint specifications, refer to the official HubSpot API documentation.
