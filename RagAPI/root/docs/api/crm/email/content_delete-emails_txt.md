# HubSpot Email Engagement API Documentation

This document details the HubSpot Email Engagement API, allowing you to log and manage emails associated with CRM records.  You can interact with emails either directly within HubSpot or through this API.

##  API Endpoints and Methods

The primary endpoint for email engagement is `/crm/v3/objects/emails`.  The following methods are supported:

* **POST `/crm/v3/objects/emails`**: Create a new email engagement.
* **GET `/crm/v3/objects/emails/{emailId}`**: Retrieve a single email by its ID.
* **GET `/crm/v3/objects/emails`**: Retrieve a list of emails.
* **PATCH `/crm/v3/objects/emails/{emailId}`**: Update an existing email.
* **PUT `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`**: Associate an existing email with a record.
* **DELETE `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`**: Remove an association between an email and a record.
* **DELETE `/crm/v3/objects/emails/{emailId}`**: Delete an email.


## Creating an Email Engagement (POST)

To create an email engagement, send a `POST` request to `/crm/v3/objects/emails`. The request body should include a `properties` object and optionally an `associations` object.

### Properties Object

The `properties` object contains details about the email.  Required fields are marked with an asterisk (*).

| Field                  | Description                                                                                                        |
|------------------------|--------------------------------------------------------------------------------------------------------------------|
| `hs_timestamp`*        | Timestamp of email creation (Unix timestamp in milliseconds or UTC format).                                      |
| `hubspot_owner_id`     | ID of the user associated with the email (determines the email creator on the record timeline).                     |
| `hs_email_direction`   | Direction of the email (`EMAIL`, `INCOMING_EMAIL`, `FORWARDED_EMAIL`).                                          |
| `hs_email_html`        | HTML body of the email (sent from a CRM record).                                                                  |
| `hs_email_status`      | Send status of the email (`BOUNCED`, `FAILED`, `SCHEDULED`, `SENDING`, `SENT`).                                 |
| `hs_email_subject`     | Subject line of the email.                                                                                       |
| `hs_email_text`        | Plain text body of the email.                                                                                    |
| `hs_attachment_ids`    | IDs of email attachments (multiple IDs separated by semicolons).                                                |
| `hs_email_headers`     | JSON escaped string containing email headers (used to populate read-only properties; see below for format). |


### Read-Only Properties

These properties are automatically populated by HubSpot from the `hs_email_headers` value:

| Field                     | Description                                         |
|--------------------------|-----------------------------------------------------|
| `hs_email_from_email`     | Sender's email address.                              |
| `hs_email_from_firstname` | Sender's first name.                                |
| `hs_email_from_lastname`  | Sender's last name.                                 |
| `hs_email_to_email`      | Recipient's email address(es).                        |
| `hs_email_to_firstname`   | Recipient's first name(s).                           |
| `hs_email_to_lastname`   | Recipient's last name(s).                            |


**Note:**  The `From` and `Sender` headers may differ, especially when using email aliases.


### Setting Email Headers

The `hs_email_headers` property is a JSON escaped string with the following structure:

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

| Field      | Description                                                              |
|------------|--------------------------------------------------------------------------|
| `to`       | Record ID to associate with.                                              |
| `types`    | Association type (`associationCategory` and `associationTypeId`).         |


## Retrieving Emails (GET)

Retrieve individual emails using `GET /crm/v3/objects/emails/{emailId}` or a list of emails using `GET /crm/v3/objects/emails`.  Both support parameters like `properties` (comma-separated list of properties) and `associations` (comma-separated list of object types for associated IDs).


## Updating Emails (PATCH)

Update emails using `PATCH /crm/v3/objects/emails/{emailId}`.  The request body contains the properties to update.  HubSpot ignores read-only and non-existent properties.  To clear a property, use an empty string.


## Associating Existing Emails (PUT)

Associate an email with a record using `PUT /crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`.


## Removing Associations (DELETE)

Remove an association using `DELETE /crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`.


## Pinning Emails

Pin an email to a record's timeline using the `hs_pinned_engagement_id` field when creating or updating the record via other HubSpot object APIs (contacts, deals, etc.).


## Deleting Emails (DELETE)

Delete emails using `DELETE /crm/v3/objects/emails/{emailId}`.  Deletion is permanent.


## Batch Operations

The documentation mentions that batch operations are available for creating, retrieving, updating, and deleting emails.  Refer to the "Endpoints" tab within the HubSpot documentation for more details on these batch methods.
