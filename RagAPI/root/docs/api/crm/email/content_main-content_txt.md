# HubSpot Email Engagement API Documentation

This document details the HubSpot Email Engagement API, allowing developers to log and manage emails associated with CRM records.  Email activities can be logged directly within HubSpot or via this API.

## API Endpoint: `/crm/v3/objects/emails`

This endpoint provides methods for creating, retrieving, updating, and deleting email engagements.  For batch operations, refer to the "Endpoints" tab within the HubSpot documentation.

### Create an Email (POST)

**Endpoint:** `/crm/v3/objects/emails`

**Request Body:**  The request body should contain a `properties` object with email details and an optional `associations` object to link the email to existing records (e.g., contacts, companies).

#### Properties Object

| Field               | Description                                                                                                                            | Required | Data Type |
|-----------------------|-----------------------------------------------------------------------------------------------------------------------------------------|----------|------------|
| `hs_timestamp`       | Required. Email creation timestamp. Use Unix timestamp (milliseconds) or UTC format (e.g., "2024-07-26T12:00:00Z").                   | Yes      | String     |
| `hubspot_owner_id`   | ID of the email owner (user). Determines the creator listed on the record timeline.                                                  | No       | String     |
| `hs_email_direction` | Email direction (`EMAIL`, `INCOMING_EMAIL`, `FORWARDED_EMAIL`).                                                                        | No       | String     |
| `hs_email_html`      | Email body (HTML) if sent from a CRM record.                                                                                         | No       | String     |
| `hs_email_status`    | Send status (`BOUNCED`, `FAILED`, `SCHEDULED`, `SENDING`, `SENT`).                                                                    | No       | String     |
| `hs_email_subject`   | Email subject line.                                                                                                                  | No       | String     |
| `hs_email_text`      | Email body (plain text).                                                                                                              | No       | String     |
| `hs_attachment_ids`  | IDs of attached files (semicolon-separated).                                                                                         | No       | String     |
| `hs_email_headers`   | JSON escaped string containing email headers.  This populates read-only properties. See "Set Email Headers" section for details. | No       | String     |


#### Read-Only Properties

These properties are automatically populated from `hs_email_headers`:

| Field                  | Description                                       |
|--------------------------|---------------------------------------------------|
| `hs_email_from_email`   | Sender's email address.                           |
| `hs_email_from_firstname` | Sender's first name.                              |
| `hs_email_from_lastname`  | Sender's last name.                               |
| `hs_email_to_email`     | Recipient(s)' email address(es).                   |
| `hs_email_to_firstname`  | Recipient(s)' first name(s).                      |
| `hs_email_to_lastname`   | Recipient(s)' last name(s).                       |


**Note:**  `From` and `Sender` headers may differ. `Sender` identifies the actual submission source.


#### Set Email Headers

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
      "email": "ToFirst ToLast <to@test.com>",
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

| Field             | Description                                                                                             |
|---------------------|---------------------------------------------------------------------------------------------------------|
| `to`               | Object containing the `id` of the record to associate.                                                |
| `types`            | Array of association types. Each object contains `associationCategory` ("HUBSPOT_DEFINED") and `associationTypeId`. |


### Retrieve Emails (GET)

**Endpoint:** `/crm/v3/objects/emails/{emailId}` (individual) or `/crm/v3/objects/emails` (list)

**Parameters:**

* `properties`: Comma-separated list of properties to return.
* `associations`: Comma-separated list of object types to retrieve associated IDs for.
* `limit`: (For list requests) Maximum results per page.


### Update Emails (PATCH)

**Endpoint:** `/crm/v3/objects/emails/{emailId}`

**Request Body:**  Contains the `properties` object with fields to update.  HubSpot ignores read-only and non-existent properties.  Use an empty string to clear a property value.


### Associate Existing Emails with Records (PUT)

**Endpoint:** `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

**Path Parameters:**

* `emailId`: Email ID.
* `toObjectType`: Object type (e.g., "contact", "company").
* `toObjectId`: Object ID.
* `associationTypeId`: Association type ID (obtainable via the associations API).


### Remove an Association (DELETE)

**Endpoint:** `/crm/v3/objects/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}` (Same as PUT)


### Pin an Email (Update Record)

Pinning an email keeps it at the top of a record's timeline.  This is done by including the email's `id` in the `hs_pinned_engagement_id` field when creating or updating a record using object APIs (contacts, companies, deals, tickets, custom objects).


### Delete Emails (DELETE)

**Endpoint:** `/crm/v3/objects/emails/{emailId}`

Email deletion is permanent.


This markdown documentation provides a comprehensive overview of the HubSpot Email Engagement API.  Remember to consult the official HubSpot API documentation for the most up-to-date information and details on error handling.
