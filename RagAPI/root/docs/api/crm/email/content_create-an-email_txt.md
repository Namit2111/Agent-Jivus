# HubSpot Email Engagement API Documentation

This document details the HubSpot Email Engagement API, allowing you to log and manage emails associated with CRM records.  You can interact with the API using HTTP requests.

## API Endpoints Base URL: `/crm/v3/objects/emails`

All endpoints below use this base URL unless otherwise specified.  Replace `{emailId}` with the actual email ID.

## 1. Create an Email (POST)

Creates a new email engagement.

**Endpoint:** `/crm/v3/objects/emails`

**Method:** `POST`

**Request Body:** JSON

**Properties Object (Required):**

| Field                | Description                                                                                                       | Type             | Required | Example                                   |
|-----------------------|-------------------------------------------------------------------------------------------------------------------|-----------------|----------|-------------------------------------------|
| `hs_timestamp`        | Email creation time (Unix timestamp in milliseconds or UTC format).                                                 | String/Number   | Yes      | `1678886400000` (milliseconds) or `2024-03-15T12:00:00Z` (UTC) |
| `hubspot_owner_id`    | ID of the email owner (HubSpot user).                                                                              | String           | No       | `47550177`                               |
| `hs_email_direction` | Email direction (`EMAIL`, `INCOMING_EMAIL`, `FORWARDED_EMAIL`).                                                  | String           | No       | `EMAIL`                                  |
| `hs_email_html`       | Email body (HTML) (sent from a CRM record).                                                                      | String           | No       | `<html>...</html>`                       |
| `hs_email_status`     | Email send status (`BOUNCED`, `FAILED`, `SCHEDULED`, `SENDING`, `SENT`).                                           | String           | No       | `SENT`                                   |
| `hs_email_subject`    | Email subject.                                                                                                   | String           | No       | "Let's talk"                              |
| `hs_email_text`       | Email body (plain text).                                                                                         | String           | No       | "Thanks for your email"                   |
| `hs_attachment_ids`   | IDs of email attachments (semicolon-separated).                                                                  | String           | No       | `123;456`                                |
| `hs_email_headers`    | JSON escaped string containing email headers (see "Set Email Headers" section).                               | String           | No       | `{\"from\":{\"email\":\"from@domain.com\",...}}` |


**Associations Object (Optional):**  Associates the email with CRM records.

| Field      | Description                                                     | Type      | Example |
|------------|-----------------------------------------------------------------|-----------|---------|
| `to`       | Record ID to associate with.                                    | Object    | `{"id": 601}` |
| `types`    | Association type.                                               | Array     | `[{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 210}]` |
    * `associationCategory`: "HUBSPOT_DEFINED"
    * `associationTypeId`:  (See default IDs [here](link_to_default_ids) or use the Associations API)


**Example Request:**

```json
{
  "properties": {
    "hs_timestamp": "2024-03-15T12:00:00Z",
    "hubspot_owner_id": "47550177",
    "hs_email_direction": "EMAIL",
    "hs_email_status": "SENT",
    "hs_email_subject": "Let's talk",
    "hs_email_text": "Thanks for your email",
    "hs_email_headers": "{\"from\":{\"email\":\"from@domain.com\",\"firstName\":\"FromFirst\",\"lastName\":\"FromLast\"},\"to\":[{\"email\":\"to@test.com\"}]}"
  },
  "associations": [
    {
      "to": {"id": 601},
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 210}]
    }
  ]
}
```

**Response:**  JSON containing the created email's details including its ID.


## 2. Set Email Headers

Email headers are used to populate read-only email properties.  Use a JSON escaped string with the following structure:

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


## 3. Retrieve Emails (GET)

**a) Retrieve a single email:**

**Endpoint:** `/crm/v3/objects/emails/{emailId}`

**Method:** `GET`

**Parameters:**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.

**b) Retrieve a list of emails:**

**Endpoint:** `/crm/v3/objects/emails`

**Method:** `GET`

**Parameters:**

* `limit`: Maximum number of results per page.
* `properties`: Comma-separated list of properties to return.


## 4. Update an Email (PATCH)

**Endpoint:** `/crm/v3/objects/emails/{emailId}`

**Method:** `PATCH`

**Request Body:** JSON containing the properties to update.  Read-only properties are ignored.  An empty string clears a property value.


## 5. Associate Existing Email with Records (PUT)

Associates an existing email with a record.

**Endpoint:** `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `PUT`

**Parameters:**

* `emailId`: Email ID.
* `toObjectType`: Object type (e.g., `contact`, `company`).
* `toObjectId`: Record ID.
* `associationTypeId`: Association type ID.


## 6. Remove an Association (DELETE)

Removes an association between an email and a record.

**Endpoint:** `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Method:** `DELETE`


## 7. Pin an Email (Update Record via Object APIs)

Pinning an email to a record places it at the top of the record's timeline.  This requires updating the record using the respective object API (contacts, companies, etc.) and including the email's ID in the `hs_pinned_engagement_id` field.


## 8. Delete an Email (DELETE)

Permanently deletes an email.  Cannot be restored.

**Endpoint:** `/crm/v3/objects/emails/{emailId}`

**Method:** `DELETE`

This documentation provides a comprehensive overview.  Refer to the HubSpot developer documentation for complete details on error handling, rate limits, and authentication. Remember to replace placeholder values like `{emailId}` with actual values.
