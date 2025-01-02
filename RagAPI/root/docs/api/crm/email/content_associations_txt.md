# HubSpot Email Engagement API Documentation

This document details the HubSpot Email Engagement API, allowing you to log and manage emails associated with CRM records.  You can interact with the API using standard HTTP requests.

## API Endpoints Base URL:

`/crm/v3/objects/emails`

## 1. Create an Email

**Method:** `POST /crm/v3/objects/emails`

**Request Body:**  JSON object with `properties` and optional `associations` objects.

**Properties Object:**

| Field             | Description                                                                                     | Type             | Required | Example                               |
|----------------------|-------------------------------------------------------------------------------------------------|--------------------|----------|---------------------------------------|
| `hs_timestamp`      | Email creation time (Unix timestamp in milliseconds or UTC format).                            | String/Number    | Yes      | `1678886400000` or `"2023-03-15T12:00:00Z"` |
| `hubspot_owner_id`   | ID of the email owner (HubSpot user).                                                           | String            | No       | `47550177`                             |
| `hs_email_direction` | Email direction (`EMAIL`, `INCOMING_EMAIL`, `FORWARDED_EMAIL`).                               | String            | No       | `"EMAIL"`                              |
| `hs_email_html`     | Email body (HTML) - sent from a CRM record.                                                    | String            | No       | `<html>...</html>`                    |
| `hs_email_status`   | Email send status (`BOUNCED`, `FAILED`, `SCHEDULED`, `SENDING`, `SENT`).                      | String            | No       | `"SENT"`                               |
| `hs_email_subject`  | Email subject.                                                                                  | String            | No       | `"Let's talk"`                         |
| `hs_email_text`     | Email body (plain text).                                                                       | String            | No       | `Thanks for your email`                |
| `hs_attachment_ids` | IDs of attached files (semicolon-separated).                                                  | String            | No       | `"123;456"`                             |
| `hs_email_headers`  | JSON-escaped string containing email headers (see "Set Email Headers" section).               | String            | No       | `{\"from\":{\"email\":\"...\"}, ...}` |


**Associations Object:** (Optional, for associating with existing records)

| Field             | Description                                                           | Type      | Required | Example                                    |
|----------------------|-----------------------------------------------------------------------|-----------|----------|---------------------------------------------|
| `to`                | ID of the record to associate with (e.g., contact, deal).            | Object    | Yes      | `{"id": 601}`                             |
| `types`             | Association type (see "Association Types" below).                  | Array     | Yes      | `[{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 210}]` |


**Example Request (with associations):**

```json
{
  "properties": {
    "hs_timestamp": "2024-03-15T12:00:00Z",
    "hubspot_owner_id": "12345",
    "hs_email_direction": "EMAIL",
    "hs_email_subject": "Test Email",
    "hs_email_text": "This is a test email."
  },
  "associations": [
    {
      "to": {"id": 601},
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 210}]
    }
  ]
}
```

**Response:**  JSON object representing the created email, including its ID.


## 2. Set Email Headers

The `hs_email_headers` property accepts a JSON-escaped string.  This string should contain the following structure:

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

This populates read-only properties like `hs_email_from_email`, `hs_email_to_email`, etc.


## 3. Read-Only Properties

Several properties are automatically populated by HubSpot from the `hs_email_headers`:

| Field                 | Description                               |
|-------------------------|-------------------------------------------|
| `hs_email_from_email`   | Sender's email address.                  |
| `hs_email_from_firstname`| Sender's first name.                      |
| `hs_email_from_lastname` | Sender's last name.                       |
| `hs_email_to_email`     | Recipient's email address(es).            |
| `hs_email_to_firstname` | Recipient's first name(s).               |
| `hs_email_to_lastname`  | Recipient's last name(s).                |


## 4. Retrieve Emails

**Method:** `GET /crm/v3/objects/emails` (for all emails) or `GET /crm/v3/objects/emails/{emailId}` (for a single email)

**Parameters:**

* `limit`: Maximum number of results per page (for GET all emails).
* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.

**Response:** JSON object(s) representing the requested email(s).


## 5. Update Emails

**Method:** `PATCH /crm/v3/objects/emails/{emailId}`

**Request Body:** JSON object containing the properties to update.  HubSpot ignores read-only and non-existent properties.  Use an empty string to clear a property value.

**Example Request:**

```json
{
  "properties": {
    "hs_email_subject": "Updated Subject"
  }
}
```

**Response:** JSON object representing the updated email.


## 6. Associate Existing Emails with Records

**Method:** `PUT /crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

* `{emailId}`: Email ID.
* `{toObjectType}`: Object type (e.g., `contact`, `company`).
* `{toObjectId}`: Object ID.
* `{associationTypeId}`: Association type ID (obtainable via the Associations API).


## 7. Remove an Association

**Method:** `DELETE /crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

Uses the same URL structure as associating emails.


## 8. Pin an Email on a Record

To pin an email, include its ID in the `hs_pinned_engagement_id` field when creating or updating a record via other HubSpot object APIs (Contacts, Companies, Deals, etc.).


## 9. Delete Emails

**Method:** `DELETE /crm/v3/objects/emails/{emailId}`

Permanently deletes the specified email.



## Association Types

Default association type IDs can be found in the HubSpot documentation.  Custom association types can be retrieved using the HubSpot Associations API.


This markdown provides a comprehensive overview of the HubSpot Email Engagement API.  Remember to consult the official HubSpot API documentation for the most up-to-date information and detailed specifications.
