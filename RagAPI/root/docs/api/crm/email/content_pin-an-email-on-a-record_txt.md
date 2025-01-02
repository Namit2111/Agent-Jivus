# HubSpot Email Engagement API Documentation

This document details the HubSpot Email Engagement API, allowing you to log and manage emails associated with CRM records.  You can interact with emails either directly through the HubSpot interface or via this API.

## API Endpoints

All endpoints are located under the `/crm/v3/objects/emails` base path.  Refer to the HubSpot API documentation for authentication details and rate limits.

### 1. Create an Email (POST `/crm/v3/objects/emails`)

Creates a new email engagement record.

**Request Body:**

The request body should be a JSON object with `properties` and optionally `associations` objects.

* **`properties` (object):** Contains email details.  Required fields are marked with an asterisk (*).

    | Field                  | Description                                                                                                 | Type             | Required | Example                                      |
    |-----------------------|-------------------------------------------------------------------------------------------------------------|-----------------|----------|----------------------------------------------|
    | `hs_timestamp`*       | Email creation timestamp (Unix timestamp in milliseconds or UTC format).                                      | string           | *        | `"2024-10-27T10:00:00Z"` or `1703657600000` |
    | `hubspot_owner_id`     | ID of the email's owner (HubSpot user).                                                                     | string           |          | `"12345"`                                   |
    | `hs_email_direction`  | Email direction (`EMAIL`, `INCOMING_EMAIL`, `FORWARDED_EMAIL`).                                             | string           |          | `"EMAIL"`                                    |
    | `hs_email_html`       | Email body (HTML, for emails sent from a CRM record).                                                       | string           |          | `"<html>...</html>"`                       |
    | `hs_email_status`     | Email send status (`BOUNCED`, `FAILED`, `SCHEDULED`, `SENDING`, `SENT`).                                    | string           |          | `"SENT"`                                     |
    | `hs_email_subject`    | Email subject.                                                                                            | string           |          | `"Meeting Request"`                           |
    | `hs_email_text`       | Email body (plain text).                                                                                   | string           |          | `"Hi there..."`                             |
    | `hs_attachment_ids`   | IDs of attached files, separated by semicolons.                                                             | string           |          | `"123;456"`                                  |
    | `hs_email_headers`    | JSON-escaped string containing email headers (see "Set Email Headers" section).                             | string           |          | `{\"from\":{\"email\":\"...\"},\"to\":[...]}` |


* **`associations` (array of objects, optional):** Associates the email with other CRM records (e.g., contacts, deals).

    | Field          | Description                                           | Type             | Example |
    |-----------------|-------------------------------------------------------|-----------------|---------|
    | `to` (object)   | Record to associate with ( `{id: recordId}` ).           | object           | `{id: 601}` |
    | `types` (array) | Association type ( `{associationCategory: "HUBSPOT_DEFINED", associationTypeId: 210}` ). | array of objects | `[...]`  |


**Example Request (JSON):**

```json
{
  "properties": {
    "hs_timestamp": "2024-10-27T10:00:00Z",
    "hubspot_owner_id": "12345",
    "hs_email_direction": "EMAIL",
    "hs_email_subject": "Test Email",
    "hs_email_text": "This is a test email.",
    "hs_email_status": "SENT"
  }
}
```

**Response (JSON):**

A successful response will include the newly created email's ID and other properties.

```json
{
  "id": "67890",
  "properties": { ... }
}
```


### 2. Set Email Headers

The `hs_email_headers` property accepts a JSON-escaped string with the following structure:

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


### 3. Retrieve Emails (GET `/crm/v3/objects/emails` or GET `/crm/v3/objects/emails/{emailId}`)

* **Retrieve Single Email:** Replace `{emailId}` with the email's ID.  Use `properties` and `associations` query parameters to specify the returned fields.

* **Retrieve Multiple Emails:** Use `limit` and `properties` query parameters to control the number of results and returned fields.


### 4. Update Emails (PATCH `/crm/v3/objects/emails/{emailId}`)

Updates an existing email.  Provide the properties to update in the request body. Read-only properties are ignored.  An empty string will clear a property value.


### 5. Associate Existing Emails with Records (PUT `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates an email with another CRM object.

### 6. Remove an Association (DELETE `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Removes an association between an email and another CRM object.


### 7. Pin an Email (Update Record via Object APIs)

Pinning an email is done indirectly by including its ID in the `hs_pinned_engagement_id` field when updating the associated record (contact, company, deal, etc.) using the respective object API.


### 8. Delete Emails (DELETE `/crm/v3/objects/emails/{emailId}`)

Permanently deletes an email.


## Read-Only Properties

Several email properties are automatically populated by HubSpot based on the email headers. These are read-only and cannot be directly modified.  Examples include `hs_email_from_email`, `hs_email_to_email`, `hs_email_from_firstname`, etc.


## Error Handling

The API will return standard HTTP status codes to indicate success or failure.  Error responses will include details about the issue.


This documentation provides a concise overview.  Always refer to the official HubSpot API documentation for the most up-to-date information and complete details on all endpoints, parameters, and error handling.
