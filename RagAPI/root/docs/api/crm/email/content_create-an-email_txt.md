# HubSpot Email Engagement API Documentation

This document details the HubSpot Email Engagement API, allowing you to log and manage emails associated with CRM records.  You can interact with emails either directly within HubSpot or via this API.  For a complete list of endpoints and their requirements, refer to the "Endpoints" tab (not included in provided text).

## Core Functionality

The API provides methods for creating, retrieving, updating, associating, and deleting emails.  Batch operations are supported for many actions.

## Creating an Email

Use a `POST` request to `/crm/v3/objects/emails` to create a new email engagement.

**Request Body:**

The request body must include a `properties` object, and optionally an `associations` object.

### Properties Object

| Field                  | Description                                                                                                                                                 | Required | Data Type    |
|-------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|---------------|
| `hs_timestamp`          | Required. Email creation timestamp. Use Unix timestamp (milliseconds) or UTC format (e.g., "2024-10-27T10:00:00Z").                                          | Yes      | String/Number |
| `hubspot_owner_id`      | ID of the email's owner (user). Determines the creator shown on the record timeline.                                                                           | No       | String        |
| `hs_email_direction`   | Email direction (`EMAIL`, `INCOMING_EMAIL`, `FORWARDED_EMAIL`).                                                                                            | No       | String        |
| `hs_email_html`         | Email body (HTML) if sent from a CRM record.                                                                                                                  | No       | String        |
| `hs_email_status`       | Email send status (`BOUNCED`, `FAILED`, `SCHEDULED`, `SENDING`, `SENT`).                                                                                      | No       | String        |
| `hs_email_subject`      | Email subject line.                                                                                                                                        | No       | String        |
| `hs_email_text`         | Email body (plain text).                                                                                                                                   | No       | String        |
| `hs_attachment_ids`     | IDs of attached files (semicolon-separated).                                                                                                                 | No       | String        |
| `hs_email_headers`      | JSON-escaped string containing email headers (see "Set Email Headers" section). This field populates read-only properties.                               | No       | String        |


### Read-Only Properties

These properties are automatically populated from `hs_email_headers`.

| Field                   | Description                                     |
|-------------------------|-------------------------------------------------|
| `hs_email_from_email`   | Sender's email address.                         |
| `hs_email_from_firstname`| Sender's first name.                            |
| `hs_email_from_lastname` | Sender's last name.                             |
| `hs_email_to_email`     | Recipient email addresses (comma-separated).     |
| `hs_email_to_firstname` | Recipients' first names (comma-separated).       |
| `hs_email_to_lastname`  | Recipients' last names (comma-separated).        |

**Note:**  `From` and `Sender` headers may differ; `Sender` indicates the actual submission source.


### Set Email Headers

`hs_email_headers` should be a JSON-escaped string with the following structure:

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

### Associations Object

To associate the email with existing records (e.g., contacts, deals), include an `associations` array.

| Field          | Description                                                                     |
|-----------------|---------------------------------------------------------------------------------|
| `to`            | Object with `id` property specifying the associated record ID.                  |
| `types`         | Array of association types, each with `associationCategory` and `associationTypeId`. |


## Retrieving Emails

Use a `GET` request to:

* `/crm/v3/objects/emails/{emailId}` (individual email)
* `/crm/v3/objects/emails` (list of emails)

Parameters include `properties`, `associations`, and `limit`.


## Updating Emails

Use a `PATCH` request to `/crm/v3/objects/emails/{emailId}`.  The request body contains the properties to update. Read-only properties are ignored.  An empty string clears a property value.


## Associating Existing Emails with Records

Use a `PUT` request to `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`.


## Removing an Association

Use a `DELETE` request to the same URL as associating existing emails.


## Pinning an Email

To pin an email to a record's timeline, include the email's `id` in the `hs_pinned_engagement_id` field when creating or updating the record via object APIs (companies, contacts, deals, tickets, custom objects).


## Deleting Emails

Use a `DELETE` request to `/crm/v3/objects/emails/{emailId}`. Deletion is permanent.


This documentation provides a summary.  Always consult the HubSpot API documentation and the "Endpoints" tab for the most up-to-date and complete information.
