# HubSpot Email Engagement API Documentation

This document details the HubSpot Email Engagement API, allowing you to log and manage emails associated with CRM records.  You can interact with emails either directly within HubSpot or through this API.

## Email Endpoint Reference

The primary endpoint for managing emails is `/crm/v3/objects/emails`.  This endpoint supports various HTTP methods for creating, retrieving, updating, and deleting email engagements.  For bulk operations, refer to the "Endpoints" tab within the HubSpot documentation (link not provided in the source text).

### Create an Email (`POST /crm/v3/objects/emails`)

To create a new email engagement, send a `POST` request to `/crm/v3/objects/emails` with the following JSON in the request body:

**Request Body:**

The request body must contain a `properties` object, and optionally an `associations` object.

#### Properties Object

| Field                | Description                                                                                                         | Required | Data Type |
|-----------------------|---------------------------------------------------------------------------------------------------------------------|----------|------------|
| `hs_timestamp`        | Required. Email creation timestamp (Unix timestamp in milliseconds or UTC format).                                  | Yes      | String     |
| `hubspot_owner_id`    | ID of the email's owner (determines the creator listed on the record timeline).                                    | No       | String     |
| `hs_email_direction` | Email direction (`EMAIL`, `INCOMING_EMAIL`, `FORWARDED_EMAIL`).                                                    | No       | String     |
| `hs_email_html`       | Body of the email (if sent from a CRM record).                                                                    | No       | String     |
| `hs_email_status`     | Send status (`BOUNCED`, `FAILED`, `SCHEDULED`, `SENDING`, `SENT`).                                               | No       | String     |
| `hs_email_subject`    | Email subject line.                                                                                             | No       | String     |
| `hs_email_text`       | Email body.                                                                                                      | No       | String     |
| `hs_attachment_ids`   | IDs of attached files (multiple IDs separated by semicolons).                                                     | No       | String     |
| `hs_email_headers`    | JSON escaped string containing email headers (used to populate read-only properties). See "Set Email Headers" below. | No       | String     |


#### Associations Object

This object allows you to associate the email with existing records (e.g., contacts, deals).  The object is an array of association objects, each with:

| Field       | Description                                                                |
|-------------|----------------------------------------------------------------------------|
| `to`        | Object with an `id` field specifying the record ID.                        |
| `types`     | Array of association types, each with `associationCategory` and `associationTypeId`. |


#### Example Request Body (with Associations):

```json
{
  "properties": {
    "hs_timestamp": "2019-10-30T03:30:17.883Z",
    "hubspot_owner_id": "11349275740",
    "hs_email_direction": "EMAIL",
    "hs_email_status": "SENT",
    "hs_email_subject": "Let's talk",
    "hs_email_text": "Thanks for your interest let's find a time to connect"
  },
  "associations": [
    {
      "to": {"id": 601},
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 210}]
    },
    {
      "to": {"id": 602},
      "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 198}]
    }
  ]
}
```


### Read-Only Properties

These properties are automatically populated by HubSpot based on the `hs_email_headers` value:

| Field                   | Description                               |
|--------------------------|-------------------------------------------|
| `hs_email_from_email`    | Sender's email address.                   |
| `hs_email_from_firstname` | Sender's first name.                      |
| `hs_email_from_lastname`  | Sender's last name.                       |
| `hs_email_to_email`      | Recipient's email addresses.              |
| `hs_email_to_firstname`  | Recipients' first names.                 |
| `hs_email_to_lastname`   | Recipients' last names.                  |


**Note:** Differences between `From` and `Sender` headers are explained in the source document.


### Set Email Headers

To set the `hs_email_headers` property, use a JSON escaped string with the following structure:

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


### Retrieve Emails (`GET /crm/v3/objects/emails/{emailId}` or `GET /crm/v3/objects/emails`)

* **Individual Email:**  Use a `GET` request to `/crm/v3/objects/emails/{emailId}`.  You can specify `properties` and `associations` parameters in the query string.
* **All Emails:** Use a `GET` request to `/crm/v3/objects/emails`.  You can use `limit` and `properties` parameters.


### Update Emails (`PATCH /crm/v3/objects/emails/{emailId}`)

Send a `PATCH` request to `/crm/v3/objects/emails/{emailId}` with the properties you want to update.  Read-only properties are ignored.  An empty string clears a property value.


### Associate Existing Emails with Records (`PUT /crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Associates an email with a record.  The URL includes the email ID, object type, object ID, and association type ID.


### Remove an Association (`DELETE /crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`)

Removes an association using the same URL structure as above.


### Pin an Email on a Record

To pin an email to a record's timeline, include the email's ID in the `hs_pinned_engagement_id` field when creating or updating the record via other HubSpot object APIs (companies, contacts, deals, tickets, custom objects).


### Delete Emails (`DELETE /crm/v3/objects/emails/{emailId}`)

Permanently deletes an email.  Deletion is irreversible.


This documentation provides a summary of the HubSpot Email Engagement API.  Consult the official HubSpot API documentation for complete details and the most up-to-date information.
