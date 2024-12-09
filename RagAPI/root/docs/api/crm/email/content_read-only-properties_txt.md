# HubSpot Email Engagement API Documentation

This document details the HubSpot Email Engagement API, allowing you to log and manage emails associated with CRM records.  You can interact with emails either directly within HubSpot or via this API.

## Core Functionality

The API provides methods for creating, retrieving, updating, associating, and deleting emails.  Batch operations are available for most actions (see the "Endpoints" tab within the HubSpot documentation for details).

## Email Creation (`POST /crm/v3/objects/emails`)

To create an email engagement, send a `POST` request to `/crm/v3/objects/emails`.  The request body must include a `properties` object and can optionally include an `associations` object.

### Properties Object

The `properties` object contains details about the email.  Required fields are marked with an asterisk (*).

| Field                 | Description                                                                                                                               |
|-----------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| `hs_timestamp`*       | Required. Email creation timestamp (Unix timestamp in milliseconds or UTC format).  Determines timeline placement on the record.             |
| `hubspot_owner_id`    | ID of the email owner (determines creator listed on the record timeline).                                                              |
| `hs_email_direction`  | Email direction (`EMAIL`, `INCOMING_EMAIL`, `FORWARDED_EMAIL`).                                                                         |
| `hs_email_html`       | Email body (HTML) if sent from a CRM record.                                                                                          |
| `hs_email_status`     | Email send status (`BOUNCED`, `FAILED`, `SCHEDULED`, `SENDING`, `SENT`).                                                             |
| `hs_email_subject`    | Email subject line.                                                                                                                      |
| `hs_email_text`       | Email body (plain text).                                                                                                                  |
| `hs_attachment_ids`   | IDs of attached files (semicolon-separated).                                                                                            |
| `hs_email_headers`    | Email headers (JSON escaped string, see "Set Email Headers" section).  Automatically populates read-only email properties.                 |


### Read-Only Properties

These properties are automatically populated by HubSpot based on the `hs_email_headers` value.

| Field                   | Description                                         |
|-------------------------|-----------------------------------------------------|
| `hs_email_from_email`   | Sender's email address.                             |
| `hs_email_from_firstname` | Sender's first name.                               |
| `hs_email_from_lastname`  | Sender's last name.                                |
| `hs_email_to_email`     | Recipient's email address(es).                       |
| `hs_email_to_firstname`  | Recipient's first name(s).                          |
| `hs_email_to_lastname`   | Recipient's last name(s).                           |


**Note:** When retrieving email headers, note the difference between `From` and `Sender` fields.  `Sender` identifies the actual submission source, which may differ from `From` (e.g., email aliases).

### Set Email Headers

Manually set `hs_email_headers` using a JSON escaped string with the following structure:

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

To associate the email with existing records (e.g., contacts, deals), include an `associations` object:

```json
{
  "associations": [
    {
      "to": { "id": 601 },
      "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 210 } ]
    },
    {
      "to": { "id": 602 },
      "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 198 } ]
    }
  ]
}
```

* `to.id`: ID of the record to associate.
* `types`: Association type (see HubSpot documentation for default and custom types).


## Email Retrieval (`GET /crm/v3/objects/emails/{emailId}` or `GET /crm/v3/objects/emails`)

Retrieve individual emails by ID or get a list of emails.  Use query parameters for filtering and pagination.

## Email Updates (`PATCH /crm/v3/objects/emails/{emailId}`)

Update individual email properties using a `PATCH` request.  HubSpot ignores read-only and non-existent properties.  Use an empty string to clear a property value.

## Email Associations Management

* **Associate:** `PUT /crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`
* **Remove:** `DELETE /crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

## Pinning Emails

Pin an email to a record's timeline using the `hs_pinned_engagement_id` field when creating or updating the record via object APIs.  Only one activity can be pinned per record.

## Email Deletion (`DELETE /crm/v3/objects/emails/{emailId}`)

Permanently delete emails (cannot be restored).


This documentation provides a summary. Refer to the HubSpot developer documentation for comprehensive details and examples.
