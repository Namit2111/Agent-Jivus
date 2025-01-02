# HubSpot Email Engagement API Documentation

This document describes the HubSpot Email Engagement API, allowing you to log and manage emails associated with CRM records.  You can interact with the API via various HTTP methods (POST, GET, PATCH, PUT, DELETE).  All endpoints are under the `/crm/v3/objects/emails` base path.


## API Endpoints

All endpoints use the base URL: `/crm/v3/objects/emails`

### 1. Create an Email (POST `/crm/v3/objects/emails`)

Creates a new email engagement.

**Request Body:**

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27T12:00:00Z",  // Required. Unix timestamp (milliseconds) or UTC format
    "hubspot_owner_id": "12345",            // ID of the email owner
    "hs_email_direction": "EMAIL",          // EMAIL, INCOMING_EMAIL, FORWARDED_EMAIL
    "hs_email_status": "SENT",              // BOUNCED, FAILED, SCHEDULED, SENDING, SENT
    "hs_email_subject": "Example Email",    // Subject of the email
    "hs_email_text": "Email body text",      // Email body (plain text)
    "hs_email_html": "<html>Email body HTML</html>", // Email body (HTML) - optional
    "hs_attachment_ids": "123;456",         // IDs of attachments (semicolon separated) - optional
    "hs_email_headers": "{\"from\":{\"email\":\"from@example.com\",\"firstName\":\"John\",\"lastName\":\"Doe\"},\"to\":[{\"email\":\"recipient@example.com\",\"firstName\":\"Jane\",\"lastName\":\"Doe\"}]}" // JSON escaped string of email headers (see below)
  },
  "associations": [  //Optional: Associate with existing records
    {
      "to": {"id": 601},
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 210}] // e.g., association with a deal
    }
  ]
}
```

**Example using `curl`:**

```bash
curl -X POST \
  https://api.hubspot.com/crm/v3/objects/emails \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -d '{ "properties": { ... } }'
```

**Response (201 Created):**  A JSON object representing the created email, including its ID.


### 2. Set Email Headers (`hs_email_headers` Property)

The `hs_email_headers` property is a JSON escaped string.  It populates read-only properties.


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
      "email": "ToFirst ToLast<to@test.com>",
      "firstName": "ToFirst",
      "lastName": "ToLast"
    }
  ],
  "cc": [],
  "bcc": []
}
```

This populates `hs_email_from_email`, `hs_email_from_firstname`, etc.


### 3. Read-only Properties

Several properties are automatically populated from `hs_email_headers`:

* `hs_email_from_email`
* `hs_email_from_firstname`
* `hs_email_from_lastname`
* `hs_email_to_email`
* `hs_email_to_firstname`
* `hs_email_to_lastname`


### 4. Retrieve an Email (GET `/crm/v3/objects/emails/{emailId}`)

Retrieves a specific email by its ID.

**Query Parameters:**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.


**Example using `curl`:**

```bash
curl -X GET \
  https://api.hubspot.com/crm/v3/objects/emails/12345 \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

**Response (200 OK):** A JSON object representing the email.


### 5. Retrieve Emails (GET `/crm/v3/objects/emails`)

Retrieves a list of emails.

**Query Parameters:**

* `limit`: Maximum number of results per page.
* `properties`: Comma-separated list of properties to return.


### 6. Update an Email (PATCH `/crm/v3/objects/emails/{emailId}`)

Updates an existing email.

**Request Body:**

Similar to the POST request, but only include the properties you want to modify.


### 7. Associate Existing Email with Records (PUT `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)


Associates an existing email with a record (e.g., contact, deal).

**Path Parameters:**

* `emailId`: ID of the email.
* `toObjectType`: Type of object (e.g., `contact`, `deal`).
* `toObjectId`: ID of the record.
* `associationTypeId`: ID of the association type.


### 8. Remove an Association (DELETE `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Removes an association between an email and a record.


### 9. Pin an Email (Update Record via Object APIs)

Pins an email to the top of a record's timeline using the `hs_pinned_engagement_id` field when updating the record via its respective object API (contacts, deals, etc.).


### 10. Delete an Email (DELETE `/crm/v3/objects/emails/{emailId}`)

Permanently deletes an email.


## Error Handling

The API returns standard HTTP status codes to indicate success or failure.  Error responses include details in the JSON body.


## Rate Limits

Be mindful of HubSpot's API rate limits to avoid exceeding them.


## Authentication

Use your HubSpot API key in the `Authorization` header as `Bearer YOUR_API_KEY`.


This comprehensive documentation provides a clear understanding of how to utilize the HubSpot Email Engagement API effectively. Remember to consult the official HubSpot API documentation for the most up-to-date information and details on batch operations.
