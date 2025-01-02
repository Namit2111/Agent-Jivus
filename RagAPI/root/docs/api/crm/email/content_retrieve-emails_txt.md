# HubSpot Email Engagement API Documentation

This document details the HubSpot Email Engagement API, allowing you to log and manage emails associated with CRM records.  You can interact with emails either directly within HubSpot or through this API.

## API Endpoints

All endpoints are under the `/crm/v3/objects/emails` base path.  Remember to replace `{emailId}` and `{toObjectId}` with the appropriate IDs.

**Base URL:**  `https://api.hubspot.com/crm/v3/objects/emails`


## Methods

### 1. Create an Email (POST `/crm/v3/objects/emails`)

Creates a new email engagement.

**Request Body:**

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27T12:00:00Z", // Required. Unix timestamp (milliseconds) or UTC format
    "hubspot_owner_id": "12345", // ID of the email owner
    "hs_email_direction": "EMAIL", // EMAIL, INCOMING_EMAIL, FORWARDED_EMAIL
    "hs_email_status": "SENT", // BOUNCED, FAILED, SCHEDULED, SENDING, SENT
    "hs_email_subject": "Test Email",
    "hs_email_text": "Email body text",
    "hs_email_html": "<html>Email body HTML</html>", //Optional
    "hs_attachment_ids": "123;456", // Multiple IDs separated by semicolons. Optional
    "hs_email_headers": "{\"from\":{\"email\":\"from@domain.com\",\"firstName\":\"FromFirst\",\"lastName\":\"FromLast\"},\"to\":[{\"email\":\"to@domain.com\",\"firstName\":\"ToFirst\",\"lastName\":\"ToLast\"}],\"cc\":[],\"bcc\":[]}" // JSON escaped string, see below for details.
  },
  "associations": [ // Optional: Associate with records
    {
      "to": {"id": 601},
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 210}] //  See default and custom association type IDs
    }
  ]
}
```

**`hs_email_headers` Details:** This field is a JSON escaped string.  It populates read-only properties.

**Example `hs_email_headers` JSON:**

```json
{
  "from": {
    "email": "from@domain.com",
    "firstName": "FromFirst",
    "lastName": "FromLast"
  },
  "to": [
    {
      "email": "to@domain.com",
      "firstName": "ToFirst",
      "lastName": "ToLast"
    }
  ],
  "cc": [],
  "bcc": []
}
```

**Response:**  A JSON object representing the newly created email, including its ID.


### 2. Retrieve an Email (GET `/crm/v3/objects/emails/{emailId}`)

Retrieves a single email by its ID.

**Request Parameters:**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.

**Example Request:** `GET /crm/v3/objects/emails/1234?properties=hs_email_subject,hs_email_text`

**Response:** A JSON object representing the email.


### 3. Retrieve Emails (GET `/crm/v3/objects/emails`)

Retrieves a list of emails.

**Request Parameters:**

* `limit`: Maximum number of results per page.
* `properties`: Comma-separated list of properties to return.

**Response:** A JSON object containing a list of emails and pagination information.


### 4. Update an Email (PATCH `/crm/v3/objects/emails/{emailId}`)

Updates an existing email.

**Request Body:**

```json
{
  "properties": {
    "hs_email_subject": "Updated Subject"
  }
}
```

**Response:** A JSON object representing the updated email.


### 5. Associate Existing Email with Records (PUT `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates an email with a record (e.g., contact, deal).

**Request URL Parameters:**

* `emailId`: ID of the email.
* `toObjectType`: Type of object (e.g., `contact`, `deal`).
* `toObjectId`: ID of the object.
* `associationTypeId`: ID of the association type (see default and custom IDs).


### 6. Remove an Association (DELETE `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Removes an association between an email and a record.  Uses the same URL as the association method.


### 7. Pin an Email (Update Record via Object APIs)

Pin an email to a record's timeline.  This requires updating the record using its respective API (contacts, deals, etc.) and including the email's `id` in the `hs_pinned_engagement_id` property.


### 8. Delete an Email (DELETE `/crm/v3/objects/emails/{emailId}`)

Permanently deletes an email.


## Read-Only Properties

These properties are automatically populated from `hs_email_headers`.

* `hs_email_from_email`
* `hs_email_from_firstname`
* `hs_email_from_lastname`
* `hs_email_to_email`
* `hs_email_to_firstname`
* `hs_email_to_lastname`


## Error Handling

The API will return standard HTTP status codes and JSON error responses indicating the nature of any issues.


## Rate Limits

Be mindful of HubSpot's API rate limits to avoid throttling.


This documentation provides a comprehensive overview of the HubSpot Email Engagement API.  Refer to the HubSpot Developer documentation for the most up-to-date information and details on batch operations.
