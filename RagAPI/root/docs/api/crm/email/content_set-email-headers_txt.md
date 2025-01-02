# HubSpot Email Engagement API Documentation

This document details the HubSpot Email Engagement API, allowing you to log and manage emails associated with CRM records.  You can interact with emails either directly within HubSpot or via this API.

## API Endpoints

All endpoints are located under the `/crm/v3/objects/emails` base path.  Remember to replace `{emailId}` and `{toObjectId}` with the actual IDs.

##  API Calls

### 1. Create an Email (`POST /crm/v3/objects/emails`)

Creates a new email engagement.

**Request Body:**

The request body uses a JSON structure with `properties` and optionally `associations` objects.

* **`properties` (required):** Contains email details.
    * `hs_timestamp` (required): Email creation timestamp.  Use Unix timestamp (milliseconds) or UTC format (e.g., "2024-10-27T10:00:00Z").
    * `hubspot_owner_id`: ID of the email owner (HubSpot user).
    * `hs_email_direction`:  `EMAIL`, `INCOMING_EMAIL`, or `FORWARDED_EMAIL`.
    * `hs_email_html`: Email body (HTML).
    * `hs_email_status`: `BOUNCED`, `FAILED`, `SCHEDULED`, `SENDING`, or `SENT`.
    * `hs_email_subject`: Email subject.
    * `hs_email_text`: Email body (plain text).
    * `hs_attachment_ids`: IDs of attached files (semicolon-separated).
    * `hs_email_headers`: JSON-escaped string containing email headers (see below).


* **`associations` (optional):**  Associates the email with other records (contacts, deals, etc.).  See below for details.

**Example Request (Creating an email with associations):**

```json
{
  "properties": {
    "hs_timestamp": 1698387200000,
    "hubspot_owner_id": "12345",
    "hs_email_direction": "EMAIL",
    "hs_email_status": "SENT",
    "hs_email_subject": "Test Email",
    "hs_email_text": "This is a test email.",
    "hs_email_headers": "{\"from\":{\"email\":\"sender@example.com\",\"firstName\":\"Sender\",\"lastName\":\"Name\"},\"to\":[{\"email\":\"recipient@example.com\",\"firstName\":\"Recipient\",\"lastName\":\"Name\"}]}"
  },
  "associations": [
    {
      "to": {"id": 601},
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 210}]
    }
  ]
}
```

**Response:** A JSON object representing the created email, including its ID.


### 2. Set Email Headers (`hs_email_headers` Property)

The `hs_email_headers` property accepts a JSON-escaped string.  This string should contain the following fields:

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

This will populate read-only properties like `hs_email_from_email`, `hs_email_to_email`, etc.

### 3. Associations

The `associations` object within the request body allows associating emails with other HubSpot records.

* **`to` (required):**  Object containing the `id` of the record to associate with.
* **`types` (required):** Array of association types. Each type needs `associationCategory` ("HUBSPOT_DEFINED") and `associationTypeId` (see HubSpot's documentation for available IDs).


### 4. Retrieve an Email (`GET /crm/v3/objects/emails/{emailId}`)

Retrieves a single email by its ID.

**Parameters:**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.

**Example:** `/crm/v3/objects/emails/123?properties=hs_email_subject,hs_email_text&associations=contact`


### 5. Retrieve Emails (`GET /crm/v3/objects/emails`)

Retrieves a list of emails.

**Parameters:**

* `limit`: Maximum number of results per page.
* `properties`: Comma-separated list of properties to return.


### 6. Update an Email (`PATCH /crm/v3/objects/emails/{emailId}`)

Updates an existing email.  Use the `properties` object to specify changes.  Read-only properties are ignored.

**Example Request:**

```json
{
  "properties": {
    "hs_email_subject": "Updated Subject"
  }
}
```


### 7. Associate an Existing Email with Records (`PUT /crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)


Associates an email with a record.

* `{emailId}`: Email ID
* `{toObjectType}`: Object type (e.g., "contact", "company").
* `{toObjectId}`: ID of the record.
* `{associationTypeId}`: Association type ID.


### 8. Remove an Association (`DELETE /crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)


Removes an association between an email and a record.  Uses the same URL structure as associating.


### 9. Pin an Email (Indirectly via Record APIs)

Pinning is done by including the email's `id` in the `hs_pinned_engagement_id` field when updating a record via its respective API (contacts, companies, deals, etc.).


### 10. Delete an Email (`DELETE /crm/v3/objects/emails/{emailId}`)

Permanently deletes an email.


## Read-Only Properties

Several properties are automatically populated by HubSpot based on the `hs_email_headers`:

* `hs_email_from_email`
* `hs_email_from_firstname`
* `hs_email_from_lastname`
* `hs_email_to_email`
* `hs_email_to_firstname`
* `hs_email_to_lastname`


## Error Handling

The API will return appropriate HTTP status codes (e.g., 400 for bad requests, 404 for not found, etc.) along with JSON error messages.


This documentation provides a comprehensive overview of the HubSpot Email Engagement API.  Refer to the official HubSpot developer documentation for the most up-to-date information and details on error handling and rate limits.
