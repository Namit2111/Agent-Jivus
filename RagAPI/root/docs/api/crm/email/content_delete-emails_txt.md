# HubSpot Email Engagement API Documentation

This document details the HubSpot Email Engagement API, allowing you to log and manage emails associated with CRM records.  You can interact with emails either directly through the HubSpot UI or via this API.

## API Endpoints

All endpoints are under the `/crm/v3/objects/emails` base path.  Remember to replace placeholders like `{emailId}` with actual values.

## Methods

### 1. Create an Email (POST `/crm/v3/objects/emails`)

Creates a new email engagement.

**Request Body:**

```json
{
  "properties": {
    "hs_timestamp": "2024-10-26T12:00:00.000Z", // Required. Unix timestamp (milliseconds) or UTC format.
    "hubspot_owner_id": "12345", // ID of the email owner.
    "hs_email_direction": "EMAIL", // "EMAIL", "INCOMING_EMAIL", or "FORWARDED_EMAIL"
    "hs_email_html": "<html>Email Body</html>", // HTML body (optional)
    "hs_email_status": "SENT", // "BOUNCED", "FAILED", "SCHEDULED", "SENDING", or "SENT"
    "hs_email_subject": "Test Email",
    "hs_email_text": "Plain text email body",
    "hs_attachment_ids": "123;456", // Multiple IDs separated by semicolons (optional)
    "hs_email_headers": "{\"from\":{\"email\":\"from@example.com\",\"firstName\":\"John\",\"lastName\":\"Doe\"},\"to\":[{\"email\":\"to@example.com\",\"firstName\":\"Jane\",\"lastName\":\"Doe\"}],\"cc\":[],\"bcc\":[]}" // JSON escaped string (see below)
  },
  "associations": [ // Optional: associate with records
    {
      "to": {"id": 601}, // ID of the record
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 210}] // Association type (see Default Association Type IDs)
    }
  ]
}
```

**`hs_email_headers` Example:**  This field is a JSON escaped string.  It populates read-only properties.

```json
{
  "from": {
    "email": "from@domain.com",
    "firstName": "FromFirst",
    "lastName": "FromLast"
  },
  "to": [
    {
      "email": "to@example.com",
      "firstName": "ToFirst",
      "lastName": "ToLast"
    }
  ],
  "cc": [],
  "bcc": []
}
```

**Response:**  A JSON object representing the created email, including its ID.


### 2. Retrieve an Email (GET `/crm/v3/objects/emails/{emailId}`)

Retrieves a single email.

**Request Parameters:**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.

**Response:** A JSON object representing the email.

**Example:** GET `/crm/v3/objects/emails/12345?properties=hs_email_subject,hs_email_text`


### 3. Retrieve Emails (GET `/crm/v3/objects/emails`)

Retrieves a list of emails.

**Request Parameters:**

* `limit`: Maximum number of results per page.
* `properties`: Comma-separated list of properties to return.

**Response:** A JSON object containing a list of emails and pagination information.


### 4. Update an Email (PATCH `/crm/v3/objects/emails/{emailId}`)

Updates an existing email.

**Request Body:**  Similar to the POST request body, but only include the properties you want to modify.

**Example:**

```json
{
  "properties": {
    "hs_email_subject": "Updated Subject"
  }
}
```

**Response:** A JSON object representing the updated email.


### 5. Associate an Existing Email with a Record (PUT `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates an email with a CRM record.

**Request Parameters:**

* `emailId`: The ID of the email.
* `toObjectType`:  The type of object (e.g., `contact`, `company`).
* `toObjectId`: The ID of the record.
* `associationTypeId`: The ID of the association type (obtainable via the Associations API).


### 6. Remove an Association (DELETE `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Removes an association between an email and a record.  Uses the same URL structure as the PUT association method.


### 7. Pin an Email (Update Record via Object APIs)

Pins an email to the top of a record's timeline. This requires updating the record (contact, company, deal, etc.) using its respective object API and including the email's `id` in the `hs_pinned_engagement_id` property.


### 8. Delete an Email (DELETE `/crm/v3/objects/emails/{emailId}`)

Permanently deletes an email.


## Default Association Type IDs

You'll need these when associating emails with records.  Refer to the HubSpot documentation for the most up-to-date list.  Example: `210` might represent the association between an email and a deal.


##  Error Handling

The API will return standard HTTP status codes (e.g., 400 for bad requests, 404 for not found, etc.) along with JSON error messages providing details about any issues.


This documentation provides a concise overview.  Consult the official HubSpot API documentation for the most complete and up-to-date information.
