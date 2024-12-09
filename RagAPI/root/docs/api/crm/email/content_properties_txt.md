# HubSpot Email Engagement API Documentation

This document details the HubSpot Email Engagement API, allowing you to log and manage emails associated with CRM records.  You can interact with emails either directly within HubSpot or via this API.

## Managing Emails via the API

This section covers the fundamental methods for managing emails using the HubSpot API.  For a complete list of endpoints and their specifications, refer to the "Endpoints" tab (not included in provided text).

### Create an Email

**Endpoint:** `/crm/v3/objects/emails`
**Method:** `POST`

To create an email engagement, send a `POST` request to the endpoint above.  The request body should include a `properties` object containing email details and an optional `associations` object to link the email with existing records (e.g., contacts, companies).

#### Properties Object

| Field             | Description                                                                                                         | Required |
|----------------------|---------------------------------------------------------------------------------------------------------------------|----------|
| `hs_timestamp`      | Required. Email creation timestamp (Unix timestamp in milliseconds or UTC format).                                     | Yes      |
| `hubspot_owner_id`  | ID of the email's owner (determines the creator shown on the record timeline).                                      | No       |
| `hs_email_direction` | Email direction (`EMAIL`, `INCOMING_EMAIL`, `FORWARDED_EMAIL`).                                                  | No       |
| `hs_email_html`     | Email body (HTML) if sent from a CRM record.                                                                       | No       |
| `hs_email_status`   | Email send status (`BOUNCED`, `FAILED`, `SCHEDULED`, `SENDING`, `SENT`).                                           | No       |
| `hs_email_subject`  | Email subject line.                                                                                             | No       |
| `hs_email_text`     | Email body (plain text).                                                                                         | No       |
| `hs_attachment_ids` | IDs of attached files (semicolon-separated).                                                                       | No       |
| `hs_email_headers`  | Email headers (JSON escaped string; see "Set Email Headers").  Automatically populates read-only email properties. | No       |


#### Read-Only Properties

These properties are automatically populated by HubSpot from the `hs_email_headers` value:

| Field                  | Description                                     |
|--------------------------|-------------------------------------------------|
| `hs_email_from_email`    | Sender's email address.                         |
| `hs_email_from_firstname` | Sender's first name.                            |
| `hs_email_from_lastname`  | Sender's last name.                             |
| `hs_email_to_email`      | Recipient(s)' email address(es).                 |
| `hs_email_to_firstname`  | Recipient(s)' first name(s).                    |
| `hs_email_to_lastname`   | Recipient(s)' last name(s).                     |


**Note:**  The `From` and `Sender` headers may differ; `Sender` identifies the actual email submitter.


#### Set Email Headers

To manually set email headers, use a JSON escaped string with the following structure:

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

#### Associations Object

To associate the email with existing records, include an `associations` array:

| Field             | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `to`               | Record ID to associate with.                                             |
| `types`            | Association type (`associationCategory`, `associationTypeId`). See details below  |


**Association Types:**

The `types` array should include an object with `associationCategory` ("HUBSPOT_DEFINED") and `associationTypeId` (see [default IDs](link_to_default_ids_or_api_docs) or use the associations API for custom types).


### Retrieve Emails

**Endpoint (single email):** `/crm/v3/objects/emails/{emailId}`
**Method:** `GET`

**Parameters:**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.

**Endpoint (all emails):** `/crm/v3/objects/emails`
**Method:** `GET`

**Parameters:**

* `limit`: Maximum number of results per page.
* `properties`: Comma-separated list of properties to return.


### Update Emails

**Endpoint:** `/crm/v3/objects/emails/{emailId}`
**Method:** `PATCH`

Update email properties by sending a `PATCH` request.  HubSpot ignores read-only and non-existent properties.  To clear a property, send an empty string.


### Associate Existing Emails with Records

**Endpoint:** `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`
**Method:** `PUT`

Associate an email with a record.  The URL contains:

* `emailId`: The email's ID.
* `toObjectType`: The record type (e.g., "contact").
* `toObjectId`: The record's ID.
* `associationTypeId`: The association type ID (obtainable via the associations API).


### Remove an Association

**Endpoint:** `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`
**Method:** `DELETE`

Remove an association using the same URL as above.


### Pin an Email on a Record

Pin an email to the top of a record's timeline using the `hs_pinned_engagement_id` field when creating or updating the record via object APIs (companies, contacts, deals, tickets, custom objects).  The email must already be associated with the record. Only one activity can be pinned per record.


### Delete Emails

**Endpoint:** `/crm/v3/objects/emails/{emailId}`
**Method:** `DELETE`

Permanently deletes an email.  Deletion is irreversible.


This documentation provides a summary.  Consult the full API documentation and the "Endpoints" tab for comprehensive details and code examples.
