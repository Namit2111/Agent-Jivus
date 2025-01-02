# HubSpot Email Engagement API Documentation

This document details the HubSpot Email Engagement API, allowing you to log and manage emails associated with CRM records.  You can interact with emails either directly through the HubSpot UI or using this API.

## API Endpoints

All endpoints are under the `/crm/v3/objects/emails` base path.  Remember to replace `{emailId}` and other bracketed placeholders with the appropriate values.


## API Calls

### 1. Create an Email (POST `/crm/v3/objects/emails`)

Creates a new email engagement.

**Request Body:**

The request body must contain a `properties` object and optionally an `associations` object.

* **`properties` object:** Contains email details.  Required fields are marked with an asterisk (*).

    | Field                | Description                                                                                             | Type             | Example                                      |
    |----------------------|---------------------------------------------------------------------------------------------------------|-----------------|----------------------------------------------|
    | `hs_timestamp`*     | Email creation timestamp (Unix timestamp in milliseconds or UTC format).                               | String           | `2024-10-27T10:00:00Z` or `1703676400000` |
    | `hubspot_owner_id`   | ID of the email owner.                                                                                 | String           | `1234567`                                    |
    | `hs_email_direction` | Email direction (`EMAIL`, `INCOMING_EMAIL`, `FORWARDED_EMAIL`).                                        | String           | `EMAIL`                                       |
    | `hs_email_html`     | Email body (HTML) (sent from a CRM record).                                                              | String           | `<html>...</html>`                          |
    | `hs_email_status`   | Email send status (`BOUNCED`, `FAILED`, `SCHEDULED`, `SENDING`, `SENT`).                               | String           | `SENT`                                        |
    | `hs_email_subject`  | Email subject.                                                                                         | String           | "Meeting Request"                             |
    | `hs_email_text`     | Email body (plain text).                                                                               | String           | "Hi there..."                                  |
    | `hs_attachment_ids` | IDs of attached files (semicolon-separated).                                                            | String           | `1;2;3`                                       |
    | `hs_email_headers`  | JSON escaped string containing email headers (see "Set Email Headers").                               | String           | `{\"from\":{\"email\":\"...\"}, ...}`         |


* **`associations` object (optional):**  Associates the email with other records (e.g., contacts, deals).

    | Field             | Description                                                    | Type     | Example                               |
    |----------------------|----------------------------------------------------------------|----------|---------------------------------------|
    | `to`               | ID of the record to associate with.                         | Object   | `{"id": 601}`                         |
    | `types`            | Association type.                                            | Array    | `[{"associationCategory":"HUBSPOT_DEFINED","associationTypeId":210}]` |


**Example Request (using `curl`):**

```bash
curl -X POST \
  https://api.hubspot.com/crm/v3/objects/emails \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -d '{
    "properties": {
      "hs_timestamp": "2024-10-27T10:00:00Z",
      "hubspot_owner_id": "1234567",
      "hs_email_direction": "EMAIL",
      "hs_email_subject": "Test Email",
      "hs_email_text": "This is a test email."
    }
  }'
```


**Response:**  A JSON object containing the created email's details, including its ID.


### 2. Set Email Headers

Email headers automatically populate read-only properties.  To set them manually, use a JSON escaped string in the `hs_email_headers` property:

**Example JSON:**

```json
{
  "from": {
    "email": "from@domain.com",
    "firstName": "FromFirst",
    "lastName": "FromLast"
  },
  "to": [
    {
      "email": "to@test.com",
      "firstName": "ToFirst",
      "lastName": "ToLast"
    }
  ],
  "cc": [],
  "bcc": []
}
```


### 3. Retrieve Emails (GET `/crm/v3/objects/emails` or GET `/crm/v3/objects/emails/{emailId}`)

* **GET `/crm/v3/objects/emails`:** Retrieves a list of emails.  Uses parameters `limit` and `properties`.
* **GET `/crm/v3/objects/emails/{emailId}`:** Retrieves a single email by ID. Uses parameters `properties` and `associations`.

**Example (GET single email):**

```bash
curl -X GET \
  https://api.hubspot.com/crm/v3/objects/emails/123 \
  -H 'Authorization: Bearer YOUR_API_KEY'
```


### 4. Update Emails (PATCH `/crm/v3/objects/emails/{emailId}`)

Updates an existing email.

**Request Body:**  Similar to create, but only includes properties to update.


### 5. Associate Existing Emails (PUT `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates an email with another record.


### 6. Remove Association (DELETE `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Removes an association between an email and a record.


### 7. Pin an Email

Pinning an email to keep it at the top of a record's timeline is done through the record's API (contacts, deals, etc.), using the `hs_pinned_engagement_id` field.


### 8. Delete Emails (DELETE `/crm/v3/objects/emails/{emailId}`)

Permanently deletes an email.


## Read-Only Properties

Several properties are automatically populated and cannot be modified:

* `hs_email_from_email`
* `hs_email_from_firstname`
* `hs_email_from_lastname`
* `hs_email_to_email`
* `hs_email_to_firstname`
* `hs_email_to_lastname`


## Error Handling

The API returns standard HTTP status codes to indicate success or failure.  Error responses will include a JSON object with details about the error.


## Authentication

Use your HubSpot API key in the `Authorization` header (e.g., `Authorization: Bearer YOUR_API_KEY`).


This documentation provides a comprehensive overview of the HubSpot Email Engagement API.  Refer to the HubSpot developer documentation for the most up-to-date information and details on batch operations.
