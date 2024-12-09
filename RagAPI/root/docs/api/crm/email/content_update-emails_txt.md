# HubSpot Email Engagement API Documentation

This document details the HubSpot Email Engagement API, allowing developers to log and manage emails associated with CRM records.  You can manage emails directly within HubSpot or via this API.

## Email Endpoint Reference

The API uses the `/crm/v3/objects/emails` endpoint for various operations.

### Create an Email

**Method:** `POST`

**Endpoint:** `/crm/v3/objects/emails`

**Request Body:**  The request body includes a `properties` object containing email details and an optional `associations` object to link the email to existing records (e.g., contacts, companies).

#### Properties Object

| Field                | Description                                                                                                                                     | Required | Data Type    |
|-----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|----------|---------------|
| `hs_timestamp`       | Required. Email creation timestamp. Use Unix timestamp (milliseconds) or UTC format (e.g., "2024-10-26T10:00:00Z").                             | Yes      | String/Number |
| `hubspot_owner_id`   | ID of the email owner (user). Determines the creator listed in the record timeline.                                                             | No       | String        |
| `hs_email_direction` | Email direction: `EMAIL`, `INCOMING_EMAIL`, `FORWARDED_EMAIL`.                                                                               | No       | String        |
| `hs_email_html`      | Email body (HTML) if sent from a CRM record.                                                                                                    | No       | String        |
| `hs_email_status`    | Email send status: `BOUNCED`, `FAILED`, `SCHEDULED`, `SENDING`, `SENT`.                                                                         | No       | String        |
| `hs_email_subject`   | Email subject line.                                                                                                                            | No       | String        |
| `hs_email_text`      | Email body (plain text).                                                                                                                          | No       | String        |
| `hs_attachment_ids`  | IDs of email attachments (semicolon-separated).                                                                                                 | No       | String        |
| `hs_email_headers`   | Email headers (JSON escaped string).  Automatically populates read-only properties. See "Set Email Headers" section for formatting.             | No       | String        |


#### Associations Object

The `associations` object allows associating the email with multiple records.  Each association requires a `to` object specifying the record ID and a `types` array defining the association type.

| Field             | Description                                                                                                        |
|--------------------|--------------------------------------------------------------------------------------------------------------------|
| `to.id`           | ID of the record to associate (e.g., contact ID, deal ID).                                                        |
| `types[].associationCategory` | Association category (e.g., `HUBSPOT_DEFINED`).                                                              |
| `types[].associationTypeId`  | Association type ID.  Use default IDs or retrieve custom IDs via the Associations API.  See [link to associations API](placeholder) |


#### Example Request Body (with associations):

```json
{
  "properties": {
    "hs_timestamp": "1698326400000",
    "hubspot_owner_id": "12345",
    "hs_email_direction": "EMAIL",
    "hs_email_status": "SENT",
    "hs_email_subject": "Test Email",
    "hs_email_text": "This is a test email."
  },
  "associations": [
    {
      "to": { "id": 601 },
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 210 }]
    }
  ]
}
```


### Read-Only Properties

These properties are automatically populated from `hs_email_headers`.

| Field                     | Description                                    |
|--------------------------|------------------------------------------------|
| `hs_email_from_email`     | Sender's email address.                         |
| `hs_email_from_firstname` | Sender's first name.                            |
| `hs_email_from_lastname`  | Sender's last name.                             |
| `hs_email_to_email`       | Recipient email addresses (comma-separated).      |
| `hs_email_to_firstname`   | Recipients' first names (comma-separated).       |
| `hs_email_to_lastname`    | Recipients' last names (comma-separated).        |


**Note:**  Differences between `From` and `Sender` headers are explained in the original document.


### Set Email Headers

To set `hs_email_headers`, use a JSON escaped string with the following structure:

```json
{
  "from": { "email": "from@domain.com", "firstName": "FromFirst", "lastName": "FromLast" },
  "to": [ { "email": "to@domain.com", "firstName": "ToFirst", "lastName": "ToLast" } ],
  "cc": [],
  "bcc": []
}
```


### Retrieve Emails

**Method:** `GET`

**Endpoint:** `/crm/v3/objects/emails` (for all emails) or `/crm/v3/objects/emails/{emailId}` (for a single email)

**Parameters:**  `properties` (comma-separated list of properties), `associations` (comma-separated list of object types for associated IDs), `limit` (max results per page).


### Update Emails

**Method:** `PATCH`

**Endpoint:** `/crm/v3/objects/emails/{emailId}`

**Request Body:**  Include only the properties to update.  Read-only properties are ignored.  An empty string clears a property value.


### Associate Existing Emails with Records

**Method:** `PUT`

**Endpoint:** `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Parameters:** `emailId`, `toObjectType` (e.g., `contact`, `company`), `toObjectId`, `associationTypeId`.


### Remove an Association

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`


### Pin an Email on a Record

Use the `hs_pinned_engagement_id` field when creating or updating records via object APIs (companies, contacts, deals, tickets, custom objects).


### Delete Emails

**Method:** `DELETE`

**Endpoint:** `/crm/v3/objects/emails/{emailId}`


This markdown documentation provides a structured overview of the HubSpot Email Engagement API. Remember to consult the official HubSpot Developer documentation for the most up-to-date information and details on error handling, authentication, and rate limits.
