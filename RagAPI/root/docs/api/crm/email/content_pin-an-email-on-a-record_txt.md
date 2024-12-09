# HubSpot Email Engagement API Documentation

This document details the HubSpot Email Engagement API, allowing developers to log and manage emails associated with CRM records.  Email activities can be logged directly within HubSpot or via this API.

## Email Endpoint Reference

The primary endpoint for interacting with emails is `/crm/v3/objects/emails`.  All examples below assume you've obtained the necessary API key and are making requests to the appropriate HubSpot API base URL.  Refer to the "Endpoints" tab for complete endpoint details and requirements.


### Create an Email

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/emails`

**Request Body:**  The request body includes a `properties` object with email details and an optional `associations` object to link the email to existing records (e.g., contacts, companies).

**Properties Object:**

| Field             | Description                                                                                                        | Required | Data Type |
|----------------------|--------------------------------------------------------------------------------------------------------------------|----------|------------|
| `hs_timestamp`      | Timestamp of email creation (Unix timestamp in milliseconds or UTC format). Determines timeline placement.         | Yes      | String     |
| `hubspot_owner_id`   | ID of the email's owner (user shown as creator on the record timeline).                                          | No       | String     |
| `hs_email_direction` | Email direction (`EMAIL`, `INCOMING_EMAIL`, `FORWARDED_EMAIL`).                                                 | No       | String     |
| `hs_email_html`     | Email body (if sent from a CRM record).                                                                        | No       | String     |
| `hs_email_status`    | Email send status (`BOUNCED`, `FAILED`, `SCHEDULED`, `SENDING`, `SENT`).                                     | No       | String     |
| `hs_email_subject`   | Email subject line.                                                                                             | No       | String     |
| `hs_email_text`     | Email body (plain text).                                                                                         | No       | String     |
| `hs_attachment_ids` | IDs of attached files (semicolon-separated).                                                                     | No       | String     |
| `hs_email_headers`   | JSON escaped string containing email headers (influences read-only properties; see below).                        | No       | String     |


**Example Request Body:**

```json
{
  "properties": {
    "hs_timestamp": "2019-10-30T03:30:17.883Z",
    "hubspot_owner_id": "47550177",
    "hs_email_direction": "EMAIL",
    "hs_email_status": "SENT",
    "hs_email_subject": "Let's talk",
    "hs_email_text": "Thanks for your email",
    "hs_email_headers": "{\"from\":{\"email\":\"from@domain.com\",\"firstName\":\"FromFirst\",\"lastName\":\"FromLast\"},\"sender\":{\"email\":\"sender@domain.com\",\"firstName\":\"SenderFirst\",\"lastName\":\"SenderLast\"},\"to\":[{\"email\":\"ToFirst+ToLast<to@test.com>\",\"firstName\":\"ToFirst\",\"lastName\":\"ToLast\"}],\"cc\":[],\"bcc\":[]}"
  }
}
```

### Read-Only Properties

These properties are automatically populated by HubSpot from the `hs_email_headers` value:

| Field                  | Description                                  |
|--------------------------|----------------------------------------------|
| `hs_email_from_email`   | Sender's email address.                      |
| `hs_email_from_firstname` | Sender's first name.                         |
| `hs_email_from_lastname`  | Sender's last name.                          |
| `hs_email_to_email`     | Recipient's email address(es).                |
| `hs_email_to_firstname`  | Recipient's first name(s).                   |
| `hs_email_to_lastname`   | Recipient's last name(s).                    |


**Note:** Differences between `From` and `Sender` headers are explained in the original document.

### Set Email Headers

The `hs_email_headers` property uses a JSON escaped string with the following structure:

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

### Associations

To associate an email with records, include an `associations` object in the request body:


**Associations Object:**

| Field             | Description                                                                    |
|----------------------|--------------------------------------------------------------------------------|
| `to`               | Record ID to associate with.                                                   |
| `types`            | Association type: `associationCategory` (e.g., `HUBSPOT_DEFINED`) and `associationTypeId`.  See default IDs or use the associations API for custom types. |


**Example:**

```json
{
  "to": { "id": 601 },
  "types": [ { "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 210 } ]
}
```

### Retrieve Emails

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/emails/{emailId}` (for individual emails) or `/crm/v3/objects/emails` (for all emails).

**Parameters:**  `properties` (comma-separated list), `associations` (comma-separated list of object types), `limit` (for bulk retrieval).


### Update Emails

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/emails/{emailId}`

**Request Body:**  Include the properties to update.  Read-only and non-existent properties are ignored.  Use an empty string to clear a property's value.


### Associate Existing Emails with Records

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Fields:** `emailId`, `toObjectType`, `toObjectId`, `associationTypeId`


### Remove an Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


### Pin an Email on a Record

To pin an email to a record's timeline, use the `hs_pinned_engagement_id` field when creating or updating the record via the relevant object APIs (companies, contacts, deals, tickets, custom objects).


### Delete Emails

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/emails/{emailId}`  (for individual emails)


This markdown provides a comprehensive overview of the HubSpot Email Engagement API. Remember to consult the HubSpot developer documentation and "Endpoints" tab for the most up-to-date information and detailed specifications.
