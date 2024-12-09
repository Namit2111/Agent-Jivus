# HubSpot Email Engagement API Documentation

This document details the HubSpot Email Engagement API, allowing you to log and manage emails associated with CRM records.  You can interact with emails either directly within HubSpot or through this API.

## Managing Emails via the API

This section outlines the basic methods for managing emails using the HubSpot API.  For a complete list of endpoints and their requirements, refer to the "Endpoints" tab (not included in provided text, assumed to be present in the actual HubSpot documentation).

### Create an Email

Use a `POST` request to `/crm/v3/objects/emails` to create a new email engagement.

**Request Body:**

The request body should contain a `properties` object for email details and an optional `associations` object to link the email to existing records (e.g., contacts, companies).

#### Properties

The `properties` object accepts the following fields:

| Field                | Description                                                                                                                              | Required |
|----------------------|-------------------------------------------------------------------------------------------------------------------------------------------|----------|
| `hs_timestamp`       | Required. Email creation timestamp (Unix timestamp in milliseconds or UTC format).                                                        | Yes      |
| `hubspot_owner_id`   | ID of the email owner (determines the creator listed on the record timeline).                                                             | No       |
| `hs_email_direction` | Email direction (`EMAIL`, `INCOMING_EMAIL`, `FORWARDED_EMAIL`).                                                                        | No       |
| `hs_email_html`      | HTML body of the email (sent from a CRM record).                                                                                         | No       |
| `hs_email_status`    | Email send status (`BOUNCED`, `FAILED`, `SCHEDULED`, `SENDING`, `SENT`).                                                              | No       |
| `hs_email_subject`   | Email subject line.                                                                                                                      | No       |
| `hs_email_text`      | Plain text body of the email.                                                                                                           | No       |
| `hs_attachment_ids`  | IDs of email attachments (semicolon-separated).                                                                                          | No       |
| `hs_email_headers`   | Email headers (JSON escaped string; automatically populates read-only properties – see "Set Email Headers").                            | No       |


#### Read-Only Properties

These properties are automatically populated by HubSpot from the `hs_email_headers` value:

| Field                  | Description                                     |
|------------------------|-------------------------------------------------|
| `hs_email_from_email`   | Sender's email address.                         |
| `hs_email_from_firstname` | Sender's first name.                             |
| `hs_email_from_lastname`  | Sender's last name.                              |
| `hs_email_to_email`    | Recipient email addresses.                       |
| `hs_email_to_firstname` | Recipients' first names.                         |
| `hs_email_to_lastname`  | Recipients' last names.                          |

**Note:** Differences between `From` and `Sender` headers are explained in the original document.


#### Set Email Headers

To manually set email headers (which populate read-only properties), use a JSON escaped string with the following structure:

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

#### Example Create Email Request:

```json
{
  "properties": {
    "hs_timestamp": "2019-10-30T03:30:17.883Z",
    "hubspot_owner_id": "47550177",
    "hs_email_direction": "EMAIL",
    "hs_email_status": "SENT",
    "hs_email_subject": "Let's talk",
    "hs_email_text": "Thanks for youremail",
    "hs_email_headers": "{\"from\":{\"email\":\"from@domain.com\",\"firstName\":\"FromFirst\",\"lastName\":\"FromLast\"},\"sender\":{\"email\":\"sender@domain.com\",\"firstName\":\"SenderFirst\",\"lastName\":\"SenderLast\"},\"to\":[{\"email\":\"ToFirst+ToLast<to@test.com>\",\"firstName\":\"ToFirst\",\"lastName\":\"ToLast\"}],\"cc\":[],\"bcc\":[]}"
  }
}
```

#### Associations

To associate an email with existing records, include an `associations` object in your request:

```json
{
  "to": {
    "id": 601
  },
  "types": [
    {
      "associationCategory": "HUBSPOT_DEFINED",
      "associationTypeId": 210
    }
  ]
}
```

* **`to`**: Record ID to associate with.
* **`types`**: Association type (`associationCategory` and `associationTypeId`).  Default and custom association type IDs are available through the Associations API.


### Retrieve Emails

Retrieve individual emails via `GET` `/crm/v3/objects/emails/{emailId}` or all emails via `GET` `/crm/v3/objects/emails`.  Use parameters like `properties`, `associations`, and `limit` to customize the response.


### Update Emails

Use a `PATCH` request to `/crm/v3/objects/emails/{emailId}` to update an email.  HubSpot ignores read-only and non-existent properties.  To clear a property, use an empty string.


### Associate Existing Emails with Records

Use a `PUT` request to `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}` to associate an email with a record.  The URL specifies the email ID, object type, object ID, and association type ID.


### Remove an Association

Use a `DELETE` request to the same URL as above to remove an association.


### Pin an Email on a Record

Pin an email to a record's timeline using the `hs_pinned_engagement_id` field when creating or updating the record via the object APIs (companies, contacts, deals, tickets, custom objects).


### Delete Emails

Use a `DELETE` request to `/crm/v3/objects/emails/{emailId}` to permanently delete an email.  Deleted emails cannot be restored.


This markdown provides a structured overview of the provided text.  Remember to consult the full HubSpot documentation for complete details and the "Endpoints" tab for all available API endpoints.
