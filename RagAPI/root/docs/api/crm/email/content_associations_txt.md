# HubSpot Email Engagement API Documentation

This document details the HubSpot API endpoints for managing email engagements.  You can log email activities directly within HubSpot or via the Email API.

## Creating an Email Engagement

To create an email engagement, send a `POST` request to `/crm/v3/objects/emails`.

**Request Body:**

The request body requires a `properties` object containing email details and optionally an `associations` object to link the email to existing records (e.g., contacts, companies).

### Properties Object:

| Field                 | Description                                                                                                                                        | Required | Data Type    |
|----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|----------|---------------|
| `hs_timestamp`        | Required. Email creation timestamp (Unix timestamp in milliseconds or UTC format). Determines timeline position.                                   | Yes      | String/Number |
| `hubspot_owner_id`    | ID of the email's owner (user listed as creator on the record timeline).                                                                            | No       | String        |
| `hs_email_direction` | Email direction (`EMAIL`, `INCOMING_EMAIL`, `FORWARDED_EMAIL`).                                                                                     | No       | String        |
| `hs_email_html`       | Body of the email (if sent from a CRM record).                                                                                                      | No       | String        |
| `hs_email_status`     | Send status (`BOUNCED`, `FAILED`, `SCHEDULED`, `SENDING`, `SENT`).                                                                               | No       | String        |
| `hs_email_subject`    | Email subject line.                                                                                                                               | No       | String        |
| `hs_email_text`       | Email body.                                                                                                                                       | No       | String        |
| `hs_attachment_ids`   | IDs of email attachments (semicolon-separated).                                                                                                  | No       | String        |
| `hs_email_headers`    | Email headers (JSON escaped string; automatically populates read-only properties; see "Set Email Headers" below).                               | No       | String        |


### Read-Only Properties:

These properties are automatically populated by HubSpot from the `hs_email_headers` value.

| Field                 | Description                                           |
|----------------------|-------------------------------------------------------|
| `hs_email_from_email` | Sender's email address.                               |
| `hs_email_from_firstname` | Sender's first name.                                  |
| `hs_email_from_lastname`  | Sender's last name.                                   |
| `hs_email_to_email`    | Recipient email addresses.                             |
| `hs_email_to_firstname` | Recipients' first names.                              |
| `hs_email_to_lastname`  | Recipients' last names.                               |


**Note:**  The `From` and `Sender` headers may differ (e.g., email alias vs. actual address).

### Set Email Headers:

`hs_email_headers` should be a JSON escaped string with the following structure:

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

### Associations Object:

To associate the email with records, include an `associations` array in the request body.

| Field          | Description                                                                          |
|-----------------|--------------------------------------------------------------------------------------|
| `to.id`         | ID of the record to associate with.                                                  |
| `types`         | Association type (array of objects).                                                  |
| `types[].associationCategory` | Association category (`HUBSPOT_DEFINED`).                                          |
| `types[].associationTypeId`  | Association type ID (retrieve via the Associations API or use default IDs). |


## Retrieving Emails

Retrieve individual emails via a `GET` request to `/crm/v3/objects/emails/{emailId}`.  Retrieve all emails with a `GET` request to `/crm/v3/objects/emails`.  Use parameters `properties` (comma-separated list) and `associations` (comma-separated list of object types) to control the returned data.  `limit` parameter is available for listing emails.

## Updating Emails

Update individual emails via a `PATCH` request to `/crm/v3/objects/emails/{emailId}`.  The request body should contain the properties to update.  Read-only properties are ignored.  An empty string clears a property value.

## Associating Existing Emails with Records

Associate an email with a record using a `PUT` request to `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`.

| Field          | Description                                                                 |
|-----------------|-----------------------------------------------------------------------------|
| `emailId`       | ID of the email.                                                            |
| `toObjectType`  | Object type (e.g., `contact`, `company`).                                     |
| `toObjectId`    | ID of the record.                                                           |
| `associationTypeId` | Association type ID (retrieve via Associations API or use default IDs). |


## Removing an Association

Remove an association using a `DELETE` request to the same URL as above.

## Pinning an Email

Pin an email to a record's timeline using the `hs_pinned_engagement_id` field when creating or updating the record via the object APIs (Companies, Contacts, Deals, Tickets, Custom Objects).

## Deleting Emails

Delete emails permanently via a `DELETE` request to `/crm/v3/objects/emails/{emailId}`.  Deleted emails cannot be restored.


This documentation provides a summary. Refer to the HubSpot API documentation for complete details and endpoint specifications.
